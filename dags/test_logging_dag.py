from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging

logger = logging.getLogger("airflow.task")

def log_message(task_name):
    now = datetime.utcnow().isoformat()
    logger.info(f"[{task_name}] Log generated at: {now}")
    logger.warning(f"[{task_name}] Warning event at: {now}")
    logger.error(f"[{task_name}] Error event at: {now}")
    for handler in logger.handlers:
        if hasattr(handler, "set_context"):
            handler.set_context(task_instance)

with DAG(
    dag_id="test_logging_dag",
    description="Simple DAG for testing logs sent to Elasticsearch",
    schedule="*/5 * * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["test", "logging"],
) as dag:

    task_a = PythonOperator(
        task_id="log_task_a",
        python_callable=log_message,
        op_kwargs={"task_name": "Task A"},
    )

    task_b = PythonOperator(
        task_id="log_task_b",
        python_callable=log_message,
        op_kwargs={"task_name": "Task B"},
    )

    task_c = PythonOperator(
        task_id="log_task_c",
        python_callable=log_message,
        op_kwargs={"task_name": "Task C"},
    )

    task_a >> task_b >> task_c
