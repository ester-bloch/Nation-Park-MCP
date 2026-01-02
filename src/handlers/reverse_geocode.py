"""Handler for reverse geocoding."""

from typing import Any, Dict

from src.api.client import NPSAPIError
from src.api.geocoding import get_geocode_client
from src.models.requests import ReverseGeocodeRequest
from src.utils.error_handler import handle_generic_error
from src.utils.logging import get_logger

logger = get_logger(__name__)


def reverse_geocode(request: ReverseGeocodeRequest) -> Dict[str, Any]:
    """
    Reverse geocode coordinates into a structured address.

    Args:
        request: ReverseGeocodeRequest with latitude/longitude

    Returns:
        Dictionary with reverse geocode result
    """
    logger.info(
        "reverse_geocode",
        latitude=request.latitude,
        longitude=request.longitude,
    )

    client = get_geocode_client()

    try:
        result = client.reverse(request.latitude, request.longitude)
    except NPSAPIError as exc:
        logger.error("reverse_geocode_failed", error=exc.message, error_type=exc.error_type)
        raise
    except Exception as exc:
        logger.error("reverse_geocode_unexpected_error", error=str(exc), exc_info=True)
        return handle_generic_error(exc, context={"tool": "reverseGeocode"})

    if not result:
        return {
            "error": "not_found",
            "message": "No reverse geocode result found for the coordinates provided.",
        }

    return {
        "placeId": result.get("place_id"),
        "displayName": result.get("display_name"),
        "latitude": float(result["lat"]) if result.get("lat") else None,
        "longitude": float(result["lon"]) if result.get("lon") else None,
        "category": result.get("category"),
        "type": result.get("type"),
        "address": result.get("address", {}),
        "source": {"provider": "Nominatim"},
    }
