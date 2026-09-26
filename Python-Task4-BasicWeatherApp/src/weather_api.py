from typing import Any

import requests

from src.config import API_KEY


class WeatherAPIError(Exception):
    """Base exception for weather API failures."""


class WeatherAPI:
    """Client for OpenWeather current-weather and forecast APIs."""

    BASE_URL = "https://api.openweathermap.org/data/2.5"
    TIMEOUT = 10

    def __init__(self, api_key: str = API_KEY) -> None:
        if not api_key:
            raise WeatherAPIError(
                "OpenWeather API key is not configured."
            )

        self.api_key = api_key

    def _request(
        self,
        endpoint: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        request_params = {
            **params,
            "appid": self.api_key,
        }

        try:
            response = requests.get(
                f"{self.BASE_URL}/{endpoint}",
                params=request_params,
                timeout=self.TIMEOUT,
            )

        except requests.Timeout as exc:
            raise WeatherAPIError(
                "The weather service request timed out."
            ) from exc

        except requests.RequestException as exc:
            raise WeatherAPIError(
                "Unable to connect to the weather service."
            ) from exc

        if response.status_code == 401:
            raise WeatherAPIError(
                "The OpenWeather API key is invalid or unauthorized."
            )

        if response.status_code == 404:
            raise WeatherAPIError(
                "The requested city was not found."
            )

        if not response.ok:
            raise WeatherAPIError(
                f"Weather service returned HTTP "
                f"{response.status_code}."
            )

        try:
            data = response.json()

        except ValueError as exc:
            raise WeatherAPIError(
                "The weather service returned invalid JSON."
            ) from exc

        if not isinstance(data, dict):
            raise WeatherAPIError(
                "Unexpected response format from weather service."
            )

        return data

    def get_current_weather(
        self,
        city: str,
    ) -> dict[str, Any]:
        city = city.strip()

        if not city:
            raise WeatherAPIError(
                "City name cannot be empty."
            )

        return self._request(
            "weather",
            {
                "q": city,
                "units": "metric",
            },
        )

    def get_forecast(
        self,
        city: str,
    ) -> dict[str, Any]:
        city = city.strip()

        if not city:
            raise WeatherAPIError(
                "City name cannot be empty."
            )

        return self._request(
            "forecast",
            {
                "q": city,
                "units": "metric",
            },
        )

    def get_current_weather_by_coordinates(
        self,
        latitude: float,
        longitude: float,
    ) -> dict[str, Any]:
        return self._request(
            "weather",
            {
                "lat": latitude,
                "lon": longitude,
                "units": "metric",
            },
        )

    def get_forecast_by_coordinates(
        self,
        latitude: float,
        longitude: float,
    ) -> dict[str, Any]:
        return self._request(
            "forecast",
            {
                "lat": latitude,
                "lon": longitude,
                "units": "metric",
            },
        )