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
        [Msg(name="user", role="user", content="我正在做 AgentScope 学习项目。")],
    )
    await memory.update_compressed_summary("用户在进行 AgentScope 学习。")

    mem = await memory.get_memory(prepend_summary=True)
    ensure(len(mem) >= 2, "summary prepend did not work")
    ensure("学习" in str(mem[0].content), "summary content mismatch")

    mem_no_summary = await memory.get_memory(prepend_summary=False)
    ensure(len(mem_no_summary) == 1, "summary disable prepend mismatch")


async def main() -> None:
    await run_validation()
    print("PASS: summary memory case")


if __name__ == "__main__":
    asyncio.run(main())
