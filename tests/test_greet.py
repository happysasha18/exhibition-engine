#!/usr/bin/env python3
"""The greeting (EX-GREET / EX-GREET-BAKE) — adapted for exhibition-engine synthetic fixture.
Run: python tests/test_greet.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
import engine_build  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
LANGS_V1 = ["ru", "en", "he", "de", "fr", "es", "uk"]
DAYPARTS = ["night", "morning", "day", "evening"]

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
TMP = Path(tempfile.mkdtemp(prefix="synth_greet_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

EXDATA = json.loads((TMP / "exhibition_data.json").read_text())
CONFIG_PATH = TMP / "config.json"
CONFIG0 = CONFIG_PATH.read_text()
INDEX_RAW = (TMP / "index.html").read_text(encoding="utf-8")
SPREAD = json.loads(CONFIG0)["exhibition"]["spread_size"]

GREET = EXDATA.get("greet") or {}
LANGS = GREET.get("langs") or {}

# ---------------------------------------------------------------- data row

titles = [(w.get("title") or "").strip() for w in EXDATA["works"]]
titles = [t for t in titles if len(t) >= 4]
all_strings = []
for L in LANGS.values():
    all_strings += [L.get("ask", "")]
    for part in (L.get("greet") or {}).values():
        all_strings += list(part)
shape_ok = (
    GREET.get("fallback") == "en"
    and all(code in LANGS for code in LANGS_V1)
    and all(
        (LANGS[code].get("ask") or "").strip() and "skip" not in LANGS[code]
        and (LANGS[code].get("exit") or "").strip()
        and "{n}" in (LANGS[code].get("more") or "")
        and (LANGS[code].get("q_more") or "").strip()
        and (LANGS[code].get("q_spent") or "").strip()
        and all((LANGS[code].get("greet") or {}).get(p) for p in DAYPARTS)
        and all(s.strip() for p in DAYPARTS for s in LANGS[code]["greet"][p])
        for code in LANGS_V1
    )
)
clean = (
    not any(t in s for t in titles for s in all_strings)
    and not any("AX-" in s for s in all_strings)
)
check("Greet block baked: seven langs × four dayparts, ask each (skip RETIRED), fallback=en, knob in config",
      shape_ok and clean and json.loads(CONFIG0)["exhibition"].get("greeting") == "ask",
      f"langs={sorted(LANGS)} shape={shape_ok} clean={clean} "
      f"knob={json.loads(CONFIG0)['exhibition'].get('greeting')}")

# ---------------------------------------------------------------- gen command contract

# CACHE points at the fixture's greetings.json (engine has no data/ at root)
CACHE = engine_build.FIXTURE / "data" / "greetings.json"
before = CACHE.read_bytes()
env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
r_nokey = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "gen_greetings.py"),
     "--keychain-service", "tlv-test-no-such-key"],
    capture_output=True, text=True, env=env)
r_check = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "gen_greetings.py"), "--check"],
    capture_output=True, text=True, env=env)
# a malformed cache must FAIL --check
bad = json.loads(CACHE.read_text())
del bad["langs"]["ru"]["greet"]["night"]
BADF = TMP / "greetings_bad.json"
BADF.write_text(json.dumps(bad))
r_bad = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "gen_greetings.py"),
     "--check", "--cache", str(BADF)],
    capture_output=True, text=True, env=env)
check("EX-GREET-BAKE gen contract: keyless run refuses + cache untouched; --check green; broken cache red",
      r_nokey.returncode != 0
      and "key" in (r_nokey.stderr + r_nokey.stdout).lower()
      and CACHE.read_bytes() == before
      and r_check.returncode == 0
      and r_bad.returncode != 0,
      f"nokey_rc={r_nokey.returncode} untouched={CACHE.read_bytes() == before} "
      f"check_rc={r_check.returncode} bad_rc={r_bad.returncode} "
      f"err={(r_nokey.stderr or r_nokey.stdout)[:120]!r}")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "EX-GREET greets in the visitor's language × hour, ABOVE the ask (B); the ask follows; he = RTL",
    "EX-GREET fallback: uncovered language meets English; legacy iw meets Hebrew",
    "EX-GREET belongs to the cold arrival: ⟲ door does not re-greet; Back to the cold step does",
    "EX-GREET missing block degrades to built-ins (door stands, entry works)",
    "EX-GREET placement is config: top / off / unrecognized→default",
    "EX-GREET phone: greeting + windows + the ask inside the first viewport",
    "EX-GREET variant is date-seeded (same day = same line)",
    "EX-GREET the closing screen speaks the visitor's language (exit — never «к двери»; «{n} more»; he=RTL)",
]

GREET_STATE = (
    "(()=>{const g=document.getElementById('exd-greet');"
    "const a=document.querySelector('.exd-ask');"
    "const d=document.getElementById('ex-door');"
    "return {vis:!!g&&!g.hidden&&g.textContent.trim()!=='',text:g?g.textContent.trim():'',"
    "ask:a?a.textContent.trim():'',"
    "dir:d?d.getAttribute('dir'):null,lang:d?d.getAttribute('lang'):null,"
    "above:(g&&a&&!g.hidden)?g.getBoundingClientRect().bottom<=a.getBoundingClientRect().top+1:null,"
    "atDoor:document.body.classList.contains('ex-door')};})()"
)

check("EX-GREET lives only in the live face (no greeting markup/strings in served index.html)",
      "exd-greet" not in INDEX_RAW
      and not any(s and s in INDEX_RAW for L in LANGS.values()
                  for p in DAYPARTS for s in (L.get("greet") or {}).get(p, [])))

if not shape_ok:
    for r in BROWSER_ROWS:
        check(r, False, "greet block not baked — implementation missing")
elif not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    RU = LANGS["ru"]
    HE = LANGS["he"]
    EN = LANGS["en"]

    def fresh(br, base):
        br.navigate(base + "/")
        br.clear_storage()
        br.evaluate("localStorage.setItem('ex-tempo','0.05')")
        br.reload()
        br.sleep(1.0)

    def to_fin(br):
        br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
        br.sleep(0.3)

    # 0 · language × hour, placement B, localized ask, RTL
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 21)
            fresh(br, base)
            ru_state = br.evaluate(GREET_STATE)
        with Browser(width=1280, height=900) as br:
            br.pretend("he", 3)
            fresh(br, base)
            he_state = br.evaluate(GREET_STATE)
        check(BROWSER_ROWS[0],
              ru_state["atDoor"] and ru_state["vis"]
              and ru_state["text"] in RU["greet"]["evening"]
              and ru_state["above"] is True
              and ru_state["ask"] == RU["ask"]
              and he_state["vis"] and he_state["text"] in HE["greet"]["night"]
              and he_state["dir"] == "rtl" and he_state["lang"] == "he"
              and he_state["ask"] == HE["ask"],
              f"ru={ru_state} he={he_state}")

        # 1 · fallback + legacy alias
        with Browser(width=1280, height=900) as br:
            br.pretend("pt-BR", 10)
            fresh(br, base)
            pt_state = br.evaluate(GREET_STATE)
        with Browser(width=1280, height=900) as br:
            br.pretend("iw", 10)
            fresh(br, base)
            iw_state = br.evaluate(GREET_STATE)
        check(BROWSER_ROWS[1],
              pt_state["vis"] and pt_state["text"] in EN["greet"]["morning"]
              and pt_state["ask"] == EN["ask"]
              and iw_state["ask"] == HE["ask"] and iw_state["dir"] == "rtl",
              f"pt={pt_state} iw={iw_state}")

        # 2 · cold-arrival only: the reopened door keeps the ask localized, no greeting; Back re-greets
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 21)
            fresh(br, base)
            cold = br.evaluate(GREET_STATE)
            br.click(".exd-window:nth-child(1)", settle=1.0)
            to_fin(br)
            br.click("#ex-return", settle=0.8)
            reopened = br.evaluate(GREET_STATE)
            br.evaluate("history.back()")
            br.sleep(0.8)
            back_walk = br.evaluate("document.body.classList.contains('ex-door')")
            br.evaluate("history.back()")
            br.sleep(0.8)
            back_cold = br.evaluate(GREET_STATE)
            check(BROWSER_ROWS[2],
                  cold["vis"]
                  and reopened["atDoor"] and not reopened["vis"]
                  and reopened["ask"] == RU["ask"]
                  and back_walk is False
                  and back_cold["atDoor"] and back_cold["vis"],
                  f"cold={cold['vis']} reopened={reopened} back_walk_at_door={back_walk} "
                  f"back_cold={back_cold['vis']}")

        # 4 · placement is config
        cfg = json.loads(CONFIG0)
        cfg["exhibition"]["greeting"] = "top"
        CONFIG_PATH.write_text(json.dumps(cfg))
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 21)
            fresh(br, base)
            top_state = br.evaluate(GREET_STATE)
            top_class = br.evaluate("document.getElementById('ex-door').classList.contains('greet-top')")
        cfg["exhibition"]["greeting"] = "off"
        CONFIG_PATH.write_text(json.dumps(cfg))
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 21)
            fresh(br, base)
            off_state = br.evaluate(GREET_STATE)
        cfg["exhibition"]["greeting"] = "banana"
        CONFIG_PATH.write_text(json.dumps(cfg))
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 21)
            fresh(br, base)
            bad_state = br.evaluate(GREET_STATE)
        CONFIG_PATH.write_text(CONFIG0)
        check(BROWSER_ROWS[4],
              top_state["vis"] and top_class
              and off_state["atDoor"] and not off_state["vis"]
              and bad_state["vis"] and bad_state["above"] is True,
              f"top={top_state['vis']}/{top_class} off={off_state['vis']} bad={bad_state['vis']}")

        # 5 · phone: nothing pushed out of the first viewport
        with Browser(width=375, height=720) as br:
            br.pretend("ru-RU", 21)
            fresh(br, base)
            ph = br.evaluate(
                "(()=>{const ih=window.innerHeight,iw=window.innerWidth;"
                "const g=document.getElementById('exd-greet').getBoundingClientRect();"
                "const a=document.querySelector('.exd-ask').getBoundingClientRect();"
                "const ws=[...document.querySelectorAll('.exd-window')].map(w=>w.getBoundingClientRect());"
                "return {greetIn:g.top>=0&&g.bottom<=ih,askIn:a.top>=0&&a.bottom<=ih,"
                "fit:ws.every(r=>r.right<=iw+1&&r.left>=-1&&r.bottom<=ih)};})()")
            check(BROWSER_ROWS[5], ph["greetIn"] and ph["askIn"] and ph["fit"], f"{ph}")

        # 6 · date-seeded variant: two loads the same day agree
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 21)
            fresh(br, base)
            t1 = br.evaluate(GREET_STATE)["text"]
            br.clear_storage()
            br.reload(); br.sleep(1.0)
            t2 = br.evaluate(GREET_STATE)["text"]
            check(BROWSER_ROWS[6],
                  t1 != "" and t1 == t2 and len(RU["greet"]["evening"]) >= 2,
                  f"t1={t1!r} t2={t2!r} variants={len(RU['greet']['evening'])}")

        # 7 · the closing screen speaks the visitor's language
        FIN_STATE = (
            "(()=>{const f=document.getElementById('exh-fin');"
            "const q=f.querySelector('.q');const m=document.getElementById('ex-unfold');"
            "const b=document.getElementById('ex-return');"
            "return {q:q?q.textContent.trim():'',more:m?m.textContent.trim():'',"
            "back:b?b.textContent.trim():'',dir:f.getAttribute('dir'),"
            "lang:f.getAttribute('lang')};})()"
        )

        def fin_of(lang):
            with Browser(width=1280, height=900) as br:
                br.pretend(lang, 15)
                fresh(br, base)
                br.click(".exd-window:nth-child(1)", settle=1.0)
                to_fin(br)
                return br.evaluate(FIN_STATE)

        en_fin, ru_fin, he_fin = fin_of("en-US"), fin_of("ru-RU"), fin_of("he")
        n_step = str(json.loads(CONFIG0)["exhibition"]["unfold_step"])
        check(BROWSER_ROWS[7],
              en_fin["back"] == EN.get("exit") and "к двери" not in en_fin["back"]
              and en_fin["q"] == EN.get("q_more")
              and en_fin["more"].startswith(EN.get("more", "").replace("{n}", n_step))
              and ru_fin["back"] == RU.get("exit") == "выход"
              and ru_fin["more"].startswith(RU.get("more", "").replace("{n}", n_step))
              and he_fin["back"] == HE.get("exit")
              and he_fin["dir"] == "rtl" and he_fin["lang"] == "he",
              f"en={en_fin} ru={ru_fin} he={he_fin}")

    # 3 · missing greet block → built-ins, entry works
    BROKEN = Path(tempfile.mkdtemp(prefix="synth_greet_broken_"))
    shutil.copytree(TMP, BROKEN, dirs_exist_ok=True)
    exd = json.loads((BROKEN / "exhibition_data.json").read_text())
    exd.pop("greet", None)
    (BROKEN / "exhibition_data.json").write_text(json.dumps(exd, ensure_ascii=False))
    with serve(BROKEN) as base2, Browser(width=1280, height=900) as br2:
        br2.pretend("ru-RU", 21)
        br2.navigate(base2 + "/")
        br2.evaluate("localStorage.clear()")
        br2.evaluate("localStorage.setItem('ex-tempo','0.05')")
        br2.reload(); br2.sleep(1.2)
        st = br2.evaluate(GREET_STATE)
        br2.click(".exd-window:nth-child(1)", settle=1.0)
        n = br2.evaluate("document.querySelectorAll('.exh-frame').length")
        check(BROWSER_ROWS[3],
              st["atDoor"] and not st["vis"]
              and st["ask"] == "что ближе сейчас?"
              and n == SPREAD,
              f"state={st} frames={n}")


# ---------------------------------------------------------------- report
shutil.rmtree(TMP, ignore_errors=True)
try:
    shutil.rmtree(BROKEN, ignore_errors=True)
except NameError:
    pass

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if status != "PASS" and detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
