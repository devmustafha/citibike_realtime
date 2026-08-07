def spark_command(job_name: str, process_date: str | None = None) -> str:
    command = f"/opt/airflow/scripts/run_spark_job.sh {job_name}"
    if process_date:
        command += f" {process_date}"
    return command
