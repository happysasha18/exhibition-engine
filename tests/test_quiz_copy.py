#!/usr/bin/env python3
"""EX-QUIZ-COPY (INV-100): the quiz chip speaks ONE adopted sentence.

The chip names the question it asks and the gift a right answer gives — «where was this shot? ·
win a wallpaper», the owner's own sentence of 2026-07-28. The words ride the ordinary localized
set (`quiz_ask`, EX-I18N) with the English source tongue standing as the fallback.

The quiz_chip_copy split (arms place / place_prize, salt quizcopy) RETIRED 2026-07-28 on his word,
the same day and for the same reason as the quiz arm before it: he read both wordings and adopted
one, and this instance's traffic could not settle a two-arm test in any useful time. These rows are
the fence that keeps the retirement true — a registry entry that came back, an arm read that came
back, or two visitors reading different words would each turn a row red.

Two levels:
  1. the registry + the baked strings + the label's own source (string/data) — always runs, no Chrome
  2. the chip's rendered words (browser) — two visitors whose tokens once dealt OPPOSITE arms must
     now read the very same sentence; Chrome absent → pinned expected SKIPs.

Run: python tests/test_quiz_copy.py
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402
from quiz_util import find_token_copy_arm, chip_copy_arm_of  # noqa: E402

SITE_URL = "https://synth.example.com"
QUIZ_WORK_ID = "synth-01"
OTHER_QUIZ_ID = "synth-03"   # answered in the walk so only synth-01 stays eligible (chosen is fixed)
ADOPTED_EN = "where was this shot? · win a wallpaper"
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the quiz-ON bake
TMP_ON = Path(tempfile.mkdtemp(prefix="synth_quizcopy_"))
build_site.OUT = TMP_ON
build_site.build(SITE_URL, enable=["quiz"])

CONFIG_ON = json.loads((TMP_ON / "config.json").read_text())
EXDATA_ON = json.loads((TMP_ON / "exhibition_data.json").read_text())
js_src = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")
EN = (EXDATA_ON.get("greet") or {}).get("langs", {}).get("en", {})

# ---- STRING/DATA row: no experiment rides the quiz any more (the retirement, EX-AB/INV-90) -------
exps = CONFIG_ON.get("experiments") or {}
check("EX-QUIZ-COPY the quiz ships with NO experiment on its flag — the quiz_chip_copy split is "
      "retired and the registry carries no entry for it",
      "quiz_chip_copy" not in exps, f"experiments={sorted(exps)}")

# ---- STRING/DATA row: the label reads the ordinary localized key with the English sentence as its
#      fallback; the arm read and both retired keys are gone from the bundle and from the bake ----
label_reads_key = ('T.quiz_ask || "%s"' % ADOPTED_EN) in js_src
no_arm_read = "abArms.quiz_chip_copy" not in js_src
no_retired_keys = ("quiz_ask_place" not in js_src and "quiz_ask_prize" not in js_src
                   and "quiz_ask_place" not in EN and "quiz_ask_prize" not in EN)
key_baked = (EN.get("quiz_ask") or "").strip() != ""
check("EX-QUIZ-COPY the chip's words come off the localized quiz_ask key with the adopted English "
      "sentence as the fallback; the arm read and both retired keys are gone",
      label_reads_key and no_arm_read and no_retired_keys and key_baked,
      f"reads_key={label_reads_key} no_arm_read={no_arm_read} "
      f"no_retired_keys={no_retired_keys} key_baked={key_baked}")

# ---------------------------------------------------------------- browser rows
BROWSER_ROWS = [
    "EX-QUIZ-COPY the chip reads the adopted sentence — «%s»" % ADOPTED_EN,
    "EX-QUIZ-COPY two visitors whose tokens once dealt OPPOSITE arms now read the SAME sentence "
    "(the split is retired, the wording is adopted)",
]

# the two anchor tokens: under the retired split these dealt opposite arms, so they are exactly the
# pair that would expose a split that quietly came back. With the OTHER quiz work answered in the
# walk, synth-01 is the ONLY eligible work, so it is always the chosen chip.
TOK_A = find_token_copy_arm("place_prize")
TOK_B = find_token_copy_arm("place")

if not chrome_available() or TOK_A is None or TOK_B is None:
    reason = "Chrome not installed" if not chrome_available() else "anchor token search failed"
    for r in BROWSER_ROWS:
        skip(r, f"{reason} (pinned expected skip)")
else:
    ver = EXDATA_ON.get("version", "")

    def chip_text_for(br, base, token):
        """Drive the walk with `token`, answer the other quiz work, scroll to synth-01, return the
        rendered chip's words (or None if no chip)."""
        br.navigate(base + "/")
        br.evaluate("localStorage.clear();sessionStorage.clear()")
        br.evaluate("localStorage.setItem('ex.visitor',%s)" % json.dumps(token))
        br.evaluate("localStorage.setItem('ex-tempo','0.1')")
        # answer the OTHER quiz work so only synth-01 is eligible → synth-01 is the chosen chip
        br.evaluate("localStorage.setItem('ex.quiz.%s', JSON.stringify({answered:true,right:false}))"
                    % OTHER_QUIZ_ID)
        br.evaluate("localStorage.setItem('ex.exhibition', JSON.stringify({v:%s, pick:%s, shown:10}))"
                    % (json.dumps(ver), json.dumps(QUIZ_WORK_ID)))
        br.reload()
        br.sleep(1.2)
        br.evaluate("const f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
                    "if(f) f.scrollIntoView({behavior:'instant'})" % QUIZ_WORK_ID)
        br.sleep(0.6)
        return br.evaluate("(()=>{const c=document.querySelector('#exh-cap .ex-quiz-chip');"
                           "return c?c.textContent.trim():null;})()")

    with serve(TMP_ON) as base:
        with Browser(width=1280, height=900) as br:
            text_a = chip_text_for(br, base, TOK_A)
        with Browser(width=1280, height=900) as br:
            text_b = chip_text_for(br, base, TOK_B)
    check(BROWSER_ROWS[0], text_a == ADOPTED_EN,
          f"token={TOK_A} once_dealt={chip_copy_arm_of(TOK_A)} chip={text_a!r}")
    check(BROWSER_ROWS[1], text_a is not None and text_a == text_b,
          f"a={text_a!r} ({chip_copy_arm_of(TOK_A)})  b={text_b!r} ({chip_copy_arm_of(TOK_B)})")

shutil.rmtree(TMP_ON, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
