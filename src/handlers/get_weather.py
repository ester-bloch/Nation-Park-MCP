"""Handler for weather lookup."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from src.api.client import NPSAPIError
from src.api.weather import get_weather_client
from src.models.requests import GetWeatherRequest
from src.utils.error_handler import handle_generic_error
from src.utils.logging import get_logger

logger = get_logger(__name__)


def _openweather_units(units: str) -> Dict[str, str]:
    if units == "imperial":
        return {"temperature": "F", "windSpeed": "mph"}
    return {"temperature": "C", "windSpeed": "m/s"}


def _openweather_timestamp(timestamp: Optional[int]) -> Optional[str]:
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def _normalize_openweather(
    data: Dict[str, Any], units: str, latitude: float, longitude: float
) -> Dict[str, Any]:
    main = data.get("main", {})
    weather = (data.get("weather") or [{}])[0]
    wind = data.get("wind", {})

    return {
        "location": {"latitude": latitude, "longitude": longitude},
        "units": _openweather_units(units),
        "current": {
            "temperature": main.get("temp"),
            "feelsLike": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "windSpeed": wind.get("speed"),
            "windDirection": wind.get("deg"),
            "condition": weather.get("main"),
            "description": weather.get("description"),
            "timestamp": _openweather_timestamp(data.get("dt")),
        },
        "source": {"provider": "OpenWeather", "fallback": False},
    }


def _normalize_open_meteo(
    data: Dict[str, Any], units: str, latitude: float, longitude: float
) -> Dict[str, Any]:
    current = data.get("current", {})
    units_map = data.get("current_units", {})

    return {
        "location": {"latitude": latitude, "longitude": longitude},
        "units": {
            "temperature": units_map.get("temperature_2m", "C"),
            "windSpeed": units_map.get("wind_speed_10m", "m/s"),
        },
        "current": {
            "temperature": current.get("temperature_2m"),
            "feelsLike": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "windSpeed": current.get("wind_speed_10m"),
            "windDirection": current.get("wind_direction_10m"),
            "conditionCode": current.get("weather_code"),
            "timestamp": current.get("time"),
        },
        "source": {"provider": "Open-Meteo", "fallback": True, "units": units},
    }


def build_weather_response(
    latitude: float, longitude: float, units: str, language: Optional[str]
) -> Dict[str, Any]:
    client = get_weather_client()

    try:
        data = client.get_openweather_current(latitude, longitude, units, language)
        return _normalize_openweather(data, units, latitude, longitude)
    except NPSAPIError as exc:
        logger.warning(
            "openweather_failed",
            error=exc.message,
            error_type=exc.error_type,
        )

    data = client.get_open_meteo_current(latitude, longitude, units)
    response = _normalize_open_meteo(data, units, latitude, longitude)
    response["source"]["fallbackReason"] = "OpenWeather unavailable"
    return response


def get_weather(request: GetWeatherRequest) -> Dict[str, Any]:
    """
    Get current weather for a given latitude and longitude.

    Args:
        request: GetWeatherRequest with coordinates and units

    Returns:
        Dictionary with weather response
    """
    logger.info(
        "get_weather",
        latitude=request.latitude,
        longitude=request.longitude,
        units=request.units,
    )

    try:
        return build_weather_response(
            request.latitude,
            request.longitude,
            request.units or "metric",
            request.language,
        )
    except NPSAPIError as exc:
        logger.error("weather_failed", error=exc.message, error_type=exc.error_type)
        raise
    except Exception as exc:
        logger.error("weather_unexpected_error", error=str(exc), exc_info=True)
        return handle_generic_error(exc, context={"tool": "getWeather"})
