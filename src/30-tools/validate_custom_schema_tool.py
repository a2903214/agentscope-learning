import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.tool import Toolkit

from common import call_tool_text, custom_schema_demo, ensure


async def run_validation() -> None:
    toolkit = Toolkit()
    custom_schema = {
        "type": "function",
        "function": {
            "name": "custom_schema_demo",
            "description": "Custom schema tool demo",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "max_items": {"type": "integer"},
                },
                "required": ["topic"],
            },
        },
    }
    toolkit.register_tool_function(
        custom_schema_demo,
        func_name="custom_schema_demo",
        json_schema=custom_schema,
    )
    custom_result = await call_tool_text(
        toolkit,
        "custom_schema_demo",
        {"topic": "agentscope", "max_items": 2},
    )
    ensure(custom_result == "agentscope:2", "custom schema tool validation failed")


async def main() -> None:
    await run_validation()
    print("PASS: custom JSON schema tool")


if __name__ == "__main__":
    asyncio.run(main())
