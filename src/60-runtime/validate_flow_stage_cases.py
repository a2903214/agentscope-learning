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
        payloads = await post_process_and_collect(
            port=port,
            prompt="sandbox=local_python stage case",
            session_id="runtime-stage-case",
        )
        events, final_result = parse_stage_events_from_payloads(payloads)
        validate_event_reasonability(events, require_all_sandboxes=False)
        ensure(final_result.startswith("local_python_done:"), "local_python final result mismatch")
    finally:
        stop_runtime_server(proc)


async def main() -> None:
    await run_validation()
    print("PASS: runtime stage cases")


if __name__ == "__main__":
    asyncio.run(main())
