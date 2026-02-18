"""00-environment: env and dependency check."""
import subprocess
import sys

from conftest import SRC


def test_00_environment() -> None:
    """Run 00-environment/main.py (Python, AgentScope, model env)."""
    r = subprocess.run(
        [sys.executable, "00-environment/main.py"],
        cwd=SRC,
        capture_output=False,
        timeout=60,
    )
    assert r.returncode == 0, "subprocess failed, see console output above"
