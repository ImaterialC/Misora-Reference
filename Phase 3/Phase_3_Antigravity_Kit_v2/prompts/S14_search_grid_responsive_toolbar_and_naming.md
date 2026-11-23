/plan Implement S14: Search Bar 5-Col Grid, Hide Current Dir, Player Icon/No `[-]`, VIEW Group, Toggle NGUI Ribbon & `Raw Commands` in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @misora.py @assets/icon.py @README.md @tests/test_s8b4_ui_polishing.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-38, BUG-39, FEAT-01, FEAT-02, FEAT-03, FEAT-04** (Track 2 · Group G1 (post-DEP-3)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S14` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (`_build_search_bar`, `_sync_scope_widgets`, `_build_menu`, `_build_main_panels`, `_save_user_prefs`/`_load_user_prefs` for `toggle_ngui_ribbon`, mode header labels)`
  * `assets/icons/ (optional matching PNG icons for Select Box / All Script; Unicode fallback mandatory)`
  * `README.md (update visible UI/shortcut labels to match `All Script` / `Raw Commands`)`
  * `tests/test_p3_s14_toolbar_search_ui.py (NEW)`
  * `CHANGELOG.md (append `### S14` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/*.py`
  * `assets/splash.py`
5. **Changelog & Version Contract:**
   - Append `### S14` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S14`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name in `misora.py`: `_build_search_bar`, `_sync_scope_widgets`, `_on_folder_path_var_trace`, `_build_menu`, `_build_main_panels`.
2. Verify hiding `folder_path_entry` on `Current File(s)` does NOT clear `selected_search_folder` or `project_folder`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-38, BUG-39, FEAT-01, FEAT-02, FEAT-03, FEAT-04)
==================================================
### A. **BUG-38 (`U-B1`, `U-B2`):** Convert Find & Replace rows in `_build_search_bar()` into ONE shared 5-column `grid` (label | entry | btn1 | btn2 | close) with equal column weights/minsize and uniform button styling so Find/Replace entries have identical `winfo_rootx()`/`winfo_width()` and all 4 buttons (`Find in Files`, `Cancel`, `Replace`, `Replace All`) have identical width and height.

### B. **FEAT-01 (`U-B21`):** In `_sync_scope_widgets()`, when `scope == 'current'`, hide (`grid_remove()`/`pack_forget()`) BOTH `folder_path_entry` and `btn_browse_search_folder` while preserving `selected_search_folder` and `project_folder` untouched.

### C. **FEAT-02 (`U-B3`+`U-B5`, `U-B4`, `U-B13`):** Convert Player button to icon-only (`player.png`, NO `{0}` label text), move OUT of NGUI ribbon into speaker/text-actions area, attach Unicode fallback + tooltip explaining `{playername}`/`{0}` (`AGENTS.md` §21). Remove standalone `[-]` button from NGUI ribbon (keep `[-]` in NGUI Glossary & menu).

### D. **FEAT-03 (`U-B6`, `U-B7`, `U-B8`, `U-B30`):** Rename `Continuous View` -> `All Script`. Group `Select Box`, `All Script`, and `Preview` into ONE unified `VIEW` group with icons + Unicode fallbacks + tooltips (`get_icon()` returns `None` when PNG missing). Update top headers to `Dialogue` / `All Script` (Preview OFF) and `Dialogue Preview` / `All Script Preview` (Preview ON). Rename bottom pane strictly to **`Raw Commands`**. Keep internal Python identifiers (`var_continuous_view`, etc.) intact; sweep View menu, tooltips, and `README.md`.

### E. **BUG-39 + FEAT-04 (`U-B14`):** Replace single packed `speaker_ribbon_row` with responsive `grid`/stacked rows (Speaker/View row + collapsible NGUI Ribbon row + Text/Box actions) so NO controls clip off-screen at `1280x720` or snapped `~960px` widths. Add `View > Toggle NGUI Ribbon` persisted in `misora_config.json`.

### F. **`CHANGELOG.md`:** Append `### S14` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s14_toolbar_search_ui.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s14_toolbar_search_ui` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-38] Geometric assertion after `update_idletasks()`: `search_entry.winfo_rootx() == replace_entry.winfo_rootx()`, equal widths, and all 4 Find/Replace buttons share identical `winfo_width()` and `winfo_height()`.
2. [Probe 2 — FEAT-01] Scope `'current'` unmaps `folder_path_entry` & `btn_browse_search_folder` while `app.selected_search_folder` remains unchanged.
3. [Probe 3 — FEAT-02 & FEAT-03] Ribbon has no standalone `[-]` button; Player button has no `{0}` text, sits outside NGUI ribbon, has tooltip; headers display `Dialogue`/`All Script`/`Dialogue Preview`/`All Script Preview` and bottom pane displays `Raw Commands`.
4. [Probe 4 — BUG-39 & FEAT-04] At `1280x720` and `960x720`, visible toolbar groups have `winfo_width() > 0` inside parent bounds; `View > Toggle NGUI Ribbon` hides/shows NGUI ribbon and persists preference.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_s8b4_ui_polishing`, `tests.test_misora_ui_integration`, and `tests.test_p3_s13_ribbon_shortcuts` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT alter Select Box behavior (S15), rulers/Preview (S17/S18), or MTL drawer (S20/S21).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s14_toolbar_search_ui.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s14_toolbar_search_ui -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s14_toolbar_search_ui` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s14_toolbar_search_ui -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
