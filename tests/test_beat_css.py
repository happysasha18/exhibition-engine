#!/usr/bin/env python3
"""EX-STORY-BEAT (INV-89) + EX-CAPTION (INV-98) — the polish clauses' CSS rule families must ship in
the SERVED css. String-level presence rows, the same level as test_sound.py's CSS rows (regex/substring
on the baked CSS text), against the ENGINE's own exhibition.css.

The client JS builds a `.exd-beat` clone for the door-pick crossing (the picked picture pulses at the
black's centre while the story's first portion loads — EX-STORY-BEAT/INV-89). If the served CSS is
missing the `.exd-beat` rule family the crossing ships an unstyled clone: no position:fixed, no
sizing, no breathing pulse, no reduced-motion hide. The caption block wraps balanced (text-wrap:balance)
and steps its type down under a narrow breakpoint (EX-CAPTION/INV-98); those rules must ship too.

This suite bakes the real served CSS (exactly as the bake emits it — the engine copies
engine/assets/exhibition.css verbatim) and asserts each rule family by string presence.

Run:            .venv/bin/python tests/test_beat_css.py
Red proof:      .venv/bin/python tests/test_beat_css.py --selftest
                (strips each asserted rule from the baked CSS and proves every new row reds — the
                assertions are load-bearing, not vacuously green.)
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402

SITE_URL = "https://synth.example.com"
SELFTEST = "--selftest" in sys.argv
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


# ---------------------------------------------------------------- bake once (the engine copies its
# own assets/exhibition.css verbatim into the bundle, so the served CSS IS the engine's CSS).
TMP = Path(tempfile.mkdtemp(prefix="synth_beat_css_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

CSS = (TMP / "exhibition.css").read_text(encoding="utf-8")

# --selftest strips every rule these rows assert, so a load-bearing row MUST flip to FAIL. The
# mutation removes each targeted block/declaration; the checks below then run against the wreck.
if SELFTEST:
    CSS = re.sub(r"\.exd-beat[^\n]*\{[^}]*\}", "", CSS)          # the whole .exd-beat family
    CSS = re.sub(r"@keyframes\s+exd-breath\s*\{[^}]*\}", "", CSS)  # the breath keyframes
    CSS = CSS.replace("text-wrap:balance", "text-wrap:normal")    # the balanced wrap
    CSS = CSS.replace("--cap-narrow-scale", "--cap-dead-scale")   # the narrow type-step
    CSS = re.sub(r"@media\s*\(prefers-reduced-motion[^{]*\{\s*\.exd-beat\s*\{[^}]*\}", "", CSS)


# ===== EX-STORY-BEAT (INV-89): the crossing clone's CSS family =====

# 1 — .exd-beat: the crossing clone's wrapper is position:fixed (never an unstyled clone flying loose)
m_beat = re.search(r"\.exd-beat\s*\{([^}]*)\}", CSS, re.S)
beat_body = m_beat.group(1) if m_beat else ""
check("EX-STORY-BEAT .exd-beat carries position:fixed (the wrapper's flight anchor)",
      bool(m_beat) and bool(re.search(r"position\s*:\s*fixed", beat_body)),
      f"found={bool(m_beat)} body={beat_body!r}")

# 2 — .exd-beat img: width:100% (the inner picture fills the clone, never an intrinsic-size blob)
m_img = re.search(r"\.exd-beat\s+img\s*\{([^}]*)\}", CSS, re.S)
img_body = m_img.group(1) if m_img else ""
check("EX-STORY-BEAT .exd-beat img carries width:100% (fills the clone's sizing)",
      bool(m_img) and bool(re.search(r"width\s*:\s*100%", img_body)),
      f"found={bool(m_img)} body={img_body!r}")

# 3 — .exd-beat.breathe img: the exd-breath animation (the slow pulse while the story writes)
m_breathe = re.search(r"\.exd-beat\.breathe\s+img\s*\{([^}]*)\}", CSS, re.S)
breathe_body = m_breathe.group(1) if m_breathe else ""
check("EX-STORY-BEAT .exd-beat.breathe img carries the exd-breath animation",
      bool(m_breathe) and "exd-breath" in breathe_body,
      f"found={bool(m_breathe)} body={breathe_body!r}")

# 4 — @keyframes exd-breath: the breath keyframes themselves are present
check("EX-STORY-BEAT @keyframes exd-breath is present",
      bool(re.search(r"@keyframes\s+exd-breath\s*\{", CSS)))

# 5 — reduced motion hides the beat entirely (the JS never builds it under reduced motion; this rule
# is the belt — INV-89's own words)
m_rm = re.search(
    r"@media\s*\(prefers-reduced-motion\s*:\s*reduce\)\s*\{\s*\.exd-beat\s*\{([^}]*)\}",
    CSS, re.S)
rm_body = m_rm.group(1) if m_rm else ""
check("EX-STORY-BEAT reduced-motion hides .exd-beat (display:none)",
      bool(m_rm) and bool(re.search(r"display\s*:\s*none", rm_body)),
      f"found={bool(m_rm)} body={rm_body!r}")


# ===== EX-CAPTION (INV-98): the caption wraps balanced + steps down on a narrow screen =====

# 6 — text-wrap:balance rides the caption's reader-facing prose (title/told/prompt) so a wrapping
# line breaks into near-equal lines rather than a long line trailed by a short orphan (INV-98)
m_bal = re.search(r"([^\n{}]*)\{[^}]*text-wrap\s*:\s*balance", CSS)
bal_sel = m_bal.group(1) if m_bal else ""
check("EX-CAPTION text-wrap:balance rides the caption prose (INV-98)",
      bool(m_bal) and ".exh-capzone" in bal_sel,
      f"selector={bal_sel.strip()!r}")

# 7 — the narrow-screen type-step: below the narrow breakpoint a configurable step scales the block
# down so the balanced text clears the picture (INV-98; the owner knob --cap-narrow-step drives it)
check("EX-CAPTION narrow-screen type-step present (--cap-narrow-scale from --cap-narrow-step)",
      bool(re.search(r"--cap-narrow-scale\s*:\s*calc\([^)]*--cap-narrow-step", CSS)))


fails = [r for r in results if r[1] == "FAIL"]
shutil.rmtree(TMP, ignore_errors=True)

for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))

if SELFTEST:
    # the red proof inverts: with every asserted rule stripped, EVERY row must have failed. A row
    # still green under the mutation is not load-bearing and the proof itself reds.
    non_fail = [r for r in results if r[1] != "FAIL"]
    print(f"\n--selftest: {len(fails)}/{len(results)} rows red under the stripped CSS")
    if non_fail:
        print("  NOT load-bearing (still green with its rule stripped): "
              + ", ".join(r[0] for r in non_fail))
    sys.exit(0 if not non_fail else 1)

print(f"\n{len(results)} rows: {len(results) - len(fails)} pass, {len(fails)} fail")
sys.exit(1 if fails else 0)
