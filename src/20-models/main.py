import asyncio
import os
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


def build_model_configs() -> list[dict]:
    default_model = MODEL_NAME
    backup_model = os.getenv("OPENAI_MODEL_BACKUP", default_model)
    return [
        {"config_name": "default_model", "model_name": default_model},
        {"config_name": "backup_model", "model_name": backup_model},
    ]


def create_agent(model_name: str) -> ReActAgent:
    model = OpenAIChatModel(**get_openai_chat_model_kwargs(model_name))
    formatter = OpenAIChatFormatter()
    return ReActAgent(
        name=f"agent_{model_name}",
        sys_prompt="You are a concise assistant.",
        model=model,
        formatter=formatter,
    )


def extract_text_content(response: Msg) -> str:
    content = response.content if hasattr(response, "content") else response
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text" and item.get("text"):
                    text_parts.append(str(item["text"]))
            elif hasattr(item, "text"):
                text = getattr(item, "text")
                if text:
                    text_parts.append(str(text))
        if text_parts:
            return " ".join(text_parts).strip()

    return str(content).strip()


async def run_once(model_name: str) -> str:
    agent = create_agent(model_name)
    response = await agent(
        Msg(
            name="user",
            role="user",
            content="请用一句中文介绍 AgentScope 的核心用途。",
        ),
    )
    return extract_text_content(response)


async def main() -> None:
    agentscope.init(project="agentscope-learning", name="20-models")
    model_configs = build_model_configs()
    default_name = model_configs[0]["config_name"]

    print("Loaded model configs:")
    for cfg in model_configs:
        print(f"- {cfg['config_name']}: {cfg['model_name']}")
    print(f"Selected default model: {default_name} -> {model_configs[0]['model_name']}")

    default_reply = await run_once(model_configs[0]["model_name"])
    backup_reply = await run_once(model_configs[1]["model_name"])

    print("\n=== Response Comparison ===")
    print(f"default_model: {default_reply}")
    print(f"backup_model : {backup_reply}")

    if default_reply == backup_reply:
        print("WARN: Both replies are identical. Try setting OPENAI_MODEL_BACKUP differently.")
    else:
        print("PASS: Different model outputs observed.")


if __name__ == "__main__":
    asyncio.run(main())
