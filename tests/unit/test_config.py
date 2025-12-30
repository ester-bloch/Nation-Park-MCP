"""Tests for configuration management."""

import os
from unittest.mock import patch

from src.config import Settings


def test_settings_default_values() -> None:
    """Test that settings have correct default values."""
    settings = Settings()

    assert settings.nps_api_base_url == "https://developer.nps.gov/api/v1"
    assert settings.log_level == "INFO"
    assert settings.server_name == "National Parks"
    assert settings.nps_api_key is None


def test_settings_from_environment() -> None:
    """Test that settings can be loaded from environment variables."""
    with patch.dict(
        os.environ,
        {
            "NPS_API_KEY": "test_key_123",
            "LOG_LEVEL": "DEBUG",
            "SERVER_NAME": "Test Server",
        },
    ):
        settings = Settings()

        assert settings.nps_api_key == "test_key_123"
        assert settings.log_level == "DEBUG"
        assert settings.server_name == "Test Server"


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
        nps_api_key="custom_key", log_level="ERROR", server_name="Custom Server"
    )

    assert settings.nps_api_key == "custom_key"
    assert settings.log_level == "ERROR"
    assert settings.server_name == "Custom Server"
