"""Unit tests for external tool handlers."""

from unittest.mock import Mock, patch

from src.api.client import NPSAPIError
from src.handlers.geocode_location import geocode_location
from src.handlers.get_air_quality import get_air_quality
from src.handlers.get_park_context import get_park_context
from src.handlers.get_weather import get_weather
from src.handlers.reverse_geocode import reverse_geocode
from src.models.requests import (
    GeocodeLocationRequest,
    GetAirQualityRequest,
    GetParkContextRequest,
    GetWeatherRequest,
    ReverseGeocodeRequest,
)


def test_geocode_location_success():
    mock_client = Mock()
    mock_client.search.return_value = [
        {
            "display_name": "Yosemite National Park, California, USA",
            "lat": "37.8651011",
            "lon": "-119.5383294",
            "category": "boundary",
            "type": "national_park",
            "importance": 0.9,
            "address": {"state": "California"},
        }
    ]

    with patch("src.handlers.geocode_location.get_geocode_client") as mock_get_client:
        mock_get_client.return_value = mock_client
        request = GeocodeLocationRequest(q="Yosemite", limit=1)
        result = geocode_location(request)

    assert result["count"] == 1
    assert result["locations"][0]["displayName"].startswith("Yosemite")
    assert result["locations"][0]["latitude"] == 37.8651011


def test_reverse_geocode_success():
    mock_client = Mock()
    mock_client.reverse.return_value = {
        "place_id": 12345,
        "display_name": "Yosemite Valley, CA, USA",
        "lat": "37.745",
        "lon": "-119.593",
        "category": "place",
        "type": "valley",
        "address": {"state": "California"},
    }

    with patch("src.handlers.reverse_geocode.get_geocode_client") as mock_get_client:
        mock_get_client.return_value = mock_client
        request = ReverseGeocodeRequest(latitude=37.745, longitude=-119.593)
        result = reverse_geocode(request)

    assert result["displayName"] == "Yosemite Valley, CA, USA"
    assert result["latitude"] == 37.745


def test_get_weather_openweather_success():
    mock_client = Mock()
    mock_client.get_openweather_current.return_value = {
        "main": {"temp": 20, "feels_like": 18, "humidity": 50, "pressure": 1012},
        "weather": [{"main": "Clear", "description": "clear sky"}],
        "wind": {"speed": 3.5, "deg": 200},
        "dt": 1710000000,
    }

    with patch("src.handlers.get_weather.get_weather_client") as mock_get_client:
        mock_get_client.return_value = mock_client
        request = GetWeatherRequest(latitude=37.0, longitude=-119.0, units="metric")
        result = get_weather(request)

    assert result["source"]["provider"] == "OpenWeather"
    assert result["current"]["temperature"] == 20


def test_get_weather_fallback_to_open_meteo():
    mock_client = Mock()
    mock_client.get_openweather_current.side_effect = NPSAPIError(
        message="OpenWeather down", error_type="http_error"
    )
    mock_client.get_open_meteo_current.return_value = {
        "current_units": {"temperature_2m": "C", "wind_speed_10m": "m/s"},
        "current": {
            "temperature_2m": 21,
            "relative_humidity_2m": 40,
            "apparent_temperature": 20,
            "wind_speed_10m": 4,
            "wind_direction_10m": 180,
            "weather_code": 2,
            "time": "2024-03-10T12:00",
        },
    }

    with patch("src.handlers.get_weather.get_weather_client") as mock_get_client:
        mock_get_client.return_value = mock_client
        request = GetWeatherRequest(latitude=37.0, longitude=-119.0, units="metric")
        result = get_weather(request)

    assert result["source"]["provider"] == "Open-Meteo"
    assert result["current"]["temperature"] == 21


def test_get_air_quality_success():
    mock_client = Mock()
    mock_client.get_nearest_city.return_value = {
        "data": {
            "city": "Yosemite Valley",
            "state": "California",
            "country": "USA",
            "current": {
                "pollution": {"ts": "2024-03-10T12:00", "aqius": 30},
                "weather": {"tp": 18, "hu": 45, "ws": 2.5, "wd": 90, "ic": "01d"},
            },
        }
    }

    with patch("src.handlers.get_air_quality.get_air_quality_client") as mock_get_client:
        mock_get_client.return_value = mock_client
        request = GetAirQualityRequest(latitude=37.0, longitude=-119.0)
        result = get_air_quality(request)

    assert result["location"]["city"] == "Yosemite Valley"
    assert result["current"]["pollution"]["aqius"] == 30


def test_get_park_context_combines_sources():
    park_details = {
        "name": "Yosemite National Park",
        "location": {"latitude": "37.8651", "longitude": "-119.5383"},
    }

    with (
        patch("src.handlers.get_park_context.get_park_details") as mock_get_park_details,
        patch(
            "src.handlers.get_park_context.build_weather_response"
        ) as mock_weather,
        patch(
            "src.handlers.get_park_context.build_air_quality_response"
        ) as mock_air_quality,
    ):
        mock_get_park_details.return_value = park_details
        mock_weather.return_value = {"source": {"provider": "OpenWeather"}}
        mock_air_quality.return_value = {"source": {"provider": "AirVisual"}}

        request = GetParkContextRequest(parkCode="yose", units="metric")
        result = get_park_context(request)

    assert result["park"]["name"] == "Yosemite National Park"
    assert result["weather"]["source"]["provider"] == "OpenWeather"
    assert result["airQuality"]["source"]["provider"] == "AirVisual"
