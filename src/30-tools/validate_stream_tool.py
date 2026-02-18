import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.tool import Toolkit

from common import call_tool_text, ensure, stream_numbers


async def run_validation() -> None:
    toolkit = Toolkit()
    toolkit.register_tool_function(stream_numbers, func_name="stream_numbers")
    stream_result = await call_tool_text(toolkit, "stream_numbers", {"n": 4})
    ensure(stream_result == "1,2,3,4", "stream tool validation failed")


async def main() -> None:
    await run_validation()
    print("PASS: stream output tool")


if __name__ == "__main__":
    asyncio.run(main())
