# Canonical Ledger Template (Phase 2.5)

Use this exact structure during **Phase 2.5** so every participating AI outputs an identical, machine-comparable master list.

```text
# MISORA-EDITOR — PHASE 2.5 CANONICAL LEDGER LOCK

Reviewer: <AI Model Name>
Cycle / Round: <e.g., v1.4.x Cycle 1>
Baseline Commit: <git commit hash of Misora-Editor>

======================================================================
1. ACCEPTED BUGS (IN SCOPE)
======================================================================
| ID | Slug | Sev | Location | Agreed Fix & Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- |
| BUG-01 | <slug> | P0 | `file.py:fn()` | <Exact expected behavior> |

======================================================================
2. ACCEPTED FEATURES & UX CHANGES (IN SCOPE)
======================================================================
| ID | Slug | Location | Agreed Spec & Guardrails |
| :--- | :--- | :--- | :--- |
| FEAT-01 | <slug> | `file.py` | <Exact UI/logic contract + non-goals> |

======================================================================
3. REPO HYGIENE & DOCS (IN SCOPE)
======================================================================
| ID | Slug | Location | Agreed Action |
| :--- | :--- | :--- | :--- |
| HYG-01 | <slug> | `...` | <Exact action> |

======================================================================
4. DEFERRED (MEASURE-FIRST / FUTURE CYCLE)
======================================================================
- DEF-01: <Description + condition to revisit>

======================================================================
5. REJECTED / RETRACTED / EXPLICIT NON-GOALS
======================================================================
- NO-01: <Description — MUST NOT be reintroduced in Phase 3>

======================================================================
6. ANTI-HALLUCINATION & OMISSION AUDIT
======================================================================
- Hallucinations / Unverified Claims Found: NONE
- Omitted Phase 2 Items Found: NONE
- Parity With Peer AIs: IDENTICAL

PHASE 2.5 STATUS: LOCKED & IDENTICAL
```
