import asyncio
from time import perf_counter
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.tool import Toolkit

from common import add_blocking, call_tool_text, ensure


async def run_validation() -> None:
    toolkit = Toolkit()
    toolkit.register_tool_function(add_blocking, func_name="add_blocking")

    start = perf_counter()
    results = await asyncio.gather(
        call_tool_text(toolkit, "add_blocking", {"a": 1, "b": 1, "delay_s": 0.2}),
        call_tool_text(toolkit, "add_blocking", {"a": 2, "b": 2, "delay_s": 0.2}),
        call_tool_text(toolkit, "add_blocking", {"a": 3, "b": 3, "delay_s": 0.2}),
    )
    elapsed = perf_counter() - start

    ensure(results == ["2", "4", "6"], "sync tool result validation failed")
    # Blocking sync functions usually run effectively serially in this scenario.
    ensure(
        elapsed >= 0.5,
        f"sync tool did not show blocking behavior, elapsed={elapsed:.3f}s",
    )
    print(f"sync elapsed: {elapsed:.3f}s (expected ~0.6s serial)")


async def main() -> None:
    await run_validation()
    print("PASS: sync function tool")


if __name__ == "__main__":
    asyncio.run(main())
