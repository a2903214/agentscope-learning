import asyncio

from validate_personal_long_term_case import run_validation as run_personal_long_term_case
from validate_summary_memory_case import run_validation as run_summary_memory_case
from validate_task_long_term_case import run_validation as run_task_long_term_case
from validate_tool_long_term_case import run_validation as run_tool_long_term_case
from validate_working_memory_case import run_validation as run_working_memory_case


async def main() -> None:
    print("=== Memory Validation Start ===")

    await run_working_memory_case()
    print("PASS: working memory case")
    await run_summary_memory_case()
    print("PASS: summary memory case")
    await run_personal_long_term_case()
    print("PASS: personal long-term memory case")
    await run_task_long_term_case()
    print("PASS: task long-term memory case")
    await run_tool_long_term_case()
    print("PASS: tool long-term memory case")

    print("=== ALL MEMORY VALIDATIONS PASSED ===")


if __name__ == "__main__":
    asyncio.run(main())
