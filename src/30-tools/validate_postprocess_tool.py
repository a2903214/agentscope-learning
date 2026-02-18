import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.tool import Toolkit

from common import call_tool_text, echo, ensure, postprocess_append_ok


async def run_validation() -> None:
    toolkit = Toolkit()
    toolkit.register_tool_function(
        echo,
        func_name="echo_postprocess",
        postprocess_func=postprocess_append_ok,
    )
    postprocess_result = await call_tool_text(toolkit, "echo_postprocess", {"text": "demo"})
    ensure(postprocess_result == "demo|OK", "postprocess validation failed")


async def main() -> None:
    await run_validation()
    print("PASS: postprocess tool")


if __name__ == "__main__":
    asyncio.run(main())
