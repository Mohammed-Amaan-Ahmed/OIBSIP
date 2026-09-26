import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from src.icons import get_weather_icon
from src.location_service import LocationService, LocationServiceError
from src.weather_api import WeatherAPI, WeatherAPIError
from src.weather_service import WeatherDataError, WeatherService


class WeatherApp:
    """Tkinter interface for the weather application."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Weather Dashboard")
        self.root.geometry("1100x900")
        self.root.minsize(950, 800)

        self.city_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="C")
        self.status_var = tk.StringVar(
            value="Enter a city to get weather."
        )

        self.weather_data = None
        self.forecast_items = []

        self.weather_api = WeatherAPI()
        self.location_service = LocationService()

        self._configure_styles()
        self._build_interface()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 22, "bold"),
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 10),
        )

        style.configure(
            "Temperature.TLabel",
            font=("Segoe UI", 30, "bold"),
        )

        style.configure(
            "ForecastTemperature.TLabel",
            font=("Segoe UI", 11, "bold"),
        )

        style.configure(
            "WeatherIcon.TLabel",
            font=("Segoe UI Emoji", 34),
        )

        style.configure(
            "ForecastIcon.TLabel",
            font=("Segoe UI Emoji", 22),
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 13, "bold"),
        )

    def _build_interface(self) -> None:
        main = ttk.Frame(
            self.root,
            padding=16,
        )
        main.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            main,
            text="Weather Dashboard",
            style="Title.TLabel",
        ).pack(
            pady=(0, 3),
        )

        ttk.Label(
            main,
            text="Current weather and forecast information",
            style="Subtitle.TLabel",
        ).pack(
            pady=(0, 12),
        )

        search_frame = ttk.Frame(main)
        search_frame.pack(
            fill="x",
            pady=(0, 7),
        )

        ttk.Label(
            search_frame,
            text="City:",
        ).pack(
            side="left",
            padx=(0, 8),
        )

        self.city_entry = ttk.Entry(
            search_frame,
            textvariable=self.city_var,
            width=35,
        )
        self.city_entry.pack(
            side="left",
            padx=(0, 8),
        )

        self.get_weather_button = ttk.Button(
            search_frame,
            text="Get Weather",
            command=self._handle_search,
        )
        self.get_weather_button.pack(
            side="left",
            padx=(0, 8),
        )

        self.location_button = ttk.Button(
            search_frame,
            text="Use My Location",
            command=self._handle_location,
        )
        self.location_button.pack(
            side="left",
        )

        unit_frame = ttk.Frame(main)
        unit_frame.pack(
            fill="x",
            pady=(0, 8),
        )

        ttk.Label(
            unit_frame,
            text="Temperature:",
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ttk.Radiobutton(
            unit_frame,
            text="Celsius (°C)",
            variable=self.unit_var,
            value="C",
            command=self._handle_unit_change,
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ttk.Radiobutton(
            unit_frame,
            text="Fahrenheit (°F)",
            variable=self.unit_var,
            value="F",
            command=self._handle_unit_change,
        ).pack(
            side="left",
        )

        ttk.Label(
            main,
            textvariable=self.status_var,
        ).pack(
            fill="x",
            pady=(0, 8),
        )

        self.current_frame = ttk.LabelFrame(
            main,
            text="Current Weather",
            padding=8,
        )
        self.current_frame.pack(
            fill="x",
            pady=(0, 8),
        )

        current_content = ttk.Frame(
            self.current_frame,
        )
        current_content.pack(
            fill="x",
        )

        self.weather_icon_label = ttk.Label(
            current_content,
            text="🌡️",
            style="WeatherIcon.TLabel",
        )
        self.weather_icon_label.pack(
            side="left",
            padx=(8, 18),
        )

        current_info = ttk.Frame(
            current_content,
        )
        current_info.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self.location_label = ttk.Label(
            current_info,
            text="No location selected",
            style="Section.TLabel",
        )
        self.location_label.pack(
            anchor="w",
        )

        self.temperature_label = ttk.Label(
            current_info,
            text="--°C",
            style="Temperature.TLabel",
        )
        self.temperature_label.pack(
            anchor="w",
        )

        self.description_label = ttk.Label(
            current_info,
            text="Weather information will appear here.",
        )
        self.description_label.pack(
            anchor="w",
        )

        details = ttk.Frame(current_info)
        details.pack(
            anchor="w",
            pady=(5, 0),
        )

        self.feels_like_label = ttk.Label(
            details,
            text="Feels like: --",
        )
        self.feels_like_label.pack(
            side="left",
            padx=(0, 20),
        )

        self.humidity_label = ttk.Label(
            details,
            text="Humidity: --",
        )
        self.humidity_label.pack(
            side="left",
            padx=(0, 20),
        )

        self.wind_label = ttk.Label(
            details,
            text="Wind: --",
        )
        self.wind_label.pack(
            side="left",
        )

        self.hourly_frame = ttk.LabelFrame(
            main,
            text="Next 6 Hours",
            padding=6,
        )
        self.hourly_frame.pack(
            fill="x",
            pady=(0, 8),
        )

        self.hourly_content = ttk.Frame(
            self.hourly_frame,
        )
        self.hourly_content.pack(
            fill="x",
        )

        self.hourly_placeholder = ttk.Label(
            self.hourly_content,
            text="Hourly forecast will appear here.",
        )
        self.hourly_placeholder.pack(
            pady=8,
        )

        self.daily_frame = ttk.LabelFrame(
            main,
            text="5-Day Forecast",
            padding=6,
        )
        self.daily_frame.pack(
            fill="both",
            expand=True,
        )

        self.daily_content = ttk.Frame(
            self.daily_frame,
        )
        self.daily_content.pack(
            fill="both",
            expand=True,
        )

        self.daily_placeholder = ttk.Label(
            self.daily_content,
            text="Five-day forecast will appear here.",
        )
        self.daily_placeholder.pack(
            pady=8,
        )

    def _handle_search(self) -> None:
        city = self.city_var.get().strip()

        if not city:
            self._show_error(
                "Please enter a city name."
            )
            return

        self._set_loading(True)

        self.status_var.set(
            f"Fetching weather for {city}..."
        )

        try:
            current_response = (
                self.weather_api.get_current_weather(
                    city,
                )
            )

            forecast_response = (
                self.weather_api.get_forecast(
                    city,
                )
            )

            self.weather_data = (
                WeatherService.parse_current_weather(
                    current_response,
                )
            )

            self.forecast_items = (
                WeatherService.parse_forecast(
                    forecast_response,
                )
            )

            self._display_current_weather()
            self._display_hourly_forecast()
            self._display_daily_forecast()

            self.status_var.set(
                f"Weather updated for "
                f"{self.weather_data.city}, "
                f"{self.weather_data.country}."
            )

        except WeatherAPIError as exc:
            self.weather_data = None
            self.forecast_items = []
            self._show_error(str(exc))

        except WeatherDataError as exc:
            self.weather_data = None
            self.forecast_items = []
            self._show_error(str(exc))

        except Exception:
            self.weather_data = None
            self.forecast_items = []
            self._show_error(
                "An unexpected error occurred "
                "while loading weather data."
            )

        finally:
            self._set_loading(False)

    def _handle_location(self) -> None:
        self._set_loading(True)

        self.status_var.set(
            "Detecting your location..."
        )

        try:
            latitude, longitude = (
                self.location_service.get_location()
            )

            current_response = (
                self.weather_api.get_current_weather_by_coordinates(
                    latitude,
                    longitude,
                )
            )

            forecast_response = (
                self.weather_api.get_forecast_by_coordinates(
                    latitude,
                    longitude,
                )
            )

            self.weather_data = (
                WeatherService.parse_current_weather(
                    current_response,
                )
            )

            self.forecast_items = (
                WeatherService.parse_forecast(
                    forecast_response,
                )
            )

            self.city_var.set(
                self.weather_data.city
            )

            self._display_current_weather()
            self._display_hourly_forecast()
            self._display_daily_forecast()

            self.status_var.set(
                f"Weather detected for "
                f"{self.weather_data.city}, "
                f"{self.weather_data.country}."
            )

        except LocationServiceError as exc:
            self._show_error(str(exc))

        except WeatherAPIError as exc:
            self.weather_data = None
            self.forecast_items = []
            self._show_error(str(exc))

        except WeatherDataError as exc:
            self.weather_data = None
            self.forecast_items = []
            self._show_error(str(exc))

        except Exception:
            self.weather_data = None
            self.forecast_items = []
            self._show_error(
                "An unexpected error occurred "
                "while detecting your location."
            )

        finally:
            self._set_loading(False)

    def _set_loading(
        self,
        loading: bool,
    ) -> None:
        state = "disabled" if loading else "normal"

        self.get_weather_button.config(
            state=state,
        )

        self.location_button.config(
            state=state,
        )

    def _display_current_weather(self) -> None:
        if self.weather_data is None:
            return

        weather = self.weather_data

        self.location_label.config(
            text=f"{weather.city}, {weather.country}",
        )

        self.weather_icon_label.config(
            text=get_weather_icon(
                weather.icon_code,
            ),
        )

        self.description_label.config(
            text=weather.description,
        )

        self.humidity_label.config(
            text=f"Humidity: {weather.humidity}%",
        )

        self.wind_label.config(
            text=f"Wind: {weather.wind_speed:.1f} m/s",
        )

        self._update_temperature_labels()

    def _update_temperature_labels(self) -> None:
        if self.weather_data is None:
            return

        temperature_c = (
            self.weather_data.temperature_c
        )

        feels_like_c = (
            self.weather_data.feels_like_c
        )

        if self.unit_var.get() == "F":
            temperature = (
                WeatherService.celsius_to_fahrenheit(
                    temperature_c,
                )
            )

            feels_like = (
                WeatherService.celsius_to_fahrenheit(
                    feels_like_c,
                )
            )

            symbol = "°F"

        else:
            temperature = temperature_c
            feels_like = feels_like_c
            symbol = "°C"

        self.temperature_label.config(
            text=f"{temperature:.1f}{symbol}",
        )

        self.feels_like_label.config(
            text=f"Feels like: {feels_like:.1f}{symbol}",
        )

        self._display_hourly_forecast()
        self._display_daily_forecast()

    def _display_hourly_forecast(self) -> None:
        for widget in self.hourly_content.winfo_children():
            widget.destroy()

        if not self.forecast_items:
            ttk.Label(
                self.hourly_content,
                text="Hourly forecast unavailable.",
            ).pack(
                pady=8,
            )
            return

        now = datetime.now()

        upcoming = [
            item
            for item in self.forecast_items
            if item.forecast_time >= now
        ]

        upcoming = upcoming[:2]

        if not upcoming:
            upcoming = self.forecast_items[:2]

        for item in upcoming:
            self._create_hourly_card(item)

    def _create_hourly_card(
        self,
        item,
    ) -> None:
        card = ttk.Frame(
            self.hourly_content,
            padding=4,
        )
        card.pack(
            side="left",
            fill="x",
            expand=True,
        )

        time_text = item.forecast_time.strftime(
            "%I:%M %p",
        ).lstrip("0")

        ttk.Label(
            card,
            text=time_text,
        ).pack()

        ttk.Label(
            card,
            text=get_weather_icon(
                item.icon_code,
            ),
            style="ForecastIcon.TLabel",
        ).pack()

        temperature = self._format_temperature(
            item.temperature_c,
        )

        ttk.Label(
            card,
            text=temperature,
            style="ForecastTemperature.TLabel",
        ).pack()

        ttk.Label(
            card,
            text=item.description,
            wraplength=120,
            justify="center",
        ).pack()

    def _display_daily_forecast(self) -> None:
        for widget in self.daily_content.winfo_children():
            widget.destroy()

        if not self.forecast_items:
            ttk.Label(
                self.daily_content,
                text="Five-day forecast unavailable.",
            ).pack(
                pady=8,
            )
            return

        daily_forecasts = (
            WeatherService.build_daily_forecasts(
                self.forecast_items,
            )
        )

        for forecast in daily_forecasts:
            self._create_daily_card(forecast)

    def _create_daily_card(
        self,
        forecast,
    ) -> None:
        card = ttk.Frame(
            self.daily_content,
            padding=5,
            relief="groove",
            borderwidth=1,
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=3,
            pady=3,
        )

        date_text = forecast.date.strftime(
            "%a\n%d %b",
        )

        ttk.Label(
            card,
            text=date_text,
            justify="center",
        ).pack(
            pady=(2, 3),
        )

        ttk.Label(
            card,
            text=get_weather_icon(
                forecast.icon_code,
            ),
            style="ForecastIcon.TLabel",
        ).pack()

        ttk.Label(
            card,
            text=forecast.description,
            wraplength=110,
            justify="center",
        ).pack(
            pady=(2, 3),
        )

        maximum = self._format_temperature(
            forecast.max_temperature_c,
        )

        minimum = self._format_temperature(
            forecast.min_temperature_c,
        )

        ttk.Label(
            card,
            text=f"High: {maximum}",
            style="ForecastTemperature.TLabel",
        ).pack()

        ttk.Label(
            card,
            text=f"Low: {minimum}",
        ).pack()

    def _format_temperature(
        self,
        temperature_c: float,
    ) -> str:
        if self.unit_var.get() == "F":
            temperature = (
                WeatherService.celsius_to_fahrenheit(
                    temperature_c,
                )
            )

            return f"{temperature:.1f}°F"

        return f"{temperature_c:.1f}°C"

    def _handle_unit_change(self) -> None:
        if self.weather_data is None:
            self.status_var.set(
                f"Temperature unit changed to "
                f"°{self.unit_var.get()}."
            )
            return

        self._update_temperature_labels()

        self.status_var.set(
            f"Temperature unit changed to "
            f"°{self.unit_var.get()}."
        )

    def _show_error(
        self,
        message: str,
    ) -> None:
        self.status_var.set(message)

        messagebox.showerror(
            "Weather App",
            message,
        )

    def run(self) -> None:
        self.root.mainloop()