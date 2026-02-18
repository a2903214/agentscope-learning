import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

import agentscope
from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.message import Msg
from agentscope.model import OpenAIChatModel

from global_model_config import MODEL_NAME, get_openai_chat_model_kwargs  # noqa: E402


async def main() -> None:
    agentscope.init(project="agentscope-learning", name="10-hello-agentscope")

    model = OpenAIChatModel(**get_openai_chat_model_kwargs(MODEL_NAME))
    formatter = OpenAIChatFormatter()

    agent = ReActAgent(
        name="hello_agent",
        sys_prompt="You are a concise assistant.",
        model=model,
        formatter=formatter,
    )

    response = await agent(
        Msg(
            name="user",
            role="user",
            content="Reply with exactly: AGENTSCOPE_OK",
        ),
    )
    text = response.content if hasattr(response, "content") else str(response)
    print("Agent response:", text)

    if "AGENTSCOPE_OK" in str(text):
        print("PASS: AgentScope hello validation succeeded.")
        raise SystemExit(0)

    print("FAIL: Agent response did not match expected content.")
    raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
