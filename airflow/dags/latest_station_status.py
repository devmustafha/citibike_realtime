from datetime import datetime, timedelta

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from utils.callbacks import notify_telegram_failure
from utils.spark import spark_command


@dag(
    dag_id="latest_station_status",
    description="Generate the latest station status snapshot",
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
def latest_station_status_pipeline():

    latest_station_status = BashOperator(
        task_id="latest_station_status",
        bash_command=spark_command("latest_station_status"),
    )

    system_metrics = BashOperator(
        task_id="system_metrics", bash_command=spark_command("system_metrics")
    )

    latest_station_status >> system_metrics


latest_station_status_pipeline()
