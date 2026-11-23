# Changelog — Misora Editor

All notable changes to `Misora-Editor` are documented in this file.
- Every implementation session (`S01..S23`) appends `### SXX` under `## [Unreleased] (Target: v1.4.1)` while keeping `__version__ == "1.4.0"`.
- `S24` (Final Acceptance Audit & Release Gate) ALWAYS appends `### S24 — Final Acceptance Audit & Release Gate` under `## [Unreleased] (Target: v1.4.1)` (recording the acceptance matrix summary, `test_01_version_unification` single-source update, manual Windows QA status, and any `BLOCKED`/risk-waived items).
- ONLY after all S24 Release Gate conditions pass (zero failing automated checks, zero unwaived `BLOCKED` P0/P1 items such as `BUG-09`, and confirmed manual Windows release blockers or explicit Project Lead risk waiver), `S24` retitles `## [Unreleased] (Target: v1.4.1)` to `## [1.4.1] - <YYYY-MM-DD>` and bumps `__version__` ONCE to `"1.4.1"`.

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
