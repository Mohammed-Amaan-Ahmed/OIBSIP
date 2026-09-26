from datetime import datetime
from typing import Any

from src.models import DailyForecast, ForecastItem, WeatherData


class WeatherDataError(Exception):
    """Raised when weather API data cannot be processed."""


class WeatherService:
    """Transforms OpenWeatherMap responses into application data."""

    @staticmethod
    def parse_current_weather(data: dict[str, Any]) -> WeatherData:
        try:
            main = data["main"]
            weather = data["weather"][0]
            wind = data["wind"]
            system = data["sys"]

            observed_timestamp = data.get("dt")

            if observed_timestamp is None:
                observed_at = datetime.now()
            else:
                observed_at = datetime.fromtimestamp(observed_timestamp)

            return WeatherData(
                city=str(data["name"]),
                country=str(system["country"]),
                temperature_c=float(main["temp"]),
                feels_like_c=float(main["feels_like"]),
                humidity=int(main["humidity"]),
                description=str(weather["description"]).capitalize(),
                wind_speed=float(wind["speed"]),
                icon_code=str(weather["icon"]),
                observed_at=observed_at,
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise WeatherDataError(
                "The current weather response is missing required data."
            ) from exc

    @staticmethod
    def parse_forecast(data: dict[str, Any]) -> list[ForecastItem]:
        try:
            entries = data["list"]
        except (KeyError, TypeError) as exc:
            raise WeatherDataError(
                "The forecast response does not contain forecast data."
            ) from exc

        forecast_items: list[ForecastItem] = []

        for entry in entries:
            try:
                forecast_time = datetime.fromtimestamp(entry["dt"])
                main = entry["main"]
                weather = entry["weather"][0]

                forecast_items.append(
                    ForecastItem(
                        forecast_time=forecast_time,
                        temperature_c=float(main["temp"]),
                        description=str(
                            weather["description"]
                        ).capitalize(),
                        icon_code=str(weather["icon"]),
                    )
                )
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                raise WeatherDataError(
                    "The forecast response contains invalid data."
                ) from exc

        return forecast_items

    @staticmethod
    def build_daily_forecasts(
        forecast_items: list[ForecastItem],
    ) -> list[DailyForecast]:
        grouped: dict[str, list[ForecastItem]] = {}

        for item in forecast_items:
            date_key = item.forecast_time.date().isoformat()
            grouped.setdefault(date_key, []).append(item)

        daily_forecasts: list[DailyForecast] = []

        for items in grouped.values():
            temperatures = [item.temperature_c for item in items]

            representative = min(
                items,
                key=lambda item: abs(item.forecast_time.hour - 12),
            )

            daily_forecasts.append(
                DailyForecast(
                    date=representative.forecast_time,
                    min_temperature_c=min(temperatures),
                    max_temperature_c=max(temperatures),
                    description=representative.description,
                    icon_code=representative.icon_code,
                )
            )

        return daily_forecasts[:5]

    @staticmethod
    def celsius_to_fahrenheit(temperature_c: float) -> float:
        return (temperature_c * 9 / 5) + 32