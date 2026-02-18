import asyncio
from time import perf_counter
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.tool import Toolkit

from common import call_tool_text, ensure, reverse_text_nonblocking


async def run_validation() -> None:
    toolkit = Toolkit()
    toolkit.register_tool_function(
        reverse_text_nonblocking,
        func_name="reverse_text_nonblocking",
    )

    start = perf_counter()
    results = await asyncio.gather(
        call_tool_text(
            toolkit,
            "reverse_text_nonblocking",
            {"text": "abc", "delay_s": 0.2},
        ),
        call_tool_text(
            toolkit,
            "reverse_text_nonblocking",
            {"text": "def", "delay_s": 0.2},
        ),
        call_tool_text(
            toolkit,
            "reverse_text_nonblocking",
            {"text": "ghi", "delay_s": 0.2},
        ),
    )
    elapsed = perf_counter() - start

    ensure(results == ["cba", "fed", "ihg"], "async tool result validation failed")
    # Non-blocking async functions should overlap and finish close to single delay.
    ensure(
        elapsed < 0.4,
        f"async tool did not show concurrency behavior, elapsed={elapsed:.3f}s",
    )
    print(f"async elapsed: {elapsed:.3f}s (expected ~0.2s concurrent)")


async def main() -> None:
    await run_validation()
    print("PASS: async function tool")


if __name__ == "__main__":
    asyncio.run(main())
