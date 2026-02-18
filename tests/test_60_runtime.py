"""60-runtime: runtime cases."""
import subprocess
import sys

from conftest import SRC


def test_60_runtime_all() -> None:
    """Run 60-runtime/main.py (all runtime cases)."""
    r = subprocess.run(
        [sys.executable, "60-runtime/main.py"],
        cwd=SRC,
        capture_output=False,
        timeout=300,
    )
    assert r.returncode == 0, "subprocess failed, see console output above"
