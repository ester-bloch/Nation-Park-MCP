"""Pydantic models for tool input validation."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FindParksRequest(BaseModel):
    """Request model for finding parks."""

    model_config = ConfigDict(populate_by_name=True)

    state_code: Optional[str] = Field(
        None,
        alias="stateCode",
        description='Filter parks by state code (e.g., "CA" for California, "NY" for New York). Multiple states can be comma-separated (e.g., "CA,OR,WA")',
    )
    q: Optional[str] = Field(
        None,
        description="Search term to filter parks by name or description",
    )
    limit: Optional[int] = Field(
        None,
        description="Maximum number of parks to return (default: 10, max: 50)",
        ge=1,
        le=50,
    )
    start: Optional[int] = Field(
        None,
        description="Start position for results (useful for pagination)",
        ge=0,
    )
    activities: Optional[str] = Field(
        None,
        description='Filter by available activities (e.g., "hiking,camping")',
    )


class GetParkDetailsRequest(BaseModel):
    """Request model for getting park details."""

    model_config = ConfigDict(populate_by_name=True)

    park_code: str = Field(
        ...,
        alias="parkCode",
        description='The park code of the national park (e.g., "yose" for Yosemite, "grca" for Grand Canyon)',
        min_length=1,
    )


class GetAlertsRequest(BaseModel):
    """Request model for getting park alerts."""

    model_config = ConfigDict(populate_by_name=True)

    park_code: Optional[str] = Field(
        None,
        alias="parkCode",
        description='Filter alerts by park code (e.g., "yose" for Yosemite). Multiple parks can be comma-separated (e.g., "yose,grca").',
    )
    limit: Optional[int] = Field(
        None,
        description="Maximum number of alerts to return (default: 10, max: 50)",
        ge=1,
        le=50,
    )
    start: Optional[int] = Field(
        None,
        description="Start position for results (useful for pagination)",
        ge=0,
    )
    q: Optional[str] = Field(
        None,
        description="Search term to filter alerts by title or description",
    )


class GetVisitorCentersRequest(BaseModel):
    """Request model for getting visitor centers."""

    model_config = ConfigDict(populate_by_name=True)

    park_code: Optional[str] = Field(
        None,
        alias="parkCode",
        description='Filter visitor centers by park code (e.g., "yose" for Yosemite). Multiple parks can be comma-separated (e.g., "yose,grca").',
    )
    limit: Optional[int] = Field(
        None,
        description="Maximum number of visitor centers to return (default: 10, max: 50)",
        ge=1,
        le=50,
    )
    start: Optional[int] = Field(
        None,
        description="Start position for results (useful for pagination)",
        ge=0,
    )
    q: Optional[str] = Field(
        None,
        description="Search term to filter visitor centers by name or description",
    )


class GetCampgroundsRequest(BaseModel):
    """Request model for getting campgrounds."""

    model_config = ConfigDict(populate_by_name=True)

    park_code: Optional[str] = Field(
        None,
        alias="parkCode",
        description='Filter campgrounds by park code (e.g., "yose" for Yosemite). Multiple parks can be comma-separated (e.g., "yose,grca").',
    )
    limit: Optional[int] = Field(
        None,
        description="Maximum number of campgrounds to return (default: 10, max: 50)",
        ge=1,
        le=50,
    )
    start: Optional[int] = Field(
        None,
        description="Start position for results (useful for pagination)",
        ge=0,
    )
    q: Optional[str] = Field(
        None,
        description="Search term to filter campgrounds by name or description",
    )


class GetEventsRequest(BaseModel):
    """Request model for getting park events."""

    model_config = ConfigDict(populate_by_name=True)

    park_code: Optional[str] = Field(
        None,
        alias="parkCode",
        description='Filter events by park code (e.g., "yose" for Yosemite). Multiple parks can be comma-separated (e.g., "yose,grca").',
    )
    limit: Optional[int] = Field(
        None,
        description="Maximum number of events to return (default: 10, max: 50)",
        ge=1,
        le=50,
    )
    start: Optional[int] = Field(
        None,
        description="Start position for results (useful for pagination)",
        ge=0,
    )
    date_start: Optional[str] = Field(
        None,
        alias="dateStart",
        description="Start date for filtering events (format: YYYY-MM-DD)",
    )
    date_end: Optional[str] = Field(
        None,
        alias="dateEnd",
        description="End date for filtering events (format: YYYY-MM-DD)",
    )
    q: Optional[str] = Field(
        None,
        description="Search term to filter events by title or description",
    )


class GeocodeLocationRequest(BaseModel):
    """Request model for geocoding a location name or address."""

    model_config = ConfigDict(populate_by_name=True)

    query: str = Field(
        ...,
        alias="q",
        description="Location query to geocode (address, place name, or landmark)",
        min_length=1,
    )
    limit: Optional[int] = Field(
        5,
        description="Maximum number of results to return (default: 5, max: 10)",
        ge=1,
        le=10,
    )


class ReverseGeocodeRequest(BaseModel):
    """Request model for reverse geocoding coordinates."""

    model_config = ConfigDict(populate_by_name=True)

    latitude: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitude of the location to reverse geocode",
    )
    longitude: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitude of the location to reverse geocode",
    )


class GetWeatherRequest(BaseModel):
    """Request model for weather lookup."""

    model_config = ConfigDict(populate_by_name=True)

    latitude: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitude for the weather lookup",
    )
    longitude: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitude for the weather lookup",
    )
    units: Optional[str] = Field(
        "metric",
        description='Units system ("metric" or "imperial")',
        pattern="^(metric|imperial)$",
    )
    language: Optional[str] = Field(
        None,
        description="Language code for localized conditions (OpenWeather only)",
        min_length=2,
        max_length=5,
    )


class GetAirQualityRequest(BaseModel):
    """Request model for air quality lookup."""

    model_config = ConfigDict(populate_by_name=True)

    latitude: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitude for the air quality lookup",
    )
    longitude: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitude for the air quality lookup",
    )


class GetParkContextRequest(BaseModel):
    """Request model for combined park context."""

    model_config = ConfigDict(populate_by_name=True)

    park_code: str = Field(
        ...,
        alias="parkCode",
        description="Park code to build the full context",
        min_length=1,
    )
    units: Optional[str] = Field(
        "metric",
        description='Units system for weather ("metric" or "imperial")',
        pattern="^(metric|imperial)$",
    )
