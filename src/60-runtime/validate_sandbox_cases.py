import asyncio

from common import (
    ensure,
    parse_stage_events_from_payloads,
    pick_free_port,
    post_process_and_collect,
    start_runtime_server,
    stop_runtime_server,
    validate_event_reasonability,
)


async def run_validation() -> None:
    port = pick_free_port()
    proc = start_runtime_server(port)
    try:
        cases = [
            ("local_python", "local_python_done:"),
            ("docker", "docker_done:"),
            ("mcp", "mcp_done:"),
        ]
        for sandbox, expected_prefix in cases:
            payloads = await post_process_and_collect(
                port=port,
                prompt=f"sandbox={sandbox} sandbox case",
                session_id=f"runtime-sandbox-{sandbox}",
            )
            events, final_result = parse_stage_events_from_payloads(payloads)
            validate_event_reasonability(events, require_all_sandboxes=False)
            unavailable = [e for e in events if e.phase == "sandbox_unavailable"]
            if unavailable:
                ensure(sandbox == "docker", "only docker can be unavailable in local setup")
                ensure(unavailable[0].status == "skipped", "docker unavailable status mismatch")
                continue
            ensure(final_result.startswith(expected_prefix), f"{sandbox} final result mismatch")
    finally:
        stop_runtime_server(proc)


async def main() -> None:
    await run_validation()
    print("PASS: runtime sandbox cases")


if __name__ == "__main__":
    asyncio.run(main())
