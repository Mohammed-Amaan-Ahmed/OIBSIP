from typing import Any

import requests


class LocationServiceError(Exception):
    """Raised when IP-based location lookup fails."""


class LocationService:
    """Retrieve approximate location information from the public IP."""

    URL = "https://ipinfo.io/json"
    TIMEOUT = 5

    def get_location(self) -> tuple[float, float]:
        try:
            response = requests.get(
                self.URL,
                timeout=self.TIMEOUT,
            )
        except requests.Timeout as exc:
            raise LocationServiceError(
                "Location service request timed out."
            ) from exc
        except requests.RequestException as exc:
            raise LocationServiceError(
                "Unable to connect to the location service."
            ) from exc

        if not response.ok:
            raise LocationServiceError(
                f"Location service returned HTTP {response.status_code}."
            )

        try:
            data: dict[str, Any] = response.json()
        except ValueError as exc:
            raise LocationServiceError(
                "Location service returned invalid JSON."
            ) from exc

        try:
            latitude, longitude = data["loc"].split(",")
            return float(latitude), float(longitude)
        except (KeyError, ValueError) as exc:
            raise LocationServiceError(
                "Location service returned an invalid coordinate."
            ) from exc