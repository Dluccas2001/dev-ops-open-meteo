from functools import lru_cache

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

    database_url: str = "postgresql://postgres:postgres@localhost:5432/weather"
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "weather-rain-prediction"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

