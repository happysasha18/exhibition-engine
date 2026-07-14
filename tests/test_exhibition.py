#!/usr/bin/env python3
"""Adaptive exhibition (EX) tests — adapted for exhibition-engine synthetic fixture.
One test per TEST_MATRIX "Adaptive exhibition" row.

Run: python tests/test_exhibition.py   (exit 0 = all green)
"""
import json
import re
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"

AXIS_ID_RE = re.compile(r"\b(?:ax|inv)-\d")
READOUT_WORDS = ["confidence", "cosine", "centroid", "kinship distance", "numeric axis"]
READOUT_RE = re.compile(r"\b\w+\s*[:=]\s*-?\d*\.\d+\b")
TS_FORBIDDEN = ["data-story", "reveal story", "reveal-story", "told-story", "told story", "narrative"]

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once

TMP = Path(tempfile.mkdtemp(prefix="synth_ex_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

INDEX = TMP / "index.html"
EXDATA = json.loads((TMP / "exhibition_data.json").read_text())
WORKS = EXDATA["works"]
VEC = EXDATA["v"]
CONFIG_PATH = TMP / "config.json"
CONFIG0 = CONFIG_PATH.read_text()
EXCFG = json.loads(CONFIG0)["exhibition"]
SPREAD = EXCFG["spread_size"]
UNFOLD = EXCFG["unfold_step"]

# a SECOND bake with the told story ON (ai_story) — the plot-per-portion drive (EX-STORY / DELTA-16,
# mirrored from an instance). The default bake above ships ai_story false; this one flips the
# story on so the client's STORY_ON path (tellStory) runs, and we STUB /api/story in the browser so
# the drive needs no worker. The built client is byte-identical to the default bake's.
STORY_ON = Path(tempfile.mkdtemp(prefix="synth_ex_story_"))
build_site.OUT = STORY_ON
build_site.build(SITE_URL, enable=["ai_story"])
build_site.OUT = TMP
STORY_VER = json.loads((STORY_ON / "exhibition_data.json").read_text())["version"]
STORY_WORKS = json.loads((STORY_ON / "exhibition_data.json").read_text())["works"]
STORY_JS = (STORY_ON / "exhibition.js").read_text(encoding="utf-8")


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def nearest_ids(pick_id, k):
    others = [w["id"] for w in WORKS if w["id"] != pick_id]
    others.sort(key=lambda i: dist(VEC[i], VEC[pick_id]))
    return others[:k]


# ---------------------------------------------------------------- HTML parse

class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metas, self.links, self.h1, self.imgs, self.anchors = [], [], [], [], []
        self.title = ""
        self._in_title = False
        self._in_h1 = None
        self._in_ld = False
        self.ldjson = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta":
            self.metas.append(d)
        elif tag == "link":
            self.links.append(d)
        elif tag == "a":
            self.anchors.append(d)
        elif tag == "img":
            self.imgs.append(d)
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = {"attrs": d, "text": ""}
        elif tag == "script" and d.get("type") == "application/ld+json":
            self._in_ld = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1" and self._in_h1 is not None:
            self.h1.append(self._in_h1["text"].strip())
            self._in_h1 = None
        elif tag == "script":
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_h1 is not None:
            self._in_h1["text"] += data
        if self._in_ld:
            self.ldjson.append(data)

    def meta(self, key):
        for m in self.metas:
            if m.get("property") == key or m.get("name") == key:
                return m.get("content", "")
        return None

    def canonical(self):
        for l in self.links:
            if l.get("rel") == "canonical":
                return l.get("href")
        return None


P = Extract()
P.feed(INDEX.read_text(encoding="utf-8"))
INDEX_RAW = INDEX.read_text(encoding="utf-8")


# ================================================================ STATIC rows

work_links = [a["href"] for a in P.anchors if (a.get("href") or "").startswith("/w/")]
work_ids_linked = len(work_links)
try:
    ld = json.loads("".join(P.ldjson))
    ld_types = json.dumps(ld)
    has_ld = ("WebSite" in ld_types) or ("CollectionPage" in ld_types)
except Exception:
    has_ld = False
og_image = P.meta("og:image") or ""
check("INV-25(a) JS-off crawlable face (h1+intro+all work links+JSON-LD+abs og:image+canonical)",
      bool(P.h1 and P.h1[0])
      and work_ids_linked == len(WORKS)
      and has_ld
      and og_image.startswith("http")
      and bool(P.meta("og:title"))
      and (P.canonical() or "").startswith("http"),
      f"h1={P.h1[:1]} links={work_ids_linked}/{len(WORKS)} ld={has_ld} ogimg={og_image[:40]}")

sm = ET.parse(TMP / "sitemap.xml").getroot()
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = [e.text for e in sm.findall(".//s:loc", ns)]
robots = (TMP / "robots.txt").read_text().lower()
check("INV-24 sitemap lists exhibition root `/` exactly once + robots→sitemap",
      locs.count(f"{SITE_URL}/") == 1 and "sitemap.xml" in robots,
      f"root count={locs.count(f'{SITE_URL}/')}")

low_raw = INDEX_RAW.lower()
# EX-STORY landed: the told story is now a real client+edge feature, so the client JS legitimately
# carries its code. The standing INV-1 invariant, though, HOLDS and is what this row guards: the
# narrator's words are client-rendered and silent when off — they must NEVER appear in the crawlable
# served HTML (no told-story text, no narrative prose baked into a static byte).
check("EX-STORY / INV-1 — no told-story text or narrative prose in the served exhibition HTML",
      not any(t in low_raw for t in TS_FORBIDDEN),
      f"hits={[t for t in TS_FORBIDDEN if t in low_raw]}")

attr_vals = " ".join(v or "" for a in (P.anchors + P.imgs + P.metas) for v in a.values()).lower()
data_star = re.findall(r'data-[a-z-]+="([^"]*)"', INDEX_RAW)
vector_in_dom = any(re.search(r"\d+\.\d+.*\d+\.\d+", d) for d in data_star)
readout = (AXIS_ID_RE.search(low_raw) or any(w in low_raw for w in READOUT_WORDS)
           or READOUT_RE.search(attr_vals) or vector_in_dom)
check("INV-1 on EX — no axis name/score/confidence in served exhibition HTML/attrs/data-*",
      not readout,
      f"axis_id={bool(AXIS_ID_RE.search(low_raw))} words={[w for w in READOUT_WORDS if w in low_raw]} vec_in_data={vector_in_dom}")


# ============================================================ EX-STORY plot-per-portion (DELTA-16)
# Mirrored from an instance. Each opened portion of works is its own PLOT: the follow-on «ещё N»
# asks /api/story for ONLY the newly opened portion's ordered ids (never the grown 0..shown set), so a
# line already read is never re-requested and never shifts; a portion counts as told only once its plot
# has come back, so a refused/failed portion stays OWED and is re-asked at the next natural beat (a
# further unfold or a return to the walk); no portion is ever named a «part N» of another; and a mid-
# visit language switch keeps already-told lines in their first tongue (verified: the engine's respeak()
# re-labels chrome only and never touches STORYLINES, so a told line byte-stands; a portion opened after
# the switch reads viewerLang() live and gets the new tongue).
PORTION_ROWS = [
    "EX-STORY «ещё N» asks ONLY the newly opened portion's ids (not the grown set)",
    "EX-STORY a served follow-on: the new works speak, and no already-read line is re-requested (byte-stands)",
    "EX-STORY-EDGE a refused follow-on stays owed — key not burned, the next return re-asks and serves",
    "EX-STORY no «part N» / «часть N» naming rides any surface (plaque, finale, controls)",
    "EX-STORY a return to the walk re-shows byte-identical told lines (a cache hit under the reproduced key)",
]

# PORTION_ROWS[3] (no-«part N»): a standing string lint over the built client — no portion is ever
# named a "part two" of another on any surface (EX-STORY plot-per-portion). Model-free, runs even when
# Chrome is absent. This can never go red against HEAD — the naming was never added; it is the ratchet
# that keeps it out.
_part_naming = re.compile(r"part\s*(?:two|three|\d+)|часть\s*\d|часть\s*(?:втор|треть)", re.I)
_named = _part_naming.findall(STORY_JS)
check(PORTION_ROWS[3], not _named,
      f"a «part N» naming string rides exhibition.js: {_named!r}" if _named else "")


# ================================================================ BROWSER rows

BROWSER_ROWS = [
    "INV-25(b) JS-on live face arrives — cold visitor meets the DOOR, static hidden",
    "EX-ALL tombstone — no full-dump control; static index stays hidden while live",
    "INV-25 FOUC guard — pre-paint hide in head + css rule + static hidden while live",
    "INV-1 on EX live DOM — caption speaks his words only, no axis readout",
    "INV-25/CS-8 broken walk data → static face returns, never a blank page",
    "EX-CAPTION the fact line reads in the UI face at weight >= 500 (legibility)",
]

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
    for r in PORTION_ROWS[:3] + PORTION_ROWS[4:]:       # [3] the no-«part N» lint ran model-free above
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base, Browser(width=1280, height=900) as br:
        br.navigate(base + "/")
        br.clear_storage()
        br.evaluate("localStorage.setItem('ex-tempo','0.05')")
        br.reload(); br.sleep(1.0)
        st = br.evaluate(
            "(()=>{return {live:document.body.classList.contains('ex-live'),"
            "door:document.body.classList.contains('ex-door'),"
            "staticShown:getComputedStyle(document.getElementById('ex-static')).display!=='none'};})()")
        check(BROWSER_ROWS[0], st["live"] and st["door"] and not st["staticShown"], f"{st}")

        br.click(".exd-window:nth-child(1)", settle=1.0)
        tomb = br.evaluate(
            "(()=>{return {allBtn:!!document.getElementById('ex-all'),"
            "live:document.body.classList.contains('ex-live'),"
            "staticShown:getComputedStyle(document.getElementById('ex-static')).display!=='none'};})()")
        check(BROWSER_ROWS[1], not tomb["allBtn"] and tomb["live"] and not tomb["staticShown"], f"{tomb}")

        raw_head = INDEX_RAW.split("</head>")[0]
        guard_in_head = ('classList.add("js")' in raw_head)
        css_rule = "html.js #ex-static" in (TMP / "exhibition.css").read_text()
        check(BROWSER_ROWS[2], guard_in_head and css_rule and not tomb["staticShown"],
              f"head_guard={guard_in_head} css_rule={css_rule} hidden_live={not tomb['staticShown']}")

        br.evaluate("document.querySelectorAll('.exh-frame')[1].scrollIntoView()")
        br.sleep(0.6)
        live_text = br.evaluate("document.body.innerText") or ""
        cap_ok = br.evaluate(
            "(()=>{const c=document.getElementById('exh-cap');if(!c)return false;"
            "const t=c.querySelector('.title');return !!t && t.textContent.trim().length>0;})()")
        low = live_text.lower()
        check(BROWSER_ROWS[3],
              cap_ok and not AXIS_ID_RE.search(low)
              and not any(w in low for w in READOUT_WORDS) and not READOUT_RE.search(low),
              f"cap={cap_ok} axis_id={bool(AXIS_ID_RE.search(low))}")

        # EX-CAPTION legibility: the fact line (place · year · medium) resolves to the UI family (the
        # content's --ui token — Helvetica in the fixture) at font-weight ≥ 500, browser-computed, not
        # the mono face — a Latin monospace hands a non-Latin script's glyphs to a thin fallback.
        meta = br.evaluate(
            "(()=>{const e=document.querySelector('#exh-cap .meta');if(!e)return null;"
            "const cs=getComputedStyle(e);return {family:cs.fontFamily,"
            "weight:parseInt(cs.fontWeight,10),size:parseFloat(cs.fontSize)};})()")
        check(BROWSER_ROWS[5],
              bool(meta) and "helvetica" in (meta["family"] or "").lower()
              and "mono" not in (meta["family"] or "").lower()
              and int(meta["weight"]) >= 500 and float(meta["size"]) >= 12,
              f"meta={meta}")

    BROKEN = Path(tempfile.mkdtemp(prefix="synth_ex_broken_"))
    import shutil as _sh
    _sh.copytree(TMP, BROKEN, dirs_exist_ok=True)
    (BROKEN / "exhibition_data.json").unlink()
    with serve(BROKEN) as base2, Browser(width=1280, height=900) as br2:
        br2.navigate(base2 + "/")
        br2.sleep(3.0)
        rec = br2.evaluate(
            "(()=>{return {live:document.body.classList.contains('ex-live'),"
            "staticShown:getComputedStyle(document.getElementById('ex-static')).display!=='none',"
            "links:document.querySelectorAll('#ex-static a[href^=\"/w/\"]').length};})()")
        check(BROWSER_ROWS[4],
              not rec["live"] and rec["staticShown"] and rec["links"] == len(WORKS), f"{rec}")

    # ---- EX-STORY plot-per-portion, driven in the flesh (DELTA-16) ---------------------------
    # A real walk behind the story-ON bundle: seed the walk state, open «ещё N», leave to the door
    # and return. Two fetch stubs record every /api/story body (window.__storyBodies), so the suite
    # reads WHICH ids each portion actually asked (the plot-per-portion law's own guarantee). The
    # stub serves a deterministic line per id ('told <id>'), modelling the edge's forever-cache: a
    # re-ask under the reproduced key returns byte-identical text.
    STUB_STORY_REC = """
    window.__storyCalls=0; window.__storyBodies=[];
    (function(){const _f=window.fetch;
    window.fetch=function(u,o){
      if(String(u).indexOf('/api/story')>=0){
        window.__storyCalls++;
        let ids=[]; try{ids=JSON.parse(o.body).ids;}catch(e){}
        window.__storyBodies.push(ids.map(String));
        return Promise.resolve(new Response(JSON.stringify({
          story_variant:'B', lines: ids.map(id=>({id:String(id),line:'told '+id,source:'facts'}))
        }),{status:200,headers:{'Content-Type':'application/json'}}));
      }
      return _f.apply(this,arguments);};})();
    """
    # the edge refuses the FIRST follow-on (call #2 — a busy/capped/429 hour) with a 404, then serves
    # every later ask. Under the plot-per-portion law the refused portion's key is never burned, so it
    # stays owed and the next natural beat (a return to the walk) re-asks it and serves.
    STUB_REFUSE_FOLLOWON = """
    window.__storyCalls=0; window.__storyBodies=[];
    (function(){const _f=window.fetch;
    window.fetch=function(u,o){
      if(String(u).indexOf('/api/story')>=0){
        window.__storyCalls++;
        let ids=[]; try{ids=JSON.parse(o.body).ids;}catch(e){}
        window.__storyBodies.push(ids.map(String));
        if(window.__storyCalls===2){ return Promise.resolve(new Response('no story',{status:404})); }
        return Promise.resolve(new Response(JSON.stringify({
          story_variant:'B', lines: ids.map(id=>({id:String(id),line:'told '+id,source:'facts'}))
        }),{status:200,headers:{'Content-Type':'application/json'}}));
      }
      return _f.apply(this,arguments);};})();
    """
    STORY_PICK = str(STORY_WORKS[0]["id"])

    def story_walk(br, base):                            # seed the walk state, land in the walk (no door)
        br.navigate(base + "/")
        br.evaluate("localStorage.clear();sessionStorage.clear()")
        br.evaluate("localStorage.setItem('ex-tempo','0.2')")
        br.evaluate("localStorage.setItem('ex.exhibition', JSON.stringify({v:%s, pick:%s, shown:%d}))"
                    % (json.dumps(STORY_VER), json.dumps(STORY_PICK), SPREAD))
        br.reload()
        br.sleep(1.5)
        br.evaluate("document.querySelector('.exh-frame').scrollIntoView({behavior:'instant'})")
        br.sleep(0.8)

    def has_unfold(br):
        return br.evaluate("!!document.getElementById('ex-unfold')")

    def to_fin(br):
        br.evaluate("(()=>{const f=document.getElementById('exh-fin'); if(f) f.scrollIntoView({behavior:'instant'});})()")
        br.sleep(0.5)

    with serve(STORY_ON) as base:
        # 1 + 2 — the follow-on asks ONLY the new portion, and no already-read id is re-requested
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_STORY_REC)
            story_walk(br, base)
            if not has_unfold(br):                       # the finale offers «ещё N» ⇒ order > spread
                skip(PORTION_ROWS[0], "no «ещё N» available on this pick (arc ≤ spread)")
                skip(PORTION_ROWS[1], "no «ещё N» available on this pick (arc ≤ spread)")
            else:
                first_ids = json.loads(br.evaluate("JSON.stringify(window.__storyBodies[0]||[])"))
                to_fin(br)
                br.click("#ex-unfold", settle=0.9)
                br.sleep(0.6)
                bodies = json.loads(br.evaluate("JSON.stringify(window.__storyBodies)"))
                new_frame_ids = json.loads(br.evaluate(
                    "JSON.stringify([...document.querySelectorAll('.exh-frame')]"
                    ".slice(%d).map(f=>f.dataset.id))" % SPREAD))
                followon = bodies[1] if len(bodies) >= 2 else []
                # the follow-on body carries ONLY the new portion's ids — the size of one «ещё N»,
                # disjoint from the first portion (never the grown 0..shown set).
                check(PORTION_ROWS[0],
                      len(bodies) >= 2
                      and len(followon) == min(UNFOLD, len(new_frame_ids))
                      and set(followon).isdisjoint(set(first_ids))
                      and set(followon) <= set(new_frame_ids),
                      f"first={len(first_ids)} followon={followon} new={new_frame_ids}")

                # the new works speak (DOM): focus the first newly opened frame, read its plaque line
                br.evaluate("document.querySelectorAll('.exh-frame')[%d]"
                            ".scrollIntoView({behavior:'instant'})" % SPREAD)
                br.sleep(0.8)
                new_told = br.evaluate(
                    "(()=>{const t=document.querySelector('#exh-cap .told');"
                    "return t?t.textContent.trim():null;})()")
                new_id0 = new_frame_ids[0] if new_frame_ids else None
                # the new work speaks, AND across the whole session no id is asked twice — an already-
                # read line is never re-requested, so it byte-stands (the guarantee at its source).
                all_asked = [i for b in bodies for i in b]
                no_reask = len(all_asked) == len(set(all_asked))
                check(PORTION_ROWS[1],
                      new_told == ("told " + new_id0 if new_id0 else None)
                      and no_reask,
                      f"new_told={new_told!r} want='told {new_id0}' asked={all_asked} no_reask={no_reask}")

        # 3 — a refused follow-on stays owed; the next return re-asks it and serves
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_REFUSE_FOLLOWON)
            story_walk(br, base)
            if not has_unfold(br):
                skip(PORTION_ROWS[2], "no «ещё N» available on this pick (arc ≤ spread)")
            else:
                to_fin(br)
                br.click("#ex-unfold", settle=0.9)        # call #2 — refused (404)
                br.sleep(0.6)
                calls_after_unfold = br.evaluate("window.__storyCalls")
                new_frame_ids = json.loads(br.evaluate(
                    "JSON.stringify([...document.querySelectorAll('.exh-frame')]"
                    ".slice(%d).map(f=>f.dataset.id))" % SPREAD))
                # the refused works are wordless for the moment
                br.evaluate("document.querySelectorAll('.exh-frame')[%d]"
                            ".scrollIntoView({behavior:'instant'})" % SPREAD)
                br.sleep(0.5)
                told_while_owed = br.evaluate(
                    "(()=>{const t=document.querySelector('#exh-cap .told');"
                    "return t?t.textContent.trim():null;})()")
                had_return = br.evaluate("!!document.getElementById('ex-return')")
                if not had_return:
                    skip(PORTION_ROWS[2], "no door to return to on this bundle (pool < door_size)")
                else:
                    to_fin(br)
                    br.click("#ex-return", settle=1.0)     # → the door
                    try:
                        br.evaluate("history.back()")      # → back to the walk (the return beat)
                    except RuntimeError:
                        pass
                    br.sleep(1.2)
                    br.evaluate("document.querySelectorAll('.exh-frame')[%d]"
                                ".scrollIntoView({behavior:'instant'})" % SPREAD)
                    br.sleep(0.8)
                    served = br.evaluate(
                        "(()=>{const t=document.querySelector('#exh-cap .told');"
                        "return {told:t?t.textContent.trim():null,calls:window.__storyCalls};})()")
                    new_id0 = new_frame_ids[0] if new_frame_ids else None
                    # owed after the refusal (silent), then a return re-asks (calls grew) and the once-
                    # refused work now speaks. HEAD burns the key before the fetch and never re-asks on
                    # return → this stays silent forever (RED).
                    check(PORTION_ROWS[2],
                          (told_while_owed == "" or told_while_owed is None)
                          and served["calls"] > calls_after_unfold
                          and served["told"] == ("told " + new_id0 if new_id0 else None),
                          f"owed_told={told_while_owed!r} calls {calls_after_unfold}->{served['calls']} "
                          f"served_told={served['told']!r} want='told {new_id0}'")

        # 5 — a return re-shows byte-identical told lines (the reproduced key hits the forever-cache)
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_STORY_REC)
            story_walk(br, base)
            br.evaluate("document.querySelector('.exh-frame').scrollIntoView({behavior:'instant'})")
            br.sleep(0.6)
            before = br.evaluate(
                "(()=>{const t=document.querySelector('#exh-cap .told');"
                "return t?t.textContent.trim():null;})()")
            first_frame_id = br.evaluate("document.querySelector('.exh-frame').dataset.id")
            br.reload()                                   # a cross-load return re-asks per portion
            br.sleep(1.4)
            br.evaluate("document.querySelector('.exh-frame').scrollIntoView({behavior:'instant'})")
            br.sleep(0.8)
            after = br.evaluate(
                "(()=>{const t=document.querySelector('#exh-cap .told');"
                "return t?t.textContent.trim():null;})()")
            check(PORTION_ROWS[4],
                  before == ("told " + first_frame_id) and after == before,
                  f"before={before!r} after={after!r} id={first_frame_id}")


# ---------------------------------------------------------------- report

import shutil
shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(STORY_ON, ignore_errors=True)
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
