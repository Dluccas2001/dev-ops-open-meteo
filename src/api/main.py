import time
from datetime import UTC, datetime

from fastapi import FastAPI

from src.config import settings

START_TIME = time.monotonic()

app = FastAPI(
    title=settings.app_name,
    description="API do pipeline Open-Meteo com DevOps e MLOps.",
    version="0.1.0",
)


@app.get("/health", tags=["monitoring"])
def health() -> dict:
    uptime = time.monotonic() - START_TIME
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.env,
        "uptime_seconds": round(uptime, 2),
        "timestamp": datetime.now(UTC).isoformat(),
    }


@app.get("/metadata", tags=["metadata"])
def metadata() -> dict:
    return {
        "project": settings.app_name,
        "data_source": "Open-Meteo",
        "forecast_days": settings.forecast_days,
        "mlflow_tracking_uri": settings.mlflow_tracking_uri,
    }
