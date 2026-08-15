#!/usr/bin/env python3
"""PASS-API-V1 §4.4b — the delivery pack's reader on the walk's own road.
Run: python3 tests/test_pass_reader.py

Root: the full-walk drive of 2026-08-14 (the site tree's
docs/immersive/evidence/2026-08-14-walk-slice-three-works.md, §2) measured the gap this suite
closes. The site composes a score for every ordered pair and ships them as a PACK of static files;
its settings record carries the pack's addresses under `pass.packs`; and no byte a visitor ran read
that name, so all nineteen steps of a real route fell back to the walk's own glide in silence and
the wire was never asked for a single shard.

WHAT IS MEASURED HERE, AND ON WHAT.

  The real walk, the real bundle, a real pack. Every browser row below bakes a synthetic site,
  writes a pack of static files beside it, serves the pair, and drives the walk's own
  `declare` — the same door the stepping input knocks on. Nothing is stubbed: the score that
  reaches the command is the score the reader fetched, weighed and filled.

  THE ROW'S OWN SHAPE PICKS THE TEMPLATE. The pack carries one template per PASSAGE SHAPE — the
  shipped one carries twenty-five — and each row names its own shape as its first entry. The pack
  written here carries two shapes whose scores differ, and two pairs in one shard: one row on each
  shape. A reader that took one template per instrument, the way the client's inline road does,
  would fill both pairs from one shape, and the two rows below read the difference in both
  directions.

  EVERY FETCHED FILE IS WEIGHED. The settings record's digest for a pack is the SHA-256 of that
  pack's manifest, and the manifest carries the SHA-256 of every other file in it. So a tampered
  shard is refused with both digests named, and the crossing glides.

  THE FOUR RED-ON-BUG PROOFS serve a CRIPPLED copy of one file — the reader, or the walk's own
  bundle — from the same root, take the same measurement, and pass when the answer MOVES. The file
  is set aside as a copy first and restored from that copy afterwards, never by a git command.
"""
import base64
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame every pass suite measures on
DUR_MS = 6500              # the pass this pack's scores run for
PIN_AT = 2.5               # the instant the two roads are photographed at

CLIENT = (ROOT / "engine" / "client" / "01a-pass.js").read_text(encoding="utf-8")
READER_SRC = (ROOT / "engine" / "assets" / "pass-reader.js").read_text(encoding="utf-8")

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ================================================================= the synthetic pack
# Written by the same rule lab/build-delivery-v1.py writes the shipped one by, stated here in full
# rather than imported, because the site tree is read-only source material and a suite that could
# only run beside it would prove nothing on its own.
#
#   head.json        {schema, shapes: [...], worksWithARow, rowShape, rowsLiveIn}
#   templates.json   {<shape>: {slots: [[path, ...], ...], score: {...}}}
#   rows/<X>.json    {"<a>__<b>__<ab|ba>": [shape index, one value per slot in slot order]}
#   authored.json    {"<a>__<b>": a whole score, standing as authored}
#   manifest.json    the index: every file's bytes and SHA-256. Its own SHA-256 is the pack digest,
#                    and the settings record carries it.


def dumps(obj):
    """The pack's own serialisation: sorted keys, no spaces — what makes two builds byte-equal."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def weave_score(strips, seed, duration=DUR_MS, intent="the band family, one cue"):
    """A ONE-CUE SCORE the woven instrument can actually draw, of the shape §4.4 states — the same
    cue tests/test_pass_stack.py plays, with the two numbers this suite varies left open."""
    def static(v):
        return {"op": "static", "value": v}
    res = {v: {"bytesEstimate": 0, "framebuffers": 0, "passes": 1, "pingPong": 0, "programs": 1,
               "textureSlots": 2, "textures": 0, "variant": v}
           for v in ("lean", "standard", "rich")}
    return {
        "schema": 2, "duration": duration, "direction": "a-to-b", "failLand": "arrive",
        "seed": 1.983657397, "pair": {"a": "a", "b": "b"}, "intent": intent,
        "interruption": {"resolve": "nearest-door", "withinMs": 500},
        "camera": {"owner": "stage", "rests": "b",
                   "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0, "pitch": 0,
                              "yaw": 0, "roll": 0, "fov": None, "owner": "stage"}]},
        "cues": [{
            "id": "pivot", "instrument": {"api": 1, "id": "weave"},
            "voice": "letter", "roles": ["surface", "breath"],
            "levels": ["SURFACE"], "levelOwnership": {"SURFACE": "owns"},
            "window": [0.0, duration / 1000.0], "works": ["a", "b"], "stack": 0,
            "cameraAuthority": "stage",
            "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                      "out": {"handle": "mix", "value": 1, "measured": True}},
            "nodes": {"pivot-mix": {"source": "cueProgress"}, "pivot-clock": {"source": "time"},
                      "pivot-strips": static(strips), "pivot-axis": static(2),
                      "pivot-speed": static(1), "pivot-seed": static(seed),
                      "pivot-nMul": static(1), "pivot-press": static(1)},
            "tracks": {"mix": {"node": "pivot-mix"}, "clock": {"node": "pivot-clock"},
                       "strips": {"node": "pivot-strips"}, "axis": {"node": "pivot-axis"},
                       "speed": {"node": "pivot-speed"}, "seed": {"node": "pivot-seed"},
                       "nMul": {"node": "pivot-nMul"}, "press": {"node": "pivot-press"}},
            "resources": res,
        }],
    }


# THE TWO SHAPES. They differ in the score they carry — a different band count, a different seed and
# a different duration — so a template picked by anything other than the row's own first entry draws
# a different picture and reads a different duration.
SHAPES = ["p-weave-three", "p-weave-eight"]
SHAPE_SCORE = {"p-weave-three": weave_score(3, 1.9837, DUR_MS, "three bands"),
               "p-weave-eight": weave_score(8, 4.2211, 3000, "eight bands")}
# The slots each shape's template leaves open, as paths into its own score. The pair's two ids are
# slots for the same reason the shipped pack makes them slots: they differ from pair to pair.
SLOTS = [["pair", "a"], ["pair", "b"], ["cues", 0, "nodes", "pivot-seed", "value"]]


def pack_score(shape, a, b, seed):
    s = json.loads(json.dumps(SHAPE_SCORE[shape]))
    s["pair"] = {"a": a, "b": b}
    s["cues"][0]["nodes"]["pivot-seed"]["value"] = seed
    return s


def write_pack(root, base, rows_by_work, authored=None, tamper=None, drop=None):
    """One pack of static files under `root/base`, with its manifest and its own digest.

    `tamper` names a file whose bytes are changed AFTER the manifest weighed them — a stale file
    answering at a fresh address, which is the one thing the digest chain exists to catch. `drop`
    names a file the manifest carries and the server does not serve."""
    d = root / base
    (d / "rows").mkdir(parents=True, exist_ok=True)
    templates = {name: {"slots": [list(p) for p in SLOTS],
                        "score": json.loads(json.dumps(SHAPE_SCORE[name]))}
                 for name in SHAPE_SCORE}
    head = {"schema": 1, "shapes": list(SHAPES),
            "worksWithARow": sorted(rows_by_work),
            "rowShape": "the shape first, indexing `shapes`, then one value per slot in slot order",
            "rowsLiveIn": "one file per departing work under rows/, named <departing work id>.json"}
    files = {"head.json": dumps(head), "templates.json": dumps(templates),
             "authored.json": dumps(authored or {})}
    for work, rows in rows_by_work.items():
        files["rows/%s.json" % work] = dumps(rows)
    manifest = {
        "schema": 1, "pack": "synthPlans", "version": 2,
        "holds": "a serialised score per ordered pair, one template per passage shape",
        "shardKey": "departing work id", "rowKey": "<a>__<b>__<ab|ba>",
        "counts": {"orderedPairsWithARow": sum(len(r) for r in rows_by_work.values()),
                   "shards": len(rows_by_work)},
        "files": {rel: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                  for rel, data in files.items()},
        "worksWithAShard": sorted(rows_by_work),
    }
    manifest_bytes = dumps(manifest)
    for rel, data in files.items():
        if rel == drop:
            continue
        if rel == tamper:
            data = data + b" "        # the same document, other bytes: a stale file at a fresh address
        (d / rel).write_bytes(data)
    (d / "manifest.json").write_bytes(manifest_bytes)
    return {"version": 2, "base": base, "digest": "sha256:" + hashlib.sha256(manifest_bytes).hexdigest(),
            "manifest": "manifest.json", "templates": "templates.json", "head": "head.json",
            "rows": "rows/{departing}.json", "authored": "authored.json",
            "holds": "the synthetic pack this suite drives the reader with"}


# ================================================================= the string rows
check("PASS-READER the bundle carries the door and the reader travels in its own file",
      'PASS_PACK_SRC = "pass-reader.js"' in CLIENT and "passPack.scoreFor(key)" in CLIENT
      and "passWarm(el)" in CLIENT
      and "sha256" not in CLIENT and "manifest.json" not in CLIENT
      and "shapes" not in CLIENT,
      "the bundle names the reader's address, asks it one synchronous question inside passScoreFor "
      "and warms at the landing; the fetch, the digest chain, the shape lookup and the fill are "
      "words that appear nowhere in it")

check("PASS-READER the reader asks for nothing while a crossing is being declared",
      "function scoreFor" in READER_SRC
      and "fetch(" not in READER_SRC.split("function scoreFor")[1].split("function warm")[0],
      "scoreFor reads what has already arrived; every fetch this file makes is reached from warm, "
      "which the walk calls when it LANDS on a work")

_lit = re.search(r"PASS_LIMITS\s*=\s*\{[^}]*\bbytes:\s*(\d+)", CLIENT)
check("PASS-READER the score fence is an observed baseline of 12 288 B with its evidence beside it",
      _lit is not None and int(_lit.group(1)) == 12288
      and "10 851 B" in CLIENT and "7708" in CLIENT and "23.1 percent" in CLIENT,
      "the literal reads %s, and the lines above it name the pack it was measured on, that pack's "
      "longest filled score and the share the old 8192 B refused"
      % (_lit and _lit.group(1)))

check("PASS-READER a score refused for its weight names the weight it was measured at",
      'why: "weighs " + bytes + " bytes, over the " + PASS_LIMITS.bytes' in CLIENT,
      "a reason that gave only the fence left the one number its author has to act on unsaid")

# ================================================================= the bake
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}
TMP = Path(tempfile.mkdtemp(prefix="synth_passreader_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
SERVED = json.loads((TMP / "config.json").read_text(encoding="utf-8"))

check("PASS-READER the bake serves the reader beside the host",
      (TMP / "pass-reader.js").exists()
      and "@@NS@@" not in (TMP / "pass-reader.js").read_text(encoding="utf-8"),
      "pass-reader.js is written by the same road pass-layer.js is, with the namespace resolved")

_caps = (SERVED.get("pass") or {}).get("capabilities") or {}
check("PASS-READER the bake publishes the client's own fence as a capability the site can read",
      _caps.get("scoreBytes") == 12288 and _lit is not None
      and _caps["scoreBytes"] == int(_lit.group(1)),
      "config.json carries pass.capabilities=%s, read OUT of the served client rather than restated "
      "— the composer measures a filled score against the number the client applies" % _caps)

# ================================================================= the browser rows
ROWS = [
    "PASS-READER a crossing takes its score from the pack, fetched at the landing before it",
    "PASS-READER the row's own shape picks its template, and a second row on the same shard picks "
    "the other",
    "PASS-READER the filled score is the pack's own score, to the last leaf",
    "PASS-READER only the works the walk landed on were ever asked for on the wire",
    "PASS-READER a landing that arrives while the pack is still opening is held, never dropped",
    "PASS-READER a missing shard glides, with the server's own answer on the diagnostic surface",
    "PASS-READER a tampered shard is refused with both digests, and the crossing glides",
    "PASS-READER a score over the fence is refused with the size it was measured at",
    "PASS-READER a pack-served score draws the same frame as the same score served inline",
]
RED = [
    "PASS-READER red-on-bug · the digest comparison removed: the tampered shard is taken",
    "PASS-READER red-on-bug · the refusal note removed: the missing shard glides in silence",
    "PASS-READER red-on-bug · the fence raised: the over-weight score is taken",
    "PASS-READER red-on-bug · the shape index ignored: the pack road stops matching the inline one",
]


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return str(path)


def same_bytes(p, q):
    return Path(p).read_bytes() == Path(q).read_bytes()


if not chrome_available():
    for r in ROWS + RED:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    SHOTS = TMP / "shots"
    SHOTS.mkdir(exist_ok=True)

    def enter(br, base):
        if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
            br.click(".exd-window", settle=1.4)
        for _ in range(25):
            if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                           "&& !document.documentElement.classList.contains('ex-face'))") == "true":
                break
            br.sleep(0.2)
        br.sleep(0.4)
        br.key("ArrowDown")           # the one step that makes the client fetch pass-layer.js
        for _ in range(30):
            if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
                # ...and one step back, so the visitor's remembered place stands where it did.
                # Every round below re-enters the walk, and a place that crept forward each time
                # would hang a different cast for every row.
                br.key("ArrowUp")
                br.sleep(1.2)         # the reader is fetched at the landing; let it land
                return True
            br.sleep(0.2)
        return False

    def cast(br):
        return js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                      ".map(function(e){return e.dataset.id;});")

    def settings(packs=None, scores=None):
        cfg = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
        cfg["pass"].pop("packs", None)
        cfg["pass"].pop("scores", None)
        if packs:
            cfg["pass"]["packs"] = packs
        if scores:
            cfg["pass"]["scores"] = scores
        (TMP / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2,
                                                    sort_keys=True) + "\n", encoding="utf-8")

    def declare(br, a, b, cause):
        # A step already in flight is ended first, so what this row measures is its OWN declare and
        # never a crossing the walk's entry started a moment earlier.
        js(br, "window.__exPass.adapter.interrupt('row-reset'); return {};")
        br.sleep(0.2)
        return js(br, """
          var A = document.querySelector('.exh-frame[data-id="%s"]');
          var B = document.querySelector('.exh-frame[data-id="%s"]');
          var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                     kind:'step', cause:'%s', velocity:0});
          window.__rcmd = cmd;
          var rep = window.__exPass.report();
          return {got: !!cmd, score: cmd ? cmd.score : null,
                  refusals: rep.refusals.filter(function(x){ return x.what === 'pack'; }),
                  cast: [].slice.call(document.querySelectorAll('.exh-frame'))
                          .map(function(e){ return e.dataset.id; }).slice(0, 3),
                  pack: rep.pack};
        """ % (a, b, cause))

    def shot(br, name):
        """One instant of the pass, held and photographed on the walk's own road."""
        js(br, """
          window.__exPass.host.configure({prepareBudgetMs: 400, settleSlackMs: 2000,
            fixedScale: true, clockPin: %f, progressPin: %f});
          window.__rtook = window.__exPass.layer().offer(window.__rcmd, {
            dock: function(){}, glide: function(){ window.__rglide = true; },
            curtain: function(){}, mark: function(){}}) === true;
          return {took: window.__rtook};
        """ % (PIN_AT, PIN_AT / (DUR_MS / 1000.0)))
        br.sleep(1.2)
        out = png(br, SHOTS / (name + ".png"))
        js(br, "window.__exPass.adapter.interrupt('bench'); "
               "window.__exPass.host.configure({clockPin:null, progressPin:null}); return {};")
        br.sleep(0.4)
        return out

    with serve(TMP) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.navigate(base + "/")
            br.sleep(0.8)
            armed = enter(br, base)
            WORKS = cast(br)

            if not armed or len(WORKS) < 3:
                for r in ROWS + RED:
                    skip(r, f"the walk never registered a host, or hung fewer than three works: "
                            f"armed={armed} works={WORKS}")
            else:
                A, B, C = WORKS[0], WORKS[1], WORKS[2]
                KEY_AB = A + "__" + B
                # ONE SHARD, TWO ROWS, TWO SHAPES. w→next stands on the second shape and w→the work
                # after it on the first; the composer's own tagged key carries one and the reversed
                # «ba» form the other, so both roads into a shard are walked. A pair is written for
                # every consecutive triple the walk hangs, so a cast that re-hangs from another work
                # still meets a pack built for it.
                SEED_AB, SEED_AC = 7.7701, 3.3302
                ROWS_BY_WORK = {}
                for _i in range(len(WORKS) - 2):
                    _a, _b, _c = WORKS[_i], WORKS[_i + 1], WORKS[_i + 2]
                    ROWS_BY_WORK[_a] = {_a + "__" + _b + "__ab": [1, _a, _b, SEED_AB],
                                        _c + "__" + _a + "__ba": [0, _a, _c, SEED_AC]}
                WANT_AB = pack_score(SHAPES[1], A, B, SEED_AB)
                WANT_AC = pack_score(SHAPES[0], A, C, SEED_AC)
                PACK_BASE = "plans/v2-synthetic/"

                def stand(rows=None, tamper=None, drop=None, authored=None):
                    """The pack as this row wants it served, and the settings record naming it."""
                    shutil.rmtree(TMP / "plans", ignore_errors=True)
                    entry = write_pack(TMP, PACK_BASE,
                                       rows if rows is not None else ROWS_BY_WORK,
                                       authored=authored, tamper=tamper, drop=drop)
                    settings(packs={"synthPlans": entry})
                    return entry

                # ---- the road as it stands --------------------------------------------------
                stand()
                br.navigate(base + "/")
                br.sleep(0.9)
                ok = enter(br, base)
                r = declare(br, A, B, "pack-road")
                took = ok and r["got"] and r["score"] is not None
                check(ROWS[0],
                      took and r["score"]["schema"] == 2
                      and r["score"]["cues"][0]["instrument"]["id"] == "weave"
                      and r["score"]["pair"] == {"a": A, "b": B},
                      "the command froze a score of schema %s naming «%s» for the pair %s; the "
                      "reader's own record reads %s"
                      % (r["score"] and r["score"]["schema"],
                         r["score"] and r["score"]["cues"][0]["instrument"]["id"],
                         r["score"] and r["score"]["pair"], json.dumps(r["pack"])[:400]))

                r2 = declare(br, A, C, "pack-road-2")
                got_ab = r["score"] or {}
                got_ac = r2["score"] or {}
                # A→B's row opens with 1, so it names SHAPES[1] — the eight-band, 3000 ms score.
                # A→C's row opens with 0 and names SHAPES[0], the three-band 6500 ms one. One shard,
                # two rows, two templates.
                check(ROWS[1],
                      got_ab.get("duration") == 3000 and got_ac.get("duration") == DUR_MS
                      and got_ab.get("intent") == "eight bands"
                      and got_ac.get("intent") == "three bands"
                      and got_ab["cues"][0]["nodes"]["pivot-strips"]["value"] == 8
                      and got_ac["cues"][0]["nodes"]["pivot-strips"]["value"] == 3,
                      "A→B's row opens with 1 and filled the eight-band template's own %s ms "
                      "score; A→C's row opens with 0 and filled the three-band template's %s ms "
                      "score — two rows of one shard, two templates. The shipped pack carries "
                      "twenty-five, and one template per instrument cannot tell these two apart"
                      % (got_ab.get("duration"), got_ac.get("duration")))

                check(ROWS[2], got_ab == WANT_AB and got_ac == WANT_AC,
                      "each filled score equals the pack's own score for that pair to the last "
                      "leaf — the three slots the template leaves open (both ids and the cue's "
                      "seed) are written at their own paths and nothing else moves"
                      if got_ab == WANT_AB and got_ac == WANT_AC else
                      "A→B differs: %s" % json.dumps({k: [got_ab.get(k), WANT_AB.get(k)]
                                                      for k in set(WANT_AB) | set(got_ab)
                                                      if got_ab.get(k) != WANT_AB.get(k)})[:500])

                asked = [s["work"] for p in r2["pack"].get("packs", []) for s in p["shards"]]
                landed = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame.seen'))"
                                ".map(function(e){return e.dataset.id;});")
                check(ROWS[3],
                      bool(asked) and A in asked and C not in asked,
                      "the reader asked for %d shard(s) — %s — and the walk has landed on %s. The "
                      "shard for the DEPARTING work is what a crossing needs, and it is asked for "
                      "when the walk lands on that work, never when it leaves it: passScoreFor "
                      "answers inside declare and a fetch begun there could not arrive in time"
                      % (len(asked), asked, landed))

                # ---- several landings inside one open ---------------------------------------
                # THE FIRST LANDING OF A VISIT OPENS THE PACK, and the walk can land again — a
                # restored place, a step taken while the head is still crossing the wire — before
                # that open has finished. Those are exactly the shards a visitor needs first. A
                # fresh reader is built here and handed three works at once, which is that race
                # stated plainly, and all three shards must arrive.
                three = [w for w in (A, B, C) if w in ROWS_BY_WORK]
                js(br, """
                  window.__mk = null;
                  window.__exPassReader = function (p) { window.__mk = p; };
                  var s = document.createElement('script');
                  s.src = 'pass-reader.js';
                  document.head.appendChild(s);
                  return {};
                """)
                for _ in range(40):
                    if br.evaluate("String(!!window.__mk)") == "true":
                        break
                    br.sleep(0.2)
                js(br, """
                  window.__rd = window.__mk.make({packs: %s, note: function(){}});
                  %s
                  return {};
                """ % (json.dumps({"synthPlans": json.loads(json.dumps(
                          json.loads((TMP / "config.json").read_text())["pass"]["packs"]
                          ["synthPlans"]))}),
                       "".join("window.__rd.warm(%s);" % json.dumps(w) for w in three)))
                states = None
                for _ in range(40):
                    rep = js(br, "return window.__rd.report();")
                    states = {s["work"]: s["state"] for s in rep["packs"][0]["shards"]}
                    if states and all(v != "asked" for v in states.values()):
                        break
                    br.sleep(0.25)
                check(ROWS[4],
                      len(three) >= 2 and len(states or {}) == len(three)
                      and all(states[w] == "read" for w in three),
                      "three works were handed to a reader in one breath, before its pack had "
                      "finished opening, and every shard arrived: %s. Held in a queue that the "
                      "open flushes either way, so a landing during the open is answered rather "
                      "than lost — which is the state the first landing of every visit is in"
                      % json.dumps(states))

                # ---- a missing shard --------------------------------------------------------
                stand(drop="rows/%s.json" % A)
                br.navigate(base + "/")
                br.sleep(0.9)
                enter(br, base)
                r = declare(br, A, B, "missing-shard")
                whys = " | ".join(x["why"] for x in r["refusals"])
                check(ROWS[5],
                      r["got"] and r["score"] is None and "404" in whys,
                      "the manifest names the shard and the server does not serve it: the command "
                      "carries no score, so the walk's own glide lands the step, and the surface "
                      "reads «%s»" % whys[:300])

                # ---- a tampered shard -------------------------------------------------------
                stand(tamper="rows/%s.json" % A)
                br.navigate(base + "/")
                br.sleep(0.9)
                enter(br, base)
                r = declare(br, A, B, "tampered-shard")
                whys = " | ".join(x["why"] for x in r["refusals"])
                check(ROWS[6],
                      r["got"] and r["score"] is None and "weigh" in whys and "manifest" in whys,
                      "the shard's bytes changed after the manifest weighed them, so it is refused "
                      "unread and the crossing glides: «%s»" % whys[:300])

                # ---- a score over the fence -------------------------------------------------
                # The over-weight score is served as an AUTHORED score, so what is measured is the
                # client's own fence over a whole score rather than a fill that went wrong.
                heavy = weave_score(3, 1.9837, DUR_MS, "x" * 380)
                heavy["provenance"] = {"pad": ["y" * 190 for _ in range(70)]}
                heavy["pair"] = {"a": A, "b": B}
                # Weighed the way passScoreCheck weighs it — the browser's own JSON.stringify —
                # rather than by a second serialiser that writes 0.0 where the first writes 0.
                heavy_bytes = js(br, "return {n: JSON.stringify(%s).length};"
                                     % json.dumps(heavy))["n"]
                stand(authored={KEY_AB: heavy})
                br.navigate(base + "/")
                br.sleep(0.9)
                enter(br, base)
                r = declare(br, A, B, "over-fence")
                said = js(br, "return window.__exPass.report().refusals.filter("
                              "function(x){ return x.what === 'score'; });")
                whys = " | ".join(str(x.get("why")) for x in said)
                check(ROWS[7],
                      r["got"] and r["score"] is None and str(heavy_bytes) in whys
                      and "12288" in whys,
                      "a score of %d B reached the client from the pack and was refused before any "
                      "instrument saw it, with its own weight in the reason: «%s»"
                      % (heavy_bytes, whys[:300]))

                # ---- the same score, two roads ---------------------------------------------
                stand()
                br.navigate(base + "/")
                br.sleep(0.9)
                enter(br, base)
                r = declare(br, A, B, "pixels-pack")
                from_pack = shot(br, "pack") if r["score"] else None

                settings(scores={KEY_AB: WANT_AB})
                br.navigate(base + "/")
                br.sleep(0.9)
                enter(br, base)
                r2 = declare(br, A, B, "pixels-inline")
                from_inline = shot(br, "inline") if r2["score"] else None
                if not from_pack or not from_inline:
                    check(ROWS[8], False,
                          "one of the two roads carried no score: pack=%s inline=%s"
                          % (bool(from_pack), bool(from_inline)))
                else:
                    check(ROWS[8], same_bytes(from_pack, from_inline),
                          "the pass held at %.2f s of %d ms, photographed on the walk's own road "
                          "with the score fetched from the pack and with the same score written "
                          "into the settings file: the two frames are byte-identical"
                          % (PIN_AT, DUR_MS)
                          if same_bytes(from_pack, from_inline) else
                          "the two frames differ, and the scores %s"
                          % ("agree" if r["score"] == r2["score"] else "differ too"))

                # ---- the red-on-bug proofs --------------------------------------------------
                # ONE FILE IS CRIPPLED AT A TIME, set aside as a copy first and restored from that
                # copy after, and the same measurement is taken. A proof passes when the answer
                # MOVES — which is what says the rule, and not something else, is holding the row.
                def crippled(path, replace_with, run):
                    aside = Path(str(path) + ".aside")
                    shutil.copy2(path, aside)
                    try:
                        Path(path).write_text(replace_with, encoding="utf-8")
                        br.navigate(base + "/")
                        br.sleep(0.9)
                        enter(br, base)
                        return run()
                    finally:
                        shutil.copy2(aside, path)
                        aside.unlink()

                READER = TMP / "pass-reader.js"
                BUNDLE = TMP / "exhibition.js"
                reader_txt = READER.read_text(encoding="utf-8")
                bundle_txt = BUNDLE.read_text(encoding="utf-8")

                RULE = "if (want && got !== want) {"
                if RULE not in reader_txt:
                    check(RED[0], False, "the digest rule's own text was not found in the served reader")
                else:
                    stand(tamper="rows/%s.json" % A)
                    hurt = reader_txt.replace(RULE, "if (false) {", 1)
                    got = crippled(READER, hurt, lambda: declare(br, A, B, "red-digest"))
                    check(RED[0], got["got"] and got["score"] is not None,
                          "with the comparison in place the tampered shard is refused unread and "
                          "the crossing glides; with `got !== want` never asked, the very same "
                          "bytes fill a score and the crossing takes it — so the row above is held "
                          "by the digest and by nothing else. Score seen: %s"
                          % (got["score"] or {}).get("intent"))

                NOTE = "note(name, why);"
                if NOTE not in reader_txt:
                    check(RED[1], False, "the note rule's own text was not found in the served reader")
                else:
                    stand(drop="rows/%s.json" % A)
                    hurt = reader_txt.replace(NOTE, "", 1)
                    got = crippled(READER, hurt, lambda: declare(br, A, B, "red-note"))
                    check(RED[1], got["got"] and got["score"] is None and not got["refusals"],
                          "with the note in place a missing shard glides AND says why; with the "
                          "note removed the same step still glides and the diagnostic surface "
                          "carries nothing at all — which is the silence this whole unit was sent "
                          "to end. Refusals seen: %s" % json.dumps(got["refusals"])[:200])

                FENCE = "bytes > PASS_LIMITS.bytes"
                if FENCE not in bundle_txt:
                    check(RED[2], False, "the fence's own text was not found in the served bundle")
                else:
                    stand(authored={KEY_AB: heavy})
                    hurt = bundle_txt.replace(FENCE, "false", 1)
                    got = crippled(BUNDLE, hurt, lambda: declare(br, A, B, "red-fence"))
                    check(RED[2], got["got"] and got["score"] is not None,
                          "with the fence in place a %d B score is refused with its weight named; "
                          "with the comparison removed the same score is taken whole — so the row "
                          "above is held by the fence at 12 288 B" % heavy_bytes)

                PICK = "var shape = pk.head.shapes[row[0]];"
                if PICK not in reader_txt:
                    check(RED[3], False, "the shape pick's own text was not found in the served reader")
                else:
                    stand()
                    hurt = reader_txt.replace(PICK, "var shape = pk.head.shapes[0];", 1)
                    def run_pick():
                        got = declare(br, A, B, "red-pick")
                        return got, (shot(br, "red-pick") if got["score"] else None)
                    got, frame = crippled(READER, hurt, run_pick)
                    check(RED[3],
                          got["score"] is not None and got["score"] != WANT_AB
                          and frame is not None and not same_bytes(frame, from_inline),
                          "with the row's own first entry read, A→B fills the shape it names and "
                          "draws the frame the inline road draws; with the index ignored and the "
                          "first template taken every time, the same pair fills a %s ms score and "
                          "the frame moves — twenty-five shapes ship, and one template per "
                          "instrument is what this proves the pack cannot use"
                          % (got["score"] or {}).get("duration"))

    shutil.rmtree(SHOTS, ignore_errors=True)

shutil.rmtree(TMP, ignore_errors=True)

# ================================================================= the verdict
for name, verdict, detail in results:
    print(f"[{verdict}] {name}" + (f"  — {detail}" if detail else ""))
_fail = sum(1 for _, v, _ in results if v == "FAIL")
_skip = sum(1 for _, v, _ in results if v == "SKIP")
print(f"\n{len(results)} rows: {len(results) - _fail - _skip} pass, {_fail} fail, {_skip} skip")
sys.exit(1 if _fail else 0)
