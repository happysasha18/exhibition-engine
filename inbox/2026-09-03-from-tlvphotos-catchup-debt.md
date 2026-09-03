# Wish: exhibition-engine's own live-spec catch-up debt

**From:** a session working in `~/tlvphotos`, closing PLAN.md row S-51 (tlvphotos' own
2.7.0 → 6.1.0 live-spec catch-up walk), 2026-09-03. This session did not touch `~/exhibition-engine`
beyond creating this `inbox/` directory (it did not exist) and writing this one file, per the pair's
own routing law (a walk covers exactly one repository).

## The gap

`~/exhibition-engine/.live-spec/installed.md` records pack **1.0.14**, from its first adoption
(2026-07-12). The pack's `VERSION` today is **6.1.0**. This host is live — active commits are landing
on it (seen from tlvphotos' side while this walk ran: `a2ee99a`, `41a869f`, `c774679`, `f5592db`,
`f13ebc5`, all 2026-09-03-dated work on `engine/build.py` and its test suite) — so this is not a
dormant tree that can wait indefinitely; it is the shared engine tlvphotos' own bake depends on
(`tests/engine_build.py` imports `~/exhibition-engine/engine/build.py` directly), running roughly
five and a half releases behind its own recorded pack.

No file in `~/exhibition-engine` was read closely enough by this session to say what the catch-up
walk there would find (tlvphotos' own walk — `.live-spec/adopt/2026-09-03-catchup-6.1.0.md` — is
the template: baseline fingerprint, skill sync via `sync-skills.sh`, external-prover install, the
citation sweep, `installed.md` rewritten from disk). Naming the debt is this wish's whole job; running
that walk is a separate piece of work for whoever holds this repository next.
