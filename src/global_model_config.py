import os
from pathlib import Path


def _load_dotenv() -> None:
    """Load key=value pairs from project .env if present."""
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        # Do not override already exported environment variables.
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

# Global defaults for Doubao (OpenAI-compatible mode).
MODEL_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
MODEL_NAME = os.getenv("OPENAI_MODEL", "doubao-seed-1-6-251015")
MODEL_API_KEY = os.getenv("OPENAI_API_KEY", "")
DOUBAO_DISABLE_THINKING = os.getenv("DOUBAO_DISABLE_THINKING", "true").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}


def require_model_api_key() -> str:
    if (
        not MODEL_API_KEY
        or MODEL_API_KEY.lower() in {"your_doubao_api_key", "your_api_key", "replace_me"}
    ):
        print("FAIL: OPENAI_API_KEY is not set.")
        print("Hint: set env var first, then rerun:")
        print('PowerShell: $env:OPENAI_API_KEY="your_doubao_api_key"')
        print('Or update ".env": OPENAI_API_KEY=your_doubao_api_key')
        raise SystemExit(1)
    return MODEL_API_KEY


def get_default_model_config(config_name: str = "default_model") -> dict:
    return {
        "config_name": config_name,
        "model_type": "openai_chat",
        "model_name": MODEL_NAME,
        "api_key": require_model_api_key(),
        "base_url": MODEL_BASE_URL,
    }


def _is_doubao_model(model_name: str) -> bool:
    lower_name = model_name.lower()
    return "doubao" in lower_name or "seed" in lower_name


def get_openai_chat_model_kwargs(model_name: str | None = None) -> dict:
    name = model_name or MODEL_NAME
    kwargs = {
        "model_name": name,
        "api_key": require_model_api_key(),
        "client_kwargs": {"base_url": MODEL_BASE_URL},
    }
    if _is_doubao_model(name) and DOUBAO_DISABLE_THINKING:
        # Doubao OpenAI-compatible option: disable model thinking output.
        kwargs["generate_kwargs"] = {"thinking": {"type": "disabled"}}
    return kwargs
