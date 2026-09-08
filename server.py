import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Test MCP Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=port,
    )