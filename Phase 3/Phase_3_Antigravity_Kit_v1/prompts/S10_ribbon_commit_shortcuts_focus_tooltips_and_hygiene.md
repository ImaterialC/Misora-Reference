<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S10
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (Claude Sonnet 4.6) -> Proceed (Sonnet 4.6 or Gemini 3.8 Flash)
- Model & Effort : Claude Sonnet 4.6 (Plan) — optional Gemini 3.8 Flash for execution after reviewing Plan Artifact
- Cheap-Model OK : HYBRID — Plan with Sonnet 4.6, execute with Flash or Sonnet 4.6
- Ledger Coverage: BUG-28, BUG-29, BUG-30, HYG-03, HYG-07, HYG-08 (Final Stabilization Gate (DEP-3 — Completes ALL P0/P1 Bugs!))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S10: Continuous Ribbon/Size/Dirty Sync, Shortcut Conflicts, Search Focus/Gutter, Tooltips & Dead Code Cleanup in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @misora.py @tests/test_s4_view_model_sync.py @tests/test_s8b4_ui_polishing.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S10`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (_insert_text_wrapper, apply_ngui_wrapper, on_insert_ruby, on_insert_font_size, _on_misora_shortcut, _bind_shortcuts, _select_result_index, _on_dialogue_edited, _commit_widget_edit, _on_card_text_edited, _on_box0_metadata_edited, ribbon tooltips, verified dead-code cleanup)`
  * `tests/test_p3_s10_editor_shortcuts_ribbon.py`
  * `PROJECT_STATE.md (verification update — mark Stabilization Track 1 COMPLETE)`
   - DO NOT modify:
  * `core/*.py`
  * `assets/*.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S10`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `_insert_text_wrapper` (5737-5767), `apply_ngui_wrapper` (5030-5033), `on_insert_ruby`, `on_insert_font_size` (7636-7655), `_on_misora_shortcut` (6146-6190), `_bind_shortcuts` (6400-6445), `_select_result_index` (8973-8979), `_on_dialogue_edited` (8278-8344), `_commit_widget_edit` (8256).
2. **MANDATORY GREP CHECK (`RF-5` for HYG-08):** Grep entire repo (`misora.py` + `tests/`) for `_update_gutter_cont` and `BatchTranslateDialog._toggle_pin_top` to PROVE zero callers before deleting.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-28, BUG-29, BUG-30, HYG-03, HYG-07, HYG-08)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-28, BUG-29, BUG-30, HYG-03, HYG-07, HYG-08**

### A. **BUG-28 (`misora.py` — DEP-3):** Resolve active card editor via `_get_card_text_widget(self.current_box_idx)` inside `_insert_text_wrapper()` and `on_insert_ruby()` (never target hidden `txt_continuous` for bundles). Remove redundant `_on_dialogue_edited()` inside `_insert_text_wrapper()` so `apply_ngui_wrapper()`'s `_commit_widget_edit()` commits ONCE and triggers `_dirty_state_changed()` (fixing stale `*` title & Undo menu in Page View). Call `_commit_widget_edit(target)` in `on_insert_font_size()`.

### B. **BUG-29 + HYG-07 (`misora.py`):** Reconcile one canonical shortcut table across `_on_misora_shortcut()`, `_bind_shortcuts()`, menus, and tooltips: fix `Ctrl+T` conflict (editor vs root), fix `<Control-C>` vs `<Control-Shift-C>` collision, add missing `Ctrl+R` (Ruby) in `MisoraShortcuts` bindtag router, allow safe `Ctrl+Alt` app accelerators (`X/C/V/A`) without breaking AltGr, and ensure `bind_all('<Control-h>', ...)` returns `'break'` (`HYG-07`).

### C. **BUG-30 (`misora.py`):** Remove erroneous `self.txt_continuous.focus_set()` after `_focus_continuous_box()` for bundle Continuous View in `_select_result_index()`. Call `self._update_gutter_clean()` inside `_on_dialogue_edited()` so Page View line numbers update live on Enter/Delete/Paste. Return `bool` from `_on_card_text_edited()` and `_on_box0_metadata_edited()` so `_commit_widget_edit()` only calls `_dirty_state_changed()` on real changes (zero dock rebuilds on arrow keys).

### D. **HYG-03 (`misora.py` — DEP-3):** Attach single-timer `ToolTip` (350ms) and Unicode fallback text to every ribbon/toolbar control currently lacking them (`Ruby`, `Player`, `B/I/U/S/Sub/Sup`, `Preview`, `All Script`, `Select Box`, etc.) per `AGENTS.md` §21.

### E. **HYG-08 (`misora.py` — `RF-5`):** ONLY after grep proves zero callers, delete `_update_gutter_cont()` (4939-4949) and `BatchTranslateDialog._toggle_pin_top()` (11952-11956); fix `NguiColorPickerPopup` gradient button text to hyphen syntax `Insert [C0-C1]` (not comma) and remove CWD `picker_error.log` write; update legacy `=== [BOX:0|...] ===` wording in `AIPromptSettingsDialog`. Leave `_is_speaker_pinned` Page View parity untouched (`DEF-06`).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s10_editor_shortcuts_ribbon.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-28] Bold/Ruby/Size wrappers in Continuous View mutate active card widget AND AST; Bold in Page View updates window title `*` and `_dirty_state_changed()` on first click.
2. [Probe 2 — BUG-29 & HYG-07] `Ctrl+T`, `Ctrl+Shift+C`, `Ctrl+R`, `Ctrl+Alt+C/V` dispatch single canonical handlers with zero collisions; `bind_all('<Control-h>')` returns `'break'`.
3. [Probe 3 — BUG-30] Search jump in Continuous View focuses active card widget (NOT `txt_continuous`); pressing Enter in Page View updates `gutter_clean` line count; arrow-key `<KeyRelease>` in Continuous card & Box 0 triggers 0 `_refresh_opened_files_list()` calls.
4. [Probe 4 — HYG-03 & HYG-08] Every ribbon button has `_tooltip` attribute; `NguiColorPickerPopup` displays hyphen gradient label; dead methods removed cleanly.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] Full `py -3.12 -m unittest discover -s tests -v` passes 100% green -> **Stabilization Gate (Track 1) UNLOCKED for Group G features!**

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT start toolbar re-layout or renaming (S11). Do NOT touch `_is_speaker_pinned` (`DEF-06`).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s10_editor_shortcuts_ribbon.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s10_editor_shortcuts_ribbon -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s10_editor_shortcuts_ribbon -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
