#!/usr/bin/env python3
"""What a visitor's browser downloads, watched as two totals — one per shipped surface.

WHY A PERSON CARES. Everything below is code that must arrive over a phone's connection before the
exhibition can be walked. When it doubles, the walk starts late on a slow connection and some
visitors leave before they see a photograph. That is the only thing this suite is here to catch.

THE TWO SURFACES.
  · The ordinary site — what every visitor pulls, whatever their device and whatever they do: the
    walk's own bundle and its one stylesheet.
  · The immersive route — the above plus everything the drawing road can ask for: the drawing host,
    the passage composer, and every instrument that ships. A single crossing fetches only the
    instruments its own score names, so this total is the worst case a long walk approaches, not
    what one crossing costs.

THE NUMBERS AND THE ROOM THEY LEAVE. Each fence is the measurement of 2026-08-18 times about one and
a half, rounded to a round number. That is deliberate slack: this watch exists to catch a doubling,
not a kilobyte, and a fence that reddens on ordinary growth teaches nobody anything and costs a
round trip to re-set. When one of these does redden, the answer is not a bigger number — it is to
ask what arrived and whether the visitor should be paying for it on the wire at all.

Measured 2026-08-18, gzip level 6 over the bytes the bake actually ships (both assets are
comment-stripped on the way out, so each is measured through the build's own stripper):
  ordinary site   82 474 B   → fence 125 000 B
  immersive route 177 321 B  → fence 270 000 B

Run: python tests/test_budget.py   (exit 0 = under both fences)
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
# The watch must measure THOSE shipped artifacts, so it borrows the very strippers the build uses
# (one home for each transform, no drift). build.py sits one level up from the engine's assets dir.
def _load_strip():
    spec = importlib.util.spec_from_file_location("_engine_build", ASSETS.parent / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.strip_css_comments, mod.strip_js_comments


strip_css_comments, strip_js_comments = _load_strip()

# The instruments are found rather than listed, so an instrument landing or leaving needs no edit
# here — it simply shows up in the immersive total, which is the number that answers for it.
ORDINARY = ["exhibition.js", "exhibition.css"]
IMMERSIVE_EXTRA = (["pass-layer.js", "pass-composer.js"]
                   + sorted(p.name for p in ASSETS.glob("pass-inst-*.js")))

SURFACES = [
    ("the ordinary site", 125_000, ORDINARY,
     "the walk's own bundle and its stylesheet — what every visitor downloads before anything happens"),
    ("the immersive route", 270_000, ORDINARY + IMMERSIVE_EXTRA,
     "the above plus the drawing host, the passage composer and every instrument that ships — the "
     "worst case a long walk on the drawing road approaches"),
]

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def gz(path):
    """gzip size at level 6 (plain `gzip -c`), mtime zeroed so the count is deterministic, over the
    bytes the bake ships — comment-stripped by the build's own stripper for the kind of file."""
    text = path.read_text(encoding="utf-8")
    strip = strip_css_comments if path.suffix == ".css" else strip_js_comments
    return len(gzip.compress(strip(text).encode("utf-8"), compresslevel=6, mtime=0))


for label, fence, files, why in SURFACES:
    missing = [f for f in files if not (ASSETS / f).exists()]
    if missing:
        check(f"BUDGET {label}: every file of the surface is present to measure", False,
              f"missing under {ASSETS}: {', '.join(missing)}")
        continue
    parts = {f: gz(ASSETS / f) for f in files}
    total = sum(parts.values())
    check(f"BUDGET {label}: {total} B gzipped over the wire, under the {fence} B fence ({why})",
          total <= fence,
          "  ".join(f"{f}={s}" for f, s in parts.items())
          + f"  TOTAL={total} B  fence={fence} B  "
          + ("under" if total <= fence else "OVER — this surface has ballooned"))

# EX-STORY-FILL ratchet: SPEC.md states a browser's story requests stay under the edge's
# per-address hourly ceiling — "two walks in one hour are 18, and five one-work asks at three
# rungs are 15, reaching 33 against the per-address ceiling of 40." This is NOT a size fence and
# not a snapshot of a typed number: every figure is read OUT OF THE SOURCE, and the row reds only
# when the relation between them breaks — a knob raised past the ceiling means real visitors are
# rate-limited mid-walk and lose the told story, which is what a person meets.
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
