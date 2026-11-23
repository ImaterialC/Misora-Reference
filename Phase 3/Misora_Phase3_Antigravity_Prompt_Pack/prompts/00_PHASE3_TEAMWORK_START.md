# PHASE 3 — MASTER TEAMWORK START PROMPT

```text
/teamwork

Project: Misora-Editor Phase 3 — implementation of the locked v1.4.x stabilization and UX ledger.
Purpose: Production-grade stabilization and implementation of the accepted Misora-Editor scope.

AUTHORITATIVE REFERENCES (READ BEFORE PLANNING)
1. Canonical locked ledger (highest authority for scope and acceptance):
   https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Phase_2.5_Canonical_Ledger_LOCKED.md
   Expected ledger blob SHA: e51291724d485eebbe18142f68ecdc4fdf4a7c1b
2. Target repository: https://github.com/ImaterialC/Misora-Editor
3. Expected pinned target baseline in the ledger: 683724edaf2afac89d2695a80e30a471a0da9195
4. Local source workspace: D:\Misora-Editor
5. Read the repository's existing AGENTS.md, PROJECT_STATE.md, README.md, tests/, core/, misora.py, and relevant assets/ before proposing any implementation.

PROJECT PHASE CLARIFICATION
We are in PROJECT PHASE 3: implementation. Phase 2.5 is already locked and must NOT be reopened. Do not reinterpret Teamwork's internal “Phase 1 / Phase 2” terminology as the Misora project phase number. Teamwork's own scoping and execution stages are merely its orchestration mechanism.

LOCKED SCOPE
Implement only canonical IDs present in the locked ledger:
- BUG-01..BUG-41
- HYG-01..HYG-08
- FEAT-01..FEAT-14
- Respect DEF-01..DEF-10 and NO-01..NO-12 as deferred, conditional, or forbidden exactly as written in the ledger.
Do not invent additional features, reopen Project Lead decisions, or silently alter requirements.

LOCKED HARD GUARDRAILS
- Preserve binary cmd_id 35 (narration) and cmd_id 32 (subtitle) unchanged across every path until a real production .unity3d fixture proves otherwise. Do not relabel or remap them based on guesses.
- Clearing a speaker must never merge adjacent narration boxes. Distinct boxes remain distinct through edit, save/reload, and Undo/Redo.
- Multi-segment editing stays available and non-blocking; segment-aware Undo/Redo must preserve old/new segment splits. Preserve complete BoxSnapshot data (seg_texts, voice_cue, extra_args).
- .misora v1 stores workspace references/state/stable lock identities only. Never embed unsaved drafts or .unity3d blobs. Never serialize runtime Record.uid. Never silently transfer an unmatched lock.
- Raw Commands remains the exact pane name. It stays read-only until FEAT-11's explicit dependency gates pass.
- Native preview overflow is 50 digit-widths OR 4+ lines, with visible bleed and no automatic shrink. Box 0 Summary capacity remains unmeasured/deferred.
- MTL Drawer All Script layout is exactly two Text widgets: one read-only clickable list and one shared editable scratchpad.
- Import from XUAT is a separate Import-menu floating resolver, strictly sourced from BepInEx\Translation\en\Text, with explicit pre-apply list and one atomic Undo operation.
- Preserve unknown/meaningful commands and voice cues. Remove only positively identified empty structural breakers under the ledger's exact ownership rules.
- Never add a second Unity bundle writer or port the legacy batch pipeline.
- Never bundle copyrighted AtlasAdv artwork or build an emulator/reskin.
- No broad rewrite/modular split of misora.py in this cycle.

NON-NEGOTIABLE EXECUTION ORDER
Follow the locked dependency order and groups:
A. Baseline and docs/ledger hygiene (HYG-01 first).
B. AST, binary parser, v2, command IDs, structural ownership, multi-segment and CSIF transaction.
C. Per-document state, locks, Undo/Redo, mutation correctness.
D. Search/Replace matching, errors, snapshots, bounded project roots.
E. Immutable Japanese XUAT keys and atomic XUAT sync.
F. MTL async queue, stale-result identity, app lifecycle, logger, security, encoding.
G. UI bug fixes and accepted UX/features only after their dependencies and P0/P1 gates pass.
Do not ship dependent features early. Do not merge groups into one massive unreviewable patch.

PHASE 1 — SAFE PREFLIGHT (NO SOURCE EDITS)
Before making a Teamwork project copy or writing any source file:
1. Inspect D:\Misora-Editor and verify it is the intended repository.
2. Record `git rev-parse HEAD`, `git status --short --branch`, staged diff, unstaged diff, untracked paths, and relevant ignored fixture paths. Do not print secrets or config values.
3. Verify whether local HEAD is the expected pinned baseline or has advanced. If it differs, inspect the commit delta and classify it against the locked ledger. Never reset/checkout/clean to force the pinned SHA.
4. Discover the actual Python version, dependency/install approach, test discovery command, current test count, and baseline test result. Do not invent commands or claim tests ran if they did not.
5. Identify available production .unity3d fixtures without copying, publishing, or modifying them. If the required fixture is absent, mark fixture-gated items BLOCKED/NOT VERIFIED.
6. Report whether the working tree contains uncommitted or ignored local data. Do not discard, stash, overwrite, delete, or blindly copy it.
7. Teamwork uses a dedicated isolated project folder. Propose exactly how the source snapshot will be created from the inspected local repository and how local changes/fixtures will be preserved. If the source is dirty or contains ambiguous ignored data, STOP and ask for explicit approval before copying.

No source changes during preflight. Produce a concise Baseline & Workspace Safety Report and a traceability map from every canonical ID to its planned milestone.

TEAMWORK PROJECT CONFIGURATION
- Choose the General distributed-coding path, not the small iterative path.
- Integrity mode: `development` with strict project-specific no-mock/no-fabrication guardrails below. Do not choose benchmark mode because it would impose unrelated from-scratch/stdlib-only restrictions.
- Keep Teamwork's dedicated directory isolated. Do not write directly into the original D:\Misora-Editor working tree during the first implementation pass.
- Use read-only Explorers for baseline and cross-reference audits.
- Give Workers exclusive file/package ownership. No two Workers may edit the same file at once.
- Assign a Critic and Challenger who did not author the relevant fix. Assign an Auditor to enforce the locked ledger and real test evidence. Use Success Auditor at final delivery.
- Prefer Claude Opus 4.6 for orchestration/high-risk review, Claude Sonnet 4.6 for bounded implementation, Gemini 3.8 Flash Fast for read-only inventory/test mapping, and GPT-OSS 120B for independent adversarial diff review IF those exact models are selectable for those roles. If model routing is unavailable, state that limitation; never pretend it was configured.

MODEL SAFETY POLICY
Gemini 3.8 Flash Fast may perform read-only discovery, inventory, simple test enumeration, and documentation checks. Do not make it the sole designer or implementer for binary serialization, AST identity, transactional CSIF, Undo identity, asynchronous MTL races, DPAPI, or immutable XUAT keys. GPT-OSS 120B may challenge a diff but cannot overrule failing tests or replace production fixture evidence. High-risk changes need a strong reasoning model plus independent tests and adversarial review.

MILESTONE ACCEPTANCE GATES
For each milestone:
1. Map each touched canonical ID to exact files/functions/tests.
2. Reproduce the defect or state honestly why reproduction is unavailable.
3. Add a focused regression test that fails before the fix and passes after it, whenever a test can represent the behavior.
4. Implement the smallest root-cause fix. No unrelated cleanup.
5. Run focused tests, then the full discovered test suite. Record exact commands, exit codes, test counts, failures, and skips.
6. Run static/compile checks only where appropriate and report actual output.
7. Have a different agent inspect the diff and test failure paths, rollback paths, and preservation invariants.
8. Update the canonical execution matrix with PASS / FAIL / BLOCKED / NOT APPLICABLE and evidence links/paths.
9. Do not mark an item PASS merely because the code appears correct or a test was written.
10. Stop the milestone if a P0/P1 regression appears; do not continue to dependent features.

GLOBAL STOP CONDITIONS
Immediately stop the affected item and report evidence if:
- A fix would change cmd_id 35 or 32 without the required production fixture.
- A fix would delete/normalize unknown commands or meaningful interstitial records without proof.
- A required production fixture is missing or cannot be inspected.
- Tests cannot be run and no equivalent verification is available.
- A change requires dependency/schema/format/API changes not authorized by the ledger.
- The local source state differs from the expected baseline and the delta cannot be safely reconciled.
- A worker proposes broad rewrites, unbounded refactors, silent fallbacks, or test weakening.

FORBIDDEN ACTIONS
- Never run `git reset --hard`, `git clean`, destructive checkout, force push, or automatic commit/push.
- Never delete existing user data, local fixtures, backups, configuration, credentials, or ignored files.
- Never add new external dependencies without Project Lead approval.
- Never weaken/remove tests, skip failures, mock the code under test, fabricate screenshots/output, or change expected results solely to pass.
- Never mark unavailable game/Windows verification as passed.
- Never bundle secrets or local fixtures into artifacts or patches.

DELIVERABLES
At the end of every milestone, produce:
- Milestone report with canonical IDs and status.
- Exact source diff summary and changed-file list.
- Regression tests added/changed.
- Exact commands and real output evidence.
- Known limitations and fixture-gated items.
- A clean patch/diff artifact that can be reviewed and later integrated into D:\Misora-Editor.

At project completion, produce the final acceptance matrix for BUG-01..BUG-41, HYG-01..HYG-08, FEAT-01..FEAT-14, DEF/NO dispositions, and a separate list of items still BLOCKED. Do not push to GitHub. Do not claim Phase 3 complete while any required P0/P1 acceptance gate is failing or unverified.

SCOPING INTERVIEW RULE
The ledger already contains the Project Lead's settled decisions. Do NOT ask me to reconfirm them. Ask at most one question at a time, and only when a critical local fact cannot be discovered safely from the repository (for example, the disposition of an uncommitted local change that must be copied into the Teamwork workspace). Otherwise inspect first and state your assumptions.

First action: complete the SAFE PREFLIGHT and prepare the reviewable Teamwork prompt artifact. Do not start implementation until I approve that artifact.
```
