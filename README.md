# NextMCP Documentation Server

> An MCP server that helps coding assistants understand and build with NextMCP

[![MCP](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)
[![NextMCP](https://img.shields.io/badge/Built%20with-NextMCP-green)](https://github.com/KeshavVarad/NextMCP)

## Overview

This MCP server provides comprehensive documentation, examples, and guidance for building MCP servers using NextMCP. It's designed to help AI coding assistants quickly understand NextMCP concepts and generate correct code.

## Features

### 🔧 Tools (5)
- **search_documentation**: Search NextMCP docs for relevant articles
- **get_full_doc**: Get complete documentation for specific topics
- **list_categories**: List all documentation categories
- **get_example_code**: Get code examples for common patterns

### 📝 Prompts (3)
- **build_server_prompt**: Generate workflow for building new MCP servers
- **debug_prompt**: Get debugging steps for common issues
- **learn_prompt**: Create personalized learning path for NextMCP topics

### 📚 Resources (3)
- **docs://stats**: Server statistics and available docs
- **docs://{doc_id}**: Access specific documentation by ID
- **examples://{example_name}**: Access code examples as resources

## Documentation Coverage

- **Getting Started**: Installation, quickstart, basics
- **Core Primitives**: Tools, Prompts, Resources
- **Authentication**: API Keys, JWT, RBAC
- **Middleware**: Request/response interceptors
- **Deployment**: Docker, cloud platforms, production setup
- **Examples**: Code samples for common patterns

## Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/nextmcp-docs-server.git
cd nextmcp-docs-server

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Server will start on `http://localhost:8000`

### Docker

```bash
# Build image
docker build -t nextmcp-docs-server .

# Run container
docker run -p 8000:8000 nextmcp-docs-server
```

### Deploy to Conduit

```bash
# Prerequisites: Conduit account and project

# Create project in Conduit dashboard
# - Name: NextMCP Docs Server
# - Git URL: https://github.com/YOUR_USERNAME/nextmcp-docs-server
# - Branch: main

# Deploy via dashboard or CLI
conduit deploy
```

## Usage Examples

### Search Documentation

```python
# Tool call
search_documentation(query="authentication")

# Returns articles about API keys, JWT, RBAC, etc.
```

### Get Example Code

```python
# Tool call
get_example_code(example_name="simple-tool")

# Returns complete code example with explanation
```

### Build Server Workflow

```python
# Prompt call
build_server_prompt(
    server_type="tool-based",
    features="auth,metrics"
)

# Returns step-by-step guide for building the server
```

### Access Documentation Resource

```
# Resource URI
docs://deployment

# Returns full deployment documentation
```

## API Endpoints

- `GET /health` - Health check (returns `{"status": "healthy"}`)
- `POST /mcp` - MCP protocol endpoint (JSON-RPC 2.0)

## Environment Variables

- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)
- `LOG_LEVEL` - Logging level (default: INFO)

## Development

### Project Structure

```
nextmcp-docs-server/
├── app.py              # Main server code
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container image definition
└── README.md          # This file
```

### Adding Documentation

To add new documentation articles, edit the `DOCS` dictionary in `app.py`:

```python
DOCS["new-topic"] = {
    "title": "New Topic Title",
    "content": "Documentation content...",
    "category": "guide",
    "tags": ["tag1", "tag2"],
}
```

### Testing

```bash
# Test locally
python app.py

# In another terminal, test with curl
curl http://localhost:8000/health

# Test MCP protocol
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 1
  }'
```

## Use Cases

### For AI Coding Assistants

This server helps AI assistants:
- Understand NextMCP architecture and patterns
- Generate correct MCP server code
- Provide debugging guidance
- Access up-to-date documentation
- Learn best practices

### For Developers

- Quick reference for NextMCP APIs
- Example code for common patterns
- Deployment guidance
- Troubleshooting help

## Contributing

Contributions welcome! To add documentation:

1. Fork the repository
2. Add documentation to `DOCS` dictionary
3. Test locally
4. Submit pull request

## License

MIT License - see LICENSE file for details

## Links

- [NextMCP Framework](https://github.com/KeshavVarad/NextMCP)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Specification](https://spec.modelcontextprotocol.io)

## Support

For issues or questions:
- GitHub Issues: https://github.com/YOUR_USERNAME/nextmcp-docs-server/issues
- NextMCP Discussions: https://github.com/KeshavVarad/NextMCP/discussions
