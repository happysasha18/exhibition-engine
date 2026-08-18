/*!pass-inst-grid-colour.js*/
// One instrument, travelling as its own file (PASS-API-V1 §7/§8, his word of 2026-08-14 08:39: the
// engine knows no effect name and loads version-pinned opaque effect files).
//
// WHAT THIS FILE IS. One instrument and the mathematics it draws by: a name, a manifest declaring
// its passes, its uniforms with the source each is bound from, its handles and its doors, and the
// pure functions that answer the numbers of one frame. The manifest's declared names are the whole
// interface — the host binds by them and refuses at registration anything it cannot supply.
//
// WHAT THIS FILE MAY NOT DO. It reads no wall clock, holds no listener, creates no WebGL context,
// loads no picture and touches no DOM (§1.2's fence). The host owns the canvas, the context, the
// frame loop, the clock, the camera and the transaction; the instrument owns the picture.
//
// OWNERSHIP. This instrument was carried over from lab/effects/grid-colour.js. The artistic
// instruments and their manifests belong to tlvphotos, which builds these files from its own
// sources; the engine's copies are what ships until that handover lands. The contract this file
// answers to is §7 and §8 of docs/design/PASS-API-V1.md, and the record that names it is the site's
// own `pass` block.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE GRID-AND-COLOUR INSTRUMENT (§8) — lab/effects/grid-colour.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The photograph is cut by a plain grid of its own — strips stacked across
  // it, annuli about its middle, a chequer of tiles, or the areas of one colour that are actually in
  // the picture — and the pieces walk out of the frame along their own lines, neighbours to opposite
  // ends, losing their colour as they go so that the last of a piece to leave is grey. Behind them
  // the second photograph is already coming in the same way, cut by ITS own grid, arriving grey and
  // filling with colour a beat before its shapes land. Between the two, for as long as the passage
  // lasts, the ground shows through the gaps the cut has opened. The count and the angle of the cut
  // travel with the hand from the first work's measured structure to the second's, so the grid the
  // eye reads at the start belongs to the work that is leaving and the one it reads at the end to
  // the work that has arrived.
  //
  // WHY IT STANDS HERE. The charter's own reading of this module: THE GRID IS A BRIDGE, NOT A
  // DECORATION (lab/CROSSING-BRIEF.md, The model — the bridge computes both structures). The module
  // is the only one in the lab that is handed BOTH works' measured grids and walks between them, and
  // it is the only one that cuts on a work's own COLOUR as well as on its geometry. Its contract row
  // in lab/data/module-contract.json carries it at level CELL+LIGHT-COLOUR with both doors written
  // out in words, and this file answers that row.
  //
  // ------------------------------------------------------------------------------------------------
  // A CANVAS 2D MODULE, AND THE SHAPE IT WAS GIVEN
  // ------------------------------------------------------------------------------------------------
  // The module holds a 2D canvas and draws ONE work: it builds the picture and its grey twin once,
  // and every frame it walks the pieces of the cut and stamps the picture into each of them through
  // a clip path. There is no shader anywhere in it, and it carries one work rather than a pair.
  //
  // THE SHAPE. Every piece of every cut here travels by a RIGID MOTION of the picture — a
  // translation along the piece's own line for a strip, a tile and a colour band, a similarity about
  // the frame's own middle for a ring — and a rigid motion is invertible. So the shader reads the
  // module backwards: for one point of the frame it asks which piece of the departing work would
  // have landed there and, where that piece has already gone, which piece of the ARRIVING work is
  // arriving into it. The piece a point belongs to is SOLVED rather than searched for — the strip
  // and the tile are found from the point's own coordinate along the cut's axis, the colour band
  // from the colour standing at the point it came from — and only the rings walk a bounded loop,
  // because a ring's own reach is read off its own radius and no two rings travel alike.
  //
  // WHAT THE REIMPLEMENTATION COST, stated plainly and measured in this port's own suite:
  //   · THE MODULE'S GREY TWIN is a whole second canvas, drawn once at build and laid over the
  //     picture at the piece's own opacity. Here the grey is the same luminance formula
  //     (0.2126/0.7152/0.0722) taken on the sampled texel, so no second surface exists. The two
  //     answer the same number.
  //   · THE MASK GRID OF THE COLOUR BANDS. The module reads the file down to 128 cells on its long
  //     side, assigns every cell to the nearest palette colour and builds each band as a canvas of
  //     whole-pixel rectangles. A shader has no build step, so the band a point belongs to is
  //     decided at the point itself, with no quantisation — the pieces have the same shape at the
  //     scale a person sees and a cleaner edge at the scale of one point.
  //   · THE HAIRLINE OVERLAP. The module grows every piece by one pixel at each edge so no seam
  //     opens between two clip paths, and draws the pieces in order so the later one wins. Both are
  //     carried: the inverse map tests the neighbouring piece first and takes it where it stands.
  //   · THE PIECES A SCORE CANNOT SEE. `pieces()` — the module's own table of the cut, read rather
  //     than shown — has no counterpart, because the host publishes no such channel. What it carried
  //     is published instead on the diagnostic surface `values` answers with, piece by piece for the
  //     two ends of each layer.
  //
  // ------------------------------------------------------------------------------------------------
  // A ONE-WORK MODULE PLAYED AS A CROSSING: TWO LAYERS FOLDED INTO ONE PASS
  // ------------------------------------------------------------------------------------------------
  // lab/data/module-contract.json records `grid-colour` as `needsTwoWorks: false`. A crossing plays
  // it as TWO layers — the module's own `flow` says which: the departing work's layer runs `out` and
  // walks its handle up, the arriving work's runs `in` and walks its handle DOWN, so at the near
  // door the first stands whole and the second is wholly outside the frame, and at the far door the
  // other way about. That is the two-layer road the module was built for, and this instrument is
  // that road folded into one pass:
  //
  //     layer A — the departing work, flow `out`, its own hand = `mix`
  //     layer B — the arriving work,  flow `in`,  its own hand = 1 − `mix`
  //
  // and the frame is layer A where a piece of A still stands, layer B where a piece of B has
  // arrived, and BARE where neither does — which is the coverage this instrument publishes.
  //
  // ONE COUNT AND ONE ANGLE SERVE BOTH LAYERS, and that is the bridge rather than a saving. The
  // module walks the count from `countFrom` (the departing work's own measured grid) to `countTo`
  // (the arriving work's) across its own handle. Handed to the arriving layer with its two ends
  // swapped — which is what a crossing does, since that layer's near door is the OTHER work's
  // structure — and read on that layer's own downward hand, the arriving layer's count comes out
  // exactly the departing layer's at every value of `mix`. So the two grids are one grid, walking
  // from the first work's structure to the second's, and the doors stand where the contract's own
  // words put them.
  //
  // WHAT `flow` COST. It does not cross as a handle a score can drive, and this is the one handle of
  // the module's own two that does not. In a crossing the flow is the PAIR'S OWN ORDER — the
  // departing work leaves, the arriving one arrives — so it is spent by this instrument rather than
  // published: a score that could set both layers to one flow would break both doors at once. It is
  // published on the manifest as an applied fact instead, and this port's report names it.
  function gridColourInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER — the module's own clip-and-stamp read backwards
    // ----------------------------------------------------------------------------------------------
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",             // the work that is leaving
      "uniform sampler2D uB;",             // the work that is arriving
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // EACH LAYER'S CUT: which of the four kinds, where its own dial stands, which sense its pieces
      // take along their lines, and how much of the dial the departures are spread over by area.
      "uniform vec4 uCutA;",
      "uniform vec4 uCutB;",
      // EACH LAYER'S GRID: the step between two pieces in points of the buffer, the cut's own axis as
      // a cosine and a sine, and the count the step was taken from.
      "uniform vec4 uGridA;",
      "uniform vec4 uGridB;",
      // THE PICTURE UNDER THAT GRID: how far it reaches across the axis the pieces stack on, how far
      // along the line they travel, the reach of that line, and the picture's own radius.
      "uniform vec4 uSpanA;",
      "uniform vec4 uSpanB;",
      // THE TWO VOICES, per layer: how much palette the pieces hold, and where the light stands.
      "uniform vec2 uVoiceA;",
      "uniform vec2 uVoiceB;",
      // The judges' channel: the cut map as colour.
      "uniform float uMask;",
      // ---- the module's own numbers, carried digit for digit -------------------------------------
      // HOW MANY COLOURS MAKE THE BANDS CUT (grid-colour.js:109, BAND_COUNT). Five, because that is
      // what a work's measured palette carries.
      "const int BANDS = 5;",
      // The luminance the grey twin is written at (grid-colour.js:278).
      "const vec3 LUMA = vec3(0.2126, 0.7152, 0.0722);",

      "vec2 into(vec2 p, vec4 f){ return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992); }",
      "float ovl(float a0, float a1, float b0, float b1){",
      "  float lo = max(a0, b0), hi = min(a1, b1);",
      "  return hi > lo ? hi - lo : 0.0;",
      "}",
      // WHERE A PIECE STANDS ON THE DIAL, given its own area (grid-colour.js localAt). The largest
      // piece waits the whole `stagger` share of the handle before it starts and every piece still
      // arrives at the far end by dial 1, so the doors are the doors they were.
      "float localAt(float u, float area, float areaMax, float s){",
      "  float off = (areaMax > 0.0 ? clamp(area / areaMax, 0.0, 1.0) : 0.0) * s;",
      "  return clamp((u - off) / (1.0 - s), 0.0, 1.0);",
      "}",
      // The hue of a colour as a turn of the circle — the angle a colour band leaves along
      // (grid-colour.js hueOf), carried line for line.
      "float hueOf(vec3 c){",
      "  float mx = max(c.r, max(c.g, c.b)), mn = min(c.r, min(c.g, c.b));",
      "  float d = mx - mn;",
      "  if (d <= 0.0) return 0.0;",
      "  if (mx == c.r) return (((c.g - c.b) / d) + (c.g < c.b ? 6.0 : 0.0)) / 6.0;",
      "  if (mx == c.g) return (((c.b - c.r) / d) + 2.0) / 6.0;",
      "  return (((c.r - c.g) / d) + 4.0) / 6.0;",
      "}",
      // THE WORK'S OWN FIVE COLOURS, read off the work itself. The module measures them on a grid of
      // the file quantised to a colour cube and takes the fullest cells (grid-colour.js
      // measuredPalette, the path a layer handed no palette takes); a shader has no build step and no
      // histogram, so the five are read at five places of the file, each one the mean of a small
      // cross so a single texel cannot decide a whole band's colour — the same guard the unfold's own
      // world tone is read with.
      "vec3 palAt(sampler2D tex, vec2 c){",
      "  return 0.25 * (texture2D(tex, c + vec2(0.02, 0.0)).rgb",
      "               + texture2D(tex, c - vec2(0.02, 0.0)).rgb",
      "               + texture2D(tex, c + vec2(0.0, 0.02)).rgb",
      "               + texture2D(tex, c - vec2(0.0, 0.02)).rgb);",
      "}",
      // WHICH OF THE FIVE A COLOUR BELONGS TO: the nearest of them in the colour cube, which is the
      // module's own assignment (grid-colour.js bandsBuild, the squared distance walk).
      "int nearestOf(vec3 c, vec3 p0, vec3 p1, vec3 p2, vec3 p3, vec3 p4){",
      "  int best = 0; float bd = dot(c - p0, c - p0);",
      "  float d1 = dot(c - p1, c - p1); if (d1 < bd) { bd = d1; best = 1; }",
      "  float d2 = dot(c - p2, c - p2); if (d2 < bd) { bd = d2; best = 2; }",
      "  float d3 = dot(c - p3, c - p3); if (d3 < bd) { bd = d3; best = 3; }",
      "  float d4 = dot(c - p4, c - p4); if (d4 < bd) { bd = d4; best = 4; }",
      "  return best;",
      "}",
      // ONE LAYER, READ BACKWARDS. `p` is a point of the frame in points of the buffer, counted from
      // the frame's own middle with y running down, which is the coordinate the module's own canvas
      // is written in. The answer is whether a piece of this layer stands at that point and, where it
      // does, the point of the STANDING picture it carries — everything else follows from that one
      // pair of numbers.
      "bool layerAt(sampler2D tex, vec4 fit, vec4 cut, vec4 grd, vec4 spn, vec2 p,",
      "             out vec2 q, out float code){",
      "  q = p; code = 0.0;",
      "  float kind = cut.x, dial = cut.y, sgn = cut.z, stag = cut.w;",
      "  float s = max(grd.x, 1e-4);",
      "  vec2 U = vec2(grd.y, grd.z), V = vec2(-grd.z, grd.y);",
      "  float spanU = spn.x, spanV = spn.y, R = spn.z, rMax = spn.w;",
      "  float diag = length(uRes);",
      // the picture standing in the frame: cover-fitted, which is exactly the seating the host
      // applied and binds as `fit`, read back out of it
      "  vec2 half2 = 0.5 * vec2(uRes.x / max(fit.x, 1e-4), uRes.y / max(fit.y, 1e-4));",

      // ---- STRIPES: strips stacked across the picture, each walking its own line ------------------
      "  if (kind < 0.5) {",
      "    float a = dot(p, U);",
      "    float areaMax = (s + 2.0) * spanV;",
      "    float band = diag + s;",
      "    for (int i = 1; i >= 0; i--) {",
      "      float k = floor(a / s) + float(i);",
      "      float a0 = k * s - 1.0, a1 = (k + 1.0) * s + 1.0;",
      "      if (a < a0 || a > a1) continue;",
      "      float dirn = (mod(k, 2.0) < 0.5 ? 1.0 : -1.0) * sgn;",
      "      float u = localAt(dial, ovl(a0, a1, -spanU * 0.5, spanU * 0.5) * spanV, areaMax, stag);",
      "      float off = dirn * R * u;",
      "      vec2 qq = p - off * V;",
      "      if (abs(dot(qq, V)) > band) continue;",
      "      if (abs(qq.x) > half2.x || abs(qq.y) > half2.y) continue;",
      "      q = qq; code = k; return true;",
      "    }",
      "    return false;",
      "  }",

      // ---- RINGS: annuli about the picture's own middle, each reading its own radius --------------
      // A ring travels by growing or shrinking about that middle — the one similarity that keeps a
      // circle a circle — and its picture grows and shrinks with it, so the inverse map is one
      // divide. EACH RING'S REACH IS ITS OWN (grid-colour.js, the head of the file, and its repair of
      // 12.08): inward, the whole middle radius, so the scale walks straight from 1 to 0 and the ring
      // is through the pole at dial 1 exactly; outward, as far as it takes for the ring's INNER edge
      // to stand past the frame's corner. One reach in points for all the rings alike is the very
      // regression that made the arriving work unreadable, and it is not reintroduced here.
      "  if (kind < 1.5) {",
      "    float n = max(1.0, grd.w);",
      "    float stp = rMax / n;",
      "    float halfD = diag * 0.5;",
      "    float rho = length(p);",
      "    float last = ceil((rMax + stp) / stp) - 1.0;",
      "    float areaMax = (last + 1.0) * (last + 1.0) - last * last;",
      "    bool got = false;",
      "    for (int i = 0; i < 98; i++) {",
      "      float k = float(i);",
      "      if (k * stp >= rMax + stp) break;",
      "      float r0 = k * stp, r1 = (k + 1.0) * stp + 1.0, rm = (r0 + r1) * 0.5;",
      "      float dirn = (mod(k, 2.0) < 0.5 ? -1.0 : 1.0) * sgn;",
      "      if (r0 <= 0.0) dirn = -1.0;",
      "      float reach = dirn < 0.0 ? rm : max(0.0, rm * ((halfD + stp) / max(r0, 1e-6) - 1.0));",
      "      float u = localAt(dial, (k + 1.0) * (k + 1.0) - k * k, areaMax, stag);",
      "      float f = (rm + dirn * reach * u) / rm;",
      "      if (f <= 0.0) continue;",
      "      if (rho < r0 * f || rho > r1 * f) continue;",
      "      vec2 qq = p / f;",
      "      if (abs(qq.x) > half2.x || abs(qq.y) > half2.y) continue;",
      "      q = qq; code = k; got = true;",   // the module draws outward, so the later ring wins
      "    }",
      "    return got;",
      "  }",

      // ---- TILES: the same cut crossed with itself, chequer neighbours to opposite ends -----------
      // A cell travels the line of the strip it is cut from, so the cell's index ACROSS that line is
      // read straight off the point, and the index ALONG it is solved: every cell lying wholly on the
      // picture carries one and the same share of the dial, so the two senses give one candidate
      // each, and the cells straddling the picture's own edge carry a share of their own and are
      // walked.
      "  if (kind < 2.5) {",
      "    float a = dot(p, U), b = dot(p, V);",
      "    float areaMax = (s + 2.0) * (s + 2.0);",
      "    for (int ik = 1; ik >= 0; ik--) {",
      "      float k = floor(a / s) + float(ik);",
      "      float a0 = k * s - 1.0, a1 = (k + 1.0) * s + 1.0;",
      "      if (a < a0 || a > a1) continue;",
      "      float ou = ovl(a0, a1, -spanU * 0.5, spanU * 0.5);",
      "      if (ou <= 0.0) continue;",
      "      bool got = false; float bj = -1e9; vec2 bq = p;",
      "      float uInt = localAt(dial, ou * (s + 2.0), areaMax, stag);",
      "      for (int sg = 0; sg < 2; sg++) {",
      "        float dsign = sg == 0 ? 1.0 : -1.0;",
      "        float off = dsign * R * uInt;",
      "        float bb = b - off;",
      "        for (int ij = 1; ij >= 0; ij--) {",
      "          float j = floor(bb / s) + float(ij);",
      "          float b0 = j * s - 1.0, b1 = (j + 1.0) * s + 1.0;",
      "          if (bb < b0 || bb > b1) continue;",
      "          float dirn = (mod(k + j, 2.0) < 0.5 ? 1.0 : -1.0) * sgn;",
      "          if (abs(dirn - dsign) > 0.5) continue;",
      "          if (ovl(b0, b1, -spanV * 0.5, spanV * 0.5) < s + 2.0 - 0.001) continue;",
      "          vec2 qq = p - off * V;",
      "          if (abs(qq.x) > half2.x || abs(qq.y) > half2.y) continue;",
      "          if (j <= bj) continue;",
      "          bj = j; bq = qq; got = true;",
      "        }",
      "      }",
      // the cells the picture's own edge runs through: their area is their own and so is their share
      "      for (int e = 0; e < 6; e++) {",
      "        float jb = e < 3 ? floor((-spanV * 0.5) / s) : floor((spanV * 0.5) / s);",
      "        float j = jb + float(e < 3 ? e - 1 : e - 4);",
      "        float b0 = j * s - 1.0, b1 = (j + 1.0) * s + 1.0;",
      "        float ov = ovl(b0, b1, -spanV * 0.5, spanV * 0.5);",
      "        if (ov <= 0.0 || ov >= s + 2.0 - 0.001) continue;",
      "        float dirn = (mod(k + j, 2.0) < 0.5 ? 1.0 : -1.0) * sgn;",
      "        float off = dirn * R * localAt(dial, ou * ov, areaMax, stag);",
      "        float bb = b - off;",
      "        if (bb < b0 || bb > b1) continue;",
      "        vec2 qq = p - off * V;",
      "        if (abs(qq.x) > half2.x || abs(qq.y) > half2.y) continue;",
      "        if (j <= bj) continue;",
      "        bj = j; bq = qq; got = true;",
      "      }",
      "      if (got) { q = bq; code = k * 64.0 + bj; return true; }",
      "    }",
      "    return false;",
      "  }",

      // ---- BANDS: the cut made of the work's OWN COLOUR -------------------------------------------
      // The other three cuts lay a geometry over the picture; this one lets the picture's own colour
      // do the cutting. Every point joins the palette colour nearest to it, and each band travels as
      // one piece ALONG ITS OWN HUE read as an angle — nothing else in the crossing could name that
      // direction, and it makes the five bands leave five different ways without a single number
      // being chosen by hand.
      "  vec3 p0 = palAt(tex, vec2(0.50, 0.50));",
      "  vec3 p1 = palAt(tex, vec2(0.25, 0.25));",
      "  vec3 p2 = palAt(tex, vec2(0.75, 0.25));",
      "  vec3 p3 = palAt(tex, vec2(0.25, 0.75));",
      "  vec3 p4 = palAt(tex, vec2(0.75, 0.75));",
      // EACH BAND'S OWN AREA against the largest, which is what its share of the stagger is read
      // from. The module counts the cells of its mask grid; here the count is taken over a lattice of
      // the file, and it is asked for only where a score has named a stagger at all.
      "  float ar0 = 1.0, ar1 = 1.0, ar2 = 1.0, ar3 = 1.0, ar4 = 1.0, arMax = 1.0;",
      "  if (stag > 0.0) {",
      "    ar0 = 0.0; ar1 = 0.0; ar2 = 0.0; ar3 = 0.0; ar4 = 0.0;",
      "    for (int gy = 0; gy < 5; gy++) {",
      "      for (int gx = 0; gx < 5; gx++) {",
      "        vec3 c = texture2D(tex, vec2(0.1 + 0.2 * float(gx), 0.1 + 0.2 * float(gy))).rgb;",
      "        int w = nearestOf(c, p0, p1, p2, p3, p4);",
      "        if (w == 0) ar0 += 1.0; else if (w == 1) ar1 += 1.0;",
      "        else if (w == 2) ar2 += 1.0; else if (w == 3) ar3 += 1.0; else ar4 += 1.0;",
      "      }",
      "    }",
      "    arMax = max(max(max(ar0, ar1), max(ar2, ar3)), max(ar4, 1.0));",
      "  }",
      "  bool got = false;",
      "  for (int i = 0; i < BANDS; i++) {",
      "    vec3 pc = i == 0 ? p0 : (i == 1 ? p1 : (i == 2 ? p2 : (i == 3 ? p3 : p4)));",
      "    float ar = i == 0 ? ar0 : (i == 1 ? ar1 : (i == 2 ? ar2 : (i == 3 ? ar3 : ar4)));",
      "    if (ar <= 0.0) continue;",
      "    float h = hueOf(pc);",
      "    vec2 W2 = vec2(cos(h * 6.28318530718), sin(h * 6.28318530718));",
      // the one reach of this module, read along this band's own line (grid-colour.js bandsBuild)
      "    float reach = diag + (abs(2.0 * half2.x * W2.y) + abs(2.0 * half2.y * W2.x)) * 0.5;",
      "    float off = reach * localAt(dial, ar, arMax, stag) * sgn;",
      "    vec2 qq = p - off * W2;",
      "    if (abs(qq.x) > half2.x || abs(qq.y) > half2.y) continue;",
      "    vec3 c = texture2D(tex, into(vec2(0.5) + qq / uRes, fit)).rgb;",
      "    if (nearestOf(c, p0, p1, p2, p3, p4) != i) continue;",
      "    q = qq; code = float(i); got = true;",   // the module draws them in order, so the later wins
      "  }",
      "  return got;",
      "}",
      // WHAT ONE PIECE SHOWS: the picture at the point the piece carries, with its palette drained as
      // far as this layer's own voice has drained it, and this layer's own light written over it.
      // Neither touches the layer's own presence — the module draws one opaque piece either way and
      // never a transparent one, and the light is written only where something is drawn.
      "vec3 shown(sampler2D tex, vec4 fit, vec2 q, vec2 voice){",
      "  vec3 c = texture2D(tex, into(vec2(0.5) + q / uRes, fit)).rgb;",
      "  c = mix(vec3(dot(c, LUMA)), c, clamp(voice.x, 0.0, 1.0));",
      "  float a = min(0.9, abs(voice.y));",
      "  if (a > 0.0005) c = mix(c, voice.y > 0.0 ? vec3(1.0) : vec3(0.0), a);",
      "  return c;",
      "}",
      "void main(){",
      "  vec2 p = vec2(vUv.x * uRes.x - uRes.x * 0.5, vUv.y * uRes.y - uRes.y * 0.5);",
      "  vec3 col = vec3(0.0);",
      "  float cover = 0.0, lay = 0.0, code = 0.0;",
      "  vec2 q;",
      // THE DEPARTING WORK IS AHEAD OF THE ARRIVING ONE along the one line, which is what a carried
      // arrival means and what the plain reverse comes to as well: where a piece of the first work
      // still stands, it is what the eye sees.
      "  if (layerAt(uA, uFitA, uCutA, uGridA, uSpanA, p, q, code)) {",
      "    col = shown(uA, uFitA, q, uVoiceA); cover = 1.0; lay = 0.5;",
      "  } else if (layerAt(uB, uFitB, uCutB, uGridB, uSpanB, p, q, code)) {",
      "    col = shown(uB, uFitB, q, uVoiceB); cover = 1.0; lay = 1.0;",
      "  }",
      // THE CUT MAP, the judges' own frame: which layer stands at this point, which piece of it, and
      // whether anything stands there at all. It is black exactly where the frame is bare, which is
      // what a row reads a door off.
      "  col = mix(col, vec3(lay, fract(code * 0.125), cover), uMask);",
      // THE COVERAGE LAW (§7, and docs/design/COVERAGE.md): an instrument writes opaque where its own
      // matter stands and clear where its matter is absent. This instrument's matter is the pieces of
      // the two works; between them, for as long as the cut is open, the frame is bare and that space
      // belongs to whatever plays underneath. At the entry door every point is claimed by the
      // departing work's own pieces standing at home and at the exit door by the arriving work's, so
      // the alpha is 1 at every point at both doors and a mixture at neither.
      "  gl_FragColor = vec4(col, cover);",
      "}",
    ].join("\n");

    var DEG = Math.PI / 180;

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function num(v, d) { var x = Number(v); return x === x ? x : d; }

    // ---- THE MODULE'S OWN NUMBERS, carried digit for digit ---------------------------------------

    /* HOW EARLY THE ARRIVING PALETTE IS FULL, in dial (grid-colour.js:97, LEAD_IN). The plan, шаг 4:
       the second work's palette arrives a beat before its forms; the beat is 0.15 of the handle. */
    var LEAD_IN = 0.15;

    /* THE FALLBACK COUNT — strips across the picture's own width, used for a work whose record
       carries no measured slice (grid-colour.js:101, FALLBACK_COUNT). A score leaning on it records
       it as a fallback; here it is the handle's own default and nothing else. */
    var FALLBACK_COUNT = 24;

    /* HOW MANY PIECES A RING CUT MAY STAND, which is the port's own number and the only bound this
       file puts on a count. The inverse map walks the rings, and a shader's walk has to be bounded at
       compile time; ninety-six rings on the tallest buffer this host draws is a ring under nine
       points wide, which is finer than the finest lattice any work of a collection has been measured
       at. It is published on the `countFrom`/`countTo` handles as an applied fact. */
    var RING_MAX = 96;

    /* THE RESPONSE CURVE (DARKROOM-DRAFT D2, his word 08-08 17:57: equal movements of the hand
       produce equal felt change), and ONE CURVE PER KIND OF CUT — which is the module's own finding
       rather than a convenience (grid-colour.js:181-235). Measured raw, strips spend everything by
       0.55 of the dial and nothing after, tiles and bands likewise, while RINGS travel almost to the
       far end, because a ring leaves through the pole and the pole is at dial 1 exactly. The shape is
       one for all four: a two-piece logarithm hinged at that kind's own median of felt change, laid
       over the kind's LIVE travel.

       THE ONE THING THIS PORT CHANGED, AND THE MODULE ASKED FOR IT BY NAME. `live` — the raw dial
       past which the frame does not change any more — is a CONSTANT in the module, and the module's
       own header says what is wrong with that: «`live` is a CONSTANT here, and it is only true for
       this module's own default departures. A score naming `stagger` 0.3 spreads the departures over
       the handle, nothing at all leaves early, and the same curve then reads 39.4 on rings and 153.8
       on tiles — far worse than no curve. So the honest next unit is named: the module must DERIVE
       `live` from its own piece table at build time — it knows each piece's start, its travel and its
       extent, so it knows the dial at which the last one clears the frame — instead of carrying four
       measured constants.»

       That is what `liveOf` below does, and it is what makes the far door EXACT BY CONSTRUCTION here
       rather than by the module's own `if (hand >= 1) return;`. The four measured constants stand as
       the curve's own far end wherever this frame's geometry does not need more of the dial than they
       give — so on the frame the module measured on, every number this file answers with is the
       module's, digit for digit — and they are carried further only where the last piece would still
       be standing in the frame at the far door, never less. The stagger is inside the derivation, so
       the two readings the module records as its own defect are closed. */
    var FEEL = {
      stripes: { live: 0.525, c: 0.30, k1: 0.2, k2: 2.2 },
      rings:   { live: 0.975, c: 0.24, k1: -0.6, k2: 2.8 },
      tiles:   { live: 0.525, c: 0.28, k1: -0.4, k2: 2.4 },
      bands:   { live: 0.550, c: 0.32, k1: 0.0, k2: 3.2 }
    };
    var KINDS = ["stripes", "rings", "tiles", "bands"];
    function kindAt(v) { return KINDS[Math.round(clamp(num(v, 0), 0, KINDS.length - 1))]; }

    function feelLog(x, k) {
      return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);
    }
    // The module's own `feel`, with `live` handed in rather than looked up.
    function feelOf(kind, u, live) {
      var F = FEEL[kind] || FEEL.stripes;
      u = clamp(u, 0, 1);
      var f = u <= 0.5 ? F.c * feelLog(2 * u, F.k1)
                       : F.c + (1 - F.c) * feelLog(2 * u - 1, F.k2);
      return live * f;
    }
    // The same walk read backwards, so a bench can put the two roads at ONE raw dial.
    function feelInv(kind, y) {
      var F = FEEL[kind] || FEEL.stripes;
      y = clamp(y, 0, 1);
      if (y <= F.c) {
        if (Math.abs(F.k1) < 1e-6) return (y / F.c) / 2;
        return Math.log(1 + (y / F.c) * (Math.exp(F.k1) - 1)) / F.k1 / 2;
      }
      var z = (y - F.c) / (1 - F.c);
      if (Math.abs(F.k2) < 1e-6) return (z + 1) / 2;
      return (Math.log(1 + z * (Math.exp(F.k2) - 1)) / F.k2 + 1) / 2;
    }

    /* HOW FAR A PROPERTY HAS TRAVELLED at this hand: nothing before its beat opens, all of it after
       the beat closes, straight across inside (grid-colour.js beatAt). A beat covering the whole
       handle is what every property did before a score could name one. */
    function beatAt(a, b, u) {
      if (!(b > a)) return u >= b ? 1 : 0;
      return clamp((u - a) / (b - a), 0, 1);
    }

    /* A VOICE AT THIS HAND (grid-colour.js voiceAt) — one breath of a named period and a named phase,
       held to nothing at both doors by the window 4u(1 − u). The period is read in the handle's own
       units, so a voice is the same voice whatever second the score walks the handle over. */
    function voiceAt(period, phase, amp, u) {
      var a = num(amp, 0), p = num(period, 0);
      if (!(a > 0) || !(p > 0)) return 0;
      return a * Math.sin(2 * Math.PI * (u / p + num(phase, 0))) * 4 * u * (1 - u);
    }

    /* HOW MUCH OF ITS PALETTE A PIECE HOLDS at this hand (grid-colour.js paletteAt). On the way out it
       drains as the piece travels and is gone by the moment the piece is; on the way in it is already
       full a `lead` of the handle before the piece reaches its place. */
    function paletteAt(flowIn, u, lead) {
      var l = clamp(num(lead, LEAD_IN), 0, 0.9);
      if (flowIn) return clamp((1 - u) / (1 - l), 0, 1);
      return clamp(1 - u, 0, 1);
    }

    // Cover-fit a work into the frame, and nothing beyond it. The module seats its picture with
    // `Math.max(W/iw, H/ih)` and cuts the pieces out of that standing picture, so both doors frame
    // alike and this port asks the host for no crop: `framings` publishes 1 at both ends.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    // The grid the door is read on, and which of the two it is. `drawn` says which one a sentence
    // names, since a reader told «a 780 x 1688 frame» would look for a device that has none.
    function gridOf(st) {
      var bw = Math.round(num(st.bufWidth, 0)), bh = Math.round(num(st.bufHeight, 0));
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(num(st.cssWidth, 0)), ch = Math.round(num(st.cssHeight, 0));
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true };
      return { w: 0, h: 0, drawn: false, given: false };
    }

    // The seating the host applied, read off the frame state where the host hands it and computed
    // from the work's own two numbers where a bench hands those instead. One seating either way, so
    // the script and the shader never work from two guesses at one.
    function fitOf(st, which, W, H) {
      var f = which === "a" ? st.fitA : st.fitB;
      if (f && f.length >= 2 && f[0] > 0 && f[1] > 0) return [f[0], f[1]];
      var iw = num(which === "a" ? st.aw : st.bw, 0), ih = num(which === "a" ? st.ah : st.bh, 0);
      if (iw > 0 && ih > 0) { var g = fit(iw, ih, W, H); return [g[0], g[1]]; }
      return [1, 1];
    }

    /* ONE LAYER'S GEOMETRY at one count and one angle. Every number here is the module's own, read on
       the buffer the shader will sample: the step between two pieces is the picture's own reach
       across the axis the pieces stack on divided by the count, so it carries no screen in it; the
       reach of a piece's line is the frame's own diagonal plus the picture's overflow along that
       line; and a ring's measure is the picture's own radius, which is the same measure read the
       ring's way. */
    function layerOf(kind, dw, dh, count, ang, W, H, diag) {
      var ca = Math.cos(ang), sa = Math.sin(ang);
      var spanU = Math.abs(dw * ca) + Math.abs(dh * sa);
      var spanV = Math.abs(dw * sa) + Math.abs(dh * ca);
      var n = Math.max(1, count);
      var radius = Math.sqrt(dw * dw + dh * dh) / 2;
      return {
        kind: kind, dw: dw, dh: dh, ca: ca, sa: sa, count: n,
        frameW: W, frameH: H, diag: diag,
        step: kind === "rings" ? radius / n : spanU / n,
        spanU: spanU, spanV: spanV, radius: radius,
        reach: kind === "rings" ? radius : diag + spanV / 2,
        // HOW MUCH FRAME A PIECE OF THIS CUT HAS TO CROSS to be wholly out of it: the frame's own
        // reach along the piece's line plus the picture's own reach along it. Read against the
        // line's own reach it is the share of the raw dial the last piece needs.
        frameV: (W * Math.abs(sa) + H * Math.abs(ca)) / 2
      };
    }

    /* THE DIAL AT WHICH THE LAST PIECE OF THIS LAYER CLEARS THE FRAME — the number the module's own
       header asks a port to derive rather than carry. It is read per kind, on this frame, with the
       stagger inside it:
         · a strip and a tile travel one line, so the worst point of the picture is its own far edge
           along that line and the share of the reach it needs is (frame + picture) / reach;
         · a ring leaving through the pole is AT the pole at dial 1 and no earlier, so a ring cut
           spends the whole dial whatever else is true of it;
         · a colour band's line is its own hue, which only the picture knows, so the share is taken
           over every direction a hue could name — the worst of them, walked finely — and the answer
           holds for whichever five colours the work turns out to carry.
       The stagger is on top: the largest piece waits its whole share before it starts, so the dial it
       finishes on is that share plus what is left of the dial times what the travel needs. */
    var LIVE_WALK = 180;          // how finely the band directions are walked, in steps of a turn
    function needOf(L, stagger) {
      var s = clamp(stagger, 0, 0.9), t, i, th, c, si, hv, pic, reach, r;
      if (L.kind === "rings") t = 1;
      else if (L.kind === "bands") {
        t = 0;
        for (i = 0; i < LIVE_WALK; i++) {
          th = Math.PI * i / LIVE_WALK;
          c = Math.abs(Math.cos(th)); si = Math.abs(Math.sin(th));
          hv = (L.frameW * c + L.frameH * si) / 2;
          pic = (L.dw * c + L.dh * si) / 2;
          reach = L.diag + (L.dw * si + L.dh * c) / 2;
          r = (hv + pic) / Math.max(reach, 1e-6);
          if (r > t) t = r;
        }
      } else t = (L.frameV + L.spanV / 2) / Math.max(L.reach, 1e-6);
      return { travel: t, live: Math.min(1, s + (1 - s) * t) };
    }

    // The numbers of one frame. Everything the shader gets beyond the seating of the two works is a
    // pure function of the pose, and every number in the pose comes from a handle a score drives, so
    // a seeded run repeats to the pixel. Nothing here reads a clock of its own: the module's every
    // position and every saturation is a pure function of its dial, which is why the `clock` handle
    // moves no pixel and is published all the same — a score owns the clock here as it does
    // everywhere, and this instrument answers that it spends none of it.
    function posed(st) {
      var g = gridOf(st);
      var W = g.given ? g.w : 1, H = g.given ? g.h : 1;
      var diag = Math.sqrt(W * W + H * H);
      var fA = fitOf(st, "a", W, H), fB = fitOf(st, "b", W, H);
      var dwA = W / Math.max(fA[0], 1e-4), dhA = H / Math.max(fA[1], 1e-4);
      var dwB = W / Math.max(fB[0], 1e-4), dhB = H / Math.max(fB[1], 1e-4);

      var hand = clamp(num(st.mix, 0), 0, 1);
      var handA = hand, handB = 1 - hand;
      var stag = clamp(num(st.stagger, 0), 0, 0.9);
      var lead = clamp(num(st.lead, LEAD_IN), 0, 0.9);
      var kindA = kindAt(st.kindA), kindB = kindAt(st.kindB);

      // THE BRIDGE. One count and one angle serve both layers, on the score's own axis. The module's
      // own header settles which axis that is: «the count and the angle walk from the departing
      // work's structure to the arriving one across THE HANDLE. All of those are the score's axis.
      // What the curve shapes is the geometry.» The module's own `stripes` and `tiles` read the
      // CURVED dial there while its `rings` reads the handle; this port reads the handle on all four,
      // which is the header's own sentence, and this port's report names the repair.
      var count = clamp(num(st.countFrom, FALLBACK_COUNT)
        + (num(st.countTo, FALLBACK_COUNT) - num(st.countFrom, FALLBACK_COUNT))
          * beatAt(clamp(num(st.countBeatIn, 0), 0, 1), clamp(num(st.countBeatOut, 1), 0, 1), hand),
        1, RING_MAX);
      var angDeg = num(st.angleFrom, 0)
        + (num(st.angleTo, 0) - num(st.angleFrom, 0))
          * beatAt(clamp(num(st.angleBeatIn, 0), 0, 1), clamp(num(st.angleBeatOut, 1), 0, 1), hand);
      var ang = angDeg * DEG;

      var LA = layerOf(kindA, dwA, dhA, count, ang, W, H, diag);
      var LB = layerOf(kindB, dwB, dhB, count, ang, W, H, diag);
      LA.frameW = W; LA.frameH = H; LA.diag = diag;
      LB.frameW = W; LB.frameH = H; LB.diag = diag;
      var nA = needOf(LA, stag), nB = needOf(LB, stag);
      // The curve's far end: the module's own measured number, carried further only where this
      // frame's own geometry needs more of the dial for the last piece to clear.
      var liveA = Math.max((FEEL[kindA] || FEEL.stripes).live, nA.live);
      var liveB = Math.max((FEEL[kindB] || FEEL.stripes).live, nB.live);
      var dialA = feelOf(kindA, handA, liveA);
      var dialB = feelOf(kindB, handB, liveB);

      // THE SENSE OF THE TRAVEL. Plainly it is the line's own direction, and the two works of a
      // crossing then walk it against each other. Under the CARRIED arrival — the one of the
      // charter's five arrival modes this module knows — the arriving layer takes the opposite
      // sense, so its pieces come in from behind the departing ones and both works ride one scroll.
      // The departing layer names no mode and keeps the plain sense.
      var carried = num(st.arrival, 0) >= 0.5;
      var senseA = 1, senseB = carried ? -1 : 1;

      // THE TWO VOICES. The colour voice is the palette: it leads the forms by the `lead` the score
      // names and breathes on a period of its own on the way. The light voice writes the whole
      // standing frame lighter and darker on a second period, over what is already drawn and only
      // where something is drawn. Both are held to nothing at either door by the window 4u(1 − u),
      // so a door is exactly the picture the file carries.
      var shade = clamp(num(st.shade, 1), 0, 1);
      var satA = clamp(paletteAt(false, handA, lead)
        + voiceAt(st.colourPeriod, st.colourPhase, st.colourAmp, handA), 0, 1);
      var satB = clamp(paletteAt(true, handB, lead)
        + voiceAt(st.colourPeriod, st.colourPhase, st.colourAmp, handB), 0, 1);
      var lightA = voiceAt(st.lightPeriod, st.lightPhase, num(st.lightAmp, 0) * shade, handA);
      var lightB = voiceAt(st.lightPeriod, st.lightPhase, num(st.lightAmp, 0) * shade, handB);

      return {
        cutA: [KINDS.indexOf(kindA), dialA, senseA, stag],
        cutB: [KINDS.indexOf(kindB), dialB, senseB, stag],
        gridA: [LA.step, LA.ca, LA.sa, LA.count],
        gridB: [LB.step, LB.ca, LB.sa, LB.count],
        spanA: [LA.spanU, LA.spanV, LA.reach, LA.radius],
        spanB: [LB.spanU, LB.spanV, LB.reach, LB.radius],
        voiceA: [satA, lightA],
        voiceB: [satB, lightB],
        // read on the diagnostic surface, bound to no uniform: what the handles came to
        hand: hand, kindA: kindA, kindB: kindB, count: count, angleDeg: angDeg,
        dialA: dialA, dialB: dialB, liveA: liveA, liveB: liveB,
        liveMeasuredA: (FEEL[kindA] || FEEL.stripes).live,
        liveMeasuredB: (FEEL[kindB] || FEEL.stripes).live,
        needA: nA.travel, needB: nB.travel,
        stagger: stag, lead: lead, carried: carried ? 1 : 0,
        satA: satA, satB: satB, lightA: lightA, lightB: lightB,
        reachA: LA.reach, reachB: LB.reach, radiusA: LA.radius, radiusB: LB.radius,
        stepA: LA.step, stepB: LB.step,
        // HOW MUCH FRAME THE LAST PIECE HAS LEFT TO CROSS at the far end of its own line, in points
        // of this grid. It is negative or nothing where the piece is out, and positive where the
        // line is too short to carry it out at all — which is the one door this instrument's own
        // geometry can fail to keep and the number the refusal below is written in.
        shortA: (nA.travel - 1) * LA.reach, shortB: (nB.travel - 1) * LB.reach,
        grid: g, mask: clamp(num(st.mask, 0), 0, 1)
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision of 2026-08-17, carried in the U27 brief: the instrument reads
    // its doors at runtime on the actual buffer, and the report it hands back is the runtime truth;
    // what the manifest declares is only the claim. The meshing instrument answered that first, the
    // unfold reads its own panel map and the mirror floor its own floor; this is the same law read in
    // this instrument's own unit, which is THE PIECE — how far the last one of a layer has still to
    // travel before it is out of the frame.
    //
    // WHAT A DOOR ASKS OF THIS INSTRUMENT. At either door one work stands whole at the plain cover
    // fit, and the other is nowhere in the frame. Three things carry that, and this reads all three
    // on the buffer rather than declaring them:
    //   · THE STANDING LAYER HAS NOT MOVED. Its own dial is exactly 0, so every piece is at its own
    //     place and the pieces together are the picture cover-fitted, which is the door.
    //   · THE OTHER LAYER IS WHOLLY OUT. Its dial stands at the far end of its own curve, and the
    //     curve's far end is derived on this frame so that the last piece has exactly cleared it.
    //     Where the line itself is too short to carry a piece out — a picture whose cover-fit
    //     overflow is larger than the frame's own diagonal can happen at an extreme mismatch of
    //     shapes — no dial closes it, and the door is refused with the points still standing.
    //   · THE COLOUR AND THE LIGHT REST. The palette is full on the standing layer and the light
    //     voice is nothing, both by the window at the handle's own ends; read rather than trusted.
    //   · THE JUDGES' CHANNEL IS SHUT. `mask` draws the cut map itself as colour, which is what it is
    //     for; left open at a door the frame is a false-colour map of the cut and not the photograph.
    //
    // AND THERE IS NOTHING HERE TO HOLD. The meshing instrument holds a leaking size whole because a
    // neighbouring size draws a whole door; here a short line is short at every count and every
    // angle a score could ask for by the same geometry, so anything this reading finds is a real
    // fault no widening closes. `held` is therefore always nothing, and it says so rather than
    // carrying a guard that could never fire.
    var DOOR_SHOW = 0.5 / 255;   // how much of the cut map may stand at a door and it still BE the
                                 // photograph: half a level of 255, an eighth of the charter's own
                                 // door bar of 6 of 255 at one point
    var DOOR_REST = 1e-9;        // the palette and the light rest exactly, by the window's own zero

    function doorWhyNoOf(v, st) {
      var mix = num(st.mix, -1);
      var want = mix === 0 ? 1 : (mix === 1 ? 0 : -1);
      if (want < 0 || !v.grid.given) return null;
      var g = v.grid;
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      var door = want ? "the entry" : "the exit";
      var work = want ? "departing" : "arriving";
      var goneShort = want ? v.shortB : v.shortA;
      var goneKind = want ? v.kindB : v.kindA;
      var stayDial = want ? v.dialA : v.dialB;
      var staySat = want ? v.satA : v.satB;
      var stayLight = want ? v.lightA : v.lightB;
      if (goneShort > 0) {
        return door + " door leaks: the " + (want ? "arriving" : "departing") + " work's own "
             + goneKind + " cut reaches " + (want ? v.reachB : v.reachA).toFixed(2)
             + " points along each piece's line, which is " + goneShort.toFixed(2)
             + " points short of carrying the last piece out" + where + ", so that work still stands "
             + "in the frame where " + door + " door's own law asks for the " + work
             + " work alone at every point";
      }
      if (stayDial !== 0) {
        return door + " door leaks: the " + work + " work's own dial stands at "
             + stayDial.toFixed(9) + " rather than at nothing" + where + ", so its pieces have left "
             + "their places where " + door + " door's own law asks for that work standing whole";
      }
      if (Math.abs(staySat - 1) > DOOR_REST || Math.abs(stayLight) > DOOR_REST) {
        return door + " door leaks: the " + work + " work stands at a palette of "
             + staySat.toFixed(9) + " and a light of " + stayLight.toFixed(9)
             + where + ", where " + door + " door's own law asks for the work's own full palette and "
             + "no light written over it";
      }
      if (v.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + v.mask.toFixed(6)
             + ", so the frame draws the cut map — the " + goneKind + " cut at " + v.count.toFixed(2)
             + " pieces across a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
             + " — instead of the " + work + " work, where " + door + " door's own law asks for the "
             + work + " work at every point";
      }
      return null;
    }

    function values(st) {
      var v = posed(st);
      v.doorHeld = null;
      v.doorWhyNo = doorWhyNoOf(v, st);
      v.doorGrid = v.grid.given && (num(st.mix, -1) === 0 || num(st.mix, -1) === 1)
        ? { w: v.grid.w, h: v.grid.h, drawn: v.grid.drawn } : null;
      return v;
    }

    var manifest = {
      id: "grid-colour", api: 1, arity: 2,
      // The first work comes apart along its own grid, the ground shows between the pieces while both
      // works are travelling, and the second work stands whole out of its own.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF. lab/data/module-contract.json carries this module's
      // level already read — CELL+LIGHT-COLOUR — and that row is carried here rather than re-decided:
      //   · CELL — the pieces. The frame is cut into cells that leave one at a time along their own
      //     lines, and the cut is the work's own measured structure at either door.
      //   · LIGHT-COLOUR — the palette and the light. The palette drains out of a departing piece and
      //     fills an arriving one a beat before it lands, and the light voice writes the standing
      //     frame lighter and darker; neither touches the layer's own presence, which is what makes
      //     them a move of colour and of light and nothing else.
      // SURFACE is not claimed: no field runs over the whole frame here, and what changes is the
      // cells and their colour rather than one surface's own attitude.
      levels: ["CELL", "LIGHT-COLOUR"],
      // WHAT THIS INSTRUMENT CUTS ON, from §8's own vocabulary. Four kinds, one per cut the module
      // plays, and the kind rides with the layer carrying that work because a cut is the work's own
      // device: `strip` for stripes, `ring` for rings, `tile` for tiles, and `band` for the cut made
      // of the work's own colour, which is the kind the composer's `shared-palette-region` pivot
      // names and which no other landed instrument cuts on.
      cuts: ["strip", "ring", "tile", "band"],
      params: { kindA: [0, 3], kindB: [0, 3], countFrom: [1, RING_MAX], countTo: [1, RING_MAX],
                angleFrom: [0, 180], angleTo: [0, 180], stagger: [0, 0.9], lead: [0, 0.9] },
      // WHAT THIS INSTRUMENT SHOWS BESIDES A CROSSING (his 19:13 word, the second register). The cut
      // a work comes apart along IS the work's own measured device — its step and its angle — so a
      // visitor watching the pieces leave is watching the rule the photograph was made by, and
      // watching it turn into the rule the next one was made by. Nothing is explained to anybody.
      register: "process",
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and carries the whole passage;
      // `clock` is the second the host hands down; the rest are the module's own declared params, its
      // two travelling structures, the beat each of them travels inside, the two voices and the
      // arrival mode. `shade` and `mask` are the judges' channels.
      //
      // NO HANDLE HERE KEEPS A CLOCK OR A ROLL OF ITS OWN. The module rolls no die at all — every
      // position and every saturation in it is a pure function of the dial — so no `seed` is
      // published, because a handle nothing reads is a handle invented. `clock` IS published, because
      // the module accepts the second the engine hands it and a score owns the clock everywhere; this
      // instrument spends none of it and says so.
      //
      // NO `travel` HANDLE, AND THAT IS A DECISION. The fleet's `travel` scales how far a picture is
      // carried, and here how far a piece is carried is exactly what the far door is made of — every
      // piece travels its own line until it is exactly out of the frame at dial 1 and no further. A
      // handle that could shorten that would be a handle that could break a door, so the travel is
      // spent by the door law instead and this port's report names it.
      //
      // `flow` DOES NOT CROSS AS A HANDLE. It is the pair's own order — the departing work's layer
      // runs `out` and the arriving work's runs `in` — and it is applied below rather than published.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0,
                 applied: { movesNoPixel: true,
                            why: "every position and every saturation in this module is a pure "
                               + "function of its own dial, so the handed second changes nothing on "
                               + "screen; the handle stands because a score owns the clock" } },
        kindA: { min: 0, max: 3, def: 0, kind: "enum", step: 1, rungs: KINDS,
                 unit: "the cut the DEPARTING work's own layer is made of",
                 reads: "structure.ownDevice.kind — the work's own measured device, since the kind is "
                      + "the work's own устройство and rides with the layer carrying that work; "
                      + "where the record names no device, the strongest of structure.radial.score "
                      + "(rings), the work's own grid count (tiles) and its strip family (stripes), "
                      + "and `band` where the pair's pivot is the composer's shared-palette-region" },
        kindB: { min: 0, max: 3, def: 0, kind: "enum", step: 1, rungs: KINDS,
                 unit: "the cut the ARRIVING work's own layer is made of",
                 reads: "the same reading off the arriving work's own record" },
        countFrom: { min: 1, max: RING_MAX, def: FALLBACK_COUNT,
                     unit: "pieces across the departing work's own drawn extent",
                     reads: "the work's own frameSide over its lattice step — structure.ownDevice."
                          + "stepPx where the work carries one and structure.grid.periodPx where it "
                          + "does not, which is the order of preference the composer's own "
                          + "`latticePx` already reads them in. A work whose record carries no "
                          + "measured slice hands over the module's own fallback of "
                          + FALLBACK_COUNT + " across its width, and a score leaning on that records "
                          + "it as a fallback",
                     applied: { ringsWalkedTo: RING_MAX,
                                why: "the inverse map walks the rings and a shader's walk is bounded "
                                   + "at compile time; the bound is finer than the finest lattice a "
                                   + "work has been measured at" } },
        countTo: { min: 1, max: RING_MAX, def: FALLBACK_COUNT,
                   unit: "pieces across the arriving work's own drawn extent",
                   reads: "the same reading off the arriving work's own record",
                   applied: { ringsWalkedTo: RING_MAX } },
        angleFrom: { min: 0, max: 180, def: 0, unit: "degrees; 0 upright, 90 flat",
                     reads: "structure.ownDevice.angleDeg — the angle the departing work's own step "
                          + "was cut at, falling to structure.grid.angleDeg where it carries no "
                          + "device, which is the composer's own `latticeAngleDeg`" },
        angleTo: { min: 0, max: 180, def: 0, unit: "degrees; 0 upright, 90 flat",
                   reads: "the same reading off the arriving work's own record" },
        // ONE PROPERTY PER BEAT (grid-colour.js, its own heading). The count and the angle no longer
        // travel over the whole handle at once: each carries a window of the handle the score names,
        // inside which that one property travels, held before it and after it. The doors stay the
        // departing work's structure at 0 and the arriving work's at 1 whatever the windows are, so
        // neither of these four can move a door.
        countBeatIn: { min: 0, max: 1, def: 0, unit: "where the count's own beat opens",
                       reads: "nothing in a work record bears on it: where in a passage a structure "
                            + "should travel is the score's reading of the step it stands at" },
        countBeatOut: { min: 0, max: 1, def: 1, unit: "where the count's own beat closes",
                        reads: "nothing in a work record bears on it" },
        angleBeatIn: { min: 0, max: 1, def: 0, unit: "where the angle's own beat opens",
                       reads: "nothing in a work record bears on it" },
        angleBeatOut: { min: 0, max: 1, def: 1, unit: "where the angle's own beat closes",
                        reads: "nothing in a work record bears on it" },
        stagger: { min: 0, max: 0.9, def: 0,
                   unit: "how much of the handle the piece departures are spread over, by piece area",
                   applied: { restsAt: "both doors",
                              why: "the largest piece waits its whole share before it starts and "
                                 + "every piece still arrives at the far end by dial 1, because the "
                                 + "curve's own far end is derived with this number inside it" },
                   reads: "nothing in this tree bears on it. A LARGER PIECE MOVES HEAVIER is the "
                        + "plan's own rule and the module reads each piece's area off its own cut, "
                        + "which the instrument recomputes; how far apart to set the departures is "
                        + "the score's own reading and no measurement of a work publishes it" },
        lead: { min: 0, max: 0.9, def: LEAD_IN,
                unit: "how early the arriving work's palette is full, as a share of the handle",
                reads: "nothing in the composer's own per-work readings bears on it. The record does "
                     + "carry palette.hueConcentration and palette.rung, and neither reaches "
                     + "`measuredParts` — that gap is named in this port's report rather than "
                     + "answered here with a number nobody measured" },
        colourPeriod: { min: 0, max: 4, def: 0, unit: "the colour voice's own breath, in handle units",
                        reads: "nothing bears on it; a voice's period is the score's own" },
        colourPhase: { min: 0, max: 1, def: 0, unit: "the head start the score gives that breath",
                       reads: "nothing bears on it" },
        colourAmp: { min: 0, max: 1, def: 0, unit: "how far that breath carries the palette",
                     applied: { restsAt: "both doors",
                                why: "the window 4u(1 − u) holds a voice to nothing at either end" },
                     reads: "nothing in `measuredParts` bears on it; the nearest reading the record "
                          + "carries is luminance.ladderPosition, which is a tone and not a hue" },
        lightPeriod: { min: 0, max: 4, def: 0, unit: "the light voice's own breath, in handle units",
                       reads: "nothing bears on it" },
        lightPhase: { min: 0, max: 1, def: 0, unit: "the head start the score gives it",
                      reads: "nothing bears on it" },
        lightAmp: { min: 0, max: 1, def: 0,
                    unit: "how far the standing frame is written lighter and darker",
                    applied: { restsAt: "both doors", scaledBy: "shade" },
                    reads: "luminance.ladderPosition of the two works, read as the distance between "
                         + "them: two works standing far apart on their own tonal ladder are what "
                         + "gives a light voice something to say between them" },
        arrival: { min: 0, max: 1, def: 0, kind: "enum", step: 1,
                   rungs: ["none named — the plain reverse", "carried"],
                   unit: "which of the charter's arrival modes brings the arriving work",
                   applied: { toTheArrivingLayerOnly: true },
                   reads: "nothing in a work record bears on it: an arrival mode is the charter's "
                        + "shelf-7 choice and belongs to the passage rather than to a photograph" },
        shade: { min: 0, max: 1, def: 1, unit: "the weight of the light voice",
                 applied: { restsAt: "both doors" } },
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { readOn: "the drawing buffer", reads: "clearance",
                                          measures: "how far the last piece of the leaving layer has "
                                                  + "still to travel along its own line, the "
                                                  + "standing layer's own dial, its palette and its "
                                                  + "light, and this channel itself",
                                          held: null } } },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE, AND BOTH ARE THE PLAIN COVER FIT — the module's own framing record in
      // lab/data/module-contract.json: «sc = Math.max(W/iw, H/ih), the plain cover-fit with no crop
      // of its own; the stripes are cut out of that standing picture, so every door frames alike».
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      // WHAT `flow` CAME TO. The module's second declared param is not a handle here: a crossing
      // spends it on the pair's own order, the departing work's layer running `out` and the arriving
      // work's `in`, and a score that could set both to one value would break both doors at once.
      applied: { flow: { departing: "out", arriving: "in",
                         why: "in a crossing the flow IS the pair's order; published here rather "
                            + "than handed to a score" } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it decides which piece of which work owns each point
      // of the frame and carries the pictures inside those pieces. Both are what it does to its own
      // surface, so the witness camera stays the stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). Its matter is the pieces of the two
      // works, and between them the frame is genuinely bare — that is the whole of this cut: what
      // leaves the eye leaves the frame, and nothing is ever faded. So the alpha is 1 where a piece
      // stands and 0 where none does, and the space between belongs to whatever plays underneath.
      // Under the placement rule (§8 as amended 14:05, and `coverageWhyNo`) that means this
      // instrument is laid OVER a ground rather than standing as the floor of a stack, which is the
      // honest consequence of a cut that opens the frame.
      coverage: { writes: true,
                  how: "1 where a piece of either work stands and 0 where the frame is bare — a "
                     + "point no departing piece still covers and no arriving piece has yet reached. "
                     + "At the entry door every point is claimed by the departing work's pieces "
                     + "standing at home and at the exit door by the arriving work's, so the alpha "
                     + "is 1 at every point at both doors and a mixture at neither" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block names — so the
      // frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, clock: 0, kindA: 0, kindB: 0,
                     countFrom: FALLBACK_COUNT, countTo: FALLBACK_COUNT, angleFrom: 0, angleTo: 0,
                     countBeatIn: 0, countBeatOut: 1, angleBeatIn: 0, angleBeatOut: 1,
                     stagger: 0, lead: LEAD_IN,
                     colourPeriod: 0, colourPhase: 0, colourAmp: 0,
                     lightPeriod: 0, lightPhase: 0, lightAmp: 0,
                     arrival: 0, shade: 1, mask: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "grid-colour", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uCutA", type: "vec4", source: "frame:cutA" },
          { name: "uCutB", type: "vec4", source: "frame:cutB" },
          { name: "uGridA", type: "vec4", source: "frame:gridA" },
          { name: "uGridB", type: "vec4", source: "frame:gridB" },
          { name: "uSpanA", type: "vec4", source: "frame:spanA" },
          { name: "uSpanB", type: "vec4", source: "frame:spanB" },
          { name: "uVoiceA", type: "vec2", source: "frame:voiceA" },
          { name: "uVoiceB", type: "vec2", source: "frame:voiceB" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own two
      // canvases per layer — the picture and its grey twin — its clip paths, its band surfaces and
      // its own draw on every parameter change are what this port does without.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/grid-colour.js", commit: "5cf8968" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument no longer answers WHETHER it takes a pair — it answers how well it
      // suits one, so a poor fit is still playable and still explains itself. The arithmetic runs in
      // the composer, which is the one place holding both records; what stands here is the
      // instrument's own statement of WHAT IT READS. RANKING ONLY: any two photographs in the world
      // get a crossing, and a measurement only ranks which genre suits.
      suits: { reads: ["structure.ownDevice.stepPx", "structure.ownDevice.confidence",
                       "structure.grid.periodPx", "structure.grid.score", "frameSide"],
               how: "the whole claim of this cut is that at the near door it stands at the DEPARTING "
                  + "work's own measured structure and at the far door at the ARRIVING work's, so it "
                  + "suits a pair by how plainly each work publishes a grid of its own to be cut "
                  + "along — a step, an angle, and how confidently they were recovered — and the "
                  + "weaker of the two readings is the fit. A whole fit is two works that each wear "
                  + "their own lattice on the surface, where the passage reads as one rule turning "
                  + "into another; a fit of nothing is two works with no measured structure at all, "
                  + "where the cut is the module's own fallback count and reads as a grid laid over "
                  + "the photographs rather than found in them — still a crossing, and it plays "
                  + "wherever nothing ranks higher" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "grid-colour",
      manifest: manifest,
      values: values,
      fit: fit,
      // The hand's own curve. The kind decides it, so the reading a host or a bench takes off this
      // entry is the DEPARTING layer's — the one whose cut the near door stands at.
      feel: function (u) { return feelOf("stripes", u, FEEL.stripes.live); },
      // read by a bench that has to put the two roads at ONE raw dial, since this port derives the
      // curve's far end per frame and the lab module carries a constant
      feelOf: feelOf,
      feelInv: feelInv,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the grid-and-colour instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's two canvases, its clip paths, its draw-on-change and
      // its own build step are gone, so every number here comes from a handle a score drives or from
      // the frame the host is about to bind.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim, so the instrument is what answers for it: at either door it reads how
      // far the leaving layer's last piece still has to travel on the buffer the host is about to
      // bind and, where the line is too short to carry it out, hands the host the reason with the
      // measured points in it instead of drawing a door that is two works at once. The host recovers
      // the transaction on that reason and the walk's own glide carries the visitor.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, clock: h.clock, kindA: h.kindA, kindB: h.kindB,
          countFrom: h.countFrom, countTo: h.countTo, angleFrom: h.angleFrom, angleTo: h.angleTo,
          countBeatIn: h.countBeatIn, countBeatOut: h.countBeatOut,
          angleBeatIn: h.angleBeatIn, angleBeatOut: h.angleBeatOut,
          stagger: h.stagger, lead: h.lead,
          colourPeriod: h.colourPeriod, colourPhase: h.colourPhase, colourAmp: h.colourAmp,
          lightPeriod: h.lightPeriod, lightPhase: h.lightPhase, lightAmp: h.lightAmp,
          arrival: h.arrival, shade: h.shade, mask: h.mask,
          reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, and BOTH WORKS' SEATING ON IT. The step between two
          // pieces, the reach of a piece's line and the curve's own far end are all read on the
          // picture as the host actually seats it, so the script and the shader work from one
          // seating rather than two guesses at one.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
          fitA: st.fitA, fitB: st.fitB,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. `request` is
        // the travel a door asks of the leaving layer's last piece — all of it, and no more — and
        // `applied` is the travel this frame's own geometry gives it.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "clearance",
              request: h.mix === 0 ? v.needB * v.reachB : v.needA * v.reachA,
              applied: h.mix === 0 ? v.reachB : v.reachA,
              moved: h.mix === 0 ? -v.shortB : -v.shortA,
              unit: "points of the drawing buffer",
              // what the two layers stood at, so a walk reads the door rather than only the sentence
              cut: [v.kindA, v.kindB], count: v.count, angleDeg: v.angleDeg,
              live: [v.liveA, v.liveB], dial: [v.dialA, v.dialB],
              palette: [v.satA, v.satB], light: [v.lightA, v.lightB],
              held: v.doorHeld, whyNo: v.doorWhyNo,
            });
          }
          if (v.doorWhyNo) { st.fail(st.token, v.doorWhyNo); return; }
        }
        st.draw(pose);
        if (st.progress >= 1 && !st.pinned) st.settle(st.token);
      },
      resize: function () {},
      cancel: function () {},
      dispose: function () { live = false; },
      contextLost: function () { live = false; },
      contextRestored: function () {},
    };
  }

  // ---- what this file declares --------------------------------------------------------------
  // The host registers this instrument under the name its own manifest carries, and refuses it when
  // that name disagrees with the name whose address this file was fetched from, when its version
  // disagrees, or when its manifest asks for something the host cannot supply.
  join({
    version: INSTRUMENT_VERSION,
    instrument: gridColourInstrument(),
  });
})();
