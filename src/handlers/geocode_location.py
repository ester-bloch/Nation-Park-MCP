"""Handler for geocoding locations."""

from typing import Any, Dict, List

from src.api.client import NPSAPIError
from src.api.geocoding import get_geocode_client
from src.models.requests import GeocodeLocationRequest
from src.utils.error_handler import handle_generic_error
from src.utils.logging import get_logger

logger = get_logger(__name__)


def _format_geocode_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    formatted = []
    for item in results:
        formatted.append(
            {
                "name": item.get("name") or item.get("display_name"),
                "displayName": item.get("display_name"),
                "latitude": float(item["lat"]) if item.get("lat") else None,
                "longitude": float(item["lon"]) if item.get("lon") else None,
                "category": item.get("category"),
                "type": item.get("type"),
                "importance": item.get("importance"),
                "boundingBox": item.get("boundingbox"),
                "address": item.get("address", {}),
            }
        )
    return formatted


def geocode_location(request: GeocodeLocationRequest) -> Dict[str, Any]:
    """
    Geocode a location name or address into coordinates.

    Args:
        request: GeocodeLocationRequest with search query and limit

    Returns:
        Dictionary with geocoding results
    """
    logger.info(
        "geocode_location",
        query=request.query,
        limit=request.limit,
    )

    client = get_geocode_client()

    try:
        results = client.search(request.query, limit=request.limit or 5)
    except NPSAPIError as exc:
        logger.error("geocode_failed", error=exc.message, error_type=exc.error_type)
        raise
    except Exception as exc:
        logger.error("geocode_unexpected_error", error=str(exc), exc_info=True)
        return handle_generic_error(exc, context={"tool": "geocodeLocation"})

    formatted_results = _format_geocode_results(results)
    return {
        "count": len(formatted_results),
        "locations": formatted_results,
        "source": {"provider": "Nominatim"},
    }
