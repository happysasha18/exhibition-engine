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
  // 2026-08-17 — `intent` MOVED FROM 400 TO 600 (U27 stage 0), and the move is a defect this unit
  // found rather than a budget it wanted. The composer writes the passage's intent as a sentence a
  // person reads — what holds, what travels, from which reading to which, and what the camera does
  // — and over the whole collection 1 004 of the 6 304 composed crossings write one longer than 400
  // characters, the longest at 507. Every one of them was refused WHOLE by this checker, with
  // «intent is no short text», so no composed crossing of that thousand could ever have played on
  // any road — the prebaked pack's included. 600 is the measured 507 plus about a fifth. The cap
  // itself stays: an intent is a sentence, not a place to put a payload.
  const PASS_LIMITS = { camera: 64, phases: 3, instruments: 8, curve: 128, text: 200,
                        intent: 600, bytes: 12288 };
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
    // instrumentNames — the instruments a transition may name, as a list of names off the
    // allow-list. THE NAME IS THE REGISTER'S OWN and it is not the record's. The bake writes the
    // instrument ADDRESS record — one entry per instrument, each with its file, version and digest
    // — into the settings block under `pass.instruments` (engine/build.py), and this register once
    // carried a setting of that same name. The register's site rung reads the settings block by the
    // name, so every resolve handed a record to a check that wants a list, and «setting
    // `instruments`: wants a list» went onto the refusal ring about four times per step — the ring
    // holds 64 rows, so within ten steps it had pushed every real refusal off (U10 §5 had to read
    // the layer's own refusal one step into the visit for exactly that reason). The record's name
    // is the landed contract of PASS-API §4.4d and the site's own delivery check reads it, so the
    // record keeps it and the register's setting takes a name of its own.
    instrumentNames: { kind: "names", of: PASS_INSTRUMENTS, max: PASS_LIMITS.instruments, def: [] },
    qualityTier: { kind: "enum", of: ["rich", "standard", "lean"], def: "standard",
                   order: ["session", "site", "default"] },
    visualLayer: { kind: "enum", of: ["off", "pass"], def: "off" },
    diagnostics: { kind: "enum", of: ["off", "on"], def: "off",
                   order: ["session", "site", "default"] },
    // familySeed — the seed the visit's own family roll runs on (§4.4f). Zero, the default, means
    // this visit rolls a seed of its own, which is the public bar: a crossing's bounded handles
    // land where no other visit's landed and every public run exists once. Any other number PINS
    // the visit, and a run at a pinned seed reproduces its predecessor to the pixel — the judging
    // mode. It resolves on the session, site and default rungs alone: a per-pair score has no
    // business setting the mode a whole visit is judged in, exactly as it has none for the tier or
    // the diagnostics switch.
    familySeed: { kind: "number", min: 0, max: 4294967295, def: 0,
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
    // THE WEIGHT IS A READING AND NO LONGER A WALL (2026-08-18, his word of 09:51). A score over
    // this number was refused WHOLE and the visitor took the walk's plain glide — 1 783 of the
    // 7 708 shipped scores at the fence's earlier value, every one of them before an instrument
    // saw it. A crossing is not worse for weighing more; a heavy score costs a little parse time
    // and nothing else, so the number is now a reading the diagnostic surface carries and the
    // passage plays. The composer fits its own scores to it before they ever arrive here, so the
    // reading stands at nothing on the product path.
    const overWeight = bytes > PASS_LIMITS.bytes
      ? "weighs " + bytes + " bytes, over the " + PASS_LIMITS.bytes + " a score is composed to fit"
      : null;
    const v = raw.schema;
    if (v !== 1 && v !== 2) return { ok: false, why: "names no schema 1 or 2" };
    const stray = Object.keys(raw).filter(
      (k) => (v === 2 ? PASS_SCORE_FIELDS2 : PASS_SCORE_FIELDS).indexOf(k) < 0);
    if (stray.length) return { ok: false, why: "unknown field «" + stray[0] + "»" };
    // THE AUTHORED LINE IS TRIMMED, NEVER THE REASON A CROSSING IS LOST. «intent is no short text»
    // refused the whole score, and over one collection 1 004 of 6 304 composed crossings were lost
    // to it — no instrument ever saw them. A line running long is a line running long: it is cut to
    // the length this client reads and the passage plays. A line that is no string at all is a
    // different thing and is simply not carried.
    let overLine = null;
    if (raw.intent !== undefined) {
      if (typeof raw.intent !== "string") {
        overLine = "the authored line is no text, so the crossing carries none";
        delete raw.intent;
      } else if (raw.intent.length > PASS_LIMITS.intent) {
        overLine = "the authored line ran to " + raw.intent.length + " characters and is trimmed to "
                 + PASS_LIMITS.intent;
        raw.intent = raw.intent.slice(0, PASS_LIMITS.intent - 1) + "…";
      }
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
    // WHAT WAS READ ABOUT THE SCORE'S SIZE travels with it rather than deciding anything.
    const noted = [overWeight, overLine].filter(Boolean);
    return { ok: true, score: raw, read: v, noted: noted.length ? noted : null };
  }

  // NO SCORE PER PAIR TRAVELS WITH THE PRODUCT. The walk deals its works afresh each visit, and a
  // quadratic pair pack could neither cover that living route nor grow with the collection. The
  // runtime road below hands two per-work records to one composer; the pair, direction, entrance,
  // route role, visit seed, capability and edge memory meet only at the instant of the crossing.
  // ---- family breath (§4.4f) ---------------------------------------------------------------------
  // A ROW MAY SAY WHAT MAY BREATHE. Filling a row's measured numbers exactly means a pair flipped
  // twice inside one visit plays one score byte for byte — the defect the site's own U9 measurement
  // read on four flips of one pair. The charter asks for the same family each time with small shifts
  // pass by pass, so a row may carry a family-bounds record naming, per SLOT it already fills, the
  // closed span the fill may roll that slot inside, and whether the score's own seed re-rolls.
  //
  // THE ROLL LIVES HERE. It knows nothing about score paths or handle names: it is given the spans
  // keyed by the runtime composer and hands back rolled values under those same keys.
  //
  // THE SEED IS THE VISIT, THE PASS INDEX AND THE PAIR. The pass index is the generation `declare`
  // has already minted for the crossing being declared, so a pair flipped twice in one visit rolls
  // twice; the visit's seed keeps the whole visit apart from every other visit; and the pair's key
  // keeps two crossings declared at the same index from sharing a roll. Nothing here reads a clock:
  // a wall-time roll would make a pinned run irreproducible, which is the very thing §4.4b's
  // determinism row exists to hold.
  const passFamilies = [];
  let passVisit = 0, passVisitPinned = false;
  // The entrance is part of a visit's artistic situation.  A different door deals a different
  // route, so it must also give the passage die a different starting point; otherwise two doors
  // can accidentally repeat the same family/phase decisions merely because their first edge has
  // the same ids.  `pick` is the product's chosen door work, never a new input or an identity.
  // The value is read only when a visit first needs a crossing and then held, which preserves the
  // seeded repeatability and the edge-memory law for the rest of that route.
  function passDoorSalt() {
    try { return pick ? passText(pick) : 0; } catch (e) { return 0; }
  }
  function passBeginAtDoor() {
    // A fresh door starts a fresh route.  It does not erase edge memory: returning through the
    // browser's history can still find its related passage, while the new route receives its own
    // die when it first crosses.
    passVisit = 0;
    passVisitPinned = false;
    passRoutePlayed = [];
    passRouteFamilyCount = Object.create(null);
    passRouteInstrumentCount = Object.create(null);
    passRouteWorldSeen = false;
  }
  function passVisitSeed() {
    if (!passVisit) {
      // Read ONCE, at the first crossing that breathes, and held for the visit: a seed that
      // re-resolved per crossing would let a mid-visit change split one visit into two families.
      const pin = passGet("familySeed") >>> 0;
      const rolled = ((Math.random() * 4294967296) >>> 0) || 1;
      passVisit = pin || passMix(rolled, passDoorSalt()) || 1;
      passVisitPinned = !!pin;
    }
    return passVisit;
  }
  function passMix(a, b) {
    let h = Math.imul((a >>> 0) ^ 0x9e3779b9, 0x85ebca6b) >>> 0;
    h = Math.imul(h ^ (b >>> 0), 0xc2b2ae35) >>> 0;
    return (h ^ (h >>> 15)) >>> 0;
  }
  function passText(s) {
    let h = 2166136261 >>> 0;
    s = String(s);
    for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619) >>> 0;
    return h >>> 0;
  }
  // The rolled values for one crossing, or a reason. A record that does not check out hands back a
  // reason and the caller refuses the WHOLE row — half a rolled score is the one outcome no road
  // here produces. A rolled value is checked against its own span before it is handed back: the
  // roll cannot produce one outside, so a value that lands there says the roll itself is broken, and
  // that is a refusal rather than a picture nobody can read back to a number.
  function passBreath(key, fam) {
    if (!fam || typeof fam !== "object" || Array.isArray(fam)) return { why: "its family bounds are no record" };
    const odd = Object.keys(fam).filter((f) => ["spans", "seed"].indexOf(f) < 0);
    if (odd.length) return { why: "its family bounds name «" + odd[0] + "», in no allow-list" };
    if (fam.seed !== undefined && typeof fam.seed !== "boolean") return { why: "its family seed is no yes-or-no" };
    const spans = fam.spans === undefined ? {} : fam.spans;
    if (!spans || typeof spans !== "object" || Array.isArray(spans)) return { why: "its family spans are no record" };
    const at = passGen, visit = passVisitSeed();
    const pass = passMix(passMix(visit, at), passText(key));
    const names = Object.keys(spans), v = {};
    for (let i = 0; i < names.length; i++) {
      const s = spans[names[i]];
      if (!Array.isArray(s) || s.length !== 2 || !Number.isFinite(+s[0]) || !Number.isFinite(+s[1])
          || +s[0] > +s[1]) {
        return { why: "the span for «" + names[i] + "» is no low-to-high pair of numbers" };
      }
      const lo = +s[0], hi = +s[1];
      const got = lo + (passMix(pass, passText(names[i])) / 4294967296) * (hi - lo);
      if (!(got >= lo && got <= hi)) {
        return { why: "the rolled «" + names[i] + "» " + got + " stands outside its span "
                      + lo + "…" + hi };
      }
      v[names[i]] = got;
    }
    const seed = fam.seed ? passMix(pass, 0x5eed5) / 4294967296 : null;
    passNote(passFamilies, { pair: key, at: at, visit: visit, pinned: passVisitPinned, seed: pass,
                             scoreSeed: seed, spans: spans, applied: v });
    return { v: v, seed: seed, at: at, visit: visit, seedOfPass: pass };
  }

  // ---- the composed road (§4.4d, U27 stage 0) ---------------------------------------------------
  // WHERE A SCORE COMES FROM. It is DERIVED, here, at the instant the walk casts the pair, from the
  // two works' own records. His word of 2026-08-17 19:21: the collection grows to thousands of works
  // and nothing on the product path may scale with the number of pairs. A table of pairs is
  // quadratic in the collection — 121 works are already 10 558 ordered pairs — while a record per
  // work is linear, and the whole living collection's records weigh 33 000 B gzipped where the pair
  // rows they replace weighed 1 862 611 B.
  //
  // WHAT LEFT WITH THE TABLE. Three roads used to answer for a pair's score, and all three are gone:
  // `pass.scores` keyed by ordered pair, the delivery pack read through pass-reader.js, and
  // `pass.scoreTables` filled into `pass.scoreTemplates`. So are the reader file, the shard warming
  // that fetched a work's outgoing crossings at every landing, and the site steps that staged and
  // copied the packs. A pair no longer has a score to find; it has one to derive.
  //
  // THE COMPOSER TRAVELS AS ITS OWN FILE, the way the picture layer and the instruments do. It is
  // fetched once, at the walk's first landing on a visit whose settings record actually carries the
  // records it reads and whose layer is on, and a visit that never reaches that state never asks for
  // it. Nothing ever waits on it: a crossing declared before it has arrived answers nothing and
  // falls through to the walk's own glide, exactly as a pair with no score always has. What stays
  // HERE is the door — where the composer is asked for, the request the walk builds for it, and the
  // one synchronous question a declare puts to it.
  const PASS_COMPOSER_SRC = "pass-composer.js";
  let passComposer = null, passComposerAsked = false, passComposerState = "absent";
  let passComposerSaid = null;
  const passPassages = [];

  // ---- THE RECORD WAVE (2026-08-19, U27 stage 3) -------------------------------------------------
  // `config.json`'s `pass` block used to carry `works` — one record per work of the whole collection
  // — so the first thing every visitor loaded grew with the collection, whether the walk was ever
  // going to show ten works or the whole gallery. His word of 13:39: a visitor picks a picture at the
  // door, ten works are chosen for it, and the visitor may add five twice more — the walk already
  // has that shape (`SPREAD`, `UNFOLD`, `MAXU`, `CAP` above), and the wire now follows it. `pass`
  // carries `records: { route, cap }` instead, and the client asks the route for exactly the ids of
  // one SELECTION at a time — never a work at a time — the instant that selection is known.
  //
  // A SELECTION IS A WAVE, and a wave is the ids `appendFrames` is about to put on the page
  // (14-walk-render.js): the first is the SPREAD the door's pick assembles, and each later one is
  // the UNFOLD ids an unfold appends. There is no third source of a wave — `appendFrames` is the one
  // place `.exh-frame` elements are ever created, whichever road walked the visitor there (a fresh
  // hang, a restored one, a hash arrival, a series glide) — so the hook lives once, at that source,
  // rather than at every road that can lead to it.
  //
  // WHAT THIS FILE OWNS is the map the wave fills and nothing else: no request loop, no retry, no
  // wait. `passWorkRecords` used to read the wire's own `works` directly; it now hands back this
  // map instead, filled wave by wave, so `passRequestFor` below and its null answer for a record
  // that has not arrived (INV: a missing record is exactly a record the walk has not asked for yet,
  // or asked for and has not heard back about) keep working unchanged — the walk's own glide is the
  // one fallback there has ever been for a pair with no record, and it stays the one fallback here.
  let passRecordsMap = Object.create(null);
  // Which ids this visit has ever asked the route for, whether the wave that asked landed or not. An
  // id is asked once: the walk never shows the same work twice inside one visit's own `order`, so
  // there is no second wave that could ever want it, and a failed wave is not retried onto a loop —
  // its ids simply stay unheld, and the pairs that would have used them take the walk's own glide.
  let passRecordsAsked = Object.create(null);
  // SAID ONCE, the way the composer's own absence is (`passComposerSaid` above): the reason the
  // route is missing is one fact about the visit, not one fact per wave, so it is written to the
  // refusal ring a single time rather than pushing every other refusal off it within a few steps —
  // the very defect U10 §5 read on the settings register before this file learned to say things once.
  let passRecordsRouteSaid = null;
  // How many waves this visit has sent, counted on the way out so the diagnostic surface can tell a
  // walk that has asked nothing yet from one whose wave is still in flight.
  let passRecordsWaves = 0;
  // …and how many of them have settled, landed or failed alike. The two together say whether the
  // walk is still waiting on the wire for anything at all.
  let passRecordsSettled = 0;
  function passRecordsRoute() { return (((EX && EX.pass) || (cfg && cfg.pass) || {})).records; }
  function passWorkRecords() { return passRecordsMap; }
  // THE ONE DOOR A WAVE COMES THROUGH. Handed the ids of the selection about to be shown, it asks the
  // route for whichever of them this visit has not asked for yet, in ONE request — never a per-id
  // loop, because the unit the composer reasons about is the selection and not a single work — and
  // it never waits for the answer: the caller (`appendFrames`) renders the instant it is called, and
  // this function's own promise resolves later, off to the side, filling `passRecordsMap` if and
  // when it lands. A crossing declared before a wave lands finds its record simply missing, which is
  // the walk's own glide, exactly as a pair with no record has always meant.
  function passRecordsAskFor(ids) {
    // A VISITOR WHO WILL NEVER SEE A CROSSING CARRIES NOTHING FOR ONE (2026-08-19). A record wave is
    // bytes of the picture layer, so a visit that has already decided to play no crossing asks for
    // none of them: the wire has to name the layer on, and stillness or a saved-data connection each
    // stand it down. The two facts this gate does NOT read are `passOpen`'s own: the registry's
    // resolved switch and the drawing-surface probe. A wave fires while the walk is FIRST RENDERING,
    // which is earlier than the layer opens, and both of those answer for a moment that has not
    // arrived yet — the probe would also spend a WebGL context at the one instant the first paint is
    // being laid out. The switch is read straight off the wire instead, which is the same fact
    // without the timing, and the surface is left to `passOpen` where it belongs: a device without
    // it simply never opens the layer, and the records it holds go unread rather than unfetched.
    const rc = passRecordsRoute();
    if (rc && (((EX && EX.pass) || (cfg && cfg.pass) || {}).visualLayer !== "pass")) return;
    const still = REDUCED ? "reduced motion" : dataSaver() ? "save data" : null;
    if (still) {
      // SAID ONCE, AND SAID HERE, because on such a visit it is the ONLY place it can be said. The
      // layer's own stand-down sentence is written by `passOpen`, and `passOpen` is reached by way
      // of a crossing that finds its two records — which a still visit never has. Without this line
      // the surface of a visit in stillness reads «asked for a crossing before it arrived», which is
      // true of the composer and says nothing about why the visit was never going to have one.
      if (passRecordsRouteSaid !== still) {
        passRecordsRouteSaid = still;
        passNote(passRefusals, { what: "records", name: "wave", why: still });
      }
      return;
    }
    if (!rc || typeof rc !== "object" || typeof rc.route !== "string" || !rc.route) {
      // THE STAND-DOWN LAW BINDS THIS ROAD TOO (EX-LOAD-3 / INV-73), the same way it binds the
      // composer's and the layer's own fetches: a wire that names no route is a wire this visit
      // never asks anything of, and every crossing takes the walk's own glide from the first step.
      if (passRecordsRouteSaid !== "absent") {
        passRecordsRouteSaid = "absent";
        passNote(passRefusals, { what: "records", name: "route",
                                 why: "the settings record carries no pass.records.route: no wave "
                                      + "is ever asked for, and the walk's own glide plays every "
                                      + "crossing" });
      }
      return;
    }
    const want = [];
    (ids || []).forEach((id) => {
      const s = String(id);
      if (!passRecordsAsked[s] && want.indexOf(s) < 0) want.push(s);
    });
    if (!want.length) return;
    // THE CAP IS THE ROUTE'S OWN, read off the wire rather than assumed: the server refuses more
    // than its own `cap` ids with a 400, and a copy of the number here would go stale the day an
    // instance's walk widens. A wire that names no usable cap falls back to this walk's own CAP —
    // the most this visit's route could ever need in one wave whatever the wire says — so a request
    // is still bounded even where the wire is silent about the number.
    const cap = Number.isFinite(+rc.cap) && +rc.cap > 0 ? Math.floor(+rc.cap) : CAP;
    let asked = want;
    if (want.length > cap) {
      asked = want.slice(0, cap);
      const left = want.slice(cap);
      passNote(passRefusals, { what: "records", name: "wave",
                               why: left.length + " id(s) of this wave stand over the route's own "
                                    + "cap of " + cap + " and are not asked for: " + left.join(",") });
    }
    // MARKED ASKED BEFORE THE REQUEST LANDS, not after: a second wave that starts while this one is
    // still in flight must not ask the route for the same id twice, and marking on send rather than
    // on receipt is what makes that true regardless of how long the route takes to answer.
    asked.forEach((id) => { passRecordsAsked[id] = true; });
    passRecordsWaves += 1;
    // THE STAMP RIDES ON THE ADDRESS so a long-held answer can never outlive the records it holds:
    // the bake writes the map's own digest beside the route, and a rebake that changes a single
    // measurement changes every address this walk asks at (2026-08-19). A wire with no stamp asks
    // without one, and the answer is then only as fresh as its own cache header says.
    const url = rc.route + "?ids=" + asked.slice().sort().map(encodeURIComponent).join(",")
      + (rc.stamp ? "&v=" + encodeURIComponent(String(rc.stamp)) : "");
    fetch(url)
      .then((r) => {
        if (!r.ok) throw new Error("the route answered " + r.status);
        return r.json();
      })
      .then((got) => {
        if (!got || typeof got !== "object" || !got.records || typeof got.records !== "object") {
          throw new Error("its answer carries no readable «records»");
        }
        // AN ID THE ANSWER OMITS IS NOT A FAILURE — §3's own contract is that the route omits an id
        // it does not carry — so nothing is noted for it here; the pair that would have used it
        // simply finds no record and takes the walk's own glide, same as always.
        asked.forEach((id) => {
          const rec = got.records[id];
          if (rec && typeof rec === "object") passRecordsMap[id] = rec;
        });
        passPrewarmAhead();   // this wave may be exactly what an earlier prewarm attempt was missing
      })
      .catch((e) => {
        // THE MAP STANDS AS IT WAS. A wave that fails — network, a refusing status, an answer this
        // client cannot read — changes nothing it has already been given; it only leaves this wave's
        // own ids unheld, and it is never retried: the next fact this visit reads about the route is
        // whatever the NEXT wave's own ids bring, not a repeat of this one.
        passNote(passRefusals, { what: "records", name: "wave",
                                 why: "the wave for " + asked.length + " id(s) did not land: "
                                      + (e && e.message ? e.message : String(e)) });
      })
      // SETTLED EITHER WAY. The wave is off the wire whether it landed or failed, and the readiness
      // the diagnostic surface publishes is about the wire rather than about the outcome.
      .then(() => { passRecordsSettled += 1; }, () => { passRecordsSettled += 1; });
  }
  function passComposerConsts() { return (((EX && EX.pass) || (cfg && cfg.pass) || {})).composer; }
  // The composer hands over a factory rather than a finished composer, so the bundle stays the one
  // owner of the settings block: the composer is handed the collection's own constants and reaches
  // nothing else in this file.
  function passComposerSet(part) {
    passComposer = null;
    const mk = part && part.make;
    if (typeof mk !== "function") {
      passComposerState = "refused";
      passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC,
                               why: "handed over no composer" });
      return;
    }
    try { passComposer = mk(passComposerConsts()) || null; } catch (e) { passComposer = null; }
    passComposerState = passComposer ? "read" : "refused";
    if (!passComposer) {
      passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC,
                               why: "the collection's constants made no composer" });
    } else {
      passPrewarmAhead();   // the composer was the missing half of every request built so far
    }
  }
  function passComposerOpen() {
    if (passComposerAsked) return;
    const consts = passComposerConsts();
    if (!consts || typeof consts !== "object" || !Object.keys(consts).length) return;
    if (passGet("visualLayer") !== "pass") return;
    // THE STAND-DOWN LAW BINDS THIS FETCH AS A CLASS (EX-LOAD-3 / INV-73), the same way it bound the
    // pack's. `passOpen` below reads the same two questions and stands the drawing machinery down,
    // so a visit under either request plays no crossing at all — fetching the file that decides one
    // would be a fetch for a crossing that can never run.
    const no = REDUCED ? "reduced motion" : dataSaver() ? "save data" : null;
    if (no) {
      passComposerAsked = true;
      passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC, why: no });
      return;
    }
    passComposerAsked = true;
    passComposerState = "asked";
    try {
      window.__@@NS@@PassComposer = passComposerSet;
      const s = document.createElement("script");
      s.src = PASS_COMPOSER_SRC;
      s.async = true;
      s.onerror = () => {
        passComposerState = "absent";
        passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC, why: "load failed" });
      };
      document.head.appendChild(s);
    } catch (e) {
      passComposerState = "absent";
      passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC, why: "no door" });
    }
  }

  // THE DIE THE WALK ROLLS, once per crossing. Charter shelf 16: a pinned seed reproduces a run
  // exactly, which is the judging mode, and the public walk rolls a fresh one each time, which is
  // the viewer mode. Both fall out of `passVisitSeed` above with no second idea of what a seed is —
  // the visit's own seed (pinned by `familySeed` or rolled once), the pass index the declare has
  // already minted, and the edge's own key. Nothing here reads a clock.
  //
  // The span is the composer's own and is READ from it: the choice core fences its seed at 0…8 and
  // the meshing instrument's manifest publishes the same span for its `seed` handle. A copy of it
  // here would be a copy that goes stale.
  // `again` is the number of the die within one crossing. A crossing is offered one die; where the
  // walk's own memory asks for another — a family still cooling on this edge — the next die is
  // rolled from the same three numbers with the try mixed in, so the second die is as reproducible
  // as the first and a pinned run stays pinned. Try 0 is the one die stage 0 rolled, unchanged.
  function passSeedFor(key, again) {
    const span = (passComposer && passComposer.seedSpan) || [0, 8];
    const lo = +span[0], hi = +span[1];
    let h = passMix(passMix(passVisitSeed(), passGen), passText(key));
    if (again) h = passMix(h, again >>> 0);
    return lo + (h / 4294967296) * (hi - lo);
  }

  // ---- THE MEMORY OF A VISIT (§4.8, charter shelf 16) --------------------------------------------
  // WHAT AN EDGE REMEMBERS. One record per edge and direction, keyed by the two work ids sorted:
  // the family, the pivot, the die, how many passes have run, when the last one ran, its cooldown
  // and the plan before it. It is created as an edge first plays and it is the SITE'S OWN — the
  // engine never sees it. Only the return reference of §4.8 — the family, the seed and the pass
  // index — crosses into the request, and that fence is a refusal on the composer's side, so
  // nothing wider can leak through even by accident.
  //
  // NOTHING HERE SCALES WITH THE NUMBER OF PAIRS (his 19:21 word). A record is written when an edge
  // is walked, so the store grows with the visitor's own steps and never with the collection; it is
  // pruned to the youngest `keep` records and anything past its own cooldown is dropped as it is
  // read. The lab's `build-edgememory-v1.py` enumerates all 7 260 edges into an 8.5 MB file, which
  // is exactly the class that word bans; it stays reference material and its data ships nowhere.
  //
  // WHAT IT HOLDS ABOUT THE PERSON: nothing. Two work ids, a family token, a pivot, numbers and two
  // stamps. No visitor identity, no remembered place, no counting wire — the same fence §4.5 draws.
  const PASS_EDGE_SRC = "@@NS@@-pass-edges";
  // THE NUMBERS OF THE EDGE MEMORY, and what is left of them after 2026-08-18.
  //
  // TWO WENT, and they were the pair that turned a reading into a verdict: how close two traces had
  // to sit before the backward pass READ AS the forward one played in reverse — a mean of 0.02 and
  // a worst of 0.05, neither measured, neither with a requirement of his behind it. The distance
  // itself is what the ranking wanted all along, and `passMirrorDistance` hands it over now.
  //
  // WHAT REMAINS, and whose each is. `visitWindowSeconds` and `cooldownSeconds` are the lab
  // builder's own (`lab/data/edgememory/defaults.json`), both awaiting the owner's eye: how long
  // after the last pass a return still counts as the same visit, and how long a record is kept. They
  // decide no crossing — the family-cooling READING is «did this family play last here», which needs
  // no duration — and are named as waiting rather than removed. `driftSpan` and `driftOpensOver`
  // shape §4.4f's own breath, which is charter shelf 16's; `keep` and `traceHandles` are working
  // values of this seat with nothing artistic resting on them.
  //
  // `dice` MOVED FROM 3 TO 8 (2026-08-19), and the move is a defect this pass found in
  // `tests/test_pass_memory.py` rather than a budget it wanted. On a RETURN edge the recorded
  // family is held by the composer's own genre choice (`pass-composer.js`, `genreFor`'s kinship
  // steps) — the die is not rolled for the family at all where a genre carrying it is reachable —
  // so on exactly the edges this number governs, consecutive dice land on the same family by
  // construction and the loop's own early-out ("a second die that lands on the same family says
  // the die does not reach this choice") stops the search after two tries almost every time, never
  // three. What still varies try to try under a held family is the rest of the plan — the actors,
  // the camera, which specific handle values the pass travels through — and that is exactly what
  // `passMirrorDistance` reads. Three tries, effectively two, measured on the fixed two-work-kind
  // fixture `tests/fixture_pass_composed.json` walks over many runs, missed a roll standing clear
  // of the recorded pass's own mirror often enough to redden the suite on an honest crossing — no
  // wire fault, no timing fault, just too few chances at a mechanism whose own comment already
  // named it a knob and not a law. 8 is not a measured floor; it is enough tries that the miss
  // rate this pass observed (roughly one run in four before the change) fell to none of nineteen
  // runs after it. Nothing here is on the hot path: `passEdgeJudge` answers a first-ever crossing
  // on its opening line, before any die is rolled, so the cost of a few extra tries is paid only on
  // a walked-back or repeated edge — never on the ordinary width of a visit.
  const PASS_EDGE = {
    visitWindowSeconds: 1800,
    cooldownSeconds: 86400,
    driftSpan: 0.25,
    driftOpensOver: 3,
    dice: 8,
    keep: 64,
    traceHandles: 48,
  };
  let passEdgeRows = null, passEdgeStorage = "unread";
  // The clock is read HERE and nowhere else, and it never reaches a die. A cooldown and a visit
  // window are wall time by their nature; a roll that read a clock would make a pinned run
  // irreproducible, which is the very thing §4.4b's determinism row exists to hold.
  function passEdgeNow() { return Date.now(); }
  function passEdgeFresh(why) {
    passEdgeStorage = "fresh";
    passNote(passRefusals, { what: "memory", name: PASS_EDGE_SRC, why: why });
  }
  // The store, read once and held for the visit. A visitor whose storage is closed or cleared walks
  // with a fresh pool and the surface says which of the two happened.
  function passEdgeAll() {
    if (passEdgeRows) return passEdgeRows;
    passEdgeRows = Object.create(null);
    let raw = null;
    try { raw = localStorage.getItem(PASS_EDGE_SRC); }
    catch (e) {
      passEdgeStorage = "unavailable";
      passNote(passRefusals, { what: "memory", name: PASS_EDGE_SRC,
                               why: "the browser's own storage is closed: a fresh pool this visit" });
      return passEdgeRows;
    }
    if (raw === null || raw === undefined) { passEdgeStorage = "fresh"; return passEdgeRows; }
    let read = null;
    try { read = JSON.parse(raw); } catch (e) { read = null; }
    if (!read || read.v !== 1 || !read.edges || typeof read.edges !== "object") {
      passEdgeFresh("the stored record is nothing this walk can read: a fresh pool");
      return passEdgeRows;
    }
    const now = passEdgeNow();
    let dropped = 0;
    Object.keys(read.edges).forEach((k) => {
      const both = read.edges[k];
      if (!both || typeof both !== "object") return;
      const kept = {};
      Object.keys(both).forEach((d) => {
        const r = both[d];
        // A record past its own cooldown says nothing any more — the family it cooled is free
        // again — so it is dropped as it is read and the store stays small by construction.
        if (!r || !Number.isFinite(+r.lastAt) || !r.family) return;
        if (now - +r.lastAt > PASS_EDGE.cooldownSeconds * 1000) { dropped += 1; return; }
        kept[d] = r;
      });
      if (Object.keys(kept).length) passEdgeRows[k] = kept;
    });
    passEdgeStorage = "read";
    if (dropped) {
      passNote(passEvents, { at: Math.round(performance.now()), name: "memory-pruned",
                             gen: passGen, kind: null, cause: null, from: null, to: null,
                             why: dropped + " record(s) past their cooldown" });
    }
    return passEdgeRows;
  }
  // Writing back. The youngest `keep` records stand and the rest go, so a browser that walks for
  // years carries a bounded store; a storage that refuses the write is said once and the visit goes
  // on without a memory, which is the fresh-pool case.
  function passEdgePut() {
    if (passEdgeStorage === "unavailable") return;
    const rows = passEdgeAll();
    const all = [];
    Object.keys(rows).forEach((k) => {
      Object.keys(rows[k]).forEach((d) => { all.push({ k: k, d: d, at: +rows[k][d].lastAt }); });
    });
    // A TRACE OUTSIDE THE VISIT WINDOW IS EVIDENCE FOR A CHECK THAT CAN NO LONGER RUN — the two
    // refusals judge a pass against the one this visit remembers — so it is dropped on the way to
    // storage. The record keeps saying what it says; only the numbers nobody will read again go.
    const now = passEdgeNow();
    all.forEach((row) => {
      const r = rows[row.k][row.d];
      if (r.provenance && r.provenance.trace
          && now - +r.lastAt > PASS_EDGE.visitWindowSeconds * 1000) {
        r.provenance.trace = null;
      }
    });
    if (all.length > PASS_EDGE.keep) {
      all.sort((x, y) => y.at - x.at);
      all.slice(PASS_EDGE.keep).forEach((row) => {
        delete rows[row.k][row.d];
        if (!Object.keys(rows[row.k]).length) delete rows[row.k];
      });
    }
    try { localStorage.setItem(PASS_EDGE_SRC, JSON.stringify({ v: 1, edges: rows })); }
    catch (e) {
      passEdgeStorage = "unavailable";
      passNote(passRefusals, { what: "memory", name: PASS_EDGE_SRC,
                               why: "the browser's own storage took no record: a fresh pool this "
                                    + "visit" });
    }
  }

  // THE FAMILY, read off the composed plan and never written onto it. The lab builder's own law
  // (`build-edgememory-v1.py`, family_of_plan): the transform the pivot's cut implies, joined by a
  // plus sign to the measure the passage travels, or «tone» where nothing travels. Both halves
  // stand on the plan already, so §4.7 gains no field for this.
  function passFamilyOf(plan) {
    if (!plan || !plan.pivot) return null;
    const t = plan.pivot.transform || plan.pivot.kind || "tone_bridge";
    const axis = (plan.travellingAxis && plan.travellingAxis.measure)
      ? plan.travellingAxis.measure : "tone";
    return t + "+" + axis;
  }
  // The ground is the stack's primary voice: it is the one full-frame instrument the viewer meets
  // before the other voices write over it.  Read it from the emitted cue list, never from a table.
  function passPrimaryOf(passage) {
    const cues = passage && passage.score && Array.isArray(passage.score.cues)
      ? passage.score.cues.slice() : [];
    cues.sort((a, b) => (+a.stack || 0) - (+b.stack || 0));
    const i = cues[0] && cues[0].instrument;
    return i && i.id ? String(i.id) : null;
  }
  let passRoutePlayed = [];
  let passRouteFamilyCount = Object.create(null);
  let passRouteInstrumentCount = Object.create(null);
  let passRouteWorldSeen = false;
  // The pivot as a thing rather than a strength: what the passage holds, without the number the
  // pair happens to hold it at. Two passes hold the same pivot when these three agree.
  function passPivotOf(plan) {
    if (!plan || !plan.pivot) return null;
    const p = plan.pivot;
    return { kind: p.kind || null, measure: p.measure === undefined ? null : p.measure,
             cut: p.cut === undefined ? null : p.cut,
             transform: p.transform === undefined ? null : p.transform };
  }
  function passPivotSame(x, y) {
    return !!x && !!y && x.kind === y.kind && x.measure === y.measure && x.cut === y.cut;
  }
  // A handle's own declared span, read off the instrument's manifest in the collection's constants.
  // The manifest is the one home of that fact; a copy here would go stale the day an instrument
  // widens a handle.
  function passHandleSpan(instrument, handle) {
    const m = (passComposerConsts() || {}).manifests || {};
    const h = (m[instrument] && m[instrument].handles) ? m[instrument].handles[handle] : null;
    if (!h || !Number.isFinite(+h.min) || !Number.isFinite(+h.max)) return null;
    // `banding` on a handle is the manifest's own word for a handle whose numbers NAME STATES rather
    // than measure an amount — the weave's `axis` is vertical or horizontal, and a value between
    // them is neither. Such a handle is no place for a breath.
    return { lo: +h.min, hi: +h.max,
             rungs: (h.rungs === undefined || h.rungs === null) ? null : h.rungs,
             named: !!h.banding };
  }

  // WHAT A PASS LOOKED LIKE, in the few numbers a reversal can be read off: the cues in the order
  // they play, each with its instrument, its window as a fraction of the passage, and every handle
  // it drives with the two ends that handle travels between. A static handle's two ends are the
  // same number. The doors themselves — `mix` — and the clock are left out: both are the same in
  // every pass by law, so they would say nothing about whether this pass is that one reversed.
  function passTraceOf(score) {
    if (!score || !Array.isArray(score.cues) || !score.cues.length) return null;
    const ms = Number(score.duration) || 0;
    if (!(ms > 0)) return null;
    let room = PASS_EDGE.traceHandles;
    const cues = score.cues.map((c) => {
      const w = Array.isArray(c.window) ? c.window : [0, 0];
      const h = {};
      Object.keys(c.tracks || {}).sort().forEach((name) => {
        if (name === "mix" || name === "clock" || room <= 0) return;
        const node = (c.nodes || {})[((c.tracks[name] || {}).node) || (c.id + "-" + name)];
        if (!node) return;
        if (node.op === "static" && Number.isFinite(+node.value)) {
          h[name] = [+node.value, +node.value];
        } else if (node.op === "mix" && Number.isFinite(+node.a) && Number.isFinite(+node.b)) {
          h[name] = [+node.a, +node.b];
        } else return;
        room -= 1;
      });
      return { id: c.id, i: (c.instrument && c.instrument.id) || null,
               w: [(+w[0] * 1000) / ms, (+w[1] * 1000) / ms], h: h };
    });
    return { ms: ms, cues: cues };
  }
  // AN AUTOMATIC REVERSED VIDEO IS REFUSED (§4.8). The backward pass reads as the forward one played
  // in reverse when the cues run in the opposite order on the same instruments, each window is the
  // mirror of its own, and every handle travels its two ends the other way about — all of it inside
  // the reversal tolerance, which is a fraction of the handle's own measured range across the
  // recorded pass. Anything the recorded pass never drove, or a different instrument in the place,
  // means these two are simply different passes and there is nothing to refuse.
  function passMirrorDiff(now, before) {
    if (!now || !before || !now.cues.length || now.cues.length !== before.cues.length) return null;
    const diffs = [];
    for (let i = 0; i < now.cues.length; i++) {
      const c = now.cues[i], p = before.cues[before.cues.length - 1 - i];
      if (!p || c.i !== p.i) return null;
      diffs.push(Math.abs(c.w[0] - (1 - p.w[1])));
      diffs.push(Math.abs(c.w[1] - (1 - p.w[0])));
      const names = Object.keys(c.h);
      if (!names.length) return null;
      for (let j = 0; j < names.length; j++) {
        const n = names[j], a = c.h[n], b = p.h[n];
        if (!b) return null;
        // The handle's own measured range across the recorded pass, which is what the tolerance is
        // a fraction of. A handle that stood still has no range of its own, so its declared span
        // stands in; a handle with neither is read against 1, which is the plainest reading of a
        // number with no scale.
        const span = passHandleSpan(c.i, n);
        let range = Math.abs(b[1] - b[0]);
        if (!(range > 0)) range = span ? Math.abs(span.hi - span.lo) : 0;
        if (!(range > 0)) range = 1;
        diffs.push(Math.abs(a[0] - b[1]) / range);
        diffs.push(Math.abs(a[1] - b[0]) / range);
      }
    }
    if (!diffs.length) return null;
    let sum = 0, worst = 0;
    for (let i = 0; i < diffs.length; i++) { sum += diffs[i]; if (diffs[i] > worst) worst = diffs[i]; }
    return { mean: sum / diffs.length, worst: worst };
  }
  // HOW FAR THIS PASS STANDS FROM THE RECORDED ONE PLAYED BACKWARDS — a distance, not a verdict.
  //
  // Two numbers stood here, a mean of 0.02 and a worst of 0.05, and they turned this distance into
  // a yes or a no: under both, the pass «read as a replay» and was refused, which cost the visitor
  // the whole crossing. Neither number was measured and neither had a requirement of his behind it,
  // so both are gone (his word of 2026-08-18 09:57). What is left is the distance itself, which is
  // all the ranking ever needed: of the dice this edge is offered, the one standing FURTHEST from
  // the recorded pass's mirror is the one that plays.
  //
  // A PASS THAT IS ITS OWN MIRROR SAYS NOTHING ABOUT AUTHORSHIP. Where the recorded pass runs the
  // same forwards and backwards — one cue over the whole passage with every handle standing still —
  // every pass on that edge matches its mirror, and reading that as a replay would be reading the
  // shape of the recorded one rather than this one. The reading answers with nothing there.
  function passMirrorDistance(now, before) {
    const d = passMirrorDiff(now, before);
    if (!d) return null;
    const self = passMirrorDiff(before, before);
    if (self && self.mean <= d.mean) return null;
    return d.mean;
  }
  // §4.8'S TWO READINGS OF A PASS, both taken HERE, because the record they read against is the
  // walk's own and the engine never sees it. A pass that carries a return reference is kin to the
  // one before it — the same family or the same pivot — and it is not that one run backwards.
  //
  // THEY WERE REFUSALS UNTIL 2026-08-18, and a refusal here cost the visitor the whole crossing:
  // the passage played nothing and the walk's plain glide ran instead. His word of 09:51 strikes
  // that out — any two photographs get a crossing — so both readings now RANK the dice this edge is
  // offered. Kinship is a plain fact and needs no number: a roll that shares neither the family nor
  // the pivot ranks below one that shares either. The mirror is a DISTANCE: of the rolls left, the
  // one standing furthest from the recorded pass's mirror plays. Nothing is refused, and nothing
  // about the law is loosened — a replay is still the last thing this walk will show.
  //
  // What comes back is {kin, distance, why}: `kin` says whether §4.8's first reading holds, and
  // `distance` is how far this roll stands from the recorded pass's mirror, with nothing where the
  // reading does not apply.
  function passEdgeJudge(passage, before) {
    if (!before || !passage || !passage.plan || !passage.score) {
      return { kin: true, distance: null, why: null };
    }
    const fam = passFamilyOf(passage.plan), piv = passPivotOf(passage.plan);
    const kin = fam === before.family || passPivotSame(piv, before.pivot);
    const distance = passMirrorDistance(passTraceOf(passage.score),
                                        before.provenance ? before.provenance.trace : null);
    let why = null;
    if (!kin) {
      why = "it shares neither the family «" + String(before.family) + "» nor the pivot of the "
          + "pass recorded on this edge: the way back is kin to the way out, never absolutely "
          + "alien";
    } else if (distance !== null) {
      why = "it stands " + distance.toFixed(4) + " of the recorded pass's own range from that "
          + "pass played backwards — the cues run in the opposite order on the same instruments "
          + "and every handle travels its ends the other way about";
    }
    return { kin: kin, distance: distance, why: why };
  }

  // THE DOOR BREATHES ON A REPEATED EDGE (charter shelf 16, §4.4f). A second pass over one edge
  // inside a visit holds the family and shifts its shaping numbers a little; a third shifts them
  // further, and by the fourth the drift stands at its whole declared width. The pass count on the
  // record is what the reach reads, and the roll is §4.4f's own — `passBreath` — so there is one
  // idea of a family's breath and not two.
  //
  // WHAT NEVER DRIFTS. A handle the composer measured off the works (`measuredHandles`) carries the
  // work's own structure — his 19:13 word lifted to the class at 19:21 — and a drift over it would
  // overwrite a measurement with a number nobody read. The doors (`mix`) and the clock never drift
  // either: an effect enters and leaves through its zero whatever the pass. The die is left alone
  // too, since it already travels as the walk's own roll.
  function passDriftScore(score, key, passes) {
    if (!score || !Array.isArray(score.cues) || !(passes > 0)) return null;
    const reach = PASS_EDGE.driftSpan * Math.min(1, passes / PASS_EDGE.driftOpensOver);
    if (!(reach > 0)) return null;
    const spans = {}, homes = [];
    score.cues.forEach((c) => {
      const instr = (c.instrument && c.instrument.id) || null;
      if (!instr) return;
      Object.keys(c.tracks || {}).sort().forEach((name) => {
        if (name === "mix" || name === "clock" || name === "seed") return;
        if (c.measuredHandles && c.measuredHandles[name] !== undefined) return;
        const span = passHandleSpan(instr, name);
        if (!span || span.rungs !== null || span.named || !(span.hi > span.lo)) return;
        const node = (c.nodes || {})[((c.tracks[name] || {}).node) || (c.id + "-" + name)];
        if (!node || node.op !== "static" || !Number.isFinite(+node.value)) return;
        const v = +node.value, w = (span.hi - span.lo) * reach;
        const lo = Math.max(span.lo, v - w), hi = Math.min(span.hi, v + w);
        if (!(hi > lo)) return;
        const slot = c.id + "." + name;
        spans[slot] = [lo, hi];
        homes.push({ slot: slot, node: node, base: v });
      });
    });
    if (!homes.length) return null;
    const rolled = passBreath(key + "#" + passes, { spans: spans });
    if (rolled.why) {
      passNote(passRefusals, { what: "memory", name: "drift", why: rolled.why });
      return null;
    }
    const moved = {};
    homes.forEach((h) => {
      const got = rolled.v[h.slot];
      if (!Number.isFinite(got)) return;
      h.node.value = Math.round(got * 10000) / 10000;
      // The note is what a picture that looks wrong is read back through, so it says the number
      // moved instead of going on describing the value the composer wrote.
      if (typeof h.node.note === "string" && h.node.note.indexOf("drifted") !== 0) {
        h.node.note = "drifted; " + h.node.note;
      }
      moved[h.slot] = [h.base, h.node.value];
    });
    return { passes: passes, reach: reach, moved: moved };
  }

  // THE EDGE THIS STEP WALKS, and what the walk's own memory says about it. The key is the two ids
  // sorted, whichever way the visitor walks, and `direction` says which way this passage runs, so
  // A to B and B to A are two distinct passages of one edge hanging on one stable key.
  function passEdgeContext(fromEl, toEl) {
    const from = fromEl && fromEl.dataset ? fromEl.dataset.id : null;
    const to = toEl && toEl.dataset ? toEl.dataset.id : null;
    if (!from || !to) return null;
    const forward = String(from) <= String(to);
    const key = String(forward ? from : to) + "__" + String(forward ? to : from);
    const direction = forward ? "a-to-b" : "b-to-a";
    const rows = passEdgeAll()[key] || null;
    const mine = rows ? (rows[direction] || null) : null;
    const other = rows ? (rows[direction === "a-to-b" ? "b-to-a" : "a-to-b"] || null) : null;
    let last = mine;
    if (other && (!last || +other.lastAt > +last.lastAt)) last = other;
    const now = passEdgeNow();
    // WITHIN A VISIT the family is held and the door breathes; ACROSS the visit boundary the pool
    // re-rolls and the family that just played is cooled (charter shelf 16). The boundary between
    // the two is the visit window, read off the last pass on this edge rather than off the page's
    // own life, so a visitor who reloads mid-thought keeps their thread.
    const within = !!last && (now - +last.lastAt) <= PASS_EDGE.visitWindowSeconds * 1000;
    const passes = within ? ((mine ? mine.passCount : 0) + (other ? other.passCount : 0)) : 0;
    return {
      key: key, direction: direction, last: last, within: within, passes: passes,
      cooled: (last && !within) ? last.family : null,
      // THE WHOLE OF WHAT CROSSES (§4.8). Three fields, and the composer refuses a fourth.
      memory: within ? { family: last.family, seed: last.seed, passIndex: last.passCount } : null,
    };
  }

  // ---- THE STEP'S ROLE ON THE ROUTE (charter shelf 15; U27 stage 2) -----------------------------
  // THE ROUTE IS THE WALK ITSELF. The hang shows `SPREAD` works and unfolds `MAXU` times by
  // `UNFOLD` — 10, then 5, then 5 on this instance's own settings, which is the route his 18:43 word
  // names. Nineteen steps at full length, and the walk deals WHICH works stand at them afresh every
  // visit, so what the walk can author is not the pair at step seven but what step seven has to do
  // to the person walking it. That is the step's ROLE, and it is what this block derives.
  //
  // NOTHING NEW IS MEASURED HERE. The hang is already ordered by kinship: `arcOrder` draws the near
  // neighbours in first and then widens its steps on purpose — «near neighbours drawn in, widening
  // steps hold contrast» (02-kinship-orderings.js) — so the DISTANCE the route crosses at each step
  // is a number the walk has already measured and already built its own shape out of. The gap of an
  // edge is `dist(vec(a), vec(b))` in the very coordinates the ordering stands on. Reading the
  // dramaturgy off that curve is reading the walk's own arc rather than laying a second one over it.
  //
  // THE GRAMMAR THE CURVE IS READ BY is charter shelf 15's, whose three functions the charter maps
  // onto tonic, subdominant and dominant: a home the eye settles in, a motion away that prepares, a
  // tension that demands resolution.
  //   · the route's WIDEST step is its one crest — the tension — so it is the culmination;
  //   · the step that leads into the crest PREPARES it, so it is a middle whatever its own gap;
  //   · a step whose gap stands above both its neighbours is a local widening — a motion away — so
  //     it is a middle too;
  //   · every other step is a quiet link, the home the eye settles in.
  // The dynamics curve of shelf 15 — about 70 parts quiet, 25 middle, 5 culmination — is therefore
  // an OUTCOME of that reading and not a quota applied to it: one crest per hang is the 5, and the
  // local widenings of a kinship arc are the 25. The realised proportion is measured by
  // `tests/test_pass_route.py` over the real hang rather than asserted here.
  //
  // TWO ROLES ARE NOT ON THE CURVE, because they are facts about the visit rather than about the
  // route's shape, and both outrank it:
  //   · a RETURN is an edge this visit has already walked. §4.8's whole claim is that the way back
  //     is kin to the way out, and the return reference crosses on exactly those edges, so the role
  //     and the reference name one and the same step.
  //   · an ENTRANCE is the visit's first crossing, wherever it falls. The visit window is read the
  //     way the memory of a visit reads it (`PASS_EDGE.visitWindowSeconds`), so a visitor who
  //     reloads mid-thought does not open a second entrance, and one who comes back tomorrow does.
  let passRouteAt = null;
  function passRouteShape() {
    let ids = null;
    // The hung route, read off the walk's own two names. A walk that has not hung yet, an instance
    // with no kinship vectors, or a hang of one work has no route to read a function off; the role
    // is then left unsaid and the composer's own default — a middle — stands, which is exactly what
    // stage 0 composed.
    try { ids = order.slice(0, shown); } catch (e) { return null; }
    if (!ids || ids.length < 2) return null;
    const stamp = ids.join(",");
    if (passRouteAt && passRouteAt.stamp === stamp) return passRouteAt;
    const gaps = [];
    for (let i = 0; i + 1 < ids.length; i++) {
      let g = NaN;
      try { g = dist(vec(ids[i]), vec(ids[i + 1])); } catch (e) { g = NaN; }
      if (!Number.isFinite(g)) return null;
      gaps.push(g);
    }
    // THE WALK'S OPENING IS NOT ITS CREST. Shelf 15 gives the route's first step to the entrance —
    // the motion away that opens the walk — so the search for the widest step begins after it. A
    // route whose widest gap happens to be its first would otherwise have its one tension eaten by
    // its own door and play no culmination at all, and this collection's hang does exactly that:
    // the walk orders by kinship and leans that order by light, and the leaned order put the widest
    // step first on the very route this stage cast. Seen on a cast route before it was reasoned
    // about. A one-step route has nothing to leave out and keeps its only step.
    let crest = gaps.length > 1 ? 1 : 0;
    for (let i = crest + 1; i < gaps.length; i++) if (gaps[i] > gaps[crest]) crest = i;
    const roles = gaps.map((g, i) => {
      if (i === crest) return "culmination";
      if (i === crest - 1) return "middle";
      const before = i > 0 ? gaps[i - 1] : -Infinity;
      const after = i + 1 < gaps.length ? gaps[i + 1] : -Infinity;
      return (g > before && g > after) ? "middle" : "quiet link";
    });
    passRouteAt = { stamp: stamp, ids: ids, gaps: gaps, roles: roles, crest: crest };
    return passRouteAt;
  }
  // Which step of the route this edge is, whichever way the visitor walks it. A step between two
  // works that do not stand next to each other in the hang is no step of the route — a restored
  // place or a pasted link lands that way — and it has no function on the curve.
  function passRouteEdgeAt(shape, fromId, toId) {
    if (!shape) return null;
    for (let i = 0; i + 1 < shape.ids.length; i++) {
      const a = String(shape.ids[i]), b = String(shape.ids[i + 1]);
      if ((a === fromId && b === toId) || (a === toId && b === fromId)) return i;
    }
    return null;
  }
  // Has this visit's thread opened? Two readings, and it takes either.
  //
  // The walk's own edge store, on the window the memory of a visit already defines, so there is one
  // idea of what «this visit» means and not two — and so a visitor who reloads mid-thought does not
  // open a second entrance.
  //
  // AND THIS PAGE'S OWN COUNT OF CROSSINGS ASKED FOR. The store is written only for a passage that
  // actually DREW, which is the right rule for the memory of an edge and the wrong one for the
  // walk's opening: a step whose picture never arrived is still a step the person took. The first
  // crossing of every visit is exactly the one that can find the host's file still on the wire, so
  // reading the store alone made the SECOND crossing an entrance too — and a route whose crest fell
  // on that second step then spent its one tension on a door, and played no culmination at all. It
  // was seen on a cast route before it was reasoned about. The opening is a fact about the person's
  // walk, so it is counted where the walk asks for a passage rather than where a picture lands.
  let passCrossings = 0;
  function passVisitOpened() {
    if (passCrossings > 0) return true;
    const rows = passEdgeAll(), now = passEdgeNow(), keys = Object.keys(rows);
    for (let i = 0; i < keys.length; i++) {
      const both = rows[keys[i]], ds = Object.keys(both);
      for (let j = 0; j < ds.length; j++) {
        if (now - +both[ds[j]].lastAt <= PASS_EDGE.visitWindowSeconds * 1000) return true;
      }
    }
    return false;
  }
  // The step's function, with the two visit facts outranking the curve. Answers null where the walk
  // can state none, and a null role is left OFF the request rather than sent as one: the composer
  // fences the field at its five names and answers an absent one with a middle.
  function passRouteRole(fromId, toId, edge) {
    if (edge && edge.passes > 0) return "return";
    if (!passVisitOpened()) return "entrance";
    const shape = passRouteShape();
    const at = passRouteEdgeAt(shape, String(fromId), String(toId));
    return at === null ? null : shape.roles[at];
  }

  // THE PASSAGE REQUEST the walk builds for one edge (§4.7, U27 stage 0). The edge is named in ONE
  // order whichever way the visitor walks it — the two ids sorted — and `direction` says which way
  // this passage runs, so A to B and B to A are two distinct passages of one edge and the site's own
  // edge record has a stable key to hang on (§4.8, stage 1 lane C).
  //
  // `routeRole` is the walk's own dramaturgy, derived just above and filled at this one place (U27
  // stage 2). `sessionMemory` is filled from the walk's own edge record: the return reference of
  // §4.8 and nothing wider, and nothing at all on an edge that has not played inside this visit's
  // window.
  function passRequestFor(fromEl, toEl) {
    const from = fromEl && fromEl.dataset ? fromEl.dataset.id : null;
    const to = toEl && toEl.dataset ? toEl.dataset.id : null;
    if (!from || !to) return null;
    const works = passWorkRecords() || {};
    const forward = String(from) <= String(to);
    const a = works[forward ? from : to], b = works[forward ? to : from];
    if (!a || !b) return null;
    const edge = passEdgeContext(fromEl, toEl);
    // THE DIE ON A REPEATED EDGE STARTS FROM THE RECORDED PASS'S OWN SEED, not a fresh one (fixed
    // 2026-08-19). §4.4f states the promise in plain words: "the same crossing met again in one
    // visit ... everything the record does not bound stays identical: the same family, the same
    // cues, the same instruments, the same stack" — only the FILL's own bounded slots (a separate
    // roll, on the edge's own key and pass count — see `passDriftScore`, called from
    // `passComposeFor` below) are meant to move pass to pass, never the family.
    //
    // Before today this function minted a fresh seed on every call, `passComposeFor`'s die included,
    // and handed the recorded family over only as a NAME for the composer's `genreFor` to go looking
    // for (`pass-composer.js`). That search is real, but for a genre whose ground is not fixed by the
    // road itself — `pivotOfPair`'s own die, mixed with THIS seed — the family it lands on moves with
    // the seed exactly as the ground does, so asking a fresh seed to reproduce yesterday's answer is
    // asking the same question a different way and hoping for the same reply. `dice: 8` (raised
    // 2026-08-19 for a different row, the mirror-distance one) does not fix this: eight fresh seeds
    // in a row can each land on some OTHER family that is still kin — none of them is the one asked
    // to hold, and `tests/test_pass_memory.py`'s drift row read exactly that eight times running the
    // same tree, family drifting off the recorded one on a roll that carried a clean reading (kin
    // through the pivot, never refused) precisely because kinship, not the family itself, was what
    // "clean" meant to the score in `passComposeFor`.
    //
    // The fix asks the composer to strike the SAME die it struck last time. `edge.memory.seed` is the
    // exact seed §4.8's own record already carries for this — `returnOf.seed`, one of the three
    // fields that were always allowed to cross (PASS-API-V1.md §4.8) — and `familyOf` in the composer
    // is a pure function of the road, the two works and the seed, so handing it back the same seed
    // reproduces the same family by construction, on the FIRST roll, with no search needed at all.
    // The shaping numbers still move: they are `passDriftScore`'s own roll, keyed on the edge and the
    // pass count and never on this seed, so the door still breathes exactly as before.
    const seed = (edge && edge.memory) ? edge.memory.seed
      : passSeedFor(String(forward ? from : to) + "__" + String(forward ? to : from));
    const req = {
      workRecordA: a,
      workRecordB: b,
      direction: forward ? "a-to-b" : "b-to-a",
      seed: seed,
      // The pose the camera rests in as the passage starts: the departing work's real box in the
      // hang at this instant, measured off the DOM by the walk's own `hangGeometry`.
      cameraState: hangGeometry(from),
      // The buffer as it stands on this device at this moment. The instrument reads the one it is
      // actually drawing on, which is the truth either way (his architecture decision of 18:00);
      // this is what the walk can see from outside it.
      buffer: { width: innerWidth, height: innerHeight, dpr: window.devicePixelRatio || 1,
                orientation: innerWidth >= innerHeight ? "landscape" : "portrait",
                quality: passGet("qualityTier") },
    };
    const role = passRouteRole(from, to, edge);
    if (role) req.routeRole = role;
    if (edge && edge.memory) req.sessionMemory = edge.memory;
    // WHAT THE WALK HAS ALREADY PLAYED, most recent letter first — charter shelf 16's letter
    // cooldowns, which the composer strikes INSIDE its dice (`coolOf` in pass-composer.js). The walk
    // is the one that knows: `passRoutePlayed` is written at the DOCK, when a passage has actually
    // landed in front of the person, so a passage this file only GUESSED at — the compose-ahead
    // below, which warms instruments and is never docked — never enters the list. A guess about what
    // might come next must not cool a letter nobody saw.
    //
    // A PREWARM REQUEST READS THE SAME LIST A REAL DECLARE WOULD, and that is deliberate rather than
    // an oversight: the prewarm's whole job is to ask what a real declare would ask, so it builds
    // its request here like every other caller. What it reads is the list AS IT STANDS WHEN THE
    // PREWARM RUNS. For the next edge that is the same list the declare will see, because the
    // compose-ahead is fired from the dock AFTER the just-played passage has been written in. For
    // the second and third edges of the look-ahead window it is not: the passages that will play
    // between now and then have not been docked yet, so their letters are missing from the list the
    // guess was struck on. THAT COSTS A WARM-UP AND NEVER AN OUTPUT — `passPrewarmEdge` below keeps
    // nothing but instrument NAMES, and `passComposeFor` re-builds its request and re-strikes its
    // dice at the real gesture — so a guess that misses leaves an unread file on the layer's own
    // registry and nothing else. It is one more reason the guess and the cast can differ, beside the
    // several the prewarm already had.
    //
    // The reading crosses as a plain list of NAMES and nothing else: the genre the passage ran on
    // and the instruments its stack carried, which is what a person actually sees repeat. Nothing in
    // it scales with the number of works or pairs (his 19:21 word), and nothing about the person
    // travels in it.
    req.walkMemory = passWalkMemory();
    return req;
  }

  // The letters of the passages behind this one, most recent first, flattened out of the walk's own
  // route record. One home for that reading, so the prewarm and a real declare read the list the
  // same way and can only ever differ by WHEN they read it.
  function passWalkMemory() {
    const out = [];
    for (let i = passRoutePlayed.length - 1; i >= 0; i--) {
      const step = passRoutePlayed[i];
      if (!step) continue;
      if (step.genre) out.push(step.genre);
      (step.stack || []).forEach((id) => { if (id) out.push(id); });
    }
    return out;
  }

  // PREWARM (2026-08-21, U27 audit): a head start for the layer's own instLoad race, never a cache a
  // real declare reads from. `passComposeFor` below still strikes its own dice, fresh, at the actual
  // gesture — this only asks the drawing layer for the file(s) a candidate passage on the NEXT one or
  // two edges would want, on the real records, the real route role and the real seed
  // (`passRequestFor` builds the exact request a real declare would), so the file is already on the
  // registry by the time a real gesture asks `offer` to wait on it. A wrong guess costs nothing more
  // than an unread file sitting in the layer's own cache (`prewarmInstruments`'s own dedup); nothing
  // here is stored per pair and nothing survives past the instrument name it asked for.
  //
  // THE ONE NUMBER THIS MECHANISM OWNS: how many steps ahead it looks. His brief's own words —
  // "the current/next 2-3 steps" — name a span, not a fixed count; the upper edge of that span is
  // what both the records ask and the compose-ahead loop below read, so a widened or narrowed span
  // moves in one place and the two never drift apart the way two separately-guessed numbers would.
  const PASS_PREWARM_STEPS = 3;
  const passPrewarmed = Object.create(null);
  function passPrewarmEdge(fromId, toId) {
    if (!passComposer || !passLayer || typeof passLayer.prewarmInstruments !== "function") return;
    const fromEl = passResolveEl({ id: fromId }), toEl = passResolveEl({ id: toId });
    if (!fromEl || !toEl) return;
    const request = passRequestFor(fromEl, toEl);
    if (!request) return;                       // one of the two carries no record yet — retried by
                                                 // the next trigger (a records wave settling, a dock)
    let got = null;
    try { got = passComposer.passageFor(request); } catch (e) { got = null; }
    if (!got || got.declined) return;
    const cues = (got.score && Array.isArray(got.score.cues)) ? got.score.cues : [];
    const names = [];
    cues.forEach((c) => {
      const id = c && c.instrument && c.instrument.id ? String(c.instrument.id) : null;
      if (id && !passPrewarmed[id]) { passPrewarmed[id] = true; names.push(id); }
    });
    if (names.length) passLayer.prewarmInstruments(names);
  }
  // Looks two edges ahead of wherever the visitor stands right now — the door's own pick before the
  // first step, the last-docked work after — reading them off `order`, the door's whole dealt hand,
  // already in memory from the moment the door was picked (no fetch of its own). Also widens the
  // records wave that far ahead, across an unfold boundary the visual walk has not reached yet: a
  // wave already in flight for an id costs nothing extra to ask again (`passRecordsAskFor`'s own
  // dedup). Self-healing rather than a single shot: called again whenever a records wave settles or
  // the composer arrives (either may have been what a request was missing) and at every dock (the
  // window slides forward with the visitor).
  //
  // CALLED FROM `dock` (the transaction's own landing) AMONG OTHER PLACES, so this function must
  // never throw: a guess about what comes next can never be allowed to break the bookkeeping of the
  // passage that is actually landing. Every road out is wrapped for exactly that reason — a failed
  // guess is silently nothing, never a broken dock.
  function passPrewarmAhead() {
    try {
      const ids = (typeof order !== "undefined" && Array.isArray(order)) ? order : null;
      if (!ids || ids.length < 2) return;
      const here = (typeof restingEl !== "undefined" && restingEl && restingEl.dataset)
        ? ids.indexOf(restingEl.dataset.id) : -1;
      const from = here >= 0 ? here : 0;
      // Records for exactly the ids the loop below can name — PASS_PREWARM_STEPS edges need
      // PASS_PREWARM_STEPS+1 endpoints — never a wider ask than the edges that follow can use.
      passRecordsAskFor(ids.slice(from, Math.min(from + PASS_PREWARM_STEPS + 1, ids.length)));
      for (let k = from; k < Math.min(from + PASS_PREWARM_STEPS, ids.length - 1); k++) {
        passPrewarmEdge(ids[k], ids[k + 1]);
      }
    } catch (e) {}
  }

  // The pair's own passage, derived. This road never waits and never fetches: a composer that has
  // not arrived answers nothing, the reason goes on the diagnostic surface, and the crossing falls
  // through to the walk's own glide exactly as a pair with no score always has. A named refusal from
  // the composer takes the same road, which is what a refusal has always meant here.
  function passComposeFor(fromEl, toEl) {
    if (!passComposer) {
      // ONCE PER STATE, never once per crossing. The refusal ring holds 64 rows and a row written
      // at every step pushes every real refusal off it inside ten steps — the defect U10 §5 read on
      // the register's own settings row. A composer that has not arrived is one fact about the
      // visit, so it is said once and said again only when that fact changes.
      if (passComposerSaid !== passComposerState) {
        passComposerSaid = passComposerState;
        passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC,
                                 why: "asked for a crossing before it arrived: "
                                      + passComposerState });
      }
      return null;
    }
    const request = passRequestFor(fromEl, toEl);
    if (!request) {
      passNote(passRefusals, { what: "composer", name: "request",
                               why: "one of the two works carries no record on this walk" });
      return null;
    }
    // THE WALK'S THREAD IS OPEN FROM HERE. Counted at the one road a real crossing comes down, and
    // not inside the role itself: the diagnostic surface hands `request` over so a row can ask what
    // the walk WOULD build for two elements, and a question is not a step the person took. It sits
    // below the two roads out, and that is deliberate (re-read 2026-08-19, when the records began
    // arriving with the selection and so could be in flight at the first step): the ENTRANCE is the
    // first crossing the visitor actually SEES, so a step that composed nothing must not spend it. A
    // visit whose first step outran its own records plays that step on the walk's own glide and
    // opens on the next one, which is the first crossing the person is actually shown.
    passCrossings += 1;
    const edge = passEdgeContext(fromEl, toEl) || { key: "", passes: 0, cooled: null, last: null,
                                                    within: false };
    // ONE CROSSING MAY BE OFFERED SEVERAL DICE, and never for the composer's own word. A composer's
    // refusal is a fact about the pair and no die moves it. What a die can move is the walk's own
    // two verdicts: a family still cooling on this edge, and the two refusals of §4.8. A cooldown
    // NEVER EMPTIES A POOL (the lab builder's own law): where the die does not move the family, the
    // cooled family plays and the surface says it did.
    let passage = null, refused = null, cooledStood = null, drifted = null;
    const rolls = [];
    // THE BEST DIE OF THE THREE IS KEPT, and one of them always plays. Each roll is read against
    // §4.8's two readings and against the family still cooling on this edge; a roll that reads clean
    // is taken at once, and where none does the FIRST roll stands — it is the one the walk's own die
    // asked for — with what was read about it recorded. Before 2026-08-18 a run of three refused
    // rolls ended in the walk's plain glide, which is the visitor paying for a reading about
    // repetition with the whole crossing.
    let best = null, bestScore = -1, bestWhy = null, bestDrift = null, bestCooled = null;
    const routeLast = passRoutePlayed.length ? passRoutePlayed[passRoutePlayed.length - 1] : null;
    for (let i = 0; i < PASS_EDGE.dice; i++) {
      if (i) request.seed = passSeedFor(edge.key, i);
      let got = null;
      try { got = passComposer.passageFor(request); } catch (e) { got = null; }
      if (!got) {
        passNote(passRefusals, { what: "composer", name: "passage", why: "the entry threw" });
        return null;
      }
      passage = got;
      if (got.declined) break;
      const fam = passFamilyOf(got.plan);
      const primary = passPrimaryOf(got);
      const worldAccent = primary === "parquet" || !!(got.score && got.score.camera
                                                       && got.score.camera.lead);
      // THE DOOR BREATHES BEFORE THE PASS IS READ, because the drifted pass is the one that would
      // play: reading the composer's own numbers and then playing others would leave §4.8's two
      // readings measuring a pass no one ever sees.
      drifted = edge.passes > 0 ? passDriftScore(got.score, edge.key, edge.passes) : null;
      const read = passEdgeJudge(got, edge.within ? edge.last : null);
      refused = read.why;
      cooledStood = (edge.cooled && fam === edge.cooled)
        ? "the family «" + fam + "» played last on this edge and is still cooling" : null;
      const repeatsFamily = !!routeLast && routeLast.family === fam;
      const repeatsPrimary = !!routeLast && routeLast.instrument === primary;
      rolls.push({ seed: request.seed, family: fam, instrument: primary,
                   repeatsPrevious: repeatsFamily || repeatsPrimary,
                   why: refused || cooledStood });
      // THE ROLL IS SCORED RATHER THAN JUDGED, on three readings and no thresholds: kinship, whether
      // the family is the one still cooling on this edge, and how far the pass stands from the
      // recorded one's mirror. The best-scoring roll plays, and one always does.
      const score = (read.kin ? 2 : 0) + (cooledStood ? 0 : 1)
                  + (read.distance === null ? 1 : Math.min(1, read.distance * 10))
                  // Route variety is a preference over lawful passages, never a quota and never a
                  // reason to lose a crossing.  An unseen family/ground and a clean handoff rank
                  // first when the pair affords them; if every die repeats, the best repeat plays.
                  + (repeatsFamily ? 0 : 3) + (repeatsPrimary ? 0 : 3)
                  + (passRouteFamilyCount[fam] ? 0 : 2)
                  + (passRouteInstrumentCount[primary] ? 0 : 2)
                  // A route should open at least one spatial sentence when the pair itself casts
                  // one: a measured parquet ground or a camera-led tonic.  This is a preference
                  // among passages the composer already justified, never an invented effect.
                  + (!passRouteWorldSeen && worldAccent ? 3 : 0);
      if (best === null || score > bestScore) {
        best = got; bestScore = score; bestWhy = refused; bestDrift = drifted;
        bestCooled = cooledStood;
      }
      // A roll that reads clean on all three is as good as a roll gets, so the walk stops asking.
      if (read.kin && !cooledStood && read.distance === null
          && !repeatsFamily && !repeatsPrimary) break;
      // A roll that read as a replay is said at once, and not only where the last one does too: a
      // pass that was passed over because it read that way is exactly what a person looking at the
      // surface is trying to find.
      passNote(passRefusals, { what: "memory", name: got.key,
                               why: "die " + (i + 1) + ": " + (refused || cooledStood) });
      // A second die that lands on the same family says the die does not reach this choice, so a
      // third would be the same waste again.
      if (i && rolls[i].family === rolls[i - 1].family) break;
    }
    if (best !== null) { passage = best; refused = bestWhy; drifted = bestDrift;
                         cooledStood = bestCooled; }
    // ONE RECORD CARRIES THE WHOLE PASSAGE: what was asked, what came back, and — written on later,
    // when the host reports — what the instrument applied on the buffer it drew on or the refusal it
    // named. `applied` is the runtime truth and it cannot be known before the frame is drawn.
    passage.memory = { crossed: request.sessionMemory || null, edgeKey: edge.key,
                       passes: edge.passes, cooled: edge.cooled || null,
                       cooledStood: cooledStood || null, rolls: rolls, refused: refused || null,
                       drift: drifted };
    passNote(passPassages, passage);
    if (passage.declined) {
      // THE ONE ROAD LEFT TO THE GLIDE FROM HERE, and it means one of the two works carries no
      // record at all — there is no PAIR, so there is nothing to compose between. Every other
      // decline the composer used to make is gone.
      passNote(passRefusals, { what: "passage", name: passage.key, why: passage.declined });
      return null;
    }
    // A PASS THAT READ AS A REPLAY STILL PLAYS, and the reading stands on the diagnostic surface in
    // plain words. It used to play nothing and the visitor took the walk's plain glide, which is a
    // reading about repetition charged to the person as a whole missing crossing.
    if (refused) passNote(passRefusals, { what: "memory", name: passage.key, why: refused });
    if (cooledStood) passNote(passRefusals, { what: "memory", name: passage.key, why: cooledStood });
    return passage.score;
  }

  // THE EDGE REMEMBERS WHAT PLAYED, written at the landing. Nothing is remembered for a passage that
  // never drew: a jump is not an authored crossing (§4.8 — an authored directed passage is invoked
  // by a real adjacent walk command and by nothing else), and a step whose picture the host declined
  // played the walk's own glide, so the edge is still unwalked as far as the memory is concerned.
  function passEdgeRemember(cmd) {
    if (!cmd || cmd.kind !== "step" || !cmd.score) return null;
    let row = null;
    for (let i = passPassages.length - 1; i >= 0; i--) {
      if (passPassages[i].score === cmd.score) { row = passPassages[i]; break; }
    }
    if (!row || row.declined || !row.plan || !row.memory) return null;
    if (!row.applied || !row.applied.instrument) return null;
    const parts = String(row.key).split("__");
    const edgeKey = row.memory.edgeKey || (parts[0] + "__" + parts[1]);
    const direction = (row.request && row.request.direction) || "a-to-b";
    const all = passEdgeAll();
    const edge = all[edgeKey] || (all[edgeKey] = {});
    const before = edge[direction] || null;
    const now = passEdgeNow();
    // The count runs on inside the visit window and starts again beyond it, so the drift a repeated
    // edge reads is this run of visits' own count and never a tally from a week ago.
    const within = !!before && (now - +before.lastAt) <= PASS_EDGE.visitWindowSeconds * 1000;
    edge[direction] = {
      edgeKey: edgeKey,
      direction: direction,
      family: passFamilyOf(row.plan),
      pivot: passPivotOf(row.plan),
      seed: row.request ? row.request.seed : null,
      passCount: within ? before.passCount + 1 : 1,
      lastAt: now,
      cooldown: { seconds: PASS_EDGE.cooldownSeconds,
                  familyCooledUntil: now + PASS_EDGE.cooldownSeconds * 1000 },
      // §4.8 names the plan before this one here. Beside it stand this pass's own plan id, so the
      // next pass has one to name, and the trace the reversal refusal is measured against — the
      // check's own evidence, which no other record holds and which is dropped with the record the
      // moment its cooldown runs out.
      provenance: { planId: row.plan.id || null,
                    previousScenePlanId: (before && before.provenance)
                      ? (before.provenance.planId || null) : null,
                    trace: passTraceOf(row.score) },
    };
    const family = passFamilyOf(row.plan);
    const instrument = row.applied.instrument || passPrimaryOf(row);
    passRoutePlayed.push({ edgeKey: edgeKey, direction: direction, family: family,
                           instrument: instrument, role: (row.request || {}).routeRole || null,
                           // The genre this passage ran on, beside the instruments it cast. A family
                           // token is not a letter — it names the pivot's transform and the measure
                           // that travelled — so the genre is what the composer's own cooldown can
                           // find in this list, and it is recorded here rather than re-derived.
                           genre: row.genre || null,
                           stack: (row.applied.cues || []).map((c) => c.instrument),
                           world: instrument === "parquet" || !!(row.score && row.score.camera
                                                                  && row.score.camera.lead) });
    passRouteFamilyCount[family] = (passRouteFamilyCount[family] || 0) + 1;
    passRouteInstrumentCount[instrument] = (passRouteInstrumentCount[instrument] || 0) + 1;
    if (instrument === "parquet" || (row.score && row.score.camera && row.score.camera.lead)) {
      passRouteWorldSeen = true;
    }
    passEdgePut();
    passMark("memory", cmd, edgeKey + " " + direction + " ×" + edge[direction].passCount);
    return edge[direction];
  }

  // WHAT THE INSTRUMENT APPLIED, written back onto the passage that asked for it. The host publishes
  // each live cue's own handles on its report, and an instrument that holds a door for itself
  // publishes what it moved and why there — the meshing one names `sizeRequest`, the size it drew,
  // how many rungs apart they stand, the leak it was holding against, and the refusal where no whole
  // size stood within reach. That reading is the runtime truth (his architecture decision of
  // 2026-08-17 18:00), and it belongs on the passage record beside the request that asked for it.
  // `key` is optional: without one the passage this walk derived last is the one that just played,
  // which is what the landing asks about.
  function passApply(key) {
    let row = null;
    for (let i = passPassages.length - 1; i >= 0; i--) {
      if (key === undefined || passPassages[i].key === key) { row = passPassages[i]; break; }
    }
    if (!row || row.declined) return null;
    let rep = null;
    try { rep = passLayer && passLayer.report ? passLayer.report() : null; } catch (e) {}
    if (!rep) return null;
    // THE GRID THE PASSAGE'S OWN FRAMES WERE DRAWN ON, which the host freezes with the run rather
    // than reading off the live canvas. The two part company whenever the buffer moves after the
    // landing — the resolution ladder steps, the window is resized — and a record naming the live
    // canvas beside readings taken on the run's own grid would say two different things at once.
    // The census is kept as the fallback for a host that predates the frozen pair.
    const drawn = rep.drawnOn || (rep.census ? { buffer: rep.census.buffer, dpr: rep.census.dpr }
                                             : null);
    row.applied = {
      instrument: rep.instrument,
      buffer: drawn ? drawn.buffer : null,
      dpr: drawn ? drawn.dpr : null,
      // `handles` is what the HOST resolved and asked each cue for. `applied` is what the INSTRUMENT
      // published about its own door on the buffer it drew on, through the frame state's
      // `reportApplied` — the request it was handed, the value it drew, how far apart the two stand,
      // the leak it was holding against, and the refusal where no whole value stood within reach.
      // The two travel side by side because the edge is read against both: the plan's intention and
      // the run-time truth.
      cues: (rep.stack || []).map((v) => ({ id: v.id, instrument: v.instrument,
                                            handles: v.handles || null,
                                            applied: v.applied || null })),
    };
    return row.applied;
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

  // ---- the visitor's hand, one normalised host signal -----------------------------------------
  // Instruments never attach input listeners.  The product observes the pointer passively while a
  // passage owns the screen and publishes one mutable, normalised record on the frozen command.
  // Reading without preventing/capturing is important: the walk's wheel/touch/key pagers remain the
  // sole owners of navigation, while a drawing voice may still answer a hover, tap or drag.
  const passInteraction = {
    active: false, gen: 0,
    pointer: { x: 0, y: 0, dx: 0, dy: 0, energy: 0, down: false,
               kind: "none", taps: 0, revision: 0 }
  };
  let passInteractionId = null;
  let passInteractionDownX = 0, passInteractionDownY = 0, passInteractionSpring = null;
  function passNormX(x) { return Math.max(-1, Math.min(1, ((+x || 0) / Math.max(1, innerWidth)) * 2 - 1)); }
  function passNormY(y) { return Math.max(-1, Math.min(1, ((+y || 0) / Math.max(1, innerHeight)) * 2 - 1)); }
  function passInteractionWrite(x, y, kind, down, impulse) {
    const p = passInteraction.pointer, nx = passNormX(x), ny = passNormY(y);
    const dx = nx - p.x, dy = ny - p.y;
    p.x = nx; p.y = ny; p.dx = dx; p.dy = dy; p.down = !!down;
    p.kind = kind || p.kind || "pointer";
    p.energy = Math.max(p.energy * 0.72,
      Math.min(1, Math.sqrt(dx * dx + dy * dy) * 3 + (+impulse || 0)));
    p.revision += 1;
  }
  function passInteractionRest() {
    if (passInteractionSpring !== null) cancelAnimationFrame(passInteractionSpring);
    const step = () => {
      passInteractionSpring = null;
      if (!passInteraction.active || passInteraction.pointer.down) return;
      const p = passInteraction.pointer;
      p.x *= 0.84; p.y *= 0.84; p.dx *= 0.7; p.dy *= 0.7; p.energy *= 0.82;
      if (Math.abs(p.x) < 0.002) p.x = 0;
      if (Math.abs(p.y) < 0.002) p.y = 0;
      if (p.energy < 0.002) p.energy = 0;
      p.revision += 1;
      if (p.x || p.y || p.energy) passInteractionSpring = requestAnimationFrame(step);
    };
    passInteractionSpring = requestAnimationFrame(step);
  }
  function passInteractionBegin(gen, seed) {
    if (passInteractionSpring !== null) cancelAnimationFrame(passInteractionSpring);
    passInteractionSpring = null; passInteraction.active = true; passInteraction.gen = gen;
    passInteractionId = null;
    const p = passInteraction.pointer;
    p.x = p.y = p.dx = p.dy = p.energy = 0; p.down = false;
    p.kind = (seed && seed.kind) || "none"; p.revision += 1;
    if (seed && Number.isFinite(+seed.x) && Number.isFinite(+seed.y)) {
      passInteractionWrite(seed.x, seed.y, seed.kind, false, seed.energy);
      passInteractionRest();
    }
    return passInteraction;
  }
  function passInteractionEnd(gen) {
    if (gen !== undefined && passInteraction.gen !== gen) return;
    passInteraction.active = false; passInteractionId = null;
    if (passInteractionSpring !== null) cancelAnimationFrame(passInteractionSpring);
    passInteractionSpring = null;
    const p = passInteraction.pointer;
    p.x = p.y = p.dx = p.dy = p.energy = 0; p.down = false; p.kind = "none";
    p.revision += 1;
  }
  addEventListener("pointerdown", (e) => {
    if (!passInteraction.active || passInteractionId !== null) return;
    passInteractionId = e.pointerId; passInteractionDownX = e.clientX;
    passInteractionDownY = e.clientY;
    passInteractionWrite(e.clientX, e.clientY, e.pointerType, true, 0.08);
  }, { capture: true, passive: true });
  addEventListener("pointermove", (e) => {
    if (!passInteraction.active || (passInteractionId !== null && e.pointerId !== passInteractionId)) return;
    const down = passInteractionId === e.pointerId;
    passInteractionWrite(e.clientX, e.clientY, e.pointerType, down, 0);
  }, { capture: true, passive: true });
  function passInteractionLift(e) {
    if (!passInteraction.active || passInteractionId !== e.pointerId) return;
    const p = passInteraction.pointer;
    const travel = Math.hypot(e.clientX - passInteractionDownX, e.clientY - passInteractionDownY);
    passInteractionWrite(e.clientX, e.clientY, e.pointerType, false, travel < 12 ? 0.55 : 0.14);
    if (travel < 12) p.taps += 1;
    passInteractionId = null; passInteractionRest();
  }
  addEventListener("pointerup", passInteractionLift, { capture: true, passive: true });
  addEventListener("pointercancel", passInteractionLift, { capture: true, passive: true });
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
    passInteractionEnd(cmd.gen);
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
    const raw = a.score || passComposeFor(a.fromEl, a.toEl);
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
    const interaction = passInteractionBegin(g, a.interaction || null);
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
      // Live by design: the command is frozen, the one host-owned signal inside it breathes while
      // this transaction owns the frame.  A renderer reads it; it never writes navigation.
      interaction: interaction,
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
    // A jump lands synchronously; it cannot race a renderer after this line.  Release the
    // same-frame input lock with the landing so an asynchronously prewarmed host becoming ready in
    // that frame cannot make the visitor's first real gesture look like a duplicate declaration.
    passFrameUnlock();
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
    passInteractionEnd(cmd.gen);
    // THE RUNTIME TRUTH, READ AT THE LANDING. The instrument has finished drawing and the host's
    // report still carries what the last transaction left behind, so this is the one instant the
    // applied state can be written back onto the passage that asked for it. It reads and decides
    // nothing: a passage that was refused or never derived leaves the row untouched.
    // THE EDGE RECORD FOLLOWS THE APPLIED READING, in that order: what the instrument applied is
    // what says a passage actually drew, and only a passage that drew is remembered on its edge.
    if (cmd.score) { passApply(); passEdgeRemember(cmd); }
    const el = passResolveEl(cmd.to);
    // THE WALK'S REST RECORD FOLLOWS THE DOCK (INV-86). `restingEl` — the section under the eye,
    // the one a turn re-docks to — is written by the in-view watcher's organic intersection alone
    // (08). A crossing moves the eye without one: the walk's own scroll stands still for the whole
    // flight, and a device change arriving mid-flight brings some other section across the
    // threshold inside the watcher's own 250 ms reflow guard, so the report that would have named
    // the arriving work is the one report the guard swallows. The record then keeps naming the
    // DEPARTING work and the next turn honours it — the visitor is thrown back one work. The
    // landing is where the arriving work is known for certain, so the landing corrects the record.
    // A door landing carries no section of its own (passResolveEl hands back a plain marker), and
    // that is what the dataset check keeps out.
    if (el && el.dataset && document.body.contains(el)) restingEl = el;
    if (el) passLandGate(el, "dock", landOn, cmd.gen);
    passMark("dock", cmd, cmd.to.id === "door" ? "door" : null);
    passPrewarmAhead();   // the window of "the next couple of steps" slides forward with the visitor
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
    // THE WALK LANDED. The composer is asked for HERE and nowhere else (§4.4d: warming happens at
    // the landing and nothing ever waits on the wire), because a crossing is declared the instant
    // the visitor moves and the passage is derived inside that same call — a fetch begun there could
    // never arrive in time. It is asked for once per visit; every landing after the first returns at
    // the first line. Nothing per work is fetched: one file decides every crossing of the walk.
    passComposerOpen();
    // THE HOST'S OWN FILE IS NOT ASKED FOR HERE, AND THE REASON IS WRITTEN DOWN RATHER THAN LEFT
    // TO BE REDISCOVERED (U27 stage 2). It is asked for at the first DECLARE instead — one line in
    // 15-motion.js — and a fetch begun at a declare cannot arrive in time for the crossing that
    // declare belongs to, so the visitor's FIRST crossing of every visit falls to the walk's own
    // glide whatever the pair. Measured on the cast route: 1 step of 19. Moving the ask to this
    // door repairs it and was tried here; it also moves the instant the host exists, and two rows of
    // `tests/test_pass_api.py` sequence a reload against the old instant and go red on it. The
    // repair is therefore named for its own pass, with those two rows re-sequenced beside it,
    // rather than half-landed in the middle of an assembly.
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
      // The passage composer, on the same surface: where its file stands, how many work records the
      // settings record carries for it to read, and one row per passage this visit has derived —
      // the key, the request that was made, the shape that came back or the refusal that was named,
      // and what the instrument applied on the buffer it drew on. A picture that looks wrong reads
      // back to the request that made it without reading anything else.
      composer: { src: PASS_COMPOSER_SRC, state: passComposerState,
                  version: passComposer ? passComposer.version : null,
                  works: Object.keys(passWorkRecords() || {}).length,
                  passages: passPassages.map((row) => ({
                    key: row.key, request: row.request, shape: row.shape || null,
                    bytes: row.bytes === undefined ? null : row.bytes,
                    overTheFence: row.overTheFence === undefined ? null : row.overTheFence,
                    declined: row.declined || null, applied: row.applied || null,
                    // The family and the pivot this passage stands on, read off its own plan: the
                    // two facts the edge record hangs on and the two the return is judged by, so a
                    // crossing that looks unrelated to the one before it reads back to them.
                    family: passFamilyOf(row.plan), pivot: passPivotOf(row.plan),
                    memory: row.memory || null })) },
      // The walk's own memory of this visit (§4.8, charter shelf 16): where the records live, what
      // the browser's storage said when they were read, the numbers the drift and the cooldowns
      // run on, and one row per remembered edge. A visitor whose storage is closed or cleared reads
      // «unavailable» or «fresh» here and walks with a pool that remembers nothing.
      memory: { src: PASS_EDGE_SRC, storage: passEdgeStorage, numbers: PASS_EDGE,
                edges: (function () {
                  const rows = passEdgeRows || {}, out = [];
                  Object.keys(rows).forEach((k) => {
                    Object.keys(rows[k]).forEach((d) => {
                      const r = rows[k][d];
                      out.push({ edgeKey: r.edgeKey, direction: r.direction, family: r.family,
                                 pivot: r.pivot, seed: r.seed, passCount: r.passCount,
                                 lastAt: r.lastAt, cooldown: r.cooldown,
                                 previousScenePlanId: (r.provenance || {}).previousScenePlanId
                                   || null,
                                 traceCues: ((r.provenance || {}).trace || { cues: [] })
                                   .cues.length });
                    });
                  });
                  return out;
                }()) },
      // THE ROUTE'S OWN DRAMATURGY (charter shelf 15, U27 stage 2): the works the hang stands at,
      // the kinship gap the walk crosses at each step, the function that gap gives the step, which
      // step is the crest, and how the five functions divide the route. A step that looks wrong
      // reads back to the gap that named it without reading anything else.
      route: (function () {
        const shape = passRouteShape();
        if (!shape) return { steps: 0, works: 0, roles: null, share: null, crest: null };
        const share = {};
        shape.roles.forEach((r) => { share[r] = (share[r] || 0) + 1; });
        return { steps: shape.roles.length, works: shape.ids.length, ids: shape.ids.slice(),
                 gaps: shape.gaps.map((g) => Math.round(g * 10000) / 10000),
                 roles: shape.roles.slice(), crest: shape.crest, share: share,
                 opened: passVisitOpened(), played: passRoutePlayed.slice() };
      }()),
      // The family roll, on the same surface (§4.4f): the visit's own seed and whether it was
      // pinned, and one row per rolled crossing carrying the pair, the pass index, the seed that
      // pass ran on, the spans it read and the value it applied to each bounded slot. A picture
      // that looks wrong reads back to the number that made it without reading anything else.
      family: { visit: passVisit || null, pinned: passVisitPinned, rolls: passFamilies.slice() },
      // THE WAVE'S OWN READINESS (2026-08-19). The records arrive with the selection now, so
      // «has this walk got what a crossing needs» is a question about a request in flight rather
      // than about a block that was always there. Three numbers answer it: how many ids this visit
      // has asked the route for, how many records it actually holds, and how many waves it has
      // sent. A crossing declared before the first wave lands takes the walk's own glide, so a row
      // that means to read a composed crossing waits on `held` the way it already waits on the
      // composer's own `state`.
      records: { asked: Object.keys(passRecordsAsked).length,
                 held: Object.keys(passRecordsMap).length,
                 waves: passRecordsWaves,
                 // NO WAVE IN FLIGHT is the only readiness that means anything to a reader, and
                 // «how many records are held» is not it: a wave may hold every id it asked for and
                 // another may still be on the wire, and a row that read the first number would
                 // read a walk mid-answer as a walk that has answered. Sent minus settled, where
                 // settled counts a wave that failed as much as one that landed — a wave that is
                 // never coming back is not in flight either.
                 inflight: passRecordsWaves - passRecordsSettled },
    };
  }
  // `score` is the checker itself, handed over so a score can be judged without being played — the
  // surface stays read-only about the walk and decides nothing on its own. `adapter` and `layer` are
  // a TESTING seam, gated the same way: they let a conformance row construct a real command and drive
  // the host directly, on real elements, without needing to simulate every input road by hand.
  if (passGet("diagnostics") === "on") {
    try {
      window.__@@NS@@Pass = {
        report: passReport, score: passScoreCheck, version: 1,
        // `passage` is the ONE entry a passage comes through, handed over so a conformance row can
        // put a request to it directly and read the score or the named refusal that comes back,
        // without driving a whole walk to reach it. `request` builds the request the walk itself
        // would build for two real elements, so a row can prove the two agree.
        passage: function (req) { return passComposer ? passComposer.passageFor(req) : null; },
        request: passRequestFor, applied: passApply, seed: passSeedFor,
        // The route's own dramaturgy, handed over the same way and for the same reason: a row that
        // judges the walk's roles needs the curve they were read off, and the report is a reading
        // rather than the thing itself. `role` answers for one edge exactly as the request does.
        route: { shape: passRouteShape, at: passRouteEdgeAt, role: passRouteRole,
                 opened: passVisitOpened },
        // The passages this visit derived, whole — the plan and the score the report's own rows
        // only summarise. A conformance row that judges a passage needs the very object the walk
        // judged, and the report is a reading rather than the thing itself.
        passages: function () { return passPassages; },
        // The walk's own memory, handed over the same way and for the same reason: a conformance
        // row reads the edge this step walks, the reference that would cross, and the verdict the
        // two refusals of §4.8 reach on a passage — without driving a whole visit to reach them.
        // `remember` is the landing's own call, so a row can play an edge and read the record back.
        memory: { edge: passEdgeContext, all: passEdgeAll, remember: passEdgeRemember,
                  judge: passEdgeJudge, trace: passTraceOf,
                  mirrorDistance: passMirrorDistance,
                  family: passFamilyOf, pivot: passPivotOf, numbers: PASS_EDGE },
        adapter: { declare: declare, dock: dock, glide: glide, interrupt: interrupt,
                   reframe: reframe, curtain: curtain, mark: passMark,
                   hangGeometry: hangGeometry, handoff: handoff, chromeReveal: chromeReveal },
        layer: function () { return passLayer; },
      };
    } catch (e) {}
  }
