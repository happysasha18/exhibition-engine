#!/usr/bin/env python3
"""S-115 — ONE production-shaped route, walked and photographed.

This is not a test and it holds no assertion. It walks a real staged site (the one
`scripts/release-v2.sh` bakes) under `?pass=diagnostics:on`, presses the visitor's own ArrowDown
between ten hung works, and for every played step writes:

  · the joined per-step diagnostic record the panel itself reads (`window.__<ns>Pass.joined`,
    exported whole through the panel's own "выгрузить" button) — route role, family/primary/pivot,
    voices with their windows/levels/handles, camera lead + track + start/middle/end poses, the
    WorkRecord measurements the ranking read with their values, the bundle ledger with its refusals,
    requested role vs realised tier and the downgrade reason;
  · the host's own live reading at the instant photographed (`host.report()`);
  · three PNGs — the step's start, its own motion peak, and its end.

THE PEAK IS THE PASSAGE'S OWN. `composer.motionPeak(cues, durSec)` names the instant the score's own
driven handles move hardest; the frame loop is pinned there (`host.configure({clockPin, progressPin})`)
and photographed. Nothing here reads this machine's wall clock, and no verdict rests on one.

WHY IT NAMES NO PAIR AND NO EFFECT. The ten works are the door's own deal (`dealDiverse`,
engine/client/05-door-deal-circle-walkstate.js) — `--seed` only fixes the die that deal already
rolls, so a route can be walked twice and photographed the second time. Which effect any pair
produces is the composer's alone; this file records what it chose.

Run:
  python3 tests/capture_route.py --stage <dir> --out <dir> --width 390 --height 844 --seed 7
"""
import argparse
import base64
import json
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
from headless import serve, Browser, chrome_available  # noqa: E402

RECORDS_ROUTE = "/api/pass/records"


# ---------------------------------------------------------------- the site's own record route
# In production a Cloudflare Worker answers this (`_worker.js`'s `passRecordsRoute`): ?ids=a,b,c →
# {"records": {...}}, capped by config.json's own `pass.records.cap`. Served here off the same
# `pass-workrecords.json` asset the Worker reads, so the walk gets the records a visitor gets.
def records_answer_for(stage):
    records = json.loads((stage / "pass-workrecords.json").read_text(encoding="utf-8"))
    cap = int(((json.loads((stage / "config.json").read_text(encoding="utf-8"))
                .get("pass") or {}).get("records") or {}).get("cap") or 20)

    def answer(raw_path):
        if not raw_path.startswith(RECORDS_ROUTE):
            return None
        ids = [i for i in parse_qs(urlparse(raw_path).query).get("ids", [""])[0].split(",") if i]
        if not ids or len(ids) > cap:
            return (400, "text/plain", "bad request")
        return (200, "application/json",
                json.dumps({"records": {i: records[i] for i in ids if i in records}}))
    return answer


def namespace_of(stage):
    """The built client's own namespace, read off the baked file rather than assumed."""
    import re
    m = re.search(r"window\.__(\w*)PassComposer\s*=", (stage / "exhibition.js").read_text("utf-8"))
    return m.group(1) if m else ""


# ---------------------------------------------------------------- what rides in before the page
PRELUDE = r"""
(function () {
  // A DIE THIS RUN CAN ROLL AGAIN. The door's own deal (dealDiverse) picks its seed work and its
  // ordering axis off Math.random; fixing the generator fixes which ten works hang, so the route
  // read on one pass is the route photographed on the next. Nothing else about the deal changes.
  var s = %(seed)d >>> 0;
  Math.random = function () {
    s |= 0; s = (s + 0x6D2B79F5) | 0;
    var t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };

  // THE COMPOSER INSTANCE ITSELF, so this run can ask the score for its own motion peak. The client
  // hands the module a setter on window; this stands in front of that setter, wraps the module's
  // `make` and keeps what it returns. The client's own call runs unchanged underneath.
  var real = null;
  Object.defineProperty(window, "__%(ns)sPassComposer", {
    configurable: true,
    get: function () {
      return function (m) {
        try {
          var om = m.make;
          m.make = function () { var i = om.apply(m, arguments); window.__composer = i; return i; };
        } catch (e) {}
        return real ? real(m) : undefined;
      };
    },
    set: function (v) { real = v; }
  });

  // Anything the live walk says went wrong, kept for the report.
  window.__errs = [];
  addEventListener("error", function (e) {
    window.__errs.push("error: " + (e.message || String(e)) + " @" + (e.filename || "") + ":" + (e.lineno || 0));
  });
  addEventListener("unhandledrejection", function (e) {
    window.__errs.push("rejection: " + String((e && e.reason) || e));
  });
  ["error", "warn"].forEach(function (k) {
    var was = console[k];
    console[k] = function () { window.__errs.push("console." + k + ": " + [].join.call(arguments, " ")); return was.apply(console, arguments); };
  });

  // The export writes to the clipboard and saves a file; the clipboard leg is read here. Headless
  // Chrome hands out no `navigator.clipboard` of its own, so one is stood up before it is stubbed.
  window.__copied = [];
  if (!navigator.clipboard) {
    Object.defineProperty(navigator, "clipboard", {configurable: true, value: {}});
  }
  navigator.clipboard.writeText = function (t) { window.__copied.push(t); return Promise.resolve(); };
})();
"""


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return Path(path).name


def wait_for(br, expr, timeout=20.0, step=0.15):
    end = time.time() + timeout
    val = None
    while time.time() < end:
        val = br.evaluate(expr)
        if val and val != "false":
            return val
        br.sleep(step)
    return val


def enter(br, base, pick=None, door_pick=None):
    """A visitor's own entry: the door, the window, the walk.

    `pick` takes the site's own share-link road instead (`#w-<id>`, engine/client/17-place-hash-boot.js):
    the hash acts as a pick, the hang is the same kinship arc a door pick assembles, and the walk is
    the same one. It exists so the ten works read on the phone can be walked again at a desktop
    width, where the door's own deal would otherwise hand out a different ten."""
    br.navigate(base + "/")
    br.clear_storage()
    br.navigate(base + "/?pass=diagnostics:on" + (("#w-" + pick) if pick else ""))
    br.sleep(1.0)
    # THE DIAGNOSTICS PANEL DRAWS OVER THE FRAME and would ride into every capture (the audit
    # measured 6271 polluted pixels, worst 195 of 255). Held at zero opacity rather than
    # display:none, so the panel keeps laying itself out and its own export keeps working. Laid
    # here rather than in the pre-load script, where no document element exists to hang it on.
    br.evaluate("var st=document.createElement('style');"
                "st.textContent='#ex-verdict{opacity:0!important;pointer-events:none!important}';"
                "document.head.appendChild(st); 0")
    br.evaluate("window.__P = (function(){for (var k in window) "
                "if (/^__\\w*Pass$/.test(k) && window[k] && window[k].host) return window[k];})(); 0")
    sel = ".exd-window" if not door_pick else (".exd-window[data-id=\"%s\"]" % door_pick)
    if not pick and js(br, "return {has: !!document.querySelector('%s')};" % sel)["has"]:
        try:
            br.click(sel, settle=1.6)
        except RuntimeError:
            br.sleep(1.2)
    elif door_pick:
        return False
    for _ in range(30):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.5)
    br.evaluate("window.__P = window.__P || (function(){for (var k in window) "
                "if (/^__\\w*Pass$/.test(k) && window[k] && window[k].host) return window[k];})(); 0")
    # the composer's own file and the record wave both have to have landed before a crossing can be
    # composed at all — polled for, never slept at
    for _ in range(150):
        got = js(br, "if (!window.__P) return {};"
                     "var r = window.__P.report();"
                     "return {st: r.composer.state, held: r.records.held,"
                     " waves: r.records.waves, inflight: r.records.inflight};")
        if (got.get("st") == "read" and (got.get("waves") or 0) > 0
                and (got.get("inflight") or 0) == 0 and (got.get("held") or 0) > 1):
            return True
        br.sleep(0.2)
    return False


def hung(br):
    return js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                  ".map(function(f){return f.dataset.id;});")


def pin(br, seconds, progress):
    br.evaluate("window.__P.host.configure({clockPin:%r, progressPin:%r}); 0" % (seconds, progress))


def unpin(br):
    br.evaluate("window.__P.host.configure({clockPin:null, progressPin:null}); 0")


LIVE_READING = """
  var P = window.__P, r = P.host.report();
  var ps = P.passages() || [];
  var row = null;
  for (var i = ps.length - 1; i >= 0; i--) { if (ps[i] && (ps[i].played || ps[i].score)) { row = ps[i]; break; } }
  var sc = row ? (row.played || row.score) : null;
  return {
    state: r.state, gen: r.gen, duration: r.duration, variant: r.variant,
    instrument: r.instrument, live: r.live, drew: r.drew, drawnOn: r.drawnOn,
    grant: r.grant, budget: r.budget, pace: r.pace, device: r.device,
    camera: r.camera, rest: r.rest, hang: r.hang, cadence: r.cadence,
    carrier: r.carrier,
    stack: (r.stack || []).map(function (v) {
      return {id: v.id, instrument: v.instrument, stack: v.stack, line: v.line, live: !!v.live,
              window: v.window, levels: v.levels, handles: v.handles, applied: v.applied};
    }),
    // THE EVENT RING IS ONE 128-ROW RING FOR THE WHOLE VISIT, not a per-transaction list — filtered
    // to this transaction's own generation, or a fault three steps back rides onto this one.
    events: (r.events || []).filter(function (e) { return e.gen === r.gen; })
             .map(function (e) { return {name: e.name, why: e.why}; }),
    scoreCamera: sc ? (sc.camera || null) : null,
    scoreDuration: sc ? sc.duration : null,
    road: row ? row.road : null,
    declined: row ? (row.declined || null) : null,
    diagnostics: row ? (row.diagnostics || null) : null
  };
"""


def peak_of(br):
    """The passage's own motion peak, off the composer's own `motionPeak`."""
    return js(br, """
      var P = window.__P, ps = P.passages() || [], row = null;
      for (var i = ps.length - 1; i >= 0; i--) { if (ps[i] && (ps[i].played || ps[i].score)) { row = ps[i]; break; } }
      var sc = row ? (row.played || row.score) : null;
      if (!sc || !window.__composer) return {ok: false, why: sc ? "no composer instance" : "no score"};
      var durSec = (sc.duration || 0) / 1000;
      var p = window.__composer.motionPeak(sc.cues || [], durSec);
      return {ok: true, at: p.at, share: p.share, flat: !!p.flat, durSec: durSec,
              cues: (sc.cues || []).map(function (c) { return c.instrument ? c.instrument.id : null; })};
    """)


def walk(br, base, out, steps, tag, frames=True, extra=None, pick=None, door_pick=None):
    """The walk itself: enter, then one ArrowDown a step, each frozen and photographed.

    `extra` is a map step-number → [progress, …]: further instants of that step's own passage to
    photograph beside its peak. It exists for one honest case — a voice whose window opens AFTER the
    passage's own motion peak is not in the peak frame at all, and the peak frame is the only one
    that counts as the gesture. An extra frame shows what that voice does inside its own window and
    is labelled as such; it never stands in for the peak.
    """
    extra = extra or {}
    if not enter(br, base, pick=pick, door_pick=door_pick):
        return {"error": "the composer or the records never settled"}
    ids = hung(br)
    played = []
    for n in range(1, steps + 1):
        # frozen at the opening BEFORE the key, so the passage this step composes cannot run past
        # the instant this run means to photograph
        pin(br, 0.001, 0.001)
        br.key("ArrowDown")
        ok = wait_for(br, "String(window.__P.host.report().state === 'running')", timeout=12.0)
        if ok != "true":
            unpin(br)
            played.append({"n": n, "skipped": "no crossing ran on this key",
                           "state": br.evaluate("window.__P.host.report().state")})
            br.sleep(1.2)
            continue
        br.sleep(0.35)
        rec = {"n": n}
        if frames:
            rec["startFrame"] = png(br, out / ("%s-step-%02d-start.png" % (tag, n)))
        pk = peak_of(br)
        rec["peak"] = pk
        if pk.get("ok"):
            pin(br, pk["at"], pk["share"])
            br.sleep(0.45)
            if frames:
                rec["peakFrame"] = png(br, out / ("%s-step-%02d-peak.png" % (tag, n)))
            rec["atPeak"] = js(br, LIVE_READING)
            for u in extra.get(n, []):
                pin(br, pk["durSec"] * u, u)
                br.sleep(0.45)
                rec.setdefault("extra", []).append(
                    {"progress": u,
                     "frame": png(br, out / ("%s-step-%02d-at%03d.png" % (tag, n, round(u * 100))))
                              if frames else None,
                     "reading": js(br, LIVE_READING)})
            pin(br, pk["durSec"] * 0.985, 0.985)
            br.sleep(0.4)
            if frames:
                rec["endFrame"] = png(br, out / ("%s-step-%02d-end.png" % (tag, n)))
        unpin(br)
        # the landing is the walk's own — polled for, never slept through
        wait_for(br, "String(window.__P.host.report().state === 'idle')", timeout=14.0)
        br.sleep(0.5)
        played.append(rec)
    # the panel's own export: the joined per-step record for every step that docked
    br.evaluate("var b=document.querySelector('.exv-dump'); if (b) b.click(); 0")
    br.sleep(0.6)
    raw = br.evaluate("window.__copied && window.__copied.length "
                      "? window.__copied[window.__copied.length-1] : null")
    export = json.loads(raw) if raw else None
    if export is None:
        # the panel's own rows carry the same joined record it exports (`JSON.stringify(joined,…)`),
        # so a clipboard the browser refuses costs the run nothing
        export = {"steps": js(br, "return [].slice.call("
                                  "document.querySelectorAll('#ex-verdict .exv-step-detail'))"
                                  ".map(function(d){return JSON.parse(d.textContent);});"),
                  "via": "the panel's own rows (the clipboard leg wrote nothing)"}
    return {"hung": ids, "steps": played, "export": export,
            "errors": js(br, "return window.__errs || [];"),
            "viewport": js(br, "return {w: innerWidth, h: innerHeight, dpr: devicePixelRatio};")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--steps", type=int, default=9)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--door-pick", default=None,
                    help="open the door and click THIS work's own window — the same road any visitor "
                         "takes, aimed at one work so a second width walks the same ten. The run "
                         "fails plainly if the deal did not hang that work.")
    ap.add_argument("--pick", default=None,
                    help="enter by the site's own #w-<id> share link on this work, instead of "
                         "opening the door — the way the same ten works are walked at a second width")
    ap.add_argument("--extra", default="",
                    help="further instants to photograph, as step:progress pairs — "
                         "\"8:0.50,9:0.60\". Each is labelled as an extra instant and never "
                         "stands in for the passage's own peak.")
    ap.add_argument("--no-frames", action="store_true",
                    help="walk and record the chain only — no PNGs (used to read a route before "
                         "photographing it)")
    a = ap.parse_args()
    stage, out = Path(a.stage), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    tag = a.tag or ("phone" if a.width < 700 else "desktop")
    if not chrome_available():
        print("Chrome is not on this machine", file=sys.stderr)
        return 3
    ns = namespace_of(stage)
    with serve(stage, answer=records_answer_for(stage)) as base:
        with Browser(width=a.width, height=a.height) as br:
            br.inject(PRELUDE % {"seed": a.seed, "ns": ns})
            extra = {}
            for pair in [x for x in a.extra.split(",") if x.strip()]:
                n, u = pair.split(":")
                extra.setdefault(int(n), []).append(float(u))
            got = walk(br, base, out, a.steps, tag, frames=not a.no_frames, extra=extra, pick=a.pick,
                       door_pick=a.door_pick)
    got["run"] = {"stage": str(stage), "width": a.width, "height": a.height,
                  "seed": a.seed, "steps": a.steps, "namespace": ns, "tag": tag,
                  "pick": a.pick, "doorPick": a.door_pick}
    p = out / ("%s-route.json" % tag)
    p.write_text(json.dumps(got, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("written %s" % p)
    print("hung: %s" % json.dumps(got.get("hung")))
    for s in got.get("steps", []):
        print(" step %02d  %s" % (s["n"], json.dumps(s.get("peak") or s.get("skipped"),
                                                     ensure_ascii=False)[:160]))
    print("errors: %s" % json.dumps(got.get("errors"), ensure_ascii=False)[:600])
    return 0


if __name__ == "__main__":
    sys.exit(main())
