from unittest.mock import Mock, patch

import requests
import pytest

from src.weather_api import WeatherAPI, WeatherAPIError


def create_response(
    status_code: int,
    json_data: object,
    ok: bool = True,
) -> Mock:
    response = Mock()
    response.status_code = status_code
    response.ok = ok
    response.json.return_value = json_data
    return response


def test_get_current_weather_by_city() -> None:
    response = create_response(
        200,
        {
            "name": "Hyderabad",
            "main": {
                "temp": 26.5,
            },
        },
    )

    with patch(
        "src.weather_api.requests.get",
        return_value=response,
    ) as mock_get:
        api = WeatherAPI("test-api-key")
        result = api.get_current_weather("Hyderabad")

    assert result["name"] == "Hyderabad"

    mock_get.assert_called_once()

    params = mock_get.call_args.kwargs["params"]

    assert params["q"] == "Hyderabad"
    assert params["units"] == "metric"
    assert params["appid"] == "test-api-key"


def test_get_forecast_by_city() -> None:
    response = create_response(
        200,
        {
            "list": [],
        },
    )

    with patch(
        "src.weather_api.requests.get",
        return_value=response,
    ) as mock_get:
        api = WeatherAPI("test-api-key")
        result = api.get_forecast("Hyderabad")

    assert result["list"] == []

    params = mock_get.call_args.kwargs["params"]

    assert params["q"] == "Hyderabad"
    assert params["units"] == "metric"
    assert params["appid"] == "test-api-key"


def test_get_current_weather_by_coordinates() -> None:
    response = create_response(
        200,
        {
            "name": "Hyderabad",
            "main": {
                "temp": 26.5,
            },
        },
    )

    with patch(
        "src.weather_api.requests.get",
        return_value=response,
    ) as mock_get:
        api = WeatherAPI("test-api-key")

        result = api.get_current_weather_by_coordinates(
            17.3850,
            78.4867,
        )

    assert result["name"] == "Hyderabad"

    params = mock_get.call_args.kwargs["params"]

    assert params["lat"] == 17.3850
    assert params["lon"] == 78.4867
    assert params["units"] == "metric"
    assert params["appid"] == "test-api-key"


def test_get_forecast_by_coordinates() -> None:
    response = create_response(
        200,
        {
            "list": [],
        },
    )

    with patch(
        "src.weather_api.requests.get",
        return_value=response,
    ) as mock_get:
        api = WeatherAPI("test-api-key")

        result = api.get_forecast_by_coordinates(
            17.3850,
            78.4867,
        )

    assert result["list"] == []

    params = mock_get.call_args.kwargs["params"]

    assert params["lat"] == 17.3850
    assert params["lon"] == 78.4867
    assert params["units"] == "metric"
    assert params["appid"] == "test-api-key"


def test_empty_city_is_rejected() -> None:
    api = WeatherAPI("test-api-key")

    with pytest.raises(
        WeatherAPIError,
        match="City name cannot be empty",
    ):
        api.get_current_weather("")


def test_missing_api_key_is_rejected() -> None:
    with pytest.raises(
        WeatherAPIError,
        match="API key is not configured",
    ):
        WeatherAPI("")


def test_invalid_api_key_returns_controlled_error() -> None:
    response = create_response(
        401,
        {
            "cod": 401,
            "message": "Invalid API key",
        },
        ok=False,
    )

    with patch(
        "src.weather_api.requests.get",
        return_value=response,
    ):
        api = WeatherAPI("invalid-test-key")

        with pytest.raises(
            WeatherAPIError,
            match="invalid or unauthorized",
        ):
            api.get_current_weather("Hyderabad")


def test_city_not_found_returns_controlled_error() -> None:
    response = create_response(
        404,
        {
            "cod": "404",
            "message": "city not found",
        },
        ok=False,
    )

    with patch(
        "src.weather_api.requests.get",
        return_value=response,
    ):
        api = WeatherAPI("test-api-key")

        with pytest.raises(
            WeatherAPIError,
            match="city was not found",
        ):
            api.get_current_weather("UnknownCity")


def test_timeout_returns_controlled_error() -> None:
    with patch(
        "src.weather_api.requests.get",
        side_effect=requests.Timeout,
    ):
        api = WeatherAPI("test-api-key")

        with pytest.raises(
            WeatherAPIError,
            match="timed out",
        ):
            api.get_current_weather("Hyderabad")


def test_network_failure_returns_controlled_error() -> None:
    with patch(
        "src.weather_api.requests.get",
        side_effect=requests.ConnectionError,
    ):
        api = WeatherAPI("test-api-key")

        with pytest.raises(
            WeatherAPIError,
            match="Unable to connect",
        ):
            api.get_current_weather("Hyderabad")


def test_invalid_json_returns_controlled_error() -> None:
    response = Mock()
    response.status_code = 200
    response.ok = True
    response.json.side_effect = ValueError

    with patch(
        "src.weather_api.requests.get",
        return_value=response,
    ):
        api = WeatherAPI("test-api-key")

        with pytest.raises(
            WeatherAPIError,
            match="invalid JSON",
        ):
            api.get_current_weather("Hyderabad")


def test_unexpected_response_format_returns_controlled_error() -> None:
    response = create_response(
        200,
        ["unexpected", "list"],
    )

    with patch(
        "src.weather_api.requests.get",
        return_value=response,
    ):
        api = WeatherAPI("test-api-key")

        with pytest.raises(
            WeatherAPIError,
            match="Unexpected response format",
        ):
            api.get_current_weather("Hyderabad")


def test_server_error_returns_controlled_error() -> None:
    response = create_response(
        500,
        {
            "message": "server error",
        },
        ok=False,
    )

    with patch(
        "src.weather_api.requests.get",
        return_value=response,
    ):
        api = WeatherAPI("test-api-key")

        with pytest.raises(
            WeatherAPIError,
            match="HTTP 500",
        ):
            api.get_current_weather("Hyderabad")