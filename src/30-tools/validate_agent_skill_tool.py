import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

from agentscope.tool import Toolkit

from common import ensure


async def run_validation() -> None:
    toolkit = Toolkit()
    skill_dir = Path(__file__).resolve().parent / "skills" / "demo-skill"
    toolkit.register_agent_skill(str(skill_dir))
    skill_prompt = toolkit.get_agent_skill_prompt()
    ensure("demo-skill" in skill_prompt, "agent skill registration failed")


async def main() -> None:
    await run_validation()
    print("PASS: agent skill tool")


if __name__ == "__main__":
    asyncio.run(main())
