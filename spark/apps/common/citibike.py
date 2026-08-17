import httpx


class CitiBikeClient:
    BASE_URL = "https://gbfs.citibikenyc.com/gbfs/en"

    def get_station_information(self):
        response = httpx.get(
            f"{self.BASE_URL}/station_information.json",
            timeout=30,
        )
        response.raise_for_status()

        return response.json()["data"]["stations"]
