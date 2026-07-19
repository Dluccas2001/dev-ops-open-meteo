import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import settings

HOURLY_COLUMNS = [
    "city",
    "uf",
    "region",
    "datetime",
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
    "ingested_at",
]

DAILY_COLUMNS = [
    "city",
    "uf",
    "region",
    "date",
    "temp_min",
    "temp_max",
    "temp_mean",
    "humidity_mean",
    "rain_sum",
    "wind_mean",
    "will_rain",
]


def find_raw_files(raw_dir: str | Path | None = None) -> list[Path]:
    base_dir = Path(raw_dir or settings.data_raw_dir) / "open_meteo"
    if not base_dir.exists():
        raise FileNotFoundError(f"Raw Open-Meteo directory not found: {base_dir}")

    raw_files = sorted(base_dir.glob("*/*.json"))
    if not raw_files:
        raise FileNotFoundError(f"No raw Open-Meteo JSON files found in {base_dir}")

    return raw_files


def load_raw_payload(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as file:
        return json.load(file)


def raw_payload_to_hourly_frame(payload: dict[str, Any]) -> pd.DataFrame:
    city = payload["city"]
    forecast = payload["forecast"]
    hourly = forecast["hourly"]
    ingested_at = pd.to_datetime(payload["ingested_at"], utc=True).tz_convert(None)

    frame = pd.DataFrame(
        {
            "city": city["slug"],
            "uf": city["uf"],
            "region": city["region"],
            "datetime": pd.to_datetime(hourly["time"]),
            "temperature_2m": pd.to_numeric(hourly["temperature_2m"]),
            "relative_humidity_2m": pd.to_numeric(hourly["relative_humidity_2m"]),
            "precipitation": pd.to_numeric(hourly["precipitation"]),
            "wind_speed_10m": pd.to_numeric(hourly["wind_speed_10m"]),
            "ingested_at": ingested_at,
        }
    )

    return frame[HOURLY_COLUMNS]


def build_hourly_dataset(raw_files: list[Path]) -> pd.DataFrame:
    frames = [raw_payload_to_hourly_frame(load_raw_payload(path)) for path in raw_files]
    hourly = pd.concat(frames, ignore_index=True)
    hourly = hourly.drop_duplicates(subset=["city", "datetime"])
    return hourly.sort_values(["city", "datetime"]).reset_index(drop=True)


def build_daily_dataset(hourly: pd.DataFrame) -> pd.DataFrame:
    daily = (
        hourly.assign(date=hourly["datetime"].dt.date)
        .groupby(["city", "uf", "region", "date"], as_index=False)
        .agg(
            temp_min=("temperature_2m", "min"),
            temp_max=("temperature_2m", "max"),
            temp_mean=("temperature_2m", "mean"),
            humidity_mean=("relative_humidity_2m", "mean"),
            rain_sum=("precipitation", "sum"),
            wind_mean=("wind_speed_10m", "mean"),
        )
    )
    daily["will_rain"] = daily["rain_sum"] > 0
    return daily[DAILY_COLUMNS].sort_values(["city", "date"]).reset_index(drop=True)


def save_processed_datasets(
    hourly: pd.DataFrame,
    daily: pd.DataFrame,
    processed_dir: str | Path | None = None,
) -> tuple[Path, Path]:
    output_dir = Path(processed_dir or settings.data_processed_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    hourly_path = output_dir / "weather_hourly.parquet"
    daily_path = output_dir / "weather_daily.parquet"

    hourly.to_parquet(hourly_path, index=False)
    daily.to_parquet(daily_path, index=False)

    return hourly_path, daily_path


def run_transform(
    raw_dir: str | Path | None = None,
    processed_dir: str | Path | None = None,
) -> tuple[Path, Path]:
    raw_files = find_raw_files(raw_dir)
    hourly = build_hourly_dataset(raw_files)
    daily = build_daily_dataset(hourly)
    return save_processed_datasets(hourly, daily, processed_dir)


def main() -> None:
    hourly_path, daily_path = run_transform()
    print(f"Saved processed hourly dataset: {hourly_path}")
    print(f"Saved processed daily dataset: {daily_path}")


if __name__ == "__main__":
    main()
