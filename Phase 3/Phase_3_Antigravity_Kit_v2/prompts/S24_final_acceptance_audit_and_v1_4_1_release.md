/plan Implement S24: Final Acceptance Audit Matrix (All 63 IDs + DEF/NO) & Single `v1.4.1` Version/Changelog Release Stamp in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @CHANGELOG.md @__init__.py @README.md @tests/

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **FINAL ACCEPTANCE AUDIT (ALL 63 IDs + DEF/NO) + v1.4.1 RELEASE** (Release Gate (GPT `08_FINAL_ACCEPTANCE_AUDIT` + Lead `v1.4.1` Changelog Contract)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S24` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `__init__.py (bump `__version__ = '1.4.1'` ONCE — only AFTER all non-fixture automated checks pass!)`
  * `misora.py (ONLY fallback version string inside `_get_app_version()` if hardcoded `'1.4.0'`)`
  * `assets/splash.py (ONLY fallback version string inside `_load_app_version()` if hardcoded `'1.4.0'`)`
  * `CHANGELOG.md (retitle `## [Unreleased] (Target: v1.4.1)` -> `## [1.4.1] - <YYYY-MM-DD>` and add final release summary)`
  * `README.md & PROJECT_STATE.md (final release version `1.4.1` + complete measured acceptance matrix)`
  * `tests/test_p3_s24_release_version.py (NEW)`
   - DO NOT modify:
  * `core/*.py (ZERO behavioral edits in release audit!)`
  * `misora.py (all application logic outside `_get_app_version` fallback)`
5. **Changelog & Version Contract:**
   - Append `### S24` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S24`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Audit `CHANGELOG.md` to confirm `### S01` through `### S23` are all present and recorded.
2. Run full read-only `py -3.12 -m compileall -q misora.py core assets tests` and `py -3.12 -m unittest discover -s tests -v` and verify `Ran N tests` (with `N > 0`; `Ran 0 tests` is a hard FAILURE), 0 failures, 0 errors, 0 skips.
3. Inspect `backups/` and `misora_config.json` cleanliness.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FINAL ACCEPTANCE AUDIT (ALL 63 IDs + DEF/NO) + v1.4.1 RELEASE)
==================================================
### A. **PART A — Complete Evidence-Based Acceptance Matrix (GPT Standard):** Build the final acceptance table inside the Walkthrough and `PROJECT_STATE.md` assigning ONE honest status (`PASS` / `FAIL` / `BLOCKED` / `DEFERRED` / `NOT-APPLICABLE`) to EVERY canonical Phase 2.5 ID:
   - `BUG-01..BUG-41` (41)
   - `FEAT-01..FEAT-14` (14)
   - `HYG-01..HYG-08` (8)
   - `DEF-01..DEF-10` (10 — verify untouched/deferred)
   - `NO-01..NO-12` (12 — verify ZERO violations)
   Every `PASS` MUST cite exact test module + command + exit code + observed output. Any item requiring a missing production `.unity3d` fixture (e.g., `BUG-09` real bundle check, `DEF-02` 35/32) MUST stay **`BLOCKED`**, NEVER `PASS`. Separate manual Windows GUI QA checklist (Ribbon Cut, Paste Box both views, DPI/Snapped layout visual check, real `Import from XUAT` smoke test) from automated passes.

### B. **PART B — Single `v1.4.1` Version Bump & `CHANGELOG.md` Release Stamp (ONLY if ZERO P0/P1 automated gates fail):**
   - Bump root `__init__.py` `__version__ = '1.4.1'` ONCE (and update `'1.4.0'` fallback strings in `misora.py:_get_app_version()` and `assets/splash.py:_load_app_version()` + `README.md` version badge). Because `HYG-06` reads `__version__`, DeepL User-Agent automatically updates to `1.4.1`.
   - Retitle `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` to `## [1.4.1] - <YYYY-MM-DD>` with a concise Indonesian/English-friendly executive summary of everything fixed in `S01..S23`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s24_release_version.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s24_release_version` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — Release Version] `__init__.__version__ == '1.4.1'`, `misora.__version__ == '1.4.1'`, `splash._VERSION == '1.4.1'`, and DeepL User-Agent reflects `'1.4.1'`; `CHANGELOG.md` contains `## [1.4.1]` with sections `S01..S23`.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] Full `py -3.12 -m unittest discover -s tests -v` exits 0 with 0 failures, 0 errors, 0 skips (`Ran 0 tests` = FAIL) and ZERO new files in `backups/`.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- ZERO new features or bug fixes in S24. If any P0/P1 automated check fails, STOP and report — do NOT bump `__version__` to `1.4.1`!
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s24_release_version.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s24_release_version -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s24_release_version` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s24_release_version -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
