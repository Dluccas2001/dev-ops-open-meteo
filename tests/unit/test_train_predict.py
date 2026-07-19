from datetime import date

import pandas as pd

from src.ml import predict, train


def training_daily_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "city": ["sao-paulo"] * 8,
            "uf": ["SP"] * 8,
            "region": ["Sudeste"] * 8,
            "date": [date(2026, 7, day) for day in range(1, 9)],
            "temp_min": [18.0, 19.0, 17.0, 16.0, 18.0, 20.0, 21.0, 19.0],
            "temp_max": [25.0, 26.0, 24.0, 23.0, 25.0, 28.0, 29.0, 27.0],
            "temp_mean": [21.0, 22.0, 20.0, 19.0, 21.5, 24.0, 25.0, 23.0],
            "humidity_mean": [80.0, 75.0, 85.0, 90.0, 70.0, 68.0, 72.0, 74.0],
            "rain_sum": [0.0, 1.2, 0.0, 2.0, 0.0, 0.0, 1.5, 0.0],
            "wind_mean": [8.0, 9.0, 7.0, 6.0, 8.5, 10.0, 11.0, 9.5],
            "will_rain": [False, True, False, True, False, False, True, False],
        }
    )


def test_train_model_saves_artifacts_and_predicts(tmp_path) -> None:
    daily = training_daily_frame()
    processed_dir = tmp_path / "processed"
    model_dir = tmp_path / "models"
    tracking_dir = tmp_path / "mlruns"
    processed_dir.mkdir()
    daily.to_parquet(processed_dir / "weather_daily.parquet", index=False)

    result = train.run_training(
        processed_dir=processed_dir,
        model_dir=model_dir,
        tracking_uri=f"file:{tracking_dir}",
    )

    assert (model_dir / train.MODEL_FILENAME).exists()
    assert (model_dir / train.MODEL_INFO_FILENAME).exists()
    assert result["metrics"]["accuracy"] >= 0.0

    prediction = predict.predict_rain(
        {
            "city": "sao-paulo",
            "region": "Sudeste",
            "temp_mean": 22.0,
            "temp_min": 18.0,
            "temp_max": 26.0,
            "humidity_mean": 75.0,
            "wind_mean": 9.0,
            "rain_sum": 0.0,
            "month": 7,
            "day_of_week": 0,
        },
        model_dir=model_dir,
    )

    assert prediction["city"] == "sao-paulo"
    assert isinstance(prediction["will_rain_tomorrow"], bool)
    assert 0.0 <= prediction["probability"] <= 1.0
