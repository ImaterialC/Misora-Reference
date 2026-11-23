/plan Implement S02: Test `backups/` Isolation, `search_engine.py` `Any` Import & Single-Version DeepL User-Agent in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/search_engine.py @core/mtl_engine.py @__init__.py @tests/

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **HYG-02, HYG-05, HYG-06** (Track 1 · Group A).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S02` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `tests/*.py (ONLY adding `app.backup_folder` TemporaryDirectory isolation in setUp/tearDown)`
  * `core/search_engine.py (ONLY importing `Any` from `typing`)`
  * `core/mtl_engine.py (ONLY replacing hardcoded DeepL User-Agent `1.3` with shared version reader — NO circular import of `misora.py` and NO version bump!)`
  * `tests/test_p3_s02_hygiene.py (NEW)`
  * `CHANGELOG.md (append `### S02` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `misora.py`
  * `__init__.py (DO NOT bump __version__ here!)`
  * `core/story_ast.py`
  * `core/script_codec.py`
  * `core/bundle_io.py`
  * `assets/*.py`
5. **Changelog & Version Contract:**
   - Append `### S02` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S02`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Grep `tests/*.py` for `MisoraApp(` and `on_save` / `on_replace_all` / `backup_folder` to list every test file that can write `.bak_*` into repo root `backups/`.
2. Inspect typing imports and `search_directory()` signature in `core/search_engine.py`.
3. Inspect DeepL `User-Agent` strings in `core/mtl_engine.py` (`_translate_deepl`, `_test_deepl_usage`) and root `__init__.py` (`__version__`).

==================================================
PART 2 — REQUIRED IMPLEMENTATION (HYG-02, HYG-05, HYG-06)
==================================================
### A. **HYG-02 (`tests/*.py`):** Redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp()` and clean up in `tearDown()` across all existing UI/save/replace tests (alongside `misora.CONFIG_PATH` isolation) so `py -3.12 -m unittest discover -s tests -v` creates ZERO new files in repo root `backups/`.

### B. **HYG-05 (`core/search_engine.py`):** Import `Any` from `typing` so `typing.get_type_hints(ProjectSearchEngine.search_directory)` resolves cleanly at runtime.

### C. **HYG-06 (`core/mtl_engine.py`):** Replace hardcoded `Misora-Story-Editor/1.3` User-Agent strings in `_translate_deepl()` and `_test_deepl_usage()` by reading the single app version source (`__init__.py`'s `__version__` via a small helper or shared constant without circularly importing `misora.py`). **DO NOT bump `__version__`** (stays `1.4.0` until `S24`).

### D. **`CHANGELOG.md`:** Append `### S02` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s02_hygiene.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s02_hygiene` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — HYG-05] `typing.get_type_hints(ProjectSearchEngine.search_directory)` raises `NameError` before patch and succeeds after patch.
2. [Probe 2 — HYG-06] Inspecting DeepL request headers (with mocked `urlopen`) shows User-Agent matches current root `__version__` (`1.4.0`), NOT hardcoded `1.3`.
3. [Probe 3 — HYG-02] Running save/replace test modules creates ZERO new files inside repo root `backups/`.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] Root `__init__.__version__` remains `'1.4.0'`.
2. [Guard 2] Full `py -3.12 -m unittest discover -s tests -v` passes with 0 failures, 0 errors, 0 skips.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- No changes to `misora.py`, `core/story_ast.py`, or `__version__`.
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s02_hygiene.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s02_hygiene -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s02_hygiene` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s02_hygiene -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
