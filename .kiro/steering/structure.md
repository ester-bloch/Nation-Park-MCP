# Project Structure

## Directory Layout

```
src/
├── main.py              # Entry point with CLI argument parsing
├── server.py            # FastMCP server setup and tool registration
├── config.py            # Pydantic settings with environment variable support
├── constants.py         # Application constants
├── api/                 # NPS API client layer
│   ├── client.py        # HTTPX client implementation
│   ├── rate_limit.py    # Rate limiting logic
│   └── retry.py         # Retry logic for API calls
├── handlers/            # Tool implementation functions
│   ├── find_parks.py
│   ├── get_park_details.py
│   ├── get_alerts.py
│   ├── get_visitor_centers.py
│   ├── get_campgrounds.py
│   └── get_events.py
├── models/              # Pydantic data models
│   ├── requests.py      # Tool input validation models
│   ├── responses.py     # API response models
│   └── errors.py        # Error models
└── utils/               # Utility functions
    ├── logging.py       # Structured logging setup
    ├── formatters.py    # Data formatting utilities
    └── error_handler.py # Error handling utilities

tests/
├── conftest.py          # Pytest fixtures and configuration
├── unit/                # Unit tests for individual components
├── integration/         # Integration tests with API
└── property/            # Property-based tests using Hypothesis
```

## Architecture Patterns

### Layered Architecture

1. **Entry Layer** (`main.py`) - CLI parsing, logging setup, server initialization
2. **Server Layer** (`server.py`) - FastMCP tool registration and request routing
3. **Handler Layer** (`handlers/`) - Business logic for each tool
4. **API Layer** (`api/`) - External API communication
5. **Model Layer** (`models/`) - Data validation and type definitions

### Key Conventions

- **Tool Registration**: Tools are registered as decorated functions in `server.py` using `@self.mcp.tool()`
- **Naming**: Tool functions use camelCase (e.g., `findParks`) to match MCP conventions, while Python code uses snake_case internally
- **Request Models**: Each tool has a corresponding Pydantic request model in `models/requests.py`
- **Error Handling**: Three-tier error handling (validation, API errors, generic errors) with structured responses
- **Logging**: Structured logging with `structlog` - use `log_request()` and `log_response()` helpers

### Code Style

- **Type Hints**: Full type annotations required (enforced by mypy strict mode)
- **Docstrings**: Google-style docstrings for all public functions
- **Line Length**: 88 characters (Black default)
- **Imports**: Sorted with isort (black-compatible profile)
- **Return Types**: Use `Dict[str, Any]` for tool return values, `NoReturn` for main functions

### Configuration

- **Settings**: Centralized in `config.py` using `pydantic-settings`
- **Environment Variables**: Loaded from `.env` file (case-insensitive)
- **Global Instance**: Settings accessed via `settings` singleton

### Testing Structure

- **Unit Tests**: Mock external dependencies, test individual functions
- **Integration Tests**: Test with real API (requires API key)
- **Property Tests**: Use Hypothesis for property-based testing
- **Fixtures**: Shared fixtures in `conftest.py`
