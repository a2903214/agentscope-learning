import asyncio

from validate_agent_skill_tool import run_validation as run_agent_skill_tool
from validate_async_tool import run_validation as run_async_tool
from validate_custom_schema_tool import run_validation as run_custom_schema_tool
from validate_group_activation import run_validation as run_group_activation
from validate_mcp_tool import run_validation as run_mcp_tool
from validate_postprocess_tool import run_validation as run_postprocess_tool
from validate_preset_kwargs_tool import run_validation as run_preset_kwargs_tool
from validate_stream_tool import run_validation as run_stream_tool
from validate_sync_tool import run_validation as run_sync_tool
from validate_llm_tool_invocation import run_validation as run_llm_tool_invocation


async def main() -> None:
    print("=== Tool Validation Start ===")

    await run_sync_tool()
    print("PASS: sync function tool")
    await run_async_tool()
    print("PASS: async function tool")
    await run_stream_tool()
    print("PASS: stream output tool")
    await run_group_activation()
    print("PASS: tool group activation")
    await run_preset_kwargs_tool()
    print("PASS: preset kwargs tool")
    await run_postprocess_tool()
    print("PASS: postprocess tool")
    await run_custom_schema_tool()
    print("PASS: custom JSON schema tool")
    await run_agent_skill_tool()
    print("PASS: agent skill tool")
    await run_mcp_tool()
    print("PASS: MCP tool (mock client)")
    await run_llm_tool_invocation()
    print("PASS: llm-driven tool invocation")

    print("=== ALL TOOL VALIDATIONS PASSED ===")


if __name__ == "__main__":
    asyncio.run(main())
