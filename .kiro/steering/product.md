# Product Overview

Python MCP National Parks Server - A Model Context Protocol (MCP) server implementation that provides access to U.S. National Parks data through the National Park Service API.

## Purpose

Enables AI assistants and applications to query National Parks information including park details, alerts, visitor centers, campgrounds, and events through standardized MCP tools.

## Key Features

- Six MCP tools for accessing National Parks data
- Integration with National Park Service API
- Type-safe request/response handling with Pydantic
- Structured logging with contextual information
- Comprehensive error handling and validation

## Tools Provided

1. `findParks` - Search parks by state, activity, or keyword
2. `getParkDetails` - Get detailed information about a specific park
3. `getAlerts` - Check current park alerts and closures
4. `getVisitorCenters` - Find visitor centers and operating hours
5. `getCampgrounds` - Discover campgrounds and amenities
6. `getEvents` - Find upcoming park events and programs

## External Dependencies

- National Park Service API (requires free API key from https://www.nps.gov/subjects/developer/get-started.htm)
- API key must be set in `.env` file as `NPS_API_KEY`
