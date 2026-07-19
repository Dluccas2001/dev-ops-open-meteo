from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class City:
    slug: str
    name: str
    uf: str
    region: str
    latitude: float
    longitude: float
    timezone: str


def load_cities(config_path: str | Path = "config/cities.yaml") -> list[City]:
    path = Path(config_path)
    with path.open(encoding="utf-8") as file:
        payload: dict[str, Any] = yaml.safe_load(file)

    cities = payload.get("cities", [])
    if not cities:
        raise ValueError(f"No cities configured in {path}")

    return [City(**city) for city in cities]
