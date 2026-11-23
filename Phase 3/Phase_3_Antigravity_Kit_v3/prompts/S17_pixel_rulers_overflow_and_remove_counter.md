/plan Implement S17: Shared Pixel-Measure Helper, Calibrated Rulers (50 Digit-Widths / Line 4+) & Remove Char Counter in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @misora.py @core/ngui_tags.py @tests/test_phase5_mtl_security_preview.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-40, FEAT-09** (Track 2 · Group G4a (DEP-8 — Split from Preview per Grok/Gemini R2)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S17` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (shared pixel-measure helper, Canvas horizontal ruler aligned to editor text origin, red vertical gutter line 4+, inline logical-line pixel overflow highlight, remove `lbl_char_count` & card `(N chars)`)`
  * `README.md (remove stale `> 45 chars` counter wording if remaining)`
  * `tests/test_p3_s17_pixel_rulers.py (NEW)`
  * `CHANGELOG.md (append `### S17` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/ngui_tags.py (KEEP `measure_line_lengths()` intact for backward-compatible unit tests!)`
  * `core/story_ast.py`
  * `assets/ (NO `AtlasAdv` sprites — `NO-02`)`
5. **Changelog & Version Contract:**
   - Append `### S17` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S17`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name in `misora.py`: `ruler_clean`, `ruler_cont`, `gutter_clean`, `_update_rendered_char_count`, and card `(N chars)` header creation in `_render_continuous_view`.
2. Inspect `tests/test_phase5_mtl_security_preview.py` to check whether `test_06` inspects `lbl_char_count` or `measure_line_lengths()` — surface any conflict in the Plan Artifact before editing (NEVER weaken existing tests silently!).

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-40, FEAT-09)
==================================================
### A. **BUG-40 + FEAT-09 (`U-B22..U-B26`, `DEP-8` — Lead Ruling #4):** (1) Create ONE shared pixel-measure helper (`_measure_dialogue_metrics`) driven directly by the active editor font (`safe_w = editor_font.measure('1234567890' * 5)` = 50 digit-widths, labeled as an estimate of the in-game font; strip NGUI tags before width measurement while giving `{playername}` a realistic non-zero width). (2) Replace static `Consolas 9pt` string rulers with a pixel-calibrated `tk.Canvas` horizontal ruler aligned to the editor text origin, showing a **red zone past 50 digit-widths** (fixing the col-60 illusion). (3) Color vertical line-number gutter red from **line 4+** (3 or more linebreaks). (4) Apply inline pixel-calibrated horizontal overflow highlighting on characters past `safe_w` per logical line (accurately handling narrow Latin vs ~2x wide Japanese CJK glyphs). (5) Remove inaccurate `lbl_char_count` and card `(N chars)` UI labels in this same session (keep `core/ngui_tags.py:measure_line_lengths()` intact).

### B. **`CHANGELOG.md`:** Append `### S17` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s17_pixel_rulers.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s17_pixel_rulers` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-40 & FEAT-09] `'1234567890'*5` fits inside `safe_w` (NOT flagged overflow); 51 digits OR wide Japanese Kanji exceeding `safe_w` triggers horizontal overflow highlight; 4th line (3+ linebreaks) triggers red gutter tag; `lbl_char_count` and `(N chars)` are removed from editor UI.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `core.ngui_tags.measure_line_lengths()` remains importable and passing; existing `tests.test_phase5_mtl_security_preview` passes.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT implement game-style Preview frames yet (S18). Box 0 Summary remains unmeasured/deferred (`DEF-04`).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s17_pixel_rulers.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s17_pixel_rulers -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s17_pixel_rulers` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s17_pixel_rulers -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
