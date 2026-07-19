from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert payload["app"] == "weather-mlops-pipeline"
    assert "timestamp" in payload


def test_metadata_endpoint() -> None:
    response = client.get("/metadata")

    assert response.status_code == 200
    payload = response.json()
    assert payload["data_source"] == "Open-Meteo"
