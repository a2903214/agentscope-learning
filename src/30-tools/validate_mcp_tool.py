import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.tool import Toolkit

from common import FakeMcpClient, call_tool_text, ensure


async def run_validation() -> None:
    toolkit = Toolkit()
    toolkit.create_tool_group("mcp_tools", description="MCP tools", active=True)
    await toolkit.register_mcp_client(FakeMcpClient(), group_name="mcp_tools")
    mcp_tool_names = [name for name in toolkit.tools.keys() if "mcp_ping" in name]
    ensure(len(mcp_tool_names) > 0, "mcp tool was not registered")
    mcp_result = await call_tool_text(toolkit, mcp_tool_names[0], {"payload": "hello"})
    ensure("hello" in mcp_result, "mcp tool validation failed")


async def main() -> None:
    await run_validation()
    print("PASS: MCP tool (mock client)")


if __name__ == "__main__":
    asyncio.run(main())
