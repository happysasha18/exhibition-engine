# The fifteen declared seams nobody reads, sorted

Written 2026-09-04. `tests/test_pass_seam_readers.py` has held fifteen instrument names in one flat
set since 2026-09-01: each declares a non-empty `manifest.seams` and none reads `.seams` back. The set
says the count and stops there, so every reader who arrives at it re-derives the same fifteen answers.
This document is those answers, taken once.

The gate's own docstring is right that it is an enforcer rather than the promise's fulfilment. What
follows changes no behaviour. It sorts the fifteen so the decision underneath them can be taken on the
right question, and it kills one wrong answer that had already been written into a plan.

## The wrong answer, killed

A plan written earlier the same night proposed connecting `droste` and `studio` first, on the reasoning
that their fixed handover shares (`0.20` and `0.18`) never shrink as more copies share a turn, while
the host's shared `seamHandoverOf(count)` does. Adversarial review falsified it at
`engine/assets/pass-layer.js:3202`:

```js
var count = s.of && handles && handles[s.of] !== undefined ? handles[s.of] : 1;
```

**No `seams` entry in any of the 27 manifests names a handle in `of`.** Every one declares
`of: null`. So `count` is `1` on every instrument, on every frame, and `seamHandoverOf(1)` reduces to
`clamp(0.125 / (W / cssW), 0.01, 0.2)` — a value that moves with device pixel ratio and render rung,
never with copy count.

Both files say so themselves, and said so before the plan was written.
`pass-inst-droste.js:634-635`: *"`of` names no handle because the width is a share of one copy and
does not depend on how many copies the dive holds."* `pass-inst-studio.js:523-525` makes the same
statement for the ring.

So connecting `droste` and `studio` is not a repair of a share that fails to shrink. It is a flat
number change — `0.20 → 0.125` and `0.18 → 0.125` at one buffer point per CSS pixel, `→ 0.0625` at
two — visible on every frame at every copy count. That is the same act, on two more instruments, that
PLAN.md row S-99 exists to decide for `planet` (`0.14 → 0.125`) and `tunnel` (`0.10 → 0.125`), where
the frames moved by 0.06 and 0.21 of 255 and nobody had said the number was changing.

One consequence the plan also missed: `studio`'s `0.18` sits below the shared clamp's ceiling of
`0.2`, so at a dropped render rung the shared value clamps up and studio's band would grow **wider**,
which is the opposite of what connecting it was supposed to buy.

## The fifteen, by what connecting each would actually cost

### Eleven carry a flat constant, and the decision is S-99's own question (class B)

`beat` (`1.0 / uRes.y`, `:428`, `:579`) · `boxfold` (`2.0 / max(uRes.y, 1.0)`, `:333`, declaration
`:932-937`) · `gates` (`hA = 1.0 / resA`, `:637-638`) · `grid-colour` (four separate literal `1.0`s in
the shader's loop bounds, `:233`, `:291`, `:303`, `:318`) · `lens` (`:269`, `:275-276`) · `unfold`
(`pt = 1.0 / uRes.y`, `:1077`) · `veil` (`:463-470`) · `waterline` (`:628-635`) · `wind` (`:498-506`)
— nine hairlines against the host's `seamHairlineOf()`, which clamps to `[1, 3]`.

Plus `droste` (`SEAM_SHARE = 0.20`, `:325`, used `:444`) and `studio` (`gSeam = smoothstep(0.82, 1.0,
x - k)`, `:206`, consumed `:305-310`) — two handover shares against `seamHandoverOf()`, which clamps to
`[0.01, 0.2]`.

`veil`, `waterline` and `wind` belong here rather than with the formula cases: each states in its own
declaration that the crossover is one point of the drawing buffer, written as `delta / (grad · h)`
with `h = 1 / uRes.y`. That is `beat`'s formula with a gradient normaliser in front of it, so the
shared value enters exactly where `beat`'s would.

The live disagreement, today, with nobody having decided it: `beat` says one buffer point and
`boxfold` says two, for the same job.

**All eleven change the picture. None of the eleven changes it for a reason a visitor could name.**
The question — does the shared number stand, or does each instrument keep its own — is word for word
S-99's question, and S-99 is scoped to three named instruments with a done-when reading three named
suites. It cannot absorb eleven more. They need their own row, decided the same way S-99 decides:
on frames, with both numbers printed.

### Two are a design question rather than a wiring job (class C)

`tilt` — `foot = max(abs(dtdy) * px * 0.5, 1e-6)` (`:143`, declaration `:625-636`); the width scales
with the plane's own projection Jacobian.
`weave` — `wV = 0.5 * (nV * warpD(uv.x, 2.0, phV) / uRes.x + abs(dEdgeV) / uRes.y)` (`:164-165`); built
from the wandering edge's own slope, on two axes.

In both, the shared scalar would have to enter as one term inside an existing expression, and deciding
what it multiplies is design.

### One must not be connected as it stands (class D)

`hero` holds its two seams at 5 and 7 buffer points on purpose — `fw` at `:239`, `rw` at `:247`, and
the same two literals again JS-side in the door reading at `:614` and `:625`. The shared hairline
clamps to `[1, 3]`, so a direct substitution would shrink a crease this instrument's own file argues
needs to be wide. Its declaration at `:770-775` already records both widths, both formulas and the
`of: null` reasoning, so there is nothing here to write down that is not written.

### One has no width to hand back (class E)

`parquet` declares `kind: "tile"`. Its tile mirror makes adjacent tiles sample the identical texture
coordinate at the shared edge — `par = mod(idx, 2.0)` at `:253`, `mir = mix(loc, 1.0 - loc, par)` at
`:254` — so the boundary is continuous by construction and there is no band, no hairline and no number
for the host to spend. Its declaration asks for a retouch that cannot exist.

## The one real defect neither the measurement nor the plan found

`seamsOf` keys its output by `kind` alone and attaches no unit (`pass-layer.js:3203`,
`out[s.kind] = ...`). Across the fleet the key `ring` carries two incompatible units:

| instrument | what `ring` means | value at one buffer point per CSS pixel |
|---|---|---|
| `droste`, `planet`, `studio`, `tunnel` | a share of one repeat's own span | ~0.125 |
| `hero`, `kaleidoscope`, `grid-colour`, `lens` | points of the drawing buffer | ~1.5 |

On `studio` the object handed to the instrument is `{wedge: 1.5, tile: 1.5, ring: 0.125}` — mixed units
under one untagged shape. Nothing misreads it today, because each instrument reads back the key it
declared and knows what it meant. It is a trap for the next reader, for any generic consumer, and for
any instrument that ever declares two entries of one `kind`, where `out[s.kind]` overwrites in
silence. (No instrument does today: every multi-entry manifest declares distinct kinds.)

## What this document does not decide

Nothing. Eleven instruments wait on a decision that is S-99's in kind and needs its own row; two wait
on a design question; two are already correct as they stand.
