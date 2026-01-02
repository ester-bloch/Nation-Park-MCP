"""FastMCP server setup and configuration."""

from typing import Any, Dict

from fastmcp import FastMCP
from pydantic import ValidationError as PydanticValidationError

from src.api.client import NPSAPIError
from src.config import settings
from src.handlers import (
    find_parks,
    geocode_location,
    get_air_quality,
    get_alerts,
    get_campgrounds,
    get_events,
    get_park_context,
    get_park_details,
    get_weather,
    get_visitor_centers,
    reverse_geocode,
)
from src.models.requests import (
    GeocodeLocationRequest,
    FindParksRequest,
    GetAlertsRequest,
    GetAirQualityRequest,
    GetCampgroundsRequest,
    GetEventsRequest,
    GetParkDetailsRequest,
    GetParkContextRequest,
    GetVisitorCentersRequest,
    GetWeatherRequest,
    ReverseGeocodeRequest,
)
from src.utils.error_handler import (
    handle_api_error,
    handle_generic_error,
    handle_validation_error,
)
from src.utils.logging import get_logger, log_request, log_response

# Set up structured logger
logger = get_logger(__name__)


class NationalParksServer:
    """National Parks MCP Server using FastMCP."""

    def __init__(self):
        """Initialize the FastMCP server."""
        self.mcp = FastMCP(name=settings.server_name)
        logger.info("server_initialized", server_name=settings.server_name)

        # Register all tools
        self._register_tools()
        logger.info("tools_registered", message="All tools registered with FastMCP")

    def _register_tools(self):
        """Register all tool handlers with FastMCP."""

        # Register find_parks tool
        @self.mcp.tool()
        def findParks(
            stateCode: str | None = None,
            q: str | None = None,
            limit: int | None = None,
            start: int | None = None,
            activities: str | None = None,
        ) -> Dict[str, Any]:
            """
            Search for national parks by state, activity, or keyword.

            Args:
                stateCode: Filter parks by state code (e.g., "CA" for California, "NY" for New York). Multiple states can be comma-separated (e.g., "CA,OR,WA")
                q: Search term to filter parks by name or description
                limit: Maximum number of parks to return (default: 10, max: 50)
                start: Start position for results (useful for pagination)
                activities: Filter by available activities (e.g., "hiking,camping")

            Returns:
                Dictionary containing park search results
            """
            # Log incoming request
            log_request(
                logger,
                "findParks",
                {
                    "stateCode": stateCode,
                    "q": q,
                    "limit": limit,
                    "start": start,
                    "activities": activities,
                },
            )

            try:
                request = FindParksRequest(
                    state_code=stateCode,
                    q=q,
                    limit=limit,
                    start=start,
                    activities=activities,
                )
                result = find_parks(request)

                # Log successful response
                response_size = (
                    result.get("total", 0) if isinstance(result, dict) else None
                )
                log_response(
                    logger, "findParks", success=True, response_size=response_size
                )

                return result
            except PydanticValidationError as e:
                # Handle validation errors with structured response
                log_response(
                    logger, "findParks", success=False, error="validation_error"
                )
                return handle_validation_error(e)
            except NPSAPIError as e:
                # Handle API errors with structured response
                log_response(logger, "findParks", success=False, error=e.error_type)
                return handle_api_error(e)
            except Exception as e:
                # Handle unexpected errors with structured response
                log_response(logger, "findParks", success=False, error="internal_error")
                return handle_generic_error(e, context={"tool": "findParks"})

        # Register get_park_details tool
        @self.mcp.tool()
        def getParkDetails(parkCode: str) -> Dict[str, Any]:
            """
            Get detailed information about a specific national park.

            Args:
                parkCode: The park code of the national park (e.g., "yose" for Yosemite, "grca" for Grand Canyon)

            Returns:
                Dictionary containing detailed park information
            """
            # Log incoming request
            log_request(logger, "getParkDetails", {"parkCode": parkCode})

            try:
                request = GetParkDetailsRequest(park_code=parkCode)
                result = get_park_details(request)

                # Log successful response
                log_response(logger, "getParkDetails", success=True)

                return result
            except PydanticValidationError as e:
                # Handle validation errors with structured response
                log_response(
                    logger, "getParkDetails", success=False, error="validation_error"
                )
                return handle_validation_error(e)
            except NPSAPIError as e:
                # Handle API errors with structured response
                log_response(
                    logger, "getParkDetails", success=False, error=e.error_type
                )
                return handle_api_error(e)
            except Exception as e:
                # Handle unexpected errors with structured response
                log_response(
                    logger, "getParkDetails", success=False, error="internal_error"
                )
                return handle_generic_error(e, context={"tool": "getParkDetails"})

        # Register get_alerts tool
        @self.mcp.tool()
        def getAlerts(
            parkCode: str | None = None,
            limit: int | None = None,
            start: int | None = None,
            q: str | None = None,
        ) -> Dict[str, Any]:
            """
            Get current alerts for parks (closures, hazards, important notices).

            Args:
                parkCode: Filter alerts by park code (e.g., "yose" for Yosemite). Multiple parks can be comma-separated (e.g., "yose,grca")
                limit: Maximum number of alerts to return (default: 10, max: 50)
                start: Start position for results (useful for pagination)
                q: Search term to filter alerts by title or description

            Returns:
                Dictionary containing alert data
            """
            # Log incoming request
            log_request(
                logger,
                "getAlerts",
                {"parkCode": parkCode, "limit": limit, "start": start, "q": q},
            )

            try:
                request = GetAlertsRequest(
                    park_code=parkCode,
                    limit=limit,
                    start=start,
                    q=q,
                )
                result = get_alerts(request)

                # Log successful response
                response_size = (
                    result.get("total", 0) if isinstance(result, dict) else None
                )
                log_response(
                    logger, "getAlerts", success=True, response_size=response_size
                )

                return result
            except PydanticValidationError as e:
                # Handle validation errors with structured response
                log_response(
                    logger, "getAlerts", success=False, error="validation_error"
                )
                return handle_validation_error(e)
            except NPSAPIError as e:
                # Handle API errors with structured response
                log_response(logger, "getAlerts", success=False, error=e.error_type)
                return handle_api_error(e)
            except Exception as e:
                # Handle unexpected errors with structured response
                log_response(logger, "getAlerts", success=False, error="internal_error")
                return handle_generic_error(e, context={"tool": "getAlerts"})

        # Register get_visitor_centers tool
        @self.mcp.tool()
        def getVisitorCenters(
            parkCode: str | None = None,
            limit: int | None = None,
            start: int | None = None,
            q: str | None = None,
        ) -> Dict[str, Any]:
            """
            Get visitor centers for parks with operating hours and contact information.

            Args:
                parkCode: Filter visitor centers by park code (e.g., "yose" for Yosemite). Multiple parks can be comma-separated (e.g., "yose,grca")
                limit: Maximum number of visitor centers to return (default: 10, max: 50)
                start: Start position for results (useful for pagination)
                q: Search term to filter visitor centers by name or description

            Returns:
                Dictionary containing visitor center data
            """
            # Log incoming request
            log_request(
                logger,
                "getVisitorCenters",
                {"parkCode": parkCode, "limit": limit, "start": start, "q": q},
            )

            try:
                request = GetVisitorCentersRequest(
                    park_code=parkCode,
                    limit=limit,
                    start=start,
                    q=q,
                )
                result = get_visitor_centers(request)

                # Log successful response
                response_size = (
                    result.get("total", 0) if isinstance(result, dict) else None
                )
                log_response(
                    logger,
                    "getVisitorCenters",
                    success=True,
                    response_size=response_size,
                )

                return result
            except PydanticValidationError as e:
                # Handle validation errors with structured response
                log_response(
                    logger, "getVisitorCenters", success=False, error="validation_error"
                )
                return handle_validation_error(e)
            except NPSAPIError as e:
                # Handle API errors with structured response
                log_response(
                    logger, "getVisitorCenters", success=False, error=e.error_type
                )
                return handle_api_error(e)
            except Exception as e:
                # Handle unexpected errors with structured response
                log_response(
                    logger, "getVisitorCenters", success=False, error="internal_error"
                )
                return handle_generic_error(e, context={"tool": "getVisitorCenters"})

        # Register get_campgrounds tool
        @self.mcp.tool()
        def getCampgrounds(
            parkCode: str | None = None,
            limit: int | None = None,
            start: int | None = None,
            q: str | None = None,
        ) -> Dict[str, Any]:
            """
            Get campgrounds for parks with amenities and availability information.

            Args:
                parkCode: Filter campgrounds by park code (e.g., "yose" for Yosemite). Multiple parks can be comma-separated (e.g., "yose,grca")
                limit: Maximum number of campgrounds to return (default: 10, max: 50)
                start: Start position for results (useful for pagination)
                q: Search term to filter campgrounds by name or description

            Returns:
                Dictionary containing campground data
            """
            # Log incoming request
            log_request(
                logger,
                "getCampgrounds",
                {"parkCode": parkCode, "limit": limit, "start": start, "q": q},
            )

            try:
                request = GetCampgroundsRequest(
                    park_code=parkCode,
                    limit=limit,
                    start=start,
                    q=q,
                )
                result = get_campgrounds(request)

                # Log successful response
                response_size = (
                    result.get("total", 0) if isinstance(result, dict) else None
                )
                log_response(
                    logger, "getCampgrounds", success=True, response_size=response_size
                )

                return result
            except PydanticValidationError as e:
                # Handle validation errors with structured response
                log_response(
                    logger, "getCampgrounds", success=False, error="validation_error"
                )
                return handle_validation_error(e)
            except NPSAPIError as e:
                # Handle API errors with structured response
                log_response(
                    logger, "getCampgrounds", success=False, error=e.error_type
                )
                return handle_api_error(e)
            except Exception as e:
                # Handle unexpected errors with structured response
                log_response(
                    logger, "getCampgrounds", success=False, error="internal_error"
                )
                return handle_generic_error(e, context={"tool": "getCampgrounds"})

        # Register get_events tool
        @self.mcp.tool()
        def getEvents(
            parkCode: str | None = None,
            limit: int | None = None,
            start: int | None = None,
            dateStart: str | None = None,
            dateEnd: str | None = None,
            q: str | None = None,
        ) -> Dict[str, Any]:
            """
            Get upcoming events and programs for parks.

            Args:
                parkCode: Filter events by park code (e.g., "yose" for Yosemite). Multiple parks can be comma-separated (e.g., "yose,grca")
                limit: Maximum number of events to return (default: 10, max: 50)
                start: Start position for results (useful for pagination)
                dateStart: Start date for filtering events (format: YYYY-MM-DD)
                dateEnd: End date for filtering events (format: YYYY-MM-DD)
                q: Search term to filter events by title or description

            Returns:
                Dictionary containing event data
            """
            # Log incoming request
            log_request(
                logger,
                "getEvents",
                {
                    "parkCode": parkCode,
                    "limit": limit,
                    "start": start,
                    "dateStart": dateStart,
                    "dateEnd": dateEnd,
                    "q": q,
                },
            )

            try:
                request = GetEventsRequest(
                    park_code=parkCode,
                    limit=limit,
                    start=start,
                    date_start=dateStart,
                    date_end=dateEnd,
                    q=q,
                )
                result = get_events(request)

                # Log successful response
                response_size = (
                    result.get("total", 0) if isinstance(result, dict) else None
                )
                log_response(
                    logger, "getEvents", success=True, response_size=response_size
                )

                return result
            except PydanticValidationError as e:
                # Handle validation errors with structured response
                log_response(
                    logger, "getEvents", success=False, error="validation_error"
                )
                return handle_validation_error(e)
            except NPSAPIError as e:
                # Handle API errors with structured response
                log_response(logger, "getEvents", success=False, error=e.error_type)
                return handle_api_error(e)
            except Exception as e:
                # Handle unexpected errors with structured response
                log_response(logger, "getEvents", success=False, error="internal_error")
                return handle_generic_error(e, context={"tool": "getEvents"})

        # Register geocode_location tool
        @self.mcp.tool()
        def geocodeLocation(q: str, limit: int | None = None) -> Dict[str, Any]:
            """
            Geocode a location name or address into coordinates.

            Args:
                q: Location query to geocode (address, place name, or landmark)
                limit: Maximum number of results to return (default: 5, max: 10)

            Returns:
                Dictionary containing geocoding results
            """
            log_request(logger, "geocodeLocation", {"q": q, "limit": limit})

            try:
                request = GeocodeLocationRequest(q=q, limit=limit)
                result = geocode_location(request)
                log_response(
                    logger,
                    "geocodeLocation",
                    success=True,
                    response_size=result.get("count") if isinstance(result, dict) else None,
                )
                return result
            except PydanticValidationError as e:
                log_response(
                    logger, "geocodeLocation", success=False, error="validation_error"
                )
                return handle_validation_error(e)
            except NPSAPIError as e:
                log_response(logger, "geocodeLocation", success=False, error=e.error_type)
                return handle_api_error(e)
            except Exception as e:
                log_response(
                    logger, "geocodeLocation", success=False, error="internal_error"
                )
                return handle_generic_error(e, context={"tool": "geocodeLocation"})

        # Register reverse_geocode tool
        @self.mcp.tool()
        def reverseGeocode(latitude: float, longitude: float) -> Dict[str, Any]:
            """
            Reverse geocode coordinates into a structured address.

            Args:
                latitude: Latitude of the location
                longitude: Longitude of the location

            Returns:
                Dictionary containing reverse geocode results
            """
            log_request(
                logger,
                "reverseGeocode",
                {"latitude": latitude, "longitude": longitude},
            )

            try:
                request = ReverseGeocodeRequest(
                    latitude=latitude, longitude=longitude
                )
                result = reverse_geocode(request)
                log_response(logger, "reverseGeocode", success=True)
                return result
            except PydanticValidationError as e:
                log_response(
                    logger, "reverseGeocode", success=False, error="validation_error"
                )
                return handle_validation_error(e)
            except NPSAPIError as e:
                log_response(logger, "reverseGeocode", success=False, error=e.error_type)
                return handle_api_error(e)
            except Exception as e:
                log_response(
                    logger, "reverseGeocode", success=False, error="internal_error"
                )
                return handle_generic_error(e, context={"tool": "reverseGeocode"})

        # Register get_weather tool
        @self.mcp.tool()
        def getWeather(
            latitude: float,
            longitude: float,
            units: str | None = None,
            language: str | None = None,
        ) -> Dict[str, Any]:
            """
            Get current weather for a given location.

            Args:
                latitude: Latitude for the weather lookup
                longitude: Longitude for the weather lookup
                units: Units system ("metric" or "imperial")
                language: Language code for localized conditions (OpenWeather only)

            Returns:
                Dictionary containing weather data
            """
            log_request(
                logger,
                "getWeather",
                {
                    "latitude": latitude,
                    "longitude": longitude,
                    "units": units,
                    "language": language,
                },
            )

            try:
                request = GetWeatherRequest(
                    latitude=latitude,
                    longitude=longitude,
                    units=units,
                    language=language,
                )
                result = get_weather(request)
                log_response(logger, "getWeather", success=True)
                return result
            except PydanticValidationError as e:
                log_response(logger, "getWeather", success=False, error="validation_error")
                return handle_validation_error(e)
            except NPSAPIError as e:
                log_response(logger, "getWeather", success=False, error=e.error_type)
                return handle_api_error(e)
            except Exception as e:
                log_response(logger, "getWeather", success=False, error="internal_error")
                return handle_generic_error(e, context={"tool": "getWeather"})

        # Register get_air_quality tool
        @self.mcp.tool()
        def getAirQuality(latitude: float, longitude: float) -> Dict[str, Any]:
            """
            Get air quality data for a given location.

            Args:
                latitude: Latitude for the air quality lookup
                longitude: Longitude for the air quality lookup

            Returns:
                Dictionary containing air quality data
            """
            log_request(
                logger,
                "getAirQuality",
                {"latitude": latitude, "longitude": longitude},
            )

            try:
                request = GetAirQualityRequest(
                    latitude=latitude,
                    longitude=longitude,
                )
                result = get_air_quality(request)
                log_response(logger, "getAirQuality", success=True)
                return result
            except PydanticValidationError as e:
                log_response(
                    logger, "getAirQuality", success=False, error="validation_error"
                )
                return handle_validation_error(e)
            except NPSAPIError as e:
                log_response(logger, "getAirQuality", success=False, error=e.error_type)
                return handle_api_error(e)
            except Exception as e:
                log_response(
                    logger, "getAirQuality", success=False, error="internal_error"
                )
                return handle_generic_error(e, context={"tool": "getAirQuality"})

        # Register get_park_context tool
        @self.mcp.tool()
        def getParkContext(
            parkCode: str,
            units: str | None = None,
        ) -> Dict[str, Any]:
            """
            Get combined park, weather, and air quality context.

            Args:
                parkCode: Park code to build the context
                units: Units system for weather ("metric" or "imperial")

            Returns:
                Dictionary containing combined park context
            """
            log_request(
                logger,
                "getParkContext",
                {"parkCode": parkCode, "units": units},
            )

            try:
                request = GetParkContextRequest(parkCode=parkCode, units=units)
                result = get_park_context(request)
                log_response(logger, "getParkContext", success=True)
                return result
            except PydanticValidationError as e:
                log_response(
                    logger, "getParkContext", success=False, error="validation_error"
                )
                return handle_validation_error(e)
            except NPSAPIError as e:
                log_response(logger, "getParkContext", success=False, error=e.error_type)
                return handle_api_error(e)
            except Exception as e:
                log_response(
                    logger, "getParkContext", success=False, error="internal_error"
                )
                return handle_generic_error(e, context={"tool": "getParkContext"})

    def run(self):
        """Run the server with stdio transport."""
        logger.info("server_starting", transport="stdio")
        try:
            # Run the server - FastMCP handles stdio transport by default
            self.mcp.run()
        except KeyboardInterrupt:
            logger.info("server_shutdown", reason="keyboard_interrupt")
        except Exception as e:
            logger.error("server_error", error=str(e), exc_info=True)
            raise


# Global server instance
_server: NationalParksServer | None = None


def get_server() -> NationalParksServer:
    """
    Get or create the global server instance.

    Returns:
        NationalParksServer instance
    """
    global _server
    if _server is None:
        _server = NationalParksServer()
    return _server
