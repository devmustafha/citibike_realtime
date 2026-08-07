from datetime import datetime, timedelta

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from utils.spark import spark_command


@dag(
    dag_id="station_daily_metrics",
    description="Generate station daily snapshot",
    start_date=datetime(2026, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["gold", "citibike"],
)
def station_daily_dag():
    BashOperator(
        task_id="station_daily_metric",
        bash_command=spark_command(
            "station_daily_metrics",
            "{{ logical_date.strftime('%Y-%m-%d') }}",
        ),
    )


station_daily_dag()
