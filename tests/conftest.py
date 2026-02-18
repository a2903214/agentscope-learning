"""
Root conftest: resolve ROOT and SRC for test_*.py.
"""
import os
import sys
from pathlib import Path

# ROOT = agentscope-learning (parent of tests/)
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# Unbuffered stdout/stderr so subprocess logs show during pytest (no TTY)
SUBPROCESS_ENV = {**os.environ, "PYTHONUNBUFFERED": "1"}

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
