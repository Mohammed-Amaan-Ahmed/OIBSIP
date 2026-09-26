from datetime import datetime

import pytest

from src.weather_service import WeatherDataError, WeatherService


def test_parse_current_weather():
    response = {
        "name": "Hyderabad",
        "sys": {
            "country": "IN",
        },
        "dt": 1790485200,
        "main": {
            "temp": 28.5,
            "feels_like": 30.0,
            "humidity": 65,
        },
        "weather": [
            {
                "description": "clear sky",
                "icon": "01d",
            }
        ],
        "wind": {
            "speed": 3.5,
        },
    }

    result = WeatherService.parse_current_weather(response)

    assert result.city == "Hyderabad"
    assert result.country == "IN"
    assert result.temperature_c == 28.5
    assert result.feels_like_c == 30.0
    assert result.humidity == 65
    assert result.description == "Clear sky"
    assert result.wind_speed == 3.5
    assert result.icon_code == "01d"
    assert isinstance(result.observed_at, datetime)


def test_parse_current_weather_rejects_missing_data():
    response = {
        "name": "Hyderabad",
        "sys": {
            "country": "IN",
        },
    }

    with pytest.raises(WeatherDataError):
        WeatherService.parse_current_weather(response)


def test_parse_forecast():
    response = {
        "list": [
            {
                "dt": 1790485200,
                "main": {
                    "temp": 28.5,
                },
                "weather": [
                    {
                        "description": "clear sky",
                        "icon": "01d",
                    }
                ],
            },
            {
                "dt": 1790496000,
                "main": {
                    "temp": 30.0,
                },
                "weather": [
                    {
                        "description": "few clouds",
                        "icon": "02d",
                    }
                ],
            },
        ]
    }

    result = WeatherService.parse_forecast(response)

    assert len(result) == 2
    assert result[0].temperature_c == 28.5
    assert result[1].description == "Few clouds"


def test_parse_forecast_rejects_missing_list():
    with pytest.raises(WeatherDataError):
        WeatherService.parse_forecast({})


def test_build_daily_forecasts():
    items = [
        # Day 1
        _forecast("2026-09-27 09:00", 25.0, "Clear sky", "01d"),
        _forecast("2026-09-27 12:00", 30.0, "Clear sky", "01d"),
        _forecast("2026-09-27 15:00", 32.0, "Few clouds", "02d"),
        # Day 2
        _forecast("2026-09-28 09:00", 24.0, "Cloudy", "03d"),
        _forecast("2026-09-28 12:00", 29.0, "Cloudy", "03d"),
    ]

    result = WeatherService.build_daily_forecasts(items)

    assert len(result) == 2

    assert result[0].min_temperature_c == 25.0
    assert result[0].max_temperature_c == 32.0

    assert result[1].min_temperature_c == 24.0
    assert result[1].max_temperature_c == 29.0


def test_build_daily_forecasts_limits_to_five_days():
    items = []

    for day in range(1, 8):
        items.append(
            _forecast(
                f"2026-09-{day:02d} 12:00",
                25.0 + day,
                "Clear sky",
                "01d",
            )
        )

    result = WeatherService.build_daily_forecasts(items)

    assert len(result) == 5


def test_celsius_to_fahrenheit():
    assert WeatherService.celsius_to_fahrenheit(0) == 32
    assert WeatherService.celsius_to_fahrenheit(100) == 212
    assert WeatherService.celsius_to_fahrenheit(25) == 77


def _forecast(
    timestamp: str,
    temperature: float,
    description: str,
    icon: str,
):
    return type(
        "ForecastItem",
        (),
        {
            "forecast_time": datetime.strptime(
                timestamp,
                "%Y-%m-%d %H:%M",
            ),
            "temperature_c": temperature,
            "description": description,
            "icon_code": icon,
        },
    )()