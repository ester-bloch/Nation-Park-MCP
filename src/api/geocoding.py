"""Nominatim geocoding client."""

from typing import Any, Dict, Optional

from src.api.external_client import ExternalAPIClient
from src.config import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


class NominatimClient:
    """Client for Nominatim geocoding APIs."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        user_agent: Optional[str] = None,
        contact_email: Optional[str] = None,
    ):
        self.base_url = base_url or settings.nominatim_base_url
        self.user_agent = user_agent or settings.nominatim_user_agent
        self.contact_email = contact_email or settings.nominatim_contact_email

        headers = {}
        if self.user_agent:
            headers["User-Agent"] = self.user_agent

        self.client = ExternalAPIClient(base_url=self.base_url, headers=headers)
        logger.info("nominatim_client_initialized", base_url=self.base_url)

    def search(self, query: str, limit: int = 5) -> list[Dict[str, Any]]:
        params = {
            "q": query,
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": limit,
        }
        if self.contact_email:
            params["email"] = self.contact_email

        data = self.client.get("/search", params=params)
        if not isinstance(data, list):
            logger.warning("nominatim_unexpected_response", response_type=type(data))
            return []
        return data

    def reverse(self, latitude: float, longitude: float) -> Dict[str, Any]:
        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "jsonv2",
            "addressdetails": 1,
        }
        if self.contact_email:
            params["email"] = self.contact_email

        data = self.client.get("/reverse", params=params)
        if not isinstance(data, dict):
            logger.warning("nominatim_unexpected_response", response_type=type(data))
            return {}
        return data


_client: Optional[NominatimClient] = None


def get_geocode_client() -> NominatimClient:
    """Get or create the global Nominatim client."""
    global _client
    if _client is None:
        _client = NominatimClient()
    return _client
