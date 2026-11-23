<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S04
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> Proceed
- Model & Effort : Claude Sonnet 4.6
- Cheap-Model OK : BORDERLINE — Recommended Claude Sonnet 4.6 (atomic transaction + regex parity + ttk theme)
- Ledger Coverage: BUG-07, BUG-08, BUG-31 (Group B3 (DEP-1))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S04: Atomic Sparse CSIF/Metadata Transaction, Backslash Parity & Dark-Theme Treeview Contrast Fix in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/script_codec.py @misora.py @tests/test_script_codec.py @tests/test_phase4_import_export_preview.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S04`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/script_codec.py (serialize, _parse_csif, apply_to_document)`
  * `misora.py (_show_paste_preview_and_apply, ScriptPastePreviewDialog._populate_tree, _apply_styles Treeview/Treeview.Heading)`
  * `tests/test_p3_s04_csif_atomic.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/undo_journal.py`
  * `misora.py (toolbar, search, save, MTL — owned by other sessions)`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S04`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `serialize()` (425-435), `_parse_csif()` (268-276), and `apply_to_document()` (442-545) in `core/script_codec.py`.
2. Inspect `_show_paste_preview_and_apply()` (10602-10766), `ScriptPastePreviewDialog._populate_tree()` (11172-11193), and `_apply_styles()` (2768+) in `misora.py`.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-07, BUG-08, BUG-31)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-07, BUG-08, BUG-31**

### A. **BUG-07 (`core/script_codec.py` + `misora.py`):** (1) Add `apply_metadata: bool = True` to `apply_to_document()`; pass `apply_metadata=apply_meta` from `_show_paste_preview_and_apply()` so unchecking Box 0 metadata strictly leaves Box 0 untouched. (2) Validate ALL sparse absolute 1-based targets (`b.index - 1`) and capture each target box's primary `Record.uid` BEFORE mutating metadata or any dialogue box; resolve by UID during application and roll back completely if any step raises (true atomic transaction). (3) In `ScriptPastePreviewDialog._populate_tree()` AND `_show_paste_preview_and_apply()` (`BoxEditDelta` + `_modified_boxes`), map sparse blocks to exact `b.index - 1` (keep cursor-relative `start_idx + k` ONLY for non-sparse payloads).

### B. **BUG-08 (`core/script_codec.py`):** In `serialize()`, add exactly ONE leading backslash to any body line matching regex `^\\*@@` (zero-or-more leading backslashes immediately followed by `@@`). In `_parse_csif()`, remove exactly ONE leading backslash from any line matching regex `^\\+@@` (one-or-more leading backslashes immediately followed by `@@`); NEVER strip all leading backslashes.

### C. **BUG-31 (`misora.py:_apply_styles()` — DEP-1):** Explicitly configure `Treeview` and `Treeview.Heading` (`background`, `fieldbackground`, `foreground`, and `map` for `selected` background/foreground using `best_contrast_fg()`) inside `_apply_styles()` so `ScriptPastePreviewDialog` and all future Treeview widgets are high-contrast across EVERY preset (light & dark, including `Midnight Violet` and `Misora Classic (Dark)`).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s04_csif_atomic.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-07] Unchecking `apply_metadata=False` on CSIF payload with `@@!title` leaves Box 0 completely unchanged.
2. [Probe 2 — BUG-07] Sparse CSIF `@@#1|Kokkoro` + `@@#3|Pecorine` applied while active `current_box_idx == 5` previews, mutates, records undo, and undoes boxes 0 and 2 (NOT 5 and 6); sparse payload with kind-conversion on earlier box still hits original target UIDs; invalid out-of-range sparse payload with `@@!title` raises and leaves BOTH Box 0 metadata and all dialogue boxes untouched.
3. [Probe 3 — BUG-08] Exact `serialize -> parse` round-trip on FOUR DISTINCT inputs: `@@x` (0 backslashes), `\@@x` (1 backslash), `\\@@x` (2 backslashes), `\\\@@x` (3 backslashes), plus ordinary `\text` not preceding `@@`.
4. [Probe 4 — BUG-31] For EVERY preset in `THEME_PRESETS`, `ttk.Style().lookup('Treeview', 'foreground')` vs `background`/`fieldbackground` has WCAG contrast ratio >= 4.5.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_script_codec.py`, `tests/test_phase2_required.py`, and `tests/test_phase4_import_export_preview.py` pass unchanged.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT alter `on_box_paste()` or `on_save()` (owned by S03/S05).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s04_csif_atomic.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s04_csif_atomic -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s04_csif_atomic -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
