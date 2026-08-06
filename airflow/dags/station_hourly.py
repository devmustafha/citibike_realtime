from datetime import datetime

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from utils.spark import spark_command


@dag(
    dag_id="station_hourly_metrics",
    description="Generate station hourly snapshot",
    start_date=datetime(2026, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    tags=["gold", "citibike"],
)
def station_hourly_dag():
    BashOperator(
        task_id="station_hourly", bash_command=spark_command("station_hourly_metrics")
    )


station_hourly_dag()
