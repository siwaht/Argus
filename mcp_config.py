# File name mcp_config.py

"""
Central registry of MCP servers.

Add every MCP server you want your agents to use here, once. Any script
can then call `get_mcp_client()` to get a `MultiServerMCPClient` wired up
with all of them, instead of redefining the server config inline.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

BASE_DIR = Path(__file__).parent

MCP_SERVERS = {
    "firecrawl-mcp": {
        "command": "npx",
        "args": ["-y", "firecrawl-mcp"],
        "transport": "stdio",
        "env": {"FIRECRAWL_API_KEY": os.environ["FIRECRAWL_API_KEY"]},
    },
    "math": {
        "transport": "stdio",  # Local subprocess communication
        "command": "python",
        "args": [str(BASE_DIR / "math_server.py")],
    },
    # Add new MCP servers below, following the same pattern:
    # "your-server-name": {
    #     "command": "...",
    #     "args": [...],
    #     "transport": "stdio",
    #     "env": {...},  # optional
    # },
    
}


def get_mcp_client() -> MultiServerMCPClient:
    """Return a MultiServerMCPClient configured with every registered MCP server."""
    return MultiServerMCPClient(MCP_SERVERS)
