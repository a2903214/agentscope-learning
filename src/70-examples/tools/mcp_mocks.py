"""MCP 模拟客户端：搜索与金融快照占位实现。"""
from agentscope.tool import ToolResponse

from .common import text_response


class SearchMCPMock:
    """搜索类 MCP 模拟，提供主题搜索提示。"""
    name = "search_mcp_mock"

    async def list_tools(self):
        class Tool:
            def __init__(self, name: str) -> None:
                self.name = name

        return [Tool("mcp_search_hint")]

    async def get_callable_function(self, func_name: str, wrap_tool_result: bool = True):
        async def mcp_search_hint(topic: str = "AI算力") -> ToolResponse:
            return text_response(f"[MCP] 搜索提示已就绪，主题={topic}")

        mcp_search_hint.__name__ = func_name
        return mcp_search_hint


class FinanceMCPMock:
    """金融类 MCP 模拟，提供标的快照占位。"""
    name = "finance_mcp_mock"

    async def list_tools(self):
        class Tool:
            def __init__(self, name: str) -> None:
                self.name = name

        return [Tool("mcp_finance_snapshot")]

    async def get_callable_function(self, func_name: str, wrap_tool_result: bool = True):
        async def mcp_finance_snapshot(symbol: str = "NVDA") -> ToolResponse:
            return text_response({"symbol": symbol, "snapshot": "mock_finance_ok"})

        mcp_finance_snapshot.__name__ = func_name
        return mcp_finance_snapshot
