from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

import asyncio
import time
import uuid
from typing import Any

from agentscope.message import ToolUseBlock
from agentscope.tool import ToolResponse, Toolkit


def text_response(text: str, *, stream: bool = False, is_last: bool = True) -> ToolResponse:
    return ToolResponse(
        content=[{"type": "text", "text": text}],
        stream=stream,
        is_last=is_last,
    )


def extract_text(resp: ToolResponse) -> str:
    parts: list[str] = []
    for block in resp.content:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(str(block.get("text", "")))
    return " ".join(parts).strip()


def to_tool_use(name: str, input_data: dict[str, Any]) -> ToolUseBlock:
    return ToolUseBlock(
        type="tool_use",
        id=str(uuid.uuid4()),
        name=name,
        input=input_data,
    )


async def call_tool_text(toolkit: Toolkit, name: str, input_data: dict[str, Any]) -> str:
    final_resp: ToolResponse | None = None
    result_stream = await toolkit.call_tool_function(to_tool_use(name, input_data))
    async for chunk in result_stream:
        final_resp = chunk
    if final_resp is None:
        raise RuntimeError(f"No tool response received for {name}.")
    return extract_text(final_resp)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def add(a: int, b: int) -> ToolResponse:
    return text_response(f"{a + b}")


async def reverse_text(text: str) -> ToolResponse:
    return text_response(text[::-1])


def add_blocking(a: int, b: int, delay_s: float = 0.2) -> ToolResponse:
    # Intentionally block to demonstrate sync tool behavior.
    time.sleep(delay_s)
    return text_response(f"{a + b}")


async def reverse_text_nonblocking(text: str, delay_s: float = 0.2) -> ToolResponse:
    # Intentionally await to demonstrate async tool concurrency.
    await asyncio.sleep(delay_s)
    return text_response(text[::-1])


async def stream_numbers(n: int) -> ToolResponse:
    if n <= 0:
        return text_response("")
    values = [str(i) for i in range(1, n + 1)]
    return text_response(",".join(values))


def greet(name: str, role: str) -> ToolResponse:
    return text_response(f"{role}:{name}")


def echo(text: str) -> ToolResponse:
    return text_response(text)


def postprocess_append_ok(_tool_call: ToolUseBlock, tool_resp: ToolResponse) -> ToolResponse:
    return text_response(f"{extract_text(tool_resp)}|OK")


def custom_schema_demo(topic: str, max_items: int = 3) -> ToolResponse:
    return text_response(f"{topic}:{max_items}")


class FakeMcpTool:
    def __init__(self, name: str) -> None:
        self.name = name


class FakeMcpClient:
    name = "fake_mcp"

    async def list_tools(self) -> list[FakeMcpTool]:
        return [FakeMcpTool("mcp_ping")]

    async def get_callable_function(self, func_name: str, wrap_tool_result: bool = True):
        async def _mcp_ping(payload: str = "ping") -> ToolResponse:
            suffix = "wrapped" if wrap_tool_result else "raw"
            return text_response(f"mcp:{payload}:{suffix}")

        if func_name != "mcp_ping":
            raise ValueError(f"Unknown fake MCP function: {func_name}")
        return _mcp_ping
