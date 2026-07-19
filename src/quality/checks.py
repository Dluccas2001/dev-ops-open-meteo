from pathlib import Path

import pandas as pd
import pandera as pa
from pandera import Check, Column, DataFrameSchema

from src.config import settings

HOURLY_SCHEMA = DataFrameSchema(
    {
        "city": Column(str, nullable=False),
        "uf": Column(str, nullable=False),
        "region": Column(str, nullable=False),
        "datetime": Column(pa.DateTime, nullable=False),
        "temperature_2m": Column(float, Check.in_range(-20, 55), nullable=False),
        "relative_humidity_2m": Column(float, Check.in_range(0, 100), nullable=False),
        "precipitation": Column(float, Check.ge(0), nullable=False),
        "wind_speed_10m": Column(float, Check.ge(0), nullable=False),
        "ingested_at": Column(pa.DateTime, nullable=False),
    },
    checks=[
        Check(lambda frame: len(frame) >= 1, error="Hourly dataset must have at least one row"),
        Check(
            lambda frame: not frame.duplicated(subset=["city", "datetime"]).any(),
            error="Hourly dataset must be unique by city and datetime",
        ),
    ],
    strict=True,
)

DAILY_SCHEMA = DataFrameSchema(
    {
        "city": Column(str, nullable=False),
        "uf": Column(str, nullable=False),
        "region": Column(str, nullable=False),
        "date": Column(pa.Date, nullable=False),
        "temp_min": Column(float, Check.in_range(-20, 55), nullable=False),
        "temp_max": Column(float, Check.in_range(-20, 55), nullable=False),
        "temp_mean": Column(float, Check.in_range(-20, 55), nullable=False),
        "humidity_mean": Column(float, Check.in_range(0, 100), nullable=False),
        "rain_sum": Column(float, Check.ge(0), nullable=False),
        "wind_mean": Column(float, Check.ge(0), nullable=False),
        "will_rain": Column(bool, nullable=False),
    },
    checks=[
        Check(lambda frame: len(frame) >= 1, error="Daily dataset must have at least one row"),
        Check(
            lambda frame: not frame.duplicated(subset=["city", "date"]).any(),
            error="Daily dataset must be unique by city and date",
        ),
        Check(
            lambda frame: (frame["temp_min"] <= frame["temp_mean"]).all()
            and (frame["temp_mean"] <= frame["temp_max"]).all(),
            error="Daily temperature aggregates must be ordered",
        ),
    ],
    strict=True,
)


def validate_hourly(hourly: pd.DataFrame) -> pd.DataFrame:
    return HOURLY_SCHEMA.validate(hourly)


def validate_daily(daily: pd.DataFrame) -> pd.DataFrame:
    return DAILY_SCHEMA.validate(daily)


def load_processed_datasets(
    processed_dir: str | Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    base_dir = Path(processed_dir or settings.data_processed_dir)
    hourly_path = base_dir / "weather_hourly.parquet"
    daily_path = base_dir / "weather_daily.parquet"

    if not hourly_path.exists():
        raise FileNotFoundError(f"Hourly dataset not found: {hourly_path}")
    if not daily_path.exists():
        raise FileNotFoundError(f"Daily dataset not found: {daily_path}")

    return pd.read_parquet(hourly_path), pd.read_parquet(daily_path)


def run_quality_checks(processed_dir: str | Path | None = None) -> None:
    hourly, daily = load_processed_datasets(processed_dir)
    validate_hourly(hourly)
    validate_daily(daily)


def main() -> None:
    run_quality_checks()
    print("Data quality checks passed for processed weather datasets.")


if __name__ == "__main__":
    main()
