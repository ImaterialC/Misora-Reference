# MULTI-AI ENGINEERING COUNCIL — PHASE 4 (DRAFT COMMAND ARCHITECTURE — 2-EXEMPLAR RULE)

Project: **[PROJECT_NAME]** | Target Executor: **Google Antigravity**
Locked Canonical Ledger: `[LEDGER_URL]` (SHA-256: `[LEDGER_SHA256]`)

## IMPORTANT — 2-EXEMPLAR RULE (DO NOT GENERATE A FULL 20+ PROMPT ZIP YET!)
To save quota and eliminate wasted rework, do **NOT** generate every session prompt in Phase 4. Instead, submit ONLY:
1. **Complete Session Roadmap Table (`S01..SNN`):**
   - Exact 1:1 mapping of ALL canonical IDs (`BUG`/`FEAT`/`HYG`) — zero duplicates, zero omissions.
   - Strict respect for `DEP-1..DEP-N` and serial file ownership on high-collision files.
   - Recommended AI model per session (e.g., Opus for high-risk core/threading, Sonnet for standard, Flash for docs/mechanical only).
   - Target test module per session + single release-gate session (`SNN`) at the very end.
2. **Antigravity Safety & Execution Strategy:**
   - Planning-first gate (`/plan` -> review -> `Proceed`), symbol-binding (anti-line-rot), failing-first TDD Probes vs Regression Guards, `ALREADY PASSING` stop rule, `BLOCKED != PASS` release gate, and local workspace/git safety rules (`.agents/rules/` & `/skills` — NO unverified fail-open hooks!).
3. **Exactly TWO Full Prompt Exemplars:**
   - **Exemplar A:** One lightweight / docs / hygiene session (e.g., `S01`).
   - **Exemplar B:** One high-risk core / multi-file session (e.g., binary/AST/threading or flagship feature).

End with: `PHASE 4 STATUS: DRAFT ARCHITECTURE SUBMITTED`
