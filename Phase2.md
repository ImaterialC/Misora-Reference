# Phase 2 — Cross-Review and Canonical Findings Ledger

**Purpose:** combine independent AI research and owner findings, verify them against evidence, resolve duplicates, and record disagreements honestly.

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
- `templates/COUNCIL_MESSAGE.md`

## Inputs supplied by the owner

The owner will manually provide:
- Every participating AI's Phase 1 report.
- The owner's own findings and observations.
- Any additional screenshots, logs, test results, or clarifications.
- The list of AIs that are active in this review.

Do not assume you can retrieve the other AI conversations yourself. Use only the material the owner actually provides.

## Review method

1. Read all supplied independent reports before forming a council-wide conclusion.
2. Create a finding register with stable IDs. Preserve source attribution: which AI or owner first raised each item.
3. Compare each finding against primary evidence. Reopen source files and reproduce behavior when feasible.
4. Merge true duplicates while retaining aliases and provenance.
5. Split findings that combine multiple unrelated defects or features.
6. Identify contradictions, missing evidence, incorrect assumptions, and unsupported claims.
7. Separate current bugs, regressions, missing core features, new feature proposals, risks, constraints, and open questions.
8. Do not treat repeated claims as independent proof.
9. Do not convert owner-reported behavior into a code-confirmed fact unless evidence confirms it.
10. Record disagreements without forcing a false consensus.

## Allowed dispositions

Use the status vocabulary in `docs/DECISION_AND_STATUS_MODEL.md`, including:
- `CONFIRMED`
- `PARTIALLY_CONFIRMED`
- `USER_REPORTED`
- `DISPUTED`
- `DUPLICATE_OF`
- `NOT_REPRODUCED`
- `PROPOSAL`
- `UNKNOWN`
- `RETRACTED`

Every finding must have a reason for its status and a next verification action where needed.

## Required output

Produce:
1. An updated canonical findings ledger using `templates/PHASE2_FINDINGS_LEDGER.md`.
2. A list of unresolved disagreements and the evidence needed to settle each.
3. A list of owner decisions required, if any.
4. A shareable English council message using `templates/COUNCIL_MESSAGE.md`. Save or attach it as a downloadable Markdown file when your surface supports file creation; otherwise provide the full Markdown in one clearly delimited block.
5. A list of the participating AIs whose reports have been included and whose reports are still missing.

Each active AI reviews the same consolidated packet. The owner copies the resulting council messages between AIs manually.

## Phase 2.5 gate

Phase 2 cannot be considered complete until the mandatory Phase 2.5 exhaustive reconciliation gate has been performed. Follow `Phase2.5.md` using the latest canonical ledger and all active AI inventories.

## Stop condition

Do not write implementation code or Antigravity execution prompts. Stop when the review packet is ready for Phase 2.5 or when a genuinely blocking owner decision is required. The owner controls the phase transition.
