"""MCP server for Zabbix API."""

import fastmcp

from .client import get_client
from .tools import get_all_tools

mcp = fastmcp.FastMCP("mcp-zabbix")


@mcp.resource("zabbix://connection")
def connection_info() -> dict[str, str]:
    """Get Zabbix connection configuration."""
    c = get_client()
    authenticated = "yes" if c.token or (c.user and c.password) else "no"
    return {
        "url": c.url,
        "authenticated": authenticated,
    }


def register_tools() -> None:
    """Register all Zabbix API tools with the MCP server."""
    tools = get_all_tools()
    for _name, func in tools.items():
        if callable(func):
            try:
                mcp.tool()(func)
            except Exception:
                pass


register_tools()
