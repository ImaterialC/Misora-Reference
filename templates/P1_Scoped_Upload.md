PHASE 1 SCOPED AUDIT — BATCH `[A/B/C/D1]` (UPLOAD-ONLY / LIMITED CONTEXT)

Project: `[PROJECT_NAME]` @ `[40_CHAR_SHA]` (`[VERSION]`)
ID Prefix: `[DS-A01..]` (match batch letter so merges never collide).
Relevant `U-xx` for this batch: `[PASTE_RELEVANT_U_ITEMS_OR_"General bug audit"]`

Rules:
1. Truncation check FIRST: verify every uploaded file reached EOF (quote final line of each code file). If any file was cut off, STOP with `BATCH: BLOCKED (TRUNCATED)`.
2. Cite `file -> symbol (ORIG lines X-Y)` (from part header if split).
3. Cross-file humility: tag `[CONFIRMED]` ONLY if provable inside uploaded files or `AGENTS.md`. If behavior depends on un-uploaded files/callers, tag `[NEEDS-VERIFY (CROSS-FILE)]` and name the external symbol for Phase 2 peers.
4. Hunt: data loss, encoding/atomicity, lock bypasses, threading/stale async races, undo/dirty order, exception swallowing, `AGENTS.md` violations. No Antigravity prompts yet.

Output (concise):
1. EOF Proof (1 line per uploaded code file).
2. Confirmed Bugs (`[DS-Xxx]`): Sev, Location, Mechanism, Minimal Fix + Test.
3. Cross-File Suspicions (`[DS-X-CVxx]`): `[NEEDS-VERIFY (CROSS-FILE)]`, Location, Risk, External Symbol to Check.
4. Wishlist (`U-xx` above only) & Hygiene notes.
End: `PHASE 1 BATCH [X]: COMPLETE`
