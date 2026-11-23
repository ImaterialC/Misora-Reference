# Changelog — Misora Editor

All notable changes to `Misora-Editor` are documented in this file.
Every Phase 3 session (`S01..S23`) appends a summary under `## [Unreleased] (Target: v1.4.1)`.
`__version__` in root `__init__.py` remains `1.4.0` during `S01..S23` and bumps ONCE to `1.4.1` in `S24` (Final Acceptance Audit & Release).

## [Unreleased] (Target: v1.4.1)

### S01 — Docs, Ledger & AGENTS.md Reconciliation
- **Ledger IDs:** `HYG-01`
- **Summary:** Reconciled `PROJECT_STATE.md`, `README.md`, and `AGENTS.md` against pinned baseline `683724edaf2afac89d2695a80e30a471a0da9195`; initialized `CHANGELOG.md`.
- **Files Changed:** `PROJECT_STATE.md`, `README.md`, `AGENTS.md`, `CHANGELOG.md`
- **Verification:** `py -3.12 -m compileall -q misora.py core assets tests` & `py -3.12 -m unittest discover -s tests -v` (record actual count)
- **Blocked / Skipped:** None

---

## [1.4.0] - 2026-11-23
- Baseline release pinned at commit `683724edaf2afac89d2695a80e30a471a0da9195` (Phases 1–7 / S0–S9c historical baseline; see `PROJECT_STATE.md`).
