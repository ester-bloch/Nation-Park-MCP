"""Tests for configuration management."""

import os
from unittest.mock import patch

from src.config import Settings


def test_settings_default_values() -> None:
    """Test that settings have correct default values."""
    settings = Settings()

    assert settings.nps_api_base_url == "https://developer.nps.gov/api/v1"
    assert settings.nominatim_base_url == "https://nominatim.openstreetmap.org"
    assert settings.openweather_base_url == "https://api.openweathermap.org/data/2.5"
    assert settings.openmeteo_base_url == "https://api.open-meteo.com/v1"
    assert settings.airvisual_base_url == "https://api.airvisual.com/v2"
    assert settings.log_level == "INFO"
    assert settings.server_name == "National Parks"
    assert settings.nps_api_key is None
    assert settings.openweather_api_key is None
    assert settings.airvisual_api_key is None


def test_settings_from_environment() -> None:
    """Test that settings can be loaded from environment variables."""
    with patch.dict(
        os.environ,
        {
            "NPS_API_KEY": "test_key_123",
            "LOG_LEVEL": "DEBUG",
            "SERVER_NAME": "Test Server",
            "OPENWEATHER_API_KEY": "weather_key",
            "AIRVISUAL_API_KEY": "air_key",
        },
    ):
        settings = Settings()

        assert settings.nps_api_key == "test_key_123"
        assert settings.log_level == "DEBUG"
        assert settings.server_name == "Test Server"
        assert settings.openweather_api_key == "weather_key"
        assert settings.airvisual_api_key == "air_key"


def test_settings_case_insensitive() -> None:
    """Test that environment variables are case insensitive."""
    with patch.dict(
        os.environ, {"nps_api_key": "lowercase_key", "log_level": "warning"}
    ):
        settings = Settings()

        assert settings.nps_api_key == "lowercase_key"
        assert settings.log_level == "warning"


def test_settings_with_custom_values() -> None:
    """Test creating settings with custom values."""
    settings = Settings(
        nps_api_key="custom_key",
        log_level="ERROR",
        server_name="Custom Server",
        nominatim_user_agent="CustomAgent/1.0",
    )

    assert settings.nps_api_key == "custom_key"
    assert settings.log_level == "ERROR"
    assert settings.server_name == "Custom Server"
    assert settings.nominatim_user_agent == "CustomAgent/1.0"
