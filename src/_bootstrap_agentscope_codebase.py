import importlib
import sys
from pathlib import Path


def ensure_local_agentscope() -> None:
    """
    Force Python to import agentscope from local codebase source tree:
    s:/agentscope/agentscope-codebase/agentscope/src
    """
    src_root = Path(__file__).resolve().parents[2] / "agentscope-codebase" / "agentscope" / "src"
    src_root_str = str(src_root)
    if src_root_str not in sys.path:
        sys.path.insert(0, src_root_str)

    agentscope = importlib.import_module("agentscope")
    module_path = str(Path(agentscope.__file__).resolve())
    if "agentscope-codebase" not in module_path.replace("\\", "/"):
        raise RuntimeError(
            "agentscope is not loaded from local codebase source. "
            f"Current module path: {module_path}"
        )
