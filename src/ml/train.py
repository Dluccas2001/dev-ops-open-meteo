import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import settings
from src.ml.features import (
    CATEGORICAL_FEATURES,
    FEATURE_COLUMNS,
    NUMERIC_FEATURES,
    build_training_dataset,
    load_daily_dataset,
)

MODEL_FILENAME = "rain_model.joblib"
MODEL_INFO_FILENAME = "model_info.json"


def build_model(y: pd.Series) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )

    classifier = (
        RandomForestClassifier(n_estimators=100, random_state=42)
        if y.nunique() > 1
        else DummyClassifier(strategy="most_frequent")
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def split_dataset(
    x: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    if len(y) < 4 or y.nunique() < 2:
        return x, x, y, y

    return train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )


def evaluate_model(model: Pipeline, x_test: pd.DataFrame, y_test: pd.Series) -> dict[str, float]:
    predictions = model.predict(x_test)
    return {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
    }


def save_model_artifacts(
    model: Pipeline,
    metrics: dict[str, float],
    model_dir: str | Path | None = None,
) -> tuple[Path, Path]:
    output_dir = Path(model_dir or settings.model_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / MODEL_FILENAME
    model_info_path = output_dir / MODEL_INFO_FILENAME

    joblib.dump(model, model_path)
    model_info = {
        "model_path": str(model_path),
        "created_at": datetime.now(UTC).isoformat(),
        "features": FEATURE_COLUMNS,
        "metrics": metrics,
        "model_version": "local",
    }
    model_info_path.write_text(json.dumps(model_info, indent=2), encoding="utf-8")

    return model_path, model_info_path


def train_model(daily: pd.DataFrame) -> tuple[Pipeline, dict[str, float]]:
    x, y = build_training_dataset(daily)
    x_train, x_test, y_train, y_test = split_dataset(x, y)
    model = build_model(y_train)
    model.fit(x_train, y_train)
    metrics = evaluate_model(model, x_test, y_test)
    return model, metrics


def log_training_run(
    model: Pipeline,
    metrics: dict[str, float],
    model_info_path: Path,
    tracking_uri: str,
) -> tuple[str, str]:
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)
    with mlflow.start_run(run_name="rain-prediction-training") as run:
        mlflow.log_params(
            {
                "model_type": model.named_steps["classifier"].__class__.__name__,
                "features": ",".join(FEATURE_COLUMNS),
            }
        )
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(str(model_info_path))
        mlflow.sklearn.log_model(model, artifact_path="model")
        return run.info.run_id, tracking_uri


def log_training_run_with_fallback(
    model: Pipeline,
    metrics: dict[str, float],
    model_info_path: Path,
    tracking_uri: str,
) -> tuple[str, str]:
    try:
        return log_training_run(model, metrics, model_info_path, tracking_uri)
    except Exception:
        fallback_tracking_uri = "file:mlruns"
        if tracking_uri == fallback_tracking_uri:
            raise
        return log_training_run(model, metrics, model_info_path, fallback_tracking_uri)


def run_training(
    processed_dir: str | Path | None = None,
    model_dir: str | Path | None = None,
    tracking_uri: str | None = None,
) -> dict[str, Any]:
    daily = load_daily_dataset(processed_dir)
    model, metrics = train_model(daily)
    model_path, model_info_path = save_model_artifacts(model, metrics, model_dir)
    run_id, resolved_tracking_uri = log_training_run_with_fallback(
        model,
        metrics,
        model_info_path,
        tracking_uri or settings.mlflow_tracking_uri,
    )

    return {
        "run_id": run_id,
        "mlflow_tracking_uri": resolved_tracking_uri,
        "model_path": str(model_path),
        "model_info_path": str(model_info_path),
        "metrics": metrics,
    }


def main() -> None:
    result = run_training()
    print(f"Trained rain prediction model: {result['model_path']}")
    print(f"MLflow tracking URI: {result['mlflow_tracking_uri']}")
    print(f"MLflow run id: {result['run_id']}")


if __name__ == "__main__":
    main()
