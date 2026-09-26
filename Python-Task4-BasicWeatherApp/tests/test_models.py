from datetime import datetime

from src.models import DailyForecast, ForecastItem, WeatherData


def test_weather_data_model():
    observed_at = datetime(2026, 9, 27, 10, 30)

    weather = WeatherData(
        city="Hyderabad",
        country="IN",
        temperature_c=28.5,
        feels_like_c=30.0,
        humidity=65,
        description="Clear sky",
        wind_speed=3.5,
        icon_code="01d",
        observed_at=observed_at,
    )

    assert weather.city == "Hyderabad"
    assert weather.country == "IN"
    assert weather.temperature_c == 28.5
    assert weather.humidity == 65
    assert weather.icon_code == "01d"


def test_forecast_item_model():
    forecast_time = datetime(2026, 9, 27, 15, 0)

    forecast = ForecastItem(
        forecast_time=forecast_time,
        temperature_c=30.2,
        description="Few clouds",
        icon_code="02d",
    )

    assert forecast.temperature_c == 30.2
    assert forecast.description == "Few clouds"


def test_daily_forecast_model():
    forecast_date = datetime(2026, 9, 27)

    daily = DailyForecast(
        date=forecast_date,
        min_temperature_c=24.0,
        max_temperature_c=31.5,
        description="Light rain",
        icon_code="10d",
    )

    assert daily.min_temperature_c == 24.0
    assert daily.max_temperature_c == 31.5
    assert daily.icon_code == "10d"