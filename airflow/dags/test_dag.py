from datetime import datetime

from airflow.operators.empty import EmptyOperator

from airflow import DAG

with DAG(
    dag_id="test_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
):
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    start >> end
