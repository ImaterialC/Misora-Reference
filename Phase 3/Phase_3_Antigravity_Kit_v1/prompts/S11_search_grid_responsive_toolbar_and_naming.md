<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S11
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan -> Proceed
- Model & Effort : Gemini 3.8 Flash (SAFE! Unambiguous geometric & naming acceptance criteria)
- Cheap-Model OK : YES (Gemini 3.8 Flash safe — geometric & exact-string assertions catch any drift)
- Ledger Coverage: BUG-38, BUG-39, FEAT-01, FEAT-02, FEAT-03, FEAT-04 (Group G1 (UX Toolbar & Naming — post-DEP-3))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S11: Search Bar 5-Col Grid, Hide Current Dir, Player Icon/No `[-]`, View Group, Toggle NGUI Ribbon & `Raw Commands` Naming in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @misora.py @assets/icon.py @README.md @tests/test_s8b4_ui_polishing.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S11`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (_build_search_bar, _sync_scope_widgets, _build_menu, _build_main_panels, _save_user_prefs/_load_user_prefs for toggle_ngui_ribbon, mode header labels)`
  * `assets/icons/ (optional matching PNG icons for Select Box / All Script if created; Unicode fallback mandatory)`
  * `README.md (update visible UI/shortcut labels to match `All Script` / `Raw Commands`)`
  * `tests/test_p3_s11_toolbar_search_ui.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/*.py`
  * `assets/splash.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S11`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `_build_search_bar()` (3371-3531), `_sync_scope_widgets()` (9098-9127), `_build_menu()` (3063-3100), and `_build_main_panels()` (3767-4265) in `misora.py`.
2. Verify `folder_path_var` trace (`_on_folder_path_var_trace` 9076) so hiding widgets on `Current File(s)` does NOT clear `selected_search_folder` or `project_folder`.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-38, BUG-39, FEAT-01, FEAT-02, FEAT-03, FEAT-04)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-38, BUG-39, FEAT-01, FEAT-02, FEAT-03, FEAT-04**

### A. **BUG-38 (`U-B1`, `U-B2`):** Convert Find & Replace rows in `_build_search_bar()` into ONE shared 5-column `grid` (label | entry | btn1 | btn2 | close) with equal column weights/minsize and uniform button styling so Find/Replace entries have identical `winfo_rootx()`/`winfo_width()` and all 4 buttons (`Find in Files`, `Cancel`, `Replace`, `Replace All`) have identical width and height.

### B. **FEAT-01 (`U-B21`):** In `_sync_scope_widgets()`, when `scope == 'current'`, hide (`grid_remove()`/`pack_forget()`) BOTH `folder_path_entry` and `btn_browse_search_folder` while preserving `selected_search_folder` and `project_folder` untouched.

### C. **FEAT-02 (`U-B3`+`U-B5`, `U-B4`, `U-B13`):** Convert Player button to icon-only (`player.png`, NO `{0}` label text), move it OUT of the NGUI formatting ribbon into the speaker/text-actions area, and attach Unicode fallback + tooltip explaining `{playername}`/`{0}` (`AGENTS.md` §21). Remove standalone `[-]` button from NGUI ribbon (keep `[-]` in NGUI Glossary & menu).

### D. **FEAT-03 (`U-B6`, `U-B7`, `U-B8`, `U-B30`):** Rename `Continuous View` -> `All Script`. Group `Select Box`, `All Script`, and `Preview` into ONE unified `VIEW` group with icons + Unicode fallbacks + tooltips (`get_icon()` returns `None` if PNG absent). Update top headers to `Dialogue` / `All Script` (Preview OFF) and `Dialogue Preview` / `All Script Preview` (Preview ON). Rename bottom pane strictly to **`Raw Commands`**. Keep internal Python identifiers (`var_continuous_view`, etc.) unchanged to prevent test churn; sweep View menu, tooltips, and `README.md`.

### E. **BUG-39 + FEAT-04 (`U-B14`):** Replace the single packed `speaker_ribbon_row` with clean responsive `grid`/stacked rows (Speaker/View row + collapsible NGUI Ribbon row + Text/Box actions) so NO controls clip off-screen at 1280x720 or snapped ~960px widths. Add `View > Toggle NGUI Ribbon` persisted in `misora_config.json`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s11_toolbar_search_ui.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-38] Geometric assertion after `update_idletasks()`: `search_entry.winfo_rootx() == replace_entry.winfo_rootx()`, equal widths, and all 4 Find/Replace action buttons share identical `winfo_width()` and `winfo_height()`.
2. [Probe 2 — FEAT-01] Switching scope to `'current'` unmaps `folder_path_entry` & `btn_browse_search_folder` while `app.selected_search_folder` remains unchanged.
3. [Probe 3 — FEAT-02 & FEAT-03] Ribbon contains no standalone `[-]` button; Player button has no `{0}` text, sits outside NGUI ribbon, has tooltip; headers display `Dialogue` / `All Script` / `Dialogue Preview` / `All Script Preview` and bottom pane displays `Raw Commands`.
4. [Probe 4 — BUG-39 & FEAT-04] At `1280x720` and `960x720`, every visible toolbar group has `winfo_width() > 0` inside parent bounds; `View > Toggle NGUI Ribbon` hides/shows NGUI ribbon and persists preference.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_s8b4_ui_polishing.py` and `tests/test_misora_ui_integration.py` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT alter Select Box behavior (S12), rulers/Preview rendering (S14), or MTL drawer (S16).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s11_toolbar_search_ui.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s11_toolbar_search_ui -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s11_toolbar_search_ui -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
