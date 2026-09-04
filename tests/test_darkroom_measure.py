#!/usr/bin/env python3
"""DR-5 — the JavaScript port of three recipes.py analysers agrees with the Python original.

For each of ten prepared frames in tests/fixtures/darkroom-frames/ (built by that directory's own
make_frames.py, which runs recipes.py's OWN load_image/to_gray/normalise — never re-implemented
here), the REAL, currently shipped `busyness`, `edgeMap`, `chanceDiff`, `mirrorCorr` and `bestAxis`
functions are extracted out of engine/assets/darkroom-measure.js by balanced-brace text extraction
— the same idiom tests/test_pass_levels.py's own `extract_function` carries (:63-97) — and run in a
bare generated Node driver script (json in on stdin-less argv-free form, json out on stdout; no
`vm`, matching tests/test_pass_levels.py:140-150) against recipes.py's real functions, imported
from that file's own absolute path (a different-length copy lives in tlvphotos-site; its line
numbers do not match the ones cited above or in darkroom-measure.js's own comments).

Three rows per frame: busyness, lines (edge_map) and mirror axis (best_axis, with chance_diff and
mirror_corr checked beside it). All three must agree within TOL (below) for a frame to pass.

chance_diff is the one function that is not a bit-for-bit port: recipes.py samples 20000 random
pixel pairs from a seeded numpy Generator to ESTIMATE the population mean absolute difference; the
JS port computes that same population quantity exactly (closed form). TOL_CHANCE below is the
sampling gap that leaves between recipes.py's own estimate and the exact answer, measured once on
real frames — not the tolerance a bug would need to clear.

The mirror axis row also isolates the bestAxis port from that one gap: it hands the JS port the
SAME base recipes.py's own chance_diff(g) produced, rather than each side computing its own, so a
bestAxis disagreement can only mean the scan itself disagrees.

PLANTED DEFECTS (DR-5), each a text mutation applied to a throwaway in-memory copy of the extracted
source — the working file on disk is never touched, the rule tests/test_pass_matter.py:358-364
states ("the source file on disk is never touched, so nothing has to be restored and no working
tree can be left changed by a red-on-bug proof"):
  - busyness threshold 28 -> 2: every frame's busyness row reds (nearly every edge pixel clears 2).
  - drop the smoothing pass out of one Sobel direction: the lines row reds.
  - narrow the mirror scan to the single column 0.5: the mirror axis row reds on every frame whose
    true axis is not centred — five of the ten chosen frames are (make_frames.py's own survey),
    which is why this row can catch it at all.

Run: python3 tests/test_darkroom_measure.py
"""
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "engine" / "assets" / "darkroom-measure.js"
FRAMES_DIR = ROOT / "tests" / "fixtures" / "darkroom-frames"

TLVPHOTOS_ANALYZE = os.path.expanduser("~/tlvphotos/lab/analyze")
sys.path.insert(0, TLVPHOTOS_ANALYZE)
import recipes as R  # noqa: E402 — the Python original, read and imported by its absolute path

# ---------------------------------------------------------------- tolerance (measured, not live)
#
# Measured 2026-09-04 by running this file's own correctness pass (uncorrupted source, all ten
# frames below, via `python3 tests/test_darkroom_measure.py`) once and taking the largest
# disagreement per quantity. busyness, edgeMap and bestAxis are deterministic arithmetic ports with
# no sampling anywhere in them, so their gap to the Python original is pure floating-point
# summation-order noise: the measured maxima were busyness=0, edgeMap=5.68e-14, bestAxis
# score=2.44e-15, bestAxis position=0, mirror_corr=9.34e-14 — folded here into one round number
# with orders of magnitude to spare. chance_diff is the one approximation (see the module
# docstring above); its measured gap, largest on columns.jpg, was 0.792 on a 0..255 scale, rounded
# up to a clean constant below.
TOL = 1e-6              # busyness (fraction), edgeMap (pixel value), bestAxis score and position
TOL_CHANCE = 0.8        # chance_diff, 0..255 scale — recipes.py's own sampling noise, not a bug budget
TOL_MIRROR_CORR = 1e-6  # mirror_corr, -1..1 scale

FRAME_NAMES = [
    "balconies", "concrete-dishes", "glass-drum", "shalom-meir", "twin-towers",
    "columns", "glassgrid", "cranes-dusk", "round-tower", "tower-sky",
]

# ---------------------------------------------------------------- extraction (real, shipped code)

SOURCE = MODULE.read_text(encoding="utf-8")


def extract_function(text, name, after_idx=0):
    """Balanced-brace extraction of `function NAME(...) { ... }` — the REAL, current body, the
    same idiom tests/test_pass_levels.py's own `extract_function` carries."""
    marker = "function %s(" % name
    idx = text.index(marker, after_idx)
    brace = text.index("{", idx)
    depth, i = 0, brace
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[idx:i + 1]
        i += 1
    raise ValueError("unbalanced braces for function %s" % name)


FUNCS = ["clampIndex", "sobelDerivative", "sobelSmooth", "edgeMap", "busyness",
         "chanceDiff", "mirrorCorr", "bestAxis"]
BASE_SRC = "\n".join(extract_function(SOURCE, f) for f in FUNCS)

TMP = Path(tempfile.mkdtemp(prefix="darkroom_measure_"))
DRIVER_PATH = TMP / "darkroom-driver.js"


def run_frame_job(src, frame, base):
    """One Node run: busyness, full edge array, chanceDiff, bestAxis(1, base) and a fixed-column
    mirrorCorr, all from the SAME frame — everything the three rows need for one photograph."""
    driver = (
        "\"use strict\";\n"
        + src + "\n"
        "var frame = " + json.dumps(frame) + ";\n"
        "var base = " + json.dumps(base) + ";\n"
        "var w = frame.width;\n"
        "var c = Math.floor(0.5 * w), m = Math.min(c, w - c);\n"
        "var h = frame.height;\n"
        "var A = [], B = [];\n"
        "for (var i = 0; i < h; i++) {\n"
        "  for (var k = 0; k < m; k++) {\n"
        "    A.push(frame.data[i * w + (c - m + k)]);\n"
        "    B.push(frame.data[i * w + (c + m - 1 - k)]);\n"
        "  }\n"
        "}\n"
        "var out = {\n"
        "  busy: busyness(frame),\n"
        "  edge: Array.prototype.slice.call(edgeMap(frame).data),\n"
        "  chanceDiff: chanceDiff(frame),\n"
        "  bestAxis: bestAxis(frame, 1, base),\n"
        "  mirrorCorr: mirrorCorr(A, B)\n"
        "};\n"
        "console.log(JSON.stringify(out));\n"
    )
    DRIVER_PATH.write_text(driver, encoding="utf-8")
    proc = subprocess.run(["node", str(DRIVER_PATH)], capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-2000:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the driver said nothing"}
    return json.loads(lines[-1])


def load_frame(name):
    d = json.loads((FRAMES_DIR / (name + ".json")).read_text(encoding="utf-8"))
    return d


def python_reference(frame):
    """The Python original's own answers for one frame, called directly — never re-described."""
    import numpy as np
    g = np.array(frame["data"], dtype=np.float64).reshape(frame["height"], frame["width"])
    base = R.chance_diff(g)
    edge = R.edge_map(g)
    busy = float((edge > 28.0).mean())
    best_score, best_pos = R.best_axis(g, 1, base)
    w = frame["width"]
    c = int(math.floor(0.5 * w))
    m = min(c, w - c)
    A = g[:, c - m:c]
    B = g[:, c:c + m][:, ::-1]
    mc = R.mirror_corr(A, B)
    return {
        "base": base, "busy": busy, "edge": edge.ravel().tolist(),
        "best_score": float(best_score), "best_pos": float(best_pos), "mirror_corr": mc,
    }


# ---------------------------------------------------------------- rows

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def evaluate_frame(name, src, tol=None, tol_chance=None, tol_mirror=None):
    """Runs one frame through the JS driver (with `src`, possibly a mutated throwaway copy) and
    the Python original, and returns (busy_ok, lines_ok, mirror_ok, detail_dict)."""
    tol = TOL if tol is None else tol
    tol_chance = TOL_CHANCE if tol_chance is None else tol_chance
    tol_mirror = TOL_MIRROR_CORR if tol_mirror is None else tol_mirror
    frame = load_frame(name)
    ref = python_reference(frame)
    got = run_frame_job(src, frame, ref["base"])
    if "error" in got:
        return False, False, False, {"error": got["error"]}

    busy_diff = abs(got["busy"] - ref["busy"])
    busy_ok = busy_diff <= tol

    edge_diffs = [abs(a - b) for a, b in zip(got["edge"], ref["edge"])]
    edge_max = max(edge_diffs) if edge_diffs else 0.0
    lines_ok = edge_max <= tol

    chance_diff_gap = abs(got["chanceDiff"] - ref["base"])
    score_diff = abs(got["bestAxis"]["score"] - ref["best_score"])
    pos_diff = abs(got["bestAxis"]["position"] - ref["best_pos"])
    mirror_corr_diff = abs(got["mirrorCorr"] - ref["mirror_corr"])
    mirror_ok = (chance_diff_gap <= tol_chance and score_diff <= tol
                 and pos_diff <= tol and mirror_corr_diff <= tol_mirror)

    detail = {
        "busy_diff": busy_diff, "edge_max_diff": edge_max,
        "chance_diff_gap": chance_diff_gap, "axis_score_diff": score_diff,
        "axis_pos_diff": pos_diff, "mirror_corr_diff": mirror_corr_diff,
        "js_pos": got["bestAxis"]["position"], "py_pos": ref["best_pos"],
    }
    return busy_ok, lines_ok, mirror_ok, detail


def main():
    if subprocess.run(["node", "--version"], capture_output=True).returncode != 0:
        print("SKIP: node not available")
        return 0

    off_centre = []
    max_busy_diff = max_edge_diff = max_chance_gap = max_score_diff = max_pos_diff = 0.0
    max_mirror_diff = 0.0

    print("-- correctness: JS port vs Python original, ten prepared frames --")
    for name in FRAME_NAMES:
        busy_ok, lines_ok, mirror_ok, d = evaluate_frame(name, BASE_SRC)
        if "error" in d:
            check("darkroom/%s" % name, False, d["error"])
            print("%-16s ERROR %s" % (name, d["error"]))
            continue
        max_busy_diff = max(max_busy_diff, d["busy_diff"])
        max_edge_diff = max(max_edge_diff, d["edge_max_diff"])
        max_chance_gap = max(max_chance_gap, d["chance_diff_gap"])
        max_score_diff = max(max_score_diff, d["axis_score_diff"])
        max_pos_diff = max(max_pos_diff, d["axis_pos_diff"])
        max_mirror_diff = max(max_mirror_diff, d["mirror_corr_diff"])
        if abs(d["py_pos"] - 0.5) > 0.03:
            off_centre.append((name, d["py_pos"]))
        check("darkroom/%s/busyness" % name, busy_ok, "diff=%.3g" % d["busy_diff"])
        check("darkroom/%s/lines" % name, lines_ok, "max diff=%.3g" % d["edge_max_diff"])
        check("darkroom/%s/mirror-axis" % name,
              mirror_ok,
              "chance_gap=%.3g score_diff=%.3g pos_diff=%.3g mirror_corr_diff=%.3g"
              % (d["chance_diff_gap"], d["axis_score_diff"], d["axis_pos_diff"],
                 d["mirror_corr_diff"]))
        print("%-16s busy=%s lines=%s mirror=%s  (busy_diff=%.3g edge_max=%.3g "
              "chance_gap=%.3g axis_score_diff=%.3g axis_pos_diff=%.3g mirror_corr_diff=%.3g)"
              % (name, "PASS" if busy_ok else "FAIL", "PASS" if lines_ok else "FAIL",
                 "PASS" if mirror_ok else "FAIL", d["busy_diff"], d["edge_max_diff"],
                 d["chance_diff_gap"], d["axis_score_diff"], d["axis_pos_diff"],
                 d["mirror_corr_diff"]))

    print("\noff-centre frames (best_axis position away from 0.5), %d found: %s"
          % (len(off_centre), ", ".join("%s=%.3f" % (n, p) for n, p in off_centre)))
    check("darkroom/off-centre-count", len(off_centre) >= 3,
          "%d off-centre frames" % len(off_centre))

    print("\nlive maximum disagreement this run (TOL beside it):")
    print("  busyness       %.3g  (TOL=%.3g)" % (max_busy_diff, TOL))
    print("  lines/edge_map %.3g  (TOL=%.3g)" % (max_edge_diff, TOL))
    print("  chance_diff    %.3g  (TOL_CHANCE=%.3g)" % (max_chance_gap, TOL_CHANCE))
    print("  best_axis score    %.3g  (TOL=%.3g)" % (max_score_diff, TOL))
    print("  best_axis position %.3g  (TOL=%.3g)" % (max_pos_diff, TOL))
    print("  mirror_corr    %.3g  (TOL_MIRROR_CORR=%.3g)" % (max_mirror_diff, TOL_MIRROR_CORR))

    # ------------------------------------------------------------ planted defects (DR-5)
    #
    # Each mutation is applied to a throwaway in-memory copy of BASE_SRC; the file on disk is
    # never touched (tests/test_pass_matter.py:358-364).
    print("\n-- planted defects: each must red the row it targets, and clear once removed --")

    def plant(frm, to):
        if BASE_SRC.find(frm) < 0:
            raise ValueError("plant target not found: %r" % frm)
        return BASE_SRC.replace(frm, to)

    # Defect 1: busyness threshold 28 -> 2. Every work's busyness row should red.
    defect1_src = plant("if (edge[i] > 28.0) count++;", "if (edge[i] > 2.0) count++;")
    d1_reds = []
    for name in FRAME_NAMES[:4]:
        busy_ok, _, _, d = evaluate_frame(name, defect1_src)
        d1_reds.append(not busy_ok)
    check("defect/busyness-threshold reds", all(d1_reds),
          "busyness row red on %d/%d sampled frames" % (sum(d1_reds), len(d1_reds)))
    print("defect 1 (threshold 28->2): busyness reds on %d/%d sampled frames"
          % (sum(d1_reds), len(d1_reds)))

    # Defect 2: drop the smoothing pass out of gx. The lines row should red.
    defect2_src = plant(
        'var gx = sobelSmooth(sobelDerivative(data, w, h, "x"), w, h, "y");',
        'var gx = sobelDerivative(data, w, h, "x");')
    d2_reds = []
    for name in FRAME_NAMES[:4]:
        _, lines_ok, _, d = evaluate_frame(name, defect2_src)
        d2_reds.append(not lines_ok)
    check("defect/sobel-pass-dropped reds", all(d2_reds),
          "lines row red on %d/%d sampled frames" % (sum(d2_reds), len(d2_reds)))
    print("defect 2 (dropped Sobel pass): lines reds on %d/%d sampled frames"
          % (sum(d2_reds), len(d2_reds)))

    # Defect 3: narrow the mirror scan to the single column 0.5. The mirror-axis row should red
    # on every off-centre frame, and only those (a centred frame's true answer IS 0.5).
    defect3_src = plant(
        "var cLo = Math.floor(lo * W), cHi = Math.floor(hi * W);",
        "var cLo = Math.floor(0.5 * W), cHi = Math.floor(0.5 * W);")
    off_names = [n for n, _p in off_centre]
    d3_reds = []
    for name in off_names:
        _, _, mirror_ok, d = evaluate_frame(name, defect3_src)
        d3_reds.append(not mirror_ok)
        print("  defect 3 on %-16s off-centre pos=%.3f -> %s"
              % (name, dict(off_centre)[name], "RED" if not mirror_ok else "still green"))
    check("defect/mirror-scan-narrowed reds", all(d3_reds) and len(off_names) >= 3,
          "mirror-axis row red on %d/%d off-centre frames" % (sum(d3_reds), len(off_names)))
    print("defect 3 (mirror scan narrowed to 0.5): mirror-axis reds on %d/%d off-centre frames"
          % (sum(d3_reds), len(off_names)))

    # Confirmation: with defects removed, the same frames are green again (BASE_SRC == unmutated
    # source, already proven green in the correctness pass above; re-checked explicitly here).
    clean_ok = []
    for name in off_names:
        _, _, mirror_ok, _ = evaluate_frame(name, BASE_SRC)
        clean_ok.append(mirror_ok)
    check("defect/mirror-scan-narrowed clears once removed", all(clean_ok),
          "mirror-axis row green on %d/%d off-centre frames with the real source"
          % (sum(clean_ok), len(off_names)))

    print()
    failed = [r for r in results if r[1] == "FAIL"]
    for name, status, detail in results:
        print("%-6s %-45s %s" % (status, name, detail))
    print("\n%d checks, %d passed, %d failed" % (len(results), len(results) - len(failed),
                                                  len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
