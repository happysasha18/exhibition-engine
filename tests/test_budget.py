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

Moved 2026-08-13, with its reason, because the fence did its job. The transition seam (EX-PASS) took
the bundle from ≈60_100 B to ≈65_334 B and tripped the 65_000 B fence. The delivery question the
fence exists to raise was ANSWERED rather than waved through: the drawing layer now ships as its own
file, `pass-layer.js`, fetched by the client only when the visualLayer setting asks for it, the
device reports WebGL2, and the visit runs neither reduced motion nor Save-Data. What stays in the
bundle is the CONTRACT — the settings register, the one transition command, the landing owner and the
door that decides whether to fetch anything at all — which cannot live outside it, since it is what
makes the decision. So the JS fence tracks the new baseline at 67_000 B (about 2.5% headroom,
deliberately tight), and the separately delivered file gets a fence of its own from day one.

Measured 2026-07-21: JS gzip ≈ 92_967 B (raw). CSS as-shipped 2026-07-23: gzip ≈ 7_415 B
(comment-stripped; the commented source is ≈ 18_801 B — comments were ~60% of the served weight).
JS as-shipped 2026-07-27: gzip ≈ 57_311 B (comment-stripped; the commented source is ≈ 104_495 B —
line-opening comments were ~45% of the served weight). The raw fence had 50 B of headroom left when
the strip landed, which is what sent the same lever the stylesheet already rides over to the script.

Run: python tests/test_budget.py   (exit 0 = under fence)
"""
import gzip
import importlib.util
import re
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
    "exhibition.js": (67_000, "the walk's own bundle: contract and chrome, comment-stripped as shipped; the picture travels separately (pass-layer.js) since 2026-08-13", strip_js_comments),
    "exhibition.css": (9_000, "single served stylesheet, comment-stripped as shipped; ~21% over the 2026-07-23 gzip of ~7_415 B", strip_css_comments),
    # 2026-08-14: the stub became a host with a frame half and one real instrument (the woven one),
    # measured at 11 628 B gzipped against the 4 000 B a 167 B stub stood behind. This file is
    # fetched ONLY on a visit that actually draws — reduced motion, Save-Data, no WebGL2 and
    # visualLayer:off never ask for it — so its bytes never touch the walk's own bundle above.
    "pass-layer.js": (13_000, "the drawing layer's own file, fetched only when a walk asks for it: the host's frame half plus the woven instrument and its shader", strip_js_comments),
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

# EX-STORY-FILL ratchet: SPEC.md states a browser's story requests stay under the edge's
# per-address hourly ceiling — "two walks in one hour are 18, and five one-work asks at three
# rungs are 15, reaching 33 against the per-address ceiling of 40." Read every number OUT OF
# THE SOURCE (never hardcoded) so a knob raised past the ceiling reds this row rather than
# leaving that sentence false.
WORKER_JS = ASSETS / "worker.js"                              # RL_PER_HOUR (the edge's own fence)
STORY_VOICE_JS = ASSETS.parent / "client" / "09-story-voice.js"  # SOLO_PER_HOUR, STORY_RETRY_MS
BUILD_PY = ASSETS.parent / "build.py"                          # bake's default config: max_unfolds

_rl_m = _solo_m = _retry_m = _maxu_m = None
if WORKER_JS.exists():
    _rl_m = re.search(r"RL_PER_HOUR\s*=\s*(\d+)", WORKER_JS.read_text())
if STORY_VOICE_JS.exists():
    _voice_src = STORY_VOICE_JS.read_text()
    _solo_m = re.search(r"SOLO_PER_HOUR\s*=\s*(\d+)", _voice_src)
    _retry_m = re.search(r"STORY_RETRY_MS\s*=\s*\[([^\]]*)\]", _voice_src)
if BUILD_PY.exists():
    _maxu_m = re.search(r'"max_unfolds":\s*(\d+)', BUILD_PY.read_text())

if not (_rl_m and _solo_m and _retry_m and _maxu_m):
    check("BUDGET EX-STORY-FILL: an hour's story requests stay under the edge's per-address ceiling",
          False,
          f"could not read RL_PER_HOUR({WORKER_JS.exists()}) SOLO_PER_HOUR/STORY_RETRY_MS"
          f"({STORY_VOICE_JS.exists()}) max_unfolds({BUILD_PY.exists()}) — see paths in test source")
else:
    rl_per_hour = int(_rl_m.group(1))
    solo_per_hour = int(_solo_m.group(1))
    rungs = len([x for x in _retry_m.group(1).split(",") if x.strip()]) + 1  # ask + its re-asks
    max_unfolds = int(_maxu_m.group(1))
    total = 2 * (1 + max_unfolds) * rungs + solo_per_hour * rungs
    check(f"BUDGET EX-STORY-FILL: two walks + the hour's solo asks ({total}) stay under "
          f"RL_PER_HOUR ({rl_per_hour})",
          total <= rl_per_hour,
          f"rungs={rungs} (len(STORY_RETRY_MS)+1) max_unfolds={max_unfolds} "
          f"SOLO_PER_HOUR={solo_per_hour} RL_PER_HOUR={rl_per_hour} — "
          f"2*(1+max_unfolds)*rungs + SOLO_PER_HOUR*rungs = {total}")

fails = [r for r in results if r[1] == "FAIL"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails)} pass, {len(fails)} fail")
sys.exit(1 if fails else 0)
