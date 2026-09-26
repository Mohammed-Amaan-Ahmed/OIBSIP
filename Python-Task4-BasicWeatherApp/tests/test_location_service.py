from unittest.mock import Mock, patch

import pytest

from src.location_service import LocationService, LocationServiceError


def test_get_location_success():
    response = Mock()
    response.ok = True
    response.json.return_value = {
        "loc": "17.3850,78.4867",
    }

    with patch(
        "src.location_service.requests.get",
        return_value=response,
    ):
        latitude, longitude = LocationService().get_location()

    assert latitude == 17.3850
    assert longitude == 78.4867


def test_get_location_invalid_coordinates():
    response = Mock()
    response.ok = True
    response.json.return_value = {
        "loc": "invalid",
    }

    with patch(
        "src.location_service.requests.get",
        return_value=response,
    ):
        with pytest.raises(LocationServiceError):
            LocationService().get_location()


def test_get_location_http_error():
    response = Mock()
    response.ok = False
    response.status_code = 500

    with patch(
        "src.location_service.requests.get",
        return_value=response,
    ):
        with pytest.raises(LocationServiceError):
            LocationService().get_location()


def test_get_location_timeout():
    import requests

    with patch(
        "src.location_service.requests.get",
        side_effect=requests.Timeout,
    ):
        with pytest.raises(LocationServiceError):
            LocationService().get_location()