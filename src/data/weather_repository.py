from typing import Any

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.data.database import get_engine


def serialize_record(record: dict[str, Any]) -> dict[str, Any]:
    serialized = {}
    for key, value in record.items():
        if hasattr(value, "isoformat"):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    return serialized


def fetch_cities(engine: Engine | None = None) -> list[dict[str, Any]]:
    own_engine = engine is None
    active_engine = engine or get_engine()
    query = text(
        """
        SELECT DISTINCT city, uf, region
        FROM weather_daily
        ORDER BY city
        """
    )
    try:
        with active_engine.connect() as connection:
            rows = connection.execute(query).mappings().all()
        return [dict(row) for row in rows]
    finally:
        if own_engine:
            active_engine.dispose()


def fetch_latest_weather(city: str, engine: Engine | None = None) -> dict[str, Any] | None:
    own_engine = engine is None
    active_engine = engine or get_engine()
    query = text(
        """
        SELECT *
        FROM weather_daily
        WHERE city = :city
        ORDER BY date DESC
        LIMIT 1
        """
    )
    try:
        with active_engine.connect() as connection:
            row = connection.execute(query, {"city": city}).mappings().first()
        return serialize_record(dict(row)) if row else None
    finally:
        if own_engine:
            active_engine.dispose()


def fetch_daily_weather(
    city: str,
    limit: int = 30,
    engine: Engine | None = None,
) -> list[dict[str, Any]]:
    own_engine = engine is None
    active_engine = engine or get_engine()
    query = text(
        """
        SELECT *
        FROM weather_daily
        WHERE city = :city
        ORDER BY date DESC
        LIMIT :limit
        """
    )
    try:
        with active_engine.connect() as connection:
            rows = connection.execute(query, {"city": city, "limit": limit}).mappings().all()
        return [serialize_record(dict(row)) for row in rows]
    finally:
        if own_engine:
            active_engine.dispose()


def fetch_weather_summary(engine: Engine | None = None) -> dict[str, Any]:
    own_engine = engine is None
    active_engine = engine or get_engine()
    try:
        daily = pd.read_sql_query("SELECT * FROM weather_daily", active_engine)
    finally:
        if own_engine:
            active_engine.dispose()

    if daily.empty:
        return {"cities": 0, "days": 0, "rainy_days": 0, "avg_temp_mean": None}

    return {
        "cities": int(daily["city"].nunique()),
        "days": int(len(daily)),
        "rainy_days": int(daily["will_rain"].sum()),
        "avg_temp_mean": round(float(daily["temp_mean"].mean()), 2),
    }
