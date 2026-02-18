import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.message import Msg
from agentscope.pipeline import FanoutPipeline

from common import DelayAgent, ensure, timed


async def run_validation() -> None:
    pipeline = FanoutPipeline(
        [
            DelayAgent("a1", 0.2, "A"),
            DelayAgent("a2", 0.2, "B"),
            DelayAgent("a3", 0.2, "C"),
        ],
        enable_gather=True,
    )
    out, elapsed = await timed(pipeline(Msg(name="user", role="user", content="demo")))
    ensure(len(out) == 3, "class fanout output size mismatch")
    ensure(elapsed < 0.4, f"class fanout should overlap, elapsed={elapsed:.3f}s")


async def main() -> None:
    await run_validation()
    print("PASS: class fanout pipeline")


if __name__ == "__main__":
    asyncio.run(main())
