from agentscope.tool import ToolResponse

from .common import text_response


class SearchMCPMock:
    name = "search_mcp_mock"

    async def list_tools(self):
        class Tool:
            def __init__(self, name: str) -> None:
                self.name = name

        return [Tool("mcp_search_hint")]

    async def get_callable_function(self, func_name: str, wrap_tool_result: bool = True):
        async def mcp_search_hint(topic: str = "AI算力") -> ToolResponse:
            return text_response(f"[MCP] search hint ready for topic={topic}")

        mcp_search_hint.__name__ = func_name
        return mcp_search_hint


class FinanceMCPMock:
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
