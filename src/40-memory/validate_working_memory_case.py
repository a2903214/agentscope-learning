import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.memory import InMemoryMemory
from agentscope.message import Msg

from common import ensure


async def run_validation() -> None:
    memory = InMemoryMemory()
    await memory.add(
        [
            Msg(name="user", role="user", content="你好"),
            Msg(name="assistant", role="assistant", content="你好，请问需要什么帮助？"),
        ],
        marks="dialog",
    )
    size = await memory.size()
    ensure(size == 2, "working memory size mismatch")

    mem = await memory.get_memory(mark="dialog")
    ensure(len(mem) == 2, "working memory retrieval mismatch")
    ensure(str(mem[0].content) == "你好", "working memory first message mismatch")


async def main() -> None:
    await run_validation()
    print("PASS: working memory case")


if __name__ == "__main__":
    asyncio.run(main())
