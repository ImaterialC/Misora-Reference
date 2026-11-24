# MULTI-AI ENGINEERING COUNCIL — PHASE 2 (CROSS-EXAMINATION & CRITIQUE)

Project: **[PROJECT_NAME]** | Pinned Baseline: `[40_CHAR_COMMIT_SHA]` | Round: **Phase 2 Round [1 / 2]**
Peer Dossiers to Cross-Check (via `MANIFEST_AUTO.md` / `_BUNDLE_Phase_1_Research*.md`):
`[PASTE_URLS_FROM_scan_meeting.bat]`

Project Lead Rulings So Far (if any):
`[PASTE_LEAD_DECISIONS_OR_"None yet"]`

## Rules for Fast, High-Signal Cross-Examination (Max 2–3 Rounds)
- **No Repetition / No Fluff:** Do NOT rewrite your Phase 1 dossier. Respond ONLY with structured verdicts backed by direct source checks.
- **Verify Before Agreeing:** If a peer cites a bug or line range you did not check, verify it in live source before marking `[AGREE — CONFIRMED]`.
- **Expose Blind Spots & Over-Engineering:** Catch duplicate IDs across peers, false positives, risky refactors, missing edge cases, and conflicting proposals.

## Required Output Structure (Strictly 3 Sections + Open Questions)
### 1. Item-by-Item Peer Verdicts
For each peer finding (`[PEER-ID]`):
- `[AGREE — CONFIRMED]` (optionally add refinement or dedup alias `= [MY-ID]`)
- `[DISAGREE — DISPROVEN]` (cite exact live code proof)
- `[NEEDS-VERIFY]` (state exact test/fixture needed)

### 2. Newly Surfaced Traps / Missed Items
- Only genuinely new bugs, dependency edges (`DEP`), or test traps uncovered during cross-checking.

### 3. Proposed Consolidation & Remaining Disagreements
- Concise summary of where the panel already agrees vs. the exact 1–3 points still needing debate or Project Lead ruling.

End with: `PHASE 2 STATUS: ROUND [N] COMPLETE` (or `READY FOR PHASE 3 CANONICAL LEDGER`)
