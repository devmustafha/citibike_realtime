from common import create_spark_session


def main() -> None:
    spark = create_spark_session()

    print(f"Spark version: {spark.version}")

    spark.stop()


if __name__ == "__main__":
    main()
