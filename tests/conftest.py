"""
Root conftest: resolve ROOT and SRC for test_*.py.
"""
import sys
from pathlib import Path

# ROOT = agentscope-learning (parent of tests/)
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
