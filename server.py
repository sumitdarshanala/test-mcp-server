import os

import uvicorn
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings


mcp = FastMCP(
    "Test MCP Server",
    transport_security=TransportSecuritySettings(
        allowed_hosts=[
            "test-mcp-server-6ml5.onrender.com",
        ],
        allowed_origins=[
            "https://test-mcp-server-6ml5.onrender.com",
        ],
    ),
)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def get_weather(city: str) -> dict:
    """Get the current weather forecast for a given city.

    Args:
        city: The name of the city to get the weather for.

    Returns:
        A dictionary containing the city name, temperature in Celsius,
        weather condition, humidity percentage, and a recommendation.
    """
    return {
        "city": city,
        "temperature_celsius": 22,
        "condition": "Partly Cloudy",
        "humidity_percent": 60,
        "recommendation": f"Mild weather in {city}. A light jacket is recommended."
    }


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