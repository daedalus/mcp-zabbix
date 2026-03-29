from unittest.mock import MagicMock, patch

from mcp_zabbix import tools


class TestTools:
    def test_tools_generated(self):
        assert len(tools.TOOLS) > 0

    def test_host_tools_exist(self):
        assert "zabbix_host_get" in tools.TOOLS
        assert "zabbix_host_create" in tools.TOOLS
        assert "zabbix_host_update" in tools.TOOLS
        assert "zabbix_host_delete" in tools.TOOLS

    def test_action_tools_exist(self):
        assert "zabbix_action_get" in tools.TOOLS
        assert "zabbix_action_create" in tools.TOOLS
        assert "zabbix_action_update" in tools.TOOLS
        assert "zabbix_action_delete" in tools.TOOLS

    def test_item_tools_exist(self):
        assert "zabbix_item_get" in tools.TOOLS
        assert "zabbix_item_create" in tools.TOOLS
        assert "zabbix_item_update" in tools.TOOLS
        assert "zabbix_item_delete" in tools.TOOLS

    def test_trigger_tools_exist(self):
        assert "zabbix_trigger_get" in tools.TOOLS
        assert "zabbix_trigger_create" in tools.TOOLS
        assert "zabbix_trigger_update" in tools.TOOLS
        assert "zabbix_trigger_delete" in tools.TOOLS

    def test_template_tools_exist(self):
        assert "zabbix_template_get" in tools.TOOLS
        assert "zabbix_template_create" in tools.TOOLS
        assert "zabbix_template_update" in tools.TOOLS
        assert "zabbix_template_delete" in tools.TOOLS

    def test_get_all_tools(self):
        all_tools = tools.get_all_tools()
        assert isinstance(all_tools, dict)
        assert len(all_tools) > 0


class TestToolExecution:
    def test_tool_calls_api(self, mock_zabbix_api):
        mock_api = MagicMock()
        mock_api.call.return_value = {"result": [{"hostid": "1"}]}

        with patch("mcp_zabbix.tools.client") as mock_client:
            mock_client.return_value.call_method.return_value = [{"hostid": "1"}]
            tool = tools.TOOLS["zabbix_host_get"]
            tool({"output": "extend"})

            mock_client.return_value.call_method.assert_called_once()

    def test_tool_with_none_params(self, mock_zabbix_api):
        with patch("mcp_zabbix.tools.client") as mock_client:
            mock_client.return_value.call_method.return_value = []
            tool = tools.TOOLS["zabbix_host_get"]
            tool(None)
            mock_client.return_value.call_method.assert_called_once()
