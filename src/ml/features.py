from pathlib import Path

import pandas as pd

from src.config import settings

NUMERIC_FEATURES = [
    "temp_mean",
    "temp_min",
    "temp_max",
    "humidity_mean",
    "wind_mean",
    "rain_sum",
    "month",
    "day_of_week",
]
CATEGORICAL_FEATURES = ["city", "region"]
FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET_COLUMN = "will_rain_tomorrow"


def load_daily_dataset(processed_dir: str | Path | None = None) -> pd.DataFrame:
    base_dir = Path(processed_dir or settings.data_processed_dir)
    daily_path = base_dir / "weather_daily.parquet"
    if not daily_path.exists():
        raise FileNotFoundError(f"Daily dataset not found: {daily_path}")
    return pd.read_parquet(daily_path)


def add_calendar_features(daily: pd.DataFrame) -> pd.DataFrame:
    frame = daily.copy()
    frame["date"] = pd.to_datetime(frame["date"])
    frame["month"] = frame["date"].dt.month
    frame["day_of_week"] = frame["date"].dt.dayofweek
    return frame


def build_training_dataset(daily: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    frame = add_calendar_features(daily)
    frame = frame.sort_values(["city", "date"]).reset_index(drop=True)
    frame["rain_sum_next_day"] = frame.groupby("city")["rain_sum"].shift(-1)
    frame = frame.dropna(subset=["rain_sum_next_day"]).copy()
    frame[TARGET_COLUMN] = frame["rain_sum_next_day"].gt(0)

    if frame.empty:
        raise ValueError("Training dataset is empty after target creation")

    return frame[FEATURE_COLUMNS], frame[TARGET_COLUMN].astype(bool)


def build_prediction_frame(payload: dict) -> pd.DataFrame:
    frame = pd.DataFrame([payload])
    if "region" not in frame:
        frame["region"] = "unknown"
    return frame[FEATURE_COLUMNS]
