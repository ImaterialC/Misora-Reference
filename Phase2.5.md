# Phase 2.5 — Exhaustive Reconciliation Gate

**Purpose:** prove that the canonical review ledger contains every in-scope item and that no AI has introduced unsupported or hallucinated work.

This is a mandatory sub-gate inside Phase 2. It is a short, strict completeness audit — not an implementation-planning phase.

## Required reading

Read:
- `README.md`
- `AGENTS.md`
- `docs/PROJECT_MANDATE.md`
- `docs/WORKFLOW_RULES.md`
- `docs/RESEARCH_AND_EVIDENCE.md`
- `docs/DECISION_AND_STATUS_MODEL.md`
- `docs/CURRENT_SESSION.md`
- `templates/PHASE2_FINDINGS_LEDGER.md`
- `templates/PHASE2_5_COMPLETENESS_AUDIT.md`

## Inputs

The owner supplies the latest canonical Phase 2 ledger, all Phase 1 reports, all owner findings, and every participating AI's independent Phase 2.5 inventory.

## Required independent inventory

Without simply copying the ledger, enumerate every item in scope under these headings:

1. Confirmed bugs and regressions.
2. Partially confirmed and user-reported bugs.
3. Missing core features.
4. Proposed new features and enhancements.
5. Risks, constraints, and architectural dependencies.
6. Open questions and items not reproduced.
7. Explicitly excluded or deferred items.

For each item, include its ID, short description, evidence/status, and source attribution.

## Reconciliation

Compare your inventory against:
- The canonical Phase 2 ledger.
- Every other active AI's Phase 2.5 inventory.
- The owner's original findings.
- The source evidence and scope in `docs/CURRENT_SESSION.md`.

Identify:
- Missing items.
- Duplicated items that should be merged.
- One ledger item that incorrectly combines multiple issues.
- Unsupported or hallucinated claims.
- Wrong or overstated status labels.
- Owner findings omitted or distorted.
- Items accidentally excluded from the current scope.
- Unresolved contradictions.

Every difference must be reconciled by ID. Do not report only a general impression.

## Required completion statement

Use `templates/PHASE2_5_COMPLETENESS_AUDIT.md`. State:
- Your total item count by category.
- Which ledger IDs match.
- Which items are missing or disputed.
- Whether any unsupported claim must be removed or downgraded.
- Whether the canonical ledger is exhaustive.

Use exactly one of these verdicts:
- `PASS — EXHAUSTIVE`: no unmatched in-scope items remain; no unsupported claims remain presented as facts.
- `PASS WITH RECORDED DISPUTES`: the inventory is complete, but named disagreements remain explicitly recorded as disputed/unknown and have an owner-approved treatment.
- `FAIL — RECONCILIATION REQUIRED`: at least one omission, unsupported claim, count mismatch, or unresolved classification remains.

## Stop condition

Do not proceed to Phase 3 unless every active AI and the owner have reviewed the reconciliation result and explicitly agree that the ledger is exhaustive, with all remaining disputes and unknowns recorded. Agreement does not mean every finding is confirmed. Never manufacture consensus.
