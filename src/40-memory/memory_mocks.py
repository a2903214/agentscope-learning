from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.memory import LongTermMemoryBase
from agentscope.message import Msg
from agentscope.tool import ToolResponse

from common import text_response


class PersonalLongTermMemory(LongTermMemoryBase):
    def __init__(self) -> None:
        super().__init__()
        self.facts: list[str] = []

    async def record(self, msgs: list[Msg | None], **kwargs):
        for msg in msgs:
            if msg is None:
                continue
            text = str(msg.content)
            if any(k in text for k in ["我叫", "我喜欢", "我在"]):
                self.facts.append(text)

    async def retrieve(self, msg: Msg | list[Msg] | None, limit: int = 5, **kwargs) -> str:
        query = str(msg.content) if isinstance(msg, Msg) else str(msg)
        matched = [f for f in self.facts if any(token in f for token in query.split())]
        return "\n".join(matched[:limit])

    async def record_to_memory(self, thinking: str, content: list[str], **kwargs) -> ToolResponse:
        self.facts.extend(content)
        return text_response(f"recorded={len(content)}")

    async def retrieve_from_memory(
        self,
        keywords: list[str],
        limit: int = 5,
        **kwargs,
    ) -> ToolResponse:
        matched: list[str] = []
        for item in self.facts:
            if any(k in item for k in keywords):
                matched.append(item)
        return text_response("\n".join(matched[:limit]))


class TaskLongTermMemory(LongTermMemoryBase):
    def __init__(self) -> None:
        super().__init__()
        self.tasks: list[str] = []

    async def record(self, msgs: list[Msg | None], **kwargs):
        for msg in msgs:
            if msg is None:
                continue
            text = str(msg.content)
            if any(k in text for k in ["任务", "TODO", "完成"]):
                self.tasks.append(text)

    async def retrieve(self, msg: Msg | list[Msg] | None, limit: int = 5, **kwargs) -> str:
        query = str(msg.content) if isinstance(msg, Msg) else str(msg)
        matched = [t for t in self.tasks if any(token in t for token in query.split())]
        return "\n".join(matched[:limit])

    async def record_to_memory(self, thinking: str, content: list[str], **kwargs) -> ToolResponse:
        self.tasks.extend(content)
        return text_response(f"recorded={len(content)}")

    async def retrieve_from_memory(
        self,
        keywords: list[str],
        limit: int = 5,
        **kwargs,
    ) -> ToolResponse:
        matched: list[str] = []
        for item in self.tasks:
            if any(k in item for k in keywords):
                matched.append(item)
        return text_response("\n".join(matched[:limit]))


class ToolLongTermMemory(LongTermMemoryBase):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[str] = []

    async def record(self, msgs: list[Msg | None], **kwargs):
        for msg in msgs:
            if msg is None:
                continue
            text = str(msg.content)
            if any(k in text for k in ["tool", "工具", "调用", "报错"]):
                self.records.append(text)

    async def retrieve(self, msg: Msg | list[Msg] | None, limit: int = 5, **kwargs) -> str:
        query = str(msg.content) if isinstance(msg, Msg) else str(msg)
        matched = [r for r in self.records if any(token in r for token in query.split())]
        return "\n".join(matched[:limit])

    async def record_to_memory(self, thinking: str, content: list[str], **kwargs) -> ToolResponse:
        self.records.extend(content)
        return text_response(f"recorded={len(content)}")

    async def retrieve_from_memory(
        self,
        keywords: list[str],
        limit: int = 5,
        **kwargs,
    ) -> ToolResponse:
        matched: list[str] = []
        for item in self.records:
            if any(k in item for k in keywords):
                matched.append(item)
        return text_response("\n".join(matched[:limit]))
