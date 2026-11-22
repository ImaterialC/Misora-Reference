# MISORA EDITOR — LOCKED & PARKED S8b-1 PROMPT (NARROWED DIALOGUE BOX PREVIEW)

> **Status:** UNANIMOUS LOCK by GPT, Qwen, and Gemini on 2026-11-22.
> **State:** **PARKED**. Strictly forbidden from early execution before S2 through S7 data integrity slices are completed.
> **Scope:** In-game Princess Connect! Re:Dive dialogue box aesthetic, cream background (#F9F5EA/#FFFDF6), double gold border, static pink indicator (▼), read-only toast with cooldown, strict wordwrap handling (summary box wraps, story box does NOT wrap).

`plaintext
/plan Implement S8b: Narrowed Game-Style Dialogue Box Preview inside Misora Editor's existing single-Box Page View Preview mode.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @misora.py @core/ngui_tags.py @docs/SCRIPT_FORMAT.md @tests/

Note: If the user attached `bandicam 2026-11-22 02-28-14-200.jpg`, use it ONLY as visual layout reference for the cream/gold dialogue box and pink `▼` marker — NOT to expand scope to menus, backgrounds, or other game screens.

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. Planning-First Gate (STRICT):
   - Do NOT modify any source or test files during this `/plan` phase.
   - Explore the live local workspace (`D:\Misora-Editor`), produce a clear **Implementation Plan artifact**, and WAIT for the user to approve (`Proceed`) before editing any file.
   - Once the user approves (`Proceed`), execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. Workspace & Git Safety:
   - Use the live local repository as the sole source of truth; ignore stale line numbers from old reports.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive checkout, `git commit`, or `git push`.
   - If unexpected unrelated uncommitted changes exist (other than already-reviewed S1 work if not yet committed), STOP and report them in the plan before proposing edits.
3. Allowed File Ownership (after approval):
   - `misora.py` (scoped to Page View Preview presentation and tightly related helpers)
   - Focused new test file `tests/test_s8b_dialogue_preview.py`
   - `PROJECT_STATE.md` (measured verification update only)
   - DO NOT modify `core/story_ast.py`, `core/bundle_io.py`, `core/undo_journal.py`, `core/mtl_engine.py`, `core/search_engine.py`, or unrelated modules.
4. No new external dependencies (pure Python/Tkinter stdlib only). No runtime DPI-awareness changes (`AGENTS.md` Rule 23).
5. Never skip, weaken, or silently mock existing tests. Note: `test_phase3_performance_config.py::test_05_clean_committed_config_has_no_machine_paths` is a known pre-existing failure on this machine due to untracked local `misora_config.json`; report it honestly and do NOT modify or weaken it.

==================================================
PART 1 — PREFLIGHT REPORT (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect the live workspace and report:
- Current Git branch, HEAD commit hash, and `git status --short`.
- Active Python 3.12 interpreter path/version (`py -3.12` preferred) and Tk version (`tkinter.TkVersion`).
- Exact current functions/widgets handling Page View Preview (`var_preview_compiled`, `_insert_compiled_ngui_text`, `_get_active_text_widget`, `_sync_gd_scroll_bounds`, `_update_rendered_char_count`, and Preview OFF focus/caret restoration).
- Confirmation that `tk.Text.count(..., "lines" / "xpixels" / "ypixels")` works as expected on this Windows Tk 8.6 runtime.

==================================================
PART 2 — LOCKED DESIGN SPECIFICATION (STRICT v1 SCOPE)
==================================================

### A. Visual Scope & Explicit Non-Goals
Implement ONLY a lightweight, read-only, code-drawn Princess Connect! Re:Dive-style dialogue panel for proofreading spatial fit:
- Fixed-size light/cream panel (`#F9F5EA` / `#FFFDF6`) with decorative double gold border (`#C9A25F` / `#E8CF96`) and dark ink text verified via `best_contrast_fg()`.
- Rendered dialogue text reusing Misora's existing NGUI renderer (`_insert_compiled_ngui_text` / `core/ngui_tags.py`).
- Static pink downward triangle (`▼`) in the bottom-right margin drawn via anti-aliased `Canvas.create_text(..., text="▼")` (NOT jagged `create_polygon`, zero image assets).
- Compact diagnostic badge/tooltip underneath showing fit/overflow status and honest disclosures.

EXPLICIT NON-GOALS (DO NOT IMPLEMENT):
- NO original game assets, portraits, sprites, or character atlas support.
- NO background/scene art, fog, particles, animation, or recurring timers/`after()` loops.
- NO typewriter effects, auto-advance, voice/audio playback, or game MENU/Skip/Auto/Speed/Bookmark/Log.
- NO full-application reskin, NO Box 0 Summary Preview, NO Full Story Script Display / Continuous View game-skin.
- NO Lock UX changes, Pin Speaker changes, rich tooltips, ribbon redesign, or S2–S7 changes.

### B. Exact Integration Boundary
- Activate this game-style dialogue panel ONLY for **Single-Box (Page) View** when Preview is ON and a normal dialogue Box is active.
- When Preview is ON for **Box 0 (Metadata/Summary)** or a **plain-text file**, keep the existing standard read-only compiled fallback cleanly (do NOT force them into the 3-line dialogue panel).
- Keep **Continuous View** Preview untouched (lightweight read-only compiled cards; NO per-card Canvas, NO inaccurate card-width overflow badge).
- When Preview is turned OFF, restore the real Page Editor's focus, caret position, and selection cleanly so the user is never left without an editable cursor.

### C. Rendering Architecture & Fixed Pixel Geometry
Use a **Hybrid** widget created once and reused across box navigation (zero per-box Canvas creation):
- **Host `tk.Canvas`:** Fixed max height (`safe_panel_h + bottom_spill_cap`), draws static cream interior, decorative double gold border anchored to `(safe_panel_w, safe_panel_h)`, outer margin tick marks at `x = safe_right` and `y = safe_bottom`, and the anti-aliased pink `▼` glyph in the dedicated right-margin gutter (outside the text column).
- **One embedded read-only `tk.Text`:** Embedded via `Canvas.create_window(x, y, window=text, width=..., height=...)` with `bd=0`, `highlightthickness=0`, `padx=0`, `pady=0`, `state="disabled"`. NEVER rely on `tk.Text(width=50)` character units to lock pixel width.
- **Locked Calibration (`50 × 3` Pixel Ruler, NOT a 50-char limit):**
  - `safe_text_w = preview_font.measure("1234567890" * 5)`
  - `safe_text_h = 3 * (preview_font.metrics("linespace") + line_spacing)`
  - Safe dimensions derive from the base preview font; rendered dimensions honor active NGUI formatting tags.
- **Z-Order Rule (CRITICAL TKINTER CONSTRAINT):** Standard Canvas vector items (`create_line`) ALWAYS render behind `create_window` widgets. Therefore, draw the horizontal/vertical overflow boundary dividers that cross the `tk.Text` spill region as raised 1–2px child `tk.Frame` dividers (created as later Canvas windows or `place()` + `lift()` above the embedded `tk.Text`), paired with Canvas tick marks in the outer margins.
- **Viewport Clamp Exemption:** Inspect `_sync_gd_scroll_bounds()` and exempt the preview host so shrinking the main window (`width = max(viewport_w, panel_w)`) NEVER squeezes the fixed dialogue panel or fabricates false overflow. Keep inner Preview scrollbars (text spill inspection) separate from outer workspace scrolling.

### D. Wrapping (`wrap="none"`) & Simultaneous Dual-Axis Overflow
- **Mandatory Wrapping:** Set **`wrap="none"`** on the new Preview `tk.Text` ONLY. Preserve existing wrapping on `txt_dialogue`, `txt_continuous`, Continuous cards, and `txt_box0_summary`.
- **Single-Helper Native Measurement:**
  - Normalize `tk.Text.count()` returns (`None`, `int`, or `tuple`) in one tested helper.
  - Perform **exactly one guarded `update_idletasks()`** per Preview render (never inside `<Configure>`) before measuring.
  - Use `count("1.0", "end-1c", "lines")`, `count("1.0", "end-1c", "ypixels")`, and per-line `count(f"{i}.0", f"{i}.end", "xpixels")`. Use `end-1c` so Tk's mandatory trailing newline never causes a false +1 line count.
  - NEVER use `dlineinfo()` to measure total height/overflow (returns `None` for off-screen lines); use `dlineinfo()` / `@x,y` index mapping ONLY for positioning visible dividers and tinting visible overflow ranges.
- **Horizontal Overflow (including within safe lines 1–3):**
  - Fires when any logical line's rendered `xpixels > safe_text_w`.
  - Expand the embedded `tk.Text` rightward into a bounded right-spill region (with horizontal scrollbar fallback if exceeding the right spill cap), show the raised vertical boundary divider at `x = safe_right`, highlight the spilled substring natively via `widget.index(f"@{safe_right},{line_y}")` to line end (no per-character measurement loops), and identify the offending line(s).
- **Vertical Overflow (Mandatory `OR` Condition):**
  - Fires when **`logical_lines > 3` OR `rendered_ypixels > safe_text_h`** (catches 2-line text with `<size=160%>`).
  - Keep the decorative gold panel pinned at `safe_panel_h`, expand `tk.Text` downward into a bounded bottom-spill region (with vertical scrollbar fallback if exceeding the cap), show the raised horizontal boundary divider at `y = safe_bottom`, and visually distinguish safe lines 1–3 (cream) from overflow lines (pale rose tint).
- **Simultaneous Dual-Axis Overflow:**
  - Horizontal and vertical overflow are independent and MUST work together (top-left `50 × 3` safe intersection), rendering both dividers and reporting both conditions in one concise diagnostic line (e.g., `⚠ Line 2 too wide · 4/3 lines`).

### E. NGUI Rendering, Legacy Counter Reconciliation & Honest Disclosures
- Sweep dynamic `cstyle_*` gradient tags on the Preview `tk.Text` before every populate so repeated navigation never accumulates unbounded Tcl tags.
- Preview-only `{playername}` / `{0}` handling: substitute a fixed representative sample name on a **temporary string copy** before rendering (never mutate `Box` data) and disclose it.
- Reconcile `_update_rendered_char_count()` (existing 45-char heuristic): avoid showing contradictory overflow verdicts alongside the new pixel-calibrated panel (relabel the legacy counter clearly as an approximate char heuristic and treat the Preview panel as authoritative in Preview mode).
- Badge/tooltip disclosures MUST honestly note: `wrap="none"` models worst-case non-NGUI scenes (no auto-shrink), Windows system fonts approximate Unity NGUI metrics, inline ruby conservatively inflates measured width, and `{playername}` uses a preview sample name.

### F. Strict Read-Only, Data Integrity, Performance & Fallback Invariants
- Pure presentation layer: NEVER mutate `StoryDocument`, `Box`, `clean_text`, raw NGUI, `UndoJournal`, `is_dirty`, or serialized output.
- Tag the preview `tk.Text` (e.g., `_misora_preview_only = True`) and exclude it from `_get_active_text_widget()`, edit commits, and `on_save()`.
- Keep text selection and `Ctrl+C` working; edit attempts show a `time.monotonic()`-cooldown toast via existing `show_toast` (ZERO new `after()` timers or animation loops).
- Performance target: ~40 ms navigation/render on the active Box only (never render/measure all boxes).
- **Agreed Fallback Criterion:** If Windows DPI scaling (100% / 125% / 150%) causes persistent divider misalignment, flicker, focus regression, or unacceptable latency, simplify cleanly to a cream `tk.Frame` + read-only `tk.Text` (`wrap="none"`) + dual-axis numeric overflow badges.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create `tests/test_s8b_dialogue_preview.py` using existing `unittest` conventions and run it BEFORE implementing S8b (confirming defect tests fail) and AFTER implementing S8b (confirming PASS). Use real Tk measurements wherever GUI is available; never fake geometry proofs with mocks.

Minimum required test cases:
1. Exactly 3 normal lines fit with zero overflow flags.
2. A 4th normal line triggers vertical overflow (`logical_lines > 3`).
3. 2 lines with `<size=160%>` exceeding `safe_text_h` trigger vertical overflow (`ypixels > safe_text_h`).
4. 1 over-wide line triggers horizontal overflow WITHOUT inflating logical line count, and marks horizontal spill within safe lines 1–3.
5. Simultaneous horizontal + vertical overflow reports both conditions together and activates both dividers.
6. Trailing `\n` does NOT create a false extra line (`end-1c` handling).
7. Repeated gradient navigation sweeps `cstyle_*` tags (tag count stays bounded).
8. Narrowing the application viewport does NOT shrink logical `safe_text_w` or fabricate false overflow.
9. Preview navigation/rendering leaves `Box` fields, `UndoJournal`, `is_dirty`, and serialized output completely unchanged, and keeps the preview widget excluded from `_get_active_text_widget()`.
10. `Ctrl+C` selection/copy remains usable in Preview, and toggling Preview OFF restores focus/caret to the real Page Editor.
11. Box 0 and plain-text Preview ON safely use the standard read-only fallback (never forced into the 3-line panel).
12. `count()` return normalizer handles `None`, `int`, and `tuple` cleanly.

==================================================
PART 4 — DELIVERABLES
==================================================
1. **Now (during `/plan` — ZERO file edits):**
   Produce an **Implementation Plan artifact** containing:
   - Preflight verification results (branch, HEAD, `git status`, Python/Tk versions, verified integration points).
   - Minimal widget hierarchy, z-order divider plan, and lifecycle.
   - Exact `count()` measurement & `_update_rendered_char_count()` reconciliation strategy.
   - Planned `tests/test_s8b_dialogue_preview.py` cases and any environment/manual Windows DPI (100/125/150% + JP/EN) verification items.
   - Any risks or contradictions found in the live code.
   STOP and wait for user approval (`Proceed`).

2. **After user clicks `Proceed`:**
   - Implement failing-first tests -> record pre-fix output -> implement S8b -> run:
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_s8b_dialogue_preview -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** with exact commands, real outputs, `git status --short`, measured Preview switch timing, and a short manual Windows DPI checklist (100/125/150%, JP/EN, `Ctrl+C`, Preview OFF caret restore).
`
