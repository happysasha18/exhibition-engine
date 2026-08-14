#!/usr/bin/env python3
"""PASS-API-V1 — the boundary between the engine's host and the artistic instruments.
Run: python3 tests/test_pass_pack.py

Root: his word of 2026-08-14 08:39 — the engine knows no TLV effect name and loads a version-pinned
opaque effect pack; tlvphotos owns the artistic instruments and their manifests.

WHAT THIS SUITE IS FOR. Until 2026-08-14 the instruments lived inside the engine's own renderer
file. The byte fence on that file broke three times in one morning, each time for the same reason:
an instrument had landed, and a fence sized for the host was being asked to answer for the picture.
The instruments left for one pack that morning, and the same failure arrived again by lunchtime: a
fourth instrument landed, the pack measured 53 732 B raw against a 38 000 B fence, and no fourth
instrument of that family fitted at any size. A fence over a bag of instruments says the bag is too
heavy and names no instrument.

SO EACH INSTRUMENT NOW TRAVELS AS ITS OWN FILE, and a visit fetches only the ones its own score
names. The host is told nothing at bake: it reads the instrument names out of the score's cues and
the addresses, versions and digests out of the SITE'S OWN SETTINGS RECORD — the same record that
already carries the score tables and the score templates. One instrument, one file, one fence.

THE ROW THAT IS THE WHOLE POINT is the first one below: the BUILT host is grepped for every
instrument name that ships today, and it reds on any of them. A boundary nobody can check is a
boundary that drifts, and this row is what makes «the engine knows no effect name» a fact about the
artifact rather than an intention about the code.

WHAT IS NEVER RESTORED FROM GIT. Every red-on-bug proof below copies the artifact into a bench root
of its own and cripples that copy. The source tree is never written to, and no run of this file asks
git to restore anything.
"""
import hashlib
import json
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
VW, VH = 390, 844

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passpack_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")

# THE SITE'S OWN RECORD, as the bake wrote it, and the built file each entry names. The names are
# read out of the record rather than written into this file, so a fifth instrument landing tomorrow
# is covered by every row below without anyone remembering to add it here.
RECORD = (json.loads((TMP / "config.json").read_text(encoding="utf-8")).get("pass") or {})
RECORD = RECORD.get("instruments") or {}
NAMES = sorted(RECORD)
BUILT = {n: (TMP / RECORD[n]["src"]).read_text(encoding="utf-8") for n in NAMES}
BYTES = {n: (TMP / RECORD[n]["src"]).read_bytes() for n in NAMES}
SOURCE = {n: (ROOT / "engine" / "assets" / RECORD[n]["src"]) for n in NAMES}


# ---------------------------------------------------------------- string rows

# ================================================================================================
# THE BOUNDARY ROW. Everything else in this file is about how the instruments travel; this is about
# what the host is allowed to know. It reads the BUILT artifact — the comment-stripped file a visitor
# downloads — so it judges code and cannot be tripped either way by prose that merely names an
# instrument. The emptiness guard keeps it from passing on nothing.
# ================================================================================================
def host_names(text):
    return sorted(set(re.findall("|".join(NAMES), text))) if NAMES else []


check("PASS-PACK the host knows no instrument name — the built host names none of them",
      len(LAYER) > 1000 and len(NAMES) >= 3 and not host_names(LAYER),
      "the engine reads the names out of a score and the addresses out of the site's own record, "
      "and registers whatever arrives by the name each manifest carries. The %d shipping today are "
      "%s, and the built host (%d characters) names %s"
      % (len(NAMES), NAMES, len(LAYER), host_names(LAYER) or "none of them"))

# THE HOST IS TOLD NOTHING AT BAKE. Until this afternoon the build stamped one address, one version
# and one digest into the host. With a file per instrument there is nothing to stamp: an address
# stamped into the host would be an instrument the engine knows, which the row above forbids.
check("PASS-PACK the built host carries no instrument address, version or digest of its own",
      not re.search(r"pass-inst-|pass-pack", LAYER)
      and not re.search(r"[0-9a-f]{64}", LAYER)
      and "@@" not in LAYER
      and 'RECORD_SRC = "config.json"' in LAYER,
      "the host holds one address — the site's own settings file — and reads every instrument "
      "address, version and digest out of the record it finds there. Nothing about any instrument "
      "is baked into it, and no bake token is left standing in it")

check("PASS-PACK the site's record names every instrument the bake served, with its own three facts",
      bool(NAMES)
      and all(RECORD[n]["src"] == "pass-inst-%s.js" % n
              and re.fullmatch(r"\d+\.\d+\.\d+", RECORD[n]["version"])
              and re.fullmatch(r"[0-9a-f]{64}", RECORD[n]["digest"]) for n in NAMES),
      "each entry carries the address the file is served at, the version it must declare and the "
      "digest its bytes must weigh to: " + ", ".join(
          "%s → %s v%s %s…" % (n, RECORD[n]["src"], RECORD[n]["version"], RECORD[n]["digest"][:12])
          for n in NAMES))

check("PASS-PACK every recorded digest is the digest of the file the build actually served",
      all(RECORD[n]["digest"] == hashlib.sha256(BYTES[n]).hexdigest() for n in NAMES),
      "a digest taken over the SOURCE would weigh a file no visitor ever fetches. " + ", ".join(
          "%s is %d B and weighs to %s…" % (n, len(BYTES[n]), hashlib.sha256(BYTES[n]).hexdigest()[:12])
          for n in NAMES))

check("PASS-PACK every file declares its own version in one place, and the build reads it from there",
      all(len(re.findall(r'var INSTRUMENT_VERSION = "',
                         SOURCE[n].read_text(encoding="utf-8"))) == 1
          and RECORD[n]["version"] == re.search(
              r'var INSTRUMENT_VERSION = "([^"]+)"',
              SOURCE[n].read_text(encoding="utf-8")).group(1) for n in NAMES),
      "one home for one fact: the version a file declares and the version the record tells a host "
      "to load cannot drift apart, because the second is read out of the first at bake")

# ================================================================================================
# THE BYTE FENCES — ONE PER INSTRUMENT, each at its own measurement plus about a tenth, with the
# reason written beside it, which is the rule §12 states.
#
# WHY ONE EACH. The single pack broke its own fence the day it was raised, and the fence could say
# only that the bag was too heavy. One instrument, one number: a move answers one question — is
# THIS picture worth its bytes to a phone — and an instrument landing beside it moves no fence but
# its own. The numbers are expected to move; 25 lab modules stand on disk and these are where they
# land, and none of them will ever be fetched by a visit whose score does not name it.
#
# What travels to a phone is the gzipped file; tests/test_budget.py carries the gzip fence for each
# of these files with its own breakdown.
# ================================================================================================
FENCES = {
    "adrift": (20_700, 18_846),
    "gears": (14_800, 13_472),
    "matter": (10_500, 9_529),
    "weave": (13_900, 12_611),
}
for _n in NAMES:
    _fence, _measured = FENCES.get(_n, (0, 0))
    check(f"PASS-PACK the «{_n}» instrument stands under its own {_fence} B fence",
          _fence > 0 and len(BYTES[_n]) < _fence,
          f"pass-inst-{_n}.js built at {len(BYTES[_n])} B against a fence sized at the "
          f"{_measured} B this instrument measured plus about a tenth. It is fetched by the host, "
          f"after the host, and only on a visit whose own score names it")

check("PASS-PACK a fence is written for every instrument that ships",
      sorted(FENCES) == NAMES,
      "an instrument landing without a fence of its own would travel unweighed. Fenced: %s. "
      "Shipping: %s" % (sorted(FENCES), NAMES))


# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-PACK a correctly recorded file loads, and its instrument is registered by name",
    "PASS-PACK a file whose bytes changed is refused, and the reason names the weighing",
    "PASS-PACK a file declaring the wrong version is refused, and the reason names both versions",
    "PASS-PACK a file that never arrives lands the product's own behaviour: the walk's glide runs",
    "PASS-PACK an instrument the host cannot supply is refused at registration, with its reason",
    "PASS-PACK a file declaring another instrument is refused, and the reason names both names",
    "PASS-PACK a score naming an instrument the record does not carry declines before takeover",
    "PASS-PACK a visit that never draws fetches no file at all",
    "PASS-PACK a drawing visit fetches the host, then only the instruments its own score names",
]

RED_ROWS = [
    "PASS-PACK red-on-bug · the host names an instrument: the boundary row stops being green",
    "PASS-PACK red-on-bug · the digest check removed: changed bytes load instead of being refused",
    "PASS-PACK red-on-bug · the version check removed: a foreign version loads instead of being refused",
    "PASS-PACK red-on-bug · the name check removed: a file registers the instrument it was not asked for",
    "PASS-PACK red-on-bug · the supply check removed: an unsupplyable instrument registers",
]

PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]

FIRST = NAMES[0] if NAMES else ""


def bench_dir(files=None, record=None, drop=(), layer_text=None, restamp=True):
    """A served root holding the host, the site's own record, the instrument files it names and the
    fixture.

    `files` replaces the text served for an instrument, by name. `restamp` writes the record with
    the digest of the bytes actually being served, which is what the build does; a row that wants a
    MISMATCH passes restamp=False. `record` edits the record itself before it is written. `drop`
    names instruments whose file is left off the root entirely, which is the road a file that fails
    to arrive takes."""
    d = Path(tempfile.mkdtemp(prefix="synth_packbench_"))
    (d / "pass-layer.js").write_text(layer_text or LAYER, encoding="utf-8")
    settings = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    rows = settings["pass"]["instruments"]
    for n in NAMES:
        text = (files or {}).get(n, BUILT[n])
        if restamp:
            rows[n]["digest"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if n not in drop:
            (d / rows[n]["src"]).write_text(text, encoding="utf-8")
    if record:
        record(rows)
    (d / "config.json").write_text(json.dumps(settings), encoding="utf-8")
    shutil.copy2(ROOT / "tests" / "fixture_pass_pack.html", d / "index.html")
    return d


def ready(br, tries=80):
    for _ in range(tries):
        if br.evaluate("String(!!window.__ready)") == "true":
            return True
        br.sleep(0.25)
    return False


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def load(br, names, tries=80):
    """Ask the host for these instruments and wait for its answer: one reason per name, or null
    where the instrument reached the registry."""
    br.evaluate("window.__load(%s); 0" % json.dumps(names))
    for _ in range(tries):
        got = js(br, "return window.__loaded;")
        if got is not None:
            return got
        br.sleep(0.25)
    return None


def on_bench(fn, **kw):
    """Stand a bench up, run `fn(br)` against it, and take the bench down again."""
    d = bench_dir(**kw)
    try:
        with serve(d) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html")
                if not ready(br):
                    return None
                return fn(br)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def score_naming(name):
    """A one-cue score naming one instrument, the shape every score on file carries."""
    return {"schema": 2, "duration": 3000,
            "cues": [{"id": "c", "instrument": {"id": name, "api": 1}, "voice": "letter",
                      "levels": ["SURFACE"], "window": [0, 3], "nodes": {}, "tracks": {}}]}


# An instrument the host cannot supply: its single uniform asks to be bound from a source that is
# neither one of the host's own six, nor a frame value the instrument answers, nor a handle it
# publishes. §7's rule is that this is refused AT REGISTRATION, with its reason.
def unsupplyable(name):
    return '''(function () {
  var join = window.__exPassInstrument;
  if (typeof join !== "function") return;
  var INSTRUMENT_VERSION = "%s";
  join({ version: INSTRUMENT_VERSION, instrument: {
    name: "%s",
    manifest: {
      passes: [{ program: "p", vert: "void main(){}", frag: "void main(){}",
                 uniforms: [{ name: "uWhat", type: "float", source: "handle:nowhere" }] }],
      handles: { mix: { min: 0, max: 1, def: 0 } },
      neutralPose: { mix: 0 },
      gl: { preserveDrawingBuffer: false },
    },
    values: function () { return { m: 0 }; },
    fit: function () { return [1, 1]; },
    prepare: function () { return { take: true }; },
    start: function () {}, frame: function () {}, resize: function () {},
    cancel: function () {}, dispose: function () {},
    contextLost: function () {}, contextRestored: function () {},
  } });
})();
''' % (RECORD[name]["version"], name)


if not chrome_available():
    for r in BROWSER_ROWS + RED_ROWS[1:]:
        skip(r, "Chrome for Testing is not installed (pinned expected skip)")
elif not all(p.exists() for p in PHOTOS):
    for r in BROWSER_ROWS + RED_ROWS[1:]:
        skip(r, "the bench photographs are not on this machine")
else:
    # ---- row 1: the good road ------------------------------------------------------------------
    got = on_bench(lambda br: {"record": js(br, "return window.__record();"),
                               "whys": load(br, NAMES),
                               "files": js(br, "return window.__files();"),
                               "reg": js(br, "return window.__registered();"),
                               "errs": js(br, "return window.__errs;")})
    if got is None:
        check(BROWSER_ROWS[0], False, "the bench never came up")
    else:
        check(BROWSER_ROWS[0],
              got["record"]["state"] == "read"
              and sorted(got["record"]["names"]) == NAMES
              and got["whys"] == {n: None for n in NAMES}
              and all(f["state"] == "loaded" for f in got["files"])
              and all(n in got["reg"] for n in NAMES)
              and not got["errs"],
              "the host read the record («%s»), asked each name for its own file, and registered "
              "%s. Registration is name-driven throughout: each instrument lands under the name its "
              "own manifest carries, and the host wrote none of those names down. Console: %s"
              % (got["record"]["state"], got["reg"], got["errs"] or "clean"))

    # ---- row 2: the bytes changed --------------------------------------------------------------
    # One character of one shader constant, and the record carries the digest of the file as it was.
    victim = "weave" if "weave" in NAMES else FIRST
    tampered = BUILT[victim].replace("0.42 * sin", "0.43 * sin", 1)
    got = on_bench(lambda br: {"whys": load(br, [victim]),
                               "reg": js(br, "return window.__registered();")},
                   files={victim: tampered}, restamp=False)
    if got is None:
        check(BROWSER_ROWS[1], False, "the bench never came up")
    else:
        why = (got["whys"] or {}).get(victim) or ""
        check(BROWSER_ROWS[1],
              tampered != BUILT[victim] and "weigh" in why and victim not in got["reg"],
              "one shader constant moved and the record still carried the old digest. The host "
              "refused with «%s», and registered %s" % (why, got["reg"] or "nothing"))

    # ---- row 3: the version is wrong -----------------------------------------------------------
    aged = BUILT[FIRST].replace('INSTRUMENT_VERSION="%s"' % RECORD[FIRST]["version"],
                                'INSTRUMENT_VERSION="0.0.9"', 1)
    if aged == BUILT[FIRST]:      # the built file may keep the spaces the source has
        aged = BUILT[FIRST].replace('INSTRUMENT_VERSION = "%s"' % RECORD[FIRST]["version"],
                                    'INSTRUMENT_VERSION = "0.0.9"', 1)
    got = on_bench(lambda br: {"whys": load(br, [FIRST]),
                               "reg": js(br, "return window.__registered();")},
                   files={FIRST: aged})
    if got is None:
        check(BROWSER_ROWS[2], False, "the bench never came up")
    else:
        why = (got["whys"] or {}).get(FIRST) or ""
        check(BROWSER_ROWS[2],
              aged != BUILT[FIRST] and "0.0.9" in why and RECORD[FIRST]["version"] in why
              and FIRST not in got["reg"],
              "the bytes weigh correctly and the file declares a version the record does not name. "
              "The host refused with «%s»" % why)

    # ---- row 4: the file never arrives ---------------------------------------------------------
    # §2's refusal roads: the host stands, registers nothing, and a scored command reaches the
    # walk's own glide — which is exactly what a visit whose renderer file never arrived looks like.
    got = on_bench(lambda br: {"whys": load(br, [FIRST]),
                               "reg": js(br, "return window.__registered();"),
                               "off": js(br, "return window.__offer(%s);"
                                             % json.dumps(score_naming(FIRST)))},
                   drop=(FIRST,))
    if got is None:
        check(BROWSER_ROWS[3], False, "the bench never came up")
    else:
        why = (got["whys"] or {}).get(FIRST) or ""
        check(BROWSER_ROWS[3],
              "404" in why and FIRST not in got["reg"] and got["off"]["took"] is False,
              "the host joined the walk and said why the file is missing — «%s» — registered "
              "nothing, and answered a scored command with `false`, which hands the landing back "
              "to the walk's own glide" % why)

    # ---- row 5: an instrument the host cannot supply -------------------------------------------
    got = on_bench(lambda br: {"whys": load(br, [FIRST]),
                               "reg": js(br, "return window.__registered();")},
                   files={FIRST: unsupplyable(FIRST)})
    if got is None:
        check(BROWSER_ROWS[4], False, "the bench never came up")
    else:
        why = (got["whys"] or {}).get(FIRST) or ""
        check(BROWSER_ROWS[4],
              "handle:nowhere" in why and "cannot supply" in why and FIRST not in got["reg"],
              "the instrument binds a uniform from a source the host has no value for, and it is "
              "refused at registration naming the source: «%s». Registered: %s"
              % (why, got["reg"] or "nothing"))

    # ---- row 6: a file declaring another instrument ---------------------------------------------
    # THE RULE ONE FILE PER INSTRUMENT NEEDS AND ONE PACK NEVER DID. A host asked one address for
    # one name, and what answers must be that instrument. Without this check an address and the
    # instrument at it could drift apart and the visitor would meet a picture nobody scored.
    other = NAMES[1] if len(NAMES) > 1 else FIRST
    swapped = BUILT[other]
    got = on_bench(lambda br: {"whys": load(br, [FIRST]),
                               "reg": js(br, "return window.__registered();")},
                   files={FIRST: swapped})
    if got is None:
        check(BROWSER_ROWS[5], False, "the bench never came up")
    else:
        why = (got["whys"] or {}).get(FIRST) or ""
        check(BROWSER_ROWS[5],
              other != FIRST and FIRST in why and other in why
              and FIRST not in got["reg"] and other not in got["reg"],
              "«%s»'s address answered with «%s»'s file, weighing correctly and declaring the right "
              "version. The host refused it with «%s» and registered %s — an instrument reached no "
              "registry under a name nobody asked for" % (FIRST, other, why, got["reg"] or "nothing"))

    # ---- row 7: a score naming an instrument the record does not carry --------------------------
    got = on_bench(lambda br: {"off": js(br, "return window.__offer(%s);"
                                             % json.dumps(score_naming("nobody"))),
                               "files": js(br, "return window.__files();"),
                               "reg": js(br, "return window.__registered();")})
    if got is None:
        check(BROWSER_ROWS[6], False, "the bench never came up")
    else:
        rows = [f for f in got["files"] if f["name"] == "nobody"]
        check(BROWSER_ROWS[6],
              got["off"]["took"] is False and got["off"]["seen"]["curtains"] == 0
              and len(rows) == 1 and rows[0]["state"] == "refused"
              and "names no instrument" in (rows[0]["why"] or ""),
              "the score named an instrument the site's record does not carry. The host refused it "
              "with «%s», raised no curtain, and answered `false`, so the walk's own glide lands "
              "the transition — the refusal stands before takeover, where it costs the visitor "
              "nothing" % (rows[0]["why"] if rows else "nothing at all"))

    # ---- rows 8 and 9: what a visit fetches ----------------------------------------------------
    # The real baked site, not a bench: the client's own door decides whether the host is fetched at
    # all, and the score decides which instruments are. The law that the renderer's file reaches only
    # a drawing visit extends to every instrument, and this reads the network to prove it.
    def walk_ready(br, tries=25):
        """The walk owns the input only once the door ceremony has finished; a key pressed before
        that is absorbed by the ceremony and steps nothing — and a step is what makes the client
        ask for the host's file at all. Without this wait the two rows below would read an empty
        network log and pass on having fetched nothing."""
        for _ in range(tries):
            if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                           "&& !document.documentElement.classList.contains('ex-face'))") == "true":
                return True
            br.sleep(0.2)
        return False

    def entered(br, base, arg):
        br.navigate(base + "/")
        br.clear_storage()
        br.navigate(base + "/?pass=" + arg)
        br.sleep(0.8)
        br.click(".exd-window", settle=1.4)
        if not walk_ready(br):
            return False
        br.sleep(0.4)
        return True

    def asked(br):
        return [u for u in br.net_log() if "pass-layer" in u or "pass-inst-" in u]

    with serve(TMP) as base:
        with Browser(width=VW, height=VH) as br:
            br.net_capture()

            # This suite BAKES the picture on, so the row that wants it off asks for off by name.
            # Reading the baked default here would have tested nothing: the first run of this row
            # read the setting as it ships, saw both files fetched, and said so.
            stood_off = entered(br, base, "diagnostics:on,visualLayer:off")
            br.net_clear()
            br.key("ArrowDown")
            br.sleep(1.4)
            off_asked = asked(br)

            br.emulate_media(prefers_reduced_motion="reduce")
            stood_quiet = entered(br, base, "diagnostics:on,visualLayer:pass")
            br.net_clear()
            br.key("ArrowDown")
            br.sleep(1.4)
            quiet_asked = asked(br)

            check(BROWSER_ROWS[7],
                  stood_off and stood_quiet and not off_asked and not quiet_asked,
                  "both visits stood in the walk and stepped (%s, %s); with the picture switched "
                  "off the visit asked for %s, and with reduced motion it asked for %s. No file "
                  "leaves the server for a visit that never draws"
                  % (stood_off, stood_quiet, off_asked or "no file", quiet_asked or "no file"))

        # The drawing visit gets a browser of its own: the reduced-motion emulation above is a
        # per-browser override, and a visit meant to draw must not inherit it.
        #
        # THE SCORES THIS BAKE CARRIES ARE NONE, so a stepped walk asks for the host and for no
        # instrument at all — which is itself the measurement this shape was built for: a visit pays
        # for the instruments its own passage names, and a passage naming none pays nothing.
        with Browser(width=VW, height=VH) as br:
            br.net_capture()
            stood = entered(br, base, "diagnostics:on,visualLayer:pass")
            br.net_clear()
            br.key("ArrowDown")
            br.sleep(2.2)
            drew = asked(br)
            named = js(br, "return (window.__exPass.report().settings || []).length > 0;")
            check(BROWSER_ROWS[8],
                  stood and any("pass-layer" in u for u in drew)
                  and not [u for u in drew if "pass-inst-" in u]
                  and named,
                  "a visit that draws asks for the host: %s. This bake carries no score for any "
                  "pair, so no cue names an instrument and not one instrument file leaves the "
                  "server — under the single pack the same visit fetched the whole farm"
                  % [u.rsplit("/", 1)[-1] for u in drew])

    # ---- the red-on-bug proofs -----------------------------------------------------------------
    # Each reverts ONE rule in this suite's own copy of the artifact, runs the row that rule answers,
    # and lets the copy go. The source tree is never written to and git is never asked to restore.
    # R1 · THE HOST NAMES AN INSTRUMENT. No browser: the boundary row is a grep over the built host,
    # so the proof is that putting one name back makes that same grep find it.
    named_layer = LAYER.replace('RECORD_SRC = "config.json"',
                                'RECORD_SRC = "config.json" /* %s */' % FIRST, 1)
    check(RED_ROWS[0],
          named_layer != LAYER and host_names(LAYER) == [] and host_names(named_layer) == [FIRST],
          "the host as built names no instrument, so the boundary row is green. Write one name "
          "back into it — a single mention of «%s» — and the same grep finds %s, which is the row "
          "going red. 0 occurrences → 1." % (FIRST, host_names(named_layer)))

    def crippled(row, find, replace, files=None, restamp=True, drop=(), read=None, expect=None,
                 detail=""):
        """Serve a host with one rule removed, run the row that rule answers, and read what moved."""
        if find not in LAYER:
            check(row, False, "the rule's own text was not found in the built host: %r" % find[:70])
            return
        d = bench_dir(files=files, restamp=restamp, drop=drop,
                      layer_text=LAYER.replace(find, replace, 1))
        try:
            with serve(d) as base:
                with Browser(width=VW, height=VH) as br:
                    br.navigate(base + "/index.html")
                    if not ready(br):
                        check(row, False, "the crippled bench never came up")
                        return
                    got = read(br)
            check(row, got == expect, detail % (got,))
        finally:
            shutil.rmtree(d, ignore_errors=True)

    # R2 · THE DIGEST CHECK. The tampered file of row 2, against a host whose comparison always
    # agrees: what was refused now loads.
    crippled(RED_ROWS[1], "if (got !== want.digest) {", "if (false) {",
             files={victim: tampered}, restamp=False,
             read=lambda br: [load(br, [victim]).get(victim), victim in js(br, "return window.__registered();")],
             expect=[None, True],
             detail="with the comparison in place these bytes are refused and the instrument never "
                    "registers; with it removed the same changed bytes load and it does. This run "
                    "read %r, where [null, true] is «no reason given, and registered»")

    # R3 · THE VERSION CHECK. The foreign-version file of row 3, against a host that stops comparing.
    crippled(RED_ROWS[2],
             'if (String(joined.version) !== String(want.version)) {', 'if (false) {',
             files={FIRST: aged},
             read=lambda br: [load(br, [FIRST]).get(FIRST), FIRST in js(br, "return window.__registered();")],
             expect=[None, True],
             detail="with the comparison in place a file declaring 0.0.9 to a record naming another "
                    "version is refused; with it removed the same file loads and registers. This "
                    "run read %r")

    # R4 · THE NAME CHECK, the rule one file per instrument needs. One instrument's file served at
    # another's address, against a host that stops asking whether it got what it asked for.
    crippled(RED_ROWS[3],
             'if (String(inst.name) !== String(name)) {', 'if (false) {',
             files={FIRST: swapped},
             read=lambda br: [load(br, [FIRST]).get(FIRST), sorted(js(br, "return window.__registered();"))],
             expect=[None, sorted([other, "test"])],
             detail="with the check in place «%s»'s address answering with «%s»'s file is refused; "
                    "with it removed the host registers the instrument it never asked for, under "
                    "the other name, and the score that named the first finds nothing. This run "
                    "read %%r" % (FIRST, other))

    # R5 · THE SUPPLY CHECK of §7. The unsupplyable instrument of row 5, against a host that stops
    # asking whether it can answer the uniform's source.
    crippled(RED_ROWS[4],
             "if (!supplySeen(String(u.source), provides)) {", "if (false) {",
             files={FIRST: unsupplyable(FIRST)},
             read=lambda br: [load(br, [FIRST]).get(FIRST), FIRST in js(br, "return window.__registered();")],
             expect=[None, True],
             detail="with the supply check in place the file carrying that instrument is refused "
                    "and nothing lands; with it removed the same instrument registers, uniform "
                    "source and all. This run read %r")


# ---------------------------------------------------------------- report
for name, verdict, detail in results:
    print(f"{verdict:5s} {name}" + (f"   — {detail}" if detail else ""))
passed = sum(1 for _, v, _ in results if v == "PASS")
failed = sum(1 for _, v, _ in results if v == "FAIL")
skipped = sum(1 for _, v, _ in results if v == "SKIP")
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")

shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if failed else 0)
