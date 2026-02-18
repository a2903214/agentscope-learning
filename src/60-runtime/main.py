import asyncio

from validate_end_to_end_runtime_case import run_validation as run_end_to_end_runtime_case
from validate_flow_stage_cases import run_validation as run_flow_stage_cases
from validate_sandbox_cases import run_validation as run_sandbox_cases


async def main() -> None:
    print("=== Runtime Validation Start ===")
    await run_flow_stage_cases()
    print("PASS: runtime stage cases")
    await run_sandbox_cases()
    print("PASS: runtime sandbox cases")
    await run_end_to_end_runtime_case()
    print("PASS: runtime end-to-end case")
    print("=== ALL RUNTIME VALIDATIONS PASSED ===")


if __name__ == "__main__":
    asyncio.run(main())
