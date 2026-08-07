import pytest
from pyspark.sql import SparkSession

from common.config import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder.master("local[2]").appName("citibike-tests").getOrCreate()
    )

    yield spark

    spark.stop()
