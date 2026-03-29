from unittest.mock import MagicMock

import pytest

from mcp_zabbix.client import ZabbixClient, client, get_client


class TestZabbixClient:
    def test_client_requires_url(self):
        with pytest.raises(ValueError, match="ZABBIX_URL is required"):
            ZabbixClient()

    def test_client_requires_auth(self):
        with pytest.raises(ValueError, match="Either ZABBIX_TOKEN or ZABBIX_USER"):
            ZabbixClient(url="http://zabbix.local/api")

    def test_client_with_token(self, mock_zabbix_api):
        c = ZabbixClient(url="http://zabbix.local/api", token="test_token")
        assert c.url == "http://zabbix.local/api"
        assert c.token == "test_token"

    def test_client_with_user_password(self, mock_zabbix_api):
        c = ZabbixClient(
            url="http://zabbix.local/api",
            user="admin",
            password="zabbix",
        )
        assert c.url == "http://zabbix.local/api"
        assert c.user == "admin"
        assert c.password == "zabbix"

    def test_client_from_env(self, mock_zabbix_api, monkeypatch):
        monkeypatch.setenv("ZABBIX_URL", "http://zabbix.local/api")
        monkeypatch.setenv("ZABBIX_TOKEN", "env_token")
        c = ZabbixClient()
        assert c.url == "http://zabbix.local/api"
        assert c.token == "env_token"

    def test_api_property(self, client, mock_zabbix_api):
        api = client.api
        assert api is not None

    def test_call_method(self, client, mock_zabbix_api):
        mock_api = MagicMock()
        mock_api.call.return_value = {"result": []}
        client._api = mock_api
        result = client.call_method("host.get", {"output": "extend"})
        assert result == {"result": []}
        mock_api.call.assert_called_once_with("host.get", {"output": "extend"})


class TestGetClient:
    def test_get_client_sets_global(self, mock_zabbix_api):
        c = get_client(url="http://zabbix.local/api", token="test_token")
        assert client() is c

    def test_client_function_returns_global(self, mock_zabbix_api):
        get_client(url="http://zabbix.local/api", token="test_token")
        c = client()
        assert c is not None
        assert c.url == "http://zabbix.local/api"
