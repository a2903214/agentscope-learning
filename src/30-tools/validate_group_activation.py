import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.tool import Toolkit

from common import add, ensure


async def run_validation() -> None:
    toolkit = Toolkit()
    toolkit.create_tool_group("math_tools", description="Math tools", active=False)
    toolkit.register_tool_function(add, group_name="math_tools", func_name="add_grouped")
    schemas_before = toolkit.get_json_schemas()
    toolkit.update_tool_groups(["math_tools"], active=True)
    schemas_after = toolkit.get_json_schemas()
    names_before = {s["function"]["name"] for s in schemas_before}
    names_after = {s["function"]["name"] for s in schemas_after}
    ensure("add_grouped" not in names_before, "group activation pre-check failed")
    ensure("add_grouped" in names_after, "group activation post-check failed")


async def main() -> None:
    await run_validation()
    print("PASS: tool group activation")


if __name__ == "__main__":
    asyncio.run(main())
