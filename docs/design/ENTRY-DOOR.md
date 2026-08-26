# The entry door — how a voice joins a running picture without replacing it

**Root.** The crossing charter's build ladder, step 0: each module must expose a continuous progress
parameter with a named neutral value — the effect's dry against its wet — because every module was
built permanently wet, and that is why layers could only crossfade. Step 1 clause (b) then puts a
seam check in the suite so a plan cannot quietly return to fading. Clause (a) held from the start:
the engine exposes no opacity handle and a plan physically cannot fade a layer. Clause (b) was built
on 2026-08-25 as `tests/test_pass_seam.py`. This is step 0, which is what clause (b) was written to
police, and it is the oldest standing debt in the engine.

**What this document is.** The contract, as landed. It states what an instrument that may stand above
another owes, why the door law had to be corrected before any of it was possible, and what the
composer needs in order to write plans against it.

## The reserved name

The dry is **`presence`**, and it is one name across the whole fleet, declared the same way in every
manifest. It says whether this voice is in the frame at all.

```js
presence: { min: 0, max: 1, def: 1, level: null,
            unit: "whether this voice is in the frame at all" },
```

At zero the instrument draws nothing anywhere and what stands beneath it shows whole. At one it draws
exactly as it always did, and that is where it rests — so a plan that says nothing about it gets the
picture that instrument has always drawn, and every score written before this contract reads
unchanged.

One name rather than nine was the decision, and it is the same decision this engine has already made
for the levels declaration, for the cut declaration and for the judges' channel. Nine instruments
each inventing a name for one thing is drift; the host and the composer learn a reserved name once.

**It is not the banned opacity handle returning, and the difference is the whole point.** An opacity
handle fades one whole layer against another — that is the crossfade the ladder's clause (a) removed
the tempting tool for, and nothing here brings it back. `presence` says whether a voice is present at
all, and for a voice standing over another it is **zero at both of that voice's doors**: the voice
joins a running picture without replacing it and stands down the same way. At no instant is one
picture weighed against another. A plan cannot use it to fade, because a plan that drove it to a
half at a door would be refused by the very door proof described below.

## The two door laws

Every door proof in the fleet was written against one law: at a door the frame must be the departing
work, or the arriving work, **at every point**. That law is correct for the lowest voice of a stack,
which is drawn onto the cleared buffer with blending disabled and must fill the frame. It is the
opposite of what a voice standing above another owes, whose door must be **absent at every point** so
that what stands beneath is what the door shows, whole and untouched.

Until this landed there was one law, and it was the reason `overlay` — the one instrument that
already carried the right handle — had its own proof refuse a zero-presence entry door.

**An instrument cannot know which law it owes**, because it cannot see where it stands. The host can:
`rec.voices` is held in draw order, ascending stack, so its first entry is the lowest voice. The
frame state each voice receives now carries `standsOver`, and each door proof reads it:

```js
var absent = st.standsOver && !(h.presence > 0);
if ((h.mix === 0 || h.mix === 1) && !absent) { ...the whole-work proof... }
```

A voice standing over another at no presence has no reading to take of a frame it never drew into,
and the whole-work proof would otherwise refuse it for doing exactly what its own law asks.

**The lowest voice keeps the old law, and the host states it.** A score whose lowest cue names a door
at zero presence is refused before it is taken (`presenceWhyNo` in `engine/assets/pass-layer.js`):
nothing stands beneath the lowest voice, so a door it draws nothing at is a door the visitor sees the
page through. It is checked for a one-cue score as well as for a stack — a lone voice is its own
lowest, and the coverage law's exemption for a one-cue score does not extend to this.

## What an instrument owes

Seven things, all inside its own file, and the shape is identical across the fleet.

1. `uniform float uPresence;` in the fragment shader.
2. The published alpha multiplied by it — one line, and the colour channel untouched, so a one-cue
   score stays byte-identical.
3. `{ name: "uPresence", type: "float", source: "handle:presence" }` in the pass's uniforms.
4. The `presence` handle in the manifest, worded as above.
5. `presence: 1` in the manifest's `neutralPose`.
6. `presence: h.presence` carried into the pose the instrument hands to `st.draw`. This matters: the
   host binds `handle:` uniforms from that pose object, not from `st.handles`.
7. The door proof reading `st.standsOver`, as above.

## What the composer needs, and it is not in this tree

`engine/assets/pass-composer.js` belongs to another worker. Two things are needed there.

**A register row.** The composer's handle register maps a handle name to a kind and a sentence saying
where its value comes from — `mix: ["progress", "the pass's own progress, door to door"]`,
`mask: ["module-rest", "a judge channel the module rests shut"]`. `presence` needs one row of the
same shape. Its value is not a reading of either photograph and it is not a module rest: it is the
plan's own statement of when a voice is in the frame, driven from the cue's own progress rather than
the pass's. The nearest existing kind is `progress`, and whether it wants a kind of its own — the
cue's progress as against the pass's — is that file's own call. The sentence should say: nothing at
the cue's own two doors, whole across its middle.

**A plan shape.** Any cue that is not the lowest of its stack must name both of its doors on
`presence` at 0 and drive `presence` from zero, up, and back to zero across its own window. The
worked example is in `tests/test_pass_seam.py`: a spline over `cueProgress` through (0, 0),
(0.5, 1), (1, 0), with `doors` naming `presence` at 0 on both sides.

One further note for that worker, learned from the bench. An instrument reads itself to be **at** a
door when its crossing dial stands at one of that dial's own two ends. A cue that pins its dial at a
constant therefore reads itself at a door on every frame of its window and runs its door proof
continuously. An upper voice's dial should run across its own window like any other letter's.

## Two things a reader will trip on, found while working through the ten shaders

**`adrift` disagrees with the host about the blend.** Its own comment beside the alpha says the host
lays a cue down with `ONE, ONE_MINUS_SRC_ALPHA` and hands colour over premultiplied; the host uses
`SRC_ALPHA, ONE_MINUS_SRC_ALPHA` and its own comment states that a premultiplied shader is refused
because it would write black wherever alpha stands below one. One of the two is wrong and the code
was not touched for it — the entry-door change gates `adrift` at its alpha's own definition, which is
correct under either blend and takes no position on which. Whoever owns `adrift` should settle it.

**`ownTheLevels` reads `cue.instrument.id` unguarded** (`engine/assets/pass-composer.js`). A cue
without an instrument throws rather than being answered about. Every cue of a real composed passage
carries one, so no visitor meets this; a caller composing synthetic cues does, and one did.

## What is landed and what is not

Landed: the host's two laws and the `standsOver` reading; the contract in `overlay` (which needed
only the door-law guard) and in the eight instruments named in the report accompanying this document.
The seam check's six handoffs all read at their own measured floors.

Not landed here: the plan validator of ladder step 4, which is what makes the contract enforceable
against a plan rather than reported on. Until it exists, a plan that stands a voice over another
without driving its `presence` from zero is a defect the seam check reports and nothing refuses.
