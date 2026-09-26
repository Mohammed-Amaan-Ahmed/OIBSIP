# OIBSIP - Oasis Infobyte Internship Projects

This repository contains my projects completed as part of the **Oasis Infobyte OIB-SIP Internship 2026**.

## Intern Information

- **Name:** Mohammed Amaan Ahmed
- **Program:** Oasis Infobyte OIB-SIP
- **Track:** Python Programming
- **Internship Start:** 05 September 2026
- **Internship Duration:** 1 Month

## Completed Tasks

### Task 2 - BMI Calculator

**Status:** Completed
**Tier:** Advanced

A Tkinter-based BMI Calculator with:

- BMI calculation and classification
- Input validation
- Color-coded BMI categories
- Multi-user BMI records
- SQLite historical storage
- BMI history viewer
- Matplotlib BMI trend visualization
- Automated unit tests

**Project:** `Python-Task2-BMICalculator/`

---

### Task 3 - Random Password Generator

**Status:** Completed
**Tier:** Advanced

A Tkinter-based secure Random Password Generator with:

- Configurable password length
- Uppercase, lowercase, numbers, and symbols
- Secure generation using Python `secrets`
- Password strength and entropy indicator
- Clipboard copying using `pyperclip`
- Ambiguous-character exclusion
- Last five generated passwords stored only for the current session
- Masked session history
- Input validation and error handling
- Automated unit tests

**Project:** `Python-Task3-RandomPasswordGenerator/`

---

### Task 4 - Basic Weather App

**Status:** Completed
**Tier:** Advanced

A Tkinter-based weather application using the OpenWeatherMap API with:

- City-based weather search
- Current weather information
- Celsius/Fahrenheit conversion
- Humidity and wind information
- Weather descriptions and icons
- Six-hour forecast
- Five-day forecast
- Optional IP-based location detection
- API key configuration through environment variables
- Network and API error handling
- Automated unit tests

**Project:** `Python-Task4-BasicWeatherApp/`

## Technology Stack

- Python
- Tkinter
- SQLite
- Matplotlib
- Requests
- python-dotenv
- Pyperclip
- OpenWeatherMap API
- Pytest
- Git
- GitHub

## Repository Structure

```text
OIBSIP/
|-- Python-Task2-BMICalculator/
|   |-- README.md
|   |-- requirements.txt
|   |-- screenshots/
|   |-- src/
|   `-- tests/
|
|-- Python-Task3-RandomPasswordGenerator/
|   |-- README.md
|   |-- requirements.txt
|   |-- screenshots/
|   |-- src/
|   `-- tests/
|
|-- Python-Task4-BasicWeatherApp/
|   |-- .env.example
|   |-- .gitignore
|   |-- README.md
|   |-- requirements.txt
|   |-- screenshots/
|   |-- src/
|   `-- tests/
|
|-- .gitignore
`-- README.md
```

## Project Approach

Each project was developed with a focus on:

- Requirement-driven implementation
- Modular Python code
- Input validation
- Error handling
- Automated testing
- Secure handling of configuration and secrets
- Documentation
- Git version control
- Practical GUI development
- Maintainable project structure

## Testing

The completed projects include automated tests covering core functionality, validation, API/service behavior, and error-handling scenarios.

## Security and Repository Hygiene

Sensitive configuration files and local development artifacts are excluded from Git using `.gitignore`.

Examples include:

- `.env`
- Virtual environments
- Python cache files
- Pytest cache
- Local database/runtime files
- IDE-specific files

API credentials are never committed to the repository. A `.env.example` file is provided where configuration is required.

## Author

**Mohammed Amaan Ahmed**

Python Programming Intern
Oasis Infobyte OIB-SIP Internship 2026
