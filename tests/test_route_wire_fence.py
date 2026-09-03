#!/usr/bin/env python3
"""ROUTE-WIRE-FENCE — run_all.py's own suite wrapper for tests/dump_route_wire_fence.py (S-31).

dump_route_wire_fence.py IS the gate already: it drives 6 real crossings on a real dealt route and
prints its own RED lines with `crossing_failures()`'s own reasons, returning 0 only when every
crossing is wire-clean. This file exists only so `run_all.py`'s `SUITES` list (which spawns
`test_<name>.py` for each registered name, gate INV-5r) can name it — S-31's own address: the fence
ran standalone, green or red, and never through the one gate command.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dump_route_wire_fence  # noqa: E402

if __name__ == "__main__":
    rc = dump_route_wire_fence.main()
    print("\n%s" % ("0 failed / 0 skipped" if rc == 0 else "1 failed / 0 skipped"))
    sys.exit(rc)
