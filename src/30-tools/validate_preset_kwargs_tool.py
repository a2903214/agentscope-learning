import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.tool import Toolkit

from common import call_tool_text, ensure, greet


async def run_validation() -> None:
    toolkit = Toolkit()
    toolkit.register_tool_function(
        greet,
        func_name="greet_with_role",
        preset_kwargs={"role": "mentor"},
    )
    greet_result = await call_tool_text(toolkit, "greet_with_role", {"name": "alice"})
    ensure(greet_result == "mentor:alice", "preset kwargs validation failed")


async def main() -> None:
    await run_validation()
    print("PASS: preset kwargs tool")


if __name__ == "__main__":
    asyncio.run(main())
