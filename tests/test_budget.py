#!/usr/bin/env python3
"""The byte-budget fence — the delivery-separability guard (INV-30).

The input-modality axis ships inside the single assembled bundle the build already produces: every
visitor loads every pole's code (finger, pointer, keyboard) whatever their platform. That monolithic
delivery is the chosen one — a split by platform or a per-pole lazy load would cost real complexity
against the one-page architecture for a slim saving. The SPEC says a byte-budget watcher guards the
choice: it reds once the bundle grows past its fence, and only then does a platform-split or lazy-load
delivery earn its build. This suite IS that watcher — it measures the SHIPPED bundle and reds on bloat.

What it measures: the gzip size (level 6 — plain `gzip -c`, deterministic mtime) of the engine's
assembled `exhibition.js` and `exhibition.css` AS SHIPPED. The site bakes the JS verbatim, so the JS
is measured raw; it comment-strips the CSS at bake (build.py: strip_css_comments — the visitor gets
rules, not prose), so the CSS is measured through that same stripper. Measuring the engine's own
assets, treated exactly as the bake treats them, guards both repos' delivery.

The fence is infrastructure rather than red-first behaviour: it is GREEN while the bundle stays under
the fence and reds only when a future change balloons it past the headroom. The fence is set at the
current measured size plus ~10-15% headroom, rounded up — enough that ordinary growth does not flake it,
tight enough that a real jump (a whole new feature's worth of code, a heavy dependency) trips it and
sends the delivery question back to the SPEC's non-goal.

Measured 2026-07-21: JS gzip ≈ 92_967 B (raw). CSS as-shipped 2026-07-23: gzip ≈ 7_415 B
(comment-stripped; the commented source is ≈ 18_801 B — comments were ~60% of the served weight).

Run: python tests/test_budget.py   (exit 0 = under fence)
"""
import gzip
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The source of truth is the engine's assembled bundle. In the engine repo it sits under
# ROOT/engine/assets; in the site repo it lives in the sibling engine checkout. Resolve either.
_CANDIDATES = [ROOT / "engine" / "assets", Path.home() / "exhibition-engine" / "engine" / "assets"]
ASSETS = next((c for c in _CANDIDATES if (c / "exhibition.js").exists()), _CANDIDATES[0])

# The served CSS is comment-stripped at bake (build.py: strip_css_comments) — the visitor downloads
# rules, not prose. The fence must measure THAT shipped artifact, so it borrows the very same stripper
# the build uses (one home for the transform, no drift). The site bakes the JS verbatim, so the JS is
# measured raw. build.py sits one level up from the engine's assets dir.
def _load_strip():
    spec = importlib.util.spec_from_file_location("_engine_build", ASSETS.parent / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.strip_css_comments


strip_css_comments = _load_strip()

# fence value + one-line reason, per asset. current × ~1.1–1.15, rounded to a round number above it.
# The transform is the exact bake-time treatment of the served asset (None = shipped verbatim).
FENCES = {
    "exhibition.js": (105_000, "monolithic all-pole bundle; ~13% over the 2026-07-21 gzip of ~92_967 B", None),
    "exhibition.css": (9_000, "single served stylesheet, comment-stripped as shipped; ~21% over the 2026-07-23 gzip of ~7_415 B", strip_css_comments),
}

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def gz(path, transform=None):
    """gzip size at level 6 (plain `gzip -c`), mtime zeroed so the count is deterministic. `transform`
    (when given) is the bake-time text treatment, so the fence measures the SHIPPED bytes, not source."""
    data = path.read_bytes()
    if transform is not None:
        data = transform(data.decode("utf-8")).encode("utf-8")
    return len(gzip.compress(data, compresslevel=6, mtime=0))


for fname, (fence, reason, transform) in FENCES.items():
    p = ASSETS / fname
    if not p.exists():
        check(f"BUDGET {fname}: asset present to measure", False, f"missing at {p}")
        continue
    size = gz(p, transform)
    check(f"BUDGET {fname}: gzip {size} B under the {fence} B fence ({reason})",
          size <= fence,
          f"gzip={size} B  fence={fence} B  ({'under' if size <= fence else 'OVER — bundle ballooned'})")

fails = [r for r in results if r[1] == "FAIL"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails)} pass, {len(fails)} fail")
sys.exit(1 if fails else 0)
