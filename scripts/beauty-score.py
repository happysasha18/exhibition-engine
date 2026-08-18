#!/usr/bin/env python3
"""beauty-score — one crossing, written from the two works' own measurements.

THE PAIR AND THE IDEA.
  A  17862145765313792 — a cyan rotor: mirrored towers fanned into a six-armed wheel, dense window
     grids edge to edge, nothing empty in the frame (`motifs.voidShare` 0.033).
  B  18061740532199044 — acid wings: the same city's scaffolding mirrored into two wings over a
     grid of glass (`motifs.voidShare` 0.0772).

  Both works were cut by their own device into TWELVE readable pieces — A's grain of 72.148 cells
  merged by 6.0123, B's 66.3762 merged by 5.5313, and both land on twelve to four decimals
  (`sets[kind="ring"].count`). That agreement is the pivot, and the cloth carries twelve ribbons
  from the first frame to the last.

  What differs is where their band families stand: A's LIES HORIZONTAL and B's STANDS VERTICAL
  (`structure.banding.axis`, at 0.7347 and 0.6504). So the passage is the quarter turn between
  them. The cloth enters lying on the rotor's own lines, weaves the two works through each other,
  and leaves standing on the wings'. One work's structure is the way in and the other's is the way
  out, and everything between is the road.

EVERY NUMBER'S SOURCE is written into the score's own node notes, so a reader can walk any frame
back to the measurement it came from.

Run: python3 scripts/beauty-score.py [--out lab/beauty-score.json] [--duration 8000]
"""
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKS = ROOT / "tests" / "fixture_pass_works.json"

A_ID = "17862145765313792"
B_ID = "18061740532199044"

# The die. One number, named here, folded into the over/under order of the basket and into each
# ribbon's own head start — so a judged run repeats to the pixel (the seventh law of liveliness).
SEED = 3.4142

# The instrument's own vocabulary for where the grain stands: 0 the vertical band family, 1 the
# horizontal one (`weave` manifest, `axis.banding`).
BAND_AXIS = {"vertical": 0.0, "horizontal": 1.0}


def r4(v):
    return round(float(v), 4)


def static(v, note=None):
    n = {"op": "static", "value": r4(v)}
    if note:
        n["note"] = note
    return n


def set_of(work, kind):
    for s in work["sets"]:
        if s["kind"] == kind:
            return s
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "lab" / "beauty-score.json"))
    ap.add_argument("--duration", type=int, default=8000)
    ap.add_argument("--depth", type=float, default=0.55,
                    help="how far under a dipping ribbon reads, 0..1")
    ap.add_argument("--ribbons", type=float, default=None,
                    help="override the derived ribbon count, for a round of judging only")
    args = ap.parse_args()

    W = json.loads(WORKS.read_text(encoding="utf-8"))["works"]
    a, b = W[A_ID], W[B_ID]

    # ---- the pivot: the count both works' own devices merge to --------------------------------
    # WHY TWICE THE RING COUNT. Both works are wound about a centre that stands inside the frame
    # (`structure.radial.centre`, 0.5/0.5 and 0.35/0.35), and a straight cut across a frame meets
    # each closed ring TWICE — once on each side of that centre. So a cloth cut across a work of
    # twelve rings carries twenty-four ribbons, and the number is the ring count read on the axis
    # the ribbons are actually cut on rather than the ring count itself.
    ringA, ringB = set_of(a, "ring"), set_of(b, "ring")
    assert abs(ringA["count"] - ringB["count"]) < 1e-6, \
        "the pivot is only a pivot while both works agree on it"
    for w in (a, b):
        c = w["structure"]["radial"]["centre"]
        assert 0 < c[0] < 1 and 0 < c[1] < 1, "a cut meets each ring twice only about a centre in frame"
    ribbons = 2.0 * float(ringA["count"]) if args.ribbons is None else args.ribbons
    pivot_note = ("sets[ring].count: A's own device grain %.4f merged by %.4f and B's %.4f merged "
                  "by %.4f both land on %.4f rings, and a cut across a centre that stands inside "
                  "the frame meets each ring twice, so the cloth carries %.4f ribbons and holds "
                  "them from door to door"
                  % (ringA["measuredGrain"], ringA["mergeFactor"],
                     ringB["measuredGrain"], ringB["mergeFactor"], ringA["count"],
                     2.0 * ringA["count"]))

    # ---- what travels: where the grain of the cloth stands ------------------------------------
    turnFrom = BAND_AXIS[a["structure"]["banding"]["axis"]]
    turnTo = BAND_AXIS[b["structure"]["banding"]["axis"]]
    assert turnFrom != turnTo, "this crossing exists because the two families cross"

    # ---- the camera's own arc, off the two measured radial centres ----------------------------
    # The flight leaves the departing work's centre, rises toward the arriving work's, and lands
    # back on the frame's own middle where the arriving work hangs. A pan of p needs a scale of at
    # least 1/(1-2p) to keep the frame full of picture, so the dolly is the approach the pan needs
    # and a tenth more — never a quarter over, which is what put round 1's weave behind a keyhole.
    ca = a["structure"]["radial"]["centre"]
    cb = b["structure"]["radial"]["centre"]
    SHARE = 0.55
    panPeak = [r4(-(cb[0] - ca[0]) * SHARE), r4(-(cb[1] - ca[1]) * SHARE)]
    reach = max(abs(panPeak[0]), abs(panPeak[1]))

    def paid(pan, margin=1.14):
        """The approach a pan of this reach has to be paid for. The host applies the pose as one
        transform on its own canvas, so a translation of p shows the page under the canvas unless
        the scale carries at least 1/(1-2p) — and a flight whose pan crests before its dolly can
        run ahead of what it has paid. Every point of the flight names its own price here, and
        `scripts/beauty-camera-check.py` walks the whole flight and proves the debt is paid."""
        return r4(margin * -math.log(1 - 2 * abs(pan)))

    # The pan is carried through three points so the dolly can be priced at each of them; the
    # dolly then goes on rising past the pan's crest to its own, later one.
    panMid = [r4(panPeak[0] * 0.45), r4(panPeak[1] * 0.45)]
    logMid, logAtPan = paid(max(abs(panMid[0]), abs(panMid[1]))), paid(reach)
    logScale = r4(logAtPan * 1.18)

    dur = args.duration
    d = dur / 1000.0

    # ---- the dial's own course ----------------------------------------------------------------
    # A straight line would spend as long on the two whole works as on the cloth. This course
    # lingers where both photographs are alive and moves briskly through the ends — the fourth law
    # of liveliness, dwell in the middle with rare lock-ins, written as the score's own monotone
    # segment rather than left to the engine's straight rail.
    # ROUND 5 PHOTOGRAPHED THE DEFECT this course exists to repair: a straight dial reached a full
    # cloth inside two thirds of a second, so the departing work never stood, there was no breath
    # before the fabric parted, and the long middle then had nothing left to spend. The course
    # below holds the first work almost whole through the opening sixth — the anticipation the
    # animation shelf asks for — carries the balance across the middle, and lands the arriving work
    # decisively rather than creeping onto it.
    mix_points = [{"at": 0.0, "value": 0.0},
                  {"at": 0.13, "value": 0.05, "shape": "smooth"},
                  {"at": 0.40, "value": 0.36, "shape": "smooth"},
                  {"at": 0.55, "value": 0.52, "shape": "smooth"},
                  {"at": 0.75, "value": 0.72, "shape": "smooth"},
                  {"at": 0.90, "value": 0.90, "shape": "smooth"},
                  {"at": 1.0, "value": 1.0, "shape": "smooth"}]

    # ---- the turn's own course, deliberately NOT the dial's ------------------------------------
    # The two voices must not move as one, or the passage reads as one handle wearing two names.
    # WHERE THE QUARTER TURN STANDS, and why it is not in the middle. At a half turn both ribbon
    # sets exist at once and the cloth is a basket; a basket drawn at the balance's own midpoint —
    # where the two works hold half the frame each — reads as a checkerboard of tiles rather than
    # as cloth, which is what round 1 photographed. So the turn is moved onto the passage's late
    # third: the woven middle plays whole on the DEPARTING work's own lines, and the turn is the
    # event that follows it, taken while the arriving work already leads, so the basket reads as
    # one picture with the other showing through rather than as two pictures tiled.
    # The half turn is CROSSED, never dwelt in: the cloth holds the departing work's line for the
    # whole woven middle, crosses the basket inside a fifth of the passage at the instant the camera
    # is closest and the ribbons travel fastest — where the eye is led away — and then stands on the
    # arriving work's line for the landing.
    turn_points = [{"at": 0.0, "value": turnFrom},
                   {"at": 0.58, "value": turnFrom, "shape": "smooth"},
                   {"at": 0.72, "value": r4((turnFrom + turnTo) / 2), "shape": "smooth"},
                   {"at": 0.86, "value": turnTo, "shape": "smooth"},
                   {"at": 1.0, "value": turnTo, "shape": "smooth"}]

    cue = {
        "id": "fabric",
        "instrument": {"api": 1, "id": "weave"},
        "voice": "letter",
        "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["SURFACE", "CELL"],
        "levelOwnership": {"SURFACE": "owns", "CELL": "owns"},
        "window": [0.0, d],
        "works": ["a", "b"],
        "stack": 0,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": {
            "dial": {"op": "segment", "in": {"source": "cueProgress"}, "points": mix_points,
                     "note": "the dial's own course: it lingers where both works are alive"},
            "grain": {"op": "segment", "in": {"source": "cueProgress"}, "points": turn_points,
                      "note": "structure.banding.axis: A «%s» = %g at %.4f, B «%s» = %g at %.4f"
                              % (a["structure"]["banding"]["axis"], turnFrom,
                                 a["structure"]["banding"]["score"],
                                 b["structure"]["banding"]["axis"], turnTo,
                                 b["structure"]["banding"]["score"])},
            "clock": {"source": "time"},
            # THE STRIP-COUNT BREATH, at the module's own rate — one voice on its own period, so
            # the joint pattern of the frame never visibly recurs inside a run (the first law).
            "breath": {"op": "oscillate", "shape": "sin", "rate": 0.021, "phase": 1.1,
                       "in": {"source": "time"}},
            # `add` and `multiply` take their arguments as a LIST. The lab's own serialised scores
            # write them as `a`/`b`, which this host cannot read: it records a handle-fallback and
            # the voice is silently absent. Round 8 caught that on this score's own breath — the
            # host's event log read «nMul: «in» is not a list» while the frame looked plausible.
            "breadth": {"op": "add", "in": [
                {"op": "static", "value": 1},
                {"op": "multiply", "in": [{"op": "static", "value": 0.22},
                                          {"node": "breath"}]}],
                "note": "the strip-count breath at the module's own 0.021 Hz"},
            "strips": static(ribbons, pivot_note),
            "axis": static(turnFrom,
                           "unread while «turn» is driven; it stands where the departing work's "
                           "own family stands, so a road that ever drops the turn keeps A's line"),
            "speed": static(1.0, "the module's own resting rate"),
            "seed": static(SEED, "the score's own die"),
            "press": static(1.0, "no hand is on this passage"),
            # HOW FAR UNDER A DIPPING RIBBON READS. A property of the fabric, not of either
            # photograph — the same class as the ribbon edge's own waves. It reaches the frame only
            # where two ribbon sets exist, so it is nothing for the whole woven middle and speaks
            # exactly across the quarter turn, which is the one stretch of this passage a
            # photographed round called blocky.
            "depth": static(args.depth, "the fabric's own: a ribbon passing under a crossing one is "
                                 "further from the eye, so it is read two levels down the "
                                 "picture's own chain as well as drawn darker"),
            # THE RIBBON'S OWN EDGE IS ALIVE, and the three numbers are the approved module's own.
            # lab/effects/weave.js:79–92 states why they exist: the width of a ribbon already
            # breathed, but the breath depended only on the coordinate ACROSS the ribbon, so the
            # edge itself stayed a straight line and «на одной оси кадр читался ровными жалюзи» —
            # even venetian blinds. Two waves of different length and different speed run ALONG the
            # ribbon so the irregularity never settles into a pattern, and both die at either door
            # with the fabric itself. The port turned that material property into a handle resting
            # at nothing and read from a texture reading no work in this collection carries, so
            # every work has drawn the blinds ever since. Restored here at the module's own values:
            # 0.34 + 0.17 = 0.51 of depth (`wave`), 1.7 cycles along the ribbon (`wavePeriod` is
            # its reciprocal) and 0.090 of a cycle a second (`waveDrift`).
            "wave": static(0.51, "lab/effects/weave.js:87 — 0.34 + 0.17, the module's own edge"),
            "wavePeriod": static(1 / 1.7, "lab/effects/weave.js:85 — 1.7 cycles along the ribbon"),
            "waveDrift": static(0.09, "lab/effects/weave.js:85 — 0.090 of a cycle a second"),
        },
        "tracks": {
            "mix": {"node": "dial"},
            "turn": {"node": "grain"},
            "clock": {"node": "clock"},
            "nMul": {"node": "breadth"},
            "strips": {"node": "strips"},
            "axis": {"node": "axis"},
            "speed": {"node": "speed"},
            "seed": {"node": "seed"},
            "press": {"node": "press"},
            "depth": {"node": "depth"},
            "wave": {"node": "wave"},
            "wavePeriod": {"node": "wavePeriod"},
            "waveDrift": {"node": "waveDrift"},
        },
        "resources": {v: {"bytesEstimate": 0, "framebuffers": 0, "passes": 1, "pingPong": 0,
                          "programs": 1, "textureSlots": 2, "textures": 0, "variant": v}
                      for v in ("lean", "standard", "rich")},
    }

    # ONE UNBROKEN FLIGHT, TWO ARCS. The host carries each place of the camera through the points
    # that name a number for it and through no others, so the pan and the dolly can hold their own
    # timings on one flight. The pan crests where the two works are most alive; the dolly comes
    # closest a little later, as the cloth turns — the approach is what the turn is watched from,
    # and two voices cresting together would read as one.
    camera = {
        "owner": "stage", "rests": "b",
        "track": [
            {"at": "a", "pan": {"x": 0, "y": 0}, "logScale": 0,
             "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"},
            {"at": r4(0.21 * d), "pan": {"x": panMid[0], "y": panMid[1]},
             "logScale": logMid, "owner": "stage"},
            {"at": r4(0.42 * d), "pan": {"x": panPeak[0], "y": panPeak[1]},
             "logScale": logAtPan, "owner": "stage"},
            {"at": r4(0.70 * d), "logScale": logScale, "owner": "stage"},
            {"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
             "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"},
        ],
    }

    intent = ("Two mirrored readings of one city, each cut by its own device into twelve pieces — "
              "the rotor's family lying flat, the wings' standing upright. The cloth holds the "
              "twelve and turns a quarter: it enters on the rotor's own horizontal lines, weaves "
              "the two works through each other, and leaves standing on the wings' vertical ones.")

    score = {
        "schema": 2, "duration": dur, "direction": "a-to-b", "failLand": "arrive",
        "seed": SEED, "pair": {"a": A_ID, "b": B_ID}, "intent": intent,
        "interruption": {"withinMs": 500, "resolve": "nearest-door"},
        "camera": camera, "cues": [cue],
        "quality": {v: {"renderScale": 1.0} for v in ("lean", "standard", "rich")},
        "provenance": {"source": "beauty-lane/%s__%s__ab" % (A_ID, B_ID),
                       "measuredAt": "2026-08-18", "by": "the beauty lane, by hand"},
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(score, indent=1, ensure_ascii=False), encoding="utf-8")
    print("%s  ribbons %.4f  turn %g→%g  pan peak %s  logScale %.4f  %d ms"
          % (out, ribbons, turnFrom, turnTo, panPeak, logScale, dur))


if __name__ == "__main__":
    main()
