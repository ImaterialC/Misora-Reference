# MESSAGE TO QWEN — PHASE 3 PROMPT STRATEGY REVIEW

Qwen,

I have reviewed your Phase 3 proposal (`Phase3_QwenVersion.md` and the S01/S02 prompt examples), Gemini's 17-session kit, GPT's Group A–G/Teamwork approach, and Grok's 23-session sequential approach.

I agree with several of your principles:
- Planning-first execution with a human Proceed gate.
- Failing-first regression probes and pre-existing regression guards.
- Explicit allowed and forbidden file ownership.
- ASCII-friendly prompt text and integrity checks.
- Conservative model routing, with GPT-OSS 120B used primarily for independent review rather than high-risk implementation.

However, I do not consider the current Qwen proposal ready for execution. Only S01 and S02 are fully drafted; the remaining sessions still need complete prompts.

## Required review and corrections

**1. Review the DEP-1 ordering issue.**

Your proposal places BUG-31 (Treeview theme) in S13 while BUG-07 is in S04. BUG-07 modifies the existing ScriptPastePreviewDialog Treeview integration.

The locked ledger requires BUG-31 before Treeview UI work.

Please determine the safest correction. My initial recommendation is to move BUG-31 before BUG-07 in S04, or place it in an earlier dedicated session. Do not merely explain the dependency away.

**2. Compare session granularity.**

Please compare your 20-session structure against:
- Gemini's S01–S17.
- Grok's S01–S23.
- GPT's A–G milestones.

Recommend the best session boundaries based on coupled source changes, file ownership, testing and rollback. Do not optimize for the smallest session count alone.

**3. Complete the prompt strategy.**

For each session, require:
- Exact canonical ledger IDs.
- Context pointers and source files.
- Allowed and forbidden file ownership.
- Preflight checks.
- Failing-first probes and regression guards.
- Exact verification commands.
- Mandatory stop conditions.
- Handoff conditions to the next session.

Make sure each ID is mapped exactly once, but also check that no acceptance criterion has been omitted merely because its ID appears in the coverage table.

**4. Preserve the locked project decisions.**

Do not reopen:
- Binary command IDs 35 and 32.
- Separate adjacent narration boxes after clearing a speaker.
- Multi-segment editing and segment-aware Undo.
- References-only `.misora` v1.
- The two-Text-widget All Script MTL design.
- The separate Import from XUAT workflow.
- The 50 digit-width / 4+ line overflow behavior.

**5. Revisit cheap-model safety.**

Distinguish between:
- Read-only discovery.
- Mechanical implementation with exact tests.
- High-risk implementation involving binary serialization, AST identity, transactional CSIF, Undo, concurrency, and XUAT identity.
- Independent adversarial verification.

Do not classify a task as Flash-safe merely because the prompt is long and detailed. Consider the consequences of an incorrect change.

## Expected response

Please return:
1. Your revised recommended session architecture.
2. A dependency audit identifying any inversions.
3. A model-routing recommendation using only the user's available models.
4. A list of required corrections to your S01/S02 examples.
5. A clear statement of which prompts are complete and which remain drafts.

Do not edit Misora-Editor source code. Do not generate another ZIP yet. This is an inter-AI design review only.

Use the locked Phase 2.5 ledger as the authority. Distinguish facts verified from source from recommendations and assumptions.

Your task is to challenge the other approaches, not to defend your original proposal automatically.