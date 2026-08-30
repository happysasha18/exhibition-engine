#!/usr/bin/env python3
"""Focused product-direction contract for the immersive crossing seam."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import assemble_client  # noqa: E402

PASS = (ROOT / "engine/client/01a-pass.js").read_text(encoding="utf-8")
RENDER = (ROOT / "engine/client/14-walk-render.js").read_text(encoding="utf-8")
MOTION = (ROOT / "engine/client/15-motion.js").read_text(encoding="utf-8")
SERIES = (ROOT / "engine/client/16-renderhang-series.js").read_text(encoding="utf-8")
SERVED = (ROOT / "engine/assets/exhibition.js").read_text(encoding="utf-8")

checks = []


def check(name, ok, detail=""):
    checks.append((name, bool(ok), detail))


check("served client is assembled from the reviewed fragments",
      SERVED == assemble_client.assemble())

check("every crossing is derived at runtime from two per-work records",
      "workRecordA: a" in PASS and "workRecordB: b" in PASS
      and "passComposer.passageFor(request)" in PASS
      and "function passScoreFor" not in PASS and "passScoreTables" not in PASS
      and "passReader" not in PASS)

check("door, direction, route role, memory and capability all reach the runtime request",
      "passDoorSalt()" in PASS and 'direction: forward ? "a-to-b" : "b-to-a"' in PASS
      and "req.routeRole = role" in PASS and "req.sessionMemory = edge.memory" in PASS
      and 'quality: passGet("qualityTier")' in PASS)

check("first passage prewarms composer, records and drawing layer before a gesture",
      all(x in RENDER for x in ("passComposerOpen();", "passRecordsAskFor(slice);", "passOpen();")))

interaction_region = PASS[PASS.index("const passInteraction ="):PASS.index("function passWhere(")]
check("one passive host interaction signal carries pointer, tap and spring without stealing input",
      "interaction: interaction" in PASS and "passInteractionRest" in interaction_region
      and "p.taps += 1" in interaction_region and "preventDefault" not in interaction_region
      and interaction_region.count("passive: true") >= 4
      and 'kind: "touch"' in MOTION and 'kind: "wheel"' in MOTION and 'kind: "key"' in MOTION)

COMPOSER = (ROOT / "engine/assets/pass-composer.js").read_text(encoding="utf-8")
check("four fitting materials turn the passive hand signal into a bounded middle-only accompaniment",
      'var pointerHandle = { weave: "press", parquet: "spin", planet: "turn",' in COMPOSER
      and '{ source: "pointer", channel: "x" }' in COMPOSER
      and 'at: 0, value: 0' in COMPOSER and 'at: 1, value: 0' in COMPOSER,
      "interaction may alter a living middle but must add zero at both doors")

check("route selection reads a whole-passage scene and its expressive handles",
      "function passSceneOf(passage)" in PASS and "function passRouteNovelty(scene)" in PASS
      and '"control:" + key' in PASS and "passSetDistance(scene.controls" in PASS
      and "if (best !== null)" in PASS and "return passage.score" in PASS)

check("diagnostics expose the applied stack for every remembered route edge",
      "passRoutePlayed.push" in PASS and "stack: (row.applied.cues || [])" in PASS
      and "played: passRoutePlayed.slice()" in PASS)

check("a side room opened during a crossing binds the work actually docked",
      "const crossing = passRunning();" in SERIES and "idx = seriesOfWork(focusedId);" in SERIES
      and "if (!S) return;" in SERIES)

failed = 0
for name, ok, detail in checks:
    print(("PASS" if ok else "FAIL"), name, ("— " + detail) if detail else "")
    if not ok:
        failed += 1
print(f"\n{len(checks) - failed} passed / {failed} failed")
raise SystemExit(1 if failed else 0)
