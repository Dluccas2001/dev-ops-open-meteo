import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.config import settings
from src.ml.features import build_prediction_frame
from src.ml.train import MODEL_FILENAME, MODEL_INFO_FILENAME


def model_path(model_dir: str | Path | None = None) -> Path:
    return Path(model_dir or settings.model_dir) / MODEL_FILENAME


def model_info_path(model_dir: str | Path | None = None) -> Path:
    return Path(model_dir or settings.model_dir) / MODEL_INFO_FILENAME


def load_model(model_dir: str | Path | None = None) -> Any:
    path = model_path(model_dir)
    if not path.exists():
        raise FileNotFoundError(f"Model artifact not found: {path}")
    return joblib.load(path)


def load_model_info(model_dir: str | Path | None = None) -> dict[str, Any]:
    path = model_info_path(model_dir)
    if not path.exists():
        raise FileNotFoundError(f"Model info not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def positive_class_probability(model: Any, prediction_frame: pd.DataFrame) -> float:
    if not hasattr(model, "predict_proba"):
        return float(model.predict(prediction_frame)[0])

    probabilities = model.predict_proba(prediction_frame)[0]
    classes = model.named_steps["classifier"].classes_
    if True not in classes:
        return 0.0

    positive_index = list(classes).index(True)
    return float(probabilities[positive_index])


def predict_rain(payload: dict[str, Any], model_dir: str | Path | None = None) -> dict[str, Any]:
    model = load_model(model_dir)
    info = load_model_info(model_dir)
    prediction_frame = build_prediction_frame(payload)
    probability = positive_class_probability(model, prediction_frame)
    will_rain = probability >= 0.5

    return {
        "city": payload["city"],
        "will_rain_tomorrow": will_rain,
        "probability": round(probability, 4),
        "model_version": info.get("model_version", "local"),
    }
