from unittest.mock import MagicMock, patch

from mcp_zabbix import mcp


class TestMCP:
    def test_mcp_server_exists(self):
        assert mcp is not None

    def test_mcp_server_name(self):
        from mcp_zabbix.mcp import mcp as mcp_server

        assert "mcp-zabbix" in str(mcp_server)

    def test_connection_resource(self):
        with patch("mcp_zabbix.mcp.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.url = "http://zabbix.local/api"
            mock_get_client.return_value = mock_client

            from mcp_zabbix.mcp import connection_info

            result = connection_info()

            assert "url" in result
            assert "authenticated" in result
