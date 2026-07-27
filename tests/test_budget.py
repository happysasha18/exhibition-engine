#!/usr/bin/env python3
"""The byte-budget fence — the delivery-separability guard (INV-30).

The input-modality axis ships inside the single assembled bundle the build already produces: every
visitor loads every pole's code (finger, pointer, keyboard) whatever their platform. That monolithic
delivery is the chosen one — a split by platform or a per-pole lazy load would cost real complexity
against the one-page architecture for a slim saving. The SPEC says a byte-budget watcher guards the
choice: it reds once the bundle grows past its fence, and only then does a platform-split or lazy-load
delivery earn its build. This suite IS that watcher — it measures the SHIPPED bundle and reds on bloat.

What it measures: the gzip size (level 6 — plain `gzip -c`, deterministic mtime) of the engine's
assembled `exhibition.js` and `exhibition.css` AS SHIPPED. The bake comment-strips BOTH on the way
out (build.py: strip_js_comments / strip_css_comments — the visitor gets code and rules, not prose),
so each is measured through its own stripper. Measuring the engine's own assets, treated exactly as
the bake treats them, guards both repos' delivery.

The fence is infrastructure rather than red-first behaviour: it is GREEN while the bundle stays under
the fence and reds only when a future change balloons it past the headroom. The fence is set at the
current measured size plus ~10-15% headroom, rounded up — enough that ordinary growth does not flake it,
tight enough that a real jump (a whole new feature's worth of code, a heavy dependency) trips it and
sends the delivery question back to the SPEC's non-goal.

Measured 2026-07-21: JS gzip ≈ 92_967 B (raw). CSS as-shipped 2026-07-23: gzip ≈ 7_415 B
(comment-stripped; the commented source is ≈ 18_801 B — comments were ~60% of the served weight).
JS as-shipped 2026-07-27: gzip ≈ 57_311 B (comment-stripped; the commented source is ≈ 104_495 B —
line-opening comments were ~45% of the served weight). The raw fence had 50 B of headroom left when
the strip landed, which is what sent the same lever the stylesheet already rides over to the script.

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

# Both served assets are comment-stripped at bake — the visitor downloads code and rules, not prose.
# The fence must measure THOSE shipped artifacts, so it borrows the very strippers the build uses (one
# home for each transform, no drift). build.py sits one level up from the engine's assets dir.
def _load_strip():
    spec = importlib.util.spec_from_file_location("_engine_build", ASSETS.parent / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.strip_css_comments, mod.strip_js_comments


strip_css_comments, strip_js_comments = _load_strip()

# fence value + one-line reason, per asset. current × ~1.1–1.15, rounded to a round number above it.
# The transform is the exact bake-time treatment of the served asset (None = shipped verbatim).
FENCES = {
    "exhibition.js": (65_000, "monolithic all-pole bundle, comment-stripped as shipped; ~13% over the 2026-07-27 gzip of ~57_311 B", strip_js_comments),
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
