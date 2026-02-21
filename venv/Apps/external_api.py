import json
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

AREA_CONFIG = {
    "tokyo": {"name": "東京", "latitude": 35.6762, "longitude": 139.6503},
    "osaka": {"name": "大阪", "latitude": 34.6937, "longitude": 135.5023},
    "nagoya": {"name": "名古屋", "latitude": 35.1815, "longitude": 136.9066},
    "hokkaido": {"name": "北海道", "latitude": 43.0618, "longitude": 141.3545},
}


class ExternalAPIError(Exception):
    """Raised when the external API request fails."""


def fetch_latest_pollen(area_key: str) -> dict:
    area = AREA_CONFIG.get(area_key)
    if area is None:
        raise ValueError(f"Unsupported area_key: {area_key}")

    params = urlencode(
        {
            "latitude": area["latitude"],
            "longitude": area["longitude"],
            "daily": "alder_pollen",
            "timezone": "Asia/Tokyo",
            "forecast_days": 1,
        }
    )
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?{params}"

    try:
        with urlopen(url, timeout=10) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise ExternalAPIError("Failed to fetch data from Open-Meteo") from exc

    pollen_values = payload.get("daily", {}).get("alder_pollen", [])
    dates = payload.get("daily", {}).get("time", [])
    pollen_value = int(pollen_values[0]) if pollen_values and pollen_values[0] is not None else 0
    observed_date = dates[0] if dates else date.today().isoformat()

    return {
        "area_key": area_key,
        "area_name": area["name"],
        "date": observed_date,
        "pollen": pollen_value,
    }
