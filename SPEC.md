# SPEC.md — mcp-zabbix

## Purpose

An MCP (Model Context Protocol) server that exposes all Zabbix API functionality, allowing AI assistants and other tools to interact with Zabbix monitoring systems through a standardized MCP interface.

## Scope

**In scope:**
- All Zabbix API methods (create, get, update, delete operations)
- Authentication (API token and user/password)
- Connection management (single Zabbix instance)
- All API namespaces: action, alert, auditlog, authentication, autoregistration, configuration, connector, correlation, dashboard, dcheck, dhost, dservice, drule, event, graph, graphitem, graphprototype, hanode, host, hostgroup, hostprototype, httptest, iconmap, image, item, itemprototype, maintenance, map, mediatype, module, notify, problem, proxy, proxygroup, regex, role, script, service, sla, template, templategroup, trend, trigger, triggerprototype, user, usergroup, valuemap, widget, wizard

**Not in scope:**
- Multiple simultaneous Zabbix instances (connection pooling)
- Webhooks for real-time data
- Zabbix sender protocol
- Zabbix get protocol

## Public API / Interface

### MCP Tools

The server exposes all Zabbix API methods as MCP tools following the pattern:
- `zabbix_<namespace>_<method>` (e.g., `zabbix_host_get`, `zabbix_host_create`)

Each tool accepts parameters matching the Zabbix API method's input parameters and returns the API response.

### MCP Resources

- `zabbix://connection` - Connection configuration resource

### Configuration

Connection is configured via environment variables:
- `ZABBIX_URL` - Zabbix API URL (required)
- `ZABBIX_TOKEN` - API token (required, or use user/password)
- `ZABBIX_USER` - Zabbix username (optional)
- `ZABBIX_PASSWORD` - Zabbix password (optional)

## Data Formats

All API calls use JSON-RPC 2.0 format over HTTP. The MCP server handles serialization/deserialization automatically.

## Edge Cases

1. Invalid Zabbix URL - raise ConfigurationError
2. Authentication failure - raise AuthenticationError with descriptive message
3. Network timeout - raise ConnectionError with timeout details
4. Invalid API parameters - raise ValidationError with parameter details
5. Zabbix API error responses - propagate as ZabbixAPIError with error code and message
6. Empty API responses - return empty list/dict appropriately
7. Large result sets - handle pagination (Zabbix default limit 1000)
8. Concurrent requests - thread-safe API client

## Performance & Constraints

- Default timeout: 30 seconds per request
- Default page size: 1000 results
- Maximum retry attempts: 3
- Thread-safe: Yes (using requests Session)
