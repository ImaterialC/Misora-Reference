PHASE 2 — CROSS-EXAMINATION (ROUND `[1/2]`)

Baseline: `[40_CHAR_SHA]`
Peer Dossiers: `[BUNDLE_OR_MANIFEST_URL]`
Lead Rulings: `[RULINGS_OR_"None"]`

Rules:
- Do NOT repeat Phase 1. Verify peer claims in live code before agreeing.
- Resolve `[NEEDS-VERIFY (CROSS-FILE)]` items from scoped batches.

Output (strictly 3 sections, concise):
1. Peer & `U-xx` Verdicts: `[ID]` -> `AGREE` (add dedup alias if duplicate) | `DISAGREE` (cite live code) | `NEEDS-VERIFY` | `REFINE`.
2. Newly Surfaced Traps / Missing `DEP` Edges (if any).
3. Remaining Unresolved Points (max 1-3 items needing Lead ruling, or `NONE`).
End: `PHASE 2 R[N]: COMPLETE` | `READY FOR PHASE 3 LEDGER`
