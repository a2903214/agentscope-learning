import asyncio

from common import (
    assert_event_guard_can_detect_corruption,
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
        payloads = await post_process_and_collect(
            port=port,
            prompt="sandbox=all end-to-end runtime case",
            session_id="runtime-e2e-case",
        )
        events, final_result = parse_stage_events_from_payloads(payloads)
        validate_event_reasonability(events, require_all_sandboxes=True)
        started = [e.sandbox for e in events if e.phase == "sandbox_started"]
        unavailable = [e.sandbox for e in events if e.phase == "sandbox_unavailable"]
        ensure("local_python" in started, "local_python should run in full flow")
        ensure("mcp" in started, "mcp should run in full flow")
        ensure(
            ("docker" in started) or ("docker" in unavailable),
            "docker should run or emit unavailable",
        )
        ensure(final_result != "", "final result should not be empty")
        assert_event_guard_can_detect_corruption(events)
    finally:
        stop_runtime_server(proc)


async def main() -> None:
    await run_validation()
    print("PASS: runtime end-to-end case")


if __name__ == "__main__":
    asyncio.run(main())
