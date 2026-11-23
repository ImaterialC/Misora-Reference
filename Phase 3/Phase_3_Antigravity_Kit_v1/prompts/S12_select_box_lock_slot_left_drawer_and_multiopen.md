<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S12
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan -> Proceed
- Model & Effort : Gemini 3.8 Flash (or Claude Sonnet 4.6 for Plan -> Flash for Execute)
- Cheap-Model OK : YES (cleanly scoped UI widgets building on already-fixed S05 state & S09 deferred startup)
- Ledger Coverage: BUG-41, FEAT-05, FEAT-06, FEAT-07 (Group G2 (post-DEP-4, DEP-9))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S12: Select Box in Both Views + Reserved Lock Slot, Collapsible Left Drawer, Empty State & Batched Multi-Open in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @misora.py @tests/test_s1_open_file_safety.py @tests/test_s4_view_model_sync.py @tests/test_s8b4_ui_polishing.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S12`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (_on_toggle_select_box_mode, _render_continuous_view Card #0 & lock slot, Dialogue header select checkbox, _toggle_dock_collapse left drawer, empty-state Open Files canvas/frame, btn_tab_files double-click, on_open_file askopenfilenames batched refresh)`
  * `tests/test_p3_s12_selection_drawer_open.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/*.py`
  * `assets/*.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S12`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `_on_toggle_select_box_mode()` (7109-7116), `_render_continuous_view()` (7695-7825), `_toggle_dock_collapse()` (9791-9815), `btn_tab_files` (3575-3584), and `on_open_file()` (9030-9055) in `misora.py`.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-41, FEAT-05, FEAT-06, FEAT-07)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-41, FEAT-05, FEAT-06, FEAT-07**

### A. **BUG-41 + FEAT-05 (`U-B11`, `U-B12`, `U-B29`):** (1) Make `Select Box` work in BOTH `Dialogue` and `All Script` views: in `Dialogue` view display an inline header checkbox `[ ] Select Box #N (X selected)` so the user can step across boxes and check/uncheck specific boxes into `_selected_boxes` for multi-box Copy/Cut (removing the misleading no-op toast). (2) Restore Box 0 (`-1`) Select Box checkbutton on Card #0 (`hdr_0`) in `All Script`. (3) Place the per-card Translation Lock button/icon immediately to the RIGHT of the Select Box checkbox inside a **fixed reserved slot width** so headers NEVER shift horizontally when `Select Box` mode toggles.

### B. **FEAT-06 (`U-B15`):** Extend existing pane-based `_toggle_dock_collapse()` / `_dock_collapsed` into a clean collapsible left drawer for `Search Results` / `Opened Files` (strictly pane-based inside `h_paned` — NEVER a `place()` overlay `NO-11`).

### C. **FEAT-07 (`U-B16`, `U-B19`, `U-B20`):** (1) Empty state (startup / 0 open files): display a centered large `'Open Files'` button with clear drag-and-drop `.unity3d` / `.misora` workspace hint underneath (reusing existing DnD handlers, hidden automatically once >=1 file opens). (2) Bind `<Double-Button-1>` on `Opened Files` tab (`btn_tab_files`) to `self.on_open_file()`. (3) Update `on_open_file()` to use `filedialog.askopenfilenames()`, preserving S1 staged semantics and performing ONE batched UI refresh at the end instead of N full `_update_views()` passes.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s12_selection_drawer_open.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-41 & FEAT-05] Enabling Select Box in `Dialogue` view shows inline checkbox; checking Box 1 & Box 3 populates `_selected_boxes == {0, 2}`; Card #0 in `All Script` has Select Box checkbox; lock icon sits right of checkbox slot with identical x-coordinate when Select Box toggles.
2. [Probe 2 — FEAT-06] Left drawer collapses and expands cleanly via pane controls without `place()` overlay.
3. [Probe 3 — FEAT-07] Empty state shows centered Open Files button when 0 docs open and hides when doc opens; double-clicking `btn_tab_files` invokes `on_open_file`; `on_open_file()` accepts multiple paths via `askopenfilenames` and calls `_update_views()` once for the batch.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_s1_open_file_safety.py`, `test_s4_view_model_sync.py`, `test_s8b4_ui_polishing.py` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT implement `.misora` serialization yet (S13).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s12_selection_drawer_open.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s12_selection_drawer_open -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s12_selection_drawer_open -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
