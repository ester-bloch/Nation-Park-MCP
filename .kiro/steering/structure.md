# Project Structure

## Directory Organization

```
src/
├── index.ts              # Entry point and server startup
├── server.ts             # MCP server configuration and tool registration
├── schemas.ts            # Zod validation schemas for all tools
├── constants.ts          # Application constants (version, state codes)
├── formatters.ts         # Data formatting utilities
├── config.ts             # Configuration management
├── handlers/             # Tool implementation handlers
│   ├── findParks.ts
│   ├── getParkDetails.ts
│   ├── getAlerts.ts
│   ├── getVisitorCenters.ts
│   ├── getCampgrounds.ts
│   └── getEvents.ts
└── utils/
    └── npsApiClient.ts   # NPS API client and type definitions
```

## Architecture Patterns

### MCP Server Pattern
- **server.ts** - Central server configuration with tool registration
- **index.ts** - Entry point that initializes server with stdio transport
- Tool handlers are registered via `ListToolsRequestSchema` and `CallToolRequestSchema`

### Handler Pattern
- Each tool has a dedicated handler in `src/handlers/`
- Handlers follow consistent structure:
  1. Input validation using Zod schemas
  2. API client calls via `npsApiClient`
  3. Data formatting and response construction
  4. Error handling with structured JSON responses

### Schema-First Design
- All tool inputs defined as Zod schemas in `schemas.ts`
- Schemas automatically converted to JSON Schema for MCP tool definitions
- Runtime validation ensures type safety

### API Client Pattern
- Singleton `npsApiClient` instance in `utils/npsApiClient.ts`
- Comprehensive TypeScript interfaces for all API response types
- Axios interceptors for error handling and rate limiting
- Environment-based configuration

## File Naming Conventions

- **Handlers**: camelCase matching tool names (e.g., `findParks.ts`)
- **Schemas**: PascalCase with "Schema" suffix (e.g., `FindParksSchema`)
- **Types**: PascalCase with descriptive suffixes (e.g., `ParkData`, `NPSResponse`)
- **Constants**: UPPER_SNAKE_CASE for exported constants

## Import Conventions

- Use `.js` extensions in imports (required for ES modules)
- Relative imports for local modules
- Absolute imports for external dependencies
- Group imports: external dependencies first, then local modules

## Error Handling

- Zod validation errors return structured validation details
- API errors caught and returned as JSON with error type classification
- Console logging for debugging while returning user-friendly error messages
- Graceful degradation when API key is missing (warnings, not failures)
