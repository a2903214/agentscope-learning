import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.message import Msg

from common import ensure, extract_text
from memory_mocks import TaskLongTermMemory


async def run_validation() -> None:
    memory = TaskLongTermMemory()

    await memory.record(
        [
            Msg(name="user", role="user", content="任务A：整理文档。"),
            Msg(name="assistant", role="assistant", content="TODO: 增加测试用例。"),
        ],
    )
    retrieved = await memory.retrieve(Msg(name="user", role="user", content="任务 TODO"), limit=5)
    ensure("任务A" in retrieved and "TODO" in retrieved, "task retrieve mismatch")

    tool_resp = await memory.record_to_memory("补充任务", ["任务B：提交代码。"])
    ensure("recorded=1" in extract_text(tool_resp), "task record_to_memory mismatch")

    tool_search = await memory.retrieve_from_memory(["任务B"], limit=3)
    ensure("任务B" in extract_text(tool_search), "task retrieve_from_memory mismatch")


async def main() -> None:
    await run_validation()
    print("PASS: task long-term memory case")


if __name__ == "__main__":
    asyncio.run(main())
