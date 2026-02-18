import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.message import Msg
from agentscope.pipeline import SequentialPipeline

from common import PrefixAgent, ensure


async def run_validation() -> None:
    pipeline = SequentialPipeline(
        [
            PrefixAgent("a1", "[class1]"),
            PrefixAgent("a2", "[class2]"),
        ],
    )
    out = await pipeline(Msg(name="user", role="user", content="demo"))
    ensure(isinstance(out, Msg), "class sequential output type mismatch")
    ensure(str(out.content) == "[class2][class1]demo", "class sequential output mismatch")


async def main() -> None:
    await run_validation()
    print("PASS: class sequential pipeline")


if __name__ == "__main__":
    asyncio.run(main())
