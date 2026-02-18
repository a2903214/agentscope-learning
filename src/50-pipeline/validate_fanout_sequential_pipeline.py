import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.message import Msg
from agentscope.pipeline import fanout_pipeline

from common import DelayAgent, ensure, timed


async def run_validation() -> None:
    agents = [
        DelayAgent("a1", 0.2, "A"),
        DelayAgent("a2", 0.2, "B"),
        DelayAgent("a3", 0.2, "C"),
    ]
    out, elapsed = await timed(
        fanout_pipeline(
            agents,
            Msg(name="user", role="user", content="fanout"),
            enable_gather=False,
        ),
    )
    ensure(len(out) == 3, "fanout sequential output size mismatch")
    ensure(elapsed >= 0.5, f"fanout sequential should be serial, elapsed={elapsed:.3f}s")


async def main() -> None:
    await run_validation()
    print("PASS: function fanout sequential pipeline")


if __name__ == "__main__":
    asyncio.run(main())
