import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.message import Msg

from common import ensure, extract_text
from memory_mocks import ToolLongTermMemory


async def run_validation() -> None:
    memory = ToolLongTermMemory()

    await memory.record(
        [
            Msg(name="assistant", role="assistant", content="工具调用 search_docs 成功。"),
            Msg(name="assistant", role="assistant", content="tool fetch_api 报错 429。"),
        ],
    )
    retrieved = await memory.retrieve(Msg(name="user", role="user", content="tool 工具"), limit=5)
    ensure("search_docs" in retrieved and "429" in retrieved, "tool retrieve mismatch")

    tool_resp = await memory.record_to_memory("记录工具经验", ["工具重试策略：指数退避。"])
    ensure("recorded=1" in extract_text(tool_resp), "tool record_to_memory mismatch")

    tool_search = await memory.retrieve_from_memory(["重试"], limit=3)
    ensure("指数退避" in extract_text(tool_search), "tool retrieve_from_memory mismatch")


async def main() -> None:
    await run_validation()
    print("PASS: tool long-term memory case")


if __name__ == "__main__":
    asyncio.run(main())
