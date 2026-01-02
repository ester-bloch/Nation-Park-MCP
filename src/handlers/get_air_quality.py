"""Handler for air quality lookup."""

from typing import Any, Dict

from src.api.air_quality import get_air_quality_client
from src.api.client import NPSAPIError
from src.models.requests import GetAirQualityRequest
from src.utils.error_handler import handle_generic_error
from src.utils.logging import get_logger

logger = get_logger(__name__)


def build_air_quality_response(latitude: float, longitude: float) -> Dict[str, Any]:
    client = get_air_quality_client()
    data = client.get_nearest_city(latitude, longitude)
    payload = data.get("data", {}) if isinstance(data, dict) else {}

    location = {
        "city": payload.get("city"),
        "state": payload.get("state"),
        "country": payload.get("country"),
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude,
        },
    }

    current = payload.get("current", {})
    pollution = current.get("pollution", {})
    weather = current.get("weather", {})

    return {
        "location": location,
        "current": {
            "pollution": {
                "timestamp": pollution.get("ts"),
                "aqius": pollution.get("aqius"),
                "mainus": pollution.get("mainus"),
                "aqicn": pollution.get("aqicn"),
                "maincn": pollution.get("maincn"),
            },
            "weather": {
                "timestamp": weather.get("ts"),
                "temperature": weather.get("tp"),
                "pressure": weather.get("pr"),
                "humidity": weather.get("hu"),
                "windSpeed": weather.get("ws"),
                "windDirection": weather.get("wd"),
                "icon": weather.get("ic"),
            },
        },
        "source": {"provider": "AirVisual"},
    }


def get_air_quality(request: GetAirQualityRequest) -> Dict[str, Any]:
    """
    Get air quality data for a given latitude and longitude.

    Args:
        request: GetAirQualityRequest with coordinates

    Returns:
        Dictionary with air quality response
    """
    logger.info(
        "get_air_quality",
        latitude=request.latitude,
        longitude=request.longitude,
    )

    try:
        return build_air_quality_response(request.latitude, request.longitude)
    except NPSAPIError as exc:
        logger.error("air_quality_failed", error=exc.message, error_type=exc.error_type)
        raise
    except Exception as exc:
        logger.error("air_quality_unexpected_error", error=str(exc), exc_info=True)
        return handle_generic_error(exc, context={"tool": "getAirQuality"})
