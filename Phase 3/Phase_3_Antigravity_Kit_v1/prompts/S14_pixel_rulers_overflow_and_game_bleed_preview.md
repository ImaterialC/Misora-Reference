<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S14
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> Proceed
- Model & Effort : Claude Sonnet 4.6 (Tkinter font metrics, Canvas ruler & hybrid Preview rendering)
- Cheap-Model OK : NO — Recommended Claude Sonnet 4.6 (subtle Tkinter pixel metrics & wrap='none' canvas geometry)
- Ledger Coverage: BUG-40, FEAT-09, FEAT-10 (Group G4 (post-DEP-2, DEP-8))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S14: Shared Pixel-Measure Helper, Calibrated Rulers (50x3), Remove Char Counter & Native Bleed Game Preview in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @misora.py @core/ngui_tags.py @tests/test_phase5_mtl_security_preview.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S14`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (shared pixel-measure helper, Canvas horizontal ruler, red vertical gutter line 4+, inline logical-line pixel overflow tag, remove lbl_char_count & card '(N chars)', Dialogue Preview & All Script Preview code-drawn 50x3 bleed frames, cstyle_* sweep)`
  * `AGENTS.md (update §19/D13 wording if still referencing 45-char counter)`
  * `README.md (remove stale '> 45 chars' counter wording)`
  * `tests/test_p3_s14_rulers_preview.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/ngui_tags.py (KEEP measure_line_lengths intact for backward-compatible unit tests!)`
  * `core/story_ast.py`
  * `assets/ (NO copyrighted AtlasAdv PNG bundled — NO-02!)`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S14`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `ruler_clean` (4300-4315), `ruler_cont` (4524-4539), `gutter_clean`, `_update_rendered_char_count()` (8449-8466), card `(N chars)` (7800-7807), `_insert_compiled_ngui_text()`, and `_on_toggle_preview_compiled()` in `misora.py`.
2. Check `tests/test_phase5_mtl_security_preview.py` to see if `test_06` tests `lbl_char_count` or `measure_line_lengths()` — note any existing test assertion in the Implementation Plan before touching UI labels (NEVER weaken tests without explicit approval!).
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-40, FEAT-09, FEAT-10)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-40, FEAT-09, FEAT-10**

### A. **BUG-40 + FEAT-09 (`U-B22..U-B26`, `DEP-8` — Lead Ruling #4):** (1) Create ONE shared pixel-measure helper (`_measure_dialogue_metrics`) driven directly by the active editor font (`safe_w = editor_font.measure('1234567890' * 5)` = 50 digit-widths, labeled as an estimate of in-game font width; strip NGUI tags before width measurement while keeping `{playername}` as realistic width, never 0). (2) Replace static `Consolas 9pt` string rulers with a pixel-calibrated `tk.Canvas` horizontal ruler aligned to the editor text origin, showing a **red zone past 50 digit-widths** (fixing the col-60 illusion). (3) Color vertical line-number gutter red from **line 4+** (`3+ linebreaks`). (4) Apply inline pixel-calibrated horizontal overflow highlighting on characters past `safe_w` per logical line (accurately handling narrow Latin vs ~2x wide Japanese CJK glyphs). (5) Remove inaccurate `lbl_char_count` and card `(N chars)` UI labels in this same release (keep `core/ngui_tags.py:measure_line_lengths()` intact).

### B. **FEAT-10 (`U-B27`, `U-B28` — Lead Ruling #4, `NO-02`, `NO-12`):** Implement code-drawn Priconne-style dialogue frames using native Tk primitives (cream/gold double frame, name plate, static pink `▼`, `best_contrast_fg()`, ZERO copyrighted `AtlasAdv` sprites). Enforce **`wrap='none'`** native game bleed semantics calibrated to **50 digit-widths × 3 lines** safe area with small margin to outer border — text visibly spills past the frame with **NO auto-shrinking**. (1) `Dialogue Preview`: single `tk.Canvas` + one embedded read-only `tk.Text` (restore caret/selection/`yview` on Preview OFF; sweep `cstyle_*` tags per render `GEM-E03`). (2) `All Script Preview`: lightweight styled `tk.Frame` cards (NO per-card Canvas). Pure presentation layer (zero doc/dirty/undo mutation; `BUG-11` guarantees plain-text saves stay safe). Box 0 Summary remains deferred (`DEF-04`).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s14_rulers_preview.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-40 & FEAT-09] 50 digits `'1234567890'*5` fits inside `safe_w` (NOT flagged overflow); 51 digits OR 30 full-width Japanese Kanji exceeding `safe_w` triggers horizontal overflow highlight; 4th line triggers red gutter highlight; `lbl_char_count` and `(N chars)` removed from editor UI.
2. [Probe 2 — FEAT-10] `Dialogue Preview` uses `wrap='none'` without auto-shrinking font size, preserves caret/selection on Preview OFF, sweeps old `cstyle_*` tags on box switch, and leaves `is_dirty == False` and `undo_depth == 0`.
3. [Probe 3 — FEAT-10] `All Script Preview` renders lightweight `tk.Frame` cards with `wrap='none'` (zero per-card `tk.Canvas` widgets).

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_p3_s05_doc_lifecycle_save.py` (plain-text save during Preview ON) still passes.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- NO `AtlasAdv` sprites (`NO-02`), NO Box 0 Summary profile (`DEF-04`), NO auto-shrinking text (`NO-12`).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s14_rulers_preview.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s14_rulers_preview -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s14_rulers_preview -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
