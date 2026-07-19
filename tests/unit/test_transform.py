from pathlib import Path

import pandas as pd

from src.jobs import transform


def test_build_hourly_dataset_from_raw_sample() -> None:
    raw_files = [Path("data/samples/open_meteo/sao-paulo/2026-07-19.json")]

    hourly = transform.build_hourly_dataset(raw_files)

    assert list(hourly.columns) == transform.HOURLY_COLUMNS
    assert len(hourly) == 4
    assert hourly["city"].unique().tolist() == ["sao-paulo"]
    assert pd.api.types.is_datetime64_any_dtype(hourly["datetime"])
    assert hourly["temperature_2m"].tolist() == [18.0, 20.0, 19.0, 23.0]


def test_build_daily_dataset_from_hourly_sample() -> None:
    raw_files = [Path("data/samples/open_meteo/sao-paulo/2026-07-19.json")]
    hourly = transform.build_hourly_dataset(raw_files)

    daily = transform.build_daily_dataset(hourly)

    assert list(daily.columns) == transform.DAILY_COLUMNS
    assert len(daily) == 2
    first_day = daily.iloc[0]
    assert first_day["city"] == "sao-paulo"
    assert first_day["temp_min"] == 18.0
    assert first_day["temp_max"] == 20.0
    assert first_day["temp_mean"] == 19.0
    assert first_day["humidity_mean"] == 78.0
    assert first_day["rain_sum"] == 0.4
    assert first_day["wind_mean"] == 9.0
    assert bool(first_day["will_rain"]) is True


def test_run_transform_writes_processed_parquets(tmp_path) -> None:
    hourly_path, daily_path = transform.run_transform(
        raw_dir="data/samples",
        processed_dir=tmp_path,
    )

    assert hourly_path == tmp_path / "weather_hourly.parquet"
    assert daily_path == tmp_path / "weather_daily.parquet"
    assert len(pd.read_parquet(hourly_path)) == 4
    assert len(pd.read_parquet(daily_path)) == 2
