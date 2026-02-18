import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.message import Msg
from agentscope.pipeline import sequential_pipeline

from common import PrefixAgent, ensure


async def run_validation() -> None:
    agents = [
        PrefixAgent("a1", "[step1]"),
        PrefixAgent("a2", "[step2]"),
    ]
    out = await sequential_pipeline(
        agents,
        Msg(name="user", role="user", content="pipeline demo"),
    )
    ensure(isinstance(out, Msg), "sequential output type mismatch")
    ensure(str(out.content) == "[step2][step1]pipeline demo", "sequential output mismatch")


async def main() -> None:
    await run_validation()
    print("PASS: function sequential pipeline")


if __name__ == "__main__":
    asyncio.run(main())
