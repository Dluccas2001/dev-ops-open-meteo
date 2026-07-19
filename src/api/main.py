import time
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.config import settings
from src.data.weather_repository import (
    fetch_cities,
    fetch_daily_weather,
    fetch_latest_weather,
    fetch_weather_summary,
)

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


def database_unavailable_error() -> HTTPException:
    return HTTPException(
        status_code=503,
        detail="Weather database is unavailable. Run transform and load jobs first.",
    )


@app.get("/cities", tags=["weather"])
def cities() -> list[dict]:
    try:
        return fetch_cities()
    except SQLAlchemyError as exc:
        raise database_unavailable_error() from exc


@app.get("/weather/latest", tags=["weather"])
def weather_latest(city: str) -> dict:
    try:
        latest = fetch_latest_weather(city)
    except SQLAlchemyError as exc:
        raise database_unavailable_error() from exc

    if latest is None:
        raise HTTPException(status_code=404, detail=f"No weather data found for city: {city}")
    return latest


@app.get("/weather/daily", tags=["weather"])
def weather_daily(city: str, limit: int = 30) -> list[dict]:
    try:
        return fetch_daily_weather(city, limit)
    except SQLAlchemyError as exc:
        raise database_unavailable_error() from exc


@app.get("/weather/summary", tags=["weather"])
def weather_summary() -> dict:
    try:
        return fetch_weather_summary()
    except SQLAlchemyError as exc:
        raise database_unavailable_error() from exc
