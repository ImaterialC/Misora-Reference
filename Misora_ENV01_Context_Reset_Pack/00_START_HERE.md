# MISORA — ENV-01 Context Reset Pack

**Purpose:** establish a smaller, reliable AI working environment before further Misora feature work.

**Status:** proposal package prepared from the Project Lead's reports, prior review decisions, and the public repository material available on 2026-11-28. It is not yet an authorized repository migration and does not modify Misora-Editor.

## Current project snapshot

- Product: Misora: Story Editor for PriconneRe:TL.
- Repositories: `ImaterialC/Misora-Editor` and `ImaterialC/Misora-Reference`.
- Latest reported local checkpoint: S11e / `v1.4.15`, commit `ead65077a2a6cf3a664543cfb50f855268a29e2a`.
- Commit state: Project Lead says committed locally and not pushed. Last supplied PowerShell transcript confirms the commit; post-commit `git status --short` was not supplied.
- Last reported automated baseline: 475 discovered/executed; 432 PASS, 35 SKIP, 6 pre-existing FAIL, 2 pre-existing ERROR. Full single-process discovery completed at S11e.
- Current direction: pause S12 and all v1.5.0 release work; prioritize ENV-01 documentation/context layering, then bug/UI triage and approved fixes.
- `v1.5.0` is not approved for promotion. Preserve the decision to cancel/pause the current v1.5.0 and upcoming S15 work. Do not rewrite historical milestone records named S15 without confirming which S15 the council meant; the old Project State already contains a completed historical S15 entry.

## Read order for every AI task

1. `ai/AGENTS_MINIMAL_DRAFT.md` — permanent rules, short.
2. `project/PROJECT_STATE_MINIMAL_DRAFT.md` — current facts and immediate priorities, short.
3. `ai/CONTEXT_ROUTER.md` — select only the task-specific references and source files.
4. Relevant issue/decision/architecture note only. Do not load the history archive by default.

## What this package contains

- `ai/AGENTS_MINIMAL_DRAFT.md`: proposed compact root agent instructions.
- `ai/CONTEXT_ROUTER.md`: task-based context loading; avoids reading the full 1 MB `misora.py` by default.
- `project/PROJECT_STATE_MINIMAL_DRAFT.md`: proposed compact current-state dashboard.
- `project/DECISION_REGISTER.md`: current decisions and unresolved governance points.
- `triage/MASTER_BACKLOG_T01_T14.md`: triage assessment of the Project Lead's 14 items.
- `architecture/ENV01_BLUEPRINT.md`: proposed documentation structure, migration safeguards, and acceptance criteria.
- `project/NEXT_ACTIONS.md`: exact work sequence for the Project Lead and agents.
- `history/README.md`: rules for preserving, not deleting, historical records.

## Evidence labels

- **REPORTED** — stated by the Project Lead or Gemini; not independently run by this reviewer.
- **SOURCE-OBSERVED** — visible in a repository source/document fetched for this review.
- **CONFIRMED** — reproduced or supported by direct source plus a reliable test/observation.
- **NEEDS-REPRO** — plausible issue requiring a controlled reproduction on the current local HEAD.
- **PROPOSAL** — feature/UX idea, not a defect.
- **DEFERRED** — intentionally outside the current scope.

Do not silently upgrade REPORTED or NEEDS-REPRO to CONFIRMED.

## Important limitation

The S11e local commit is not pushed according to the Project Lead. Public GitHub `main` may therefore lag the working repository. All version, status, source, and test claims about the local checkpoint must be rechecked locally before changing files. This package is a planning aid, not a substitute for that preflight.
