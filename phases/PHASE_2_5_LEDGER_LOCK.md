# Phase 2.5 — Canonical Ledger Lock & Anti-Hallucination Sync

## Objective
A **fast, strict synchronization gate** immediately after Phase 2 consensus and before Phase 3 prompt engineering.

In long multi-AI debates, small user requests or confirmed bugs are easily dropped, misnumbered, or silently mutated ("slug collisions"). Phase 2.5 guarantees that **every single AI holds the exact same, complete, hallucination-free master ledger** of everything agreed upon in Phase 2.

---

## Rules for Phase 2.5

1. **Zero New Brainstorming:** Do NOT introduce brand-new features or reopen settled arguments. Only list items explicitly agreed upon during Phase 2.
2. **100% Uniformity & Zero Omissions:**
   - Assign a single canonical ID to every accepted item:
     - `BUG-01`, `BUG-02`, ... (Confirmed bugs & data/thread safety fixes)
     - `FEAT-01`, `FEAT-02`, ... (Approved features & UX improvements)
     - `HYG-01`, `HYG-02`, ... (Repo hygiene, docs, config, cleanup)
     - `DEF-01`, `DEF-02`, ... (Explicitly deferred / measure-first items)
     - `NO-01`, `NO-02`, ... (Explicitly rejected / retracted / out-of-scope items)
   - Every item from Phase 2 MUST appear in one of those buckets — nothing vanishes silently!
3. **Anti-Hallucination Audit:** Each AI MUST double-check the compiled ledger against the Phase 2 transcript and source code and answer two explicit questions:
   - **Hallucination Check:** Does any item contain an unverified claim, retracted bug, wrong file/method name, or invented requirement?
   - **Omission Check:** Was any agreed bug, user manual finding, UX detail, or edge-case guardrail forgotten?
4. **Fast Convergence:**
   - Round 1 of Phase 2.5: Each AI outputs (or verifies against the first compiled) Canonical Ledger.
   - If ANY mismatch/omission/hallucination is found -> fix immediately and re-confirm.
   - Once **ALL AIs** confirm `PHASE 2.5 STATUS: LOCKED & IDENTICAL`, proceed immediately to **Phase 3**.
5. **Language Split:** Short status note to the user in **Indonesian**; canonical ledger + audit block in **English** inside **ONE single fenced `text` code block**.

---

## Required English Block Template

```text
# MISORA-EDITOR — PHASE 2.5 CANONICAL LEDGER LOCK

Reviewer: <AI Model Name>
Baseline Commit: <commit hash / version>

======================================================================
1. ACCEPTED BUGS (IN SCOPE)
======================================================================
| ID | Slug | Sev | Location | Agreed Behavior / Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- |
| BUG-01 | ... | P0 | `file.py:fn()` | ... |

======================================================================
2. ACCEPTED FEATURES & UX CHANGES (IN SCOPE)
======================================================================
| ID | Slug | Location | Agreed Spec & Guardrails |
| :--- | :--- | :--- | :--- |
| FEAT-01 | ... | `file.py` | ... |

======================================================================
3. REPO HYGIENE & DOCS (IN SCOPE)
======================================================================
| ID | Slug | Location | Agreed Action |
| :--- | :--- | :--- | :--- |
| HYG-01 | ... | ... | ... |

======================================================================
4. DEFERRED (MEASURE-FIRST / LATER CYCLE)
======================================================================
- DEF-01: <Item & trigger condition>

======================================================================
5. REJECTED / RETRACTED / EXPLICIT NON-GOALS
======================================================================
- NO-01: <Retracted finding or explicit user non-goal — DO NOT reintroduce>

======================================================================
6. ANTI-HALLUCINATION & OMISSION AUDIT
======================================================================
- Hallucinations / Unverified Claims Found: [NONE | List exact IDs]
- Omitted Phase 2 Items Found: [NONE | List exact missing items]
- Ledger Parity With Peer AIs: [IDENTICAL | MISMATCH — see diff]

PHASE 2.5 STATUS: [MISMATCH FOUND | LOCKED & IDENTICAL]
```
