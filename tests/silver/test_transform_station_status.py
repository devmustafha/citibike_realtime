from spark.apps.silver.station_status.transform import transform_station_status


def test_transform_removes_null_station_id(spark):
    df = spark.createDataFrame(
        [
            ("123", 1720000000),
            (None, 1720000000),
        ],
        ["station_id", "last_reported"],
    )

    result = transform_station_status(df)

    assert result.count() == 1
    assert result.first().station_id == "123"


def test_transform_removes_null_last_reported(spark):
    df = spark.createDataFrame(
        [
            ("123", 1720000000),
            ("456", None),
        ],
        ["station_id", "last_reported"],
    )

    result = transform_station_status(df)

    assert result.count() == 1
    assert result.first().station_id == "123"


def test_transform_creates_correct_partition_values(spark):
    df = spark.createDataFrame(
        [
            ("123", 1720000000),
        ],
        ["station_id", "last_reported"],
    )

    result = transform_station_status(df)

    row = result.select(
        "year",
        "month",
        "day",
    ).first()

    assert row.year == 2024
    assert row.month == 7
    assert row.day == 3
