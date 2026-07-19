from datetime import date

import pandas as pd

from src.ml import features


def sample_daily_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "city": ["sao-paulo", "sao-paulo", "sao-paulo"],
            "uf": ["SP", "SP", "SP"],
            "region": ["Sudeste", "Sudeste", "Sudeste"],
            "date": [date(2026, 7, 19), date(2026, 7, 20), date(2026, 7, 21)],
            "temp_min": [18.0, 19.0, 17.0],
            "temp_max": [25.0, 26.0, 24.0],
            "temp_mean": [21.0, 22.0, 20.0],
            "humidity_mean": [80.0, 75.0, 85.0],
            "rain_sum": [0.0, 1.2, 0.0],
            "wind_mean": [8.0, 9.0, 7.0],
            "will_rain": [False, True, False],
        }
    )


def test_build_training_dataset_creates_next_day_target() -> None:
    x, y = features.build_training_dataset(sample_daily_frame())

    assert list(x.columns) == features.FEATURE_COLUMNS
    assert len(x) == 2
    assert y.tolist() == [True, False]
    assert x["month"].tolist() == [7, 7]
    assert x["day_of_week"].tolist() == [6, 0]


def test_build_prediction_frame_adds_unknown_region() -> None:
    frame = features.build_prediction_frame(
        {
            "city": "sao-paulo",
            "temp_mean": 22.0,
            "temp_min": 18.0,
            "temp_max": 26.0,
            "humidity_mean": 75.0,
            "wind_mean": 9.0,
            "rain_sum": 0.0,
            "month": 7,
            "day_of_week": 0,
        }
    )

    assert list(frame.columns) == features.FEATURE_COLUMNS
    assert frame.iloc[0]["region"] == "unknown"
