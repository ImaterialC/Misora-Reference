/plan Implement S05: Dark-Theme Treeview Contrast (DEP-1 FIRST), Atomic Sparse CSIF/Metadata & Backslash Parity in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @misora.py @core/script_codec.py @tests/test_script_codec.py @tests/test_phase4_import_export_preview.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-31, BUG-07, BUG-08** (Track 1 · Group B3 (DEP-1 STRICTLY FIRST)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S05` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (`_apply_styles` Treeview/Treeview.Heading FIRST, then `_show_paste_preview_and_apply`, `ScriptPastePreviewDialog._populate_tree`)`
  * `core/script_codec.py (`serialize`, `_parse_csif`, `apply_to_document`)`
  * `tests/test_p3_s05_treeview_csif.py (NEW)`
  * `CHANGELOG.md (append `### S05` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/undo_journal.py`
  * `misora.py (toolbar, search, save, MTL)`
5. **Changelog & Version Contract:**
   - Append `### S05` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S05`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name: `_apply_styles`, `ScriptPastePreviewDialog._populate_tree`, `_show_paste_preview_and_apply` in `misora.py`; `serialize`, `_parse_csif`, `apply_to_document` in `core/script_codec.py`.
2. Confirm `DEP-1` execution order: `BUG-31` (`_apply_styles` Treeview contrast) MUST be implemented and verified FIRST before editing `ScriptPastePreviewDialog` in `BUG-07`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-31, BUG-07, BUG-08)
==================================================
### A. **BUG-31 (IMPLEMENT FIRST — DEP-1, `misora.py:_apply_styles()`):** Explicitly configure `Treeview` and `Treeview.Heading` (`background`, `fieldbackground`, `foreground`, and `map` selected contrast via `best_contrast_fg()`) inside `_apply_styles()` so `ScriptPastePreviewDialog` and all future Treeview widgets are legible across EVERY preset in `THEME_PRESETS` (light & dark, including `Midnight Violet` and `Misora Classic (Dark)`).

### B. **BUG-07 (`core/script_codec.py` + `misora.py`):** (1) Add `apply_metadata: bool = True` to `apply_to_document()` and wire `apply_metadata=apply_meta` from `_show_paste_preview_and_apply()` so unchecking Box 0 metadata leaves Box 0 strictly untouched. (2) Validate ALL sparse absolute 1-based targets (`b.index - 1`) and capture each target box's primary `Record.uid` BEFORE mutating metadata or any dialogue box; resolve by UID during application and roll back completely if any step raises (atomic transaction). (3) In `ScriptPastePreviewDialog._populate_tree()`, `BoxEditDelta`, and `_modified_boxes`, map sparse blocks to exact `b.index - 1` (cursor-relative `start_idx + k` ONLY for non-sparse payloads).

### C. **BUG-08 (`core/script_codec.py`):** In `serialize()`, add exactly ONE leading backslash to any body line matching regex `^\\*@@` (zero-or-more leading backslashes immediately followed by `@@`). In `_parse_csif()`, remove exactly ONE leading backslash from any line matching regex `^\\+@@` (one-or-more leading backslashes immediately followed by `@@`); NEVER strip all leading backslashes.

### D. **`CHANGELOG.md`:** Append `### S05` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s05_treeview_csif.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s05_treeview_csif` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-31 (FIRST)] For EVERY preset in `THEME_PRESETS`, `Treeview` foreground vs background/fieldbackground WCAG contrast ratio >= 4.5 (fails on dark themes pre-patch).
2. [Probe 2 — BUG-07] `apply_metadata=False` on CSIF with `@@!title` leaves Box 0 untouched; sparse `@@#1|Kokkoro` + `@@#3|Pecorine` applied while `current_box_idx == 5` previews, mutates, records undo, and undoes boxes 0 and 2 (NOT 5 and 6); invalid out-of-range sparse payload with `@@!title` raises and leaves BOTH Box 0 and all dialogue untouched.
3. [Probe 3 — BUG-08] Exact `serialize -> parse` round-trip on FOUR DISTINCT inputs: `@@x` (0 backslashes), `\@@x` (1 backslash), `\\@@x` (2 backslashes), `\\\@@x` (3 backslashes), plus ordinary `\text` not preceding `@@`.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_script_codec`, `tests.test_phase2_required`, and `tests.test_phase4_import_export_preview` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT alter `on_save` (S06) or `on_box_paste` (already handled in S04).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s05_treeview_csif.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s05_treeview_csif -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s05_treeview_csif` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s05_treeview_csif -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
