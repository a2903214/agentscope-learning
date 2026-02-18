import importlib
import os
import platform
import sys
from importlib import metadata
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402


def check_python() -> bool:
    ok = True
    print(f"Python executable: {sys.executable}")
    print(f"Python version   : {platform.python_version()}")
    if sys.version_info < (3, 10):
        print("ERROR: AgentScope requires Python >= 3.10.")
        ok = False
    return ok


def check_agentscope() -> bool:
    try:
        ensure_local_agentscope()
        importlib.import_module("agentscope")
        print("OK   : import agentscope")
    except Exception as exc:  # pragma: no cover - environment dependent
        print(f"ERROR: cannot import agentscope: {exc}")
        print("Hint : run `pip install -U agentscope` in the active environment.")
        return False

    try:
        version = metadata.version("agentscope")
    except Exception:
        version = "unknown"
    print(f"AgentScope version: {version}")

    smoke_imports = [
        "agentscope.agent",
        "agentscope.message",
        "agentscope.pipeline",
        "agentscope.tool",
    ]
    ok = True
    for module_name in smoke_imports:
        try:
            importlib.import_module(module_name)
            print(f"OK   : import {module_name}")
        except Exception as exc:  # pragma: no cover - environment dependent
            print(f"ERROR: cannot import {module_name}: {exc}")
            ok = False
    return ok


def check_model_env() -> None:
    keys = [
        "OPENAI_API_KEY",
        "DASHSCOPE_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
    ]
    present = [k for k in keys if os.getenv(k)]
    if present:
        print("Model API keys found:", ", ".join(present))
    else:
        print("WARN : no model API key found in environment.")


def main() -> None:
    print("=== Environment Validation ===")
    python_ok = check_python()
    agentscope_ok = check_agentscope()
    check_model_env()

    if python_ok and agentscope_ok:
        print("PASS : AgentScope environment is ready.")
        raise SystemExit(0)

    print("FAIL : Environment is not ready. See errors above.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
