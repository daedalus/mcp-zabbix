# mcp-zabbix

> MCP server for Zabbix API - exposes all Zabbix API functionality via MCP

[![PyPI](https://img.shields.io/pypi/v/mcp-zabbix.svg)](https://pypi.org/project/mcp-zabbix/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-zabbix.svg)](https://pypi.org/project/mcp-zabbix/)

mcp-name: io.github.daedalus/mcp-zabbix

## Install

```bash
pip install mcp-zabbix
```

## Configuration

Set the following environment variables:

- `ZABBIX_URL` - Zabbix API URL (required)
- `ZABBIX_TOKEN` - API token (required, or use user/password)
- `ZABBIX_USER` - Zabbix username (optional)
- `ZABBIX_PASSWORD` - Zabbix password (optional)

## Usage

```python
from mcp_zabbix import mcp

mcp.run()
```

Or via CLI:

```bash
mcp-zabbix
```

## API

The MCP server exposes all Zabbix API methods as tools. Tools follow the pattern:
- `zabbix_<namespace>_<method>` (e.g., `zabbix_host_get`, `zabbix_host_create`)

## Development

```bash
git clone https://github.com/daedalus/mcp-zabbix.git
cd mcp-zabbix
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypy src/
```
