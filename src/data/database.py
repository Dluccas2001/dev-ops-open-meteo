from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, URL, make_url

from src.config import settings


def get_engine(database_url: str | None = None) -> Engine:
    return create_engine(database_url or settings.resolved_database_url)


def quote_identifier(identifier: str) -> str:
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'


def build_maintenance_url(url: URL) -> URL:
    return url.set(database="postgres")


def ensure_database_exists(database_url: str | None = None) -> None:
    url = make_url(database_url or settings.resolved_database_url)
    if not url.drivername.startswith("postgresql"):
        return

    database_name = url.database
    if not database_name:
        raise ValueError("DATABASE_URL must include a database name")

    maintenance_engine = create_engine(build_maintenance_url(url), isolation_level="AUTOCOMMIT")
    try:
        with maintenance_engine.connect() as connection:
            exists = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :database_name"),
                {"database_name": database_name},
            ).scalar()
            if not exists:
                connection.execute(text(f"CREATE DATABASE {quote_identifier(database_name)}"))
    finally:
        maintenance_engine.dispose()
