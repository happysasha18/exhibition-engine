#!/usr/bin/env python3
"""EX-STORY-LEAD: the opening plot covers the first few works, the rest of the spread waits.

A visit that rests in the opening works used to buy a telling for the whole first spread — one ask
covering ten works, of which most visits read one or two. The first spread now carries two portions:
a short opening plot over the first `story_lead` works, asked the moment the walk stands, and one
plot over the rest of that spread, asked as the focus comes within a work of it. Each portion keeps
its own edge cache key, and a shorter opening slice repeats across visitors more often, so it is
served from that cache more often too.

Rows:
  1 (data)    the bake ships the knob, and the client clamps it
  2 (string)  storyPortions splits the first spread; portionReached gates a mid-spread portion on
              the focus, and leaves every other portion asked at its own beat
  3 (browser) the arrival asks ONE plot and it names exactly the opening works
  4 (browser) reaching the opening portion's last work asks the REST of the spread, once

The browser rows drive the real client with `fetch` standing in for the edge, so the ids each ask
carries are read straight off the request the client made. Chrome absent → pinned expected SKIPs.

Run: python tests/test_story_lead.py
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

SITE_URL = "https://synth.example.com"
LEAD = 3
SPREAD = 10
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


TMP = Path(tempfile.mkdtemp(prefix="synth_storylead_"))
build_site.OUT = TMP
build_site.build(SITE_URL, enable=["ai_story"])

CONFIG = json.loads((TMP / "config.json").read_text())
js_src = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")

# ---- 1 · the knob ships and is clamped client-side -----------------------------------------------
ex = CONFIG.get("exhibition") or {}
check("EX-STORY-LEAD the bake ships story_lead, and the client clamps it to a sane range",
      ex.get("story_lead") == LEAD and "clampInt(EX.story_lead, 3, 1, 12)" in js_src,
      f"config={ex.get('story_lead')!r} clamp_present={'clampInt(EX.story_lead' in js_src}")

# ---- 2 · the split and its gate live in the client ----------------------------------------------
split = ("const lead = Math.min(STORY_LEAD, first);" in js_src
         and "if (lead < first) parts.push([lead, first]);" in js_src)
gate = ("function portionReached(lo)" in js_src
        and "if (lo <= 0 || lo >= SPREAD) return true;" in js_src
        and "if (portionReached(lo)) askPortion(lo, hi);" in js_src)
check("EX-STORY-LEAD the first spread splits into the opening plot and the rest, and a mid-spread "
      "portion is asked only once the focus has come near it",
      split and gate, f"split={split} gate={gate}")

# ---------------------------------------------------------------- browser rows
BROWSER_ROWS = [
    "EX-STORY-LEAD the arrival asks ONE plot, naming exactly the opening works",
    "EX-STORY-LEAD reaching the opening portion's last work asks the REST of the spread, once",
]

# `fetch` stands in for the edge: every /api/story ask is recorded with the ids it carried and
# answered with a plot naming those same ids, so the client walks its ordinary success path.
STUB = """
(() => {
  window.__asks = [];
  const of = window.fetch;
  window.fetch = function (u, o) {
    if (String(u).indexOf('/api/story') >= 0) {
      let ids = [];
      try { ids = JSON.parse(o.body).ids; } catch (e) {}
      window.__asks.push(ids);
      const body = JSON.stringify({
        story_variant: 'a',
        lines: ids.map((id) => ({ id: id, line: 'a told line', source: 'facts' })),
      });
      return Promise.resolve(new Response(body, {
        status: 200, headers: { 'Content-Type': 'application/json' } }));
    }
    return of.apply(this, arguments);
  };
})()
"""

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.2')")
            br.reload()
            br.sleep(1.0)
            # the stub goes in AT THE DOOR: the walk's first ask rides the door pick, so nothing has
            # been asked yet at this point
            br.evaluate(STUB)
            if br.evaluate("!!document.querySelector('.exd-window')"):
                br.click(".exd-window:nth-child(1)", settle=1.2)
            br.sleep(1.2)
            asks = br.evaluate("window.__asks") or []
            first_ok = len(asks) == 1 and len(asks[0]) == LEAD
            check(BROWSER_ROWS[0], first_ok,
                  f"asks after arrival={[len(a) for a in asks]} (expected exactly one of {LEAD})")

            # walk to the opening portion's last work — the rest of the spread is asked there
            br.evaluate("(()=>{const f=document.querySelectorAll('.exh-frame');"
                        "if(f[%d]) f[%d].scrollIntoView({behavior:'instant',block:'center'});})()"
                        % (LEAD - 1, LEAD - 1))
            br.sleep(1.4)
            asks2 = br.evaluate("window.__asks") or []
            rest = asks2[1] if len(asks2) > 1 else []
            second_ok = (len(asks2) == 2 and len(rest) == SPREAD - LEAD
                         and not set(rest) & set(asks2[0]))
            check(BROWSER_ROWS[1], second_ok,
                  f"asks after reaching work {LEAD}={[len(a) for a in asks2]} "
                  f"(expected {LEAD} then {SPREAD - LEAD}, no work told twice)")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
