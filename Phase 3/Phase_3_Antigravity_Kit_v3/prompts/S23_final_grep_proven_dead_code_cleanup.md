/plan Implement S23: Final Grep-Proven Dead Code & Misleading Label Cleanup (Standalone Final Implementation Session) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @misora.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **HYG-08** (Track 2 · Final Hygiene (`HYG-08` — Standalone per Grok R1/R2)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S23` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (ONLY symbols grep proves have ZERO callers + verified misleading labels)`
  * `tests/test_p3_s23_dead_code_cleanup.py (NEW)`
  * `CHANGELOG.md (append `### S23` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/*.py`
  * `assets/*.py`
  * `misora.py (`_is_speaker_pinned` behavior — deferred in `DEF-06`!)`
5. **Changelog & Version Contract:**
   - Append `### S23` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S23`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. **MANDATORY REPO-WIDE GREP (`RF-5`):** Grep the ENTIRE repo (`misora.py`, `core/`, `assets/`, `tests/`) and paste exact hit counts into the Implementation Plan for:
   1. `_update_gutter_cont`
   2. `BatchTranslateDialog._toggle_pin_top`
   3. Comma gradient label `Insert [C0,C1]` (or `[{c0_code},{c1_code}]`) in `NguiColorPickerPopup`
   4. CWD `picker_error.log` write
   5. Legacy `=== [BOX:0|...] ===` checkbox wording in `AIPromptSettingsDialog`

==================================================
PART 2 — REQUIRED IMPLEMENTATION (HYG-08)
==================================================
### A. **HYG-08 (`misora.py` — `RF-5`):** Delete `_update_gutter_cont()` and `BatchTranslateDialog._toggle_pin_top()` ONLY if repo-wide grep proves ZERO callers (if any candidate gained a caller in S01–S22, leave it and report why). Fix `NguiColorPickerPopup` gradient button label to canonical hyphen syntax `[{c0_code}-{c1_code}]`, remove CWD `picker_error.log` write (log via `self.app.logger` only), and update legacy `=== [BOX:0|...] ===` wording in `AIPromptSettingsDialog` to accurate CSIF wording. **DO NOT touch `_is_speaker_pinned` (`DEF-06`).**

### B. **`CHANGELOG.md`:** Append `### S23` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s23_dead_code_cleanup.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s23_dead_code_cleanup` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — HYG-08] Removed zero-caller dead functions no longer exist on their classes (`not hasattr(MisoraApp, '_update_gutter_cont')`, `not hasattr(BatchTranslateDialog, '_toggle_pin_top')`) when grep confirmed 0 callers; `NguiColorPickerPopup` displays hyphen gradient syntax (not comma); no CWD `picker_error.log` write exists.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `_update_gutter_clean` remains intact and functional; full `py -3.12 -m unittest discover -s tests -v` passes with 0 failures.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT touch `_is_speaker_pinned` (`DEF-06`) or any behavior outside `HYG-08`.
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s23_dead_code_cleanup.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s23_dead_code_cleanup -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s23_dead_code_cleanup` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s23_dead_code_cleanup -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
