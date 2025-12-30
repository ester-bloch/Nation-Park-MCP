"""Main entry point for the Python MCP National Parks server."""

import sys

from src.config import settings


def main() -> None:
    """Start the server."""
    # Basic validation that API key is configured
    if not settings.nps_api_key:
        print(
            "Warning: NPS_API_KEY not configured. "
            "Some functionality may be limited.",
            file=sys.stderr,
        )

    print(f"Starting {settings.server_name} MCP Server...")
    print(f"API Base URL: {settings.nps_api_base_url}")
    print(f"Log Level: {settings.log_level}")

    # TODO: Initialize and run FastMCP server
    # This will be implemented in task 5.1
    print("Server setup complete. FastMCP server initialization pending...")


if __name__ == "__main__":
    main()
