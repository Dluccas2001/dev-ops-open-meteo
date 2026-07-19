import json
from datetime import UTC, datetime

from src.config import settings
from src.data.cities import City
from src.jobs import ingest


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self.payload


def test_build_forecast_params() -> None:
    city = City(
        slug="sao-paulo",
        name="Sao Paulo",
        uf="SP",
        region="Sudeste",
        latitude=-23.5505,
        longitude=-46.6333,
        timezone="America/Sao_Paulo",
    )

    params = ingest.build_forecast_params(city)

    assert params["latitude"] == -23.5505
    assert params["longitude"] == -46.6333
    assert params["forecast_days"] == settings.forecast_days
    assert params["timezone"] == "America/Sao_Paulo"
    assert "temperature_2m" in params["hourly"]


def test_ingest_city_saves_raw_payload(monkeypatch, tmp_path) -> None:
    city = City(
        slug="sao-paulo",
        name="Sao Paulo",
        uf="SP",
        region="Sudeste",
        latitude=-23.5505,
        longitude=-46.6333,
        timezone="America/Sao_Paulo",
    )
    forecast_payload = {
        "latitude": -23.55,
        "longitude": -46.63,
        "hourly": {
            "time": ["2026-07-19T00:00"],
            "temperature_2m": [18.5],
            "relative_humidity_2m": [80],
            "precipitation": [0.0],
            "wind_speed_10m": [9.2],
        },
    }

    def fake_get(url, params, timeout):
        assert url == settings.open_meteo_base_url
        assert params["latitude"] == city.latitude
        assert timeout == 30
        return FakeResponse(forecast_payload)

    monkeypatch.setattr(ingest.requests, "get", fake_get)
    monkeypatch.setattr(settings, "data_raw_dir", str(tmp_path))

    output_path = ingest.ingest_city(city, datetime(2026, 7, 19, 12, 0, tzinfo=UTC))

    assert output_path == tmp_path / "open_meteo" / "sao-paulo" / "2026-07-19.json"
    saved_payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved_payload["source"] == "open-meteo"
    assert saved_payload["city"]["slug"] == "sao-paulo"
    assert saved_payload["forecast"] == forecast_payload
