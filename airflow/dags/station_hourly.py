from datetime import datetime, timedelta

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from utils.callbacks import notify_telegram_failure
from utils.spark import spark_command


@dag(
    dag_id="station_hourly_metrics",
    description="Generate station hourly snapshot",
    start_date=datetime(2026, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=20),
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
        "on_failure_callback": notify_telegram_failure,
    },
    tags=["gold", "citibike"],
)
def station_hourly_dag():
    BashOperator(
        task_id="station_hourly",
        bash_command=spark_command(
            "station_hourly_metrics", "{{ logical_date.strftime('%Y-%m-%d') }}"
        ),
    )


station_hourly_dag()
