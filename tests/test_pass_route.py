#!/usr/bin/env python3
"""EX-ROUTE — the walk's own dramaturgy: what a step of the route is FOR, and how it is read.
Run: python3 tests/test_pass_route.py

Root: charter shelf 15 (`lab/CROSSING-BRIEF.md` in the tlvphotos tree) — the route's roles are
entrance, quiet link, middle, culmination and return, mapped onto a harmonic grammar of a home the
eye settles in, a motion away that prepares, and a tension that demands resolution, with a dynamics
curve of about 70 parts quiet, 25 middle and 5 culmination across a walk. Unit brief:
docs/immersive/briefs/2026-08-17-U27-composed-full-route.md, stage 2, and his 18:43 formulation of
the full route — 10 works, extendable twice by 5, every edge composed.

WHAT THIS MEASURES.

  The route is the walk itself. `SPREAD`, `UNFOLD` and `MAXU` are settings this shell already had —
  10, 5 and 2 — so the 10+5+5 route is the product's own shape and nothing was invented to carry it.

  The function of a step is READ, not typed. The hang is already ordered by kinship: `arcOrder`
  draws the near neighbours in and then widens its steps on purpose, so the distance the route
  crosses at each step is a number the walk has already measured. Every role below comes off that
  curve by shelf 15's grammar — the widest step is the crest, the step that leads into it prepares
  it, a step standing above both its neighbours is a motion away, and everything else is a home the
  eye settles in.

  Two roles outrank the curve because they are facts about the VISIT rather than about the route's
  shape: an edge this visit has already walked is a return (which is the same edge §4.8's return
  reference crosses on), and the visit's first crossing is an entrance.

  The role reaches the composer. It is put on the passage request at one place, and the composer's
  own reading of the request echoes it, so what the walk authored is what the passage was bounded by.

WHAT EVERY ROW HERE IS ANCHORED TO. Three things, and no fourth.

  1. THE WALK'S OWN SETTINGS AND THE COMPOSER'S OWN FENCE. The route's length is read from the
     bundle's own `spread_size` / `unfold_step` / `max_unfolds` lines, and the five role names from
     the composer's own `routeRoles`. Neither is typed twice here.

  2. THE RULE, RE-DERIVED AND COMPARED. The role rows recompute shelf 15's grammar in Python from
     the gaps the walk publishes and compare it against the roles the walk published beside them.
     A change to the curve moves both sides together, so these never re-base on a change of content;
     they redden only when the walk stops reading the grammar it says it reads.

  3. NOTHING — a measured reading, printed so a person can read the number. The realised dynamics
     share is one of these: it is the outcome of the grammar over one dealt hang, not a quota, and
     the walk deals a different hang every visit.

WHAT IS NEVER RESTORED FROM GIT. Every red-on-bug row below serves a COPY of the built bundle with
one rule put back the way it stood. The source tree is never written to; the copy lives in the
temporary bake this suite serves and is restored byte for byte afterwards.
"""
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
FIXTURE = Path(__file__).resolve().parent / "fixture_pass_composed.json"
CLIENT = ROOT / "engine" / "assets" / "exhibition.js"
COMPOSER = ROOT / "engine" / "assets" / "pass-composer.js"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


TMP = Path(tempfile.mkdtemp(prefix="synth_route_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
SRC = (ROOT / "engine" / "client" / "01a-pass.js").read_text(encoding="utf-8")
BUNDLE = (TMP / "exhibition.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- the route is the walk's own shape
# The three numbers are read out of the bundle's own knob lines rather than restated: a route of ten
# extendable twice by five is what this shell already builds, and the unit's own 10+5+5 is that.
KNOB = {name: re.search(r"const %s = clampInt\(EX\.(\w+), (\d+), " % name, BUNDLE)
        for name in ("SPREAD", "UNFOLD", "MAXU")}
check("EX-ROUTE the route is the walk's own 10+5+5 — the hang's spread, its unfold step and how "
      "many unfolds it allows, each read off the shell's own settings",
      all(KNOB.values())
      and KNOB["SPREAD"].group(2) == "10" and KNOB["SPREAD"].group(1) == "spread_size"
      and KNOB["UNFOLD"].group(2) == "5" and KNOB["UNFOLD"].group(1) == "unfold_step"
      and KNOB["MAXU"].group(2) == "2" and KNOB["MAXU"].group(1) == "max_unfolds"
      and "const CAP = SPREAD + MAXU * UNFOLD;" in BUNDLE,
      "spread=%s unfold=%s unfolds=%s, so the route runs to %s works and %s steps"
      % (KNOB["SPREAD"].group(2) if KNOB["SPREAD"] else "?",
         KNOB["UNFOLD"].group(2) if KNOB["UNFOLD"] else "?",
         KNOB["MAXU"].group(2) if KNOB["MAXU"] else "?",
         10 + 2 * 5, 10 + 2 * 5 - 1))

# ---------------------------------------------------------------- one home for the five names
COMPOSER_ROLES = re.search(r'var ROUTE_ROLES = \[([^\]]+)\]', COMPOSER.read_text(encoding="utf-8"))
FENCED = set(re.findall(r'"([^"]+)"', COMPOSER_ROLES.group(1))) if COMPOSER_ROLES else set()
ROUTE_BLOCK = SRC[SRC.index("let passRouteAt = null;"):SRC.index("// THE PASSAGE REQUEST")]
SAID = set(re.findall(r'"(entrance|quiet link|middle|culmination|return)"', ROUTE_BLOCK))
check("EX-ROUTE the five functions the walk can state are exactly the five the composer fences on",
      bool(FENCED) and SAID == FENCED,
      "the walk states %s; the composer accepts %s" % (sorted(SAID), sorted(FENCED)))

# ---------------------------------------------------------------- one place writes the role
check("EX-ROUTE the role is derived in one place and put on the request in one place",
      SRC.count("function passRouteRole(") == 1
      and SRC.count("req.routeRole = role") == 1
      and SRC.count("routeRole") == 2,
      "passRouteRole is declared %d time(s) and the request is written %d time(s)"
      % (SRC.count("function passRouteRole("), SRC.count("req.routeRole = role")))

# ---------------------------------------------------------------- the browser rows
BROWSER_ROWS = [
    "EX-ROUTE every step of the hung route carries a function, read off the walk's own kinship gaps "
    "by shelf 15's grammar",
    "EX-ROUTE the route's realised dynamics: one crest, and the home the eye settles in carries the "
    "largest share",
    "EX-ROUTE the walk's authored role reaches the composer, and the composer's own reading of the "
    "request echoes it",
    "EX-ROUTE a route's steps do not all read alike — the functions of one hang are several",
    "EX-ROUTE the visit's FIRST crossing is an entrance, and the crossing after it is not",
    "EX-ROUTE an edge this visit has already walked asks as a RETURN, and the return reference of "
    "§4.8 crosses on that same step",
    "EX-ROUTE a step between two works that do not stand next to each other states no function, and "
    "the composer's own default stands",
    "EX-ROUTE «ещё 5» lengthens the route and the functions are re-read on the longer curve",
    "EX-ROUTE red-on-bug · the crest rule reverted: the route carries no culmination at all",
    "EX-ROUTE red-on-bug · the local-widening rule reverted: every motion away collapses",
    "EX-ROUTE red-on-bug · the return rule reverted: a walked-back edge stops asking as a return",
    "EX-ROUTE red-on-bug · the entrance rule reverted: the visit's first crossing is not an entrance",
]


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


# EX-PASS-RECORDS (2026-08-19): `pass.works` left config.json — the site now carries `pass.records`
# (a route + a cap) and the id → record map is answered over that route instead, the way a Cloudflare
# Worker answers it in production (engine/assets/worker.js's `passRecordsRoute`). This suite serves
# the same contract locally through the harness's `answer` hook (tests/headless_harness.py's `serve`,
# threaded through by tests/headless.py) — RECORDS_STORE is filled by `put_records` below and read by
# `records_answer`, a MUTABLE dict shared by both so a hook bound into `serve(...)` before any id is
# known still sees records `put_records` writes afterward.
RECORDS_ROUTE = "/api/pass/records"
RECORDS_CAP = 20   # spread_size 10 + max_unfolds 2 × unfold_step 5 — the built-in defaults (build.py)
RECORDS_STORE = {}


def records_answer(raw_path):
    """The harness's `answer` hook for this suite: answers `GET /api/pass/records?ids=...` the way
    the Worker does — over-cap or empty is refused with 400, an id `RECORDS_STORE` does not carry is
    simply left out of the answer."""
    if not raw_path.startswith(RECORDS_ROUTE):
        return None
    ids = [i for i in parse_qs(urlparse(raw_path).query).get("ids", [""])[0].split(",") if i]
    if not ids or len(ids) > RECORDS_CAP:
        return (400, "text/plain", "bad request")
    out = {i: RECORDS_STORE[i] for i in ids if i in RECORDS_STORE}
    return (200, "application/json", json.dumps({"records": out}))


def put_records(base_dir, ids):
    """The settings record as the site writes it for the composed road. The fixture's two records
    are re-keyed onto the works this bake hangs — what the composer reads is measurement, and the id
    is only its name."""
    cfg = json.loads((base_dir / "config.json").read_text(encoding="utf-8"))
    fix = json.loads(FIXTURE.read_text(encoding="utf-8"))
    src = [fix["works"][fix["pair"]["a"]], fix["works"][fix["pair"]["b"]]]
    works = {}
    for i, wid in enumerate(ids):
        rec = json.loads(json.dumps(src[i % 2]))
        rec["id"] = wid
        works[wid] = rec
    RECORDS_STORE.update(works)
    cfg["pass"] = dict(cfg.get("pass") or {}, visualLayer="pass", composer=fix["consts"],
                       records={"route": RECORDS_ROUTE, "cap": RECORDS_CAP})
    (base_dir / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return works


# The picture layer of this suite. A record is written only for a passage that actually DREW, and
# what says one drew is the host's own report; a stub host stands in for the renderer so the route's
# returns are measured on every machine and not only on one with a working WebGL2 context.
STUB = """
  if (!window.__exPassLayer) return {no: true};
  window.__exPassLayer({
    offer: function () { return true; },
    report: function () { return {active: false, instrument: 'stub',
                                  census: {buffer: '800x600', dpr: 1},
                                  stack: [{id: 'pivot', instrument: 'stub', handles: {}}]}; },
    cancel: function () {}, resize: function () {}
  });
  return {no: false};
"""

DECLARE = """
  var A = document.querySelector('.exh-frame[data-id="%s"]');
  var B = document.querySelector('.exh-frame[data-id="%s"]');
  if (!A || !B) return {absent: true};
  var req = window.__exPass.request(A, B);
  var cmd = window.__exPass.adapter.declare({fromEl: A, toEl: B, dir: %s, span: 100,
                                             kind: 'step', cause: 'route', velocity: 0});
  window.__cmd = cmd;
  var rows = window.__exPass.report().composer.passages;
  var row = rows.length ? rows[rows.length - 1] : null;
  var no = window.__exPass.report().refusals.filter(function (x) { return x.what === 'declare'; });
  return {absent: false, got: !!cmd, hasScore: !!(cmd && cmd.score),
          asked: req ? (req.routeRole === undefined ? null : req.routeRole) : null,
          crossed: req ? (req.sessionMemory || null) : null,
          read: row && row.request ? row.request.routeRole : null,
          key: row ? row.key : null, declined: row ? row.declined : null,
          noWhy: no.length ? no[no.length - 1].why : null};
"""

LAND = """
  var cmd = window.__cmd;
  if (!cmd) return {no: true};
  window.__exPass.adapter.dock(cmd);
  var r = window.__exPass.report();
  return {no: false, edges: r.memory.edges.length, opened: r.route.opened};
"""


def declare(br, a, b, direction=1):
    """One step declared programmatically. Two declares inside one animation frame are refused by
    law (§1.1), and a headless browser can hold a frame open far longer than a person's hand does,
    so a refusal for that one reason is waited out rather than read as an answer."""
    got = {}
    for _ in range(10):
        got = js(br, DECLARE % (a, b, direction))
        if got.get("absent") or got.get("got") or "one frame" not in (got.get("noWhy") or ""):
            return got
        br.sleep(0.3)
    return got


def enter(br, base, pass_arg="diagnostics:on,familySeed:4242", clear=True):
    br.navigate(base + "/")
    if clear:
        br.clear_storage()
    br.navigate(base + "/" + ("?pass=" + pass_arg if pass_arg else ""))
    br.sleep(0.8)
    if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
        try:
            br.click(".exd-window", settle=1.4)
        except RuntimeError:
            br.sleep(1.0)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)
    # The engine's own file arrives at the walk's LANDING (§4.4d), with no crossing needed. The
    # PICTURE layer's door opens elsewhere — at the first real step — so one real step is taken
    # here, and it is the visit's own first crossing. That crossing is what the entrance row reads,
    # off the passage record the walk keeps, rather than a declare made afterwards: a declare made
    # afterwards would be the SECOND crossing and would read the curve instead of the opening.
    # AND THE RECORDS THE STEP WILL NEED (2026-08-19). Since they arrive with the selection rather
    # than inside the settings block, «the composer has landed» no longer means «a crossing can be
    # composed»: the wave is a request of its own and can still be in flight. A step taken before it
    # lands plays the walk's own glide and composes nothing, which for this suite would silently move
    # the visit's opening onto the NEXT step.
    #
    # THE TWO FACTS ARE WAITED ON TOGETHER, NOT ONE NESTED INSIDE THE OTHER (2026-08-19, same-day
    # fix). The composer's own script and the first record wave are two independent async arrivals
    # with no order between them — nothing in the client ever makes one wait on the other. The first
    # shape of this wait nested the records check inside the composer-state check, so a composer
    # slow to arrive (this suite's own Chrome under load, a cold fetch) let the OUTER loop exhaust
    # its budget and fall through in silence: ArrowDown then fired with `passComposer` still null,
    # `passComposeFor` refused before ever building a request, and the visit's real first crossing
    # composed nothing — the entrance role this file's rows read off `composer.passages[0]` was
    # never written, and every row downstream that assumed it was read a later crossing as if it
    # were the first. Reading both facts on every tick, until both hold, closes that gap: a slow
    # composer is waited out rather than raced past. The budget (150 ticks, 30s) is generous against
    # this suite's own launch of a fresh Chrome for every row: a script fetch racing page-load work
    # under a loaded machine is exactly the case this wait exists for.
    for _ in range(150):
        got = js(br, "var r = window.__exPass.report();"
                     "return {st: r.composer.state, held: r.records.held};")
        if got.get("st") == "read" and (got.get("held") or 0) > 1:
            break
        br.sleep(0.2)
    br.key("ArrowDown")
    for _ in range(30):
        if br.evaluate("String(!!window.__exPassLayer)") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.6)
    js(br, STUB)


def grammar(gaps):
    """Shelf 15's grammar, re-derived here from the gaps the walk publishes. The row compares this
    against the roles the walk published beside them, so both sides move together when the hang
    moves and the row goes on measuring the same claim."""
    # The search for the widest step begins AFTER the route's first, which shelf 15 gives to the
    # entrance; a one-step route keeps its only step.
    crest = max(range(1 if len(gaps) > 1 else 0, len(gaps)), key=lambda i: (gaps[i], -i))
    out = []
    for i, g in enumerate(gaps):
        if i == crest:
            out.append("culmination")
        elif i == crest - 1:
            out.append("middle")
        else:
            before = gaps[i - 1] if i > 0 else float("-inf")
            after = gaps[i + 1] if i + 1 < len(gaps) else float("-inf")
            out.append("middle" if (g > before and g > after) else "quiet link")
    return out


# The plants: one rule of the derivation put back the way it stood, in a COPY of the bundle the
# browser is served. Each names the line it reverts and what that line was for.
PLANTS = {
    "crest": ('if (i === crest) return "culmination";',
              'if (false) return "culmination";'),
    "widening": ('return (g > before && g > after) ? "middle" : "quiet link";',
                 'return "quiet link";'),
    "return": ('if (edge && edge.passes > 0) return "return";',
               'if (false) return "return";'),
    "entrance": ('if (!passVisitOpened()) return "entrance";',
                 'if (false) return "entrance";'),
}
SERVED = TMP / "exhibition.js"
ORIGINAL = SERVED.read_text(encoding="utf-8")


def plant(name):
    was, now = PLANTS[name]
    if ORIGINAL.count(was) != 1:
        return False
    SERVED.write_text(ORIGINAL.replace(was, now), encoding="utf-8")
    return True


def unplant():
    SERVED.write_text(ORIGINAL, encoding="utf-8")


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP, answer=records_answer) as base:
        with Browser(width=1280, height=900) as br:
            # EVERY WORK OF THE CATALOGUE IS GIVEN A RECORD, not only the ten this entry hung: the
            # walk deals its works afresh on every entry, so a record set built from one hang would
            # leave the next hang's works unrecorded and every request would answer nothing.
            everyone = [w["id"] for w in json.loads(
                (TMP / "exhibition_data.json").read_text(encoding="utf-8"))["works"]]
            put_records(TMP, everyone)
            enter(br, base)

            shape = js(br, "return window.__exPass.report().route;")
            ids = shape.get("ids") or []

            # 0 · the curve names every step
            want = grammar(shape["gaps"]) if shape.get("gaps") else []
            check(BROWSER_ROWS[0],
                  bool(want) and want == shape["roles"] and len(shape["roles"]) == len(ids) - 1,
                  "%d works, %d steps; gaps %s; the walk reads %s and shelf 15's grammar over those "
                  "same gaps reads %s; the crest stands at step %s"
                  % (shape["works"], shape["steps"], shape["gaps"], shape["roles"], want,
                     (shape["crest"] or 0) + 1))

            # 1 · the realised dynamics
            share = shape.get("share") or {}
            n = max(1, shape.get("steps") or 1)
            check(BROWSER_ROWS[1],
                  share.get("culmination") == 1
                  and share.get("quiet link", 0) >= share.get("middle", 0),
                  "over %d steps: %d quiet (%.0f%%), %d middle (%.0f%%), %d culmination (%.0f%%) — "
                  "the outcome of the grammar over one dealt hang, against shelf 15's ~70/25/5"
                  % (n, share.get("quiet link", 0), 100.0 * share.get("quiet link", 0) / n,
                     share.get("middle", 0), 100.0 * share.get("middle", 0) / n,
                     share.get("culmination", 0), 100.0 * share.get("culmination", 0) / n))

            # 2 · the role reaches the composer. The visit's first crossing is the real step
            # `enter` took, and it is an entrance by the rule above; the step measured here is the
            # SECOND, where the curve is what answers.
            first = js(br, "var rows = window.__exPass.report().composer.passages;"
                           "var row = rows.length ? rows[0] : null;"
                           "return {absent: !row,"
                           " asked: row && row.request ? row.request.routeRole : null,"
                           " crossed: row && row.request ? (row.request.sessionMemory || null)"
                           "          : null};")
            second = declare(br, ids[1], ids[2]) if len(ids) > 2 else {"absent": True}
            check(BROWSER_ROWS[2],
                  not second.get("absent") and second.get("asked") == shape["roles"][1]
                  and second.get("read") == second.get("asked"),
                  "the walk asked for «%s» on step 2 and the composer read «%s»; the curve names "
                  "«%s» there" % (second.get("asked"), second.get("read"),
                                  shape["roles"][1] if len(shape["roles"]) > 1 else "?"))

            # 3 · the steps of one route do not all read alike
            kinds = sorted(set(shape["roles"]))
            check(BROWSER_ROWS[3], len(kinds) >= 2,
                  "the route's %d steps carry %d different functions: %s"
                  % (shape["steps"], len(kinds), kinds))

            # 4 · the entrance is the first crossing and only the first
            check(BROWSER_ROWS[4],
                  first.get("asked") == "entrance" and second.get("asked") != "entrance",
                  "the visit's first crossing asked «%s» and the one after it «%s»"
                  % (first.get("asked"), second.get("asked")))

            # 5 · a walked-back edge is a return, and the reference crosses on it
            js(br, LAND)
            back = declare(br, ids[2], ids[1], direction=-1) if len(ids) > 2 else {"absent": True}
            js(br, LAND)
            check(BROWSER_ROWS[5],
                  back.get("asked") == "return" and bool(back.get("crossed"))
                  and sorted((back.get("crossed") or {}).keys()) == ["family", "passIndex", "seed"],
                  "walking the same edge back asked «%s» and carried %s"
                  % (back.get("asked"), back.get("crossed")))

            # 6 · a step off the route's own thread states no function
            off = declare(br, ids[0], ids[len(ids) - 1]) if len(ids) > 3 else {"absent": True}
            check(BROWSER_ROWS[6],
                  off.get("asked") is None and off.get("read") == "middle",
                  "a step between two works standing %d apart in the hang asked «%s», and the "
                  "composer read «%s»" % (len(ids) - 1, off.get("asked"), off.get("read")))

            # 7 · the unfold lengthens the route
            grew = js(br, "var b = document.getElementById('ex-unfold');"
                          "if (b) b.click();"
                          "return {clicked: !!b};")
            br.sleep(1.0)
            longer = js(br, "return window.__exPass.report().route;")
            check(BROWSER_ROWS[7],
                  grew["clicked"] and longer["steps"] > shape["steps"]
                  and longer["roles"] == grammar(longer["gaps"]),
                  "«ещё 5» took the route from %d steps to %d, and the grammar over the longer "
                  "curve reads the walk's own roles back: %s"
                  % (shape["steps"], longer["steps"], longer["share"]))

            # ---- the four red-on-bug rows, each on a COPY of the served bundle ----
            for row, name, want_of in (
                    (8, "crest", "culmination"),
                    (9, "widening", "middle")):
                if not plant(name):
                    check(BROWSER_ROWS[row], False,
                          "the line this plant reverts stands %d time(s) in the served bundle"
                          % ORIGINAL.count(PLANTS[name][0]))
                    continue
                enter(br, base)
                planted = js(br, "return window.__exPass.report().route;")
                unplant()
                enter(br, base)
                stands = js(br, "return window.__exPass.report().route;")
                # THE FLOOR EACH PLANT LEAVES BEHIND. Reverting the crest rule leaves no culmination
                # at all. Reverting the local-widening rule leaves exactly the one middle the crest's
                # own preparation is, since that line is a separate rule and this plant does not
                # touch it — so the row measures the collapse rather than an emptying.
                floor = 0 if name == "crest" else (1 if (planted["crest"] or 0) > 0 else 0)
                check(BROWSER_ROWS[row],
                      (planted["share"].get(want_of, 0) == floor
                       and stands["share"].get(want_of, 0) > floor),
                      "with the rule reverted the route carries %d step(s) of «%s» (%s), which is "
                      "the %d the other rules still name; with it standing it carries %d (%s)"
                      % (planted["share"].get(want_of, 0), want_of, planted["share"], floor,
                         stands["share"].get(want_of, 0), stands["share"]))

            # the return rule
            if plant("return"):
                enter(br, base)
                ids2 = js(br, "return window.__exPass.report().route.ids;")
                declare(br, ids2[1], ids2[2])
                js(br, LAND)
                planted_back = declare(br, ids2[2], ids2[1], direction=-1)
                unplant()
                check(BROWSER_ROWS[10],
                      planted_back.get("asked") != "return" and back.get("asked") == "return",
                      "with the rule reverted a walked-back edge asks «%s»; with it standing it "
                      "asks «%s»" % (planted_back.get("asked"), back.get("asked")))
            else:
                check(BROWSER_ROWS[10], False, "the return line was not found in the served bundle")

            # the entrance rule
            if plant("entrance"):
                enter(br, base)
                planted_first = js(br, "var rows = window.__exPass.report().composer.passages;"
                                       "var row = rows.length ? rows[0] : null;"
                                       "return {asked: row && row.request"
                                       "        ? row.request.routeRole : null};")
                unplant()
                check(BROWSER_ROWS[11],
                      planted_first.get("asked") != "entrance"
                      and first.get("asked") == "entrance",
                      "with the rule reverted the visit's first crossing asks «%s»; with it "
                      "standing it asks «%s»" % (planted_first.get("asked"), first.get("asked")))
            else:
                check(BROWSER_ROWS[11], False, "the entrance line was not found in the served bundle")

shutil.rmtree(TMP, ignore_errors=True)

print()
for name, verdict, detail in results:
    print("[%s] %s%s" % (verdict, name, ("  — " + detail) if detail else ""))
n_pass = sum(1 for r in results if r[1] == "PASS")
n_fail = sum(1 for r in results if r[1] == "FAIL")
n_skip = sum(1 for r in results if r[1] == "SKIP")
print("\n%d rows: %d pass, %d fail, %d skip" % (len(results), n_pass, n_fail, n_skip))
sys.exit(1 if n_fail else 0)
