"""40-memory: memory cases."""
import subprocess
import sys

from conftest import SRC


def test_40_memory_all() -> None:
    """Run 40-memory/main.py (all memory cases)."""
    r = subprocess.run(
        [sys.executable, "40-memory/main.py"],
        cwd=SRC,
        capture_output=False,
        timeout=300,
    )
    assert r.returncode == 0, "subprocess failed, see console output above"
