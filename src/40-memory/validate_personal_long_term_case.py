import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.message import Msg

from common import ensure, extract_text
from memory_mocks import PersonalLongTermMemory


async def run_validation() -> None:
    memory = PersonalLongTermMemory()

    await memory.record(
        [
            Msg(name="user", role="user", content="我叫小李。"),
            Msg(name="user", role="user", content="我喜欢篮球。"),
            Msg(name="user", role="user", content="今天天气不错。"),
        ],
    )
    retrieved = await memory.retrieve(Msg(name="user", role="user", content="小李 喜欢"), limit=5)
    ensure("我叫小李" in retrieved and "我喜欢篮球" in retrieved, "personal retrieve mismatch")

    tool_resp = await memory.record_to_memory("记录偏好", ["我在杭州工作。"])
    ensure("recorded=1" in extract_text(tool_resp), "personal record_to_memory mismatch")

    tool_search = await memory.retrieve_from_memory(["杭州"], limit=3)
    ensure("杭州" in extract_text(tool_search), "personal retrieve_from_memory mismatch")


async def main() -> None:
    await run_validation()
    print("PASS: personal long-term memory case")


if __name__ == "__main__":
    asyncio.run(main())
