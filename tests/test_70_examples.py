"""70-examples: stock hot-topic analysis (default args)."""
import subprocess
import sys

from conftest import SRC, SUBPROCESS_ENV


def test_70_examples_default_args() -> None:
    """Run 70-examples/main.py with defaults: --topic AI算力 --horizon 中期 --risk 中等."""
    r = subprocess.run(
        [
            sys.executable,
            "70-examples/main.py",
            "--topic", "AI算力",
            "--horizon", "中期",
            "--risk", "中等",
        ],
        cwd=SRC,
        capture_output=False,
        timeout=600,
        env=SUBPROCESS_ENV,
    )
    assert r.returncode == 0, "subprocess failed, see console output above"
