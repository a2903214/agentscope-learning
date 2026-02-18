"""50-pipeline: pipeline cases."""
import subprocess
import sys

from conftest import SRC


def test_50_pipeline_all() -> None:
    """Run 50-pipeline/main.py (all pipeline cases)."""
    r = subprocess.run(
        [sys.executable, "50-pipeline/main.py"],
        cwd=SRC,
        capture_output=False,
        timeout=300,
    )
    assert r.returncode == 0, "subprocess failed, see console output above"
