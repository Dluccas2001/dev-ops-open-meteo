from pydantic import BaseModel, Field


class RainPredictionRequest(BaseModel):
    city: str
    temp_mean: float
    temp_min: float
    temp_max: float
    humidity_mean: float = Field(ge=0, le=100)
    wind_mean: float = Field(ge=0)
    rain_sum: float = Field(ge=0)
    month: int = Field(ge=1, le=12)
    day_of_week: int = Field(ge=0, le=6)
    region: str = "unknown"


class RainPredictionResponse(BaseModel):
    city: str
    will_rain_tomorrow: bool
    probability: float
    model_version: str
