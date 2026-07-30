"""
Minimal MCP server using FastMCP.
---------------------------------
Run as a standalone process. The client launches it via stdio and auto-
discovers every @mcp.tool() function as a callable tool.
"""

from fastmcp import FastMCP

mcp = FastMCP("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


if __name__ == "__main__":
    mcp.run(transport="stdio")   # stdio = simplest local transport.