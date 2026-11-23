# MILESTONE B — AST, BINARY, V2, STRUCTURAL OWNERSHIP & CSIF

```text
/plan

Implement Milestone B only from the locked ledger: BUG-01..BUG-09 and HYG-04 where safe. Follow DEP-5 prerequisites. Do not implement Raw Commands editing (FEAT-11) in this milestone.

Authoritative ledger:
https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Phase_2.5_Canonical_Ledger_LOCKED.md

Primary scope:
- BUG-01 strict binary parse; reject truncated/trailing malformed records rather than silently returning partial AST.
- BUG-02 kind conversion must preserve the target primary Record.uid and never merge separate adjacent narration boxes. Clearing a speaker retains distinct boxes.
- BUG-03 lossless v2 representation, cmd_id 0 preservation, whitespace/category collision handling, invalid UTF-8 surrogate representation, and Raw Commands metadata highlight correction.
- BUG-04 readable command labels vs numeric command identity; structural breaker classification by verified numeric IDs. HARD GUARDRAIL: cmd_id 35 and 32 remain unchanged everywhere.
- BUG-05 unified breaker/voice-cue ownership for insert/delete/move and exact structural Undo snapshots.
- BUG-06 segment-aware edit Undo/Redo and full internal BoxSnapshot preservation.
- BUG-07 atomic sparse CSIF validation/application, apply_metadata checkbox, stable target Record.uid capture, exact preview/undo indices, full rollback.
- BUG-08 CSIF escape backslash parity.
- BUG-09 non-target bundle verification is fixture-gated. Investigate only with genuine production fixtures.
- HYG-04 removed_records lifecycle only after proving undo/rollback no longer depends on tombstones.

Mandatory safety constraints:
- Do not change binary IDs 35 or 32. No speculative mapping to 9 or 61.
- Do not alter the empty-argument space sentinel (DEF-01) without live-client evidence.
- No command-specific arity assertions; unknown commands and arguments must remain preservable.
- Unknown/interstitial commands must not be deleted as if they were empty tap breakers.
- Preserve cmd_id 12 vo_ voice cue attachment exactly under the ledger contract.
- Use staged/transactional mutation for sparse CSIF; failure must leave the original document unchanged.
- Do not add a second bundle writer or port legacy packer code.
- Do not enable FEAT-11 Raw Commands editing before all DEP-5 gates pass and are accepted in a later milestone.

Test strategy:
Add regression tests for truncated headers/lengths/payloads; command 0; IDs 35/32; speaker-clear adjacent narration separation; move/delete voice cues and breakers; multi-segment edit/paste/undo; sparse CSIF targets and metadata suppression; invalid sparse rollback; 0..3 leading backslashes before @@; surrogateescape v2 round trips.
Use synthetic tests for deterministic logic. Use real production fixtures only for format/game compatibility claims.

Deliverable and gate:
Show exact tests and output, source diff, and independent Critic/Challenger findings. Any fixture-dependent condition is BLOCKED, not PASS. Do not begin Milestone C until all non-fixture P0/P1 items in this milestone pass and the Project Lead reviews the report.
```
