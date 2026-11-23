# Phase 4 — Antigravity Execution Feedback and Verification

**Purpose:** evaluate the actual result of an owner-approved Antigravity execution slice. This phase is an execution-feedback loop, not another multi-AI design debate.

## Required reading

Read:
- `README.md`
- `AGENTS.md`
- `docs/PROJECT_MANDATE.md`
- `docs/WORKFLOW_RULES.md`
- `docs/RESEARCH_AND_EVIDENCE.md`
- `docs/ANTIGRAVITY_EXECUTION_RULES.md`
- `templates/PHASE4_EXECUTION_REVIEW.md`

## Inputs from the owner

The owner will provide as available:
- The approved Phase 3 slice and exact Antigravity prompt.
- Antigravity's response and execution summary.
- Changed-file list and Git diff.
- Test commands, outputs, screenshots, logs, and errors.
- Any follow-up questions from Antigravity.

Do not assume you can inspect the local workspace. If the owner has not supplied a diff, file, screenshot, or log, say what is missing.

## Review tasks

1. Verify whether Antigravity followed the approved scope and file boundaries.
2. Compare each changed file with the task objective.
3. Check acceptance criteria one by one.
4. Evaluate test quality and distinguish passed, failed, skipped, and not-run tests.
5. Look for regressions, incomplete code paths, unsafe assumptions, error handling gaps, and data corruption risks.
6. Identify whether a claimed fix is actually demonstrated by a test or only described.
7. Check whether documentation, versioning, configuration, and backward compatibility were handled where required.
8. Give the owner a concise Indonesian explanation and exact next action.
9. If necessary, produce one narrowly scoped English follow-up prompt for Antigravity.

## Required output

Use `templates/PHASE4_EXECUTION_REVIEW.md`. Include:
- Slice ID and approved objective.
- Files changed.
- Scope compliance.
- Acceptance criteria table.
- Tests passed/failed/skipped/not run.
- Verified defects or risks.
- Missing evidence.
- Verdict: `ACCEPT`, `ACCEPT WITH FOLLOW-UP`, or `REJECT / REWORK`.
- Exact next prompt or manual action, if any.

## Debate boundary

Do not restart Phases 1–3 or reopen the entire council debate for an ordinary implementation question. Reopen a finding or planning decision only when new evidence materially changes the scope, architecture, severity, or approved approach. Tell the owner why the earlier gate needs to be revisited.

## Stop condition

Review only the execution material supplied for the approved slice. Stop after your verification and recommendation. The owner decides whether to send a follow-up prompt, accept the slice, or request another council review.
