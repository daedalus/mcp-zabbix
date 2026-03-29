"""MCP tools for Zabbix API."""

from collections.abc import Callable
from typing import Any

from .client import client


def create_tool(
    name: str, namespace: str, method: str
) -> Callable[[dict[str, Any] | None], dict[str, Any]]:
    """Create a tool function dynamically."""

    def tool(params: dict[str, Any] | None = None) -> dict[str, Any]:
        return client().call_method(f"{namespace}.{method}", params)

    tool.__name__ = name
    tool.__doc__ = f"Zabbix API {namespace}.{method} method"
    return tool


NAMESPACES = [
    "action",
    "alert",
    "apiinfo",
    "auditlog",
    "authentication",
    "autoregistration",
    "configuration",
    "connector",
    "correlation",
    "dashboard",
    "dcheck",
    "dhost",
    "dservice",
    "drule",
    "event",
    "graph",
    "graphitem",
    "graphprototype",
    "hanode",
    "host",
    "hostgroup",
    "hostprototype",
    "httptest",
    "iconmap",
    "image",
    "item",
    "itemprototype",
    "maintenance",
    "map",
    "mediatype",
    "module",
    "notify",
    "problem",
    "proxy",
    "proxygroup",
    "regex",
    "role",
    "script",
    "service",
    "sla",
    "template",
    "templategroup",
    "trend",
    "trigger",
    "triggerprototype",
    "user",
    "usergroup",
    "valuemap",
    "widget",
    "wizard",
]

METHODS = ["create", "get", "update", "delete"]

TOOLS: dict[str, Any] = {}

for namespace in NAMESPACES:
    for method in METHODS:
        tool_name = f"zabbix_{namespace}_{method}"
        TOOLS[tool_name] = create_tool(tool_name, namespace, method)

        full_method_name = f"{namespace}.{method}"
        if namespace == "apiinfo" and method == "get":
            TOOLS[tool_name] = create_tool(tool_name, namespace, "version")

        if namespace == "apiinfo":
            continue

        if namespace in [
            "alert",
            "auditlog",
            "dhost",
            "dservice",
            "event",
            "graphitem",
            "problem",
            "trend",
        ] and method in ["create", "update", "delete"]:
            continue

        if namespace == "apiinfo" and method in ["create", "update", "delete"]:
            continue

        if namespace == "authentication":
            TOOLS[f"zabbix_{namespace}_get"] = create_tool(
                f"zabbix_{namespace}_get", namespace, "get"
            )
            TOOLS[f"zabbix_{namespace}_update"] = create_tool(
                f"zabbix_{namespace}_update", namespace, "update"
            )
            continue

        if namespace == "autoregistration":
            TOOLS[f"zabbix_{namespace}_get"] = create_tool(
                f"zabbix_{namespace}_get", namespace, "get"
            )
            TOOLS[f"zabbix_{namespace}_update"] = create_tool(
                f"zabbix_{namespace}_update", namespace, "update"
            )
            continue

    if namespace not in [
        "alert",
        "auditlog",
        "dhost",
        "dservice",
        "event",
        "graphitem",
        "problem",
        "trend",
        "apiinfo",
    ]:
        tool_name = f"zabbix_{namespace}_exists"
        TOOLS[tool_name] = create_tool(tool_name, namespace, "exists")

    if namespace == "service":
        for method in [
            "create",
            "delete",
            "get",
            "update",
            "addtimes",
            "deletetimes",
            "gettimes",
            "updatetimes",
        ]:
            tool_name = f"zabbix_service_{method}"
            TOOLS[tool_name] = create_tool(tool_name, "service", method)

    if namespace == "sla":
        for method in [
            "create",
            "delete",
            "get",
            "update",
            "get_sla",
            "create_schedule",
            "delete_schedule",
            "get_schedule",
            "update_schedule",
        ]:
            tool_name = f"zabbix_sla_{method}"
            TOOLS[tool_name] = create_tool(tool_name, "sla", method)

    if namespace == "user":
        for method in [
            "create",
            "delete",
            "get",
            "update",
            "login",
            "logout",
            "checkAuthentication",
            "updateprofile",
            "changepassword",
            "resetpassword",
        ]:
            tool_name = f"zabbix_user_{method}"
            TOOLS[tool_name] = create_tool(tool_name, "user", method)

    if namespace == "widget":
        for method in ["get", "create", "update", "delete"]:
            tool_name = f"zabbix_widget_{method}"
            TOOLS[tool_name] = create_tool(tool_name, "widget", method)

    if namespace == "wizard":
        for method in ["get", "create", "update", "delete"]:
            tool_name = f"zabbix_wizard_{method}"
            TOOLS[tool_name] = create_tool(tool_name, "wizard", method)

    if namespace == "module":
        for method in [
            "create",
            "delete",
            "get",
            "update",
            "install",
            "uninstall",
            "refresh",
        ]:
            tool_name = f"zabbix_module_{method}"
            TOOLS[tool_name] = create_tool(tool_name, "module", method)

    if namespace == "notify":
        for method in ["get", "create", "update", "delete"]:
            tool_name = f"zabbix_notify_{method}"
            TOOLS[tool_name] = create_tool(tool_name, "notify", method)

    if namespace == "configuration":
        for method in ["export", "import", "importcompare"]:
            tool_name = f"zabbix_configuration_{method}"
            TOOLS[tool_name] = create_tool(tool_name, "configuration", method)


def get_all_tools() -> dict[str, Any]:
    """Return all available tools."""
    return TOOLS
