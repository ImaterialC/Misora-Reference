# Finding IDs, Statuses, and Decisions

## Stable IDs

Use stable IDs within one review session:
- `BUG-001`, `BUG-002` — defects.
- `REG-001` — regressions.
- `CORE-001` — missing core capabilities.
- `FEAT-001` — feature proposals.
- `RISK-001` — risks.
- `Q-001` — open questions.
- `CON-001` — constraints.

Do not renumber an ID after it has been used in reports. If two findings merge, keep one canonical ID and list the other as an alias or `DUPLICATE_OF`. If one item splits, retain the original as a parent/reference and create new IDs.

## Evidence/review status

- `CONFIRMED` — supported by direct primary evidence or reproducible testing.
- `PARTIALLY_CONFIRMED` — some but not all parts are supported.
- `USER_REPORTED` — owner reports behavior, not yet independently reproduced.
- `DISPUTED` — credible evidence or interpretations conflict.
- `DUPLICATE_OF` — same underlying issue as another canonical ID.
- `NOT_REPRODUCED` — reproduction attempt did not demonstrate the issue; this does not automatically prove absence.
- `PROPOSAL` — desired capability, not an existing defect.
- `UNKNOWN` — insufficient evidence to classify.
- `RETRACTED` — claim withdrawn because it was incorrect or out of scope.

## Priority

- `P0` — critical data loss, security exposure, or blocker making the app unusable for its core purpose.
- `P1` — major functionality broken or required for the next planned milestone.
- `P2` — important but has a viable workaround or is not blocking the current milestone.
- `P3` — minor issue, polish, or later enhancement.

Severity and priority are different. A potentially severe issue may still need more evidence before it receives an implementation priority.

## Decision records

Every material decision records:
- Decision ID.
- Date/session.
- Decision statement.
- Evidence and linked finding IDs.
- Alternatives considered.
- Known trade-offs.
- Active AI positions and any dissent.
- Owner decision/approval.
- Conditions that would trigger reopening.

The owner is the product decision-maker. AI consensus informs but does not replace owner approval.
