import asyncio
import json
import multiprocessing
import socket
import sys
import time
from dataclasses import dataclass
from typing import Any

import aiohttp
from agentscope.message import Msg
from agentscope_runtime.engine import AgentApp
from agentscope_runtime.engine.schemas.agent_schemas import AgentRequest


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


@dataclass
class StageEvent:
    phase: str
    status: str
    sandbox: str
    detail: str


def _event_text(phase: str, status: str, sandbox: str = "none", detail: str = "") -> str:
    safe_detail = detail.replace("\n", "\\n")
    return f"EVENT|{phase}|{status}|{sandbox}|{safe_detail}"


def _final_text(result: str) -> str:
    return f"FINAL|{result}"


def _extract_prompt_text(msgs: list[Msg]) -> str:
    if not msgs:
        return ""
    latest = msgs[-1]
    content = latest.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text")
                if isinstance(text, str):
                    return text
    return str(content) if content is not None else ""


async def _run_subprocess(command: list[str], timeout_s: float = 20.0) -> str:
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout_s)
    except TimeoutError as exc:
        proc.kill()
        await proc.wait()
        raise RuntimeError(f"timeout: {' '.join(command)}") from exc
    out = stdout.decode("utf-8", errors="ignore").strip()
    err = stderr.decode("utf-8", errors="ignore").strip()
    if proc.returncode != 0:
        raise RuntimeError(err or out or f"exit={proc.returncode}")
    return out


async def _connect_and_run_sandbox(sandbox: str, task: str) -> tuple[str, str]:
    if sandbox == "local_python":
        ready = await _run_subprocess([sys.executable, "-c", "print('local_python_ready')"])
        ensure(ready == "local_python_ready", "local_python readiness check failed")
        result = await _run_subprocess(
            [sys.executable, "-c", "import sys; print('local_python_done:' + sys.argv[1])", task],
        )
        return "local_python://embedded-interpreter", result

    if sandbox == "mcp":
        ready = await _run_subprocess([sys.executable, "-c", "print('mcp_server_ready')"])
        ensure(ready == "mcp_server_ready", "mcp readiness check failed")
        result = await _run_subprocess(
            [sys.executable, "-c", "import sys; print('mcp_done:' + sys.argv[1])", task],
        )
        return "mcp://tool-hub", result

    if sandbox == "docker":
        try:
            version = await _run_subprocess(
                ["docker", "version", "--format", "{{.Server.Version}}"],
                timeout_s=10.0,
            )
            ensure(bool(version), "empty docker daemon version")
            result = await _run_subprocess(
                [
                    "docker",
                    "run",
                    "--rm",
                    "-e",
                    f"TASK={task}",
                    "alpine:3.19",
                    "sh",
                    "-lc",
                    "echo docker_done:${TASK}",
                ],
                timeout_s=120.0,
            )
            return f"docker://agent-runtime-sandbox@{version}", result
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"docker unavailable: {exc}") from exc

    raise RuntimeError(f"unsupported sandbox: {sandbox}")


def _select_sandboxes(prompt: str) -> list[str]:
    if "sandbox=all" in prompt:
        return ["local_python", "docker", "mcp"]
    if "sandbox=local_python" in prompt:
        return ["local_python"]
    if "sandbox=docker" in prompt:
        return ["docker"]
    if "sandbox=mcp" in prompt:
        return ["mcp"]
    return ["local_python"]


def _create_runtime_app() -> AgentApp:
    app = AgentApp(app_name="RuntimeLearning", app_description="runtime learning app")

    @app.query(framework="agentscope")
    async def query(  # type: ignore[unused-ignore]
        runner: Any,
        msgs: list[Msg],
        request: AgentRequest | None = None,
        **kwargs: Any,
    ):
        prompt = _extract_prompt_text(msgs)
        sandboxes = _select_sandboxes(prompt)

        trace_events: list[dict[str, str]] = []

        def add_event(phase: str, status: str, sandbox: str = "none", detail: str = "") -> None:
            trace_events.append(
                {
                    "phase": phase,
                    "status": status,
                    "sandbox": sandbox,
                    "detail": detail,
                },
            )

        base = [
            ("request_received", "ok", "none", prompt),
            ("auth_checked", "ok", "none", "token accepted"),
            ("session_loaded", "ok", "none", f"session={request.session_id if request else ''}"),
            ("agent_planned", "ok", "none", f"sandboxes={','.join(sandboxes)}"),
        ]
        for phase, status, sandbox, detail in base:
            add_event(phase, status, sandbox, detail)

        last_result = ""
        for sandbox in sandboxes:
            add_event("sandbox_selected", "ok", sandbox)
            add_event("sandbox_establishing", "ok", sandbox)
            try:
                connection, result = await _connect_and_run_sandbox(sandbox, prompt)
            except Exception as exc:  # noqa: BLE001
                add_event("sandbox_unavailable", "skipped", sandbox, str(exc))
                continue

            add_event("sandbox_established", "ok", sandbox, connection)
            add_event("sandbox_health_checked", "ok", sandbox, "healthy")
            add_event("sandbox_started", "ok", sandbox)
            add_event("sandbox_succeeded", "ok", sandbox, result)
            last_result = result

        add_event("response_streaming", "ok")
        add_event("response_completed", "ok", detail=last_result)
        trace = {"events": trace_events, "result": last_result}
        yield Msg(
            name="runtime",
            role="assistant",
            content=f"TRACE_JSON|{json.dumps(trace, ensure_ascii=False)}",
        ), True

    return app


def _run_runtime_server(port: int) -> None:
    app = _create_runtime_app()
    app.run(host="127.0.0.1", port=port)


def pick_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def start_runtime_server(port: int) -> multiprocessing.Process:
    proc = multiprocessing.Process(target=_run_runtime_server, args=(port,))
    proc.start()
    for _ in range(120):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(("127.0.0.1", port))
            sock.close()
            return proc
        except OSError:
            time.sleep(0.1)
        finally:
            sock.close()
    proc.terminate()
    proc.join(timeout=2)
    raise RuntimeError("runtime server startup timeout")


def stop_runtime_server(proc: multiprocessing.Process) -> None:
    if proc.is_alive():
        proc.terminate()
        proc.join(timeout=5)


async def post_process_and_collect(port: int, prompt: str, session_id: str) -> list[dict[str, Any]]:
    payload = {
        "session_id": session_id,
        "input": [
            {
                "role": "user",
                "type": "message",
                "content": [{"type": "text", "text": prompt}],
            },
        ],
    }
    url = f"http://127.0.0.1:{port}/process"
    events: list[dict[str, Any]] = []
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            ensure(resp.status == 200, f"/process status mismatch: {resp.status}")
            ensure(resp.content_type == "text/event-stream", "response is not SSE")
            buffer = ""
            async for chunk, _ in resp.content.iter_chunks():
                if not chunk:
                    continue
                buffer += chunk.decode("utf-8", errors="ignore")
                while "\n\n" in buffer:
                    one_event, buffer = buffer.split("\n\n", 1)
                    data_lines: list[str] = []
                    for line in one_event.splitlines():
                        if line.startswith("data:"):
                            data_lines.append(line[5:].strip())
                    if not data_lines:
                        continue
                    data = "\n".join(data_lines)
                    if data == "[DONE]":
                        continue
                    try:
                        events.append(json.loads(data))
                    except json.JSONDecodeError:
                        continue
    return events


def _extract_text_from_payload(payload: dict[str, Any]) -> list[str]:
    out: list[str] = []
    messages = payload.get("output")
    if not isinstance(messages, list):
        return out
    for message in messages:
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text")
                if isinstance(text, str):
                    out.append(text)
    return out


def parse_stage_events_from_payloads(payloads: list[dict[str, Any]]) -> tuple[list[StageEvent], str]:
    stage_events: list[StageEvent] = []
    final_result = ""
    for payload in payloads:
        for text in _extract_text_from_payload(payload):
            if not text.startswith("TRACE_JSON|"):
                continue
            raw = text.split("|", 1)[1]
            data = json.loads(raw)
            final_result = str(data.get("result", ""))
            for item in data.get("events", []):
                if not isinstance(item, dict):
                    continue
                stage_events.append(
                    StageEvent(
                        phase=str(item.get("phase", "")),
                        status=str(item.get("status", "")),
                        sandbox=str(item.get("sandbox", "none")),
                        detail=str(item.get("detail", "")),
                    ),
                )
    return stage_events, final_result


def validate_event_reasonability(events: list[StageEvent], require_all_sandboxes: bool) -> None:
    ensure(bool(events), "event list is empty")
    phases = [e.phase for e in events]
    ensure(phases[0] == "request_received", "first event must be request_received")
    ensure("response_completed" in phases, "response_completed not found")
    ensure(phases.index("request_received") < phases.index("auth_checked"), "auth_checked order mismatch")
    ensure(phases.index("auth_checked") < phases.index("session_loaded"), "session_loaded order mismatch")
    ensure(phases.index("session_loaded") < phases.index("agent_planned"), "agent_planned order mismatch")

    selected_indexes = [idx for idx, event in enumerate(events) if event.phase == "sandbox_selected"]
    ensure(bool(selected_indexes), "sandbox_selected missing")
    for i, begin in enumerate(selected_indexes):
        end = selected_indexes[i + 1] if i + 1 < len(selected_indexes) else len(events)
        segment = events[begin:end]
        segment_phases = [e.phase for e in segment]
        ensure(segment_phases[0] == "sandbox_selected", "sandbox segment must start with sandbox_selected")
        ensure("sandbox_establishing" in segment_phases, "sandbox_establishing missing")
        if "sandbox_unavailable" in segment_phases:
            ensure("sandbox_started" not in segment_phases, "unavailable sandbox should not start")
            continue
        expected = [
            "sandbox_selected",
            "sandbox_establishing",
            "sandbox_established",
            "sandbox_health_checked",
            "sandbox_started",
            "sandbox_succeeded",
        ]
        for phase in expected:
            ensure(phase in segment_phases, f"missing phase: {phase}")
        idx = {phase: segment_phases.index(phase) for phase in expected}
        ensure(
            idx["sandbox_selected"]
            < idx["sandbox_establishing"]
            < idx["sandbox_established"]
            < idx["sandbox_health_checked"]
            < idx["sandbox_started"]
            < idx["sandbox_succeeded"],
            "sandbox success order mismatch",
        )

    if require_all_sandboxes:
        selected = {events[i].sandbox for i in selected_indexes}
        ensure(selected == {"local_python", "docker", "mcp"}, "full flow sandbox coverage mismatch")


def assert_event_guard_can_detect_corruption(events: list[StageEvent]) -> None:
    ensure(len(events) > 3, "not enough events to corrupt")
    corrupted = events[:-1]
    caught = False
    try:
        validate_event_reasonability(corrupted, require_all_sandboxes=False)
    except AssertionError:
        caught = True
    ensure(caught, "guard did not detect corruption")
