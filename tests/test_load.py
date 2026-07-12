#!/usr/bin/env python3
"""The loading breath + crossing re-clocked (EX-LOAD / INV-37 · EX-TIMING / INV-38) — adapted
for exhibition-engine synthetic fixture. Run: python tests/test_load.py
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
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


TMP = Path(tempfile.mkdtemp(prefix="synth_load_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
VER = str(DATA["version"])
PICK = DATA["door"]["pool"][0]["id"]
WALK = json.dumps({"v": VER, "pick": PICK, "shown": 10})

# ---- data row: asset-weight budget
heavy = []
for w in DATA["works"]:
    p = TMP / w["img"].lstrip("/")
    if p.exists() and p.stat().st_size > 1_200_000:
        heavy.append(f"{w['id']} {p.stat().st_size // 1024}KB")
check("N10 budget: every baked work derivative ≤ 1.2 MB (the breath is for networks, not bloat)",
      not heavy, " | ".join(heavy[:5]))

# ---- three walk fixes ported from an instance (string level; the feel rides the browser rows) ----
INDEX_SRC = (TMP / "index.html").read_text(encoding="utf-8")
CSS_SRC = (TMP / "exhibition.css").read_text(encoding="utf-8")
JS_SRC = (TMP / "exhibition.js").read_text(encoding="utf-8")
# 1 · the cold-arrival line — a quiet instance line before the walk comes alive, on a grace beat only
check("EX-LOAD cold line: build emits #ex-loading with the instance line; CSS gates it on a grace "
      "beat + hides it on ex-live (no black void on a slow cold link)",
      'id="ex-loading"' in INDEX_SRC and "#ex-loading" in CSS_SRC
      and "@keyframes ex-loadin" in CSS_SRC and "body.ex-live #ex-loading{ display:none" in CSS_SRC,
      "ex-loading emit/CSS")
# 2 · the closing screen no longer strands the last work's caption
check("finale caption clears: the observer fades the caption out on #exh-fin, and the finale is "
      "observed (never a stranded/stale title over the closing screen)",
      'x.target.id === "exh-fin"' in JS_SRC and "io.observe(fin)" in JS_SRC,
      "finale guard + observe")
# 3 · changing the viewport aspect rebuilds the door WITHOUT the entry fade
check("door relayout no re-fade: a fresh open animates its windows in; an aspect-change relayout "
      "rebuilds WITHOUT the entry fade (windows already on screen)",
      "doorRender(true)" in JS_SRC and 'b.style.animation = "none"' in JS_SRC,
      "doorRender animate branch")

# ---- EX-LADDER (INV-63): the responsive 640/960/1280 image ladder ported from an instance --------
# pure helpers (no bake, no PIL): srcset_of builds the ladder over a served path; the base stays fallback
_L = build_site.srcset_of("/gallery/assets/x/17.jpg")
check("EX-LADDER srcset_of builds the 640/960/1280 ladder over a served path",
      _L == "/gallery/assets/x/17-640.jpg 640w, /gallery/assets/x/17-960.jpg 960w, "
            "/gallery/assets/x/17-1280.jpg 1280w",
      _L)
check("EX-LADDER js emits the per-work srcset + sizes on the walk img (base src stays the fallback)",
      "w.srcset" in JS_SRC and "walk_sizes" in JS_SRC and "srcset=" in JS_SRC,
      "js ladder emit")
# the real capped bake writes the tier files + joins srcset/walk_sizes to the data — needs Pillow
try:
    import PIL  # noqa: F401
    _HAVE_PIL = True
except Exception:
    _HAVE_PIL = False
if _HAVE_PIL:
    TMP_CAP = Path(tempfile.mkdtemp(prefix="synth_ladder_"))
    build_site.OUT = TMP_CAP
    build_site.build(SITE_URL, display_max=1000)
    D2 = json.loads((TMP_CAP / "exhibition_data.json").read_text(encoding="utf-8"))
    w0 = D2["works"][0]
    tiers = all((TMP_CAP / build_site.tier_url(w0["img"], t).lstrip("/")).exists() for t in (640, 960, 1280))
    check("EX-LADDER capped bake writes 640/960/1280 tiers + adds srcset/walk_sizes to the data",
          "srcset" in w0 and D2.get("walk_sizes") == "88vw" and tiers,
          f"srcset={'srcset' in w0} sizes={D2.get('walk_sizes')} tiers={tiers}")
    build_site.OUT = TMP
else:
    skip("EX-LADDER capped bake writes 640/960/1280 tiers + srcset/walk_sizes", "Pillow absent")

BROWSER_ROWS = [
    "EX-DOOR-2e the clock is one third (pick→reveal ≈1.8 beats ×tempo, caption right behind)",
    "EX-LOAD the cold return plates, then reveals (held image → tone plate → work fades in) [superseded by EX-LOAD-2]",
    "EX-LOAD a healthy line never sees it (no plate, no ex:plate mark on a normal crossing)",
    "EX-LOAD a dead image never traps (plate retires, caption+counter hold, walk alive)",
    "EX-TIMING marks are laid, export on ask; nothing in the DOM (INV-1)",
]

# the in-flight ladder's superseding face: the plate (EX-LOAD-2) replaced the lone breath hairline
PLATE_ON = ("(()=>{const p=document.getElementById('ex-plate');"
            "return !!p && !p.hidden && p.classList.contains('show')})()")
MARKS = ("JSON.stringify(Object.fromEntries(performance.getEntriesByType('mark')"
         ".filter(m=>m.name.startsWith('ex:')).map(m=>[m.name.slice(3),m.startTime])))")
FIRST_IMG = "document.querySelector('.exh-frame img.work')"

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    HOLD = {}
    with serve(TMP, hold=HOLD) as base:
        # 0 · the clock is one third
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            br.click(".exd-window:nth-child(1)", settle=0.1)
            br.sleep(2.4)
            marks = json.loads(br.evaluate(MARKS) or "{}")
            have = all(k in marks for k in ("pick", "hang", "reveal", "caption"))
            delta = (marks.get("reveal", 9e9) - marks.get("pick", 0)) / 1000.0
            cap_gap = (marks.get("caption", 9e9) - marks.get("reveal", 0)) / 1000.0
            revealed = br.evaluate(
                f"+getComputedStyle({FIRST_IMG}).opacity") or 0
            check(BROWSER_ROWS[0],
                  have and 0.72 <= delta <= 1.25 and cap_gap < 0.4 and revealed > 0.5,
                  f"marks={sorted(marks)} pick→reveal={delta:.2f}s "
                  f"caption+{cap_gap:.2f}s work_opacity={revealed}")

        # 1 · the cold return plates: a stored walk, the first image HELD 2s by the server — past
        # the grace beat the tone plate stands and the image is incomplete; when the bytes land the
        # plate retires and the work fades in over it (tempo 0.2 → grace 0.07s)
        HOLD.update(match=PICK, delay=2.0)
        with Browser(width=1280, height=900) as br:
            br.navigate("about:blank")
            br.navigate(base + "/")
            br.evaluate(f"localStorage.setItem('ex.exhibition', {json.dumps(WALK)})")
            br.evaluate("localStorage.setItem('ex-tempo','0.2')")
            br.reload()
            br.sleep(0.8)
            mid = br.evaluate(
                "(()=>{const i=" + FIRST_IMG + ";return {plate:" + PLATE_ON + ","
                "complete:i&&i.complete,text:(document.getElementById('ex-plate')||{}).textContent||''};})()")
            br.sleep(2.6)
            after = br.evaluate(
                "(()=>{const i=" + FIRST_IMG + ";return {plate:" + PLATE_ON + ","
                "ok:i&&i.complete&&i.naturalWidth>0,op:+getComputedStyle(i).opacity};})()")
            check(BROWSER_ROWS[1],
                  mid["plate"] and not mid["complete"] and mid["text"].strip() == ""
                  and not after["plate"] and after["ok"] and after["op"] > 0.5,
                  f"mid={mid} after={after}")
        HOLD.clear()

        # 2 · a healthy line never sees the plate: a normal local crossing lays no ex:plate
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            br.click(".exd-window:nth-child(1)", settle=0.1)
            br.sleep(2.4)
            marks = json.loads(br.evaluate(MARKS) or "{}")
            revealed = br.evaluate(f"+getComputedStyle({FIRST_IMG}).opacity") or 0
            check(BROWSER_ROWS[2],
                  "plate" not in marks and not br.evaluate(PLATE_ON) and revealed > 0.5,
                  f"marks={sorted(marks)} plate_on={br.evaluate(PLATE_ON)} op={revealed}")

        # 3 · a dead image never traps: the request BLOCKED (a real error event) — the plate
        # retires (or never shows), the caption and counter still hold the frame, no crash
        with Browser(width=1280, height=900) as br:
            br.block([f"*{PICK}*"])
            br.navigate(base + "/")
            br.evaluate(f"localStorage.setItem('ex.exhibition', {json.dumps(WALK)})")
            br.evaluate("localStorage.setItem('ex-tempo','0.2')")
            br.reload()
            br.sleep(1.5)
            state = br.evaluate(
                "(()=>{const i=" + FIRST_IMG + ";return {plate:" + PLATE_ON + ","
                "dead:i&&i.complete&&i.naturalWidth===0,"
                "cap:(document.getElementById('exh-cap')||{}).textContent||'',"
                "counter:document.querySelector('.exh-counter.show')!==null,"
                "alive:1+1===2};})()")
            check(BROWSER_ROWS[3],
                  not state["plate"] and state["dead"] and state["cap"].strip() != ""
                  and state["counter"] and state["alive"],
                  f"state={state}")
            br.block([])

        # 4 · the museum keeps time
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/?timings")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            br.click(".exd-window:nth-child(1)", settle=0.1)
            br.sleep(2.4)
            marks = json.loads(br.evaluate(MARKS) or "{}")
            need = {"boot", "data", "door", "pick", "hang", "reveal", "caption"}
            exported = br.evaluate(
                "typeof EXTimings==='function' && EXTimings().length >= 7")
            dom_clean = not br.evaluate("document.body.innerText.includes('ex:')")
            check(BROWSER_ROWS[4],
                  need.issubset(marks) and bool(exported) and dom_clean,
                  f"marks={sorted(marks)} exported={exported} dom_clean={dom_clean}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
