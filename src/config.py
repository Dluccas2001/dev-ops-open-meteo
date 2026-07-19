from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: str = "development"
    app_name: str = "weather-mlops-pipeline"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    open_meteo_base_url: str = "https://api.open-meteo.com/v1/forecast"
    forecast_days: int = 7

    data_raw_dir: str = "data/raw"
    data_processed_dir: str = "data/processed"
    model_dir: str = "models"

    database_url: str | None = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "open-meteo"
    db_user: str = "postgres"
    db_password: str = "postgres"

    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "weather-rain-prediction"

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url

        user = quote_plus(self.db_user)
        password = quote_plus(self.db_password)
        database = quote_plus(self.db_name)
        return f"postgresql://{user}:{password}@{self.db_host}:{self.db_port}/{database}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
