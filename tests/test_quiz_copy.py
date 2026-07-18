#!/usr/bin/env python3
"""EX-QUIZ-COPY (INV-93 · EX-AB): the quiz chip's words ride the quiz_chip_copy experiment.

The chip drops the bare «question?». Its words are dealt off the visitor's seed by the
quiz_chip_copy arm (salt "quizcopy", arms ["place","place_prize"]): the plain arm names the act
(«guess the place»), the reward arm names the gift as well («guess the place · win a wallpaper»).
The words localize through EX-I18N (quiz_ask_place / quiz_ask_prize) with English source-tongue
fallbacks; an absent registry falls to the plain copy.

Two levels:
  1. the registry + baked strings (string/data) — always runs, no Chrome
  2. the chip's rendered words per forced arm (browser) — a token forced to each arm drives the
     real chip; Chrome absent → pinned expected SKIPs.

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
from quiz_util import find_token_copy_arm, arm_of, chip_copy_arm_of  # noqa: E402

SITE_URL = "https://synth.example.com"
QUIZ_WORK_ID = "synth-01"
OTHER_QUIZ_ID = "synth-03"   # answered in the walk so only synth-01 stays eligible (chosen is fixed)
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

# ---- STRING/DATA row: the experiment is registered with the pinned arms + salt (EX-AB/INV-90) ----
exp = (CONFIG_ON.get("experiments") or {}).get("quiz_chip_copy") or {}
reg_ok = (exp.get("arms") == ["place", "place_prize"]
          and exp.get("salt") == "quizcopy"
          and exp.get("flag") == "quiz"
          and exp.get("metric") == "walk_unfold")
check("EX-QUIZ-COPY the quiz_chip_copy experiment is registered when the quiz ships "
      "(arms place/place_prize, salt quizcopy, metric walk_unfold)",
      reg_ok, f"entry={exp}")

# ---- STRING/DATA row: quizLabel reads BOTH keys with English source-tongue fallbacks; the plain
#      arm is the no-registry default; the bare «question?» chip fallback is gone ----------------
label_reads_arm = ("abArms && abArms.quiz_chip_copy" in js_src
                   and 'T.quiz_ask_prize || "guess the place · win a wallpaper"' in js_src
                   and 'T.quiz_ask_place || "guess the place"' in js_src)
no_bare_question = '"question?"' not in js_src        # the bare-question chip fallback is retired
keys_baked = "quiz_ask_place" in EN and "quiz_ask_prize" in EN
check("EX-QUIZ-COPY quizLabel deals the words off the arm with English fallbacks; keys baked; "
      "the bare «question?» chip fallback is retired",
      label_reads_arm and no_bare_question and keys_baked,
      f"reads_arm={label_reads_arm} no_bare_question={no_bare_question} keys_baked={keys_baked}")

# ---------------------------------------------------------------- browser rows
BROWSER_ROWS = [
    "EX-QUIZ-COPY the reward arm (place_prize) names the gift — the chip reads «guess the place · win a wallpaper»",
    "EX-QUIZ-COPY the plain arm (place) names the act — the chip reads «guess the place»",
]

# force each arm: a token that deals quiz_arm=on AND the wanted quiz_chip_copy arm. With the OTHER
# quiz work answered in the walk, synth-01 is the ONLY eligible work, so it is always chosen and its
# chip renders — the arm is the only free variable, exactly what these rows measure.
TOK_PRIZE = find_token_copy_arm("place_prize")
TOK_PLACE = find_token_copy_arm("place")

if not chrome_available() or TOK_PRIZE is None or TOK_PLACE is None:
    reason = "Chrome not installed" if not chrome_available() else "arm token search failed"
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
            prize_text = chip_text_for(br, base, TOK_PRIZE)
            check(BROWSER_ROWS[0],
                  prize_text == "guess the place · win a wallpaper",
                  f"token={TOK_PRIZE} copy_arm={chip_copy_arm_of(TOK_PRIZE)} chip={prize_text!r}")
        with Browser(width=1280, height=900) as br:
            place_text = chip_text_for(br, base, TOK_PLACE)
            check(BROWSER_ROWS[1],
                  place_text == "guess the place",
                  f"token={TOK_PLACE} copy_arm={chip_copy_arm_of(TOK_PLACE)} chip={place_text!r}")

shutil.rmtree(TMP_ON, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
