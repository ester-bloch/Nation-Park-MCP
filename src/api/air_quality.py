"""Air quality API client for AirVisual."""

from typing import Any, Dict, Optional

from src.api.client import NPSAPIError
from src.api.external_client import ExternalAPIClient
from src.config import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


class AirQualityClient:
    """Client for AirVisual API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key or settings.airvisual_api_key
        self.client = ExternalAPIClient(base_url=base_url or settings.airvisual_base_url)
        logger.info("airvisual_client_initialized")

    def get_nearest_city(self, latitude: float, longitude: float) -> Dict[str, Any]:
        if not self.api_key:
            raise NPSAPIError(
                message="AirVisual API key not configured",
                error_type="missing_api_key",
                details={"provider": "AirVisual"},
            )

        params = {"lat": latitude, "lon": longitude, "key": self.api_key}
        return self.client.get("/nearest_city", params=params)


_client: Optional[AirQualityClient] = None


def get_air_quality_client() -> AirQualityClient:
    """Get or create the global AirVisual client."""
    global _client
    if _client is None:
        _client = AirQualityClient()
    return _client
