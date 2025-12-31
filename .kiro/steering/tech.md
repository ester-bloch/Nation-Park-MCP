# Technology Stack

## Build System

- **Package Manager**: Poetry (primary) or pip
- **Python Version**: 3.9+
- **Build Backend**: poetry-core

## Core Dependencies

- **fastmcp** (^0.1.0) - FastMCP SDK for MCP server implementation
- **httpx** (^0.27.0) - Modern async HTTP client for API requests
- **pydantic** (^2.0.0) - Data validation and settings management
- **pydantic-settings** (^2.0.0) - Environment-based configuration
- **python-dotenv** (^1.0.0) - Environment variable loading
- **structlog** (^23.0.0) - Structured logging

## Development Tools

- **pytest** - Testing framework with coverage, mocking, and property-based testing (hypothesis)
- **black** - Code formatter (line length: 88)
- **isort** - Import sorting (black-compatible profile)
- **flake8** - Linting (extends ignore: E203, W503, E501)
- **mypy** - Static type checking (strict mode enabled)
- **pre-commit** - Git hooks for code quality

## Common Commands

### Setup
```bash
# Install dependencies
poetry install

# Install with dev dependencies
poetry install --with dev

# Install pre-commit hooks
pre-commit install
```

### Running
```bash
# Start the server
poetry run python-mcp-nationalparks

# Or with Python directly
python -m src.main
```

### Testing
```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=src --cov-report=html

# Run specific test types
poetry run pytest tests/unit/
poetry run pytest tests/integration/
poetry run pytest tests/property/
```

### Code Quality
```bash
# Format code
poetry run black src tests

# Sort imports
poetry run isort src tests

# Lint
poetry run flake8 src tests

# Type check
poetry run mypy src

# Run all pre-commit hooks
pre-commit run --all-files
```

## Configuration Files

- `pyproject.toml` - Poetry dependencies, tool configurations (black, isort, mypy, pytest, coverage)
- `.flake8` - Flake8 linting rules
- `.pre-commit-config.yaml` - Pre-commit hook definitions
- `.env` - Environment variables (not in git, use `.env.example` as template)
