import os

import uvicorn
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route

from mcp.server.fastmcp import FastMCP


# Create MCP server
mcp = FastMCP("Test MCP Server")


# Test tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


# Health check
async def health(request):
    return PlainTextResponse("MCP server is running")


# Create the SSE ASGI application
sse_app = mcp.sse_app()


# Mount MCP SSE server
app = Starlette(
    routes=[
        Route("/", endpoint=health),
        Mount("/", app=sse_app),
    ]
)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
    )