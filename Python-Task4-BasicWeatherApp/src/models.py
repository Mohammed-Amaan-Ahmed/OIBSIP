from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WeatherData:
    city: str
    country: str
    temperature_c: float
    feels_like_c: float
    humidity: int
    description: str
    wind_speed: float
    icon_code: str
    observed_at: datetime


@dataclass(frozen=True)
class ForecastItem:
    forecast_time: datetime
    temperature_c: float
    description: str
    icon_code: str


@dataclass(frozen=True)
class DailyForecast:
    date: datetime
    min_temperature_c: float
    max_temperature_c: float
    description: str
    icon_code: str