import asyncio
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

import agentscope
from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.message import Msg, ToolUseBlock
from agentscope.model import OpenAIChatModel
from agentscope.tool import ToolResponse, Toolkit

from common import ensure, extract_text, text_response

# Allow importing shared model config from src/.
from global_model_config import MODEL_NAME, get_openai_chat_model_kwargs  # noqa: E402


def _extract_msg_text(msg: Msg) -> str:
    content = msg.content if hasattr(msg, "content") else msg
    if isinstance(content, str):
        return content

    text_parts: list[str] = []
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(str(item.get("text", "")))
            elif hasattr(item, "text"):
                text_parts.append(str(getattr(item, "text", "")))
    return " ".join(part for part in text_parts if part).strip()


async def run_validation() -> None:
    agentscope.init(project="agentscope-learning", name="30-tools-llm-validation")

    toolkit = Toolkit()
    tracker: dict[str, Any] = {
        "called": False,
        "tool_name": "",
        "tool_input": {},
        "tool_result": "",
    }

    def lookup_project_token(key: str) -> ToolResponse:
        mapping = {
            "agentscope": "AS-LRN-2026",
            "runtime": "AS-RT-2026",
        }
        return text_response(mapping.get(key.lower(), "UNKNOWN"))

    def capture_tool_call(tool_call: ToolUseBlock, tool_resp: ToolResponse) -> ToolResponse:
        tracker["called"] = True
        tracker["tool_name"] = tool_call["name"]
        tracker["tool_input"] = dict(tool_call["input"])
        tracker["tool_result"] = extract_text(tool_resp)
        return tool_resp

    toolkit.register_tool_function(
        lookup_project_token,
        func_name="lookup_project_token",
        func_description="Return internal project token by key.",
        postprocess_func=capture_tool_call,
    )

    model = OpenAIChatModel(**get_openai_chat_model_kwargs(MODEL_NAME))
    formatter = OpenAIChatFormatter()
    agent = ReActAgent(
        name="tool_validation_agent",
        sys_prompt=(
            "You are a strict assistant. "
            "When user asks for token, you MUST call tool `lookup_project_token` "
            "and return exactly one line in format RESULT=<token>."
        ),
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        parallel_tool_calls=False,
        print_hint_msg=False,
    )

    response = await agent(
        Msg(
            name="user",
            role="user",
            content=(
                "请调用工具 lookup_project_token 获取 key=agentscope 的 token。"
                "不要自己猜测，不要解释。最后仅返回 RESULT=<token>。"
            ),
        ),
    )
    reply_text = _extract_msg_text(response)

    ensure(tracker["called"], "LLM did not call tool as expected")
    ensure(tracker["tool_name"] == "lookup_project_token", "Unexpected tool called by LLM")
    ensure(
        str(tracker["tool_input"].get("key", "")).lower() == "agentscope",
        "Tool input key mismatch",
    )
    ensure(tracker["tool_result"] == "AS-LRN-2026", "Tool returned unexpected result")
    ensure("AS-LRN-2026" in reply_text, "Final LLM reply does not include tool result")

    print(f"TOOL CALLED: {tracker['tool_name']}({tracker['tool_input']})")
    print(f"TOOL RESULT: {tracker['tool_result']}")
    print(f"MODEL REPLY: {reply_text}")


async def main() -> None:
    await run_validation()
    print("PASS: llm-driven tool invocation")


if __name__ == "__main__":
    asyncio.run(main())
