import asyncio
from time import perf_counter
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.message import Msg


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def text_of(msg: Msg | list[Msg] | None) -> str:
    if isinstance(msg, Msg):
        return str(msg.content)
    if isinstance(msg, list):
        return " | ".join(str(m.content) for m in msg)
    return ""


class PrefixAgent:
    def __init__(self, name: str, prefix: str) -> None:
        self.name = name
        self.prefix = prefix

    async def __call__(self, msg: Msg | list[Msg] | None, **kwargs) -> Msg:
        src = text_of(msg)
        return Msg(name=self.name, role="assistant", content=f"{self.prefix}{src}")


class DelayAgent:
    def __init__(self, name: str, delay_s: float, content: str) -> None:
        self.name = name
        self.delay_s = delay_s
        self.content = content

    async def __call__(self, msg: Msg | list[Msg] | None, **kwargs) -> Msg:
        await asyncio.sleep(self.delay_s)
        return Msg(name=self.name, role="assistant", content=self.content)


class QueuePrintAgent:
    def __init__(self, name: str, outputs: list[str]) -> None:
        self.name = name
        self.outputs = outputs
        self._queue: asyncio.Queue | None = None
        self._enabled = False

    def set_msg_queue_enabled(self, enabled: bool, queue: asyncio.Queue) -> None:
        self._enabled = enabled
        self._queue = queue

    async def __call__(self, msg: Msg | list[Msg] | None, **kwargs) -> Msg:
        if self._enabled and self._queue is not None:
            for text in self.outputs:
                await self._queue.put(
                    (
                        Msg(name=self.name, role="assistant", content=text),
                        True,
                        None,
                    ),
                )
        return Msg(name=self.name, role="assistant", content=self.outputs[-1])


async def timed(coro):
    start = perf_counter()
    result = await coro
    return result, perf_counter() - start
