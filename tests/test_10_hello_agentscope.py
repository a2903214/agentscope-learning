"""10-hello-agentscope: Hello AgentScope check."""
import subprocess
import sys

from conftest import SRC


def test_10_hello_agentscope() -> None:
    """Run 10-hello-agentscope/main.py."""
    r = subprocess.run(
        [sys.executable, "10-hello-agentscope/main.py"],
        cwd=SRC,
        capture_output=False,
        timeout=120,
    )
    assert r.returncode == 0, "subprocess failed, see console output above"
