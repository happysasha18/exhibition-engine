#!/usr/bin/env python3
"""PASS-API-V1 — the boundary between the engine's host and the artistic effect pack.
Run: python3 tests/test_pass_pack.py

Root: his word of 2026-08-14 08:39 — the engine knows no TLV effect name and loads a version-pinned
opaque effect pack; tlvphotos owns the artistic effect pack and its manifests.

WHAT THIS SUITE IS FOR. Until 2026-08-14 the three instruments lived inside the engine's own
renderer file. The byte fence on that file broke three times in one morning, each time for the same
reason: an instrument had landed, and a fence sized for the host was being asked to answer for the
picture. The instruments now ship in pass-pack.js, which the host fetches by address, weighs against
the digest the build stamped, and loads only when the bytes match and the version it declares is the
version this host was told.

THE ROW THAT IS THE WHOLE POINT is the first one below: the BUILT host is grepped for the three
instrument names that ship today, and it reds on any of them. A boundary nobody can check is a
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
PACK = (TMP / "pass-pack.js").read_text(encoding="utf-8")
PACK_BYTES = (TMP / "pass-pack.js").read_bytes()

# The three instrument names that ship in the pack today. The row below reads them out of the PACK
# rather than writing them into this file twice, so a fourth instrument landing tomorrow is covered
# by the same row without anyone remembering to add it here.
NAMES = sorted(set(re.findall(r'function (\w+)Instrument\(\)', PACK)))


def stamped(text):
    """The address, version and digest the build stamped into a host, read back out of it."""
    return {
        "src": (re.search(r'src: "([^"]+)", version:', text) or [None, None])[1],
        "version": (re.search(r'version: "([^"]*)", digest:', text) or [None, None])[1],
        "digest": (re.search(r'digest: "([^"]*)"', text) or [None, None])[1],
    }


STAMP = stamped(LAYER)


# ---------------------------------------------------------------- string rows

# ================================================================================================
# THE BOUNDARY ROW. Everything else in this file is about how the pack travels; this is about what
# the host is allowed to know. It reads the BUILT artifact — the comment-stripped file a visitor
# downloads — so it judges code and cannot be tripped either way by prose that merely names an
# instrument. The emptiness guard keeps it from passing on nothing.
# ================================================================================================
def host_names(text):
    return sorted(set(re.findall("|".join(NAMES), text))) if NAMES else []


check("PASS-PACK the host knows no instrument name — the built host names none of the three",
      len(LAYER) > 1000 and len(NAMES) == 3 and not host_names(LAYER),
      "the engine loads an opaque pack and registers whatever it declares, by the name each "
      "manifest carries. The three the pack ships today are %s, and the built host (%d characters) "
      "names %s" % (NAMES, len(LAYER), host_names(LAYER) or "none of them"))

check("PASS-PACK the build stamps an address, a version and a digest into the host",
      STAMP["src"] == "pass-pack.js"
      and bool(re.fullmatch(r"\d+\.\d+\.\d+", STAMP["version"] or ""))
      and bool(re.fullmatch(r"[0-9a-f]{64}", STAMP["digest"] or "")),
      "the host is told three things and checks all three: it fetched %r, expects version %r and "
      "expects its bytes to weigh to %s" % (STAMP["src"], STAMP["version"],
                                            (STAMP["digest"] or "")[:16] + "…"))

check("PASS-PACK the stamped digest is the digest of the pack the build actually served",
      STAMP["digest"] == hashlib.sha256(PACK_BYTES).hexdigest(),
      "a digest taken over the SOURCE would weigh a file no visitor ever fetches. The served pack "
      "is %d B and weighs to %s" % (len(PACK_BYTES), hashlib.sha256(PACK_BYTES).hexdigest()[:16] + "…"))

check("PASS-PACK the pack declares its own version in one place, and the build reads it from there",
      len(re.findall(r'var PACK_VERSION = "', (ROOT / "engine" / "assets" / "pass-pack.js")
                     .read_text(encoding="utf-8"))) == 1
      and STAMP["version"] == re.search(
          r'var PACK_VERSION = "([^"]+)"',
          (ROOT / "engine" / "assets" / "pass-pack.js").read_text(encoding="utf-8")).group(1),
      "one home for one fact: the number a pack declares and the number a host is told to load "
      "cannot drift apart, because the second is read out of the first at bake")

# THE PACK'S OWN BYTE FENCE, FROM DAY ONE — the same rule §12 states for the renderer's file: the
# measurement plus about a tenth, with the reason written into the test.
#
# Measured 2026-08-14 at 34 589 B built. The fence stands at 38 000 B, 3 411 B above it.
#
# WHAT THIS FENCE IS FOR, AND HOW IT DIFFERS FROM THE HOST'S. The host's fence guards a machine that
# should not grow much; this one guards a picture that is expected to grow, because 25 lab modules
# stand on disk and this is where they land. The number will move, and each move answers one
# question — is the added picture worth its bytes to a phone. What the split bought is that the
# question is now asked about the picture alone: an instrument landing here moves no fence of the
# host's, and the host's own budget stopped tracking the effect farm.
#
# What travels to a phone is the gzipped file, at 7 894 B under an 8 700 B fence
# (tests/test_budget.py, which carries its own breakdown).
PACK_FENCE = 38000
check(f"PASS-PACK the pack carries a byte fence of its own from day one (now {PACK_FENCE} B)",
      len(PACK_BYTES) < PACK_FENCE,
      f"pass-pack.js built at {len(PACK_BYTES)} B — three instruments with their shaders, response "
      f"curves, field constants and manifests. It is fetched by the host, after the host, and only "
      f"on a visit that actually draws")


# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-PACK a correctly stamped pack loads, and every instrument it declares is registered by name",
    "PASS-PACK a pack whose bytes changed is refused, and the reason names the weighing",
    "PASS-PACK a pack declaring the wrong version is refused, and the reason names both versions",
    "PASS-PACK a pack that never arrives lands the product's own behaviour: the walk's glide runs",
    "PASS-PACK an instrument the host cannot supply is refused at registration, with its reason",
    "PASS-PACK a pack is refused WHOLE — one bad instrument leaves none of it registered",
    "PASS-PACK a visit that never draws fetches neither file",
    "PASS-PACK a drawing visit fetches both, the host first and its pack after it",
]

RED_ROWS = [
    "PASS-PACK red-on-bug · the host names an instrument: the boundary row stops being green",
    "PASS-PACK red-on-bug · the digest check removed: changed bytes load instead of being refused",
    "PASS-PACK red-on-bug · the version check removed: a foreign version loads instead of being refused",
    "PASS-PACK red-on-bug · the supply check removed: an unsupplyable instrument registers",
]

PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]


def bench_dir(pack_text=None, layer_text=None, restamp=True, drop_pack=False):
    """A served root holding one host, one pack and the fixture.

    `restamp` re-stamps the host with the digest of the pack actually being served, which is what
    the build does; a row that wants a MISMATCH passes restamp=False and hands over changed bytes.
    `drop_pack` serves no pack at all, which is the road a pack that fails to arrive takes."""
    d = Path(tempfile.mkdtemp(prefix="synth_packbench_"))
    pack = PACK if pack_text is None else pack_text
    layer = LAYER if layer_text is None else layer_text
    if restamp:
        layer = layer.replace(STAMP["digest"], hashlib.sha256(pack.encode("utf-8")).hexdigest())
    (d / "pass-layer.js").write_text(layer, encoding="utf-8")
    if not drop_pack:
        (d / "pass-pack.js").write_text(pack, encoding="utf-8")
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


# A pack declaring one instrument the host cannot supply: its single uniform asks to be bound from a
# source that is neither one of the host's own six, nor a frame value the instrument answers, nor a
# handle it publishes. §7's rule is that this is refused AT REGISTRATION, with its reason.
UNSUPPLYABLE = """
  function strangerInstrument() {
    return {
      name: "stranger",
      manifest: {
        passes: [{ program: "stranger", vert: "void main(){}", frag: "void main(){}",
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
    };
  }
"""


def with_stranger(text):
    """The pack, plus one instrument the host cannot supply, declared last."""
    text = text.replace("  join({", UNSUPPLYABLE + "\n  join({", 1)
    return text.replace("gearsInstrument()]", "gearsInstrument(), strangerInstrument()]", 1)


if not chrome_available():
    for r in BROWSER_ROWS + RED_ROWS[1:]:
        skip(r, "Chrome for Testing is not installed (pinned expected skip)")
elif not all(p.exists() for p in PHOTOS):
    for r in BROWSER_ROWS + RED_ROWS[1:]:
        skip(r, "the bench photographs are not on this machine")
else:
    # ---- row 1: the good road ------------------------------------------------------------------
    got = on_bench(lambda br: {"pack": js(br, "return window.__pack();"),
                               "reg": js(br, "return window.__registered();"),
                               "errs": js(br, "return window.__errs;")})
    if got is None:
        check(BROWSER_ROWS[0], False, "the bench never came up")
    else:
        check(BROWSER_ROWS[0],
              got["pack"]["state"] == "loaded"
              and got["pack"]["version"] == STAMP["version"]
              and got["pack"]["why"] is None
              and all(n in got["reg"] for n in NAMES)
              and not got["errs"],
              "the pack loaded at version %s and the host registered %s. Registration is name-"
              "driven throughout: each instrument lands under the name its own manifest carries, "
              "and the host wrote none of those names down. Console: %s"
              % (got["pack"]["version"], got["reg"], got["errs"] or "clean"))

    # ---- row 2: the bytes changed --------------------------------------------------------------
    # One character of one shader constant, and the host is told the digest of the file as it was.
    tampered = PACK.replace("0.42 * sin", "0.43 * sin", 1)
    got = on_bench(lambda br: {"pack": js(br, "return window.__pack();"),
                               "reg": js(br, "return window.__registered();")},
                   pack_text=tampered, restamp=False)
    if got is None:
        check(BROWSER_ROWS[1], False, "the bench never came up")
    else:
        check(BROWSER_ROWS[1],
              tampered != PACK
              and got["pack"]["state"] == "refused"
              and "weigh" in (got["pack"]["why"] or "")
              and not [n for n in NAMES if n in got["reg"]],
              "one shader constant moved and the host was told the old digest. It refused with "
              "«%s», and registered none of the three" % (got["pack"]["why"],))

    # ---- row 3: the version is wrong -----------------------------------------------------------
    aged = PACK.replace('PACK_VERSION="%s"' % STAMP["version"],
                        'PACK_VERSION="0.0.9"', 1)
    if aged == PACK:      # the built file may keep the spaces the source has
        aged = PACK.replace('PACK_VERSION = "%s"' % STAMP["version"],
                            'PACK_VERSION = "0.0.9"', 1)
    got = on_bench(lambda br: {"pack": js(br, "return window.__pack();"),
                               "reg": js(br, "return window.__registered();")},
                   pack_text=aged, restamp=True)
    if got is None:
        check(BROWSER_ROWS[2], False, "the bench never came up")
    else:
        check(BROWSER_ROWS[2],
              aged != PACK
              and got["pack"]["state"] == "refused"
              and "0.0.9" in (got["pack"]["why"] or "")
              and STAMP["version"] in (got["pack"]["why"] or "")
              and not [n for n in NAMES if n in got["reg"]],
              "the bytes weigh correctly and the pack declares a version this host was not told to "
              "load. It refused with «%s»" % (got["pack"]["why"],))

    # ---- row 4: the pack never arrives ---------------------------------------------------------
    # §2's refusal roads: the host stands, registers no instrument, and a scored command reaches the
    # walk's own glide — which is exactly what a visit whose renderer file never arrived looks like.
    score = {"schema": 2, "duration": 3000,
             "cues": [{"id": "c", "instrument": {"id": NAMES[0], "api": 1}, "voice": "letter",
                       "levels": ["SURFACE"], "window": [0, 3], "nodes": {}, "tracks": {}}]}
    got = on_bench(lambda br: {"pack": js(br, "return window.__pack();"),
                               "reg": js(br, "return window.__registered();"),
                               "off": js(br, "return window.__offer(%s);" % json.dumps(score))},
                   drop_pack=True)
    if got is None:
        check(BROWSER_ROWS[3], False, "the bench never came up")
    else:
        check(BROWSER_ROWS[3],
              got["pack"]["state"] == "refused"
              and not [n for n in NAMES if n in got["reg"]]
              and got["off"]["took"] is False,
              "the host joined the walk and said why the pack is missing — «%s» — registered none "
              "of the three, and answered a scored command with `false`, which hands the landing "
              "back to the walk's own glide" % (got["pack"]["why"],))

    # ---- rows 5 and 6: an instrument the host cannot supply ------------------------------------
    stranger = with_stranger(PACK)
    got = on_bench(lambda br: {"pack": js(br, "return window.__pack();"),
                               "reg": js(br, "return window.__registered();")},
                   pack_text=stranger, restamp=True)
    if got is None:
        check(BROWSER_ROWS[4], False, "the bench never came up")
        check(BROWSER_ROWS[5], False, "the bench never came up")
    else:
        why = got["pack"]["why"] or ""
        check(BROWSER_ROWS[4],
              stranger != PACK
              and got["pack"]["state"] == "refused"
              and "stranger" in why and "handle:nowhere" in why and "cannot supply" in why,
              "the added instrument binds a uniform from a source the host has no value for, and "
              "it is refused at registration naming both the instrument and the source: «%s»" % why)
        check(BROWSER_ROWS[5],
              got["pack"]["state"] == "refused"
              and not [n for n in NAMES if n in got["reg"]],
              "the other three instruments in that pack are sound, and none of them was registered "
              "— a pack is judged whole before any of it lands, because a stack missing a voice is "
              "a picture nobody wrote. Registered: %s" % (got["reg"],))

    # ---- rows 7 and 8: what a visit fetches ----------------------------------------------------
    # The real baked site, not a bench: the client's own door decides whether the host is fetched
    # at all, and the host's own door decides whether the pack is. The law that the renderer's file
    # reaches only a drawing visit extends to the pack, and this reads the network to prove it.
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
            off_asked = [u for u in br.net_log() if "pass-layer" in u or "pass-pack" in u]

            br.emulate_media(prefers_reduced_motion="reduce")
            stood_quiet = entered(br, base, "diagnostics:on,visualLayer:pass")
            br.net_clear()
            br.key("ArrowDown")
            br.sleep(1.4)
            quiet_asked = [u for u in br.net_log() if "pass-layer" in u or "pass-pack" in u]

            check(BROWSER_ROWS[6],
                  stood_off and stood_quiet and not off_asked and not quiet_asked,
                  "both visits stood in the walk and stepped (%s, %s); with the picture switched "
                  "off the visit asked for %s, and with reduced motion it asked for %s. Neither "
                  "file leaves the server for a visit that never draws"
                  % (stood_off, stood_quiet, off_asked or "neither file",
                     quiet_asked or "neither file"))

        # The drawing visit gets a browser of its own: the reduced-motion emulation above is a
        # per-browser override, and a visit meant to draw must not inherit it.
        with Browser(width=VW, height=VH) as br:
            br.net_capture()
            stood = entered(br, base, "diagnostics:on,visualLayer:pass")
            br.net_clear()
            br.key("ArrowDown")
            br.sleep(2.2)
            drew = [u for u in br.net_log() if "pass-layer" in u or "pass-pack" in u]
            order = [("host" if "pass-layer" in u else "pack") for u in drew]
            check(BROWSER_ROWS[7],
                  stood
                  and any("pass-layer" in u for u in drew)
                  and any("pass-pack" in u for u in drew)
                  and order.index("host") < order.index("pack"),
                  "a visit that draws asks for both, in this order: %s. The pack is fetched BY the "
                  "host, so it cannot be asked for before the host has arrived and been run" % order)

    # ---- the red-on-bug proofs -----------------------------------------------------------------
    # Each reverts ONE rule in this suite's own copy of the artifact, runs the row that rule answers,
    # and lets the copy go. The source tree is never written to and git is never asked to restore.
    # R1 · THE HOST NAMES AN INSTRUMENT. No browser: the boundary row is a grep over the built host,
    # so the proof is that putting one name back makes that same grep find it.
    named = LAYER.replace('src: "pass-pack.js"', 'src: "pass-pack.js" /* %s */' % NAMES[0], 1)
    check(RED_ROWS[0],
          named != LAYER and host_names(LAYER) == [] and host_names(named) == [NAMES[0]],
          "the host as built names no instrument, so the boundary row is green. Write one name "
          "back into it — a single mention of «%s» — and the same grep finds %s, which is the row "
          "going red. 0 occurrences → 1." % (NAMES[0], host_names(named)))

    # R2 · THE DIGEST CHECK. The tampered pack of row 2, against a host whose comparison always
    # agrees: what was refused now loads.
    tampered = PACK.replace("0.42 * sin", "0.43 * sin", 1)
    d = bench_dir(pack_text=tampered, restamp=False)
    try:
        hurt = (d / "pass-layer.js").read_text(encoding="utf-8").replace(
            "if (got !== PACK.digest) {", "if (false) {", 1)
        (d / "pass-layer.js").write_text(hurt, encoding="utf-8")
        if "if (false) {" not in hurt:
            check(RED_ROWS[1], False, "the digest comparison's own text was not found")
        else:
            with serve(d) as base:
                with Browser(width=VW, height=VH) as br:
                    br.navigate(base + "/index.html")
                    state = js(br, "return window.__pack().state;") if ready(br) else None
            check(RED_ROWS[1], state == "loaded",
                  "with the comparison in place these bytes are refused («state: refused»); with it "
                  "removed the same changed bytes load. This run read %r" % (state,))
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # R3 · THE VERSION CHECK. The foreign-version pack of row 3, against a host that stops comparing.
    d = bench_dir(pack_text=aged, restamp=True)
    try:
        hurt = (d / "pass-layer.js").read_text(encoding="utf-8").replace(
            'if (String(pack.version) !== String(PACK.version)) {', 'if (false) {', 1)
        (d / "pass-layer.js").write_text(hurt, encoding="utf-8")
        with serve(d) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html")
                got = js(br, "return {state: window.__pack().state, v: window.__pack().version};") \
                    if ready(br) else None
        check(RED_ROWS[2],
              got is not None and got["state"] == "loaded" and got["v"] == "0.0.9",
              "with the comparison in place a pack declaring 0.0.9 to a host told %s is refused; "
              "with it removed the same pack loads and the host records the foreign version it "
              "took. This run read %r" % (STAMP["version"], got))
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # R4 · THE SUPPLY CHECK of §7. The unsupplyable instrument of row 5, against a host that stops
    # asking whether it can answer the uniform's source.
    d = bench_dir(pack_text=with_stranger(PACK), restamp=True)
    try:
        hurt = (d / "pass-layer.js").read_text(encoding="utf-8").replace(
            "if (!supplySeen(String(u.source), provides)) {", "if (false) {", 1)
        (d / "pass-layer.js").write_text(hurt, encoding="utf-8")
        with serve(d) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html")
                got = js(br, "return {state: window.__pack().state, reg: window.__registered()};") \
                    if ready(br) else None
        check(RED_ROWS[3],
              got is not None and got["state"] == "loaded" and "stranger" in got["reg"],
              "with the supply check in place the pack carrying «stranger» is refused whole and "
              "nothing lands; with it removed the same instrument registers, uniform source and "
              "all. This run read %r" % (got,))
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------- report
for name, verdict, detail in results:
    print(f"{verdict:5s} {name}" + (f"   — {detail}" if detail else ""))
passed = sum(1 for _, v, _ in results if v == "PASS")
failed = sum(1 for _, v, _ in results if v == "FAIL")
skipped = sum(1 for _, v, _ in results if v == "SKIP")
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")

shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if failed else 0)
