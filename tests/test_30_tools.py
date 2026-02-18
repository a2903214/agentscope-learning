"""30-tools: tool cases (sync/async/stream/MCP/Skill etc)."""
import subprocess
import sys

from conftest import SRC, SUBPROCESS_ENV


def test_30_tools_all() -> None:
    """Run 30-tools/main.py (all tool cases)."""
    r = subprocess.run(
        [sys.executable, "30-tools/main.py"],
        cwd=SRC,
        capture_output=False,
        timeout=300,
        env=SUBPROCESS_ENV,
    )
    assert r.returncode == 0, "subprocess failed, see console output above"
