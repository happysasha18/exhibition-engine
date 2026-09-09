/*!pass-touch.js*/
// The touch layer over a standing work — what a hand does to a picture nobody is crossing away from.
// Fetched separately, the same shape as pass-hand.js (a classic script, a namespaced receiver
// installed by the client before this file runs, one plain object handed to the join). His word of
// 2026-09-09 19:26: a work at rest stands still; where the hand touches or hovers, something
// happens — a kaleidoscope, a lens, a ripple as on water, and more — and which one, with which
// numbers, is decided from what is known about the picture.
//
// THREE PARTS LIVE HERE.
//   1. The effects: one fragment shader with a mode per effect, driven only by the hand — where it
//      is, how long it has stayed, whether it presses, where it tapped. Every effect fades in as the
//      hand arrives and out as it leaves; a tap drops a ripple in every mode.
//   2. The assignment: `assign(record)` reads the work's own record (symmetry, structure, texture,
//      colour, matter — the same record the composer reads) and ranks every effect by what the
//      picture itself supports; the winner plays, and the ranking says why in plain words so a page
//      can show the reasoning.
//   3. The overlay: one canvas laid over the standing work's own <img>, sized to its box, hidden
//      whenever the hand is off and nothing is fading. Pointer events pass through it (the walk's
//      own pagers keep navigation); this file listens on the window, passively, and asks only
//      whether the element under the pointer is the work it is attached to.
//
// The frame loop runs only while a hand is on the picture or an effect is still fading. At rest
// nothing here draws, so a resting work costs nothing and stands exactly as still as before.
(function () {
  var join = window.__@@NS@@PassTouch;
  if (typeof join !== "function") return;

  var TARGET_SEL = ".exh-frame img.work";
  // The client hands over `recordFor(id)` at join: the record a work's wave lands, or null while
  // it is still in the air. A work attached before its record landed is re-read on the hand's next
  // arrival, so the first touch after the wave plays what the record chose, not the default.
  var hostRecordFor = null;
  function host(api) { hostRecordFor = (api && typeof api.recordFor === "function") ? api.recordFor : null; }

  // ---- the effects -----------------------------------------------------------------------------
  // `params` are the numbers the shader reads; `assign` overrides them from the record.
  var EFFECTS = [
    { id: "kaleido", title: "калейдоскоп", mode: 0,
      note: "картинка складывается в зеркальные дольки вокруг точки касания; держишь дольше — круг шире",
      params: { radius: 0.22, strength: 1, count: 6, flag: 1, speed: 0.15 } },
    { id: "lens", title: "линза", mode: 1,
      note: "лупа под пальцем: середина крупнее, край расщепляет цвет; нажатие увеличивает сильнее",
      params: { radius: 0.19, strength: 1.2 } },
    { id: "water", title: "рябь", mode: 2,
      note: "тап роняет каплю — круги расходятся и гаснут; рука волнует воду под собой",
      params: { radius: 0.22, strength: 1.6, period: 0.09 } },
    { id: "swirl", title: "вихрь", mode: 3,
      note: "картинка закручивается вокруг точки касания; держишь — сильнее, нажал — ещё сильнее",
      params: { radius: 0.3, strength: 1.4, dir: 1 } },
    { id: "chroma", title: "разлом цвета", mode: 4,
      note: "красный, зелёный и синий разъезжаются от руки наружу",
      params: { radius: 0.38, strength: 1 } },
    { id: "negative", title: "проявка", mode: 5,
      note: "под рукой картинка уходит в негатив мягким пятном, как плёнка на свету",
      params: { radius: 0.24, strength: 1 } },
    { id: "heat", title: "марево", mode: 6,
      note: "над рукой воздух дрожит, как над горячим асфальтом",
      params: { radius: 0.34, strength: 1.8 } },
    { id: "drops", title: "капли на стекле", mode: 7,
      note: "вокруг руки на стекле проступают капли, каждая — маленькая линза",
      params: { radius: 0.36, strength: 1.6, count: 16 } },
    { id: "melt", title: "плавка", mode: 8,
      note: "под рукой картинка течёт вниз столбиками; чем дольше держишь, тем длиннее потёки",
      params: { radius: 0.32, strength: 1, count: 90 } },
    { id: "focus", title: "фокус", mode: 9,
      note: "резким остаётся круг под рукой, остальное мягко размывается",
      params: { radius: 0.17, strength: 1 } },
    { id: "funnel", title: "воронка", mode: 10,
      note: "картинка стягивается в точку под рукой, как в воронку; держишь — глубже",
      params: { radius: 0.34, strength: 0.7 } },
    { id: "hue", title: "карусель оттенков", mode: 11,
      note: "вокруг руки цвета проворачиваются по кругу оттенков; нажатие крутит быстрее",
      params: { radius: 0.36, strength: 1 } },
    { id: "torch", title: "фонарик", mode: 12,
      note: "картинка темнеет, и только под рукой горит светлое пятно",
      params: { radius: 0.24, strength: 1 } },
    { id: "mirror", title: "зеркало", mode: 13,
      note: "через точку касания проходит зеркальная ось — половина картинки отражается на другую; ось идёт за рукой",
      params: { radius: 1, strength: 1, axis: [1, 0] } },
    { id: "blinds", title: "жалюзи", mode: 14,
      note: "картинка разрезана на полосы по её собственному ритму; у руки полосы сдвигаются вразнобой",
      params: { radius: 0.4, strength: 1, axis: [0, 1], period: 0.08 } },
    { id: "mosaic", title: "мозаика", mode: 15,
      note: "картинка разбита на плитки её собственной решётки; у руки плитки переворачиваются",
      params: { radius: 0.3, strength: 1, period: 0.07 } },
    { id: "shore", title: "вода у горизонта", mode: 16,
      note: "ниже линии горизонта картинка становится водой и отражает верх; тап — круги по воде",
      params: { radius: 0.3, strength: 1, horizon: 0.5 } },
    { id: "split", title: "разрез", mode: 17,
      note: "по линии, которая делит картинку на две области, она раздвигается, когда рука рядом",
      params: { radius: 0.4, strength: 1, line: [0.5, 0.5], axis: [1, 0] } },
    { id: "spiral", title: "спираль", mode: 18,
      note: "картинка закручивается спиралью вокруг руки — чем дальше от неё, тем сильнее поворот",
      params: { radius: 0.5, strength: 1, dir: 1 } },
    { id: "rays", title: "лучи", mode: 19,
      note: "из точки касания картинка расходится лучами, как при рывке объектива",
      params: { radius: 0.5, strength: 1 } },
  ];
  var BY_ID = {};
  EFFECTS.forEach(function (e) { BY_ID[e.id] = e; });

  // ---- the assignment --------------------------------------------------------------------------
  // Every rule reads one or two fields of the record and gives one effect a score between 0 and 1
  // with the parameters those very fields set. The strongest score plays. `text` is the rule in
  // words, for a page that shows the reasoning; `why` is the same rule filled with this record's
  // numbers.
  function num(v, d) { v = +v; return isFinite(v) ? v : d; }
  function get(o, path, d) {
    var cur = o;
    for (var i = 0; i < path.length; i++) {
      if (!cur || typeof cur !== "object") return d;
      cur = cur[path[i]];
    }
    return cur === undefined || cur === null ? d : cur;
  }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
  function f2(v) { return (Math.round(v * 100) / 100).toFixed(2); }

  var RULES = [
    { effect: "kaleido",
      text: "поворотная симметрия (structure.rotational.score, порядок n): чем выше, тем скорее калейдоскоп; долек 2n, зеркальные — если секторы зеркальны; скорость поворота от закрученности (polar.twirl)",
      read: function (r) {
        var s = num(get(r, ["structure", "rotational", "score"]), 0);
        var n = Math.round(num(get(r, ["structure", "rotational", "n"]), 2));
        var mir = get(r, ["symmetry", "rotation", "wedgesMirrored"], true) ? 1 : 0;
        var tw = num(get(r, ["structure", "polar", "twirl"]), 0);
        return { score: s + (n >= 3 ? 0.12 : 0),
                 params: { count: clamp(2 * n, 4, 12), flag: mir, speed: 0.08 + 0.5 * tw },
                 why: "поворот порядка " + n + " читается на " + f2(s) + " → " + clamp(2 * n, 4, 12) +
                      " долек" + (mir ? ", зеркальные" : "") + ", поворот " + f2(0.08 + 0.5 * tw) };
      } },
    { effect: "spiral",
      text: "закрученность (structure.polar.twirl): спираль вокруг руки, сила по чтению",
      read: function (r) {
        var tw = num(get(r, ["structure", "polar", "twirl"]), 0);
        return { score: tw * 1.1, params: { strength: 0.6 + 1.2 * tw },
                 why: "закрученность " + f2(tw) + " → сила спирали " + f2(0.6 + 1.2 * tw) };
      } },
    { effect: "funnel",
      text: "вид в туннель (structure.polar.tunnel): воронка под рукой, глубина по чтению",
      read: function (r) {
        var t = num(get(r, ["structure", "polar", "tunnel"]), 0);
        return { score: t * 0.95, params: { strength: 0.4 + 0.6 * t },
                 why: "туннель " + f2(t) + " → глубина воронки " + f2(0.4 + 0.6 * t) };
      } },
    { effect: "rays",
      text: "лучи из центра (structure.polar.radial_streak): лучи из точки касания",
      read: function (r) {
        var s = num(get(r, ["structure", "polar", "radial_streak"]), 0);
        return { score: s, params: { strength: 0.5 + s },
                 why: "лучи читаются на " + f2(s) + " → длина лучей " + f2(0.5 + s) };
      } },
    { effect: "mirror",
      text: "зеркальность (symmetry.reflection.*.reading): зеркало по самой сильной оси картинки — вертикальной, горизонтальной или диагональной",
      read: function (r) {
        var best = null;
        [["leftOntoRight", [1, 0], "вертикальная"], ["topOntoBottom", [0, 1], "горизонтальная"],
         ["mainDiagonal", [0.7071, -0.7071], "диагональная"], ["antiDiagonal", [0.7071, 0.7071], "обратная диагональная"]]
          .forEach(function (ax) {
            var v = num(get(r, ["symmetry", "reflection", ax[0], "reading"]), 0);
            if (!best || v > best.v) best = { v: v, axis: ax[1], name: ax[2] };
          });
        return { score: best.v * 0.9, params: { axis: best.axis },
                 why: best.name + " ось читается на " + f2(best.v) + " → зеркало по ней" };
      } },
    { effect: "blinds",
      text: "полосы (structure.banding.score, axis, periodPx): жалюзи вдоль оси полос с их шагом",
      read: function (r) {
        var s = num(get(r, ["structure", "banding", "score"]), 0);
        var ax = get(r, ["structure", "banding", "axis"], "horizontal");
        var per = num(get(r, ["structure", "banding", "periodPx"]), 0) / Math.max(1, num(r && r.frameSide, 1440));
        per = per > 0.01 ? clamp(per, 0.03, 0.3) : 0.08;
        return { score: s * 1.3, params: { axis: ax === "vertical" ? [1, 0] : [0, 1], period: per },
                 why: "полосы " + (ax === "vertical" ? "вертикальные" : "горизонтальные") + " на " + f2(s) +
                      ", шаг " + f2(per) + " ширины кадра → жалюзи с этим шагом" };
      } },
    { effect: "mosaic",
      text: "решётка (structure.grid.score, periodPx): мозаика плитками решётки; вступает при чтении выше 0.2",
      read: function (r) {
        var s = num(get(r, ["structure", "grid", "score"]), 0);
        var per = num(get(r, ["structure", "grid", "periodPx"]), 0) / Math.max(1, num(r && r.frameSide, 1440));
        per = per > 0.01 ? clamp(per, 0.03, 0.25) : 0.07;
        return { score: s > 0.2 ? 0.3 + s : s * 0.5, params: { period: per },
                 why: "решётка читается на " + f2(s) + ", шаг " + f2(per) + " → плитки этого шага" };
      } },
    { effect: "shore",
      text: "горизонт (structure.horizon.seam, y): вода ниже линии горизонта; вступает при шве выше 0.25",
      read: function (r) {
        var seam = num(get(r, ["structure", "horizon", "seam"]), 0);
        var y = num(get(r, ["structure", "horizon", "y"]), 0.5);
        return { score: seam > 0.25 ? 0.35 + seam : seam * 0.5, params: { horizon: 1 - y },
                 why: "шов горизонта " + f2(seam) + " на высоте " + f2(y) + " → вода ниже него" };
      } },
    { effect: "split",
      text: "области (structure.regions.score, line.x/line.y explains): разрез по линии, которая объясняет больше",
      read: function (r) {
        var s = num(get(r, ["structure", "regions", "score"]), 0);
        var lx = get(r, ["structure", "regions", "line", "x"], null);
        var ly = get(r, ["structure", "regions", "line", "y"], null);
        var ex = lx ? num(lx.explains, 0) : 0, ey = ly ? num(ly.explains, 0) : 0;
        var vertical = ex >= ey;
        var at = vertical ? num(lx && lx.at, 0.5) : num(ly && ly.at, 0.5);
        var e = Math.max(ex, ey);
        return { score: s * e * 1.4, params: { line: vertical ? [at, 0.5] : [0.5, 1 - at], axis: vertical ? [1, 0] : [0, 1] },
                 why: "области " + f2(s) + ", линия " + (vertical ? "x=" + f2(at) : "y=" + f2(at)) +
                      " объясняет " + f2(e) + " → разрез по ней" };
      } },
    { effect: "water",
      text: "гладкость (1 − measures.texture) и спектральный период (texture.spectralPeriodPx): рябь; длина волны от периода",
      read: function (r) {
        var tx = num(get(r, ["measures", "texture"]), 0.5);
        var per = num(get(r, ["texture", "spectralPeriodPx"]), 0) / Math.max(1, num(r && r.frameSide, 1440));
        per = per > 0.005 ? clamp(per, 0.03, 0.2) : 0.09;
        return { score: 0.3 + 0.35 * (1 - tx), params: { period: per },
                 why: "фактура " + f2(tx) + " (гладкость " + f2(1 - tx) + "), период " + f2(per) + " → длина волны ряби" };
      } },
    { effect: "heat",
      text: "яркость (luminance.level) и бетон/асфальт в веществах (matter.substanceVotes): марево",
      read: function (r) {
        var lum = num(get(r, ["luminance", "level"]), 0.5);
        var votes = get(r, ["matter", "substanceVotes"], {}) || {};
        var conc = num(votes["бетон"], 0) + num(votes["асфальт"], 0) + num(votes["камень"], 0);
        var total = 0; Object.keys(votes).forEach(function (k) { total += num(votes[k], 0); });
        var share = total ? conc / total : 0;
        return { score: 0.2 + 0.35 * lum + 0.3 * share, params: { strength: 1.4 + 1.2 * share },
                 why: "яркость " + f2(lum) + ", доля бетона/камня " + f2(share) + " → сила марева " + f2(1.4 + 1.2 * share) };
      } },
    { effect: "drops",
      text: "стекло в веществах (matter.substanceVotes.стекло): капли; чем больше стекла, тем гуще капли",
      read: function (r) {
        var votes = get(r, ["matter", "substanceVotes"], {}) || {};
        var glass = num(votes["стекло"], 0), total = 0;
        Object.keys(votes).forEach(function (k) { total += num(votes[k], 0); });
        var share = total ? glass / total : 0;
        return { score: 0.22 + 0.55 * share, params: { count: Math.round(12 + 16 * share) },
                 why: "доля стекла " + f2(share) + " → плотность капель " + Math.round(12 + 16 * share) };
      } },
    { effect: "chroma",
      text: "цветность (palette.colourfulness × colour.sat): разлом цвета",
      read: function (r) {
        var c = num(get(r, ["palette", "colourfulness"]), 0.3) * num(get(r, ["colour", "sat"]), 0.3);
        return { score: 0.2 + 0.9 * c, params: { strength: 0.8 + 1.5 * c },
                 why: "цветность×насыщенность " + f2(c) + " → размах разлома " + f2(0.8 + 1.5 * c) };
      } },
    { effect: "hue",
      text: "насыщенность (colour.sat) и собранность оттенков (palette.hueConcentration): карусель оттенков",
      read: function (r) {
        var s = num(get(r, ["colour", "sat"]), 0.3), h = num(get(r, ["palette", "hueConcentration"]), 0.5);
        return { score: 0.15 + 0.6 * s * h, params: { strength: 0.6 + s },
                 why: "насыщенность " + f2(s) + ", собранность оттенков " + f2(h) + " → карусель на " + f2(0.6 + s) };
      } },
    { effect: "negative",
      text: "бесцветность (1 − colour.sat) и контраст (colour.contrast): проявка в негатив",
      read: function (r) {
        var s = num(get(r, ["colour", "sat"]), 0.3), c = num(get(r, ["colour", "contrast"]), 0.4);
        return { score: 0.18 + 0.45 * (1 - s) + 0.2 * c, params: {},
                 why: "насыщенность " + f2(s) + ", контраст " + f2(c) + " → негатив" };
      } },
    { effect: "torch",
      text: "темнота (1 − colour.brightness): фонарик",
      read: function (r) {
        var b = num(get(r, ["colour", "brightness"]), 0.5);
        return { score: 0.18 + 0.6 * (1 - b), params: { radius: 0.18 + 0.12 * b },
                 why: "яркость " + f2(b) + " → фонарик, пятно " + f2(0.18 + 0.12 * b) };
      } },
    { effect: "melt",
      text: "фактура (measures.texture) и металл в веществах: плавка",
      read: function (r) {
        var tx = num(get(r, ["measures", "texture"]), 0.3);
        var votes = get(r, ["matter", "substanceVotes"], {}) || {};
        var metal = num(votes["металл"], 0), total = 0;
        Object.keys(votes).forEach(function (k) { total += num(votes[k], 0); });
        var share = total ? metal / total : 0;
        return { score: 0.15 + 0.3 * tx + 0.25 * share, params: { strength: 0.8 + share },
                 why: "фактура " + f2(tx) + ", доля металла " + f2(share) + " → плавка" };
      } },
    { effect: "lens",
      text: "названные предметы (measures.named_objects): линза — есть что разглядывать",
      read: function (r) {
        var n = num(get(r, ["measures", "named_objects"]), 0.3);
        return { score: 0.28 + 0.4 * n, params: { strength: 1 + 0.6 * n },
                 why: "предметов " + f2(n) + " → увеличение " + f2(1 + 0.6 * n) };
      } },
    { effect: "focus",
      text: "пустота (motifs.voidShare): фокус — резкий круг в пустом поле",
      read: function (r) {
        var v = num(get(r, ["motifs", "voidShare"]), 0.3);
        return { score: 0.15 + 0.4 * v, params: { radius: 0.12 + 0.1 * v },
                 why: "пустота " + f2(v) + " → круг резкости " + f2(0.12 + 0.1 * v) };
      } },
    { effect: "swirl",
      text: "закрученность (polar.twirl) и кольца (structure.radial.subType = ring): вихрь",
      read: function (r) {
        var tw = num(get(r, ["structure", "polar", "twirl"]), 0);
        var ring = get(r, ["structure", "radial", "subType"], "") === "ring" ? 1 : 0;
        return { score: 0.2 + 0.5 * tw + 0.15 * ring, params: { strength: 1 + tw, dir: ring ? -1 : 1 },
                 why: "закрученность " + f2(tw) + (ring ? ", кольца" : "") + " → вихрь силой " + f2(1 + tw) };
      } },
  ];

  function assign(record) {
    var rec = record || {};
    var ranked = RULES.map(function (rule) {
      var out;
      try { out = rule.read(rec); } catch (e) { out = { score: 0, params: {}, why: "правило не прочиталось: " + (e && e.message || e) }; }
      var def = BY_ID[rule.effect];
      var params = {};
      Object.keys(def.params).forEach(function (k) { params[k] = def.params[k]; });
      Object.keys(out.params || {}).forEach(function (k) { params[k] = out.params[k]; });
      return { effect: rule.effect, title: def.title, score: clamp(num(out.score, 0), 0, 1.5),
               params: params, why: out.why, text: rule.text };
    });
    ranked.sort(function (a, b) { return b.score - a.score; });
    var top = ranked[0];
    return { effect: top.effect, title: top.title, params: top.params, why: top.why,
             ranked: ranked, hasRecord: !!record };
  }

  // ---- the shader ------------------------------------------------------------------------------
  // CAPABILITY — the vertex shader is the one full-screen quad every effect draws on; it carries no
  // number of its own, and the fragment shader beside it reads every number from the uniforms above.
  var VS = "attribute vec2 aPos; varying vec2 vUv; void main(){ vUv = aPos*0.5+0.5; gl_Position = vec4(aPos,0.0,1.0); }";
  var FS = [
    "precision highp float;",
    "varying vec2 vUv;",
    "uniform sampler2D uTex; uniform vec2 uCover; uniform float uAspect;",
    "uniform vec2 uP; uniform float uAmt; uniform float uHold; uniform float uTime; uniform float uDown;",
    "uniform int uMode; uniform vec4 uRip[8];",
    "uniform float uRadius; uniform float uStrength; uniform float uCount; uniform float uFlag; uniform float uSpeed;",
    "uniform vec2 uAxis; uniform float uPeriod; uniform float uHorizon; uniform vec2 uLine; uniform float uDir;",
    "vec4 tex(vec2 uv){ return texture2D(uTex, (clamp(uv,0.0,1.0)-0.5)*uCover+0.5); }",
    "float hash(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }",
    "float noise(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.0-2.0*f);",
    "  return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y); }",
    "vec2 asp(vec2 v){ return vec2(v.x*uAspect, v.y); }",
    "vec2 unasp(vec2 v){ return vec2(v.x/uAspect, v.y); }",
    "vec3 hueRotate(vec3 c, float a){",
    "  const vec3 k = vec3(0.57735);",
    "  float cs = cos(a), sn = sin(a);",
    "  return c*cs + cross(k,c)*sn + k*dot(k,c)*(1.0-cs); }",
    "vec4 blur(vec2 uv, float r){",
    "  vec4 s = vec4(0.0);",
    "  for (int i = 0; i < 12; i++) {",
    "    float a = float(i)*0.5236; float rr = r*(0.5+0.5*mod(float(i),2.0));",
    "    s += tex(uv + unasp(vec2(cos(a),sin(a)))*rr); }",
    "  return s/12.0; }",
    // every tap ripples, in every mode: the displacement and the gloss it adds
    "vec2 ripple(vec2 uv, out float gloss){",
    "  vec2 disp = vec2(0.0); gloss = 0.0;",
    "  for (int i = 0; i < 8; i++) {",
    "    vec4 rp = uRip[i]; if (rp.z < 0.0) continue;",
    "    float dt = uTime - rp.z; if (dt < 0.0 || dt > 3.5) continue;",
    "    vec2 o = asp(uv - rp.xy); float dist = length(o);",
    "    float front = dt*0.38;",
    "    float env = exp(-dt*1.0)*exp(-dist*3.2)*smoothstep(front+0.07, front-0.07, dist);",
    "    float w = sin(dist*(6.2831853/uPeriod) - dt*10.0)*env*rp.w;",
    "    disp += unasp(normalize(o+1e-5))*w*0.028*uStrength; gloss += w; }",
    "  return disp; }",
    "void main(){",
    "  vec2 uv = vUv;",
    "  float gloss; vec2 rd = ripple(uv, gloss);",
    "  vec2 d2 = asp(uv - uP); float d = length(d2);",
    "  float hold = min(uHold, 4.0);",
    "  float r = uRadius*uAmt;",
    "  float k = uAmt*smoothstep(uRadius, 0.0, d);",
    "  vec4 col;",
    "  if (uMode == 0) {",
    "    float rr = uAmt*(uRadius*0.65 + uRadius*0.4*min(hold,2.0));",
    "    if (d < rr) {",
    "      float ang = atan(d2.y, d2.x) + hold*uSpeed;",
    "      float seg = 6.2831853/max(2.0, uCount);",
    "      ang = mod(ang, seg); if (uFlag > 0.5 && ang > seg*0.5) ang = seg - ang;",
    "      vec2 q = uP + unasp(vec2(cos(ang), sin(ang))*d);",
    "      col = mix(tex(q + rd), tex(uv + rd), smoothstep(rr-0.02, rr, d));",
    "    } else col = tex(uv + rd);",
    "  } else if (uMode == 1) {",
    "    if (d < r) {",
    "      float q = 1.0 - (d/r)*(d/r);",
    "      float mag = 1.0 + (uStrength + 0.9*uDown + 0.3*min(hold,1.0))*q;",
    "      vec2 dir = uv - uP;",
    "      col = vec4(tex(uP + dir/(mag*1.03) + rd).r, tex(uP + dir/mag + rd).g, tex(uP + dir/(mag*0.97) + rd).b, 1.0);",
    "      col.rgb *= 1.0 - 0.35*smoothstep(r*0.8, r, d);",
    "      col = mix(col, tex(uv + rd), smoothstep(r-0.006, r, d));",
    "    } else col = tex(uv + rd);",
    "  } else if (uMode == 2) {",
    "    float stir = k;",
    "    vec2 disp = rd + (vec2(noise(uv*22.0 + uTime*1.9), noise(uv*22.0 + 9.0 - uTime*1.4)) - 0.5)*0.03*stir*uStrength;",
    "    col = tex(uv + disp);",
    "    col.rgb += gloss*0.45 + stir*0.08*(noise(uv*40.0 + uTime*2.5) - 0.5);",
    "  } else if (uMode == 3) {",
    "    float kk = k*k; float a = uDir*kk*(uStrength + 0.5*hold + 1.6*uDown);",
    "    float c = cos(a), s = sin(a);",
    "    col = tex(uP + unasp(mat2(c,-s,s,c)*d2) + rd);",
    "  } else if (uMode == 4) {",
    "    vec2 dir = unasp(normalize(d2+1e-5))*k*(0.016 + 0.012*uDown)*uStrength;",
    "    col = vec4(tex(uv+dir+rd).r, tex(uv+rd).g, tex(uv-dir+rd).b, 1.0);",
    "  } else if (uMode == 5) {",
    "    float kk = uAmt*smoothstep(uRadius + 0.04*hold, uRadius*0.4, d);",
    "    col = tex(uv + rd);",
    "    vec3 neg = 1.0 - col.rgb; neg = mix(neg, vec3(dot(neg, vec3(0.3,0.59,0.11))), 0.35)*vec3(1.05,1.0,0.9);",
    "    col.rgb = mix(col.rgb, neg, kk);",
    "  } else if (uMode == 6) {",
    "    vec2 w = vec2(noise(vec2(uv.x*22.0, uv.y*16.0 - uTime*2.6)) - 0.5, noise(vec2(uv.x*18.0 + 7.0, uv.y*14.0 - uTime*3.2)) - 0.5);",
    "    col = tex(uv + w*0.03*k*uStrength + rd);",
    "    col.rgb += 0.08*k*(noise(uv*30.0 - uTime*3.5) - 0.5)*uStrength;",
    "  } else if (uMode == 7) {",
    "    vec2 g = vec2(uCount*uAspect, uCount);",
    "    vec2 cell = floor(uv*g); vec2 f = fract(uv*g);",
    "    vec2 c = vec2(hash(cell), hash(cell+3.1))*0.6 + 0.2;",
    "    float rad = 0.2 + 0.24*hash(cell+7.7);",
    "    float show = step(hash(cell+1.3), 0.35 + 0.6*k)*k;",
    "    float dd = length(asp((f-c)/g))*uCount;",
    "    col = tex(uv + rd);",
    "    if (dd < rad && show > 0.0) {",
    "      float q = 1.0 - (dd/rad)*(dd/rad);",
    "      vec2 dir = uv - (cell+c)/g;",
    "      col = mix(col, tex(uv - dir*1.2*q*uStrength + rd), show);",
    "      col.rgb += show*0.18*q*(1.0 - smoothstep(0.0, 0.5, dd/rad));",
    "      col.rgb *= 1.0 - show*0.3*smoothstep(rad*0.7, rad, dd); }",
    "  } else if (uMode == 8) {",
    "    float colId = floor(uv.x*uCount*uAspect);",
    "    float h = hash(vec2(colId, 2.0));",
    "    float near = uAmt*smoothstep(uRadius, 0.0, abs(uv.x - uP.x)*uAspect);",
    "    float below = smoothstep(uP.y + 0.05, uP.y - 0.25, uv.y);",
    "    float drip = near*below*(0.05 + 0.1*hold)*(0.3 + h)*uStrength;",
    "    col = tex(vec2(uv.x, uv.y + drip) + rd);",
    "    col.rgb *= 1.0 - 0.6*drip*h;",
    "  } else if (uMode == 9) {",
    "    float kk = uAmt*smoothstep(uRadius*0.6, uRadius*1.4, d);",
    "    col = blur(uv + rd, 0.014*kk*uStrength);",
    "    col.rgb *= 1.0 - 0.12*kk;",
    "  } else if (uMode == 10) {",
    "    float pull = k*uStrength*(0.6 + 0.2*hold + 0.4*uDown);",
    "    vec2 q = uP + (uv - uP)*(1.0 - pull*0.85);",
    "    col = tex(q + rd);",
    "    col.rgb *= 1.0 - 0.5*pull*pull;",
    "  } else if (uMode == 11) {",
    "    col = tex(uv + rd);",
    "    col.rgb = hueRotate(col.rgb, k*uStrength*(1.5 + 0.8*hold + 2.0*uDown));",
    "  } else if (uMode == 12) {",
    "    float light = exp(-(d*d)/(uRadius*uRadius*0.5));",
    "    col = tex(uv + rd);",
    "    col.rgb *= mix(1.0, mix(0.28, 1.35, light), uAmt*uStrength);",
    "  } else if (uMode == 13) {",
    "    vec2 n = normalize(uAxis);",
    "    float s = dot(asp(uv - uP), n);",
    "    vec2 m = uv - unasp(2.0*s*n);",
    "    col = mix(tex(uv + rd), tex(m + rd), uAmt*step(0.0, s));",
    "    col.rgb *= 1.0 - 0.25*uAmt*(1.0 - smoothstep(0.0, 0.01, abs(s)));",
    "  } else if (uMode == 14) {",
    "    vec2 n = normalize(uAxis); vec2 t = vec2(-n.y, n.x);",
    "    float idx = floor(dot(asp(uv), n)/uPeriod);",
    "    float kk = uAmt*smoothstep(uRadius, 0.0, d)*uStrength;",
    "    vec2 q = uv + unasp(t*(hash(vec2(idx, 5.0)) - 0.5)*0.35*kk);",
    "    col = tex(q + rd);",
    "    col.rgb *= 1.0 - 0.12*kk*step(0.92, fract(dot(asp(uv), n)/uPeriod));",
    "  } else if (uMode == 15) {",
    "    vec2 g = vec2(1.0/(uPeriod), 1.0/(uPeriod))*vec2(1.0, 1.0);",
    "    vec2 cell = floor(asp(uv)*g); vec2 f = fract(asp(uv)*g);",
    "    float h = hash(cell + 11.0);",
    "    vec2 ff = h < 0.5 ? vec2(1.0 - f.x, f.y) : vec2(f.x, 1.0 - f.y);",
    "    vec2 q = unasp((cell + ff)/g);",
    "    float kk = uAmt*smoothstep(uRadius, uRadius*0.3, d)*step(hash(cell+2.0), 0.3 + 0.7*k);",
    "    col = mix(tex(uv + rd), tex(q + rd), kk*uStrength);",
    "  } else if (uMode == 16) {",
    "    float below = smoothstep(uHorizon + 0.01, uHorizon - 0.01, uv.y);",
    "    vec2 m = vec2(uv.x, 2.0*uHorizon - uv.y);",
    "    float depth = (uHorizon - uv.y);",
    "    vec2 wob = (vec2(noise(vec2(uv.x*30.0, uv.y*60.0 - uTime*1.2)), noise(vec2(uv.x*24.0 + 5.0, uv.y*50.0 - uTime*1.6))) - 0.5)*0.02*(0.5 + k);",
    "    vec4 water = tex(m + wob + rd*2.0);",
    "    water.rgb = mix(water.rgb, water.rgb*vec3(0.75, 0.85, 1.0), 0.5)*(0.85 - 0.25*depth) + gloss*0.5;",
    "    col = mix(tex(uv + rd), water, uAmt*below*uStrength);",
    "  } else if (uMode == 17) {",
    "    vec2 n = normalize(uAxis); vec2 t = vec2(-n.y, n.x);",
    "    float s = dot(asp(uv - uLine), n);",
    "    float side = s > 0.0 ? 1.0 : -1.0;",
    "    float gap = uAmt*smoothstep(uRadius, 0.0, d)*uStrength*(0.05 + 0.03*hold + 0.06*uDown);",
    "    vec2 q = uv - unasp(n*side*gap*0.5 + t*side*gap*0.6);",
    "    float inGap = step(abs(s), gap*0.5);",
    "    col = tex(q + rd)*(1.0 - inGap) + vec4(0.02, 0.02, 0.025, 1.0)*inGap;",
    "  } else if (uMode == 18) {",
    "    float a = uDir*uAmt*uStrength*(0.6 + 0.2*hold + 0.5*uDown)*log(1.0 + d*6.0)*smoothstep(uRadius*1.4, 0.0, d);",
    "    float c = cos(a), s = sin(a);",
    "    col = tex(uP + unasp(mat2(c,-s,s,c)*d2) + rd);",
    "  } else {",
    "    vec4 s = vec4(0.0);",
    "    float len = k*uStrength*0.35;",
    "    for (int i = 0; i < 10; i++) { float q = float(i)/9.0; s += tex(uP + (uv - uP)*(1.0 - len*q) + rd); }",
    "    col = s/10.0;",
    "    col.rgb += 0.06*k;",
    "  }",
    "  gl_FragColor = vec4(col.rgb, 1.0);",
    "}"].join("\n");

  // ---- the overlay -----------------------------------------------------------------------------
  var S = null;        // the one renderer: canvas, gl, program, uniforms, texture
  var att = null;      // { img, container, record, effect, params, assigned }
  var hand = { p: { x: 0.5, y: 0.5 }, inside: false, down: false, amt: 0, enteredAt: 0, rip: [] };
  var t0 = (typeof performance !== "undefined" ? performance.now() : Date.now());
  var raf = 0, lastErr = null, frames = 0;
  var reduced = false;
  try { reduced = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches); } catch (e) {}
  function now() { return (typeof performance !== "undefined" ? performance.now() : Date.now()); }

  var refused = false;   // a device that cannot carry this layer is asked once, never on every attach
  var making = false;
  function scheduleMake() {
    if (S || refused || making) return;
    making = true;
    setTimeout(function () {
      making = false;
      if (!make() || !att) return;
      if (S.canvas.parentNode !== att.container) att.container.appendChild(S.canvas);
      place();
      if (hand.inside || hand.rip.length) wake();
    }, 0);
  }
  function make() {
    if (S) return S;
    if (refused) return null;
    var canvas = document.createElement("canvas");
    canvas.setAttribute("aria-hidden", "true");
    canvas.style.cssText = "position:absolute;left:0;top:0;width:0;height:0;pointer-events:none;" +
      "visibility:hidden;z-index:3;display:block;";
    var gl = canvas.getContext("webgl", { antialias: false, preserveDrawingBuffer: false, alpha: false })
          || canvas.getContext("experimental-webgl");
    if (!gl) { lastErr = "no webgl"; refused = true; return null; }
    // A software rasteriser draws a full-frame shader in whole seconds and starves everything else
    // on the page — the walk's own hand included. Such a device gets the still picture and nothing
    // here; the picture is never worse for it.
    try {
      var dbg = gl.getExtension("WEBGL_debug_renderer_info");
      var renderer = dbg ? String(gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL)) : "";
      if (/swiftshader|llvmpipe|softpipe|software|mesa offscreen/i.test(renderer)) {
        lastErr = "software renderer: " + renderer; refused = true; return null;
      }
    } catch (e) {}
    function sh(type, src) {
      var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      return s;
    }
    var prog = gl.createProgram();
    try {
      gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS));
      gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS));
    } catch (e) { lastErr = String(e && e.message || e); refused = true; return null; }
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { lastErr = gl.getProgramInfoLog(prog); refused = true; return null; }
    gl.useProgram(prog);
    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var aPos = gl.getAttribLocation(prog, "aPos");
    gl.enableVertexAttribArray(aPos);
    gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);
    var U = {};
    ["uTex", "uCover", "uAspect", "uP", "uAmt", "uHold", "uTime", "uDown", "uMode", "uRip",
     "uRadius", "uStrength", "uCount", "uFlag", "uSpeed", "uAxis", "uPeriod", "uHorizon", "uLine", "uDir"]
      .forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });
    var tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    canvas.addEventListener("webglcontextlost", function (e) { e.preventDefault(); S = null; att = null; }, false);
    S = { canvas: canvas, gl: gl, U: U, tex: tex, texImg: null, iw: 1, ih: 1, density: 1, slow: 0 };
    return S;
  }

  // The canvas sits over the picture's own box inside its container, whatever the screen or the
  // orientation: the box is measured, never assumed, and measured again on every resize.
  function place() {
    if (!S || !att) return;
    var img = att.img, c = att.container;
    var ir = img.getBoundingClientRect(), cr = c.getBoundingClientRect();
    var left = ir.left - cr.left + c.scrollLeft, top = ir.top - cr.top + c.scrollTop;
    var cs = S.canvas.style;
    cs.left = left + "px"; cs.top = top + "px"; cs.width = ir.width + "px"; cs.height = ir.height + "px";
    try { cs.borderRadius = getComputedStyle(img).borderRadius; } catch (e) {}
    var dpr = Math.min(window.devicePixelRatio || 1, 2) * S.density;
    var w = Math.max(1, Math.round(ir.width * dpr)), h = Math.max(1, Math.round(ir.height * dpr));
    // a phone's budget: no more than about 2.6 million pixels a frame, whatever its density
    var cap = 2600000;
    if (w * h > cap) { var f = Math.sqrt(cap / (w * h)); w = Math.max(1, Math.round(w * f)); h = Math.max(1, Math.round(h * f)); }
    if (S.canvas.width !== w || S.canvas.height !== h) {
      S.canvas.width = w; S.canvas.height = h;
      S.gl.viewport(0, 0, w, h);
    }
  }

  function upload(img) {
    if (!S) return false;
    if (!img.complete || !img.naturalWidth) return false;
    if (S.texImg === img) return true;
    var gl = S.gl;
    gl.bindTexture(gl.TEXTURE_2D, S.tex);
    try { gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, img); }
    catch (e) { lastErr = "texture: " + (e && e.message || e); return false; }
    S.texImg = img; S.iw = img.naturalWidth; S.ih = img.naturalHeight;
    return true;
  }

  function draw() {
    raf = 0;
    if (!S || !att) return;
    if (!upload(att.img)) { S.canvas.style.visibility = "hidden"; return; }
    // A picture the page has hidden — held back under a crossing, covered by a closer look — is not
    // one to draw over: the overlay goes with it and the loop stops until the hand comes back.
    try {
      var cs = getComputedStyle(att.img);
      if (cs.visibility === "hidden" || cs.display === "none" || +cs.opacity === 0) {
        S.canvas.style.visibility = "hidden"; hand.inside = false; hand.down = false; hand.amt = 0; return;
      }
    } catch (e) {}
    place();
    var gl = S.gl, U = S.U, p = att.params;
    var t = (now() - t0) / 1000;
    var target = hand.inside ? 1 : 0;
    hand.amt += (target - hand.amt) * (hand.inside ? 0.16 : 0.09);
    if (Math.abs(target - hand.amt) < 0.003) hand.amt = target;
    var hold = hand.inside ? (now() - hand.enteredAt) / 1000 : 0;
    var aspect = S.canvas.width / S.canvas.height;
    var ia = S.iw / S.ih;
    var cover = ia > aspect ? [aspect / ia, 1] : [1, ia / aspect];
    gl.uniform1i(U.uTex, 0);
    gl.uniform2f(U.uCover, cover[0], cover[1]);
    gl.uniform1f(U.uAspect, aspect);
    gl.uniform2f(U.uP, hand.p.x, hand.p.y);
    gl.uniform1f(U.uAmt, hand.amt);
    gl.uniform1f(U.uHold, hold);
    gl.uniform1f(U.uTime, t);
    gl.uniform1f(U.uDown, hand.down ? 1 : 0);
    gl.uniform1i(U.uMode, att.effect.mode);
    gl.uniform1f(U.uRadius, num(p.radius, 0.25));
    gl.uniform1f(U.uStrength, num(p.strength, 1));
    gl.uniform1f(U.uCount, num(p.count, 6));
    gl.uniform1f(U.uFlag, num(p.flag, 1));
    gl.uniform1f(U.uSpeed, num(p.speed, 0.15));
    var ax = p.axis || [1, 0];
    gl.uniform2f(U.uAxis, num(ax[0], 1), num(ax[1], 0));
    gl.uniform1f(U.uPeriod, num(p.period, 0.09));
    gl.uniform1f(U.uHorizon, num(p.horizon, 0.5));
    var ln = p.line || [0.5, 0.5];
    gl.uniform2f(U.uLine, num(ln[0], 0.5), num(ln[1], 0.5));
    gl.uniform1f(U.uDir, num(p.dir, 1));
    var rip = new Float32Array(32);
    for (var i = 0; i < 8; i++) {
      var r = hand.rip[i];
      rip[i * 4] = r ? r.x : 0; rip[i * 4 + 1] = r ? r.y : 0;
      rip[i * 4 + 2] = r ? r.t : -1; rip[i * 4 + 3] = r ? r.s : 0;
    }
    gl.uniform4fv(U.uRip, rip);
    var before = now();
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    frames += 1;
    // THE DEVICE SETS ITS OWN DENSITY. A frame that takes longer than two screen refreshes is a
    // frame the eye reads as a stutter; three in a row halve the pixel density, and a device that
    // stutters even at a quarter density gets the still picture. Measured on the visitor's own
    // device, never on a build host.
    if (now() - before > 34) {
      if (++S.slow >= 3) {
        S.slow = 0;
        if (S.density > 0.26) S.density *= 0.5;
        else { lastErr = "too slow at quarter density"; refused = true; detach(); return; }
      }
    } else S.slow = 0;
    S.canvas.style.visibility = "visible";
    hand.rip = hand.rip.filter(function (rr) { return t - rr.t < 3.5; });
    var alive = hand.inside || hand.amt > 0 || hand.rip.length > 0;
    if (alive) raf = requestAnimationFrame(draw);
    else S.canvas.style.visibility = "hidden";
  }
  function wake() { if (S && att && !raf) raf = requestAnimationFrame(draw); }

  // ---- the hand, read off the window: passive, capture, never owning navigation ----------------
  function over(e) {
    if (!att) return false;
    var el = e.target;
    if (el === att.img || (S && el === S.canvas)) return true;
    if (el && el.closest) {
      var w = el.closest(TARGET_SEL);
      if (w === att.img) return true;
      // another work is under the pointer: the walk re-attaches on its own roads, not here
      if (w && w !== att.img) return false;
    }
    // Anything else — a caption, a plaque, the frame itself, a finger held with capture on the
    // element it started on — is judged by the picture's own box, which is what the hand is over.
    var r = att.img.getBoundingClientRect();
    return e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
  }
  function pos(e) {
    var r = att.img.getBoundingClientRect();
    return { x: clamp((e.clientX - r.left) / Math.max(1, r.width), 0, 1),
             y: clamp(1 - (e.clientY - r.top) / Math.max(1, r.height), 0, 1) };
  }
  function enter(e) {
    if (!hand.inside) {
      hand.inside = true; hand.enteredAt = now();
      if (att && !att.record && hostRecordFor && att.workId != null) {
        var rec = null;
        try { rec = hostRecordFor(att.workId); } catch (err) { rec = null; }
        if (rec) reassign(rec);
      }
    }
    hand.p = pos(e);
    wake();
  }
  // The record landed after the attach: the same choice attach would have made, on the live hand.
  function reassign(rec) {
    var assigned = assign(rec);
    var effect = att.override ? (BY_ID[att.override] || BY_ID[assigned.effect]) : BY_ID[assigned.effect];
    var params = {};
    Object.keys(effect.params).forEach(function (k) { params[k] = effect.params[k]; });
    assigned.ranked.forEach(function (row) {
      if (row.effect === effect.id) Object.keys(row.params).forEach(function (k) { params[k] = row.params[k]; });
    });
    att.record = rec; att.effect = effect; att.params = params; att.assigned = assigned;
  }
  function leave() { hand.inside = false; hand.down = false; wake(); }
  function onMove(e) {
    if (!att) return;
    if (over(e)) enter(e); else if (hand.inside && !hand.down) leave();
  }
  function onDown(e) {
    if (!att || !over(e)) return;
    enter(e);
    hand.down = true;
    var t = (now() - t0) / 1000;
    hand.rip.push({ x: hand.p.x, y: hand.p.y, t: t, s: 1 });
    if (hand.rip.length > 8) hand.rip.shift();
    wake();
  }
  function onUp(e) {
    if (!att) return;
    hand.down = false;
    if (e.pointerType === "touch") leave();   // a finger has no hover: lifting it is leaving
    else if (!over(e)) leave();
    wake();
  }
  var listening = false;
  function listen() {
    if (listening) return;
    listening = true;
    var opt = { capture: true, passive: true };
    addEventListener("pointermove", onMove, opt);
    addEventListener("pointerdown", onDown, opt);
    addEventListener("pointerup", onUp, opt);
    addEventListener("pointercancel", onUp, opt);
    addEventListener("resize", function () { if (att) { place(); wake(); } });
    addEventListener("orientationchange", function () { setTimeout(function () { if (att) { place(); wake(); } }, 120); });
    addEventListener("scroll", function () { if (att && hand.amt > 0) place(); }, { capture: true, passive: true });
  }

  // ---- the door --------------------------------------------------------------------------------
  // attach(img, record, opts): lay the overlay over this picture, with the effect the record assigns
  // (or opts.effect, by id, to override — the lab's own road). opts.container: the positioned box
  // the canvas lives in; the walk's own frame by default.
  function attach(img, record, opts) {
    opts = opts || {};
    if (!img || reduced || refused) return false;
    var container = opts.container || (img.closest && img.closest(".exh-frame")) || img.parentNode;
    if (!container) return false;
    // THE CONTEXT IS NEVER RAISED INSIDE A POINTER HANDLER. Creating a WebGL context and compiling
    // the shader takes real time, and attach is called from the walk's own pointerover/pointerdown
    // road; doing that work there delays the hand's first frame (measured 2026-09-09: the hand's
    // press-and-drag row read a stale transform once in three runs). The renderer is raised on the
    // next turn of the event loop, and the overlay begins with the first hand event after it stands.
    if (!S) { scheduleMake(); }
    var assigned = assign(record);
    var effect = BY_ID[opts.effect] || BY_ID[assigned.effect];
    var params = {};
    Object.keys(effect.params).forEach(function (k) { params[k] = effect.params[k]; });
    if (!opts.effect || opts.effect === assigned.effect) {
      Object.keys(assigned.params).forEach(function (k) { params[k] = assigned.params[k]; });
    } else {
      // an override still takes the record's own numbers for that effect, where a rule set any
      assigned.ranked.forEach(function (row) {
        if (row.effect === effect.id) Object.keys(row.params).forEach(function (k) { params[k] = row.params[k]; });
      });
    }
    if (opts.params) Object.keys(opts.params).forEach(function (k) { params[k] = opts.params[k]; });
    var same = att && att.img === img;
    var workId = opts.workId != null ? opts.workId : (record && record.id != null ? record.id
                 : (img.closest && img.closest(".exh-frame") && img.closest(".exh-frame").dataset.id) || null);
    att = { img: img, container: container, record: record || null, workId: workId, override: opts.effect || null,
            effect: effect, params: params, assigned: assigned };
    if (S && S.canvas.parentNode !== container) container.appendChild(S.canvas);
    if (!same) { hand.inside = false; hand.down = false; hand.amt = 0; hand.rip = []; if (S) S.canvas.style.visibility = "hidden"; }
    if (!img.complete || !img.naturalWidth) img.addEventListener("load", function () { wake(); }, { once: true });
    listen();
    if (S) place();
    return true;
  }
  function detach() {
    if (!att) return;
    att = null;
    hand.inside = false; hand.down = false; hand.amt = 0; hand.rip = [];
    if (raf) { cancelAnimationFrame(raf); raf = 0; }
    if (S) S.canvas.style.visibility = "hidden";
  }
  function report() {
    return {
      attached: att ? { effect: att.effect.id, params: att.params, hasRecord: !!att.record, why: att.assigned.why } : null,
      hand: { inside: hand.inside, down: hand.down, amt: +hand.amt.toFixed(3), ripples: hand.rip.length },
      frames: frames, error: lastErr, reduced: reduced,
      canvas: S ? { w: S.canvas.width, h: S.canvas.height, visible: S.canvas.style.visibility === "visible" } : null,
    };
  }

  try { window.__@@NS@@PassTouchReport = report; } catch (e) {}
  join({ attach: attach, detach: detach, assign: assign, report: report, host: host,
         effects: EFFECTS.map(function (e) { return { id: e.id, title: e.title, note: e.note, params: e.params }; }),
         rules: RULES.map(function (r) { return { effect: r.effect, text: r.text }; }) });
})();
