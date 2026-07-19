from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Engine

from src.config import settings
from src.data.database import ensure_database_exists, get_engine

HOURLY_TABLE = "weather_hourly"
DAILY_TABLE = "weather_daily"


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


def prepare_daily_for_sql(daily: pd.DataFrame) -> pd.DataFrame:
    prepared = daily.copy()
    prepared["date"] = pd.to_datetime(prepared["date"]).dt.date
    return prepared


def load_dataframes(hourly: pd.DataFrame, daily: pd.DataFrame, engine: Engine) -> None:
    hourly.to_sql(HOURLY_TABLE, engine, if_exists="replace", index=False)
    prepare_daily_for_sql(daily).to_sql(DAILY_TABLE, engine, if_exists="replace", index=False)


def run_load(
    processed_dir: str | Path | None = None,
    database_url: str | None = None,
) -> None:
    ensure_database_exists(database_url)
    engine = get_engine(database_url)
    try:
        hourly, daily = load_processed_datasets(processed_dir)
        load_dataframes(hourly, daily, engine)
    finally:
        engine.dispose()


def main() -> None:
    run_load()
    print(f"Loaded processed datasets into tables: {HOURLY_TABLE}, {DAILY_TABLE}")


if __name__ == "__main__":
    main()
