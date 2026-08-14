# Packsplit reconciled with the landed coverage law — 2026-08-14

Unit U1 of the V2 restart sequence (`docs/V2-RESTART-HANDOFF.md`). The branch that gave every
instrument a file of its own was standing one commit behind the coverage law, and the one file the
law was written into is the file this branch deleted. This is what was done, what was measured, and
what a reader should not take from it.

## The commits

| what | commit |
| --- | --- |
| base — the branch as it was handed over | `9a33b31` |
| the woven suite's two-line repair | `e21a057` |
| merged in — `pass-api-v1`, the integration reference | `e20029e` |
| result — the merge, resolved | `8dcfa53` |

This evidence file is committed on top of `8dcfa53`. Nothing was pushed and nothing was merged into
`pass-api-v1`: that merge belongs to the delivery seat.

## What was done

**The two-line repair (`tests/test_pass_weave.py`).** The table row read the running instrument
synchronously inside the offer call, where the host is still awaiting its instrument's own file and
names none, so it read empty. The name is now captured in the loop that already waits for the host
to go idle — the same loop, and for the same reason, that the curtain is read in. The row's other
claims are untouched.

**The merge (`e20029e` into `pass-api-v1-packsplit`).** One delete/modify conflict, expected:
`engine/assets/pass-pack.js` is deleted here and was modified at `8ccbf96`. It stays deleted, and
`8ccbf96`'s five hunks are carried over character for character into the files each instrument now
travels in:

- `pass-inst-weave.js` — the `coverage: { writes: false }` block, with its reason;
- `pass-inst-matter.js` — `coverage: { writes: true }` and the alpha `1.0 - cov`;
- `pass-inst-gears.js` — `coverage: { writes: true }` and the alpha `1.0 - cov`.

The port was checked both ways rather than by eye. Every non-wrapper line of the four instrument
files stands verbatim in `pass-pack.js` at `e20029e` — the only lines with no home there are the 33
per file that the split itself introduced (the file header, the `join` call, `INSTRUMENT_VERSION`,
the declaration record). And every line of that pack has a home in one of the four files, but for
the pack's own 30 wrapper lines. The weave floor's move from 8 to 6 with its `applied` record, which
the brief lists among the deltas to port, already stood on this branch and stands identically at
`e20029e`: nothing to carry.

`engine/assets/pass-layer.js` merged whole — the straight source-over blend, `coverageWhyNo` called
from `scoreWhyNo`, and the two diagnostic readers.

`tests/test_pass_stack.py` conflicted in three places. This branch's row 2 rebuilds a whole
arrangement from git — host, record, instrument files — and already carries `e20029e`'s repair in a
form that spans both arrangements, so it stands; `e20029e`'s coverage row replaces the superseded
opacity-debt row.

`tests/test_pass_coverage.py` arrived written against one pack and now reads the same eighteen rows
off the split arrangement: the shaders are read out of every built instrument file the site's record
names, a bench serves the host with that record and the files it names, and a red-on-bug revert
names the ONE file it cripples instead of counting occurrences inside a pack. No row was added,
removed or weakened.

`docs/design/COVERAGE.md` arrived citing `pass-pack.js` for its three shaders. Each citation now
names the file its own instrument travels in, at the same line counts.

## The commands, exactly

    python3 tests/test_pass_weave.py
    git merge e20029e            # resolved as above; git was never asked to restore a working tree
    python3 tests/test_pass_coverage.py
    python3 tests/run_all.py

## The results

**The woven suite alone: 43 of 43**, 0 failed, 0 skipped — the number the branch's own commit
expected.

**The coverage suite alone: 18 of 18**, 0 failed, 0 skipped, run before the merge was committed so
that its before-and-after rows stood against the genuinely pre-coverage arrangement at `e21a057`.
Its numbers reproduce `8ccbf96`'s to the last digit: the ground reaches 100.0% of the frame at
2.00 s and 15.8% at 5.00 s, the stack differs from the travelling voice alone by mean 42.478 of 255,
both doors agree at worst channel 0, the whole-frame-weight residuals stand at 39.70 and 21.64
channel units, and the 21 one-cue comparisons across three instruments and seven instants are exact.

**The full engine run: 55 of 55 suites green**, wall 247 s, exit 0. The census is the 54 the branch
recorded plus `pass_coverage`, which is the one suite `8ccbf96` added. Log:
`/Users/sashaabramovich/exhibition-engine-packsplit/docs/design/evidence/2026-08-14-packsplit-prover.log`.

## Equivalence: the split arrangement beside `e20029e`

One score — the one-cue score `test_pass_stack.py` measures row 2 on — played at both doors and the
middle instant, 0.0 s, 1.5 s and 3.0 s, on a 390×844 frame. The whole of the older arrangement was
rebuilt from git at `e20029e` and put through the very same steps `engine/build.py` puts the source
through: the pack, then the host stamped with that pack's version and the digest of the bytes the
bench actually serves, then that revision's own bench page.

| instant | mean | worst channel |
| --- | --- | --- |
| 0.0 s | 0.000000 of 255 | 0 of 255 |
| 1.5 s | 0.000000 of 255 | 0 of 255 |
| 3.0 s | 0.000000 of 255 | 0 of 255 |

Both benches drew a real picture rather than agreeing on an empty one: the frames carry a spread of
61.5 to 66.1 grey levels about a mean of 123 to 129. In the tree this measurement lives as
`test_pass_stack.py` row 2, which runs it against `HEAD` on every full run; this run read `e20029e`
in place of `HEAD` and changed nothing else.

## The byte fences

Every fence under its number. The gzip fences are `tests/test_budget.py`'s, the raw fences are
`tests/test_pass_pack.py`'s for the instruments and `tests/test_pass_api.py`'s for the host, and all
of them ran green inside the full run.

| file | raw | raw fence | gzip | gzip fence |
| --- | --- | --- | --- | --- |
| `pass-layer.js` (the host) | 85 069 | 86 000 | 23 327 | 24 000 |
| `pass-inst-adrift.js` | 18 842 | 20 700 | 5 444 | 6 000 |
| `pass-inst-gears.js` | 13 600 | 14 800 | 4 594 | 5 000 |
| `pass-inst-matter.js` | 9 661 | 10 500 | 3 279 | 3 550 |
| `pass-inst-weave.js` | 12 830 | 13 900 | 4 171 | 4 500 |
| `exhibition.js` (the walk's own bundle) | — | — | 67 985 | 68 000 |
| `exhibition.css` | — | — | 7 743 | 9 000 |

The coverage law cost the host 316 B gzipped, which leaves it 673 B of headroom; it cost the three
instruments between 58 and 128 B raw each. The walk's own bundle is untouched at 15 B under its
fence, as it was.

## Conclusion

The split arrangement and the pack arrangement at `e20029e` now draw the same picture from the same
score, to the pixel, with the coverage law standing in both. Every suite the engine has is green at
55 of 55, and every file is under its own fence. The merge into `pass-api-v1` is deliberately not
done here.

## Limitations

- **The coverage suite's before-and-after rows go quiet once this merge is committed.** They rebuild
  the arrangement at `HEAD`, and `HEAD` now carries coverage, so row 54 and the two evidence rows
  compare like with like and pass without separating anything. This is inherited from `e20029e`,
  where the same rows stand against a `HEAD` that already carries `8ccbf96`; it is not introduced
  here. The meaningful reading is the pre-commit run recorded above.
- The host's gzipped headroom is now 673 B. The next thing that lands in `pass-layer.js` should be
  weighed before it is written.
- `tests/suite_timings.json` is the full run's own record, replaced by that run as the runner's own
  note says it always may be.
