#!/usr/bin/env python3
"""EX-EDGE-GUARD (INV-51): bot/rate/budget fences in worker.js, all decided BEFORE any model call.
These are static source checks — the actual KV counters run only on Cloudflare edge, not locally.
Run: python tests/test_guard.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


worker = (ROOT / "engine" / "assets" / "worker.js").read_text(encoding="utf-8")

# 1 · constants present with correct names
check("EX-EDGE-GUARD BOT_RE constant declared",
      re.search(r"\bconst BOT_RE\s*=\s*/", worker) is not None,
      "BOT_RE missing from worker.js")

check("EX-EDGE-GUARD RL_PER_HOUR constant declared (numeric)",
      re.search(r"\bconst RL_PER_HOUR\s*=\s*\d+", worker) is not None,
      "RL_PER_HOUR missing or non-numeric")

check("EX-EDGE-GUARD DAY_MODEL_CAP constant declared (numeric)",
      re.search(r"\bconst DAY_MODEL_CAP\s*=\s*\d+", worker) is not None,
      "DAY_MODEL_CAP missing or non-numeric")

# 2 · helper functions present
for fn in ("isBot", "clientIp", "overRate", "overBudget", "chargeModelCall", "englishFrom"):
    check(f"EX-EDGE-GUARD {fn}() function declared",
          f"function {fn}(" in worker,
          f"{fn} missing from worker.js")

# 3 · isBot checks both empty UA and BOT_RE
check("EX-EDGE-GUARD isBot() checks empty UA (no UA = bot)",
      "!ua.trim()" in worker and "BOT_RE.test(ua)" in worker,
      "isBot does not check empty UA or BOT_RE")

# 4 · hourly window uses floor(Date.now() / 3600000)
check("EX-EDGE-GUARD overRate uses hourly bucket (floor(Date.now()/3600000))",
      "Math.floor(Date.now() / 3600000)" in worker,
      "overRate hourly bucket formula missing")

# 5 · chargeModelCall uses 2-day TTL (172800s)
check("EX-EDGE-GUARD chargeModelCall charges budget counter (expirationTtl: 172800)",
      "172800" in worker,
      "chargeModelCall 172800 TTL missing")

# 6 · englishFrom copies titles and merges src.strings + dir:ltr
check("EX-EDGE-GUARD englishFrom() assembles ltr English (src.strings + greet + titles + dir:ltr)",
      'dir: "ltr"' in worker and "src.strings" in worker and "src.greet" in worker,
      "englishFrom ltr assembly missing")

# 7 · i18n route: bot/budget guard fires BEFORE model call
# The i18n handling runs from the pathname !== "/api/i18n" check to the visitor function definition.
i18n_block = worker[
    worker.find('if (url.pathname !== "/api/i18n")'):
    worker.find("\nasync function visitor(")
]
check("EX-EDGE-GUARD i18n route: isBot/overBudget → englishFrom fallback",
      "isBot(req)" in i18n_block and "englishFrom(src)" in i18n_block,
      "i18n route missing isBot/englishFrom guard")

check("EX-EDGE-GUARD i18n route: overRate → 429 slow-down",
      "overRate(env, req)" in i18n_block and "429" in i18n_block,
      "i18n route missing overRate 429 guard")

check("EX-EDGE-GUARD i18n route: chargeModelCall before translate()",
      "chargeModelCall(env)" in i18n_block and "translate(" in i18n_block
      and i18n_block.index("chargeModelCall(env)") < i18n_block.index("translate("),
      "i18n route: chargeModelCall not before translate()")

# 8 · story route: bot/budget guard fires BEFORE model call (after cache hit)
story_fn = worker[worker.find("async function story("):]
story_fn = story_fn[:story_fn.find("\nasync function narrate(")]  # trim to story function body
check("EX-EDGE-GUARD story route: isBot/overBudget → no story silence",
      "isBot(req)" in story_fn and '"no story"' in story_fn,
      "story route missing isBot/no-story guard")

check("EX-EDGE-GUARD story route: overRate → 429 slow-down",
      "overRate(env, req)" in story_fn and "429" in story_fn,
      "story route missing overRate 429 guard")

check("EX-EDGE-GUARD story route: chargeModelCall before narrate()",
      "chargeModelCall(env)" in story_fn and "narrate(" in story_fn
      and story_fn.index("chargeModelCall(env)") < story_fn.index("narrate("),
      "story route: chargeModelCall not before narrate()")

fails = [r for r in results if r[1] == "FAIL"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails)} pass, {len(fails)} fail")
sys.exit(1 if fails else 0)
