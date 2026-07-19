import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import requests

from src.config import settings
from src.data.cities import City, load_cities

HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
]


def build_forecast_params(city: City) -> dict[str, Any]:
    return {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "hourly": ",".join(HOURLY_VARIABLES),
        "forecast_days": settings.forecast_days,
        "timezone": city.timezone,
    }


def fetch_forecast(city: City, timeout_seconds: int = 30) -> dict[str, Any]:
    response = requests.get(
        settings.open_meteo_base_url,
        params=build_forecast_params(city),
        timeout=timeout_seconds,
    )
    response.raise_for_status()
    return response.json()


def build_raw_payload(
    city: City,
    forecast: dict[str, Any],
    ingested_at: datetime,
) -> dict[str, Any]:
    return {
        "source": "open-meteo",
        "ingested_at": ingested_at.isoformat(),
        "city": {
            "slug": city.slug,
            "name": city.name,
            "uf": city.uf,
            "region": city.region,
            "latitude": city.latitude,
            "longitude": city.longitude,
            "timezone": city.timezone,
        },
        "forecast": forecast,
    }


def save_raw_payload(payload: dict[str, Any], city_slug: str, run_date: date) -> Path:
    output_dir = Path(settings.data_raw_dir) / "open_meteo" / city_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{run_date.isoformat()}.json"
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    return output_path


def ingest_city(city: City, ingested_at: datetime | None = None) -> Path:
    current_ingested_at = ingested_at or datetime.now(UTC)
    forecast = fetch_forecast(city)
    payload = build_raw_payload(city, forecast, current_ingested_at)
    return save_raw_payload(payload, city.slug, current_ingested_at.date())


def run_ingestion() -> list[Path]:
    cities = load_cities()
    output_paths = [ingest_city(city) for city in cities]
    return output_paths


def main() -> None:
    output_paths = run_ingestion()
    for output_path in output_paths:
        print(f"Saved raw Open-Meteo payload: {output_path}")


if __name__ == "__main__":
    main()
