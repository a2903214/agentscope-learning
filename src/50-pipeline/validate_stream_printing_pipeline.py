import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.message import Msg
from agentscope.pipeline import stream_printing_messages

from common import QueuePrintAgent, ensure


async def run_validation() -> None:
    agent = QueuePrintAgent("printer", ["chunk-1", "chunk-2", "chunk-3"])
    task = agent(Msg(name="user", role="user", content="start"))

    collected: list[str] = []
    async for msg, _is_last in stream_printing_messages([agent], task):
        collected.append(str(msg.content))

    ensure(collected == ["chunk-1", "chunk-2", "chunk-3"], "stream printing output mismatch")


async def main() -> None:
    await run_validation()
    print("PASS: stream printing pipeline")


if __name__ == "__main__":
    asyncio.run(main())
