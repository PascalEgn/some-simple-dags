import shutil
import datetime
import logging
import os
import shutil

from airflow.sdk import dag, task
from airflow.sdk.definitions.param import Param

logger = logging.getLogger("airflow.task")


@dag(
    schedule="0 0 */1 * *",
    catchup=False,
    tags=["service", "log_cleanup"],
    params={
        "retention_days": Param(
            14, type="integer", description="Log retention period in days"
        ),
    }
)
def cleanup_logs():
    @task
    def find_and_cleanup_logs(**context):
        airflow_home = os.getenv("AIRFLOW_HOME", "/opt/airflow")
        logs_dir = os.path.join(airflow_home, "logs")
        retention_days = context["params"].get("retention_days")
        logger.info(
            f"Cleaning up logs older than {retention_days} days in {logs_dir}"
        )
        cutoff_time = datetime.datetime.now(datetime.UTC) - datetime.timedelta(
            days=retention_days
        )

        if not os.path.exists(logs_dir):
            logger.warning(f"Logs directory {logs_dir} does not exist.")
            return

        for dag_id in os.listdir(logs_dir):
            dag_path = os.path.join(logs_dir, dag_id)
            if os.path.isdir(dag_path):
                for run in os.listdir(dag_path):
                    run_path = os.path.join(dag_path, run)
                    if os.path.isdir(run_path) and not os.path.islink(run_path):
                        file_mod_time = datetime.datetime.fromtimestamp(
                            os.path.getmtime(run_path), datetime.UTC
                        )
                        if file_mod_time < cutoff_time:
                            logger.info(f"Deleting log file: {run_path}")
                            try:
                                shutil.rmtree(run_path)
                            except Exception as e:
                                logger.error(f"Failed to delete {run_path}: {e}")
            if not os.listdir(dag_path):
                logger.info(f"Deleting empty log directory: {dag_path}")
                shutil.rmtree(dag_path)
    find_and_cleanup_logs()


cleanup_logs()
