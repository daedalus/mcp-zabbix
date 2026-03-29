from unittest.mock import patch

import pytest

from mcp_zabbix.client import ZabbixClient


@pytest.fixture
def mock_zabbix_api():
    with patch("mcp_zabbix.client.ZabbixAPI") as mock:
        yield mock


@pytest.fixture
def client(mock_zabbix_api):
    return ZabbixClient(
        url="http://zabbix.local/api",
        token="test_token",
    )


@pytest.fixture
def client_with_user_pass(mock_zabbix_api):
    return ZabbixClient(
        url="http://zabbix.local/api",
        user="admin",
        password="zabbix",
    )
