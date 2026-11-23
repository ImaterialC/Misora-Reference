/plan Implement S18: Code-Drawn Game-Style `Dialogue Preview` & `All Script Preview` (Native Bleed, `wrap='none'`, No `AtlasAdv`) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @misora.py @tests/test_p3_s06_doc_state_save.py @tests/test_p3_s17_pixel_rulers.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **FEAT-10** (Track 2 · Group G4b (post-DEP-2, DEP-8)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S18` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (`_on_toggle_preview_compiled`, `_insert_compiled_ngui_text`, `cstyle_*` sweep, `Dialogue Preview` single Canvas + embedded read-only Text, `All Script Preview` lightweight styled `tk.Frame` cards)`
  * `tests/test_p3_s18_game_preview.py (NEW)`
  * `CHANGELOG.md (append `### S18` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/*.py`
  * `assets/ (ZERO copyrighted `AtlasAdv` sprites in MIT repo — `NO-02`!)`
5. **Changelog & Version Contract:**
   - Append `### S18` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S18`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Verify S06 (`BUG-11`, `DEP-2`) and S17 (`DEP-8` shared pixel-measure helper) are green.
2. Bind by symbol name in `misora.py`: `_on_toggle_preview_compiled`, `_insert_compiled_ngui_text`, `_configure_editor_rich_tags`, `_update_views`, `_render_continuous_view`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FEAT-10)
==================================================
### A. **FEAT-10 (`U-B27`, `U-B28` — Lead Ruling #4, `NO-02`, `NO-12`):** Implement code-drawn Priconne-style dialogue frames using native Tk primitives (cream/gold double border, name plate, static pink `▼`, `best_contrast_fg()`, ZERO copyrighted `AtlasAdv` art). Consume S17's shared pixel-measure helper (`DEP-8`) calibrated to **50 digit-widths without a linebreak OR 3 or more linebreaks (4+ lines)** safe area with small visual margin to the outer border. Enforce **`wrap='none'`** so over-wide or 4+ line text visibly bleeds past the frame with **NO auto-shrinking** (`NO-12`). (1) **`Dialogue Preview`:** single `tk.Canvas` + one embedded read-only `tk.Text` (restore caret/selection/`yview` on Preview OFF; sweep `cstyle_*` tags per render `GEM-E03`). (2) **`All Script Preview`:** lightweight styled `tk.Frame` cards (NO per-card `tk.Canvas`). Pure presentation layer: zero doc/dirty/undo mutation; `BUG-11` guarantees plain-text saves stay safe. Box 0 Summary remains deferred (`DEF-04`).

### B. **`CHANGELOG.md`:** Append `### S18` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s18_game_preview.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s18_game_preview` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — FEAT-10] `Dialogue Preview` uses `wrap='none'` without auto-shrinking font size, restores caret/selection on Preview OFF, sweeps old `cstyle_*` tags on box switch, and leaves `is_dirty == False` and `undo_depth == 0`.
2. [Probe 2 — FEAT-10] `All Script Preview` renders lightweight `tk.Frame` cards with `wrap='none'` (zero per-card `tk.Canvas` widgets).

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_p3_s06_doc_state_save` (plain-text save while Preview ON) and `tests.test_p3_s17_pixel_rulers` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- NO `AtlasAdv` sprites (`NO-02`), NO Box 0 Summary limits (`DEF-04`), NO auto-shrink (`NO-12`).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s18_game_preview.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s18_game_preview -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s18_game_preview` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s18_game_preview -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
