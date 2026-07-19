from pathlib import Path

from sqlalchemy import create_engine

from src.data import weather_repository
from src.jobs import load, transform


def test_load_dataframes_and_query_with_sqlite(tmp_path) -> None:
    raw_files = [Path("data/samples/open_meteo/sao-paulo/2026-07-19.json")]
    hourly = transform.build_hourly_dataset(raw_files)
    daily = transform.build_daily_dataset(hourly)
    engine = create_engine(f"sqlite:///{tmp_path / 'weather.db'}")

    load.load_dataframes(hourly, daily, engine)

    cities = weather_repository.fetch_cities(engine)
    latest = weather_repository.fetch_latest_weather("sao-paulo", engine)
    daily_rows = weather_repository.fetch_daily_weather("sao-paulo", engine=engine)
    summary = weather_repository.fetch_weather_summary(engine)

    assert cities == [{"city": "sao-paulo", "uf": "SP", "region": "Sudeste"}]
    assert latest is not None
    assert latest["city"] == "sao-paulo"
    assert len(daily_rows) == 2
    assert summary == {
        "cities": 1,
        "days": 2,
        "rainy_days": 1,
        "avg_temp_mean": 20.0,
    }
