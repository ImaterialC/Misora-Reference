# Phase 3 — Antigravity Prompt Engineering & Session Slicing Debate

## Objective
Transform the locked Phase 2.5 Canonical Ledger into **execution-ready Google Antigravity prompt(s)**. In this phase, AIs debate the **execution strategy** — NOT whether a bug/feature exists (that was locked in Phase 2.5).

---

## What AIs Must Debate & Finalize in Phase 3

1. **Session Slicing & Dependency Order:**
   - How many Antigravity sessions (`Session 1`, `Session 2`, ... / `S1`, `S2`, ...) should this cycle be split into so each prompt stays focused, safe, and reviewable?
   - Verify strict dependency ordering (e.g., data integrity/contracts before features that depend on them).
   - Map EVERY `BUG-*`, `FEAT-*`, and `HYG-*` ID from Phase 2.5 to **exactly one** session (100% coverage table).
2. **File Ownership & Guardrails:**
   - Define exact allowed files vs. forbidden (`DO NOT modify`) files per session.
   - Ensure compliance with `ANTIGRAVITY_GUIDE.md` (`/plan` Planning-First Gate, no destructive git commands, no new deps, no test weakening).
3. **Verification & Test Strategy:**
   - Specify exact failing-first **Probes** vs. pre-existing **Regression Guards** (remember: Guards must never reference new post-patch attributes!).
   - Specify exact Windows verification commands (`py -3.12 -m compileall ...`, `py -3.12 -m unittest ...`).
   - Note any known environment quirks (e.g., untracked local config files, modal dialog suppression).
4. **Prompt Quality Cross-Check:**
   - Review peer drafts honestly. Which prompt is clearest, tightest, least prone to hallucination or over-engineering?
   - Merge the best parts until **ALL AIs agree on the exact same final Antigravity prompt(s)**.

---

## Strict Exit Condition

Phase 3 ends ONLY when:
1. All AIs confirm 100% coverage of the Phase 2.5 Canonical Ledger.
2. All AIs agree on session order, test plan, and exact prompt wording (`PHASE 3 STATUS: APPROVED & IDENTICAL`).
3. The User approves the final prompt(s) to launch Phase 4.

---

## Required Output Structure

- **To User (Indonesian):** Brief summary of the proposed session roadmap, key trade-offs, and whether you approve moving to Phase 4.
- **Inter-AI Block (English, inside a single fenced `text` block during debate):**
  - Session Coverage Table (`Phase 2.5 ID -> Session #`)
  - Critique of peer session order / test strategy / prompt guardrails
  - Draft or Final Prompt(s) following `templates/ANTIGRAVITY_PROMPT_TEMPLATE.md`
  - Mandatory closing tag:
    `PHASE 3 STATUS: [OPEN — DEBATING PLAN/PROMPTS | APPROVED & IDENTICAL]`
