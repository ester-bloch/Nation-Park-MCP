"""Pytest configuration and shared fixtures."""

from typing import Any, Dict

import pytest

from src.config import Settings


@pytest.fixture
def mock_settings() -> Settings:
    """Mock settings for testing."""
    return Settings(
        nps_api_key="test_api_key",
        nps_api_base_url="https://developer.nps.gov/api/v1",
        log_level="DEBUG",
        server_name="Test National Parks",
    )


@pytest.fixture
def mock_nps_response() -> Dict[str, Any]:
    """Mock NPS API response for testing."""
    return {
        "total": "1",
        "limit": "50",
        "start": "0",
        "data": [
            {
                "id": "77E0D7B0-1942-494A-ACE2-9004D2BDC59E",
                "url": "https://www.nps.gov/yell/index.htm",
                "fullName": "Yellowstone National Park",
                "parkCode": "yell",
                "description": "On March 1, 1872, Yellowstone became the first national park for all to enjoy the unique hydrothermal and geologic features.",
                "latitude": "44.59824417",
                "longitude": "-110.5471695",
                "latLong": "lat:44.59824417, long:-110.5471695",
                "states": "ID,MT,WY",
                "contacts": {
                    "phoneNumbers": [
                        {
                            "phoneNumber": "3073447381",
                            "description": "",
                            "extension": "",
                            "type": "Voice",
                        }
                    ],
                    "emailAddresses": [
                        {
                            "description": "",
                            "emailAddress": "yell_visitor_services@nps.gov",
                        }
                    ],
                },
                "entranceFees": [],
                "entrancePasses": [],
                "fees": [],
                "directionsInfo": "Yellowstone National Park is located in the northwest corner of Wyoming, and includes small areas of Montana and Idaho as well.",
                "directionsUrl": "http://www.nps.gov/yell/planyourvisit/directions.htm",
                "operatingHours": [
                    {
                        "exceptions": [],
                        "description": "Yellowstone is open 24 hours a day when open. However, services and roads are limited in winter.",
                        "standardHours": {
                            "wednesday": "All Day",
                            "monday": "All Day",
                            "thursday": "All Day",
                            "sunday": "All Day",
                            "tuesday": "All Day",
                            "friday": "All Day",
                            "saturday": "All Day",
                        },
                        "name": "Yellowstone National Park",
                    }
                ],
                "addresses": [
                    {
                        "postalCode": "82190",
                        "city": "Yellowstone National Park",
                        "stateCode": "WY",
                        "countryCode": "US",
                        "provinceTerritoryCode": "",
                        "line1": "PO Box 168",
                        "type": "Physical",
                        "line3": "",
                        "line2": "",
                    }
                ],
                "images": [
                    {
                        "credit": "Jim Peaco",
                        "title": "Bison",
                        "altText": "Bison walking on a road with snow covered ground",
                        "caption": "Bison are the largest mammals in Yellowstone National Park",
                        "url": "https://www.nps.gov/common/uploads/structured_data/3C7D2FBB-1DD8-B71B-0BED99731011CFCE.jpg",
                    }
                ],
                "weatherInfo": "Yellowstone's weather can vary dramatically, even within a single day.",
                "name": "Yellowstone",
                "designation": "National Park",
            }
        ],
    }
