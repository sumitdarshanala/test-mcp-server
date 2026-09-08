import os

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import PlainTextResponse

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Test MCP Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


async def health(request):
    return PlainTextResponse("MCP server is running")


app = Starlette(
    routes=[
        Route("/", endpoint=health),
        Mount("/", app=mcp.sse_app()),
    ]
)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
    )