from producer.client import CitiBikeClient


def main():
    print("Hello from citibike-realtime!")
    client = CitiBikeClient()

    response = client.fetch_station_status()

    print(f"Stations: {len(response.data.stations)}")

    first_station = response.data.stations[0]

    print(first_station.station_id)
    print(first_station.num_bikes_available)

    client.close()


if __name__ == "__main__":
    main()
