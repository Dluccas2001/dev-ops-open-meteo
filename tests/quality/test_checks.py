from pathlib import Path

import pandera.errors
import pytest

from src.jobs import transform
from src.quality import checks


def test_validate_processed_sample() -> None:
    raw_files = [Path("data/samples/open_meteo/sao-paulo/2026-07-19.json")]
    hourly = transform.build_hourly_dataset(raw_files)
    daily = transform.build_daily_dataset(hourly)

    checks.validate_hourly(hourly)
    checks.validate_daily(daily)


def test_validate_hourly_rejects_invalid_temperature() -> None:
    raw_files = [Path("data/samples/open_meteo/sao-paulo/2026-07-19.json")]
    hourly = transform.build_hourly_dataset(raw_files)
    hourly.loc[0, "temperature_2m"] = 80.0

    with pytest.raises(pandera.errors.SchemaError):
        checks.validate_hourly(hourly)


def test_run_quality_checks_from_parquets(tmp_path) -> None:
    transform.run_transform(raw_dir="data/samples", processed_dir=tmp_path)

    checks.run_quality_checks(tmp_path)
