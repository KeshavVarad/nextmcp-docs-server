"""
NextMCP Documentation Server - Help coding assistants understand NextMCP.

This MCP server provides comprehensive access to NextMCP documentation,
examples, and best practices to help AI assistants build MCP servers correctly.

Features:
- Tools: Search docs, get examples, check API reference
- Prompts: Templates for building MCP servers
- Resources: Access to documentation files and code samples
"""

from nextmcp import NextMCP, argument

# Initialize the server
app = NextMCP(
    "nextmcp-docs",
    description="NextMCP documentation and examples server for AI coding assistants"
)

# NextMCP documentation knowledge base
DOCS = {
    "getting-started": {
        "title": "Getting Started with NextMCP",
        "content": """NextMCP is a production-grade Python SDK for building MCP (Model Context Protocol) servers with minimal boilerplate.

Key Features:
- Decorator-based API for tools, prompts, and resources
- Built-in health checks and metrics
- Automatic MCP protocol handling
- Production-ready with logging and error handling
- Easy deployment

Quick Start:
1. Install: pip install nextmcp
2. Create app.py with @app.tool(), @app.prompt(), @app.resource()
3. Run: python app.py
""",
        "category": "guide",
        "tags": ["getting-started", "quickstart", "basics"],
    },
    "tools": {
        "title": "NextMCP Tools",
        "content": """Tools are model-driven actions - callable functions exposed to AI models.

Decorator: @app.tool()

Example:
```python
@app.tool()
def search_docs(query: str) -> dict:
    '''Search documentation for the given query.'''
    results = search(query)
    return {"results": results}
```

Best Practices:
- Use clear function names and docstrings
- Return JSON-serializable data
- Handle errors gracefully
- Provide type hints
""",
        "category": "primitives",
        "tags": ["tools", "primitives", "api"],
    },
    "prompts": {
        "title": "NextMCP Prompts",
        "content": """Prompts are user-driven workflow templates that guide AI assistants.

Decorator: @app.prompt()

Example:
```python
@app.prompt(description="Research a topic")
@argument("topic", description="Topic to research")
@argument("depth", suggestions=["basic", "detailed"])
def research(topic: str, depth: str = "basic") -> str:
    return f"Research {topic} at {depth} level..."
```

Features:
- Arguments with suggestions
- Completion functions
- Tags for organization
- Dynamic content generation
""",
        "category": "primitives",
        "tags": ["prompts", "primitives", "workflows"],
    },
    "resources": {
        "title": "NextMCP Resources",
        "content": """Resources are application-driven context providers - data exposed to models.

Decorator: @app.resource()

Static Resource:
```python
@app.resource("config://app", description="App config")
def app_config() -> dict:
    return {"version": "1.0.0"}
```

Dynamic Resource Template:
```python
@app.resource_template("docs://{doc_id}")
async def get_doc(doc_id: str) -> dict:
    return load_document(doc_id)
```

Features:
- Static and dynamic resources
- Subscribable resources (real-time updates)
- Template parameters with completion
- Custom URI schemes
""",
        "category": "primitives",
        "tags": ["resources", "primitives", "context"],
    },
    "deployment": {
        "title": "Deploying NextMCP Servers",
        "content": """NextMCP servers can be deployed in multiple ways:

1. Direct Python:
   python app.py

2. Docker:
   - Create Dockerfile with Python base image
   - Install nextmcp and dependencies
   - CMD ["python", "app.py"]

3. Cloud Platforms:
   - Render, Railway, Fly.io
   - K8s with health checks
   - Serverless (with adaptations)

Health Checks:
NextMCP includes built-in /health endpoint that returns:
{"status": "healthy", "service": "your-server-name"}

Environment Variables:
- PORT: Server port (default: 8000)
- HOST: Server host (default: 0.0.0.0)
- LOG_LEVEL: Logging level (default: INFO)
""",
        "category": "deployment",
        "tags": ["deployment", "docker", "cloud", "production"],
    },
    "examples": {
        "title": "NextMCP Examples",
        "content": """NextMCP includes many example servers:

1. knowledge_base: All 3 primitives (tools, prompts, resources)
2. weather_bot: Simple tool-based server
3. blog_server: Resource templates and content management
4. auth_api_key: API key authentication
5. auth_jwt: JWT token authentication
6. auth_rbac: Role-based access control
7. metrics_example: Prometheus metrics integration
8. plugin_example: Plugin system
9. websocket_chat: WebSocket transport

Each example demonstrates specific NextMCP features and patterns.
See: https://github.com/KeshavVarad/NextMCP/tree/main/examples
""",
        "category": "examples",
        "tags": ["examples", "samples", "templates"],
    },
    "authentication": {
        "title": "NextMCP Authentication",
        "content": """NextMCP supports multiple authentication methods:

1. API Keys:
```python
from nextmcp.auth import APIKeyAuth

auth = APIKeyAuth()
auth.add_key("key-123", "user1")
app.add_middleware(auth)
```

2. JWT Tokens:
```python
from nextmcp.auth import JWTAuth

auth = JWTAuth(secret="your-secret")
app.add_middleware(auth)
```

3. RBAC (Role-Based Access Control):
```python
from nextmcp.auth import RBACAuth

auth = RBACAuth()
auth.add_role("admin", ["read", "write", "delete"])
app.add_middleware(auth)
```

Best Practices:
- Store secrets in environment variables
- Use HTTPS in production
- Implement proper token expiration
- Log auth failures for monitoring
""",
        "category": "security",
        "tags": ["auth", "security", "middleware"],
    },
    "middleware": {
        "title": "NextMCP Middleware",
        "content": """Middleware intercepts requests and responses for cross-cutting concerns.

Built-in Middleware:
- Authentication (API Key, JWT, RBAC)
- Rate Limiting
- CORS
- Request Logging
- Error Handling

Custom Middleware:
```python
from nextmcp.middleware import Middleware

class CustomMiddleware(Middleware):
    async def before_request(self, request):
        # Process request
        pass

    async def after_response(self, response):
        # Process response
        return response

app.add_middleware(CustomMiddleware())
```

Order matters - middleware is executed in the order added.
""",
        "category": "middleware",
        "tags": ["middleware", "interceptors", "cross-cutting"],
    },
}

STATS = {
    "total_searches": 0,
    "total_docs": len(DOCS),
}


# ============================================================================
# TOOLS - Search and access documentation
# ============================================================================

@app.tool()
def search_documentation(query: str) -> dict:
    """
    Search NextMCP documentation for relevant articles.

    Args:
        query: Search query (e.g., "tools", "authentication", "deployment")

    Returns:
        Search results with matching documentation
    """
    STATS["total_searches"] += 1
    results = []

    query_lower = query.lower()
    for key, doc in DOCS.items():
        if (
            query_lower in doc["title"].lower()
            or query_lower in doc["content"].lower()
            or any(query_lower in tag for tag in doc["tags"])
        ):
            results.append({
                "id": key,
                "title": doc["title"],
                "category": doc["category"],
                "tags": doc["tags"],
                "preview": doc["content"][:200] + "...",
            })

    return {
        "query": query,
        "count": len(results),
        "results": results,
    }


@app.tool()
def get_full_doc(doc_id: str) -> dict:
    """
    Get the complete documentation for a specific topic.

    Args:
        doc_id: Document ID (e.g., "tools", "deployment", "examples")

    Returns:
        Full documentation content
    """
    if doc_id not in DOCS:
        return {"error": f"Documentation '{doc_id}' not found"}

    return {"id": doc_id, **DOCS[doc_id]}


@app.tool()
def list_categories() -> list[str]:
    """
    List all documentation categories.

    Returns:
        List of available categories (primitives, deployment, security, etc.)
    """
    categories = sorted({doc["category"] for doc in DOCS.values()})
    return categories


@app.tool()
def get_example_code(example_name: str) -> dict:
    """
    Get example code for common NextMCP patterns.

    Args:
        example_name: Example to retrieve (e.g., "simple-tool", "auth-setup", "resource-template")

    Returns:
        Example code with explanation
    """
    examples = {
        "simple-tool": {
            "description": "Basic tool implementation",
            "code": '''from nextmcp import NextMCP

app = NextMCP("my-server")

@app.tool()
def calculate(x: float, y: float, operation: str) -> float:
    """Perform basic arithmetic operations."""
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation == "multiply":
        return x * y
    elif operation == "divide":
        return x / y if y != 0 else float('inf')

if __name__ == "__main__":
    app.run()
''',
        },
        "auth-setup": {
            "description": "API key authentication setup",
            "code": '''from nextmcp import NextMCP
from nextmcp.auth import APIKeyAuth

app = NextMCP("secure-server")
auth = APIKeyAuth()
auth.add_key("secret-key-123", "user1", roles=["read", "write"])
app.add_middleware(auth)

@app.tool()
def protected_action(data: str) -> dict:
    """This tool requires authentication."""
    return {"success": True, "data": data}

if __name__ == "__main__":
    app.run()
''',
        },
        "resource-template": {
            "description": "Dynamic resource with templates",
            "code": '''from nextmcp import NextMCP

app = NextMCP("docs-server")

# Static resource
@app.resource("config://app", description="App configuration")
def get_config() -> dict:
    return {"version": "1.0.0", "name": "My Server"}

# Dynamic resource template
@app.resource_template("docs://{doc_id}", description="Get document by ID")
async def get_document(doc_id: str) -> dict:
    docs = {"readme": "# README\\nWelcome!", "api": "# API\\nEndpoints..."}
    return {"id": doc_id, "content": docs.get(doc_id, "Not found")}

# Template completion
@app.template_completion("get_document", "doc_id")
def complete_doc_ids(partial: str) -> list[str]:
    all_ids = ["readme", "api", "changelog"]
    return [id for id in all_ids if partial in id]

if __name__ == "__main__":
    app.run()
''',
        },
    }

    if example_name not in examples:
        available = list(examples.keys())
        return {
            "error": f"Example '{example_name}' not found",
            "available": available,
        }

    return examples[example_name]


# ============================================================================
# PROMPTS - Workflow templates for building MCP servers
# ============================================================================

@app.prompt(description="Build a new MCP server", tags=["development", "quickstart"])
@argument("server_type", description="Type of server to build",
          suggestions=["tool-based", "documentation", "api-wrapper", "data-provider"])
@argument("features", description="Features to include",
          suggestions=["auth", "rate-limiting", "metrics", "websockets"])
def build_server_prompt(server_type: str, features: str = "none") -> str:
    """Generate a prompt for building a new NextMCP server."""

    feature_list = features.split(",") if features != "none" else []

    prompt = f"""Build a NextMCP server of type: {server_type}

Step 1: Setup
- Create app.py
- Import: from nextmcp import NextMCP
- Initialize: app = NextMCP("your-server-name", description="...")

Step 2: Implement primitives based on server type:
"""

    if server_type == "tool-based":
        prompt += """
- Add tools with @app.tool() decorator
- Each tool should have clear docstrings
- Return JSON-serializable data
- Handle errors gracefully
"""
    elif server_type == "documentation":
        prompt += """
- Add search tool with @app.tool()
- Add resource templates with @app.resource_template()
- Add prompts for common workflows with @app.prompt()
- Include statistics resource
"""
    elif server_type == "api-wrapper":
        prompt += """
- Create tools for each API endpoint
- Add authentication if API requires it
- Implement rate limiting
- Cache responses where appropriate
"""

    if "auth" in feature_list:
        prompt += """
Step 3: Add Authentication
- Choose: APIKeyAuth, JWTAuth, or RBACAuth
- Add keys/tokens for test users
- Apply middleware: app.add_middleware(auth)
"""

    if "metrics" in feature_list:
        prompt += """
Step 4: Add Metrics
- Import: from nextmcp.metrics import PrometheusMetrics
- Initialize: metrics = PrometheusMetrics()
- Add middleware: app.add_middleware(metrics)
"""

    prompt += """
Final Step: Run server
- Add: if __name__ == "__main__": app.run()
- Test locally: python app.py
- Access: http://localhost:8000

Use search_documentation() and get_example_code() tools for reference.
"""

    return prompt


@app.prompt(description="Debug a NextMCP server issue", tags=["debugging", "troubleshooting"])
@argument("issue_type", description="Type of issue",
          suggestions=["server-not-starting", "tool-not-working", "auth-failing", "deployment-error"])
def debug_prompt(issue_type: str) -> str:
    """Generate debugging steps for common NextMCP issues."""

    debug_steps = {
        "server-not-starting": """Debugging server startup issues:

1. Check Python version: python --version (requires 3.10+)
2. Verify NextMCP installation: pip show nextmcp
3. Check for import errors: python -c "import nextmcp; print(nextmcp.__version__)"
4. Review error logs for stack traces
5. Ensure port 8000 is available: lsof -i :8000

Common causes:
- Missing dependencies
- Port already in use
- Python version incompatibility
- Syntax errors in app.py
""",
        "tool-not-working": """Debugging tool execution:

1. Verify decorator is correct: @app.tool()
2. Check function signature has type hints
3. Ensure return type is JSON-serializable
4. Test function independently: python -c "from app import my_tool; print(my_tool('test'))"
5. Review server logs for exceptions

Common causes:
- Missing type hints
- Returning non-JSON types (objects, datetime, etc.)
- Uncaught exceptions in tool code
- Incorrect argument names
""",
        "auth-failing": """Debugging authentication:

1. Verify middleware is added: app.add_middleware(auth)
2. Check API key/token format
3. Review auth logs for rejection reasons
4. Test with curl: curl -H "Authorization: Bearer TOKEN" http://localhost:8000/health
5. Ensure auth middleware is before other middleware

Common causes:
- Wrong token format
- Expired JWT tokens
- Middleware order incorrect
- Missing auth header in request
""",
        "deployment-error": """Debugging deployment issues:

1. Check health endpoint: curl http://your-app.com/health
2. Review deployment logs
3. Verify environment variables are set
4. Ensure correct Python version in runtime
5. Check Dockerfile if using containers

Common causes:
- Missing environment variables
- Incorrect PORT binding
- Health check timeout
- Dependencies not installed
- File paths incorrect in production

Use get_full_doc("deployment") for detailed deployment guide.
""",
    }

    return debug_steps.get(issue_type, f"Debug steps for '{issue_type}' not available. Search documentation for help.")


@app.prompt(description="Learn about NextMCP features", tags=["learning", "documentation"])
@argument("topic", description="Topic to learn",
          suggestions=["tools", "prompts", "resources", "authentication", "deployment", "middleware"])
@argument("learn_style", description="Learning style",
          suggestions=["overview", "hands-on", "deep-dive"])
def learn_prompt(topic: str, learn_style: str = "overview") -> str:
    """Generate a learning path for NextMCP topics."""

    return f"""Learning path for: {topic} ({learn_style} style)

Step 1: Get documentation
Use: get_full_doc("{topic}")

Step 2: Understand the concept
- Read the full documentation
- Review code examples
- Understand the use cases

Step 3: Hands-on practice
Use: get_example_code("simple-tool") or similar examples
- Copy the example code
- Modify it for your use case
- Run and test locally

Step 4: Build something
- Combine what you learned with other features
- Refer to documentation as needed
- Use search_documentation() to find related topics

Step 5: Deploy and iterate
- Use get_full_doc("deployment") for deployment guide
- Test in production environment
- Monitor and improve

Recommended next topics after {topic}:
{", ".join([t for t in ["tools", "prompts", "resources", "deployment"] if t != topic])}
"""


# ============================================================================
# RESOURCES - Documentation access and stats
# ============================================================================

@app.resource("docs://stats", description="Documentation server statistics")
def docs_stats() -> dict:
    """Get current documentation statistics."""
    return {
        "total_docs": STATS["total_docs"],
        "total_searches": STATS["total_searches"],
        "categories": list_categories(),
        "available_examples": ["simple-tool", "auth-setup", "resource-template"],
    }


@app.resource_template("docs://{doc_id}", description="Get specific documentation by ID")
async def get_doc_resource(doc_id: str) -> dict:
    """Access documentation as a resource."""
    if doc_id not in DOCS:
        return {"error": f"Documentation '{doc_id}' not found"}

    return {"id": doc_id, **DOCS[doc_id]}


@app.resource_template("examples://{example_name}", description="Get example code")
def get_example_resource(example_name: str) -> dict:
    """Access example code as a resource."""
    return get_example_code(example_name)


# Template completions
@app.template_completion("get_doc_resource", "doc_id")
def complete_doc_ids(partial: str) -> list[str]:
    """Suggest documentation IDs."""
    return [doc_id for doc_id in DOCS.keys() if partial in doc_id]


@app.template_completion("get_example_resource", "example_name")
def complete_example_names(partial: str) -> list[str]:
    """Suggest example names."""
    examples = ["simple-tool", "auth-setup", "resource-template"]
    return [ex for ex in examples if partial in ex]


# ============================================================================
# Main entry point
# ============================================================================

if __name__ == "__main__":
    print("🚀 Starting NextMCP Documentation Server...")
    print(f"📚 Documentation articles: {len(DOCS)}")
    print(f"🏷️  Categories: {len(list_categories())}")
    print("\nServer capabilities:")
    print("  • 5 Tools (search, get doc, list categories, get example, etc.)")
    print("  • 3 Prompts (build server, debug, learn)")
    print("  • 3 Resources (stats, docs/{id}, examples/{name})")
    print("\n⚡ Server ready to help build MCP servers!\n")

    app.run()
