from src.icons import get_weather_icon


def test_known_weather_icon():
    assert get_weather_icon("01d") == "☀️"


def test_night_weather_icon():
    assert get_weather_icon("01n") == "🌙"


def test_rain_icon():
    assert get_weather_icon("10d") == "🌦️"


def test_unknown_icon_uses_fallback():
    assert get_weather_icon("unknown") == "🌡️"