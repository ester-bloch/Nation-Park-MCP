"""Handler for combined park context."""

from datetime import datetime, timezone
from typing import Any, Dict

from src.api.client import NPSAPIError
from src.handlers.get_air_quality import build_air_quality_response
from src.handlers.get_park_details import get_park_details
from src.handlers.get_weather import build_weather_response
from src.models.errors import ErrorResponse
from src.models.requests import GetParkContextRequest, GetParkDetailsRequest
from src.utils.error_handler import handle_generic_error
from src.utils.logging import get_logger

logger = get_logger(__name__)


def _parse_coordinate(value: Any) -> float | None:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _build_error(message: str, context: Dict[str, Any]) -> Dict[str, Any]:
    response = ErrorResponse(
        error="context_error",
        message=message,
        details=context,
    )
    return response.model_dump()


def get_park_context(request: GetParkContextRequest) -> Dict[str, Any]:
    """
    Get combined park, weather, and air quality context.

    Args:
        request: GetParkContextRequest with park code and optional units

    Returns:
        Dictionary with full context response
    """
    logger.info("get_park_context", park_code=request.park_code, units=request.units)

    try:
        park_details = get_park_details(
            GetParkDetailsRequest(park_code=request.park_code)
        )
        if isinstance(park_details, dict) and park_details.get("error"):
            return park_details

        location = park_details.get("location", {}) if isinstance(park_details, dict) else {}
        latitude = _parse_coordinate(location.get("latitude"))
        longitude = _parse_coordinate(location.get("longitude"))

        if latitude is None or longitude is None:
            return _build_error(
                "Park location coordinates are unavailable for this park.",
                {"parkCode": request.park_code},
            )

        weather = build_weather_response(
            latitude,
            longitude,
            request.units or "metric",
            None,
        )

        try:
            air_quality = build_air_quality_response(latitude, longitude)
        except NPSAPIError as exc:
            air_quality = ErrorResponse(
                error=exc.error_type,
                message=exc.message,
                details=exc.details,
            ).model_dump()

        return {
            "park": park_details,
            "location": {"latitude": latitude, "longitude": longitude},
            "weather": weather,
            "airQuality": air_quality,
            "contextGeneratedAt": datetime.now(timezone.utc).isoformat(),
        }
    except NPSAPIError as exc:
        logger.error("park_context_failed", error=exc.message, error_type=exc.error_type)
        raise
    except Exception as exc:
        logger.error("park_context_failed", error=str(exc), exc_info=True)
        return handle_generic_error(exc, context={"tool": "getParkContext"})
