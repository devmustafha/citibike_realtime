from producer.client import CitiBikeClient


def main():
    print("Hello from citibike-realtime!")
    client = CitiBikeClient()

    data = client.fetch_station_status()
    print(data.keys())

    client.close()


if __name__ == "__main__":
    main()
