"""Weather API clients with OpenWeather and Open-Meteo support."""

from typing import Any, Dict, Optional

from src.api.client import NPSAPIError
from src.api.external_client import ExternalAPIClient
from src.config import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


class WeatherClient:
    """Client for weather providers."""

    def __init__(
        self,
        openweather_api_key: Optional[str] = None,
        openweather_base_url: Optional[str] = None,
        openmeteo_base_url: Optional[str] = None,
    ):
        self.openweather_api_key = openweather_api_key or settings.openweather_api_key
        self.openweather_client = ExternalAPIClient(
            base_url=openweather_base_url or settings.openweather_base_url
        )
        self.openmeteo_client = ExternalAPIClient(
            base_url=openmeteo_base_url or settings.openmeteo_base_url,
            enable_retry=False,
        )

    def get_openweather_current(
        self, latitude: float, longitude: float, units: str, language: Optional[str]
    ) -> Dict[str, Any]:
        if not self.openweather_api_key:
            raise NPSAPIError(
                message="OpenWeather API key not configured",
                error_type="missing_api_key",
                details={"provider": "OpenWeather"},
            )

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.openweather_api_key,
            "units": units,
        }
        if language:
            params["lang"] = language

        return self.openweather_client.get("/weather", params=params)

    def get_open_meteo_current(
        self, latitude: float, longitude: float, units: str
    ) -> Dict[str, Any]:
        current_fields = [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "wind_speed_10m",
            "wind_direction_10m",
            "weather_code",
        ]
        params: Dict[str, Any] = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(current_fields),
        }

        if units == "imperial":
            params["temperature_unit"] = "fahrenheit"
            params["wind_speed_unit"] = "mph"

        return self.openmeteo_client.get("/forecast", params=params)


_client: Optional[WeatherClient] = None


def get_weather_client() -> WeatherClient:
    """Get or create the global weather client."""
    global _client
    if _client is None:
        _client = WeatherClient()
    return _client
