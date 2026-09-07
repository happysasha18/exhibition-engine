#!/usr/bin/env python3
"""S-115 stage 1 — the bench the arsenal audit stands on.

This module holds no assertion. It answers, by RUNNING rather than by reading source, the two
questions a browser cannot answer, and it hands the browser rows the material they need for the
other two:

  · WHAT THE CHOOSER CAN CAST. The real `engine/assets/pass-composer.js` is driven in node over the
    fixed synthetic corpus (`tests/synthetic_works.py`), across every route role the composer itself
    publishes and a stated span of seeds, and every instrument every request casts is recorded with
    the slot it was cast into.

  · WHAT IT WAS CAST WITH. For every casting, the composed cue's OWN nodes are read against that
    instrument's OWN published manifest — the shipped `engine/assets/pass-inst-<id>.js`, loaded and
    executed so its `def` is the value the file itself computes rather than a number scraped out of
    it. A handle that never leaves its own `def` across the whole passage is a handle that says
    nothing.

WHICH HANDLES COUNT AS A VOICE SAYING SOMETHING, AND THE BOUNDARY IS THE MANIFEST'S OWN.

  Every instrument declares a structural `level` per handle, and four names across the whole fleet
  declare `level: null` — `pass-inst-parquet.js` says why in its own words: "`mix` is the crossing's
  own dial, `seed` the score's die, and `shade`/`mask` are the fleet's judge channels ... all four
  are the passage's own idiom rather than a structural level". `clock` and `presence` carry the same
  null. So a handle with a level is this instrument's own contribution to the picture, and a handle
  without one is the passage's idiom that every cue drives whatever instrument stands in it.

  This matters because it is the difference between a real reading and a vacuous one. Every cue in
  the fleet drives `mix` from 0 to 1; counting that as "a non-neutral handle" would pass every
  instrument that was ever cast, which is exactly the claim the owner says is false. So the reading
  below asks only about handles that declare a level.

WHAT THE CORPUS IS AND WHAT IT IS NOT. `tests/synthetic_works.py`, unchanged and unread by anything
here except through its own `corpus()` and `pairs()`. Nothing in this file names a photograph, and
the size of the sweep is the corpus's own pair list times the composer's own route roles times the
seed span stated below — none of which grows when a photograph is added to the collection.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = Path(__file__).resolve().parent / "fixture_pass_composed.json"
CLIENT = ROOT / "engine" / "client" / "01a-pass.js"

# The two fences the client itself applies, read out of its own `PASS_LIMITS` literal rather than
# retyped — the same road `tests/test_pass_composed.py` already takes them by, and for the same
# reason: a composer measured against a number this file invented would be measured against nothing.
_LIMITS = re.search(r"PASS_LIMITS\s*=\s*\{([^}]*)\}", CLIENT.read_text(encoding="utf-8")).group(1)
CLIENT_INTENT = int(re.search(r"\bintent:\s*(\d+)", _LIMITS).group(1))
CLIENT_BYTES = int(re.search(r"\bbytes:\s*(\d+)", _LIMITS).group(1))

# THE SEED SPAN THIS AUDIT WALKS, STATED RATHER THAN IMPLIED. The span itself is the composer's own
# `seedSpan`, which it reads off `gears`' own `seed` handle — no number here. What this file chooses
# is the STEP it walks that span in, and it is a half step for one reason: a seed is a die, the
# chooser reads it at whatever resolution it likes, and the finer the walk the more of the arsenal a
# fleet-wide reachability claim has actually looked at. `tests/test_pass_seam.py` searched for its
# own real bundles in half steps for the same reason. Anything an instrument needs a finer die than
# this to be cast at all is, for this audit's purposes, a finding rather than a miss.
SEED_STEP = 0.5

# ---------------------------------------------------------------- the driver
# Run against a copy of the composer held in memory, exactly as `tests/test_pass_composed.py`'s own
# driver runs it: the module is the shipped file, its namespace resolved, joined through the same
# `window.__PassComposer` door the bake gives it. Every instrument file the engine ships is loaded
# the same way, through `window.__PassInstrument`, so the manifests read here are the ones the
# renderer itself will register rather than a copy frozen in a fixture.
DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm"), path = require("path");
const [modulePath, fixturePath, corpusPath] = process.argv.slice(2);
const CAPS = JSON.parse(process.env.CLIENT_CAPS || "{}");
const SEED_STEP = Number(process.env.SEED_STEP);

let source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
if (!joined) { console.log(JSON.stringify({error: "the composer joined nothing"})); process.exit(0); }

// THE ROSTER IS THE SHIPPED FILES, never a list typed here. An audit that walked a hand-kept list
// would go quiet the day an instrument is added, which is the one failure it exists to prevent.
const assetsDir = path.dirname(modulePath);
const live = {};
for (const f of fs.readdirSync(assetsDir).filter((n) => /^pass-inst-.*\.js$/.test(n))) {
  const isrc = fs.readFileSync(path.join(assetsDir, f), "utf8").replace(/@@NS@@/g, "");
  const sb = {window: {__PassInstrument: (r) => { live[r.instrument.name] = r.instrument.manifest; }},
              console, document: undefined};
  vm.createContext(sb);
  vm.runInContext(isrc, sb, {filename: f});
}
const ROSTER = Object.keys(live).sort();

const fix = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
// The client's own two fences, handed in for the reason test_pass_composed.py records: a fixture
// carrying no byte fence leaves `fitTheWeight` on its first line and the composer under test is
// never asked to fit, so the scores this audit reads would be scores no visitor is ever served.
fix.consts.intentFenceChars = CAPS.intent;
fix.consts.scoreFenceBytes = CAPS.bytes;
// And each handle's own declared level onto the fixture's copy of the manifests, by the same road
// and for the same reason: the level's one home is the instrument's own file.
for (const iid of ROSTER) {
  const theirs = live[iid].handles || {};
  const mine = (fix.consts.manifests[iid] || {}).handles || null;
  if (!mine) continue;
  for (const h of Object.keys(theirs)) if (mine[h]) mine[h].level = theirs[h].level;
}

const corpus = JSON.parse(fs.readFileSync(corpusPath, "utf8"));
const works = corpus.works;
const composer = joined.make(fix.consts);

// A node's value may be the module's own Flt wrapper ({v: <number>}) rather than a bare number —
// the composer prints a non-integer through it so the score keeps four decimals on the wire.
function toNum(v) { return (v && typeof v === "object" && "v" in v) ? Number(v.v) : Number(v); }

// EVERY VALUE A COMPOSED NODE CAN STAND AT ACROSS THE PASSAGE, and whether it travels at all. This
// is the whole of fact 2's arithmetic and it reads the score's own node shapes, nothing else: a
// static node stands at one value; a mix runs between its two ends; a spline visits its points; a
// map lands on its `to` pair; a clamp and a curve are the same question one node deeper; a node
// standing on a `source` is driven by the passage itself and therefore travels whatever it carries.
function reach(node, out) {
  out = out || {vals: [], travels: false};
  if (!node || typeof node !== "object") return out;
  if (node.source) { out.travels = true; return out; }
  if (node.op === "static") { out.vals.push(toNum(node.value)); return out; }
  if (node.op === "mix") { out.vals.push(toNum(node.a), toNum(node.b)); return reach(node.t, out); }
  if (node.op === "spline") {
    (node.points || []).forEach((p) => out.vals.push(toNum(p.value)));
    return reach(node["in"], out);
  }
  if (node.op === "map") {
    (node.to || []).forEach((v) => out.vals.push(toNum(v)));
    return reach(node["in"], out);
  }
  if (node.op === "clamp" || node.op === "curve" || node["in"]) return reach(node["in"], out);
  if ("value" in node) { out.vals.push(toNum(node.value)); return out; }
  return out;
}

// One composed cue, read against its own instrument's published manifest.
function readCue(cue) {
  const iid = (cue.instrument || {}).id;
  const man = (live[iid] || {}).handles || {};
  const driven = {}, moved = [], idle = [], undeclared = [];
  for (const h of Object.keys(cue.tracks || {})) {
    const spec = man[h];
    if (!spec) { undeclared.push(h); continue; }
    const node = (cue.nodes || {})[(cue.tracks[h] || {}).node];
    const level = spec.level === undefined ? null : spec.level;
    const r = reach(node);
    const def = Number(spec.def);
    const away = r.vals.some((v) => v === v && Math.abs(v - def) > 0);
    driven[h] = {level: level, def: def, vals: r.vals.slice(0, 4), travels: r.travels,
                 away: away, node: (cue.tracks[h] || {}).node};
    if (level) ((away || r.travels) ? moved : idle).push(h);
  }
  return {iid: iid, id: cue.id, stack: cue.stack, window: [toNum(cue.window[0]), toNum(cue.window[1])],
          levels: cue.levels, voice: cue.voice, driven: driven, moved: moved, idle: idle,
          undeclared: undeclared, levelled: moved.length + idle.length};
}

const SEEDS = [];
for (let s = composer.seedSpan[0]; s <= composer.seedSpan[1] + 1e-9; s += SEED_STEP) {
  SEEDS.push(Math.round(s / SEED_STEP) * SEED_STEP);
}
const ROLES = composer.routeRoles;
const PAIRS = corpus.pairs;

const seen = {};        // iid -> what the sweep saw of it
const reps = {};        // iid -> a casting fit to photograph: driven, and live at the passage's peak
const repsAny = {};     // iid -> the first casting at all, so an instrument with no fit rep still says why
const idleReps = {};    // iid -> the first casting whose every levelled handle stood at its own def
let polyRep = null, camRep = null, declined = 0, tried = 0;

function camMoves(camera) {
  return ((camera || {}).track || []).some((pt) =>
    Math.abs(toNum(pt.logScale) || 0) > 0 || Math.abs(toNum(pt.pitch) || 0) > 0
    || Math.abs(toNum(pt.roll) || 0) > 0 || Math.abs(toNum(pt.yaw) || 0) > 0
    || Math.abs(toNum((pt.pan || {}).x) || 0) > 0 || Math.abs(toNum((pt.pan || {}).y) || 0) > 0);
}

for (const [a, b, dir] of PAIRS) {
  for (const role of ROLES) {
    for (const seed of SEEDS) {
      tried++;
      let p;
      try {
        p = composer.passageFor({workRecordA: works[a], workRecordB: works[b], direction: dir,
                                 seed: seed, routeRole: role});
      } catch (e) { declined++; continue; }
      if (!p || !p.score) { declined++; continue; }
      const sc = p.score;
      const durSec = Number(sc.duration) / 1000;
      // THE PASSAGE'S OWN PEAK, taken from the composer's own `motionPeak` rather than from a share
      // of the travel this file chose. It is the instant the score's own driven handles are moving
      // hardest, which is where fact 4 photographs.
      const peak = composer.motionPeak(sc.cues || [], durSec);
      const req = {a: a, b: b, dir: dir, role: role, seed: seed, dur: durSec,
                   peakAt: peak.at, peakShare: peak.share, peakFlat: !!peak.flat};
      const cues = (sc.cues || []).map(readCue);
      // A CAMERA-LED PASSAGE THE ROW CAN ACTUALLY ISOLATE. The track has to move, and every cue in
      // it has to leave the camera to the STAGE: a cue holding its own camera authority moves the
      // picture from inside the instrument, so flattening the stage's track would not be the same
      // score with the camera standing still, and the row would be reading something else.
      if (!camRep && camMoves(sc.camera)
          && (sc.cues || []).every((c) => c.cameraAuthority === "stage")) {
        camRep = {req: req, json: p.json, cues: cues, camera: sc.camera};
      }
      // A REAL BUNDLE FOR THE POLYPHONY ROWS: three voices, every one of them standing on the frame
      // at the peak the score's own motion names, so "each voice has a visible contribution" is a
      // question that can be asked of one photograph rather than of three separate passages.
      if (!polyRep && cues.length >= 3
          && cues.every((c) => c.window[0] <= peak.at && peak.at <= c.window[1] && c.moved.length)) {
        polyRep = {req: req, json: p.json, cues: cues};
      }
      for (const c of cues) {
        const s = seen[c.iid] || (seen[c.iid] = {casts: 0, moved: 0, idle: 0, bare: 0, slots: {},
                                                 roles: {}, undeclared: {}});
        s.casts++;
        s.slots[c.stack] = (s.slots[c.stack] || 0) + 1;
        s.roles[role] = (s.roles[role] || 0) + 1;
        if (c.moved.length) s.moved++; else s.idle++;
        // A casting that drove no levelled handle AT ALL is a different silence from one that drove
        // them and left every one at its own default, and the row that reds on either says which.
        if (!c.levelled) s.bare++;
        c.undeclared.forEach((h) => { s.undeclared[h] = (s.undeclared[h] || 0) + 1; });
        if (!repsAny[c.iid]) repsAny[c.iid] = {req: req, cue: c, json: p.json};
        if (!idleReps[c.iid] && !c.moved.length) idleReps[c.iid] = {req: req, cue: c};
        if (!reps[c.iid] && c.moved.length
            && c.window[0] <= peak.at && peak.at <= c.window[1]) {
          reps[c.iid] = {req: req, cue: c, json: p.json};
        }
      }
    }
  }
}

console.log(JSON.stringify({
  version: joined.version, roster: ROSTER, seeds: SEEDS, roles: ROLES,
  pairs: PAIRS.length, tried: tried, declined: declined,
  seen: seen, reps: reps, repsAny: repsAny, idleReps: idleReps,
  polyRep: polyRep, camRep: camRep,
  manifests: ROSTER.reduce((o, i) => { o[i] = live[i].handles; return o; }, {}),
}));
"""


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


def survey(corpus_path, timeout=900):
    """Drive the real composer over the synthetic corpus and hand back what it cast, with what."""
    tmp = Path(tempfile.mkdtemp(prefix="synth_arsenal_"))
    driver = tmp / "arsenal-driver.js"
    driver.write_text(DRIVER, encoding="utf-8")
    env = dict(os.environ, SEED_STEP=str(SEED_STEP),
               CLIENT_CAPS=json.dumps({"intent": CLIENT_INTENT, "bytes": CLIENT_BYTES}))
    proc = subprocess.run(["node", str(driver), str(MODULE), str(FIXTURE), str(corpus_path)],
                          capture_output=True, text=True, env=env, timeout=timeout)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-400:]}
    return json.loads(proc.stdout.strip().splitlines()[-1])


# ---------------------------------------------------------------- the neutral counterpart

def neutralise(score, iid, manifests, cue_id=None):
    """The same score with one instrument's own driven, levelled handles forced to the neutral its
    own manifest publishes — and nothing else touched.

    This is fact 4's control, and its whole worth is that it changes ONE thing. The windows, the
    stack, the doors, the camera, the duration and every other voice stand exactly as composed, so
    the two passages draw the same number of calls in the same order at the same instant. What
    differs is the value of this instrument's own handles, which is the thing being asked about.

    The rewrite points each such handle's track at a fresh static node rather than editing the node
    it already names, so a node another handle reads as its input cannot be changed underneath it.
    """
    out = deepcopy(score)
    touched = []
    for cue in out.get("cues", []):
        if (cue.get("instrument") or {}).get("id") != iid:
            continue
        if cue_id is not None and cue.get("id") != cue_id:
            continue
        man = (manifests.get(iid) or {})
        for h in sorted(cue.get("tracks") or {}):
            spec = man.get(h)
            if not spec or not spec.get("level"):
                continue           # the passage's own idiom, not this instrument's own voice
            name = "%s-neutral-%s" % (cue.get("id"), h)
            cue.setdefault("nodes", {})[name] = {"op": "static", "value": spec.get("def")}
            cue["tracks"][h] = {"node": name}
            touched.append("%s.%s→%s" % (cue.get("id"), h, spec.get("def")))
    return out, touched


def flatten_camera(score):
    """The same score with the camera's own track flattened — every pose at rest, nothing else
    touched. The camera is one transform the host lays over whatever the instruments drew, so a
    flattened track is the picture those same instruments drew with the camera standing still."""
    out = deepcopy(score)
    cam = out.get("camera") or {}
    track = cam.get("track") or []
    for pt in track:
        pt["logScale"] = 0
        pt["pitch"] = 0
        pt["roll"] = 0
        pt["yaw"] = 0
        pt["fov"] = None
        if isinstance(pt.get("pan"), dict):
            pt["pan"] = {"x": 0, "y": 0}
    return out, len(track)


# ---------------------------------------------------------------- the pixel predicate
# TAKEN WHOLE FROM `tests/test_pass_seam.py`, not re-invented. That file argues the bound from the
# mechanism and the argument is unchanged here: the only thing a lawful redraw of one picture may
# change is the resampling, every resampling filter writes an output pixel as a weighted average of
# the input pixels around it, and an average lies between the smallest and the largest of them. So a
# pixel is lawful when it falls inside the range its own 3x3 neighbourhood spanned on the other
# side, either direction may be the resampled one, and what is reported is the EXCESS in the
# picture's own 0-255 units. Two renderings of one picture read zero; a picture that became another
# picture does not.
#
# It is copied rather than imported for one reason and it is not laziness: importing
# `tests/test_pass_seam.py` would RUN its whole suite, browser and all, as a side effect of the
# import. The functions below are byte-for-byte its own.

def arr(path):
    from PIL import Image
    import numpy as np
    return np.asarray(Image.open(path).convert("RGB")).astype(np.int16)


def _band(x):
    """The range each pixel's own 3x3 neighbourhood spans, per channel."""
    import numpy as np
    h, w, _ = x.shape
    pad = np.pad(x, ((1, 1), (1, 1), (0, 0)), mode="edge")
    views = [pad[dy:dy + h, dx:dx + w] for dy in (0, 1, 2) for dx in (0, 1, 2)]
    return np.minimum.reduce(views), np.maximum.reduce(views)


def _excess(a, b):
    import numpy as np
    lo, hi = _band(a)
    return np.maximum(np.maximum(b - hi, lo - b), 0)


def resample_excess(pa, pb):
    import numpy as np
    a, b = arr(pa), arr(pb)
    if a.shape != b.shape:
        return {"worst": 255, "share": 1.0, "mean": 255.0, "why": f"{a.shape} vs {b.shape}"}
    e = np.minimum(_excess(a, b), _excess(b, a))
    return {"worst": int(e.max()), "share": round(float((e.max(axis=2) > 0).mean()), 6),
            "mean": round(float(e.mean()), 6), "why": None}


def crop_of(path, box, scale, inset=2):
    """Both shots cropped to the same region in shot pixels. The inset drops the outermost ring of
    the rect, where the renderer's own sample and the browser's image scaler read half a point
    differently and nothing about the gesture is said."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    x0 = int(round(box["x"] * scale)) + inset
    y0 = int(round(box["y"] * scale)) + inset
    x1 = int(round((box["x"] + box["w"]) * scale)) - inset
    y1 = int(round((box["y"] + box["h"]) * scale)) - inset
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(im.size[0], x1), min(im.size[1], y1)
    if x1 - x0 < 4 or y1 - y0 < 4:
        return None
    return im.crop((x0, y0, x1, y1))


def cropped_excess(pa, pb, box, scale, shots, tag):
    """The predicate, applied over the region the renderer claims."""
    ca, cb = crop_of(pa, box, scale), crop_of(pb, box, scale)
    if ca is None or cb is None:
        return {"worst": 255, "share": 1.0, "mean": 255.0, "why": "the claimed rect is too small"}
    a_p, b_p = Path(shots) / (tag + "-a.png"), Path(shots) / (tag + "-b.png")
    ca.save(a_p)
    cb.save(b_p)
    out = resample_excess(a_p, b_p)
    out["size"] = ca.size
    return out


# ---------------------------------------------------------------- browser plumbing
# Also taken from `tests/test_pass_seam.py`, for the same reason and with one addition of this
# file's own: `stack_at`, which reads each voice's own handles and the instrument's own applied row
# off the host's report, because that is the one place the runtime publishes what it received.

import base64  # noqa: E402 — beside the plumbing it belongs to rather than at the top

HOOKS = """window.HOOKS = function () {
  var A = window.__exPass.adapter;
  return { dock: A.dock, glide: A.glide, curtain: A.curtain, mark: A.mark,
           hangGeometry: A.hangGeometry, handoff: A.handoff };
};
0"""


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return str(path)


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def canvas_box(br):
    return js(br, "var c=document.querySelector('canvas');"
                  "if(!c) return null;"
                  "var b=c.getBoundingClientRect();"
                  "return {x:b.left, y:b.top, w:b.width, h:b.height,"
                  " iw:innerWidth, ih:innerHeight, vis:c.style.visibility};")


def shot_scale(br, path):
    from PIL import Image
    return Image.open(path).size[0] / float(br.evaluate("String(innerWidth)"))


def wait_state(br, want, tries=60, nap=0.1):
    for _ in range(tries):
        if js(br, "return window.__exPass.host.report().state;") == want:
            return True
        br.sleep(nap)
    return False


def enter(br):
    if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
        br.click(".exd-window", settle=1.4)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)
    br.key("ArrowDown")
    for _ in range(30):
        if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
            br.evaluate(HOOKS)
            return True
        br.sleep(0.2)
    return False


def rest_revealed(br, a, tries=40, nap=0.1):
    """Wait until the resting work's own reveal has finished — the picture stands at full strength.
    A row comparing pixels against a half-faded photograph would be reading the fade."""
    for _ in range(tries):
        op = js(br, "var I=document.querySelector('.exh-frame[data-id=\"%s\"] img.work');"
                    "return I ? Number(getComputedStyle(I).opacity) : 1;" % a)
        if op >= 0.999:
            return True
        br.sleep(nap)
    return False


def rest_at(br, a):
    """The walk put back on the departing work, its picture centred in the frame, nothing in flight
    and the reveal finished. Without the scroll the work hangs off the top of the viewport and the
    rect the renderer claims lies outside the shot entirely."""
    js(br, "window.__exPass.adapter.interrupt('arsenal-rest'); return null;")
    wait_state(br, "idle")
    for _ in range(10):
        js(br, "var A=document.querySelector('.exh-frame[data-id=\"%s\"]');"
               "A.classList.add('seen');"
               "scrollTo(0, Math.round(scrollY + A.getBoundingClientRect().top"
               " + (A.getBoundingClientRect().height - innerHeight)/2)); return null;" % a)
        br.sleep(0.35)
        top = float(js(br, "return document.querySelector('.exh-frame[data-id=\"%s\"]')"
                           ".getBoundingClientRect().top;" % a))
        if abs(top) < 3:
            return rest_revealed(br, a)
    return False


def pin(br, seconds, progress):
    br.evaluate("window.__exPass.host.configure({clockPin:%r, progressPin:%r}); 0"
                % (seconds, progress))


def offer(br, a, b, cause, sc):
    return js(br, """
      window.__arsenalScore = %s;
      var A = document.querySelector('.exh-frame[data-id="%s"]');
      var B = document.querySelector('.exh-frame[data-id="%s"]');
      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                 kind:'step', cause:'%s', velocity:0,
                                                 score: window.__arsenalScore});
      window.__cmd = cmd;
      var took = cmd ? window.__exPass.layer().offer(cmd, window.HOOKS()) : false;
      return {got: !!cmd, took: took, gen: cmd ? cmd.gen : null};
    """ % (json.dumps(sc), a, b, cause))


def stack_at(br):
    """WHAT THE RUNTIME ITSELF SAYS IT RECEIVED, at the frame it last drew.

    `handles` is what the HOST resolved for that voice and handed down — and it is built by walking
    the INSTRUMENT'S OWN MANIFEST (`handlesOf`, engine/assets/pass-layer.js), so a handle the score
    drives that the instrument does not declare never appears here at all, and a track the host
    could not evaluate is replaced by the manifest's own `def` and logged as `handle-fallback`.
    Those two are exactly what "the handle never reached the renderer" looks like from outside.

    `applied` beside it is the INSTRUMENT'S own published reading of its door on the buffer it drew
    on. It is reported here as evidence and asserted on nowhere: an instrument publishes it at its
    doors, so at the middle of a passage it is legitimately empty.

    EVERY EVENT COMES BACK WITH THE GENERATION THAT LOGGED IT, and the caller keeps only its own.
    The host's `log` is one 128-row ring for the whole visit (engine/assets/pass-layer.js), not a
    per-passage list, so a fallback from a passage three rows ago is sitting in it. A reader that
    took the ring whole would hang one passage's fault on the next one that happened to ask.
    """
    return js(br, "var r = window.__exPass.host.report();"
                  "return {state: r.state, live: r.live, drew: r.drew,"
                  " stack: (r.stack||[]).map(function(s){return {id: s.id,"
                  "   instrument: s.instrument, stack: s.stack, live: !!s.live,"
                  "   window: s.window, handles: s.handles, applied: s.applied};}),"
                  " fallbacks: r.events.filter(function(e){return e.name === 'handle-fallback';})"
                  "   .map(function(e){return {gen: e.gen, why: e.why};}),"
                  " shed: r.events.filter(function(e){"
                  "   return e.name === 'voice-shed' || e.name === 'score-shed'"
                  "       || e.name === 'no-instrument' || e.name === 'plan-lightened';})"
                  "   .map(function(e){return {gen: e.gen, why: e.name + ': ' + e.why};}),"
                  " last: r.events.slice(-6).map(function(e){return e.name + ': ' + e.why;})};")


# ---------------------------------------------------------------- the one bounded audit command
# HIS WORD OF 07.09.2026 11:00. This harness is allowed to be ONE bounded audit command with a saved
# result, and no more: its job is to NAME the instruments that are genuinely unreachable or neutral,
# and it does not replace looking at the screen. It is not a verification framework, it does not
# sweep production pairs, and it is not worth a day.
#
# The bound is the corpus's own: a fixed set of constructed records and pair cases that does not grow
# with the collection, walked once. The result is written where a person and a later run can both
# read it, so the answer is looked up rather than recomputed.
#
#   python3 tests/arsenal_truth.py            → writes tests/arsenal_truth.json and prints the names
#
# The suite `tests/test_pass_route_direction.py` is the other reader of the same harness, and it is
# the one that holds the standing verdict. This entry exists so a person can ask the question in one
# command without driving a browser at all: facts 1 and 2 alone already name the unreachable and the
# neutral, which is exactly what he asked this file to be for.
if __name__ == "__main__":
    import tempfile as _tf
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import synthetic_works as _sw

    _out = Path(__file__).resolve().parent / "arsenal_truth.json"
    _dir = Path(_tf.mkdtemp(prefix="arsenal_truth_"))
    _corpus = _dir / "synthetic-works.json"
    _corpus.write_text(json.dumps({"works": _sw.corpus(), "pairs": _sw.pairs()}), encoding="utf-8")
    if not node_available():
        print("node is not installed, so this command cannot ask the composer anything")
        raise SystemExit(2)
    _s = survey(_corpus)
    if _s.get("error"):
        print("the composer would not load: " + _s["error"])
        raise SystemExit(2)

    # THE FIELD NAMES ARE THE NODE SIDE'S OWN (`seen[iid]` above): `casts` how many requests cast it,
    # `moved` how many of those drove a levelled handle away from its own default, `idle` how many did
    # not, and `bare` how many drove no levelled handle at all. Read here rather than renamed, so one
    # vocabulary crosses the whole harness.
    _rows = _s.get("seen") or {}
    _roster = _s.get("roster") or sorted(_rows)
    _never = sorted(i for i in _roster if not (_rows.get(i) or {}).get("casts"))
    _idle = sorted((i for i in _roster if (_rows.get(i) or {}).get("idle")),
                   key=lambda i: -_rows[i]["idle"])
    _out.write_text(json.dumps({"tried": _s.get("tried"), "declined": _s.get("declined"),
                                "seeds": _s.get("seeds"), "roles": _s.get("roles"),
                                "pairs": _s.get("pairs"), "version": _s.get("version"),
                                "seen": _rows}, indent=2, sort_keys=True) + "\n")
    print(f"{_s.get('tried')} requests over the constructed corpus "
          f"({_s.get('pairs')} pair cases x {len(_s.get('roles') or [])} roles x "
          f"{len(_s.get('seeds') or [])} seeds), {_s.get('declined')} declined")
    print("never cast at all: " + (", ".join(_never) if _never else "none — every instrument is "
                                                                    "reachable"))
    print("cast with every levelled handle at its own default, at least once:")
    for i in _idle:
        r = _rows[i]
        print(f"  {i}: {r['idle']} of {r['casts']} castings"
              + (f", of which {r['bare']} drive no levelled handle at all" if r.get("bare") else ""))
    if not _idle:
        print("  none")
    print(f"\nwritten to {_out}")
    shutil.rmtree(_dir, ignore_errors=True)
