from fastapi.testclient import TestClient

from src.api import main

client = TestClient(main.app)


def test_cities_endpoint(monkeypatch) -> None:
    monkeypatch.setattr(
        main,
        "fetch_cities",
        lambda: [{"city": "sao-paulo", "uf": "SP", "region": "Sudeste"}],
    )

    response = client.get("/cities")

    assert response.status_code == 200
    assert response.json()[0]["city"] == "sao-paulo"


def test_weather_latest_endpoint(monkeypatch) -> None:
    monkeypatch.setattr(
        main,
        "fetch_latest_weather",
        lambda city: {"city": city, "date": "2026-07-20", "rain_sum": 0.0},
    )

    response = client.get("/weather/latest?city=sao-paulo")

    assert response.status_code == 200
    assert response.json()["city"] == "sao-paulo"


def test_weather_latest_endpoint_returns_404(monkeypatch) -> None:
    monkeypatch.setattr(main, "fetch_latest_weather", lambda city: None)

    response = client.get("/weather/latest?city=sao-paulo")

    assert response.status_code == 404


def test_weather_daily_endpoint(monkeypatch) -> None:
    monkeypatch.setattr(
        main,
        "fetch_daily_weather",
        lambda city, limit: [{"city": city, "limit": limit}],
    )

    response = client.get("/weather/daily?city=sao-paulo&limit=5")

    assert response.status_code == 200
    assert response.json() == [{"city": "sao-paulo", "limit": 5}]


def test_weather_summary_endpoint(monkeypatch) -> None:
    monkeypatch.setattr(
        main,
        "fetch_weather_summary",
        lambda: {"cities": 1, "days": 2, "rainy_days": 1, "avg_temp_mean": 20.5},
    )

    response = client.get("/weather/summary")

    assert response.status_code == 200
    assert response.json()["cities"] == 1
