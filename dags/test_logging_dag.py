from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging

def log_message(task_name, **kwargs):
    logger = logging.getLogger("airflow.task")

    now = datetime.utcnow().isoformat()
    logger.info(f"[{task_name}] Log generated at: {now}")
    logger.warning(f"[{task_name}] Warning event at: {now}")
    logger.error(f"[{task_name}] Error event at: {now}")

    for handler in logger.handlers:
        print("Handler found:", handler)


with DAG(
    dag_id="test_logging_dag",
    description="Simple DAG for testing logs sent to OpenSearch",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["test", "logging"],
) as dag:

    task_a = PythonOperator(
        task_id="log_task_a",
        python_callable=log_message,
        op_kwargs={"task_name": "Task A"},
        provide_context=True,
    )

    task_b = PythonOperator(
        task_id="log_task_b",
        python_callable=log_message,
        op_kwargs={"task_name": "Task B"},
        provide_context=True,
    )

    task_c = PythonOperator(
        task_id="log_task_c",
        python_callable=log_message,
        op_kwargs={"task_name": "Task C"},
        provide_context=True,
    )

    task_a >> task_b >> task_c
