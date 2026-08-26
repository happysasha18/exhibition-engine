#!/usr/bin/env python3
"""S-01 — the diagnostics-only crossing verdict panel.
Run: python3 tests/test_pass_verdict.py

Root: the tlvphotos plan наряд S-01. `engine/client/19-verdict.js` is the one file this наряд adds;
it draws a verdict panel that is invisible unless the address already carries
?pass=diagnostics:on — the key `01a-pass.js` already reads into the settings register — and, wired
into `engine/assemble_client.py`'s MANIFEST, offers three buttons ("огонь", "ок", "мимо") and a note
field after every real crossing between two works, and one "выгрузить" button that copies the whole
session's rows to the clipboard AND saves them as `verdicts-ГГГГ-ММ-ДД.json`, in the schema S-02
reads:

    { "walk": "<адрес маршрута>", "startedAt": "<ISO 8601>",
      "rows": [ { "n": 1, "from": "<id>", "to": "<id>", "road": "<дорога>", "cues": [...],
                  "durationMs": 6979, "verdict": "огонь|ок|мимо", "note": "<строка>" } ] }

WHAT THIS MEASURES, three rows, exactly the наряд's three "готово когда":

  0 · under the key, a real crossing between two works leaves the panel visible with three buttons
      (their exact labels), a note field and a dump button.
  1 · without the key, the same walk leaves no trace at all — no panel, no element of its own class,
      no diagnostic surface either.
  2 · the export — read off BOTH carriers, the clipboard write and the file the browser actually
      saved to disk — is one record naming the whole schema and nothing else, with the verdict and
      the note the row asked for.

RED BEFORE THE НАРЯД'S OWN EDIT: with `engine/client/19-verdict.js` absent from
`engine/assemble_client.py`'s MANIFEST, `#ex-verdict` never reaches the built client, so row 0 finds
no panel and fails outright, and row 2 finds no button to click and fails outright rather than being
skipped — a missing feature reds here, it is never quietly passed over. Row 1 is a negative that
already holds with nothing built yet; it keeps holding once the panel exists, which is what a route
walked WITHOUT the key must always show.
"""
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
FIXTURE = Path(__file__).resolve().parent / "fixture_pass_composed.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


TMP = Path(tempfile.mkdtemp(prefix="synth_verdict_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

BROWSER_ROWS = [
    "S-01 the panel stands under ?pass=diagnostics:on, with three buttons after a real crossing",
    "S-01 a route walked without the key leaves the panel, and every trace of it, absent",
    "S-01 the export — clipboard and the saved file alike — carries exactly the named schema",
]

RECORDS_ROUTE = "/api/pass/verdict-records"
RECORDS_CAP = 20
RECORDS_STORE = {}


def records_answer(raw_path):
    if not raw_path.startswith(RECORDS_ROUTE):
        return None
    ids = [i for i in parse_qs(urlparse(raw_path).query).get("ids", [""])[0].split(",") if i]
    if not ids or len(ids) > RECORDS_CAP:
        return (400, "text/plain", "bad request")
    out = {i: RECORDS_STORE[i] for i in ids if i in RECORDS_STORE}
    return (200, "application/json", json.dumps({"records": out}))


def put_records(base_dir, ids):
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


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


def wait_for(br, expr, timeout=15.0, step=0.2):
    """Poll a JS expression until it returns truthy (or the deadline) — no fixed-sleep races.
    15s of headroom: a road's own typed duration runs as long as 11000ms (pass-composer.js), so a
    budget shorter than that reads the panel before a real crossing has had time to land."""
    end = time.time() + timeout
    val = None
    while time.time() < end:
        val = br.evaluate(expr)
        if val:
            return val
        br.sleep(step)
    return val


def wait_ready(br, budget=150):
    for _ in range(budget):
        got = js(br, "if (!window.__exPass) return {st: null, held: 0};"
                     "var r = window.__exPass.report();"
                     "return {st: r.composer.state, held: r.records.held,"
                     " waves: r.records.waves, inflight: r.records.inflight};")
        if (got.get("st") == "read" and (got.get("waves") or 0) > 0
                and (got.get("inflight") or 0) == 0 and (got.get("held") or 0) > 1):
            return True
        br.sleep(0.2)
    return False


def enter(br, base, pass_arg=None, step=True):
    br.navigate(base + "/")
    br.clear_storage()
    br.navigate(base + "/" + (("?pass=" + pass_arg) if pass_arg else ""))
    br.sleep(0.8)
    if js(br, "return {has: !!document.querySelector('.exd-window')};")["has"]:
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
    if step:
        if pass_arg and "diagnostics:on" in pass_arg:
            wait_ready(br)
        br.key("ArrowDown")
        br.sleep(0.6)


CLIP_STUB = ("window.__copied=[];if(navigator.clipboard)navigator.clipboard.writeText="
             "(t)=>{window.__copied.push(t);return Promise.resolve();};")


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    # EVERY work of the fixture collection gets a record, not only the ids one particular door pick
    # happens to hang — a fresh entry deals a random SPREAD off a collection wider than it (24
    # works, a spread of 10), so an id list captured off one hang can miss entirely the ids the
    # very next hang shows. Reading the collection's own content file sidesteps the mismatch rather
    # than chasing it with a second query after the fact.
    all_ids = [w["id"] for w in json.loads(
        (ROOT / "tests" / "fixture_content" / "content_tags.json").read_text(encoding="utf-8"))]
    recorded = list(put_records(TMP, all_ids))

    with serve(TMP, answer=records_answer) as base:
        # ---- rows 0 and 2 · under the key, a real crossing and its export ---------------------
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            enter(br, base, "diagnostics:on", step=True)
            # The dock this step aims for lands off the composer's own async road (the record
            # wave, the composer's file) — `wait_ready` only waits for that machinery to be IN
            # PLACE, not for THIS step's own landing to have reached it, so the panel is polled
            # for the condition itself — shown AND pending — rather than assumed the instant the
            # key is up, or after some fixed sleep too short for the road actually picked.
            wait_for(br, "(()=>{var p=document.getElementById('ex-verdict');"
                         "return !!(p && p.hidden===false && p.dataset.pending==='1');})()")

            panel = js(br, "var p = document.getElementById('ex-verdict');"
                          "if (!p) return {present: false};"
                          "var btns = [].slice.call(p.querySelectorAll('.exv-btn'))"
                          ".map(function (b) { return b.textContent; });"
                          "return {present: true, hidden: p.hidden,"
                          " pending: p.dataset.pending, btns: btns,"
                          " hasNote: !!p.querySelector('.exv-note'),"
                          " hasDump: !!p.querySelector('.exv-dump')};")
            check(BROWSER_ROWS[0],
                  panel.get("present") and panel.get("hidden") is False
                  and panel.get("pending") == "1"
                  and panel.get("btns") == ["огонь", "ок", "мимо"]
                  and panel.get("hasNote") and panel.get("hasDump"),
                  f"panel: {json.dumps(panel, ensure_ascii=False)}")

            # ---- row 2 · a verdict and a note, then the export ----------------------------------
            if not (panel.get("present") and panel.get("btns") and panel.get("hasDump")):
                check(BROWSER_ROWS[2], False,
                      f"no panel/buttons to drive an export from: "
                      f"{json.dumps(panel, ensure_ascii=False)}")
            else:
                br.evaluate("document.querySelector('.exv-note').value = 'нравится';")
                br.click('.exv-btn[data-verdict="ok"]', settle=0.3)
                br.click(".exv-dump", settle=0.5)

                copied_raw = br.evaluate(
                    "window.__copied && window.__copied.length "
                    "? window.__copied[window.__copied.length - 1] : null")
                copied = json.loads(copied_raw) if copied_raw else None

                saved = []
                end = time.time() + 6
                while time.time() < end and not saved:
                    saved = [f for f in Path(br._profile).glob("verdicts-*.json")
                             if not f.name.endswith(".crdownload")]
                    if not saved:
                        time.sleep(0.2)
                on_disk = json.loads(saved[0].read_text(encoding="utf-8")) if saved else None

                named = {"n", "from", "to", "road", "cues", "durationMs", "verdict", "note"}
                row = (copied.get("rows") or [{}])[0] if copied else {}
                ok = bool(copied) and bool(on_disk) and on_disk == copied
                if ok:
                    ok = (set(copied.keys()) == {"walk", "startedAt", "rows"}
                          and isinstance(copied["walk"], str) and bool(copied["walk"])
                          and isinstance(copied["startedAt"], str)
                          and len(copied["rows"]) == 1
                          and set(row.keys()) == named
                          and row["n"] == 1
                          and row["from"] in recorded and row["to"] in recorded
                          and isinstance(row["cues"], list)
                          and isinstance(row["durationMs"], (int, float))
                          and row["verdict"] == "ок"
                          and row["note"] == "нравится")
                check(BROWSER_ROWS[2], ok,
                      f"clipboard={json.dumps(copied, ensure_ascii=False)[:400]} "
                      f"file-matches-clipboard="
                      f"{on_disk == copied if (copied and on_disk) else False} "
                      f"saved-files={[f.name for f in saved]}")

        # ---- row 1 · no trace at all without the key ------------------------------------------
        with Browser(width=1280, height=900) as br2:
            enter(br2, base, None, step=True)
            trace = js(br2, "return {panel: !!document.getElementById('ex-verdict'),"
                            " marked: document.querySelectorAll('[class*=\"exv-\"]').length,"
                            " global: typeof window.__exPass};")
            check(BROWSER_ROWS[1],
                  trace.get("panel") is False and trace.get("marked") == 0
                  and trace.get("global") == "undefined",
                  f"trace left on a plain walk: {json.dumps(trace, ensure_ascii=False)}")

shutil.rmtree(TMP, ignore_errors=True)

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
