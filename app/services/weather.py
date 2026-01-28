import httpx


async def fetch_temperature(city_name: str) -> float | None:
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "current_weather": "true",
        "timezone": "UTC",
    }

    async with httpx.AsyncClient() as client:
        geo_resp = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name, "count": 1},
            timeout=10,
        )
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data.get("results"):
            return None

        location = geo_data["results"][0]

        weather_resp = await client.get(
            url,
            params={
                **params,
                "latitude": location["latitude"],
                "longitude": location["longitude"],
            },
            timeout=10,
        )
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()

        return weather_data["current_weather"]["temperature"]
