from pathlib import Path

from src.data.cities import load_cities


def test_load_cities_from_yaml() -> None:
    cities = load_cities(Path("config/cities.yaml"))

    assert len(cities) == 10
    assert cities[0].slug == "sao-paulo"
    assert cities[0].latitude == -23.5505
    assert cities[0].timezone == "America/Sao_Paulo"
