"""20-models: multi-model config comparison."""
import subprocess
import sys

from conftest import SRC, SUBPROCESS_ENV


def test_20_models() -> None:
    """Run 20-models/main.py."""
    r = subprocess.run(
        [sys.executable, "20-models/main.py"],
        cwd=SRC,
        capture_output=False,
        timeout=120,
        env=SUBPROCESS_ENV,
    )
    assert r.returncode == 0, "subprocess failed, see console output above"
