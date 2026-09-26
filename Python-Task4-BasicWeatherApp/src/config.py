import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "OPENWEATHER_API_KEY is not configured. "
        "Create a .env file with your OpenWeather API key."
    )