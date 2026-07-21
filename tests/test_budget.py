#!/usr/bin/env python3
"""The byte-budget fence — the delivery-separability guard (INV-30).

The input-modality axis ships inside the single assembled bundle the build already produces: every
visitor loads every pole's code (finger, pointer, keyboard) whatever their platform. That monolithic
delivery is the chosen one — a split by platform or a per-pole lazy load would cost real complexity
against the one-page architecture for a slim saving. The SPEC says a byte-budget watcher guards the
choice: it reds once the bundle grows past its fence, and only then does a platform-split or lazy-load
delivery earn its build. This suite IS that watcher — it measures the SHIPPED bundle and reds on bloat.

What it measures: the gzip size (level 6 — plain `gzip -c`, deterministic mtime) of the engine's
assembled `exhibition.js` (the source of truth the assembler writes) and `exhibition.css`. The site
bakes these verbatim, so measuring the engine's own assets guards both repos' delivery.

The fence is infrastructure rather than red-first behaviour: it is GREEN while the bundle stays under
the fence and reds only when a future change balloons it past the headroom. The fence is set at the
current measured size plus ~10-15% headroom, rounded up — enough that ordinary growth does not flake it,
tight enough that a real jump (a whole new feature's worth of code, a heavy dependency) trips it and
sends the delivery question back to the SPEC's non-goal.

Measured 2026-07-21: JS gzip ≈ 92_967 B, CSS gzip ≈ 16_358 B (level 6, mtime=0).

Run: python tests/test_budget.py   (exit 0 = under fence)
"""
import gzip
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The source of truth is the engine's assembled bundle. In the engine repo it sits under
# ROOT/engine/assets; in the site repo it lives in the sibling engine checkout. Resolve either.
_CANDIDATES = [ROOT / "engine" / "assets", Path.home() / "exhibition-engine" / "engine" / "assets"]
ASSETS = next((c for c in _CANDIDATES if (c / "exhibition.js").exists()), _CANDIDATES[0])

# fence value + one-line reason, per asset. current × ~1.1–1.15, rounded to a round number above it.
FENCES = {
    "exhibition.js": (105_000, "monolithic all-pole bundle; ~13% over the 2026-07-21 gzip of ~92_967 B"),
    "exhibition.css": (19_000, "single served stylesheet; ~16% over the 2026-07-21 gzip of ~16_358 B"),
}

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def gz(path):
    """gzip size at level 6 (plain `gzip -c`), mtime zeroed so the count is deterministic."""
    return len(gzip.compress(path.read_bytes(), compresslevel=6, mtime=0))


for fname, (fence, reason) in FENCES.items():
    p = ASSETS / fname
    if not p.exists():
        check(f"BUDGET {fname}: asset present to measure", False, f"missing at {p}")
        continue
    size = gz(p)
    check(f"BUDGET {fname}: gzip {size} B under the {fence} B fence ({reason})",
          size <= fence,
          f"gzip={size} B  fence={fence} B  ({'under' if size <= fence else 'OVER — bundle ballooned'})")

fails = [r for r in results if r[1] == "FAIL"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails)} pass, {len(fails)} fail")
sys.exit(1 if fails else 0)
