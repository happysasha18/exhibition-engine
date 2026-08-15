  // ---- EX-PASS: the transition seam — live settings, one command, one landing owner -------------
  // The seam a visual transition layer plugs into. It draws NOTHING. With no layer registered the
  // walk's own glide (15-motion.js) runs exactly as it always did, so on the served walk this
  // fragment changes no pixel until a layer registers itself through passLayerSet.
  //
  // Every value below is a LIVE SETTING: a validated name with a range, a safe default, a source
  // ladder, an observable applied value and a recorded fallback. None is a compile-time constant.
  // Changing a registered value needs no rebuild. A rebuild belongs to a change of CAPABILITY —
  // a new name in the register, a new instrument, a new driver kind, a new shader branch — never
  // to a change of a registered value.
  //
  // Placed right after the knobs fragment because the in-view watcher (08) builds its observer at
  // EVALUATION time and reads landProgress from here; everything else is called from handlers,
  // long after the whole client has evaluated.
  //
  // The standard source ladder, first match wins: the session's own override, then the pair's
  // score, then the site's live config, then the built-in default. A descriptor may name its own
  // order; qualityTier and diagnostics do, because a per-pair score has no business setting them.
  const PASS_KEY = "@@NS@@-pass";
  const PASS_ORDER = ["session", "score", "site", "default"];
  const PASS_INSTRUMENTS = ["weave"];
  const PASS_DRIVERS = ["static", "phase", "velocity", "pointer", "capability"];
  const PASS_DRIVERS_BUILT = ["static"];
  const PASS_CURVES = ["linear", "smooth", "ease-in", "ease-out", "spline"];
  // A limit is part of the CAPABILITY, so raising one is a rebuild, never a setting.
  // `text` is the fence on a NAME — a setting name, a cause, an instrument name — and it keeps its
  // full force there. `intent` is a separate fence on the one field §4.4 calls prose: a score's
  // opening line, authored at build time, which the lab's own generator writes at about 250
  // characters. Reading one limit for both would have refused a real score for being a sentence.
  //
  // `bytes` IS AN OBSERVED BASELINE WITH ITS EVIDENCE, NOT A CHOSEN ROUND NUMBER. It stood at
  // 8192 B while the only score a pair could carry was the one a site wrote by hand. Since the
  // passage composer ships, a crossing's score is a serialised composed passage, and those were
  // measured: the delivery pack of 2026-08-15 (`plans/v2-b27cc41a8bf15346/`, built by the site's own
  // lab/build-delivery-v1.py) carries 7708 filled scores whose median weighs 7029 B and whose
  // LONGEST weighs 10 851 B, read as JSON.stringify writes them — the very measure passScoreCheck
  // applies below. At 8192 B, 1783 of those 7708 were refused before any instrument saw them, which
  // is 23.1 percent of everything the composer had to say. The baseline is therefore set at
  // 12 288 B: the shipped pack's longest score passes with 1 437 B to spare, and a score half again
  // as long as anything the composer has ever written still does not.
  // It is a CAPABILITY and not a setting — raising it is this rebuild — and the bake publishes it
  // into the settings record under `pass.capabilities`, so the composer measures a filled score
  // against the number the client actually applies instead of against a copy of it.
  const PASS_LIMITS = { camera: 64, phases: 3, instruments: 8, curve: 128, text: 200,
                        intent: 400, bytes: 12288 };
  const PASS_SCORE_FIELDS = ["schema", "intent", "seed", "pair", "params"];
  // PASS-API §4.4a: two schema versions live at once. Version 2 carries the cue list a host plays;
  // version 1 keeps working, because such an address can already sit in a visitor's session store.
  const PASS_SCORE_FIELDS2 = ["schema", "intent", "pair", "seed", "duration", "direction",
                              "interruption", "failLand", "camera", "cues", "quality", "provenance",
                              "chromeReveal"];

  // The register. `def` is the safe default; `kind` decides the check.
  // landProgress — where in a frame's travel the walk calls the arriving work current. 0.55 is
  // today's value, carried over so the seam changes no behaviour; it is a setting like any other.
  // landCommit — who commits the arriving work: the in-view watcher, or the transition's end.
  // flightMs — the transition's own duration; 0 hands the duration back to the walk's glide.
  const PASS_REG = {
    landProgress: { kind: "number", min: 0, max: 1, def: 0.55 },
    landCommit: { kind: "enum", of: ["observe", "transitionEnd"], def: "observe" },
    flightMs: { kind: "number", min: 0, max: 4000, def: 0 },
    phaseWindows: { kind: "ratio3", def: [0.25, 0.5, 0.25] },
    cameraTrack: { kind: "points", max: PASS_LIMITS.camera, def: [] },
    instruments: { kind: "names", of: PASS_INSTRUMENTS, max: PASS_LIMITS.instruments, def: [] },
    qualityTier: { kind: "enum", of: ["rich", "standard", "lean"], def: "standard",
                   order: ["session", "site", "default"] },
    visualLayer: { kind: "enum", of: ["off", "pass"], def: "off" },
    diagnostics: { kind: "enum", of: ["off", "on"], def: "off",
                   order: ["session", "site", "default"] },
  };

  const passEvents = [];
  const passRefusals = [];
  const passApplied = {};
  function passNote(list, row) { list.push(row); if (list.length > 64) list.shift(); }

  // ?pass=landProgress:0.531,diagnostics:on writes the session store once, the way ?reset writes its
  // wipe once, then the address strips itself so the walk's own address stays clean.
  function passSession() {
    try {
      const o = JSON.parse(sessionStorage.getItem(PASS_KEY) || "{}");
      return (o && typeof o === "object") ? o : {};
    } catch (e) { return {}; }
  }
  (function () {
    const q = new URLSearchParams(location.search);
    const raw = q.get("pass");
    if (!raw) return;
    const put = passSession();
    raw.split(",").forEach((pair) => {
      const i = pair.indexOf(":");
      if (i <= 0) return;
      const k = pair.slice(0, i).trim(), v = pair.slice(i + 1).trim();
      if (!PASS_REG[k]) { passNote(passRefusals, { what: "setting", name: k, why: "unknown name" }); return; }
      put[k] = /^-?\d*\.?\d+$/.test(v) ? parseFloat(v) : v;
    });
    try { sessionStorage.setItem(PASS_KEY, JSON.stringify(put)); } catch (e) {}
    q.delete("pass");
    const rest = q.toString();
    try {
      history.replaceState(history.state, "",
        location.pathname + (rest ? "?" + rest : "") + location.hash);
    } catch (e) {}
  })();

  // One value, checked. Returns {ok, value, why}. A refused value never reaches the walk; the
  // caller falls back and the report says so, so a bad setting is visible instead of silent.
  function passCheck(d, v) {
    if (v === undefined || v === null) return { ok: false, why: "absent" };
    const k = d.kind;
    if (k === "number") {
      const n = typeof v === "number" ? v : parseFloat(v);
      if (!Number.isFinite(n)) return { ok: false, why: "no number" };
      if (n < d.min || n > d.max) return { ok: false, why: "outside " + d.min + "…" + d.max };
      return { ok: true, value: n };
    }
    if (k === "enum") {
      const s = String(v);
      return d.of.indexOf(s) < 0 ? { ok: false, why: "outside the named set" } : { ok: true, value: s };
    }
    if (k === "ratio3") {
      if (!Array.isArray(v) || v.length !== PASS_LIMITS.phases) return { ok: false, why: "wants three shares" };
      const a = v.map(Number);
      if (a.some((x) => !Number.isFinite(x) || x < 0 || x > 1)) return { ok: false, why: "a share outside 0…1" };
      if (Math.abs(a[0] + a[1] + a[2] - 1) > 0.001) return { ok: false, why: "the shares miss 1" };
      return { ok: true, value: Object.freeze(a) };
    }
    if (k === "points") {
      if (!Array.isArray(v)) return { ok: false, why: "wants a list" };
      if (v.length > d.max) return { ok: false, why: "over " + d.max };
      const pts = [];
      for (let i = 0; i < v.length; i++) {
        const p = v[i];
        if (!p || typeof p !== "object" || Array.isArray(p)) return { ok: false, why: "no record" };
        if (Object.keys(p).some((f) => ["at", "x", "y", "scale"].indexOf(f) < 0)) {
          return { ok: false, why: "unknown field" };
        }
        const at = Number(p.at);
        if (!Number.isFinite(at) || at < 0 || at > 1) return { ok: false, why: "outside 0…1" };
        pts.push(Object.freeze({ at: at, x: Number(p.x) || 0, y: Number(p.y) || 0,
                                 scale: Number.isFinite(Number(p.scale)) ? Number(p.scale) : 1 }));
      }
      return { ok: true, value: Object.freeze(pts) };
    }
    if (k === "names") {
      if (!Array.isArray(v)) return { ok: false, why: "wants a list" };
      if (v.length > d.max) return { ok: false, why: "over " + d.max };
      const out = [];
      for (let i = 0; i < v.length; i++) {
        const s = String(v[i]);
        if (s.length > PASS_LIMITS.text) return { ok: false, why: "name too long" };
        if (d.of.indexOf(s) < 0) return { ok: false, why: "no allow-list" };
        out.push(s);
      }
      return { ok: true, value: Object.freeze(out) };
    }
    return { ok: false, why: "no check" };
  }

  // The driver graph. A setting's value may be a plain value (a static driver, written short) or a
  // record naming how the frame's value is found: base + phase-curve + velocity-response +
  // pointer-response. Only the static kind is BUILT here; the rest are part of the declared schema,
  // validate like any other, and fall back to their base with the fallback recorded. Nonlinear shape
  // rides named curves and spline points from the score — the format accepts no expression and no
  // executable field.
  function passDriver(d, v) {
    if (v === null || v === undefined || typeof v !== "object" || Array.isArray(v) || !v.driver) {
      const plain = passCheck(d, v);
      return plain.ok
        ? { ok: true, node: { driver: "static", base: plain.value, curve: null, points: null, supported: true } }
        : { ok: false, why: plain.why };
    }
    if (Object.keys(v).some((f) => ["driver", "base", "curve", "points"].indexOf(f) < 0)) {
      return { ok: false, why: "driver names an unknown field" };
    }
    const kind = String(v.driver);
    if (PASS_DRIVERS.indexOf(kind) < 0) return { ok: false, why: "driver on no allow-list" };
    const base = passCheck(d, v.base);
    if (!base.ok) return { ok: false, why: "driver base " + base.why };
    let curve = null, points = null;
    if (v.curve !== undefined) {
      curve = String(v.curve);
      if (PASS_CURVES.indexOf(curve) < 0) return { ok: false, why: "curve on no allow-list" };
    }
    if (v.points !== undefined) {
      if (!Array.isArray(v.points)) return { ok: false, why: "points want a list" };
      if (v.points.length > PASS_LIMITS.curve) return { ok: false, why: "over " + PASS_LIMITS.curve };
      const pts = v.points.map(Number);
      if (pts.some((x) => !Number.isFinite(x))) return { ok: false, why: "a point is no number" };
      points = Object.freeze(pts);
    }
    const built = PASS_DRIVERS_BUILT.indexOf(kind) >= 0;
    if (!built) passNote(passRefusals, { what: "driver", name: kind, why: "declared, drawn by no renderer yet — the base stands" });
    return { ok: true, node: { driver: built ? kind : "static", asked: kind, base: base.value,
                               curve: curve, points: points, supported: built } };
  }

  function passRawFrom(src, key, score) {
    if (src === "session") return passSession()[key];
    if (src === "score") return (score && score.params) ? score.params[key] : undefined;
    if (src === "site") return (((EX && EX.pass) || (cfg && cfg.pass) || {}))[key];
    if (src === "default") return PASS_REG[key].def;
    return undefined;
  }
  // Resolve one name against the ladder, recording what was asked, who won, what got applied.
  function passResolve(key, score) {
    const d = PASS_REG[key];
    const order = d.order || PASS_ORDER;
    let asked, from = null, why = null, node = null;
    for (let i = 0; i < order.length; i++) {
      const src = order[i];
      const raw = passRawFrom(src, key, score);
      if (raw === undefined || raw === null) continue;
      const got = passDriver(d, raw);
      if (got.ok) { asked = raw; from = src; node = got.node; break; }
      if (why === null) { asked = raw; why = got.why; }
      passNote(passRefusals, { what: "setting", name: key, source: src, why: got.why });
    }
    if (from === null) { node = passDriver(d, d.def).node; from = "default"; }
    passApplied[key] = Object.freeze({
      name: key, asked: asked === undefined ? null : asked, source: from, applied: node.base,
      driver: node.asked || node.driver, supported: node.supported,
      fallback: why !== null || from === "default", why: why });
    return Object.freeze(node);
  }
  // The one convenience read for code that wants a value now (the watcher's threshold, the layer
  // switch). Anything inside a running transition reads the frozen snapshot instead.
  function passGet(key, score) { return passResolve(key, score).base; }

  // The score: a versioned record with an allow-list of fields. An unknown field refuses the WHOLE
  // score, so a typo lands as a refusal in the report instead of half-applying.
  function passScoreCheck(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return { ok: false, why: "no record" };
    let bytes = 0;
    try { bytes = JSON.stringify(raw).length; } catch (e) { return { ok: false, why: "does not write out" }; }
    // The refusal names the size it MEASURED beside the fence it applied. A score refused for its
    // weight is refused for a number, and a reason that gives only the fence leaves the one thing
    // its author has to act on unsaid.
    if (bytes > PASS_LIMITS.bytes) {
      return { ok: false, why: "weighs " + bytes + " bytes, over the " + PASS_LIMITS.bytes
                             + " a score may weigh" };
    }
    const v = raw.schema;
    if (v !== 1 && v !== 2) return { ok: false, why: "names no schema 1 or 2" };
    const stray = Object.keys(raw).filter(
      (k) => (v === 2 ? PASS_SCORE_FIELDS2 : PASS_SCORE_FIELDS).indexOf(k) < 0);
    if (stray.length) return { ok: false, why: "unknown field «" + stray[0] + "»" };
    if (raw.intent !== undefined && (typeof raw.intent !== "string" || raw.intent.length > PASS_LIMITS.intent)) {
      return { ok: false, why: "intent is no short text" };
    }
    if (raw.seed !== undefined && !Number.isFinite(Number(raw.seed))) return { ok: false, why: "seed is no number" };
    const p = raw.params;
    if (p !== undefined) {
      if (!p || typeof p !== "object" || Array.isArray(p)) return { ok: false, why: "params is no record" };
      const bad = Object.keys(p).filter((k) => !PASS_REG[k]);
      if (bad.length) return { ok: false, why: "params names «" + bad[0] + "», in no register" };
      const shut = Object.keys(p).filter((k) => (PASS_REG[k].order || PASS_ORDER).indexOf("score") < 0);
      if (shut.length) return { ok: false, why: "«" + shut[0] + "» is closed to a score" };
    }
    return { ok: true, score: raw, read: v };
  }

  // A SCORE PER PAIR CANNOT COVER A DEALT WALK. The walk deals its works afresh each visit and
  // orders them by its own arc, so a pair scored ahead of time essentially never comes up; and a
  // collection of 121 works holds about fourteen thousand ordered pairs, which one whole score each
  // would make ~50 MB of settings file. So a site may carry, beside `pass.scores`:
  //   pass.scoreTemplates[<instrument>]  one score with its per-pair numbers left empty and its
  //                                      slots named — cue, roles, levels, window, doors, camera,
  //                                      quality, interruption and driver graph, all of it the same
  //                                      whatever two works are in hand;
  //   pass.scoreTables[<instrument>]     one row per ordered pair, carrying ONLY that pair's
  //                                      measured numbers.
  // Filling a template's named slots from a row is a data operation: nothing is measured in the
  // browser, so the law that measuring and casting happen at build time keeps its full force. A pair
  // with no row hands back nothing and the walk's own glide runs, exactly as a pair with no score of
  // its own always has; a row the template cannot take is refused WHOLE and says why, the same way a
  // score naming an unknown field is.
  // `readiness` is the one row field that fills no slot: it is the pair's own measured readiness,
  // and the row is refused outright when it stands under the table's floor — the same floor the
  // build-time walk applies, carried in the table so the refusal needs no measurement here. The
  // score is built on a COPY of the template, so a row refused halfway leaves nothing behind.
  function passFillScore(key) {
    const p = (((EX && EX.pass) || (cfg && cfg.pass) || {}));
    const tables = p.scoreTables || {}, templates = p.scoreTemplates || {};
    const insts = Object.keys(tables);
    for (let i = 0; i < insts.length; i++) {
      const tbl = tables[insts[i]] || {}, row = (tbl.rows || {})[key];
      if (!row || typeof row !== "object") continue;
      const no = (why) => { passNote(passRefusals, { what: "row", name: key, why: why }); return null; };
      const tpl = templates[insts[i]] || {}, slots = tpl.slots;
      let score = null;
      try { score = JSON.parse(JSON.stringify(tpl.score)); } catch (e) {}
      if (!score || !slots || typeof slots !== "object") return no("no template for this table's instrument");
      const stray = Object.keys(row).filter((k) => !slots[k] && k !== "readiness");
      if (stray.length) return no("row names «" + stray[0] + "», a slot the template lacks");
      if (typeof tbl.readinessFloor === "number" && !(row.readiness >= tbl.readinessFloor)) {
        return no("readiness " + row.readiness + " stands under the floor " + tbl.readinessFloor);
      }
      const names = Object.keys(slots);
      for (let j = 0; j < names.length; j++) {
        const n = names[j], s = slots[n];
        const cue = (score.cues || []).filter((c) => c && c.id === s.cue)[0];
        if (typeof row[n] !== "number" || !Number.isFinite(row[n])) return no("the row's «" + n + "» is no measured number");
        if (!cue || !cue.nodes || !cue.nodes[s.node]) return no("slot «" + n + "» names a node the template lacks");
        cue.nodes[s.node].value = row[n];
        if (s.score) score[s.score] = row[n];
      }
      const ids = key.split("__");
      score.pair = { a: ids[0], b: ids[1] };
      return score;
    }
    return null;
  }
  // ---- the delivery pack (§4.4b) ----------------------------------------------------------------
  // A SCORE PER PAIR CANNOT TRAVEL IN THE SETTINGS FILE EITHER, once the composer writes one for
  // every ordered pair: 7708 composed scores are megabytes, and the settings file is parsed at boot
  // by every visitor. So the site ships them as a PACK of static files — a head, one template per
  // passage shape, and one row file per DEPARTING work — and its settings record carries the pack's
  // addresses alone, under `pass.packs`.
  //
  // THE READER TRAVELS AS ITS OWN FILE, the way the picture and the instruments do. It is fetched
  // once, on the first landing of a walk whose settings record actually names a pack and whose
  // layer is on, and a visit that never reaches that state never asks for it. What stays HERE is
  // the door: where the reader is asked for, the one synchronous question a declare puts to it, and
  // the landing that warms the next crossing's shard. That division is the byte fence's own
  // answer — the bundle carries the contract and the picture travels — and it is the same shape
  // pass-layer.js already stands on.
  const PASS_PACK_SRC = "pass-reader.js";
  let passPack = null, passPackAsked = false, passPackState = "absent", passPackWarm = null;
  function passPackBlock() { return (((EX && EX.pass) || (cfg && cfg.pass) || {})).packs; }
  // The reader hands over a factory rather than a finished reader, so the bundle stays the one
  // owner of the settings block and of the diagnostic surface: the reader is handed the addresses
  // it may fetch and one way to speak, and it reaches nothing else in this file.
  function passPackSet(part) {
    passPack = null;
    const mk = part && part.make;
    if (typeof mk !== "function") {
      passPackState = "refused";
      passNote(passRefusals, { what: "pack", name: PASS_PACK_SRC, why: "handed over no reader" });
      return;
    }
    try {
      passPack = mk({
        packs: passPackBlock(),
        note: (name, why) => passNote(passRefusals, { what: "pack", name: name, why: why }),
      }) || null;
    } catch (e) { passPack = null; }
    passPackState = passPack ? "read" : "refused";
    if (passPack && passPackWarm) { try { passPack.warm(passPackWarm); } catch (e) {} }
  }
  function passPackOpen() {
    if (passPackAsked) return;
    const block = passPackBlock();
    if (!block || typeof block !== "object" || !Object.keys(block).length) return;
    if (passGet("visualLayer") !== "pass") return;
    passPackAsked = true;
    passPackState = "asked";
    try {
      window.__@@NS@@PassReader = passPackSet;
      const s = document.createElement("script");
      s.src = PASS_PACK_SRC;
      s.async = true;
      s.onerror = () => {
        passPackState = "absent";
        passNote(passRefusals, { what: "pack", name: PASS_PACK_SRC, why: "load failed" });
      };
      document.head.appendChild(s);
    } catch (e) {
      passPackState = "absent";
      passNote(passRefusals, { what: "pack", name: PASS_PACK_SRC, why: "no door" });
    }
  }
  // THE WALK LANDED ON A WORK. The shard holding that work's outgoing crossings is asked for now,
  // because a crossing is declared the instant the visitor moves and passScoreFor answers inside
  // that same call — a fetch begun there could never arrive in time. The reader asks once per work;
  // a landing before the reader itself has arrived is remembered, and warmed the moment it joins.
  function passWarm(el) {
    const id = el && el.dataset ? el.dataset.id : null;
    if (!id) return;
    passPackOpen();
    passPackWarm = id;
    if (passPack) { try { passPack.warm(id); } catch (e) {} }
  }

  // The pair's own score, without an engine rebuild. The site writes `pass.scores`, keyed
  // "<departing id>__<arriving id>", into its own site.json; the bake carries the whole `pass` block
  // into config.json as DATA and judges none of it (engine/build.py), so a new score for a pair is a
  // content change. A pair with a score of its own takes it; a pair with only a row takes the filled
  // template; a pair with neither keeps the walk's own glide, which is the standing fallback — the
  // same road a refused score takes.
  function passScoreFor(fromEl, toEl) {
    const a = fromEl && fromEl.dataset ? fromEl.dataset.id : null;
    const b = toEl && toEl.dataset ? toEl.dataset.id : null;
    if (!a || !b) return null;
    const key = a + "__" + b;
    const rec = (((EX && EX.pass) || (cfg && cfg.pass) || {})).scores;
    if (rec && rec[key]) return rec[key];
    // The pack, asked for what has ALREADY arrived. This road never waits and never fetches: a
    // shard that has not landed answers nothing, the reason goes on the diagnostic surface, and the
    // crossing falls through to the walk's own glide exactly as a pair with no score always has.
    if (passPack) {
      try { const s = passPack.scoreFor(key); if (s) return s; } catch (e) {}
    }
    return passFillScore(key);
  }

  // Every setting resolves ONCE, at nav-start, and the result is frozen onto the command. A live
  // change lands on the NEXT transition; the geometry and the camera of a transition already in
  // flight stay as they were. A setting whose descriptor names a way to apply live may travel inside
  // the flight; none does yet, so a running transition is fully frozen.
  function passSnapshot(score) {
    const out = {};
    Object.keys(PASS_REG).forEach((k) => { out[k] = passResolve(k, score); });
    return Object.freeze(out);
  }

  let passGen = 0;
  let passNav = null;
  let passPending = null;
  let passLastEl = null, passLastGen = -1;
  function passWhere(el) {
    if (!el) return null;
    // PASS-API §1.1: the door is a destination like any other. It carries no dataset.id of its own
    // (it is not a work), so it is named by its element id instead — the one case passWhere resolves
    // by anything other than dataset.
    if (el.id === "ex-door") return Object.freeze({ id: "door", n: null });
    return Object.freeze({ id: (el.dataset && el.dataset.id) || null,
                           n: (el.dataset && el.dataset.n) ? +el.dataset.n : null });
  }
  // The marks carry their own prefix, so the walk's existing timings keep their exact shape and the
  // suite's mark counts stay honest; the seam's own suite filters this prefix.
  function passMark(name, cmd, extra) {
    const row = { at: Math.round(performance.now()), name: name,
                  gen: cmd ? cmd.gen : 0, kind: cmd ? cmd.kind : null, cause: cmd ? cmd.cause : null,
                  from: cmd && cmd.from ? cmd.from.id : null, to: cmd && cmd.to ? cmd.to.id : null,
                  why: extra || null };
    passNote(passEvents, row);
    try { performance.mark("@@NS@@-pass:" + name, { detail: row }); }
    catch (e) { try { performance.mark("@@NS@@-pass:" + name); } catch (e2) {} }
  }
  // A held-back landing always lands, never strands.
  function passFlush() {
    const p = passPending; passPending = null;
    if (p) { passLastEl = p.el; passLastGen = passGen; p.commit(p.el, "flush"); }
  }
  function passEnd(name, why) {
    if (!passNav) return;
    const cmd = passNav; passNav = null;
    passFlush();
    passMark(name, cmd, why);
  }
  // The one place a transition is declared. Every road that moves the visitor from one work to
  // another comes through here — the stepping input AND every programmatic jump — so the state
  // contract is the same for all of them, whatever the picture does.
  function passStart(a) {
    passEnd("nav-abort", "superseded");
    passGen += 1;
    const g = passGen;
    let score = null;
    const raw = a.score || passScoreFor(a.fromEl, a.toEl);
    if (raw) {
      const seen = passScoreCheck(raw);
      if (seen.ok) {
        score = seen.score;
        // The checker says which version it read (§4.4a). A version-1 score is read forward: its
        // five fields keep feeding the settings ladder exactly as they always did, and it names no
        // cue — so no instrument takes the command and the walk's glide plays, which is what a
        // version-1 score has always meant. The reading is recorded rather than assumed.
        if (seen.read === 1) {
          passNote(passRefusals, { what: "score", name: "schema 1",
                                   why: "read forward: params feed the ladder, no cue to play" });
        }
      } else passNote(passRefusals, { what: "score", name: raw.intent || "unnamed", why: seen.why });
    }
    const cmd = Object.freeze({
      gen: g,
      from: passWhere(a.fromEl), to: passWhere(a.toEl),
      dir: (+a.dir < 0) ? -1 : 1,
      span: Math.abs(+a.span || 0),
      kind: a.kind === "jump" ? "jump" : "step",
      cause: String(a.cause || "step").slice(0, PASS_LIMITS.text),
      velocity: +a.velocity || 0,
      reduced: !!REDUCED,
      saveData: !!dataSaver(),
      rtl: (document.documentElement.getAttribute("dir") === "rtl"),
      dpr: window.devicePixelRatio || 1,
      viewport: Object.freeze({ w: innerWidth, h: innerHeight }),
      params: passSnapshot(score),
      // The score travels frozen ON the command, so the host reads the cue, the duration and the
      // fail policy of THIS transaction and never a live value that moved under it mid-flight.
      score: score,
      signal: Object.freeze({ get aborted() { return g !== passGen; } }),
    });
    passNav = cmd;
    passMark("nav-start", cmd);
    return cmd;
  }
  function passLandNow() { passEnd("nav-land", null); }
  function passAbortNow(why) { passEnd("nav-abort", why || "cancelled"); }

  // ---- ProductNavigationAdapter (PASS-API §1.1) -------------------------------------------------
  // declare(a) is the ONE door every road between two works now knocks on — the stepping road and
  // every programmatic jump alike. It adds the two locks §1.1 names on top of passStart's freeze:
  //   - a command whose destination is absent is refused outright (never reaches passStart, never
  //     mints a generation) — the class of defect a null-destination jump could leave behind (a
  //     landing keyed on the destination has nothing to read).
  //   - two declares inside one animation frame make the second a refusal with its reason; a declare
  //     arriving while another is merely RUNNING still supersedes it (passStart's own job, unchanged)
  //     — only the same-frame race is new law.
  let passFrameLock = false;
  function passFrameUnlock() { passFrameLock = false; }
  function declare(a) {
    if (!a || !a.toEl) {
      passNote(passRefusals, { what: "declare", name: (a && a.cause) || "unnamed", why: "no destination" });
      return null;
    }
    if (passFrameLock) {
      passNote(passRefusals, { what: "declare", name: a.cause || "unnamed", why: "second declare in one frame" });
      return null;
    }
    passFrameLock = true;
    try { requestAnimationFrame(passFrameUnlock); } catch (e) { passFrameLock = false; }
    return passStart(a);
  }
  // A programmatic move — a restored place, a pasted link, a closed room, a rotation, a fresh hang,
  // the Back arrow. It takes the SAME command and the same landing owner, so the state contract
  // covers every road between two works; the picture layer declines it by kind, so the eye still
  // sees an instant land. A jump with no destination is refused by declare and lands nothing.
  function passJump(toEl, cause, fromEl) {
    const cmd = declare({ fromEl: fromEl || null, toEl: toEl || null, dir: 1, span: 0,
                          kind: "jump", cause: cause, velocity: 0 });
    if (cmd) passLandNow();
    return cmd;
  }

  // dock(cmd) — PASS-API §1.1/§2.4: makes the arriving work current, exactly once, keyed on the
  // command's OWN frozen generation together with its destination (never the live global passGen,
  // which is exactly the key the seam got wrong — §10.2). Called by the host on settle/fail/cancel;
  // reads cmd.to and takes no element, so a caller cannot dock a work the command never named.
  const passDockKeys = Object.create(null);
  function passResolveEl(to) {
    if (!to) return null;
    if (to.id === "door" || to.id === null) return { id: "exh-fin" };  // the door's own landing clears
    return stage.querySelector('.exh-frame[data-id="' + String(to.id).replace(/"/g, "") + '"]');
  }
  function dock(cmd) {
    if (!cmd || !cmd.to) return;
    const key = cmd.gen + ":" + (cmd.to.id === null ? "" : cmd.to.id);
    if (passDockKeys[key]) {
      passNote(passRefusals, { what: "dock", name: key, why: "already docked" });
      return;
    }
    passDockKeys[key] = true;
    const el = passResolveEl(cmd.to);
    if (el) passLandGate(el, "dock", landOn, cmd.gen);
    passMark("dock", cmd, cmd.to.id === "door" ? "door" : null);
    // The chrome comes back HERE and nowhere else, so it can only ever follow the arrival. The
    // curtain has already dropped and the canvas has already been released (the host calls
    // handoff(cmd) before dock — §2.2 settle/fail), so this is the first instant the walk owns its
    // own pixels again. Focus travels with the chrome rather than standing apart from it: the
    // accessibility handoff is one of the chrome's named parts, and two owners would move focus
    // twice.
    chromeReveal(cmd);
  }

  // ---- hangGeometry (PASS-API §1.1) --------------------------------------------------------------
  // THE WORK'S REAL BOX in the exhibition layout at this instant, measured off the DOM. The walk
  // seats a work by CSS — max-height 82dvh, max-width 88vw, the work's own aspect kept, a 2px radius
  // — so only the element itself knows where it stands, and the number changes with every resize,
  // turn and re-hang. The renderer lays its own frame onto this box at both ends of a passage, which
  // is what makes the two handoffs exact instead of approximately right.
  //
  // The element measured is the PICTURE, never the section around it: the section is a full-viewport
  // grid cell and says nothing about where the work hangs inside it.
  function hangGeometry(workId) {
    const el = passResolveEl({ id: workId });
    const im = (el && el.querySelector) ? el.querySelector("img.work") : null;
    if (!im || !im.getBoundingClientRect) return null;
    const r = im.getBoundingClientRect();
    if (!r.width || !r.height) return null;
    // The walk shows a work WHOLE, so its crop is 1 and its fit contains rather than covers. Both
    // are READ rather than assumed, because a layout that ever crops must say so here instead of
    // letting the renderer seat a whole work into a cropped box. The radius and any transform the
    // layout applies travel with them for the same reason.
    const cs = getComputedStyle(im);
    return Object.freeze({
      workId: workId, x: r.left, y: r.top, w: r.width, h: r.height,
      fit: cs.objectFit || "fill", crop: 1,
      radius: parseFloat(cs.borderTopLeftRadius) || 0,
      transform: cs.transform === "none" ? null : cs.transform,
      dpr: window.devicePixelRatio || 1,
      orientation: innerWidth >= innerHeight ? "landscape" : "portrait",
    });
  }

  // handoff(cmd) — the DOM's work is shown and the renderer's canvas released inside ONE frame.
  // The work's own reveal carries an opacity transition on the walk's road (it fades in as the
  // visitor scrolls to it); a passage has already drawn that work, so the transition is switched off
  // for this one reveal and the picture is simply there. Nothing fades, and no frame draws neither
  // picture: the DOM is revealed FIRST and the canvas dropped after, inside the same task.
  // THE WALK IS PLACED AT THE ARRIVING WORK. A takeover returns before the walk's own glide ever
  // runs (15-motion.js: an offer that is taken returns), so nothing else moves the walk, and the
  // work a passage arrived at would be revealed a viewport away from the eye. The placement is
  // instant — the passage was the animation, and a second one here would be the walk travelling
  // twice — and it is called once under cover, mid-passage, while the renderer's canvas stands at
  // the whole frame and nothing of the walk is in sight.
  //
  // `place` asks for that placement alone. Called without it the whole handoff runs: the work's own
  // reveal carries an opacity transition on the walk's road, and a passage has already drawn that
  // work, so the transition is switched off for this one reveal and the picture is simply there.
  // Nothing fades, and no frame draws neither picture — the DOM is revealed FIRST and the canvas
  // dropped after, inside the same task.
  function handoff(cmd, place) {
    if (!cmd || !cmd.to) return;
    const el = passResolveEl(cmd.to);
    const im = (el && el.querySelector) ? el.querySelector("img.work") : null;
    if (im) scrollTo(0, frameCenter(el));
    if (place) { passMark("place", cmd, null); return; }
    if (im) { im.style.transition = "none"; im.style.opacity = "1"; }
    if (el && el.classList) el.classList.add("seen");
    curtain(false);
    passMark("handoff", cmd, null);
  }

  // ---- chromeReveal (PASS-API §1.1) --------------------------------------------------------------
  // The walk's own chrome comes back after the arrival and the handoff, ONCE per command, with its
  // parts named: the title and plaque, the counter, share, the sound control, the series and control
  // affordances, and the focus and accessibility handoff. The timing is data a score may name; with
  // no score naming it the default below plays, so a site that writes no timing still gets the whole
  // choreography.
  //
  // SOUND IS SHOWN, NEVER TOUCHED. The control is put back on screen; whether it is playing, at what
  // volume, and what the visitor asked for are the sound player's own state and cross a passage
  // untouched.
  // The six parts and the millisecond each waits by default. One record names them, so the parts a
  // score may time and the parts the choreography plays can never drift apart.
  //
  // THE REVEAL IS ONCE BECAUSE THE LANDING IS ONCE. dock is its only caller, and dock already keeps
  // the one ledger that says whether this command has landed — keyed on the command's own
  // generation together with its destination (§2.4/§10.2). A second ledger here would be a second
  // home for one fact, and the two could disagree; the conformance rows measure the reveal count
  // across every exit rather than trusting either.
  const PASS_CHROME_MS = { plaque: 0, counter: 0, share: 90, sound: 90, series: 140, focus: 0 };
  function chromeReveal(cmd) {
    if (!cmd || !cmd.to) return;
    const el = passResolveEl(cmd.to);
    const named = (cmd.score && cmd.score.chromeReveal) || {};
    // Four of the six are one element each, put back by the very class the walk already shows them
    // with. `series` stands up the series and control affordances, which live INSIDE the plaque the
    // landing wrote — one body class carries them together. `focus` is the accessibility handoff.
    const one = { plaque: cap, counter: counter, share: shareBtn,
                  sound: document.getElementById("ex-sound") };
    Object.keys(PASS_CHROME_MS).forEach((name) => {
      const asked = Number(named[name]);
      const ok = Number.isFinite(asked) && asked >= 0 && asked <= 2000;
      if (named[name] !== undefined && !ok) {
        passNote(passRefusals, { what: "chrome", name: name, why: "outside 0…2000 ms" });
      }
      const go = () => {
        try {
          if (one[name]) one[name].classList.add("show");
          else if (name === "series") document.body.classList.add("ex-pass-chrome");
          else if (el && el.focus && !stage.contains(document.activeElement)) el.focus({ preventScroll: true });
        } catch (e) {}
        passMark("chrome-" + name, cmd, null);
      };
      const ms = ok ? asked : PASS_CHROME_MS[name];
      if (ms > 0) setTimeout(go, ms); else go();
    });
    passMark("chrome", cmd, null);
  }

  // glide(cmd) — the walk's own scroll animation, the standing fallback; called by the host when no
  // renderer takes the command (a decline, a timed-out prepare, or no renderer registered at all).
  function glide(cmd) {
    if (!cmd) return;
    const el = passResolveEl(cmd.to);
    if (el && el.getBoundingClientRect) glideToFrame(frameCenter(el), cmd.velocity || 0, "pass");
    else passLandNow();
  }

  // interrupt(reason) — PASS-API §1.1/§10.3: ends the transaction in flight from a product surface
  // that stands in front of the walk. Reaches the host too (a takeover the per-frame glide checker
  // never sees, because during a takeover that loop does not run) and then ends the bundle's own
  // bookkeeping the way passAbortNow always has.
  // The host is told FIRST, and unconditionally. The bundle's own bookkeeping can already have
  // landed while a renderer still holds the frame — a takeover whose command has flushed its
  // nav-land is exactly that state — and returning early on `passNav` left the renderer drawing
  // over a walk the product believed it had finished with. §10.3's whole claim is that a surface
  // standing in front of the walk reaches the renderer; it cannot depend on the bundle's own record.
  function interrupt(reason) {
    if (passLayer && typeof passLayer.cancel === "function") {
      try { passLayer.cancel(reason); } catch (e) {}
    }
    if (passNav) passAbortNow(reason);
  }

  // reframe(viewport) — the resize/orientation road tells a RUNNING transaction its frame changed
  // size, so it resizes in place instead of being superseded (§10.3's third repair).
  function reframe(viewport) {
    if (passLayer && typeof passLayer.resize === "function") {
      try { passLayer.resize(viewport); } catch (e) {}
    }
  }
  function passRunning() {
    try { return !!(passLayer && passLayer.report && passLayer.report().active); }
    catch (e) { return false; }
  }

  // curtain(on) — the host only. Covers the walk with the renderer's canvas and hides the covered
  // walk from the accessibility tree; the caption's own size/change watchers suspend with it. Focus
  // returns to the arriving work at the landing (dock already restores the plaque/counter/share).
  function curtain(on) {
    document.body.classList.toggle("ex-pass-curtain", !!on);
    if (on) { stage.setAttribute("aria-hidden", "true"); stage.inert = true; }
    else { stage.removeAttribute("aria-hidden"); stage.inert = false; }
    try {
      if (capRO) {
        if (on) capRO.disconnect();
        else { const im = capInViewImg(); if (im) capRO.observe(im); }
      }
    } catch (e) {}
    try {
      if (capMO) {
        if (on) capMO.disconnect();
        else capMO.observe(cap, { childList: true, subtree: true, characterData: true });
      }
    } catch (e) {}
  }

  // The one owner of «this work is now current». The in-view watcher (08) and the end of a
  // transition both arrive here. A work that is ALREADY the last one landed, inside the same
  // generation, is a repeat — that is the watcher re-reporting what is still on screen after a
  // rebuilt threshold, and it commits nothing twice. A visitor who walks back to a work does land
  // it again: the work between them moved the last-landed mark.
  // `gen` lets a caller pin the generation the check reads against instead of the LIVE passGen — the
  // host's own dock(cmd) passes cmd.gen, its command's own frozen generation, so a callback arriving
  // after a newer command has already declared still keys against the generation it actually belongs
  // to (PASS-API §10.2: keyed on generation AND destination, never a global that has moved on).
  function passLandGate(el, reason, commit, gen) {
    if (!el) return;
    passWarm(el);
    const g = gen === undefined ? passGen : gen;
    if (el === passLastEl && g === passLastGen) return;
    if (reason === "observe" && passNav && passNav.to
        && passNav.to.id === ((el.dataset && el.dataset.id) || null)
        && passGet("landCommit") === "transitionEnd") {
      passPending = { el: el, commit: commit };
      return;
    }
    passLastEl = el; passLastGen = g;
    commit(el, reason);
  }

  // A drawing layer registers itself here. With none registered — the state of this branch — every
  // command falls through to the walk's own glide, which is the fallback the seam keeps reversible:
  // turning the layer off is a setting, never a rebuild.
  let passLayer = null, passState = "absent";
  // PASS-API §12: the renderer's own file registers the HOST here — a registry taking one
  // instrument, exposing offer/resize/cancel/report. The seam's old {name, run} shape is gone with
  // the single run(cmd, done) entry point it belonged to (§0, "Where it stands").
  function passLayerSet(layer) {
    passLayer = (layer && typeof layer.offer === "function") ? layer : null;
    passState = passLayer ? "registered" : "absent";
  }
  function passVisualTakes(cmd) {
    if (!passLayer) return false;
    if (cmd.kind === "jump") return false;
    if (cmd.reduced || cmd.saveData) return false;
    return cmd.params.visualLayer.base === "pass";
  }
  // A layer that throws is dropped for the rest of the visit and the walk's glide takes at once. The
  // host owns the offer/prepare/decline decision entirely (§2.1); a `true` return means the host has
  // taken responsibility for landing this command — by taking over, or by calling the glide hook
  // itself when it declines — never that a renderer is now drawing.
  function passOffer(cmd) {
    try {
      return passLayer.offer(cmd, { dock: dock, glide: glide, curtain: curtain, mark: passMark,
                                    hangGeometry: hangGeometry, handoff: handoff }) === true;
    }
    catch (e) {
      passNote(passRefusals, { what: "layer", name: "offer", why: "threw" });
      passLayerSet(null);
      return false;
    }
  }

  // The drawing layer ships as its OWN file, fetched the first time a walk wants it: this bundle
  // carries the door and none of the picture. One request per visit, one capability probe, and
  // every refusal on the diagnostic surface. The walk keeps gliding throughout — the layer joins a
  // later transition when it arrives, and a visit where it never arrives is the walk as it is today.
  const PASS_SRC = "pass-layer.js";
  let passAsked = false, passAble = null;
  function passCan() {
    if (passAble === null) {
      try {
        const g = document.createElement("canvas").getContext("webgl2");
        passAble = !!g;
        const lose = g && g.getExtension("WEBGL_lose_context");
        if (lose) lose.loseContext();
      } catch (e) { passAble = false; }
    }
    return passAble;
  }
  function passOpen() {
    if (passAsked || passLayer) return;
    if (passGet("visualLayer") !== "pass") return;
    const no = REDUCED ? "reduced motion" : dataSaver() ? "save data" : passCan() ? null : "no webgl2";
    if (no) { passNote(passRefusals, { what: "layer", name: PASS_SRC, why: no }); passAsked = true; return; }
    passAsked = true;
    passState = "asked";
    try {
      window.__@@NS@@PassLayer = passLayerSet;
      const s = document.createElement("script");
      s.src = PASS_SRC;
      s.async = true;
      s.onerror = () => { passState = "absent"; passNote(passRefusals, { what: "layer", name: PASS_SRC, why: "load failed" }); };
      document.head.appendChild(s);
    } catch (e) { passState = "absent"; passNote(passRefusals, { what: "layer", name: PASS_SRC, why: "no door" }); }
  }

  // The diagnostic surface: technical rows only — the register, the lifecycle, the refusals, the
  // command in flight, and what the device reports. The told story, the quiz answers, the gift, the
  // visitor's own marks, the remembered place and anything the counting wire carries stay out by
  // construction: this function reads its own four lists and nothing else.
  function passPlain(params) {
    const out = {};
    Object.keys(params).forEach((k) => { out[k] = params[k].base; });
    return out;
  }
  function passReport() {
    return {
      version: 1,
      // resolved FRESH on every read: the register's rows report where each name stands NOW, so a
      // value changed mid-session is visible at once. What a running transition froze is a separate
      // row of its own, below, and the two never pretend to be the same reading.
      settings: Object.keys(PASS_REG).map((k) => { passResolve(k, null); return passApplied[k]; }),
      events: passEvents.slice(),
      refusals: passRefusals.slice(),
      nav: passNav ? { gen: passNav.gen, kind: passNav.kind, cause: passNav.cause,
                       to: passNav.to ? passNav.to.id : null, params: passPlain(passNav.params) } : null,
      device: { reduced: !!REDUCED, saveData: !!dataSaver(), dpr: window.devicePixelRatio || 1,
                webgl2: passAble, viewport: { w: innerWidth, h: innerHeight } },
      limits: PASS_LIMITS,
      drivers: { declared: PASS_DRIVERS.slice(), built: PASS_DRIVERS_BUILT.slice() },
      layer: passState,
      // The delivery pack, on the same surface: where the reader stands, and what it says about
      // every pack the settings record names and every shard this visit has asked for.
      pack: Object.assign({ src: PASS_PACK_SRC, state: passPackState, warm: passPackWarm },
                          passPack ? passPack.report() : {}),
    };
  }
  // `score` is the checker itself, handed over so a score can be judged without being played — the
  // surface stays read-only about the walk and decides nothing on its own. `adapter` and `layer` are
  // a TESTING seam, gated the same way: they let a conformance row construct a real command and drive
  // the host directly, on real elements, without needing to simulate every input road by hand.
  if (passGet("diagnostics") === "on") {
    try {
      window.__@@NS@@Pass = {
        report: passReport, score: passScoreCheck, fill: passFillScore, version: 1,
        adapter: { declare: declare, dock: dock, glide: glide, interrupt: interrupt,
                   reframe: reframe, curtain: curtain, mark: passMark,
                   hangGeometry: hangGeometry, handoff: handoff, chromeReveal: chromeReveal },
        layer: function () { return passLayer; },
      };
    } catch (e) {}
  }
