/plan Implement S24: Final Acceptance Audit Matrix (All 63 IDs + DEF/NO) & Single `v1.4.1` Version/Changelog Release Stamp in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @CHANGELOG.md @__init__.py @README.md @tests/test_phase4_import_export_preview.py @tests/

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **FINAL ACCEPTANCE AUDIT (ALL 63 IDs + DEF/NO) + v1.4.1 RELEASE GATE** (GPT `08_FINAL_ACCEPTANCE_AUDIT` + Lead `v1.4.1` Changelog Contract + Qwen `MF-S24`).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S24` starts from the accepted tree of `S23` (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from `S01..S23` as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `tests/test_phase4_import_export_preview.py` — **SCOPED STRICTLY to `test_01_version_unification`**: replace hardcoded `expected_version = "1.4.0"` with `expected_version` derived from root `__init__.__version__` (single source per `AGENTS.md` §21), **KEEPING ALL consistency assertions intact** (`root == misora.__version__ == _get_app_version() == splash._VERSION == About "Version X" text`). This preserves single-source intent and is NOT test weakening (`MF-S24`).
  * `CHANGELOG.md` (append `### S24 — Final Acceptance Audit & Release Gate` under `## [Unreleased] (Target: v1.4.1)`; promote heading to `## [1.4.1] - <YYYY-MM-DD>` ONLY if all release gates in Part 2B pass or have explicit Project Lead risk approval!)
  * `PROJECT_STATE.md` (complete evidence-based final acceptance matrix for all 63 IDs + `DEF-01..10` + `NO-01..12` + manual Windows QA record)
  * `__init__.py` (bump `__version__ = '1.4.1'` ONCE — **ONLY if ALL Release Gate conditions in Part 2B are met!**)
  * `misora.py` (ONLY fallback version string inside `_get_app_version()` if hardcoded `'1.4.0'` — **ONLY if Release Gate passes!**)
  * `assets/splash.py` (ONLY fallback version string inside `_load_app_version()` if hardcoded `'1.4.0'` — **ONLY if Release Gate passes!**)
  * `README.md` (final release version badge `'1.4.1'` — **ONLY if Release Gate passes!**)
  * `tests/test_p3_s24_release_version.py` (NEW)
   - DO NOT modify:
  * `core/*.py` (ZERO behavioral edits in release audit!)
  * `misora.py` (all application logic outside `_get_app_version` fallback)
  * Any other test file outside `tests/test_phase4_import_export_preview.py::test_01_version_unification` and `tests/test_p3_s24_release_version.py`
5. **Changelog & Release-Gate Contract (STRICT):**
   - `S24` ALWAYS appends `### S24 — Final Acceptance Audit & Release Gate` under `## [Unreleased] (Target: v1.4.1)` recording the acceptance matrix summary, the `test_01_version_unification` single-source update, manual Windows QA status, and any `BLOCKED` / risk-waived items.
   - `S24` promotes `## [Unreleased] (Target: v1.4.1)` to `## [1.4.1] - <YYYY-MM-DD>` and bumps `__version__` to `'1.4.1'` **ONLY** when EVERY condition in Part 2B is satisfied. Otherwise STOP cleanly leaving `### S24` under `## [Unreleased]` and `__version__ == '1.4.0'`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S24`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current findings in the Implementation Plan:
1. Audit `CHANGELOG.md` to confirm `### S01` through `### S23` are all present and recorded.
2. **Hardcoded Version Grep (`MF-S24`):** Grep `tests/` for hardcoded `"1.4.0"`, report `tests/test_phase4_import_export_preview.py::test_01_version_unification` (around line 82) and any other hit, and explicitly authorize deriving `expected_version` from root `__init__.__version__` as part of this release patch (never weakening consistency assertions).
3. Run read-only `py -3.12 -m compileall -q misora.py core assets tests` and `py -3.12 -m unittest discover -s tests -v`; verify `Ran N tests` (`N > 0`; `Ran 0 tests` = hard FAILURE), 0 failures, 0 errors, and 0 unexpected skips (any skip MUST be explicitly documented as fixture-`BLOCKED`).
4. Report live status of:
   - Every P0/P1 item (especially whether `BUG-09` real production `.unity3d` verification is `PASS` or `BLOCKED`).
   - All mandatory manual Windows release checks (`AGENTS.md` §29: Ribbon Cut, Paste Box in both views; plus DPI/snapped layout visual check and `Import from XUAT` smoke test) — report whether the Project Lead has supplied confirmed manual PASS results or explicit written risk acceptance.
5. Inspect `backups/` and `misora_config.json` cleanliness.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FINAL ACCEPTANCE AUDIT + RELEASE GATE)
==================================================
### A. **PART A — Complete Evidence-Based Acceptance Matrix & Single-Source Test Fix (`MF-S24`):**
1. Build the final acceptance table inside the Walkthrough and `PROJECT_STATE.md` assigning ONE honest status (`PASS` / `FAIL` / `BLOCKED` / `DEFERRED` / `NOT-APPLICABLE`) to EVERY canonical Phase 2.5 ID:
   - `BUG-01..BUG-41` (41)
   - `FEAT-01..FEAT-14` (14)
   - `HYG-01..HYG-08` (8)
   - `DEF-01..DEF-10` (10 — verify untouched/deferred)
   - `NO-01..NO-12` (12 — verify ZERO violations)
   Every `PASS` MUST cite exact test module + command + exit code + observed output. Any item requiring a missing production `.unity3d` fixture (e.g., `BUG-09` real bundle check, `DEF-02` 35/32) MUST stay **`BLOCKED`**, NEVER `PASS`.
2. Update `tests/test_phase4_import_export_preview.py::test_01_version_unification` (`MF-S24`): replace hardcoded `expected_version = "1.4.0"` with `expected_version` derived from root `__init__.__version__`, keeping ALL cross-module consistency assertions (`root == misora.__version__ == _get_app_version() == splash._VERSION == About "Version X" text`) intact. Record this update in `CHANGELOG.md` `### S24`.

### B. **PART B — Mandatory Release Gate Before Single `v1.4.1` Version Bump (`GPT-1`, `GPT-2`):**
**ALL FOUR conditions MUST hold BEFORE bumping `__version__` to `'1.4.1'` or promoting `## [Unreleased]`:**
1. **Zero Automated Failures:** `compileall` and full `unittest discover` exit 0 with `Ran N tests` (`N > 0`), 0 failures, 0 errors, and 0 unexpected skips.
2. **Zero Unwaived `BLOCKED` P0/P1 Items (`GPT-1`):** `BLOCKED` is NOT `FAIL`, and it is ALSO NOT `PASS`. Every P0/P1 item MUST be **`PASS`** before release. If `BUG-09` (P1 real production `.unity3d` bundle verification) or any other P0/P1 item remains `BLOCKED` due to missing fixtures, **DO NOT bump `__version__` automatically** — STOP and require either (a) testing with a real production `.unity3d` fixture supplied by the Project Lead, OR (b) explicit written risk acceptance from the Project Lead authorizing release with `BUG-09` production check `BLOCKED`.
3. **Mandatory Manual Windows Release Blockers Confirmed (`GPT-2`, `AGENTS.md` §29):** Automated unit tests do NOT substitute for Windows GUI checks. Before bumping `__version__` to `'1.4.1'`, the Project Lead must confirm manual Windows results (or provide explicit written risk acceptance):
   - **Ribbon Cut (`AGENTS.md` §29 blocker):** Manual Windows PASS confirmed.
   - **Paste Box in BOTH Dialogue and All Script views (`AGENTS.md` §29 blocker):** Manual Windows PASS confirmed.
   - **DPI & snapped half-screen layout (`BUG-39`/`FEAT-04`):** Manual Windows visual inspection recorded.
   - **`Import from XUAT` (`FEAT-14`):** Manual Windows smoke test on a matching `BepInEx\Translation\en\Text` folder recorded.
4. **Release Stamp (ONLY once Conditions 1–3 are satisfied or explicitly risk-waived by the Project Lead):**
   - Bump root `__init__.py` `__version__ = '1.4.1'` ONCE (and update `'1.4.0'` fallback strings in `misora.py:_get_app_version()` and `assets/splash.py:_load_app_version()` + `README.md` version badge). Because `HYG-06` reads `__version__`, DeepL User-Agent automatically updates to `'1.4.1'`.
   - Append `### S24 — Final Acceptance Audit & Release Gate` in `CHANGELOG.md`, then retitle `## [Unreleased] (Target: v1.4.1)` to `## [1.4.1] - <YYYY-MM-DD>` with a concise executive summary of `S01..S24`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s24_release_version.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s24_release_version` BEFORE applying the version bump. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes pre-bump, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken probes or plant fake bugs. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (ONLY active when Part 2B Release Gate is approved; MUST FAIL before bump, PASS after bump):**
1. [Probe 1 — Release Version] `__init__.__version__ == '1.4.1'`, `misora.__version__ == '1.4.1'`, `misora._get_app_version() == '1.4.1'`, `splash._VERSION == '1.4.1'`, and DeepL User-Agent reflects `'1.4.1'`; `CHANGELOG.md` contains `## [1.4.1]` with sections `### S01` through `### S24`.

- **Regression Guards (MUST PASS both before (`1.4.0`) AND after (`1.4.1`) bump):**
1. [Guard 1 — `MF-S24` Single-Source Consistency] `tests/test_phase4_import_export_preview.py::test_01_version_unification` passes BOTH before (`1.4.0`) and after (`1.4.1`) because `expected_version` is derived from root `__init__.__version__` while preserving all cross-module consistency assertions.
2. [Guard 2 — Full Discovery (`m1` aligned with `/misora-verify`)] Full `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`, `Ran 0 tests` = FAIL), 0 failures, 0 errors, and 0 unexpected skips (any skip MUST be explicitly documented as fixture-`BLOCKED` — never treated as `PASS`), with ZERO new files in `backups/`.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- ZERO new features or bug fixes in S24.
- If ANY condition in Part 2B (automated gate, unwaived `BLOCKED` P0/P1 such as `BUG-09`, or unconfirmed manual Windows release blockers) is not satisfied, STOP after recording Part A + `### S24` under `## [Unreleased]` — **DO NOT bump `__version__` to `'1.4.1'`!**
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact (including Preflight hardcoded `"1.4.0"` grep, `BUG-09` status, and manual Windows blocker status) and WAIT for `Proceed` (plus Project Lead manual QA confirmation / risk waiver if needed for Part 2B).
2. **After `Proceed`:**
   - Apply `MF-S24` single-source update to `tests/test_phase4_import_export_preview.py::test_01_version_unification` and confirm Guard 1 passes at `1.4.0`.
   - If Part 2B Release Gate is satisfied/approved: write `tests/test_p3_s24_release_version.py` -> run pre-bump (Probe 1 fails at `1.4.0`, Guards pass) -> apply `v1.4.1` bump & `CHANGELOG.md` promotion. (If Part 2B is NOT yet satisfied: stop cleanly at audit-only with `__version__ == '1.4.0'` and `### S24` under `## [Unreleased]`.)
   - Run `/misora-verify tests.test_p3_s24_release_version` (or `/misora-verify tests.test_phase4_import_export_preview` if audit-only hold):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_phase4_import_export_preview -v`
     * `py -3.12 -m unittest tests.test_p3_s24_release_version -v` (when Part 2B executed; `Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver the final **Walkthrough artifact** containing the full 85-ID matrix (41 BUG + 14 FEAT + 8 HYG + 10 DEF + 12 NO), exact commands & real stdout, `git status --short`, manual Windows QA status, explicit list of any `BLOCKED`/risk-waived items, and confirmation that `backups/` and `misora_config.json` were untouched.
