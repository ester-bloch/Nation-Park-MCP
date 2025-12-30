# Product Overview

## National Parks MCP Server

This is a Model Context Protocol (MCP) server that provides real-time access to U.S. National Parks data through the National Park Service (NPS) API. The server enables AI assistants like Claude to help users discover, explore, and plan visits to national parks.

## Core Functionality

The server exposes 6 main tools for park information:

- **findParks** - Search and filter parks by state, activities, or keywords
- **getParkDetails** - Get comprehensive information about specific parks
- **getAlerts** - Check current closures, hazards, and important notices
- **getVisitorCenters** - Find visitor centers and their operating hours
- **getCampgrounds** - Discover campgrounds and their amenities
- **getEvents** - Find upcoming park events and programs

## Target Use Cases

- Trip planning and park discovery
- Real-time safety and closure information
- Activity-based park recommendations
- Campground and accommodation research
- Event and program discovery

## Distribution

The server is distributed via npm and can be installed through Smithery for easy Claude Desktop integration. Users need a free NPS API key to access the service.
