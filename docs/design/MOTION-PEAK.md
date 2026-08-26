# The motion peak — charter shelf 5, the conjuror (2026-08-25)

Ready to apply. This note carries the whole change to `engine/assets/pass-composer.js` as three
edits, each quoted against the file as it stands so the applier can find it by reading rather than
by line number — the file has moved under several workers today and will move again. Nothing here
touches any other file. The test that proves it is `tests/test_pass_peak.py`.

## What the shelf asks for

> the CONJUROR (the content swap sits at the plan's motion peak, computable as argmax of summed
> normalized parameter velocity, where the eye is led away)

## What stands today

`fillPlan`'s camera block asserts the peak instead of computing it. Its own comment says so:

```js
        // WHERE THE TWO MIDDLE POINTS STAND IN TIME. Shelf 5's conjuror law puts the content swap
        // at the plan's motion peak, and the travelling cue's own window is the composer's own
        // reading of where that peak sits — so the outbound and inbound poses land at the
        // travelling cue's own open and close.
```

No parameter velocity is summed, normalised or maximised anywhere in the file. Where a plan travels
on no cue of its own, the same comment says outright that "there is no motion peak the composer can
name" and falls back to a tone split.

## The measurement

Over the passage's own normalised time `u`, every handle the plan drives has a rate of change.
Each is divided by that handle's **own published range** — `HANDLE_SPECS[instrument][handle]`, the
manifest's own `min` and `max` — so a handle that swings across a wide span does not drown one that
swings across a narrow one, and every term lands in the same unit: fractions of a handle's own range
per unit of passage time. The sum of those terms is one dimensionless reading of how fast the whole
plan is moving at that instant, and its argmax is the motion peak.

### Two handles are out of the sum, and for one reason

A measurement cannot read the thing it is placing.

- **The door.** The handle each cue's own `doors` record names carries the share of the arriving work
  standing in the frame — it *is* the content swap the shelf places. Counting its own speed makes the
  law say the swap sits where the swap moves fastest, which says nothing. It is also where the eye is
  *looking* rather than where the eye is *led away*, which is the half of the shelf's sentence that
  says what the sum is for.
- **The camera.** Its two middle points are what this reading places, so their velocity is a
  consequence of the answer and never an input to it. The flight's magnitudes are read a few lines
  further down, *after* the two points are placed; that order is what keeps the loop out.

Leaving the door in is not a small matter of taste. With the door counted, the arriving cue's
`in`-eased door has its greatest slope at the passage's very last instant, and the peak lands there
on many pairs — which would push the excursion against the passage's close, where the camera's own
final rest pose already stands, and a pose standing on another pose is the step shelf 2 calls a
camera cut. With the door out, the peak lands where the accompaniment actually moves.

### The derivative of each node kind, written out

Every one is the derivative of the evaluator `pass-layer.js` actually runs. `D` is the passage in
seconds; `w₀`/`w₁` are the cue's own window; `x′` is the input node's own slope.

| kind | value | slope, per unit of passage time |
|---|---|---|
| `static` | fixed | 0 |
| `progress` | `u` | 1 |
| `time` | `u·D` | `D` |
| `cueProgress` | `p = (u·D − w₀)/(w₁ − w₀)` | `D/(w₁ − w₀)` inside the window, 0 outside — the host clamps it, and a clamped reading has stopped moving |
| `curve` | `c(x)` | `c′(x)·x′`, and 0 once `x` has left nought-to-one |
| `map` | `t₀ + (t₁ − t₀)(x − f₀)/(f₁ − f₀)` | `(t₁ − t₀)/(f₁ − f₀)·x′`; an empty `from` range is the node the host itself refuses, and it reads 0 |
| `mix` | `a + (b − a)·t` | `a′ + (b′ − a′)·t + (b − a)·t′` |
| `clamp` | `x` held between `min` and `max` | `x′` strictly between them, 0 at or past either |
| `spline` | the Hermite piece below | `H′(x)·x′`, and 0 before the first point and after the last, where the host holds the value |

The four named curves, carried from `pass-layer.js`'s own `CURVES`:

```
linear(x) = x                 linear'(x) = 1
smooth(x) = x²(3 − 2x)        smooth'(x) = 6x(1 − x)
in(x)     = x²                in'(x)     = 2x
out(x)    = 1 − (1 − x)²      out'(x)    = 2(1 − x)
```

The monotone spline, on the piece between points `a` and `b` of width `h`, with the Fritsch–Carlson
tangents `mₐ`/`m_b` the host's own `splineSlopes` computes, and `s = (x − aₐₜ)/h`:

```
H(s)  = (2s³ − 3s² + 1)·vₐ + (s³ − 2s² + s)·h·mₐ + (3s² − 2s³)·v_b + (s³ − s²)·h·m_b
H′(x) = [ (6s² − 6s)·vₐ + (3s² − 4s + 1)·h·mₐ + (6s − 6s²)·v_b + (3s² − 2s)·h·m_b ] / h
```

A host signal a plan cannot know — `velocity`, `capability`, `noise`, `pointer` — carries no shape:
the composer decides at the instant two works meet and the visitor has not moved yet. An operator
this block writes nowhere is read the same way. Neither refuses anything; both simply add nothing to
the ranking.

### The walk

A thousand steps over the passage's own normalised time, **strictly inside it**. The two ends are
where the two works stand still — the camera's own first and last points are the neutral rest,
shelf 2's *resting exactly when B stands* — so the instant the eye is led away is an instant inside
the crossing rather than one of its two ends. A thousand steps is the walk `voicePeak` already takes
in this same file, for the reason stated there: it resolves the crest to four decimal places, the
precision a score is written at.

The peak is the **middle of the first maximal run** of grid points, not its first instant, so a
plateau reads as its own centre — and a sum that never changes has the whole interior for its
plateau, whose middle is the passage's own middle.

## Where the swap goes

`camera.track[1].at` and `camera.track[2].at`. Those two values, and no others.

Today they are the two ends of `span` — the travelling cue's own window, or the tone split. Under
the shelf, `span` keeps only its **length**; where the excursion stands is the peak's business. With
`q` the peak's own share of the passage, `L` the excursion's length and `D` the passage:

```
track[1].at = q · (D − L)          track[2].at = q · (D − L) + L
```

The excursion of length `L` leaves `D − L` of room over, and the two legs — the flight out of the
departing pose and the flight back into the arriving one — take that room in the same proportion the
peak takes the passage.

## Every claim, by construction

Over the whole span of the values involved: every `q` in nought to one, every `L` no longer than
`D`, every published handle range, every node kind, every named curve, every window shape.

**The sum is bounded.** Every term is `|slope|` divided by a published range that is strictly
positive (a range of nothing contributes nothing and is dropped before the division). Every slope is
a product of three bounded factors: a curve derivative, which is at most 2 for all four named shapes
and 0 outside nought-to-one; a handle's own travel across its published range, which is 1 after the
division; and `D/(w₁ − w₀)`, which is finite because a window with no length contributes nothing at
all. A finite sum of finite terms is finite, for every cue table and not merely for the ones the
collection happens to produce.

**The argmax exists for every passage.** The walk is a finite list of numbers, so it has a largest;
the run attaining that largest is non-empty, so its middle is a real index. A passage carrying one
cue that drives nothing but fixed readings sums to nought at every step, the run is the whole
interior, and the peak is the passage's own middle. Nothing here can return nothing and nothing here
declines — the reading ranks, and a plan whose handles barely move still has a peak.

**The placement stays inside the passage, and four things fall out of the two lines by algebra:**

- `q(D − L)` lies between nought and `D − L`, and `q(D − L) + L` between `L` and `D`, so both points
  stand inside the passage. No clamp is needed and none is written.
- They keep their order and stand exactly `L` apart, so the excursion is the same journey the
  composition sized — moved, never stretched.
- The peak itself stands **inside** the excursion, at the same share `q` of it: `qD − q(D − L) = qL`
  is never negative, and `q(D − L) + L − qD = L(1 − q)` never is either. The camera is out on its
  flight at the instant the plan moves fastest, which is the whole of what the shelf asks.
- The two legs are `q(D − L)` and `(1 − q)(D − L)` — equal only where the peak stands exactly at the
  passage's middle. Shelf 18's reading of 2026-08-19, outbound and return taking different shares,
  survives as a measured fact rather than as a shape this branch has to arrange.

`L ≤ D` is already true of every `span` the branch can build: a cue window is composed inside the
passage, and the tone split runs from half of one share of the passage to half of one plus that
share, which is half the passage wide wherever the share stands. The guard in the code states it
anyway, so the arithmetic answers for values that never reach it.

**Where no instant is louder than another** the shelf names no peak and the excursion is left exactly
where the measurement put it — his word of 2026-08-19, *if the records genuinely cannot supply a
middle, leave it*. That is not a crossing refused: the flight still flies, the doors still open, and
the passage plays whole.

## What a viewer sees differently

The camera is out on its flight — off centre, turned, or come in — at the moment the picture's own
parts are moving fastest, instead of at whatever moment the travelling voice happened to open.

---

# The three edits

## Edit 1 — the arithmetic

**Goes beside** `fillPlan`, immediately above it, at the same indentation as `voicePeak` and
`noteFor`. Find the anchor by reading; it is the only occurrence in the file:

```js
    function fillPlan(key, row, tpl, ctx) {
```

**Insert the block below directly before that line.** It adds nothing that was not already in the
file's own vocabulary: `num`, `isFlt`, `HANDLE_SPECS` are all in scope at that point.

```js
    // ============================================================================================
    // THE PLAN'S MOTION PEAK — charter shelf 5, THE CONJUROR
    // ============================================================================================
    // The shelf's own sentence: "the content swap sits at the plan's motion peak, computable as
    // argmax of summed normalized parameter velocity, where the eye is led away". Everything below
    // is that sentence and nothing else. Nothing here is prepared before the visit, nothing is
    // indexed by the pair, and nothing is chosen at bake: the reading is taken off the score this
    // composition has just written, at the instant two photographs meet.
    //
    // THE SUM. Over the passage's own normalised time, every handle the plan drives has a rate of
    // change. Each is divided by that handle's OWN PUBLISHED RANGE — `HANDLE_SPECS[instrument][h]`,
    // the manifest's own min and max — so a handle that swings across a wide span does not drown
    // one that swings across a narrow one, and every term is in the same unit: fractions of a
    // handle's own range per unit of passage time. The sum of those terms is one dimensionless
    // reading of how fast the whole plan is moving at an instant.
    //
    // TWO HANDLES ARE OUT OF THE SUM, AND FOR ONE REASON: a measurement cannot read the thing it is
    // placing.
    //
    //   THE DOOR is the content swap itself — the cue's own `doors` record names the handle, and
    //   what it carries is the share of the arriving work standing in the frame. Counting its speed
    //   would make the shelf's law say the swap sits where the swap moves fastest, which says
    //   nothing. It is also where the eye is looking rather than where the eye is led away, which
    //   is the half of the sentence that names what the sum is for.
    //
    //   THE CAMERA's own track is the other. Its two middle points are what this reading PLACES, so
    //   their velocity is a consequence of the answer and never an input to it. The flight's
    //   magnitudes are read a few lines below off the same pair, after the two points are placed;
    //   the order is what keeps the loop out.
    //
    // A HANDLE WHOSE RANGE IS EMPTY, and an operator this file writes nowhere, each add nothing and
    // refuse nothing. The reading RANKS: a plan whose handles barely move still has a peak, and the
    // crossing still plays. There is no floor here and no threshold anywhere below.
    //
    // THE WALK STANDS STRICTLY INSIDE THE PASSAGE. The two ends are where the two works stand
    // still — the camera's own first and last points are the neutral rest pose, shelf 2's "resting
    // exactly when B stands" — so the instant the eye is led away is an instant INSIDE the
    // crossing rather than one of its two ends. A thousand steps is the same walk `voicePeak` above
    // already takes over a curve this file knows every number of, and for the same stated reason:
    // it resolves the crest to four decimal places, which is the precision a score is written at.
    //
    // THE PEAK IS A PLATEAU'S MIDDLE, not its first instant. Where several instants tie for the
    // maximum the peak is the middle of the first run of them, so a sum that never changes at all
    // reads as the passage's own middle rather than as its first step — the argmax of a flat
    // function is the whole span, and the whole span's middle is the honest name for it.
    var PEAK_STEPS = 1000;

    // THE FOUR NAMED CURVES AND THEIR DERIVATIVES, WRITTEN OUT. The four shapes are the drawing
    // host's own (`pass-layer.js`'s `CURVES`), carried here so the rate this file reads is the rate
    // the viewer actually sees:
    //
    //     linear(x) = x                 linear'(x) = 1
    //     smooth(x) = x²(3 − 2x)        smooth'(x) = 6x(1 − x)
    //     in(x)     = x²                in'(x)     = 2x
    //     out(x)    = 1 − (1 − x)²      out'(x)    = 2(1 − x)
    //
    // Every one of the four derivatives is bounded on nought to one, and 2 is the largest any of
    // them reaches — `in` at the close, `out` at the open, `smooth` 1.5 at the middle. That is the
    // first half of the bound the whole sum answers to.
    var PEAK_CURVES = {
      linear: [function (x) { return x; }, function () { return 1; }],
      smooth: [function (x) { return x * x * (3 - 2 * x); },
               function (x) { return 6 * x * (1 - x); }],
      "in": [function (x) { return x * x; }, function (x) { return 2 * x; }],
      out: [function (x) { return 1 - (1 - x) * (1 - x); },
            function (x) { return 2 * (1 - x); }]
    };

    // THE MONOTONE SPLINE'S OWN TANGENTS — `pass-layer.js`'s `splineSlopes`, Fritsch–Carlson,
    // carried over unchanged so the course this file differentiates is the course the host draws.
    function peakSlopes(pts) {
      var n = pts.length, d = [], m = [], i, h, a, b, s;
      for (i = 0; i < n - 1; i++) {
        h = num(pts[i + 1].at) - num(pts[i].at);
        d.push(h > 0 ? (num(pts[i + 1].value) - num(pts[i].value)) / h : 0);
      }
      for (i = 0; i < n; i++) m.push(i === 0 || i === n - 1 ? 0 : (d[i - 1] + d[i]) / 2);
      for (i = 0; i < n - 1; i++) {
        if (d[i] === 0) { m[i] = 0; m[i + 1] = 0; continue; }
        a = m[i] / d[i]; b = m[i + 1] / d[i];
        if (a < 0) { a = 0; m[i] = 0; }
        if (b < 0) { b = 0; m[i + 1] = 0; }
        s = a * a + b * b;
        if (s > 9) { s = 3 / Math.sqrt(s); m[i] = s * a * d[i]; m[i + 1] = s * b * d[i]; }
      }
      return m;
    }

    // ONE READING: a node's value at normalised passage time `u`, and its rate of change there,
    // handed back as `[value, slope]`. The slope is in the node's own units PER UNIT OF PASSAGE
    // TIME, so two handles living in windows of different lengths are already comparable before
    // either is divided by its own published range.
    //
    // THE DERIVATIVE OF EACH KIND, and every one of them is the derivative of the evaluator
    // `pass-layer.js` actually runs:
    //
    //   static      value is fixed              slope 0
    //   cueProgress p = (u·D − w₀)/(w₁ − w₀)    slope D/(w₁ − w₀) inside the window, 0 outside it,
    //                                           because the host clamps it and a clamped reading
    //                                           has stopped moving
    //   progress    u                           slope 1
    //   time        u·D                         slope D
    //   curve       c(x)                        slope c′(x)·x′, and 0 where x has left nought-to-one
    //   map         t₀ + (t₁ − t₀)(x − f₀)/(f₁ − f₀)
    //                                           slope (t₁ − t₀)/(f₁ − f₀)·x′; an empty `from` range
    //                                           is the node the host itself refuses, and it reads 0
    //   mix         a + (b − a)·t               slope a′ + (b′ − a′)·t + (b − a)·t′
    //   clamp       x held between min and max  slope x′ strictly between them, 0 at or past either
    //   spline      the Hermite piece between two points, with the tangents above:
    //                 H(s) = (2s³ − 3s² + 1)·vₐ + (s³ − 2s² + s)·h·mₐ
    //                      + (3s² − 2s³)·v_b   + (s³ − s²)·h·m_b
    //                 H′(x) = [ (6s² − 6s)·vₐ + (3s² − 4s + 1)·h·mₐ
    //                         + (6s − 6s²)·v_b + (3s² − 2s)·h·m_b ] / h  ·  x′
    //                                           and 0 before the first point and after the last,
    //                                           where the host holds the value
    //
    // A HOST SIGNAL A PLAN CANNOT KNOW — velocity, capability, noise, pointer — carries no shape
    // here. It is read at nought with no slope, because the composer is deciding at the instant two
    // works meet and the visitor has not moved yet. An operator this file writes nowhere is read
    // the same way. Neither refuses anything; both simply add nothing to the ranking.
    function peakRead(spec, u, cue, durSec, depth) {
      if (spec === null || spec === undefined) return [0, 0];
      if (typeof spec === "number" || isFlt(spec)) return [num(spec), 0];
      if (typeof spec !== "object") return [0, 0];
      depth = depth || 0;
      if (depth > 64) return [0, 0];
      if (spec.node) {
        var ref = (cue.nodes || {})[spec.node];
        return ref ? peakRead(ref, u, cue, durSec, depth + 1) : [0, 0];
      }
      if (spec.source !== undefined) {
        if (spec.source === "progress") return [u, 1];
        if (spec.source === "time") return [u * durSec, durSec];
        if (spec.source === "cueProgress") {
          var w = cue.window || [0, durSec];
          var w0 = num(w[0]), w1 = num(w[1]);
          if (!(w1 > w0)) return [0, 0];
          var p = (u * durSec - w0) / (w1 - w0);
          if (p <= 0) return [0, 0];
          if (p >= 1) return [1, 0];
          return [p, durSec / (w1 - w0)];
        }
        return [0, 0];
      }
      var r, ra, rb, rt, c, f, t, f0, f1, t0, t1, lo, hi;
      switch (spec.op) {
        case "static":
          return [num(spec.value), 0];
        case "curve":
          c = PEAK_CURVES[spec.name] || PEAK_CURVES.linear;
          r = peakRead(spec["in"], u, cue, durSec, depth + 1);
          if (r[0] <= 0) return [c[0](0), 0];
          if (r[0] >= 1) return [c[0](1), 0];
          return [c[0](r[0]), c[1](r[0]) * r[1]];
        case "map":
          r = peakRead(spec["in"], u, cue, durSec, depth + 1);
          f = spec.from || [0, 1]; t = spec.to || [0, 1];
          f0 = num(f[0]); f1 = num(f[1]); t0 = num(t[0]); t1 = num(t[1]);
          if (f1 - f0 === 0) return [0, 0];
          return [t0 + (t1 - t0) * ((r[0] - f0) / (f1 - f0)), (t1 - t0) / (f1 - f0) * r[1]];
        case "mix":
          ra = peakRead(spec.a, u, cue, durSec, depth + 1);
          rb = peakRead(spec.b, u, cue, durSec, depth + 1);
          rt = peakRead(spec.t, u, cue, durSec, depth + 1);
          return [ra[0] + (rb[0] - ra[0]) * rt[0],
                  ra[1] + (rb[1] - ra[1]) * rt[0] + (rb[0] - ra[0]) * rt[1]];
        case "clamp":
          r = peakRead(spec["in"], u, cue, durSec, depth + 1);
          lo = spec.min === undefined ? -Infinity : num(spec.min);
          hi = spec.max === undefined ? Infinity : num(spec.max);
          if (r[0] <= lo) return [lo, 0];
          if (r[0] >= hi) return [hi, 0];
          return r;
        case "spline":
          return peakSpline(spec, u, cue, durSec, depth);
        default:
          return [0, 0];
      }
    }

    function peakSpline(spec, u, cue, durSec, depth) {
      var pts = spec.points;
      if (Object.prototype.toString.call(pts) !== "[object Array]" || !pts.length) return [0, 0];
      var r = peakRead(spec["in"] === undefined ? { source: "progress" } : spec["in"],
                       u, cue, durSec, depth + 1);
      var x = r[0], n = pts.length, i;
      if (n === 1 || x <= num(pts[0].at)) return [num(pts[0].value), 0];
      if (x >= num(pts[n - 1].at)) return [num(pts[n - 1].value), 0];
      var m = peakSlopes(pts);
      for (i = 1; i < n - 1; i++) if (x <= num(pts[i].at)) break;
      var pa = pts[i - 1], pb = pts[i];
      var h = num(pb.at) - num(pa.at);
      if (!(h > 0)) return [num(pb.value), 0];
      var va = num(pa.value), vb = num(pb.value);
      var s = (x - num(pa.at)) / h, s2 = s * s, s3 = s2 * s;
      var value = (2 * s3 - 3 * s2 + 1) * va + (s3 - 2 * s2 + s) * h * m[i - 1]
                + (3 * s2 - 2 * s3) * vb + (s3 - s2) * h * m[i];
      var slope = ((6 * s2 - 6 * s) * va + (3 * s2 - 4 * s + 1) * h * m[i - 1]
                   + (6 * s - 6 * s2) * vb + (3 * s2 - 2 * s) * h * m[i]) / h;
      return [value, slope * r[1]];
    }

    // THE PEAK ITSELF. `at` is the instant in seconds, `share` the same instant as a share of the
    // passage, `top` the largest the sum reached and `flat` whether it ever changed at all.
    //
    // THE BOUND, BY CONSTRUCTION. Every term is |slope| divided by a published range that is
    // strictly positive, and every slope is a product of three bounded factors: a curve derivative
    // (at most 2), a handle's own travel across its published range (at most 1 after the division),
    // and the ratio of the passage's own length to the cue window's — which is finite because a
    // window with no length contributes nothing at all. So the sum is a finite sum of finite terms
    // for every cue table, and `top` is finite for every one of them.
    //
    // THE ARGMAX EXISTS FOR EVERY PASSAGE. The walk is a finite list of numbers, so it has a
    // largest; the run attaining it is non-empty, so its middle is a real index. A passage carrying
    // one cue that drives nothing but fixed readings sums to nought at every step, the run is the
    // whole interior, and the peak is the passage's own middle. Nothing here can return nothing,
    // and nothing here declines.
    function motionPeak(cues, durSec) {
      if (!(durSec > 0) || !cues || !cues.length) return { at: 0, share: 0.5, flat: true, top: 0 };
      var terms = [], i, k, u, s;
      for (k = 0; k < cues.length; k++) {
        (function (c) {
          var specs = HANDLE_SPECS[(c.instrument || {}).id] || {};
          var door = ((c.doors || {})["in"] || {}).handle;
          var tracks = c.tracks || {};
          Object.keys(tracks).sort().forEach(function (h) {
            if (h === door) return;
            var sp = specs[h];
            if (!sp) return;
            var range = Math.abs(num(sp[1]) - num(sp[0]));
            if (!(range > 0)) return;
            var node = (c.nodes || {})[(tracks[h] || {}).node];
            if (!node) return;
            terms.push([node, c, 1 / range]);
          });
        }(cues[k]));
      }
      var sums = [], top = -Infinity, low = Infinity;
      for (i = 1; i < PEAK_STEPS; i++) {
        u = i / PEAK_STEPS;
        s = 0;
        for (k = 0; k < terms.length; k++) {
          s += Math.abs(peakRead(terms[k][0], u, terms[k][1], durSec, 0)[1]) * terms[k][2];
        }
        sums.push(s);
        if (s > top) top = s;
        if (s < low) low = s;
      }
      var lo = -1, hi = 0;
      for (i = 0; i < sums.length; i++) {
        if (sums[i] >= top) { if (lo < 0) lo = i; hi = i; }
        else if (lo >= 0) break;
      }
      if (lo < 0) { lo = 0; hi = sums.length - 1; }
      var share = (lo + hi + 2) / 2 / PEAK_STEPS;
      return { at: share * durSec, share: share, flat: top === low, top: top };
    }

```

## Edit 2 — the placement

Inside `fillPlan`'s camera block, a few lines after `var camera = copy(tpl.camera);`.

**Replace these two lines** — the only occurrence in the file:

```js
        camera.track[1].at = span[0];
        camera.track[2].at = span[1];
```

**with:**

```js
        // WHERE THE TWO MIDDLE POINTS STAND IN TIME — charter shelf 5, THE CONJUROR. `span` above
        // gives the excursion its LENGTH, measured: the travelling cue's own window, or the two
        // works' own tone split where the plan travels on no cue. That length is not touched here.
        // What the shelf decides is WHERE the excursion stands, and the answer is the plan's own
        // motion peak — the argmax of its summed normalised parameter velocity, `motionPeak` above.
        //
        // THE ROOM IS SHARED IN THE PEAK'S OWN PROPORTION. The excursion of length `L` leaves the
        // passage `D − L` of room over, and the two legs — the flight out of the departing pose and
        // the flight back into the arriving one — take that room in the same proportion the peak
        // takes the passage. Writing `q` for the peak's own share:
        //
        //     track[1].at = q · (D − L)          track[2].at = q · (D − L) + L
        //
        // FOUR THINGS FALL OUT OF THOSE TWO LINES BY ALGEBRA, for every `q` in nought to one and
        // every `L` no longer than `D`, so none of them needs a clamp and none can be lost to a
        // pair the collection happens not to carry:
        //
        //   · both points stand inside the passage — the first between nought and `D − L`, the
        //     second between `L` and `D`;
        //   · they keep their order and stand exactly `L` apart, so the excursion is the same
        //     journey the measurement above sized, moved rather than stretched;
        //   · the peak itself stands INSIDE the excursion, at the same share `q` of it as it holds
        //     of the passage — `qD − q(D − L) = qL` is never negative and `q(D − L) + L − qD =
        //     L(1 − q)` never is either, so the camera is out on its flight at the instant the
        //     plan moves fastest, which is the whole of what the shelf asks for;
        //   · the two legs are `q(D − L)` and `(1 − q)(D − L)`, which are equal only where the peak
        //     stands exactly at the passage's middle. Shelf 18's reading of 2026-08-19 — outbound
        //     and return taking different shares — therefore survives as a measured fact rather
        //     than as a shape this branch has to arrange.
        //
        // `L ≤ D` IS ALREADY TRUE OF EVERY `span` THIS BRANCH CAN BUILD: a cue window is composed
        // inside the passage, and the tone split runs from half of one share of the passage to half
        // of one plus that share, which is half the passage wide wherever the share stands. The
        // guard below states it anyway, so the arithmetic answers for values that never reach it.
        //
        // AND WHERE NO INSTANT IS LOUDER THAN ANOTHER the shelf names no peak, and the excursion is
        // left exactly where the measurement above put it — his word of 2026-08-19, "if the records
        // genuinely cannot supply a middle, leave it". That is not a crossing refused: the flight
        // still flies, the doors still open, and the passage plays whole.
        var camPeak = motionPeak(cues, duration / 1000.0);
        var camAt0 = num(span[0]), camAt1 = num(span[1]);
        var camLen = camAt1 - camAt0, camRoom = duration / 1000.0 - camLen;
        if (!camPeak.flat && camRoom >= 0) {
          camAt0 = camPeak.share * camRoom;
          camAt1 = camAt0 + camLen;
        }
        camera.track[1].at = flt(r4(camAt0));
        camera.track[2].at = flt(r4(camAt1));
```

### Edit 2b — the stale comment above `var span;` (do this, or the file lies)

The paragraph directly above `var span;` states the law this change replaces. Replace the whole
comment, from `// WHERE THE TWO MIDDLE POINTS STAND IN TIME. Shelf 5's conjuror law puts the content
swap` down to and including `// it in two by an unmeasured half each.`, with:

```js
        // HOW LONG THE EXCURSION IS. `span` decides the LENGTH of the witness camera's excursion
        // and nothing about where it stands: where the plan travels on a cue of its own, the
        // travelling cue's own window gives that length; where it travels on no cue, the two works'
        // own TONE does — `luminance.level` (`measuredParts()`'s own `level`, the identical reading
        // the flight's own `reach` a few lines below takes on this same pair).
        //
        // WHERE THE EXCURSION STANDS is decided below, by the plan's own motion peak — shelf 5's
        // conjuror law, computed rather than asserted. Until 2026-08-25 the two middle points
        // simply took `span`'s own two ends, and the comment that stood here called the travelling
        // cue's window "the composer's own reading of where that peak sits": no parameter velocity
        // was ever summed, normalised or maximised, and where a plan travelled on no cue this file
        // said outright that there was no motion peak it could name. `motionPeak` above names one
        // for every plan.
```

## Edit 3 — the arithmetic travels beside the entry

The file already hands out its pure arithmetics for one stated reason — *what each of them claims is
a claim about NUMBERS, so it can be answered over the whole span of numbers it takes rather than over
whichever photographs are on disk*. The peak's claims are of exactly that kind, and
`tests/test_pass_peak.py` puts them to it that way. **Find this line** in the returned object at the
end of `make`:

```js
             version: COMPOSER_VERSION, writeJson: writeJson,
```

**and add one line under it:**

```js
             motionPeak: motionPeak,
```

---

# What the applier must check

Run, in the foreground, single files only:

```
python3 tests/test_pass_peak.py         # eight rows, all must be green
python3 tests/test_pass_composed.py     # row statuses must be unchanged from before the edit
```

## What may legitimately move

- **`camera.track[1].at` and `camera.track[2].at`, and nothing else.** Measured over every one of the
  14 520 ordered pairs the shipped records make, against the file as it stood at 2026-08-25: on no
  pair does any field other than those two differ, and no pair changes whether it composes or
  declines. A score's weight moves by at most six bytes in either direction, so the byte-fence row's
  headroom moves by at most that.
- **`test_pass_composed.py`'s memory row** reads `JSON.stringify(plan.camera.track)` as part of *what
  varies across a return*. The camera track now varies on more returns than before, never fewer, so
  the row can only get stronger.
- **Six rows in `test_pass_composed.py` were already red** on the file as it stood at 2026-08-25,
  under other workers' in-flight edits, and none of them is a camera row: the register-row promise
  row, the levels-law cast row, adrift's `seamA`/`seamB`, the LIGHT-COLOUR accompaniment row, the
  `ownedTracks` red-on-bug plant, and the wave-on-the-wire browser row. Base and patched were run
  back to back against one snapshot of the source and every row landed on the same side. Do not read
  those six as this change.

## What must not move

- **The camera-flight row** in `test_pass_composed.py` reads the two middle points' `pan`, `logScale`,
  `pitch`, `yaw` and `roll`. This change touches none of them, and the poses are computed after the
  two `at` values as they always were.
- **The camera-point-fence row** — the track still carries exactly four points.
- **`tests/test_pass_drivers.py`'s dolly rows** read `camera.track[1].logScale`. Untouched.
- **`tests/test_pass_stack.py`'s accompaniment count** reads only that a camera track exists.
- **The two neutral ends.** `track[0]` and `track[3]` are never written by this change, so shelf 2's
  *resting exactly when B stands* is unchanged.

## One thing this change strands, named rather than left quiet

The no-travel fallback builds `span` as `[0.5·s·D, (0.5 + 0.5·s)·D]`, whose **length is half the
passage whatever `s` reads** — the tone share `camLvlShare` only ever moved the two ends together.
Once the peak decides where the excursion stands, that share reaches nothing at all: a reading taken
off the two works that no longer touches the plan. It is left in place here because removing it is a
second decision and this note carries one, but it should not be left standing. The two honest
answers are to delete it and write the length plainly:

```js
          span = [flt(0), flt(r4(0.5 * duration / 1000.0))];
```

or to route the tone reading into the excursion's **length**, where it would actually be seen. Either
way `tests/test_pass_peak.py`'s length row reads `D/2` for a no-travel plan and would need re-basing
only for the second.
