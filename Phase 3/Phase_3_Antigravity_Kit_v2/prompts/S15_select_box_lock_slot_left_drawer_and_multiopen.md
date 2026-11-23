/plan Implement S15: Select Box Both Views + Reserved Lock Slot, Collapsible Left Drawer, Empty State & Batched Multi-Open in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @misora.py @tests/test_s1_open_file_safety.py @tests/test_s4_view_model_sync.py @tests/test_s8b4_ui_polishing.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-41, FEAT-05, FEAT-06, FEAT-07** (Track 2 · Group G2 (post-DEP-4, DEP-9)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S15` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (`_on_toggle_select_box_mode`, `_render_continuous_view` Card #0 & lock slot, Dialogue header select checkbox, `_toggle_dock_collapse` left drawer, empty-state Open Files frame, `btn_tab_files` double-click, `on_open_file` `askopenfilenames` batched refresh)`
  * `tests/test_p3_s15_selection_drawer_open.py (NEW)`
  * `CHANGELOG.md (append `### S15` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/*.py`
  * `assets/*.py`
5. **Changelog & Version Contract:**
   - Append `### S15` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S15`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name in `misora.py`: `_on_toggle_select_box_mode`, `_render_continuous_view`, `_toggle_dock_collapse`, `btn_tab_files`, `on_open_file`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-41, FEAT-05, FEAT-06, FEAT-07)
==================================================
### A. **BUG-41 + FEAT-05 (`U-B11`, `U-B12`, `U-B29`):** (1) Make `Select Box` work in BOTH `Dialogue` and `All Script`: in `Dialogue` view display inline header checkbox `[ ] Select Box #N (X selected)` so the user can step across boxes and check/uncheck specific boxes into `_selected_boxes` for Copy/Cut (removing the misleading no-op toast). (2) Restore Box 0 (`-1`) Select Box checkbutton on Card #0 (`hdr_0`) in `All Script`. (3) Place per-card Translation Lock button/icon immediately to the RIGHT of the Select Box checkbox inside a **fixed reserved slot width** so headers NEVER shift horizontally when `Select Box` mode toggles.

### B. **FEAT-06 (`U-B15`):** Extend existing pane-based `_toggle_dock_collapse()` / `_dock_collapsed` into a clean collapsible left drawer for `Search Results` / `Opened Files` (strictly pane-based inside `h_paned` — NEVER a `place()` overlay `NO-11`).

### C. **FEAT-07 (`U-B16`, `U-B19`, `U-B20`):** (1) Empty state (startup / 0 open files): centered large `'Open Files'` button with drag-and-drop `.unity3d` / `.misora` workspace hint underneath (reusing existing DnD handlers, auto-hidden when >=1 file opens). (2) Bind `<Double-Button-1>` on `Opened Files` tab (`btn_tab_files`) to `self.on_open_file()`. (3) Update `on_open_file()` to `filedialog.askopenfilenames()`, preserving S1 staged semantics and performing ONE batched UI refresh at the end.

### D. **`CHANGELOG.md`:** Append `### S15` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s15_selection_drawer_open.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s15_selection_drawer_open` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-41 & FEAT-05] Select Box in `Dialogue` shows inline checkbox; checking Box 1 & Box 3 sets `_selected_boxes == {0, 2}`; Card #0 in `All Script` has Select Box checkbox; lock icon sits right of checkbox slot with identical x-coordinate when Select Box toggles.
2. [Probe 2 — FEAT-06] Left drawer collapses and expands cleanly via `h_paned` without `place()` overlay.
3. [Probe 3 — FEAT-07] Empty state displays centered Open Files button when 0 docs open and hides when doc opens; double-clicking `btn_tab_files` invokes `on_open_file`; multi-file `askopenfilenames` calls `_update_views()` once for the batch.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_s1_open_file_safety`, `tests.test_s4_view_model_sync`, and `tests.test_s8b4_ui_polishing` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT implement `.misora` serialization yet (S16).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s15_selection_drawer_open.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s15_selection_drawer_open -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s15_selection_drawer_open` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s15_selection_drawer_open -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
