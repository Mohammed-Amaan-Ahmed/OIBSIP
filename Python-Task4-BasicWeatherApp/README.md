\# Basic Weather App



\## Oasis Infobyte Python Programming Internship



\*\*Intern:\*\* Mohammed Amaan Ahmed

\*\*Track:\*\* Python Programming

\*\*Task:\*\* Task 4 - Basic Weather App

\*\*Tier:\*\* Advanced



\## Objective



Build a Python weather application that retrieves live weather information from a weather API, processes the response, and presents current conditions and forecasts through a graphical user interface.



\## Features



\- City-based weather search

\- Current temperature

\- Feels-like temperature

\- Humidity

\- Wind speed

\- Weather description

\- Weather condition icons

\- Celsius and Fahrenheit temperature units

\- Next 6-hour forecast

\- 5-day forecast

\- IP-based location detection

\- Automatic weather lookup using detected coordinates

\- API error handling

\- Invalid city handling

\- Invalid API key handling

\- Network and timeout error handling

\- Invalid JSON response handling

\- GUI error messages

\- Automated unit tests



\## Technology Stack



\- Python 3

\- Tkinter

\- Requests

\- python-dotenv

\- OpenWeather API

\- ipinfo.io

\- pytest



\## Project Structure



```text

Python-Task4-BasicWeatherApp/

├── .env.example

├── .gitignore

├── README.md

├── requirements.txt

├── screenshots/

│   ├── 01-weather-dashboard-startup.png

│   ├── 02-current-weather-celsius.png

│   ├── 03-current-weather-fahrenheit.png

│   ├── 04-six-hour-forecast.png

│   └── 05-five-day-forecast.png

├── src/

│   ├── \_\_init\_\_.py

│   ├── config.py

│   ├── gui.py

│   ├── icons.py

│   ├── location\_service.py

│   ├── main.py

│   ├── models.py

│   ├── weather\_api.py

│   └── weather\_service.py

└── tests/

&#x20;   ├── \_\_init\_\_.py

&#x20;   ├── test\_icons.py

&#x20;   ├── test\_location\_service.py

&#x20;   ├── test\_models.py

&#x20;   ├── test\_weather\_api.py

&#x20;   └── test\_weather\_service.py
