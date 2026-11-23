# Phase 3 — Dependency-Aware Implementation Planning

**Purpose:** agree on implementation order and divide work into safe, testable Antigravity execution sessions. Phase 3 produces plans and prompts only.

## Required reading

Read:
- `README.md`
- `AGENTS.md`
- `docs/PROJECT_MANDATE.md`
- `docs/WORKFLOW_RULES.md`
- `docs/RESEARCH_AND_EVIDENCE.md`
- `docs/DECISION_AND_STATUS_MODEL.md`
- `docs/CURRENT_SESSION.md`
- `docs/ANTIGRAVITY_EXECUTION_RULES.md`
- `templates/PHASE3_EXECUTION_PLAN.md`

Proceed only after Phase 2 and the Phase 2.5 completeness gate have passed.

## Planning inputs

Use only the owner-approved canonical ledger, reconciled statuses, explicit scope decisions, and verified technical evidence. Do not reintroduce rejected or unsupported findings.

## Planning principles

1. Resolve blockers and critical defects in the existing Misora Editor before attempting a Datamine plugin integration.
2. Prioritize by severity, user impact, dependency order, risk, and testability — not by how interesting a feature sounds.
3. Keep each Antigravity session small, bounded, and independently verifiable.
4. Separate refactoring from behavior changes where practical.
5. Preserve source reference tools. Changes to the Misora Editor belong in the Misora Editor repository unless the owner explicitly approves otherwise.
6. Avoid implementing the entire Datamine scope in one prompt.
7. Explicitly identify tasks that require owner input, credentials, game data, or manual verification.
8. Never plan to expose secrets, private data, live databases, or copyrighted payloads in the public reference repository.

## Every execution slice must define

- Slice ID and objective.
- Ledger IDs addressed.
- Why this slice comes now and its dependencies.
- Exact target repository and allowed paths.
- Files or components that must not be changed.
- Expected user-visible behavior.
- Acceptance criteria written as testable statements.
- Unit, integration, regression, and manual tests as appropriate.
- Required test data and environment assumptions.
- Data migration or compatibility considerations.
- Rollback/recovery approach.
- Stop conditions and questions that must return to the owner.
- A complete English Antigravity prompt.

## Consensus process

Each active AI reviews the same proposed sequence. Record disagreements with evidence and alternatives. The owner decides any unresolved product preference or priority dispute. Do not force a unanimous technical claim without evidence.

## Required output

Use `templates/PHASE3_EXECUTION_PLAN.md`. Deliver:
1. Agreed priority order.
2. Dependency map.
3. Numbered Antigravity execution slices.
4. Acceptance criteria and tests for every slice.
5. Risks, rollback points, and owner decisions.
6. Copy-paste-ready English prompts for each approved slice.

## Stop condition

Do not edit code, modify repositories, or claim implementation has started. Stop and wait for the owner's explicit approval to send the first execution prompt to Antigravity.
