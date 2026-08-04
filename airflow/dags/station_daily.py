from datetime import datetime

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from utils.spark import spark_command


@dag(
    dag_id="station_daily_metrics",
    description="Generate station daily snapshot",
    start_date=datetime(2026, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    tags=["gold", "citibike"],
)
def station_daily_dag():
    station_daily = BashOperator(
        task_id="station_daily_metric",
        bash_command=spark_command("station_daily_metrics"),
    )


station_daily_dag()
