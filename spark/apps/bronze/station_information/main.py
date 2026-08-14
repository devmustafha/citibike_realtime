from common.io import write_bucket
from common.session import create_spark_session
from common.storage import BRONZE_STATION_INFORMATION_PATH

from producer.client import CitiBikeClient


def load_stations_information_data() -> None:
    try:
        spark = create_spark_session("station-information")
        client = CitiBikeClient()
        station_information = client.get_station_information()
        station_information_df = spark.createDataFrame(station_information)
        print("hello", station_information_df.show(5))
        write_bucket(station_information_df, BRONZE_STATION_INFORMATION_PATH)

        spark.stop()
    finally:
        pass


if __name__ == "__main__":
    load_stations_information_data()
