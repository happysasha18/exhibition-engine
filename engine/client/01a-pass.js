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
  // A limit is part of the CAPABILITY, so raising one is a rebuild, never a setting. Four of the
  // seven are capabilities and always were: `camera` and `curve` fence how much a track may carry,
  // `instruments` how many a transition may name, and `text` is the fence on a NAME — a setting
  // name, a cause, an instrument name, a row on the refusal ring — where it keeps its full force.
  //
  // `bytes` AND `intent` NO LONGER DECIDE ANYTHING IN THIS CLIENT (2026-08-25). Both were set from
  // tallies over a collection of photographs: a median and a longest weight read across a shipped
  // pack of scores, and a count of composed crossings whose authored line ran past the cap before
  // it. Charter shelf 20 does not let a tally over the collection calibrate behaviour, and neither
  // number says anything about the next collection this engine is pointed at. Both readings they
  // used to drive are re-founded in `passScoreCheck` below. The weight is read against a ceiling
  // CONSTRUCTED from this client's own capability — see `passScoreCeiling`: at most `instruments`
  // cues, each driving at most as many handles as the widest manifest the client actually holds,
  // each track at most `curve` points, each point as wide as the writer itself says a point is. The
  // authored line is read for STRUCTURE rather than for length, which is the question its own fence
  // was always for — «an intent is a sentence, not a place to put a payload» — and a length never
  // answered it. Neither of the two numbers is read anywhere in this file any more.
  //
  // THEY STAY ON THIS LINE FOR ONE REASON, AND IT IS NOT THIS CLIENT'S. `engine/build.py` reads
  // these two literals straight out of it and publishes them into the settings record as
  // `pass.capabilities.scoreBytes` and `pass.capabilities.intentChars`, and the composer fits its
  // scores and its prose to them. Retiring them is a change to the WIRE rather than to this file: it
  // needs `engine/build.py`, the composer's own read of `intentChars`, and the bake rows that check
  // the published pair against these very literals. Until that is done they are two numbers held in
  // step and nothing else, and they are the last tally-derived numbers left on this road.
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

  // HOW WIDE A WRITTEN POINT CAN BE, asked of the writer rather than guessed. A track's curve is a
  // list of points and a point is a pair of numbers with the punctuation JSON puts around them; the
  // widest a number ever writes is a double at full precision with a three-digit exponent. This
  // stands once, at evaluation, and it is a fact about the FORMAT — nothing about any collection of
  // pictures and nothing measured over one.
  const PASS_POINT_CHARS = JSON.stringify({ t: -1.2345678901234567e-308,
                                            v: -1.2345678901234567e-308 }).length;
  // THE WEIGHT THIS CLIENT COULD EVER NEED TO READ, CONSTRUCTED FROM ITS OWN CAPABILITY (2026-08-25).
  //
  // It stood at a number taken from a tally over the collection — a median and a longest measured
  // across a shipped pack of scores — which charter shelf 20 does not allow to calibrate behaviour,
  // and which says nothing about the next collection this engine is pointed at anyway. The bound is
  // derived here instead, from three facts that are all capabilities of THIS client:
  //   · a score names at most `PASS_LIMITS.instruments` cues — the register's own fence on how many
  //     instruments a transition may name;
  //   · a cue drives at most as many handles as the widest instrument the client actually holds a
  //     manifest for, read off those manifests at the moment the question is asked;
  //   · a handle's track carries at most `PASS_LIMITS.curve` points, and a point is at most
  //     `PASS_POINT_CHARS` wide.
  // Their product bounds the cue body, which is the whole of a score's weight but for the envelope,
  // and every envelope field but one is bounded by its own register entry. THE ONE UNBOUNDED FIELD
  // IS `intent`, now that its length fence is gone (below) — so this reading is not vacuous: it is
  // exactly the reading that catches an authored line running away, which is the one way a score can
  // grow past what this client could ever have needed. A client that holds no manifest yet can
  // construct nothing and states no reading, which is the honest answer rather than a guess.
  function passScoreCeiling() {
    const m = (passComposerConsts() || {}).manifests || {};
    let widest = 0;
    Object.keys(m).forEach((id) => {
      const h = m[id] && m[id].handles;
      const n = h ? Object.keys(h).length : 0;
      if (n > widest) widest = n;
    });
    if (!widest) return null;
    return PASS_LIMITS.instruments * widest * PASS_LIMITS.curve * PASS_POINT_CHARS;
  }
  // WHETHER AN AUTHORED LINE IS PROSE OR A PAYLOAD, and the question is structural rather than long.
  // §4.4's own sentence about the score is «The score names no expression, no function and no
  // executable string», and the `intent` fence's own comment said the same thing in its own words:
  // an intent is a sentence, not a place to put a payload. A length never answered that question —
  // it only cut honest sentences that ran long — so what is asked now is whether the line carries
  // structure prose does not: the braces and brackets a record is written with, the angle brackets
  // and backslashes and backticks of markup and code, and the two tokens that name a function. A
  // sentence in any of the tongues this walk speaks carries none of them, and a payload cannot avoid
  // them. Nothing here has a number in it.
  const PASS_PROSE_STRUCTURE = /[{}[\]<>\\`]|=>|function\s*\(/;
  // The score: a versioned record with an allow-list of fields. AN UNKNOWN FIELD IS STRIPPED AND
  // NOTED, NOT A REFUSAL OF THE WHOLE SCORE (2026-08-24) — the same conversion the weight fence and
  // the intent-length fence already took on 2026-08-18: a score is composed by the collection's own
  // composer, and a field the client's own allow-list has not yet learned about used to cost the
  // visitor the whole crossing over one name it did not recognise. The field is cut, the cut is
  // recorded on `noted`, and the passage plays.
  //
  // THE STRIP COPIES AND NEVER EDITS WHAT IT WAS HANDED (2026-08-25). It used to `delete` off the
  // caller's own object and write back into it, so a checker meant to READ a score was quietly
  // editing the composer's output in place, and whatever else held a reference to it saw a different
  // record afterwards. What comes back is a new envelope carrying the fields that are named; the
  // record handed in is untouched, and a cue is copied only where something had to come off it.
  //
  // AND THE STRIP NOW DESCENDS INTO THE CUES (2026-08-25). Until today it read `Object.keys(raw)` and
  // nothing else, so the fence stood on the envelope alone and a cue could carry anything at all.
  // The contract names thirteen fields a cue may hold and calls four of them plan-only — `cast`,
  // `levelOwnership`, `measuredHandles`, `returnOf` — and those four were reaching the host inside
  // cue records because nothing on this road ever looked. Two comments elsewhere in the engine argue
  // that the levels law may leave the host BECAUSE a closed cue allow-list refuses what it does not
  // name; that allow-list is this one, and until today it did not exist here. The composer's own
  // `serialise` holds a deny-list of the same four names, but it judges the composer's freshly built
  // output and can only ever catch it contradicting itself — a score arriving by any other road, a
  // hand-written one on the settings ladder among them, passed unread.
  const PASS_CUE_FIELDS = ["cameraAuthority", "doors", "id", "instrument", "levels", "nodes",
                           "resources", "roles", "stack", "tracks", "voice", "window", "works"];
  function passScoreCheck(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return { ok: false, why: "no record" };
    let bytes = 0;
    try { bytes = JSON.stringify(raw).length; } catch (e) { return { ok: false, why: "does not write out" }; }
    const v = raw.schema;
    if (v !== 1 && v !== 2) return { ok: false, why: "names no schema 1 or 2" };
    // THE WEIGHT IS A READING AND NO LONGER A WALL (2026-08-18, his word of 09:51). A score over the
    // fence was refused WHOLE and the visitor took the walk's plain glide, every one of them before
    // an instrument saw it. A crossing is not worse for weighing more; a heavy score costs a little
    // parse time and nothing else, so it is a reading the diagnostic surface carries and the passage
    // plays. What it is read against is now constructed rather than tallied — see `passScoreCeiling`.
    const ceiling = passScoreCeiling();
    const overWeight = (ceiling !== null && bytes > ceiling)
      ? "weighs " + bytes + " bytes, over the " + ceiling + " this client could ever need to read"
      : null;
    // THE ENVELOPE, COPIED FIELD BY NAMED FIELD. Everything the allow-list holds is carried over by
    // reference; everything else is left behind and said.
    const allowed = v === 2 ? PASS_SCORE_FIELDS2 : PASS_SCORE_FIELDS;
    const score = {}, stray = [];
    Object.keys(raw).forEach((k) => {
      if (allowed.indexOf(k) < 0) stray.push(k); else score[k] = raw[k];
    });
    let overField = null;
    if (stray.length) {
      overField = "the unknown field" + (stray.length > 1 ? "s" : "") + " «" + stray.join("», «")
                + "» " + (stray.length > 1 ? "were" : "was") + " stripped";
    }
    // THE CUES, THE SAME WAY AND ONE LEVEL DOWN. A cue that carries only what it may is carried over
    // untouched; one carrying anything else is COPIED without it, so the score handed in still holds
    // whatever it held. The names cut are said once for the whole score rather than once per cue: a
    // plan-only field leaks across every cue of a passage at once, and sixty rows saying the same
    // name would push every other reading off the refusal ring.
    let overCue = null;
    if (v === 2 && Array.isArray(score.cues)) {
      const cut = [];
      const cues = score.cues.map((c) => {
        if (!c || typeof c !== "object" || Array.isArray(c)) return c;
        const names = Object.keys(c).filter((k) => PASS_CUE_FIELDS.indexOf(k) < 0);
        if (!names.length) return c;
        names.forEach((k) => { if (cut.indexOf(k) < 0) cut.push(k); });
        const out = {};
        Object.keys(c).forEach((k) => { if (PASS_CUE_FIELDS.indexOf(k) >= 0) out[k] = c[k]; });
        return out;
      });
      if (cut.length) {
        score.cues = cues;
        overCue = "the cue" + (cut.length > 1 ? "s carried the unknown fields «" : " carried the "
                  + "unknown field «") + cut.join("», «") + "», stripped";
      }
    }
    // THE AUTHORED LINE IS NO LONGER CUT TO A LENGTH. It used to be sliced to a number taken from a
    // tally over one collection, which destroyed prose the composer wrote to fit a fence that
    // answered the wrong question — and the trimmed line's only reader on this road is a NAME on the
    // refusal ring, which shortens its own row (see `declare` below, where `PASS_LIMITS.text` fences
    // a name exactly as it fences a cause). What is asked here is the question the fence was always
    // for: is this a sentence, or a payload. A line that reads as a payload is not carried, and a
    // line that is no text at all is not carried either; a long sentence is a long sentence and
    // travels whole.
    let overLine = null;
    if (score.intent !== undefined) {
      if (typeof score.intent !== "string") {
        overLine = "the authored line is no text, so the crossing carries none";
        delete score.intent;
      } else if (PASS_PROSE_STRUCTURE.test(score.intent)) {
        overLine = "the authored line carries structure a sentence does not, so it reads as a "
                 + "payload and the crossing carries none";
        delete score.intent;
      }
    }
    if (score.seed !== undefined && !Number.isFinite(Number(score.seed))) return { ok: false, why: "seed is no number" };
    const p = score.params;
    if (p !== undefined) {
      if (!p || typeof p !== "object" || Array.isArray(p)) return { ok: false, why: "params is no record" };
      const bad = Object.keys(p).filter((k) => !PASS_REG[k]);
      if (bad.length) return { ok: false, why: "params names «" + bad[0] + "», in no register" };
      const shut = Object.keys(p).filter((k) => (PASS_REG[k].order || PASS_ORDER).indexOf("score") < 0);
      if (shut.length) return { ok: false, why: "«" + shut[0] + "» is closed to a score" };
    }
    // WHAT WAS READ ABOUT THE SCORE travels with it rather than deciding anything.
    const noted = [overWeight, overLine, overField, overCue].filter(Boolean);
    return { ok: true, score: score, read: v, noted: noted.length ? noted : null };
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
    passViewerSeen = [];
    passViewerLingered = [];
    passViewerSkipped = [];
    passViewerStanding = null;
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
  // Which ids this visit has ever asked the route for AND HEARD BACK ABOUT, whether the wave landed
  // or failed to reach the wire at all. A wave that fails the wire is retried with backoff instead
  // of poisoning its ids for the visit (2026-08-24): its ids come OFF this map in the same beat that
  // the retry is scheduled, so a later selection naming the same work asks again rather than finding
  // it permanently unheld. `passRecordsRetryCount` tracks how many times each id has been retried, so
  // the backoff grows and eventually stops rather than hammering a route that is genuinely down.
  let passRecordsAsked = Object.create(null);
  let passRecordsRetryCount = Object.create(null);
  // UNJUSTIFIED — how many times a work record is asked for again, and how long the first wait is.
  // Both were chosen here and nothing measured either.
  const RECORDS_RETRY_MAX = 3, RECORDS_RETRY_BASE_MS = 1500;
  // WHICH IDS ARE STILL ON THE WIRE AT THIS INSTANT (2026-08-25). `passRecordsAsked` cannot answer
  // that: it says an id has been asked for AND heard back about, so it reads the same for «the answer
  // has not come yet» and «the answer came and carried nothing for this id» — opposite facts for a
  // step deciding whether there is anything to wait for. An id goes on this map the beat its wave is
  // sent and comes off it the beat that wave settles, with a record if the route carried one and
  // without if the route omitted it (§3's own contract: an omitted id is a definite nothing). A wave
  // that FAILS keeps its ids here only while a retry is still owed them; the id whose retries are
  // spent comes off, because nothing is coming for it any more. So this map IS the life of the
  // request, and it is the only bound the wait below has — no hold of its own, no number.
  let passRecordsInFlight = Object.create(null);
  // Whoever is holding a step until the ids it needs stop being in flight (`passRecordsAwait`),
  // exactly the way `passLayerWaiters` holds one until the layer's own file lands. Drained on every
  // settle, landed and spent alike; a waiter whose own ids are still coming puts itself straight back
  // on and the next settle drains it again.
  let passRecordsWaiters = [];
  // How many steps this visit has held on a wave, counted on the way in, so the diagnostic surface
  // can tell a walk that never had to wait from one that waited and then composed.
  let passRecordsHolds = 0;
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
  // «IS A RECORD FOR ANY OF THESE STILL COMING?» — the one question a step that means to wait asks.
  // An id already held is not coming (it is here); an id nobody has asked for is not coming either
  // (a still visit, a wire naming no route: `passRecordsAskFor` returned before sending anything, so
  // nothing was ever marked in flight and every road below answers false at once).
  function passRecordsComing(ids) {
    for (let i = 0; i < ids.length; i++) {
      const s = String(ids[i]);
      if (!passRecordsMap[s] && passRecordsInFlight[s]) return true;
    }
    return false;
  }
  // Drained where a wave settles. Each waiter re-reads its OWN ids rather than being told which wave
  // landed, so a waiter needing two ids that went out on two different waves is released by whichever
  // one finishes last and by nothing earlier.
  function passRecordsSettleWaiters() {
    const q = passRecordsWaiters; passRecordsWaiters = [];
    q.forEach((fn) => { try { fn(); } catch (e) {} });
  }
  // Calls `done` the moment none of `ids` is on the wire any longer — because the record arrived,
  // because the route answered without it, or because its retries are spent. TERMINATES BY
  // CONSTRUCTION: every settle either takes an id off `passRecordsInFlight` or spends one of the
  // RECORDS_RETRY_MAX tries that id has, and a waiter is only ever re-armed while at least one of its
  // ids is still on that map. A wait that is still standing is therefore a request still alive.
  function passRecordsAwait(ids, done) {
    const tick = () => {
      if (passRecordsComing(ids)) { passRecordsWaiters.push(tick); return; }
      done();
    };
    tick();
  }
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
                                    + "cap of " + cap + " and go out in a second wave: " + left.join(",") });
      // A SECOND WAVE ASKS FOR WHAT THE FIRST COULD NOT CARRY, rather than dropping it on the floor
      // (2026-08-24): the cap is the route's own per-REQUEST ceiling, not a statement that these ids
      // are unwanted. They stand unmarked in `passRecordsAsked` until their own wave goes out, so
      // this call finds them exactly as it found the ones just capped — and chains again itself if
      // even `left` stands over the cap.
      passRecordsAskFor(left);
    }
    // MARKED ASKED BEFORE THE REQUEST LANDS, not after: a second wave that starts while this one is
    // still in flight must not ask the route for the same id twice, and marking on send rather than
    // on receipt is what makes that true regardless of how long the route takes to answer.
    asked.forEach((id) => { passRecordsAsked[id] = true; passRecordsInFlight[id] = true; });
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
          // OFF THE WIRE EITHER WAY. An id the answer carried is held from here; an id the answer
          // omitted is §3's own definite nothing, and neither is «still coming». A step waiting on
          // either is released by this line rather than by a clock.
          delete passRecordsInFlight[id];
        });
        passPrewarmAhead();   // this wave may be exactly what an earlier prewarm attempt was missing
      })
      .catch((e) => {
        // THE MAP OF RECORDS STANDS AS IT WAS — a wave that fails leaves nothing it has already been
        // given changed. Its ids are RETRIED WITH BACKOFF instead of poisoned for the visit
        // (2026-08-24): a network hiccup or a refusing status is a fact about that one attempt, not
        // a fact about whether the route will ever answer for these ids, so each id comes off
        // `passRecordsAsked` and goes back on the wire once its own backoff has passed — up to
        // RECORDS_RETRY_MAX tries, past which it is treated as genuinely unreachable this visit.
        const why = "the wave for " + asked.length + " id(s) did not land: "
                  + (e && e.message ? e.message : String(e));
        passNote(passRefusals, { what: "records", name: "wave", why: why });
        let delay = RECORDS_RETRY_BASE_MS;
        const retryIds = [];
        asked.forEach((id) => {
          delete passRecordsAsked[id];
          const n = (passRecordsRetryCount[id] || 0) + 1;
          passRecordsRetryCount[id] = n;
          if (n <= RECORDS_RETRY_MAX) {
            retryIds.push(id);
            delay = Math.max(delay, RECORDS_RETRY_BASE_MS * Math.pow(2, n - 1));
          } else {
            // ITS RETRIES ARE SPENT, so nothing is coming for this id any more and it comes off the
            // wire's own map. A step held on it is released here — onto the walk's plain glide, which
            // is what a pair with no record has always meant — rather than held on a request that has
            // stopped existing. This `else` is the far end of the wait's bound.
            delete passRecordsInFlight[id];
          }
        });
        if (retryIds.length) setTimeout(() => { passRecordsAskFor(retryIds); }, delay);
      })
      // SETTLED EITHER WAY. The wave is off the wire whether it landed or failed, and the readiness
      // the diagnostic surface publishes is about the wire rather than about the outcome. Whoever is
      // HOLDING A STEP on one of these ids is woken here, for the same reason and in the same beat:
      // the wave's own settling is the event, and a waiter still owed an id simply re-arms.
      .then(() => { passRecordsSettled += 1; passRecordsSettleWaiters(); },
            () => { passRecordsSettled += 1; passRecordsSettleWaiters(); });
  }
  function passComposerConsts() { return (((EX && EX.pass) || (cfg && cfg.pass) || {})).composer; }
  // THE P2/P3 SKEW'S STRUCTURAL FIX, PREPARED HERE AND NAMED AS A FOLLOW-UP (2026-08-24). The site's
  // record and the composer's own idea of what it may cast can drift apart — "the site's record
  // names no instrument by that name" — because each is baked separately. The real fix is for the
  // composer to read its castable set from the very record the host already holds (`passLayer.
  // castable()`) instead of a second baked copy of its own; this wires that hand-off, feature-
  // detected against a `setCastable` the composer does not carry yet, so it is a no-op today and
  // starts working the moment the composer's own file adds it. Until then the skew still sheds to
  // the funnel: an instrument named by the composer that this host cannot load is an unknown
  // instrument to `voicesFor`, which sheds that voice (or the funnel casts the last resort) rather
  // than declining the crossing outright.
  function passWireCastable() {
    if (!passComposer || !passLayer) return;
    if (typeof passComposer.setCastable !== "function") return;
    if (typeof passLayer.castable !== "function") return;
    try { passComposer.setCastable(passLayer.castable()); } catch (e) {}
  }
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
      passWireCastable();
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
    // UNJUSTIFIED — how long a visit's own window stands open. Half an hour was chosen here and no
    // reading of any visitor's own walk stands behind it.
    visitWindowSeconds: 1800,
    // UNJUSTIFIED — how long a family stays cooled once a visit has spent it. A day was chosen here
    // and nothing measured it.
    cooldownSeconds: 86400,
    // UNJUSTIFIED — how far a repeated pass may drift inside its own family. A quarter was chosen
    // here and nothing measured it.
    driftSpan: 0.25,
    // UNJUSTIFIED — the pass count past which the drift opens at all. Three was chosen here and
    // nothing measured it.
    driftOpensOver: 3,
    // UNJUSTIFIED — how many tries the return's own die is given. The sentence above says plainly
    // that eight is not a measured floor: it was raised until a miss this seat kept seeing stopped
    // being seen, over runs of one fixed two-work fixture, which is a reading of that fixture and
    // not of the collection.
    dice: 8,
    // UNJUSTIFIED — how many edge records the browser's own store keeps. Sixty-four was chosen here
    // and nothing measured it.
    keep: 64,
    // UNJUSTIFIED — how many handles of a pass the trace carries. Forty-eight was chosen here and
    // nothing measured it.
    traceHandles: 48,
  };
  let passEdgeRows = null, passEdgeStorage = "unread";
  // WHAT EACH REMEMBERED PASS WAS ASKED ON, keyed by the edge and the direction that played it. The
  // walk's own note to itself, written at the landing (`passEdgeRemember`) and read by the held
  // pre-check on a return (`passComposeFor`); it holds the `walkMemory` list the recorded pass was
  // struck with, because the composer's instrument cast weighs its pool through that list and the
  // seed alone therefore reproduces the family and not the instrument.
  //
  // NOT PART OF THE STORE, deliberately. §4.8 names what an edge remembers and what crosses back to
  // the composer, and this is neither: it never leaves the page, never reaches storage, and answers
  // no question outside the visit window. It is bounded by the same thing the route is — a walk has
  // as many edges as it has steps.
  const passEdgeWalk = Object.create(null);
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
  // ---- THE VISIT'S OWN MEMORY OF ITSELF (charter shelf 16's fourth pipeline step) ----------------
  // The shelf's dice run in order: base weights, letter cooldowns, the day's weather, THE VIEWER'S
  // MEMORY, roll. The composer has carried all five for a while — `viewerBiasOf` is bounded
  // [0.7, 1.3] and the recurrence fold reads `seenWorks` — but nothing ever filled the fourth,
  // because `passRequestFor` built every other field of the request and never this one. So the
  // fourth step multiplied by exactly one on every real visit: a family lingered over never warmed,
  // one skipped past never cooled, and a work met a second time was handed the same facet.
  //
  // WHAT THE WALK OBSERVES, AND IT OBSERVES NOTHING NEW. Three readings, all of them already taken:
  //   · which works have been met — the arrival of every landing, which `dock` already knows;
  //   · the letters each passage carried — the genre and the instruments of the row `passRoutePlayed`
  //     already writes at that same landing, the same vocabulary `coolOf` cools;
  //   · how long the person stayed with the work that landed — the span between that landing and the
  //     next declare, both of which this file already stamps.
  //
  // LINGERED OR SKIPPED, DECIDED AGAINST THE CROSSING'S OWN LENGTH. The dwell is compared with the
  // duration of the passage that delivered the work, which is a number the walk already froze onto
  // that command — so the comparison is between two things the visit itself produced and no third
  // number is introduced for it. Staying with a work at least as long as the crossing that brought
  // it there is lingering; leaving before it is skipping. Every step falls in exactly one of the two,
  // so nothing is ever left unclassified and no step is measured against anything but itself.
  //
  // OBSERVED, NEVER OBEYED — the shelf's own caution, and it binds. Nothing here decides anything:
  // the three lists cross as plain names, and the only thing that reads them is a bounded multiplier
  // inside the composer's die, which ranks candidates and refuses none.
  //
  // EPHEMERAL BY CONSTRUCTION. Seeds and determinism are the judging mode; ephemerality is the
  // viewer mode. These are plain arrays in this closure — no storage is written, none is read, and
  // nothing survives the page. A fresh door starts them over with the route they belong to.
  let passViewerSeen = [];        // the works this visit has been shown, arrival by arrival
  let passViewerLingered = [];    // the letters of the passages it stayed with
  let passViewerSkipped = [];     // the letters of the passages it walked away from
  let passViewerStanding = null;  // the arrival now standing: when it landed, what it cost, its letters
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
  // WHICH OF TWO CANDIDATE PASSAGES THE WALK PREFERS, read by `passComposeFor`'s roll race below,
  // where the order of the readings and every rank in it are written out. The readings are compared
  // one at a time and the first that separates the two decides, so nothing is ever weighted against
  // anything else and no exchange rate between two unlike readings is needed. Strict: a candidate
  // equal on every reading does NOT displace the one already leading, which is the race's own
  // tie-break rule and is argued where it is used.
  function passRollBetter(now, was) {
    if (!was) return true;
    for (let i = 0; i < now.length; i++) {
      if (now[i] > was[i]) return true;
      if (now[i] < was[i]) return false;
    }
    return false;
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
  //
  // AND `mask`, THE JUDGES' OWN CHANNEL (2026-08-24). It is the one handle every instrument that
  // publishes it reads back AT ITS OWN DOOR — `pass-inst-*.js`'s `doorWhyNoOf`, "the entry door
  // leaks: the judges' own channel stands at …", which refuses the door the moment the channel
  // stands over half a level of 255 — and no branch of the composer ever drives it: `sourceOf` names
  // it «module-rest», nothing writes `wanted.mask`, so `fillPlan` takes the `req === null` road and
  // writes `{op:"static", value: <the manifest's own def>}`, which is 0 on every instrument that
  // publishes the handle. This roll was therefore the ONE writer that could ever move it off zero,
  // and a door met on a repeated edge refused the whole crossing on a number the roll had put there
  // itself. It is skipped here rather than tolerated at the door: the door's law is the picture's,
  // and a breath has no business inside a channel whose whole meaning is that it stands shut.
  //
  // `mask` NAMED ONE INSTANCE OF A CLASS, AND THE CLASS IS THE MANIFEST'S OWN WORD, NOT A NAME LIST
  // (2026-08-25). `unfold`'s `field` was found the same night carrying the identical fault — its
  // manifest declares `applied: { pitchDegreesAtWhole: PITCH_MAX, shutAt: 0 }` (pass-inst-unfold.js)
  // and its own `doorWhyNoOf` refuses the door the moment `worldPx` — `field` read through its curve
  // — leaks past a hair at either door. `gates`' `jamb` declares the same door-rest under a longer
  // key, `applied: { shutBelowTheSlotsOwnWidth: true, shutAtTheFarDoor: true }` (pass-inst-gates.js)
  // — the module's own gate that must close by the far door so both leaves clear the frame. Two
  // instruments, two handle names, one manifest word: `shutAt…`, published beside the handle
  // whenever the module holds it at a fixed reading right at a door. `passHandleShutsAtDoor` below
  // reads that word off the manifest directly, so the next instrument that publishes a door-rest
  // channel is caught the day it ships and never needs a fourth name added here by hand. `mask`
  // stays in the name list beside it rather than folding into the generalized check: its own
  // manifest entries carry no `shutAt…` key (`applied.readAtADoor` on `unfold`, `applied.shows` on
  // `gates`) — it is exempted here on what §4.4f says about the judges' channel, not on what the
  // manifest happens to spell.
  //
  // A handle's manifest may publish, beside its range, that the module holds a fixed reading there
  // AT A DOOR — `applied.shutAt` (`unfold.field`) or `applied.shutAtTheFarDoor` (`gates.jamb`), both
  // read as one word rather than two: any key of `applied` that starts `shutAt` names a door-rest
  // channel, on any instrument, and a breath has no business inside one for the same reason `mask`
  // does not carry one.
  function passHandleShutsAtDoor(instrument, handle) {
    const m = (passComposerConsts() || {}).manifests || {};
    const h = (m[instrument] && m[instrument].handles) ? m[instrument].handles[handle] : null;
    const applied = h && h.applied;
    if (!applied || typeof applied !== "object") return false;
    return Object.keys(applied).some((k) => k.indexOf("shutAt") === 0);
  }
  function passDriftScore(score, key, passes) {
    if (!score || !Array.isArray(score.cues) || !(passes > 0)) return null;
    const reach = PASS_EDGE.driftSpan * Math.min(1, passes / PASS_EDGE.driftOpensOver);
    if (!(reach > 0)) return null;
    const spans = {}, homes = [];
    score.cues.forEach((c) => {
      const instr = (c.instrument && c.instrument.id) || null;
      if (!instr) return;
      Object.keys(c.tracks || {}).sort().forEach((name) => {
        if (name === "mix" || name === "clock" || name === "seed" || name === "mask") return;
        if (passHandleShutsAtDoor(instr, name)) return;
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
    let last = mine, lastDir = direction;
    if (other && (!last || +other.lastAt > +last.lastAt)) {
      last = other;
      lastDir = direction === "a-to-b" ? "b-to-a" : "a-to-b";
    }
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
      // WHAT THE PASS `memory` NAMES WAS ASKED ON — read off the walk's own note to itself
      // (`passEdgeWalk`, written at the landing) and never off the stored record, which §4.8 fences
      // at its own nine names. It rides to the composer on `walkMemory`, a field the request already
      // carries, so nothing about the contract moves either. Read only by the held pre-check in
      // `passComposeFor`, and only inside the visit window, which is the only span where a held pass
      // means anything. It follows the SAME row `memory` does — whichever direction played last —
      // since the question and the die it was struck with have to come off one pass.
      heldWalk: within ? (passEdgeWalk[key + "|" + lastDir] || null) : null,
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
  // tension that demands resolution. Until 2026-08-25 those three words lived only in this comment
  // — the code read the curve and wrote the five names straight out, so nothing ever named a key,
  // changed one, or measured a step's tension against one. The block below is the layer the shelf
  // asks for, and the five names are now the IMAGE of the three functions rather than a second
  // ordering standing beside them.
  //
  // ---- THE HARMONIC LAYER (charter shelf 15, «THE HARMONIC LAYER», his word 18:10) --------------
  //
  // A KEY IS A REGION OF THE COLLECTION'S SPACE — the charter's own definition — «a matter family
  // plus a palette world». Both halves are read off ONE work's own record at the moment the key is
  // named, so a key could not have existed before the works in front of it were known, and no key is
  // ever stored, tabulated or baked.
  //
  //   · THE MATTER FAMILY is what the picture is made of. The record's `structure` block carries one
  //     entry per structural device the picture was read for, and every entry that was actually
  //     scored carries its own `score`. Nothing is listed by name here — the entries are read off
  //     the record's own keys, so a record that grows a further device is read the day it ships —
  //     and the family a work belongs to is simply the device its own record scores highest. The
  //     record's coarser word for the same fact, `structure.ownDevice.kind`, is left where it is:
  //     it names one family and carries no reading for any other, and a key needs a reading for
  //     every family, not only for the work's own.
  //
  //     THERE IS A SECOND READING OF THE SAME QUESTION, and the next reader should know why it is
  //     not the one used here. The record grew a `matter` block in the lab on 2026-08-25 —
  //     `matter.material`, `matter.materialSecond` and `matter.substance` with their votes, read off
  //     `lab/data/material-subject.json` — which says what the picture is made of and what it
  //     depicts in words. It has not been staged into this tree's records yet, so nothing here can
  //     read it today. When it arrives it still will not name the key on its own: a vote against a
  //     closed vocabulary is a reading only the works that vocabulary covers have, while the
  //     structural device is a reading EVERY work has, and a key that some works cannot be named in
  //     would leave those works standing outside every key on the route. The two are worth putting
  //     together later — the words could tell two works apart that score the same device — but the
  //     reading that never comes up empty has to be the one the family stands on.
  //   · THE PALETTE WORLD is the record's `palette` — the hue it leads with, or the rung it names
  //     when it leads with no hue at all — and how tightly it holds it (`hueConcentration`).
  //
  // HOW FAR A WORK STANDS FROM A KEY is the same two readings put to a key that is not its own: its
  // own score for that key's family, and where that key's hue falls in its own hue list. The two
  // averaged give how much of the work stands AT home; the remainder is how far it stands away. A
  // work whose record has not arrived reads null and is never refused on that account — it simply
  // adds no reading of its own, and the step it arrives at is read on the curve alone, which is
  // exactly what this file did before the layer existed.
  function passMatterOf(rec) {
    const s = rec && rec.structure;
    if (!s || typeof s !== "object") return null;
    const out = {};
    Object.keys(s).forEach((k) => {
      const v = s[k];
      if (!v || typeof v !== "object" || !Number.isFinite(+v.score)) return;
      out[k] = Math.max(0, Math.min(1, +v.score));
    });
    return Object.keys(out).length ? out : null;
  }
  function passPaletteOf(rec) {
    const p = rec && rec.palette;
    if (!p || typeof p !== "object") return null;
    const hues = Array.isArray(p.hues) ? p.hues.filter((h) => typeof h === "string" && h) : [];
    const rung = typeof p.rung === "string" && p.rung ? p.rung : null;
    if (!hues.length && !rung) return null;
    // A record that names its palette but not how tightly it holds it is read as holding it whole:
    // the reading ranks the work, and a missing number may not push it below one that has one.
    const hold = Number.isFinite(+p.hueConcentration)
      ? Math.max(0, Math.min(1, +p.hueConcentration)) : 1;
    return { hues: hues, rung: rung, hold: hold };
  }
  // THE KEY THIS ONE WORK IS IN, read off its own record. Ties inside the matter block are broken on
  // the entry name so two visits reading the same record name the same key.
  function passWorkKey(rec) {
    const matter = passMatterOf(rec), pal = passPaletteOf(rec);
    let family = null;
    if (matter) {
      Object.keys(matter).sort().forEach((k) => {
        if (family === null || matter[k] > matter[family]) family = k;
      });
    }
    const world = pal ? (pal.hues.length ? pal.hues[0] : pal.rung) : null;
    if (family === null && world === null) return null;
    return { matter: family, palette: world };
  }
  function passKeyName(key) {
    return key ? String(key.matter || "-") + "/" + String(key.palette || "-") : "-";
  }
  function passSameKey(a, b) {
    return !!a && !!b && a.matter === b.matter && a.palette === b.palette;
  }
  // TWO KEYS APART ON BOTH THEIR AXES — the charter's «two axes changed» rule read against the two a
  // key is made of. Shelf 15 says the key change IS that rule («another family — the «two axes
  // changed» rule is the key change»), and a key's two axes are the matter family and the palette
  // world, so a key that moved on one axis alone has not changed enough for the allusion law. An
  // axis neither key was read on cannot have changed and is not counted as having done so.
  function passKeysTwoAxesApart(a, b) {
    if (!a || !b) return false;
    return a.matter !== b.matter && a.palette !== b.palette;
  }
  // HOW MUCH OF THIS WORK STANDS AT HOME IN THIS KEY, from 0 to 1, or null where the work's record
  // says nothing the key can be read against. Never a refusal: a work always ranks somewhere.
  function passStandingIn(rec, key) {
    if (!rec || !key) return null;
    let sum = 0, read = 0;
    const matter = passMatterOf(rec);
    if (key.matter && matter) { sum += +matter[key.matter] || 0; read++; }
    const pal = passPaletteOf(rec);
    if (key.palette && pal) {
      const at = pal.hues.indexOf(key.palette);
      // The hue the work leads with is the whole of its hold; a hue it carries further down its own
      // list is that hold divided by how far down it stands. A rung answers where hues do not.
      sum += at >= 0 ? pal.hold / (1 + at) : (pal.rung === key.palette ? pal.hold : 0);
      read++;
    }
    return read ? sum / read : null;
  }
  // Does this work stand further from the key than it stands in it? The two halves of one reading
  // compared against each other, so there is no number chosen from outside to compare them to.
  function passStandsAway(home) { return home !== null && (1 - home) > home; }
  //
  // TWO OF THE FIVE NAMES ARE FACTS ABOUT THE VISIT rather than about the route's shape, and before
  // this layer they OVERRODE the curve — which is exactly the two orderings the shelf says must not
  // stand beside each other. They are read as functions now, and the name follows from the function:
  //   · a RETURN is an edge this visit has already walked. The walk restates something it has
  //     already resolved, and a restatement of home is a TONIC. §4.8's own claim is that the way
  //     back is kin to the way out, and the return reference crosses on exactly those edges, so the
  //     function, the name and the reference all name one and the same step.
  //   · an ENTRANCE is the visit's first crossing, wherever it falls. It is where the key is first
  //     stated at this person's ear, and a key being stated is a TONIC — there is no tension to be
  //     had against a key the walk has not yet said. That is also why an entrance can never collide
  //     with a culmination: the crest is the widest step of a route heard AGAINST a key, and the
  //     opening is the step that says the key. The visit window is read the way the memory of a
  //     visit reads it (`PASS_EDGE.visitWindowSeconds`), so a visitor who reloads mid-thought does
  //     not open a second entrance, and one who comes back tomorrow does.
  let passRouteAt = null;
  // THE FIVE NAMES ARE THE IMAGE OF THE THREE FUNCTIONS — one map, standing once, so a step has one
  // ordering and not two that can disagree. A tonic goes by three names, depending on what the walk
  // is doing with home at that step: restating one it has already resolved is a return, stating one
  // for the first time this visit is an entrance, and settling into the one in force is a quiet
  // link. A dominant goes by two: the one the whole route builds to is the culmination, any other is
  // a middle. A subdominant prepares, and preparation has a single name. Nothing outside this
  // function ever writes one of the five.
  function passRoleOfFunction(fn, standingAs) {
    if (fn === "dominant") return standingAs === "crest" ? "culmination" : "middle";
    if (fn === "subdominant") return "middle";
    if (standingAs === "restated") return "return";
    if (standingAs === "founding") return "entrance";
    return "quiet link";
  }
  function passRouteShape() {
    let ids = null;
    // The hung route, read off the walk's own two names. A walk that has not hung yet, an instance
    // with no kinship vectors, or a hang of one work has no route to read a function off; the role
    // is then left unsaid and the composer's own default — a middle — stands, which is exactly what
    // stage 0 composed.
    try { ids = order.slice(0, shown); } catch (e) { return null; }
    if (!ids || ids.length < 2) return null;
    // THE KEY EACH HUNG WORK IS IN, read off the record the walk holds for it at this instant. The
    // records arrive wave by wave (`passRecordsMap`), so the reading is part of what the shape is
    // held against: a route re-read once its records land answers on the keys, and the same route
    // read before them answers on the curve alone. The stamp carries the names rather than a tally
    // of them, so a work whose key is read differently re-reads the shape and nothing counts works.
    const recs = passWorkRecords() || {};
    const recOf = (id) => recs[String(id)] || null;
    const keys = ids.map((id) => passWorkKey(recOf(id)));
    const stamp = ids.join(",") + "|" + keys.map(passKeyName).join(",");
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

    // ---- MODULATION: the walk changes key THROUGH A PIVOT WORK, never by cutting ----------------
    // The walk opens in the key of the first hung work whose record it holds. It changes key when it
    // meets TWO WORKS IN A ROW that agree on a key which is not the one in force — one work standing
    // outside the key is an excursion the walk resolves out of, and it takes a second work agreeing
    // with the first before a new home has been stated. That rule is local, needs no number chosen
    // from outside, and counts nothing.
    //
    // WHERE the change lands is the pivot. The hang order is the walk's own and this layer never
    // reorders it, so what the layer authors is which station the change is DECLARED at: the work,
    // among those from the last change up to and including the first of the two that agree, whose
    // own record belongs MOST to both keys at once — the largest of «the smaller of its two
    // standings». That is the charter's pivot chord read off a record: a work that holds in the key
    // being left and in the key being entered. The search runs over a stretch that always holds at
    // least one work, so a modulation always has a pivot and no walk is ever refused for want of
    // one; where nothing belongs to both, the ranking still returns its best and the change lands
    // there rather than being declined.
    let founding = -1;
    for (let i = 0; i < keys.length; i++) if (keys[i]) { founding = i; break; }
    const modulations = [], modKeys = [];
    if (founding >= 0) {
      let cur = keys[founding], start = founding;
      for (let i = founding; i + 1 < keys.length; i++) {
        if (!keys[i] || !keys[i + 1]) continue;
        if (!passSameKey(keys[i], keys[i + 1]) || passSameKey(keys[i], cur)) continue;
        const to = keys[i];
        let at = start, best = -Infinity;
        for (let j = start; j <= i; j++) {
          const rec = recOf(ids[j]);
          const leaving = passStandingIn(rec, cur), entering = passStandingIn(rec, to);
          const both = Math.min(leaving === null ? 0 : leaving, entering === null ? 0 : entering);
          // Works that belong EQUALLY to both keys leave the walk free to turn at any of them, and
          // it turns at the last: the key in force is held for as long as the belonging allows, so
          // the change is declared as late as it can be rather than as early. Where nothing belongs
          // to both at all the whole stretch reads alike, the last of it is the work the new key
          // first stands at, and the change lands there — which is the only shape a walk with no
          // pivot chord to cross on can take, and it still lands.
          if (both >= best) { best = both; at = j; }
        }
        modulations.push({ at: at, from: passKeyName(cur), to: passKeyName(to),
                           belonging: Math.round(best * 10000) / 10000 });
        modKeys.push(to);
        cur = to; start = at;
      }
    }
    // The key in force at each hung work: the founding key until a pivot is reached, the new key
    // from the pivot onward. The pivot itself is heard in the key it opens, which is what makes it a
    // pivot rather than a cut — it belongs to the key behind it too.
    const keyAt = [];
    {
      let cur = founding >= 0 ? keys[founding] : null, m = 0;
      for (let i = 0; i < ids.length; i++) {
        while (m < modulations.length && modulations[m].at <= i) { cur = modKeys[m]; m++; }
        keyAt.push(cur);
      }
    }

    // ---- THE FUNCTION EACH STEP CARRIES ---------------------------------------------------------
    // Two readings answer for a step, and both are live: the PULL of the step — the kinship gap the
    // walk crosses there, which the hang has already measured for its own ordering — and the
    // STANDING of the work it arrives at against the key in force where the step begins.
    //   · the route's WIDEST step is the one pull nothing on the route exceeds: it DEMANDS
    //     resolution, so it is the DOMINANT the charter calls the culmination, and the crest law is
    //     its suspension.
    //   · the step that leads into the crest prepares it, so it is a SUBDOMINANT whatever its own
    //     pull — motion away, preparation.
    //   · a step whose pull stands above both its neighbours is a widening, and the key says what
    //     kind: a widening that also carries the eye OUT of the key is a DOMINANT, a widening that
    //     stays inside the key is a SUBDOMINANT. This is the one place the key changes what a step
    //     IS, and it is why a route read before its records land reads the same as this file always
    //     did — with no key, no widening can carry the eye out of one, and every widening prepares.
    //   · every other step is where the pull rests: the TONIC, the home the eye settles in. A work
    //     the eye settles on that is NOT in the key is not a fourth function — it is either the
    //     start of a modulation or the deceptive landing below, which is the charter's own reading
    //     of it: home promised, an unexpected kin arrived at.
    const standing = gaps.map((g, i) => passStandingIn(recOf(ids[i + 1]), keyAt[i]));
    const functions = gaps.map((g, i) => {
      if (i === crest) return "dominant";
      if (i === crest - 1) return "subdominant";
      const before = i > 0 ? gaps[i - 1] : -Infinity;
      const after = i + 1 < gaps.length ? gaps[i + 1] : -Infinity;
      if (!(g > before && g > after)) return "tonic";
      return passStandsAway(standing[i]) ? "dominant" : "subdominant";
    });
    const roles = functions.map((fn, i) => passRoleOfFunction(fn, i === crest ? "crest" : "route"));

    // ---- CADENCES: where the walk LANDS ---------------------------------------------------------
    // A landing is a step whose pull falls below the one before it — the tension the previous step
    // raised lets go. What the landing is called follows from what raised it and where it arrives:
    //   · a dominant released onto a work standing in the key is the AUTHENTIC cadence, the strong
    //     landing;
    //   · a subdominant released onto a work standing in the key is the PLAGAL one, the soft
    //     landing;
    //   · a dominant released onto a work standing OUTSIDE the key is the DECEPTIVE cadence — home
    //     was demanded, an unexpected kin arrived. It is kin because the pull fell: the two works
    //     stand close in the very coordinates the hang is ordered by.
    // ITS RARITY IS THE WALK'S OWN, not a frequency chosen here. Four readings have to hold at once
    // on one step and none of them is tunable: the step before it has to be a dominant, which is
    // either the single crest of the route or a widening that carried the eye out of the key; the
    // pull has to fall; the arriving work has to stand further from the key than in it; and it must
    // not be a modulation, because a modulation moves the key to the pivot and the arriving work is
    // then read at home in the key it helped state. Nothing here counts how often it happens.
    const cadences = gaps.map((g, i) => {
      if (i === 0 || !(g < gaps[i - 1])) return null;
      const away = passStandsAway(standing[i]), from = functions[i - 1];
      if (from === "dominant") return away ? "deceptive" : "authentic";
      if (from === "subdominant") return away ? null : "plagal";
      return null;
    });
    // ---- TRANSPOSITION: the same progression replayed in another key ----------------------------
    // The route falls into ERAS — a run of steps heard in one key, the key changing at a pivot. An
    // era's PROGRESSION is nothing new measured: it is the string of functions its steps already
    // carry, in order. A REPRISE is an era whose progression opens the way an earlier era's opened,
    // in a key that stands two axes away from the one it was first heard in.
    //
    // WHY TWO AXES AND NOT ONE. Shelf 15's allusion law asks a motif that returns to come back
    // TRANSFORMED — «minimum two of five axes changed» — and names the key change as that rule:
    // «another family — the «two axes changed» rule is the key change». A key has two axes, the
    // matter family and the palette world, so a progression returning in a key that moved on one
    // axis alone is the return the viewer can name — «а! ну да», the shelf's own recorded failure.
    // Both axes apart is the case the shelf is after, and it is read off the two keys themselves.
    //
    // WHY THE OPENING RUN. Two eras are rarely the same length — the walk deals a fresh hang every
    // visit and the pivots fall where the works put them — so what can repeat is how an era OPENS.
    // The reading is the longest opening run the two eras share, and it takes at least two functions
    // for a progression to have a shape at all: one function repeating is not a progression
    // returning, it is two stations doing the same thing. Where several earlier eras answer, the
    // longest shared opening wins and the earliest of equals is taken, so one hang reads one way.
    //
    // WHAT A REPRISE DOES, AND WHAT IT MUST NOT DO. It changes no function and no name. The five
    // names a step can ask under are untouched, the passage request is untouched, and nothing the
    // viewer can be shown says a reprise happened — because the shelf's own target is wordless déjà
    // vu and its recorded failure is the viewer being able to name the return. It is a reading of
    // the walk the author composes over, published on the walk's own diagnostic surface beside the
    // functions it is made of, and nowhere else.
    const eras = [];
    for (let i = 0; i < functions.length; i++) {
      const name = passKeyName(keyAt[i]);
      const last = eras.length ? eras[eras.length - 1] : null;
      if (last && last.key === name) { last.pattern.push(functions[i]); continue; }
      eras.push({ at: i, key: name, keyOf: keyAt[i], pattern: [functions[i]] });
    }
    const reprises = [];
    for (let e = 1; e < eras.length; e++) {
      let best = null;
      for (let p = 0; p < e; p++) {
        if (!passKeysTwoAxesApart(eras[p].keyOf, eras[e].keyOf)) continue;
        let n = 0;
        while (n < eras[p].pattern.length && n < eras[e].pattern.length
               && eras[p].pattern[n] === eras[e].pattern[n]) n++;
        if (n < 2) continue;
        if (!best || n > best.span) best = { of: eras[p].at, span: n, from: eras[p].key };
      }
      if (best) {
        reprises.push({ at: eras[e].at, span: best.span, of: best.of,
                        from: best.from, to: eras[e].key });
      }
    }
    passRouteAt = { stamp: stamp, ids: ids, gaps: gaps, roles: roles, crest: crest,
                    functions: functions, keys: keys.map(passKeyName),
                    keyAt: keyAt.map(passKeyName), standing: standing,
                    modulations: modulations, cadences: cadences,
                    eras: eras.map((e) => ({ at: e.at, key: e.key, pattern: e.pattern.slice() })),
                    reprises: reprises };
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
  // THE STATION THIS STEP IS for this person at this instant: the function it carries, and which of
  // the five names that function goes by here. Answers a null function and a null name where the
  // walk can state none, and a null name is left OFF the request rather than sent as one: the
  // composer fences the field at its five names and answers an absent one with a middle.
  //
  // The two visit facts are read as FUNCTIONS here rather than as names laid over one, so there is a
  // single ordering and no second one to disagree with it. Both are tonics, for the reasons written
  // out above `passRouteAt`, and both keep the precedence they have always had: a step the visitor
  // has already walked, and the step that opens the visit, are heard as home whatever the route's
  // own curve says about them.
  function passRouteStation(fromId, toId, edge) {
    const shape = passRouteShape();
    const at = shape ? passRouteEdgeAt(shape, String(fromId), String(toId)) : null;
    if (edge && edge.passes > 0) {
      return { at: at, fn: "tonic", role: passRoleOfFunction("tonic", "restated") };
    }
    if (!passVisitOpened()) {
      return { at: at, fn: "tonic", role: passRoleOfFunction("tonic", "founding") };
    }
    if (at === null) return { at: null, fn: null, role: null };
    const fn = shape.functions[at];
    return { at: at, fn: fn, role: passRoleOfFunction(fn, at === shape.crest ? "crest" : "route") };
  }
  function passRouteRole(fromId, toId, edge) {
    return passRouteStation(fromId, toId, edge).role;
  }

  // THE PASSAGE REQUEST the walk builds for one edge (§4.7, U27 stage 0). The edge is named in ONE
  // order whichever way the visitor walks it — the two ids sorted — and `direction` says which way
  // this passage runs, so A to B and B to A are two distinct passages of one edge and the site's own
  // edge record has a stable key to hang on (§4.8, stage 1 lane C).
  //
  // `routeRole` is the walk's own dramaturgy, derived just above and filled at this one place (U27
  // stage 2), and `routeFunction` beside it is the harmonic function that name is the image of.
  // `sessionMemory` is filled from the walk's own edge record: the return reference of §4.8 and
  // nothing wider, and nothing at all on an edge that has not played inside this visit's window.
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
    // THE STATION THIS STEP IS, asked once and read twice. `routeRole` is the name the step asks
    // under and is left exactly as it was, so nothing downstream of it shifts. `routeFunction` is
    // the function that name is the image OF, and it is on the request because the name alone cannot
    // carry it: a subdominant and a dominant are both called a middle, and those are the two the
    // composer most needs apart — one is a preparation, the other a tension that demands resolution.
    // The two come off ONE call, so the request cannot state a name and a function that disagree.
    // Both are omitted where the walk can state none, which is the composer's own «missing means
    // unstated» road rather than a sixth name or a fourth function.
    const station = passRouteStation(from, to, edge);
    const role = station.role;
    if (role) req.routeRole = role;
    if (station.fn) req.routeFunction = station.fn;
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
    // …AND THE VISIT'S OWN MEMORY OF ITSELF, shelf 16's fourth step, filled at this one place for
    // the same reason `walkMemory` is: the walk is the one that knows. Left OFF the request where
    // the visit has been shown nothing yet, rather than sent as three empty lists — an absent field
    // and three empty lists mean the same thing to the composer's fence, and the absent one says it
    // without claiming a reading that was never taken.
    const viewer = passViewerMemory();
    if (viewer) req.viewerMemory = viewer;
    // …AND THE DAY, shelf 16's third dice step, stated by the walk for the same reason the two above
    // are (§4.4g). The shelf asks for two things that meet here and never says which wins: the day's
    // weather is to bias what plays, and a pinned seed is to reproduce a run exactly. Its own last
    // two sentences settle it — seeds and determinism are the JUDGING mode, ephemerality is the
    // VIEWER mode — so the day is an input the VIEWER mode states and the judging mode does not.
    // A public walk sends the instant it cast this pair and the composition breathes with the day; a
    // pinned walk sends none, the day's bias reads neutral on every candidate, and the run
    // reproduces. It is `passEdgeNow` because that is this file's one clock and it stays the one:
    // stating the instant here is what lets the composer hold none, so «the die carries no clock»
    // becomes true of the composer as well as of this file. `passVisitSeed` is asked first only to
    // RESOLVE the pin — it is read lazily at the first crossing that needs a seed, and a visit whose
    // first crossing is a return (a reload inside the visit window) would otherwise read the flag
    // before anything had set it.
    passVisitSeed();
    if (!passVisitPinned) req.day = passEdgeNow();
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

  // HOW LONG THIS CROSSING ITSELF LASTS, read off the command the walk froze — the score's own
  // duration where the pair carries one, and the settings ladder's flight otherwise. It is the same
  // reading the drawing layer's `durationOf` takes, from the same two places and in the same order,
  // so the length a dwell is judged against is the length the person actually watched.
  function passCrossingMsOf(cmd) {
    const named = cmd && cmd.score ? Number(cmd.score.duration) : NaN;
    if (Number.isFinite(named) && named > 0) return named;
    const p = cmd && cmd.params ? cmd.params.flightMs : null;
    const base = Number(p ? p.base : 0);
    return Number.isFinite(base) && base > 0 ? base : 0;
  }
  // THE ARRIVAL, NOTED AT THE LANDING. `grew` says whether this landing wrote a row of its own on
  // the route record a moment ago — only a passage that actually drew does, which is the same rule
  // the edge memory already keeps — so a landing that carried no passage contributes the work it
  // brought and no letters, rather than borrowing the letters of some earlier crossing.
  function passViewerArrived(cmd, grew) {
    const id = cmd && cmd.to ? cmd.to.id : null;
    if (!id || id === "door") { passViewerStanding = null; return; }
    passViewerSeen.push(String(id));
    const step = grew && passRoutePlayed.length
      ? passRoutePlayed[passRoutePlayed.length - 1] : null;
    const letters = [];
    if (step) {
      if (step.genre) letters.push(step.genre);
      (step.stack || []).forEach((name) => { if (name) letters.push(name); });
    }
    passViewerStanding = { at: passEdgeNow(), letters: letters,
                           crossingMs: passCrossingMsOf(cmd) };
  }
  // THE DEPARTURE, NOTED AT THE NEXT DECLARE. The work that was standing is left now, so the dwell
  // it was given is closed and its letters are filed on one of the two lists. A landing that carried
  // no letters files nothing and still counts as met, which is the honest reading: the visit knows it
  // was shown the work and knows nothing about what carried it there.
  function passViewerLeft() {
    const last = passViewerStanding;
    passViewerStanding = null;
    if (!last || !last.letters.length) return;
    const dwell = passEdgeNow() - last.at;
    const list = dwell >= last.crossingMs ? passViewerLingered : passViewerSkipped;
    last.letters.forEach((name) => { list.push(name); });
  }
  // The three lists as the request carries them, or nothing at all where the visit has yet to be
  // shown anything — which is the neutral case the composer's own fence answers the same way a
  // missing field is answered, so a first crossing reads exactly as it always did.
  function passViewerMemory() {
    if (!passViewerSeen.length && !passViewerLingered.length && !passViewerSkipped.length) {
      return null;
    }
    return { lingered: passViewerLingered.slice(), skipped: passViewerSkipped.slice(),
             seenWorks: passViewerSeen.slice() };
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
  // UNJUSTIFIED — how many steps ahead the prewarm looks. His brief names a span rather than a
  // count, and this file took the upper edge of it; nothing measured where the edge should stand.
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
    // THE BEST DIE IS KEPT, and one of them always plays. Each roll is read against §4.8's two
    // readings, against the family still cooling on this edge, and against what this route has
    // already shown; a roll that stands at the best of every reading that CAN stand at its best is
    // taken at once, and where none does the roll that led stays. Before 2026-08-18 a run of refused
    // rolls ended in the walk's plain glide, which is the visitor paying for a reading about
    // repetition with the whole crossing.
    //
    // THE RACE COULD NOT RUN AT ALL UNTIL 2026-08-25, and the loop's own condition is where it
    // stopped. It read `best === null && i < PASS_EDGE.dice`, while the body sets `best` on the
    // FIRST roll that is not declined — so the condition was false by the time it was next tested
    // and the loop ended after one iteration, every time, for every pair. `PASS_EDGE.dice` is 8;
    // the most dice that loop could ever roll is 1, and it does not depend on what the dice landed
    // on: over every combination of the loop's own controls — any `dice`, either `heldStart`, a
    // decline, a clean read or a repeated family at any position — the count is 1. So the scoring
    // below decided nothing on the product path: there was never a second candidate for a best to be
    // best OF, `bestScore` was written and never compared against, and both stopping rules under the
    // race were unreachable. The condition now bounds the race by the dice alone; what ENDS it early
    // is the two stated rules at the foot of the loop, which is what they were written for.
    let best = null, bestReadings = null, bestWhy = null, bestDrift = null, bestCooled = null;
    const routeLast = passRoutePlayed.length ? passRoutePlayed[passRoutePlayed.length - 1] : null;
    // A RETURN TRIES THE EDGE'S OWN HELD PASS FIRST, and takes it outright the moment it legally
    // casts (charter shelf 16, amended tonight: "a route's pressure toward variety ... never
    // outranks the kinship a return owes on an edge already walked ... owed on what is DRAWN — the
    // instrument, the gesture it makes and the level it makes it at"). Scoring the held die in the
    // same race as the others is one of the two things that defeated it: `repeatsFamily` and
    // `repeatsPrimary` exist to space two DIFFERENT edges apart, and scored the one die that is
    // SUPPOSED to repeat as if it were the weakest option. So it is tried here, outside the race,
    // and taken whenever the composer does not decline it; the scored dice below run unchanged for
    // a first crossing (`edge.memory` is null then) and, for a return, only as a fallback where the
    // held pass cannot legally cast.
    //
    // THE OTHER THING THAT DEFEATED IT WAS THE QUESTION, NOT THE DIE (2026-08-24). `request.seed`
    // carries `edge.memory.seed`, and the note above this function used to say that reproduces the
    // recorded pass by construction. It does not, and the claim cost a night: the composer's
    // instrument cast runs the candidate pool through `dieWeighted(pool, seed, key, letters)`, whose
    // weight is `fit × coolOf(id) × viewerBiasOf(id)`, and `coolOf` reads the request's OWN
    // `walkMemory` — the letters the walk has docked so far. That list is a letter or three longer
    // at every step, so the same seed struck two steps later stands on different weights and lands
    // on a different instrument. It reproduces the recorded FAMILY (which `genreFor` holds off
    // `memory.family` outright, on a search that does not read the cooldowns) and nothing below it,
    // which is exactly the shape the evidence showed: the family held while the instrument moved
    // on almost every trip.
    //
    // So the held pre-check asks the composer THE QUESTION THE RECORDED PASS WAS ASKED — the same
    // records, the same direction, the same seed, the same role («return» on every pass but the
    // first), the same session memory, and now the same walk memory, replayed off `passEdgeWalk`.
    // Every input to the cast is then the one that produced the pass being held, so the
    // instrument comes back by construction rather than by luck. The pass count still turns the
    // order of the moves over inside the composer (§4.8 allows it), and the door still breathes
    // through `passDriftScore` below, so a return is held without being a replay.
    //
    // A DECLINE PUTS THE LIVE QUESTION BACK. The scored dice below are fresh choices for this step
    // and the walk's own cooldowns are exactly what should rank them, so the replayed list is
    // restored to the live one the moment the held pass does not cast.
    // `heldTook` is what ends the race before it starts, and it says so in its own name. The loop
    // used to ask `best === null` for this, which reads as «nothing has won yet» and is true of the
    // race's own first roll as much as of the held pass — that is how the race came to end after one
    // die. §4.8's claim is about the HELD pass and nothing else: where it casts, it plays outright.
    let heldStart = 0, heldTook = false;
    if (edge.memory && edge.memory.seed) {
      const liveWalk = request.walkMemory;
      if (Array.isArray(edge.heldWalk)) request.walkMemory = edge.heldWalk;
      let got = null;
      try { got = passComposer.passageFor(request); } catch (e) { got = null; }
      if (!got) {
        passNote(passRefusals, { what: "composer", name: "passage", why: "the entry threw" });
        return null;
      }
      passage = got;
      if (!got.declined) {
        const fam = passFamilyOf(got.plan);
        const primary = passPrimaryOf(got);
        drifted = edge.passes > 0 ? passDriftScore(got.score, edge.key, edge.passes) : null;
        const read = passEdgeJudge(got, edge.within ? edge.last : null);
        refused = read.why;
        cooledStood = (edge.cooled && fam === edge.cooled)
          ? "the family «" + fam + "» played last on this edge and is still cooling" : null;
        rolls.push({ seed: request.seed, family: fam, instrument: primary,
                     repeatsPrevious: (!!routeLast && routeLast.family === fam)
                                      || (!!routeLast && routeLast.instrument === primary),
                     why: refused || cooledStood });
        // The held pass ends the race before it starts — §4.8 takes it outright — so it carries no
        // readings of its own: there is nothing for it to be compared against.
        best = got; bestReadings = null; bestWhy = refused; bestDrift = drifted;
        bestCooled = cooledStood; heldTook = true;
      } else {
        request.walkMemory = liveWalk;
        passNote(passRefusals, { what: "memory", name: edge.key,
                                 why: "the held instrument could not legally cast: "
                                      + got.declined });
      }
      heldStart = 1;
    }
    for (let i = heldStart; !heldTook && i < PASS_EDGE.dice; i++) {
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
      // THE ONE INSTRUMENT NAME TYPED INTO A DECISION on this road, and it is the underived half of
      // rank 8 below — see the note there, and `passRouteRemember`, which reads the same name to
      // decide whether the route has opened a spatial sentence at all. It stands until his word says
      // what a spatial sentence is; the manifests publish each instrument's own levels and do not
      // agree with this name, so reading them would change the preference rather than ground it.
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
      // ---- THE ROLL RACE, SWEPT 2026-08-25 --------------------------------------------------------
      // WHAT STOOD HERE. Eight readings were multiplied by eight numbers — 2, 1, 3, 3, 2, 2, 3 and a
      // ×10 — and added into one score, and the largest score played. Not one of the eight comes from
      // charter shelf 20's three sources: not a picture's own record, not the dramaturgy of the walk,
      // not the session. They are exchange rates between readings that have no common scale, and an
      // exchange rate invented here is the same class `pass-composer.js` swept out of itself on
      // 2026-08-18 on his 09:57 word — «убирай тоже как класс». The sweep stopped at the file
      // boundary; this is the other side of it.
      //
      // AND THE NUMBERS WERE NOT MERELY UNFOUNDED, THEY WERE WRONG, provably and over their whole
      // span rather than over any sample. Every term but the distance is a boolean, and the distance
      // was clamped into 0…1, so the sum a candidate can carry WITHOUT being kin runs to
      // 1 + 1 + 3 + 3 + 2 + 2 + 3 = 15 while kinship itself was worth 2. A candidate that is not kin
      // to the pass this edge already played beat a kin candidate on any one of several readings
      // alone — the world accent's 3 did it single-handed. The charter's own amendment of 2026-08-24
      // evening says the opposite in as many words: «a route's pressure toward variety is a
      // preference among edges met for the FIRST time, and it never outranks the kinship a return
      // owes on an edge already walked». One added number overruled a law, and no sum of
      // incommensurable readings can be prevented from doing that.
      //
      // WHAT STANDS NOW: THE READINGS IN A STATED ORDER, EACH AT ITS OWN SCALE. Nothing is weighted
      // and nothing is added, so no exchange rate is needed and none is invented. The candidates are
      // compared reading by reading, and the first reading that separates two of them decides — so a
      // lower reading can never outweigh a higher one, whatever it holds. Eight numbers are replaced
      // by no numbers at all: what replaces them is the ORDER, and every rank in it is derived.
      //
      //   1 KIN to the pass this edge already played. The charter's amendment ranks it above the
      //     variety readings in its own sentence, and that is the whole of why it is first. On an
      //     edge met for the first time this visit `passEdgeJudge` has no recorded pass to read and
      //     answers kin for every candidate, so this rank decides nothing there and the order falls
      //     through by construction to exactly the edges the amendment calls «met for the FIRST
      //     time». The order does not need to be told which kind of edge it is on.
      //   2 THE LETTER STILL COOLING on this edge. Same source as rank 1 — the edge's own memory —
      //     and below it because kinship is a law a return OWES (§4.8: «the way back is kin to the
      //     way out, never absolutely alien») while a cooldown is step two of shelf 16's dice, a
      //     bias on a pool that «NEVER EMPTIES A POOL». A law outranks a bias.
      //   3 HOW FAR THE PASS STANDS from the recorded one played backwards. Third because it is the
      //     DEGREE of what the two above answer in kind: a candidate that is kin and not cooling is
      //     already lawful, and this says how far it stands from being a literal mirror of what
      //     played. It is also the one reading here that is a number, so it belongs where a number
      //     belongs — separating candidates the facts above could not — and never added to a fact.
      //     Read at its own scale, larger is further from the mirror and better. A null reading is
      //     `passMirrorDistance` saying the two cannot be read as mirrors at all — a different cue
      //     count, different instruments, or the recorded pass standing closer to itself than this
      //     one does — and a pass that is not a mirror in any degree stands further from being one
      //     than any pass that is, so null ranks above every measured distance. That is what the
      //     retired ×10 was reaching for and it needs no number: the old clamp made null merely TIE
      //     with any distance past a tenth, which is a claim about a tenth that nothing supports.
      //   4 THE INSTRUMENT DOES NOT REPEAT THE STEP JUST PLAYED, and 5 the family does not. The
      //     amendment orders these two as well, in the same sentence: «That kinship is owed on what
      //     is DRAWN — the instrument, the gesture it makes and the level it makes it at, because
      //     «тот же эффект» is his own word for the thing, while a family is a name a composition
      //     gives its own pivot and nobody can see one». What a person can see outranks what nobody
      //     can, so the instrument stands above the family wherever both are read.
      //   6 THE INSTRUMENT IS ONE THIS ROUTE HAS NOT SHOWN, and 7 the family is one it has not. The
      //     same two things as 4 and 5, read over the whole route instead of over the step just
      //     taken. Below them because a repeat the person walks straight into is the one they can
      //     see; a repeat some rooms back is the same thing at a distance. Instrument above family
      //     again, on the same sentence.
      //   8 A SPATIAL SENTENCE THIS ROUTE HAS NOT OPENED — and this one is NOT derived. Ranks 1 to 7
      //     each read a fact the charter or §4.8 names; this reads whether the passage is «a
      //     measured parquet ground or a camera-led tonic», and neither half comes off anything: the
      //     camera lead is a field of the score, but which instruments make a spatial sentence is a
      //     name typed here. The instrument manifests do publish the levels each one works at, and
      //     they do not agree with the name — `parquet` declares SURFACE and CELL, while `boxfold`
      //     and `planet` are the two that declare WORLD — so reading the manifest would not preserve
      //     this preference, it would replace it with a different one. It is left standing, and left
      //     LAST, which is the whole of what can honestly be done with it: at the foot of the order
      //     it can only separate two candidates that every derived reading above it read alike, and
      //     it can no longer outrank the kinship it used to outrank on its own. What it needs is his
      //     word on what a spatial sentence is, after which it can be read off the manifest like any
      //     other fact about an instrument.
      //
      // NO CANDIDATE IS SCORED OUT OF THE RACE. Every reading is a preference and none is a fence:
      // the comparison only ever asks which of two candidates stands higher, so the worst-reading
      // candidate on every rank still plays where it is the only one. The race resolves for every
      // pair because the first roll takes the lead unconditionally and is only ever replaced by one
      // that stands strictly higher.
      const readings = [
        read.kin ? 1 : 0,
        cooledStood ? 0 : 1,
        read.distance === null ? Infinity : read.distance,
        repeatsPrimary ? 0 : 1,
        repeatsFamily ? 0 : 1,
        passRouteInstrumentCount[primary] ? 0 : 1,
        passRouteFamilyCount[fam] ? 0 : 1,
        (!passRouteWorldSeen && worldAccent) ? 1 : 0,
      ];
      rolls.push({ seed: request.seed, family: fam, instrument: primary,
                   repeatsPrevious: repeatsFamily || repeatsPrimary,
                   readings: readings.slice(), why: refused || cooledStood });
      // THE TIE-BREAK IS A RULE AND NO LONGER AN ACCIDENT. Two candidates equal on all eight
      // readings are candidates the walk can state no preference between, and the one already
      // leading stays. That is not «whichever was tried first» by chance: die 0's seed is
      // `passSeedFor(edge.key)`, the edge's own name struck once, and every later die is a RE-ROLL
      // of that same question. A re-roll exists to find something better, so it must EARN the
      // replacement; where it finds nothing better the edge's own first answer stands. It is
      // reproducible on a pinned run for the same reason — the dice are tried in the order the
      // edge's key strikes them and no clock reaches this — which is what §4.4b's determinism row
      // asks. `passRollBetter` is that rule, and it is strict on purpose.
      if (best === null || passRollBetter(readings, bestReadings)) {
        best = got; bestReadings = readings; bestWhy = refused; bestDrift = drifted;
        bestCooled = cooledStood;
      }
      // THE WALK STOPS ASKING when the roll stands at the best of every reading that CAN stand at
      // its best on this step — ranks 1 to 5. Those five are about this edge and the step just
      // taken, so a candidate can top all of them on any route. Ranks 6 to 8 are about what the
      // whole route has already shown, and on a route that has already shown every family there is
      // no candidate left that could top them; a stopping rule that asked for those too would be a
      // rule that can never be satisfied, and the walk would burn every die to learn nothing.
      if (read.kin && !cooledStood && read.distance === null
          && !repeatsFamily && !repeatsPrimary) break;
      // A roll that read as a replay is said at once, and not only where the last one does too: a
      // pass that was passed over because it read that way is exactly what a person looking at the
      // surface is trying to find.
      passNote(passRefusals, { what: "memory", name: got.key,
                               why: "die " + (i + 1) + ": " + (refused || cooledStood) });
      // A second die that lands on the same family says the die does not reach this choice, so a
      // third would be the same waste again. Read off `rolls`' own length rather than `i`: on a
      // return whose held instrument declined, `heldStart` skips die 0 without a roll ever pushed
      // for it, so `i` and the array's own index no longer walk together.
      if (rolls.length > 1
          && rolls[rolls.length - 1].family === rolls[rolls.length - 2].family) break;
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
    // The score the command carries is the one the CHECKER handed on, which is a copy of the one the
    // composer wrote wherever anything came off it (`passScoreCheck`, 2026-08-25). A row is found by
    // either — the score it composed, or the reading of that score that actually went to the host.
    for (let i = passPassages.length - 1; i >= 0; i--) {
      const r = passPassages[i];
      if (r.score === cmd.score || r.played === cmd.score) { row = r; break; }
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
    // THE QUESTION THIS PASS WAS STRUCK ON, held for the length of the page and never stored
    // (2026-08-24). The seed alone does NOT reproduce a pass, which is the claim that cost a night:
    // the composer's instrument cast runs its pool through `dieWeighted(..., letters)`, whose weight
    // is `fit × coolOf(id) × viewerBiasOf(id)`, and `coolOf` reads the request's own `walkMemory` —
    // the letters the walk has docked so far. That list is a letter or three longer at every step,
    // so the same seed asked again two steps later stands on different weights and answers a
    // different instrument. A return has to put the question back the way it stood, so the list is
    // kept here for the held pre-check in `passComposeFor` to replay.
    //
    // NOT ON THE STORED RECORD, and that is the law rather than thrift: §4.8 fences what the edge
    // remembers at nine names and the return reference at three, and this is neither — it is the
    // walk's own note to itself about a question it asked a moment ago. It lives as long as the page
    // does, which is longer than any run of returns can be, and a reload simply re-anchors at the
    // first pass after it.
    //
    // ANCHORED AT THE FIRST PASS OF A RUN, never rewritten by the passes that follow: a list rolled
    // forward each time would walk the answer forward with it, one letter at a time, which is the
    // slow version of the very drift this closes. A run that has gone cold (`within` false) starts
    // its own anchor, the same boundary `passCount` itself restarts on.
    const walkAt = edgeKey + "|" + direction;
    if (!within || !Array.isArray(passEdgeWalk[walkAt])) {
      passEdgeWalk[walkAt] = (row.request && Array.isArray(row.request.walkMemory))
        ? row.request.walkMemory.slice() : null;
    }
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
  //
  // WHICH RUNG WON, CARRIED WITH THE VALUE. A frozen node used to say what the value IS and not
  // where it came from, and the two are different facts: a tier of «standard» because a visitor or
  // the site asked for one is a NAMED tier, and a tier of «standard» because nobody said anything is
  // the register's own default standing in. The drawing layer needs to tell them apart — charter
  // shelf 19 has a named setting outrank the device's own reading and an unnamed one yield to it —
  // and `passApplied` already holds the answer, resolved a line earlier by the very call above. It
  // is copied onto the node rather than read from `passApplied` later, because a command is frozen
  // at nav-start and `passApplied` keeps moving with the session after it.
  function passSnapshot(score) {
    const out = {};
    Object.keys(PASS_REG).forEach((k) => {
      const node = passResolve(k, score);
      const row = passApplied[k];
      out[k] = Object.freeze({
        driver: node.driver, asked: node.asked, base: node.base, curve: node.curve,
        points: node.points, supported: node.supported,
        source: row ? row.source : "default",
      });
    });
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
    // THE DWELL JUST ENDED IS CLOSED BEFORE THIS STEP COMPOSES, so the crossing being declared reads
    // a memory that already includes the work the person is walking away from. Closing it after
    // would compose every step against the visit as it stood one step ago.
    passViewerLeft();
    passGen += 1;
    const g = passGen;
    let score = null;
    const raw = a.score || passComposeFor(a.fromEl, a.toEl);
    if (raw) {
      const seen = passScoreCheck(raw);
      if (seen.ok) {
        score = seen.score;
        // THE SCORE THAT PLAYS IS A READING OF THE SCORE THAT WAS COMPOSED, and since 2026-08-25 it
        // is a COPY rather than the same object edited in place. The walk's own passage record is
        // found again at the landing by the IDENTITY of the score that played (`passEdgeRemember`),
        // so the row that composed this one is told which reading of it went to the host. Without
        // this line the record is never found and never written: no return, no drift, no cooldown —
        // the whole of §4.8 silently off, on nothing but a changed object identity. That coupling
        // was invisible while the checker mutated in place, which is its own argument for not.
        if (raw !== score) {
          for (let i = passPassages.length - 1; i >= 0; i--) {
            if (passPassages[i].score === raw) { passPassages[i].played = score; break; }
          }
        }
        // The checker says which version it read (§4.4a). A version-1 score is read forward: its
        // five fields keep feeding the settings ladder exactly as they always did, and it names no
        // cue — so no instrument takes the command and the walk's glide plays, which is what a
        // version-1 score has always meant. The reading is recorded rather than assumed.
        if (seen.read === 1) {
          passNote(passRefusals, { what: "score", name: "schema 1",
                                   why: "read forward: params feed the ladder, no cue to play" });
        }
      // THE RING SHORTENS ITS OWN ROW, and the score keeps its prose. The authored line is a NAME
      // here and nowhere else on this road, so it is fenced by the fence on a name — the same
      // `PASS_LIMITS.text` that fences `cause` a few lines below — instead of the client editing the
      // composer's sentence to fit a number before anything has even asked for it.
      } else passNote(passRefusals, { what: "score", why: seen.why,
                                      name: String(raw.intent || "unnamed").slice(0, PASS_LIMITS.text) });
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
    const routeWas = passRoutePlayed.length;
    if (cmd.score) { passApply(); passEdgeRemember(cmd); }
    // THE VISIT NOTES WHAT IT WAS SHOWN, at the one instant the arrival is certain. It follows the
    // route record rather than standing beside it, so the letters it files are the letters that
    // landing actually wrote — `routeWas` is what says whether it wrote any.
    passViewerArrived(cmd, passRoutePlayed.length > routeWas);
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
  // UNJUSTIFIED — how long each part of the walk's own chrome waits before it comes back. The six
  // waits were chosen here and nothing measured any of them; a score may name its own in their
  // place, which moves who chose them and not whether anything did.
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
    // THE HOST'S OWN FILE IS ASKED FOR HERE TOO, THE SAME LAW AS THE COMPOSER'S TWO LINES ABOVE
    // (U27 stage 2, closing what §10.3's neighbour left open). `passOpen` is guarded on `passAsked`,
    // so this is a no-op wherever an earlier road — the door's own pick, the first render — already
    // fired it; what this line adds is the one path neither of those covers: it makes the landing
    // itself, not a declare, the backstop that guarantees the fetch has started before the visitor's
    // FIRST crossing is ever composed, whatever road brought the visit here.
    passOpen();
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
  // Whoever is waiting for the layer script to land (`passLayerAwait`, below) rather than for a
  // real decline. Drained the instant `passLayerSet` runs, whichever way it lands.
  let passLayerWaiters = [];
  // PASS-API §12: the renderer's own file registers the HOST here — a registry taking one
  // instrument, exposing offer/resize/cancel/report. The seam's old {name, run} shape is gone with
  // the single run(cmd, done) entry point it belonged to (§0, "Where it stands").
  function passLayerSet(layer) {
    passLayer = (layer && typeof layer.offer === "function") ? layer : null;
    passState = passLayer ? "registered" : "absent";
    passWireCastable();          // the P2/P3 follow-up: either half landing tries the hand-off again
    const q = passLayerWaiters; passLayerWaiters = [];
    q.forEach((fn) => { try { fn(); } catch (e) {} });
  }
  function passVisualTakes(cmd) {
    if (!passLayer) { passMark("visual-declined", cmd, "the layer is not registered"); return false; }
    if (cmd.kind === "jump") { passMark("visual-declined", cmd, "a jump carries no crossing"); return false; }
    if (cmd.reduced || cmd.saveData) {
      passMark("visual-declined", cmd, cmd.reduced ? "reduced motion" : "save data");
      return false;
    }
    if (cmd.params.visualLayer.base !== "pass") {
      passMark("visual-declined", cmd, "visualLayer is not set to pass");
      return false;
    }
    passMark("visual-passed", cmd, null);
    return true;
  }
  // THE LAYER SCRIPT ASKED FOR BUT NOT YET LANDED is not the same fact as a layer that will never
  // come (2026-08-24). `passOpen` fires the fetch once, at the setting's own word, and a genuine
  // absence — reduced motion, save-data, no webgl2, the setting itself standing off, or the fetch
  // itself failing — is judged once and does not change mid-visit; none of those are held here.
  // What IS held is the narrow window between that fetch starting and its script's own load event,
  // which a gesture can easily land inside on a visit's very first step. `passLayerPending` names
  // the window; `passLayerAwait` waits it out, bounded, before falling back to the plain glide.
  // UNJUSTIFIED — how long a gesture waits for the drawing layer's own script to finish loading
  // before it takes the plain glide instead. This file chose 350 ms and nothing measured it.
  const PASS_LAYER_HOLD_MS = 350;
  function passLayerPending(cmd) {
    if (!cmd || cmd.reduced || cmd.saveData || cmd.kind === "jump") return false;
    if (passGet("visualLayer") !== "pass") return false;
    return passAsked && !passLayer && passState === "asked";
  }
  function passLayerAwait(cmd, done) {
    if (!passLayerPending(cmd)) { done(false); return; }
    let rung = false;
    const finishOnce = (ok) => { if (rung) return; rung = true; clearTimeout(t); done(ok); };
    const t = setTimeout(() => finishOnce(false), PASS_LAYER_HOLD_MS);
    passLayerWaiters.push(() => finishOnce(!!passLayer));
  }
  // A layer that throws stands for the rest of the visit and is dropped only after several throws
  // in a row with no successful offer between them (2026-08-24) — it used to be torn down on its
  // very first throw, losing the whole visual layer for every later crossing over one bad frame. The
  // host owns the offer/prepare/decline decision entirely (§2.1); a `true` return means the host has
  // taken responsibility for landing this command — by taking over, or by calling the glide hook
  // itself when it declines — never that a renderer is now drawing.
  // A STEP WHOSE RECORDS ARE STILL ON THE WIRE WAITS FOR THEM (2026-08-25). The works were chosen
  // before the wave went out — the door picks the hand and asks for its ids in the same beat — so a
  // crossing declared inside that window is not a crossing without a record, it is a crossing whose
  // record is on its way. Until today it read as the first and took the walk's plain glide, which is
  // the visitor paying for the wire's latency with the whole passage.
  //
  // HELD HERE, AND NOT EARLIER, because this is the first road that knows the step is a crossing at
  // all. `passVisualTakes` has already stood down every visit that will never play one — reduced
  // motion, save-data, a jump, a wire whose layer is off, no registered layer — so none of them ever
  // reaches this line, let alone waits at one.
  //
  // A `true` return is exactly what §2.1 already means by it: THIS FILE has taken responsibility for
  // landing the command, by a passage or by the glide, and the caller goes no further. That is the
  // same word the host gives when it takes over, and the caller has always honoured it.
  function passRecordsHold(cmd) {
    if (!cmd || cmd.score) return false;         // composed already; there is nothing to wait for
    if (!passComposer) return false;             // the composer's own absence, said on its own road
    const from = cmd.from && cmd.from.id, to = cmd.to && cmd.to.id;
    // The door is not a work and carries no record, so a crossing touching it never had one coming.
    if (!from || !to || from === "door" || to === "door") return false;
    if (!passRecordsComing([from, to])) return false;
    passRecordsHolds += 1;
    passMark("records-hold", cmd, from + "__" + to);
    passRecordsAwait([from, to], () => {
      // A NEWER DECLARE OWNS ITS OWN LANDING — the law the walk's own layer hold reads by. A second
      // gesture inside this wait has already declared and landed a step of its own, and acting on
      // the stale command here would move the visitor twice.
      if (cmd.gen !== passGen) return;
      passRecordsResume(cmd);
    });
    return true;
  }
  // THE HELD STEP, DECLARED AGAIN NOW THAT THE ANSWER IS IN. The command being held was frozen
  // before the wave landed — its score and the settings ladder `passSnapshot` read off that score
  // are both a reading of a walk that had no record — so the step is re-declared rather than patched:
  // `passStart` supersedes the held command by the ordinary road and mints one whose score, params
  // and generation are all a reading of THIS instant. Nothing is stored between the two: the fresh
  // declare composes from the records the map now holds, on its own dice, exactly as a gesture
  // arriving a moment later would have.
  function passRecordsResume(cmd) {
    const standing = (el) => !!(el && el.dataset && document.body.contains(el));
    const fromEl = passResolveEl(cmd.from), toEl = passResolveEl(cmd.to);
    const fresh = (standing(fromEl) && standing(toEl))
      ? passStart({ fromEl: fromEl, toEl: toEl, dir: cmd.dir, span: cmd.span, kind: cmd.kind,
                    cause: cmd.cause, velocity: cmd.velocity })
      : null;
    if (!fresh) {
      passNote(passRefusals, { what: "records", name: "hold",
                               why: "a work of the held step left the hang while its wave was in "
                                    + "flight: the walk's own glide carries the step" });
      glide(cmd);
      return;
    }
    if (!fresh.score) {
      // THE WAVE CAME BACK WITH NOTHING FOR THIS PAIR — the route omitted an id, or its retries were
      // spent. The step still happens, on the walk's own glide, which is what a pair with no record
      // has always meant; the difference from before is only that the walk waited to find out.
      passNote(passRefusals, { what: "records", name: "hold",
                               why: "the wave settled carrying no record for this pair: the held "
                                    + "step takes the walk's own glide" });
    }
    if (passVisualTakes(fresh) && passOffer(fresh)) return;
    glide(fresh);
  }
  let passOfferThrows = 0;
  // UNJUSTIFIED — how many times the layer's own `offer` may throw in a row before this file stops
  // asking it. Three was chosen here and nothing measured it.
  const PASS_OFFER_THROW_MAX = 3;
  function passOffer(cmd) {
    if (passRecordsHold(cmd)) return true;
    try {
      const took = passLayer.offer(cmd, { dock: dock, glide: glide, curtain: curtain, mark: passMark,
                                    hangGeometry: hangGeometry, handoff: handoff }) === true;
      passOfferThrows = 0;
      if (!took) passMark("visual-declined", cmd, "the layer's own offer returned false");
      return took;
    }
    catch (e) {
      passOfferThrows += 1;
      passNote(passRefusals, { what: "layer", name: "offer",
                               why: "threw (" + passOfferThrows + " in a row)" });
      passMark("visual-declined", cmd, "the layer's offer threw");
      if (passOfferThrows >= PASS_OFFER_THROW_MAX) passLayerSet(null);
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
                // THE VISIT'S OWN MEMORY OF ITSELF beside the edge store, and plainly apart from it:
                // the edge store is written to the browser and survives a reload, and these three
                // lists are this page's alone and die with it. `standing` is the arrival the person
                // is looking at right now — the dwell that has not closed yet.
                visit: { lingered: passViewerLingered.slice(),
                         skipped: passViewerSkipped.slice(),
                         seenWorks: passViewerSeen.slice(),
                         standing: passViewerStanding
                           ? { letters: passViewerStanding.letters.slice(),
                               crossingMs: passViewerStanding.crossingMs }
                           : null },
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
                 // THE HARMONIC LAYER'S OWN READINGS beside them (shelf 15): the function each step
                 // carries, the key each hung work is in and the key in force where each step
                 // begins, how much of the arriving work stands at home there, where the walk
                 // changed key and through which work, and where it landed. A step that looks wrong
                 // reads back to the key it was heard in without reading anything else.
                 functions: shape.functions.slice(), keys: shape.keys.slice(),
                 keyAt: shape.keyAt.slice(),
                 standing: shape.standing.map((s) => s === null ? null
                                                                : Math.round(s * 10000) / 10000),
                 modulations: shape.modulations.slice(), cadences: shape.cadences.slice(),
                 // …and the eras the key changes cut the route into, with the progression each
                 // opens with, and where one era replays another's opening in a key two axes away.
                 // A reading for the author, never for the viewer: nothing downstream of here can
                 // show a person that a reprise happened.
                 eras: shape.eras.slice(), reprises: shape.reprises.slice(),
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
                 inflight: passRecordsWaves - passRecordsSettled,
                 // …and how many INDIVIDUAL ids are still on the wire, which is the number a step
                 // holds on (`passRecordsComing`). A wave count cannot answer it: one wave may carry
                 // twenty ids and a second wave one, and what a crossing waits for is its own two.
                 coming: Object.keys(passRecordsInFlight).length,
                 // How many steps are holding on a wave at this instant, and how many ever have.
                 waiting: passRecordsWaiters.length, holds: passRecordsHolds },
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
                 // `station` is the same answer with its function beside it, so a row can prove the
                 // name a step asks under is the image of the function it carries and not a second
                 // reading standing next to it. `key` and `standing` are the two record readings a
                 // key is named and measured by, handed over for the same reason.
                 station: passRouteStation, key: passWorkKey, standing: passStandingIn,
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
