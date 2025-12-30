# Technology Stack

## Core Technologies

- **Runtime**: Node.js with ES modules
- **Language**: TypeScript (ES2022 target, Node16 module resolution)
- **MCP Framework**: @modelcontextprotocol/sdk for server implementation
- **HTTP Client**: Axios for NPS API integration
- **Validation**: Zod for schema validation and type safety
- **Environment**: dotenv for configuration management

## Key Dependencies

### Production
- `@modelcontextprotocol/sdk` - MCP server framework
- `axios` - HTTP client for external API calls
- `zod` - Runtime type validation and schema generation
- `dotenv` - Environment variable management

### Development
- `typescript` - TypeScript compiler
- `@types/node` - Node.js type definitions
- `ts-node` - TypeScript execution for development

## Build System

### Commands
- `npm run build` - Compile TypeScript to JavaScript and set executable permissions
- `npm test` - Currently not implemented (placeholder)

### Build Configuration
- **Input**: `src/` directory
- **Output**: `build/` directory
- **Entry Point**: `build/index.js` (executable)
- **Module System**: ES modules with `.js` extensions in imports

## External API Integration

### National Park Service API
- **Base URL**: https://developer.nps.gov/api/v1
- **Authentication**: API key via `X-Api-Key` header
- **Rate Limiting**: Handled with axios interceptors
- **Environment Variable**: `NPS_API_KEY` required

## Distribution

- **Package Manager**: npm
- **Registry**: Published to npm registry
- **Installation**: Available via Smithery (`npx -y @smithery/cli install`)
- **Execution**: Runs as CLI tool via `npx mcp-server-nationalparks`
