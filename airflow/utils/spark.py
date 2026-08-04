def spark_command(job_name: str) -> str:
    return f"/opt/airflow/scripts/run_spark_job.sh {job_name}"
