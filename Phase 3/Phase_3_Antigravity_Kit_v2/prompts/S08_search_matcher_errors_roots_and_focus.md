/plan Implement S08: Search Match-Case/Errors/Snapshots/Spans, Bounded Project Roots & Search Focus/Gutter/No-Op KeyRelease in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/search_engine.py @core/story_ast.py @misora.py @tests/test_s6_threading_decoupling.py @tests/test_s9a_search_unicode.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-21, BUG-22, BUG-23, BUG-30** (Track 1 · Group D1 (DEP-7 part 1)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S08` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/story_ast.py (ONLY `norm_search` `match_case` parameter)`
  * `core/search_engine.py (`_norm_search_with_spans`, `_compile_matcher`, `search_file`, `search_directory` error/skipped channel & raw span fix)`
  * `misora.py (`_detect_environment`, `_on_folder_path_var_trace`, `on_browse_project_folder`, `on_open_paths_dialog`, `on_start_search`, `_run_background_search`, `_process_search_queue`, `_select_result_index`, `_on_dialogue_edited` gutter update, `_commit_widget_edit`/`_on_card_text_edited`/`_on_box0_metadata_edited` no-op guard)`
  * `tests/test_p3_s08_search_roots_focus.py (NEW)`
  * `CHANGELOG.md (append `### S08` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/xunity_sync.py`
  * `core/mtl_engine.py`
  * `core/script_codec.py`
  * `misora.py (`on_replace_all`, `_apply_delta` — owned by S09)`
5. **Changelog & Version Contract:**
   - Append `### S08` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S08`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name in `core/search_engine.py`: `_norm_search_with_spans`, `_compile_matcher`, `search_file`, `search_directory`.
2. Bind by symbol name in `misora.py`: `_detect_environment`, `on_start_search`, `_run_background_search`, `_process_search_queue`, `_select_result_index`, `_on_dialogue_edited`, `_commit_widget_edit`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-21, BUG-22, BUG-23, BUG-30)
==================================================
### A. **BUG-21 (`core/story_ast.py` + `core/search_engine.py`):** Add `match_case: bool = False` to BOTH `story_ast.norm_search()` and `ProjectSearchEngine._norm_search_with_spans()` (preserving 100% S9a equivalence), applying `.casefold()` ONLY when `not match_case`. Wire `options.match_case` into whitespace-insensitive matching in `_compile_matcher()`.

### B. **BUG-22 (`core/search_engine.py` + `misora.py`):** (1) Stop silently swallowing bundle/text decode errors; add `os.walk(..., onerror=...)` and report structured `(path, reason)` skipped entries surfaced in the UI (clearly distinguishing 0 matches / matches / partial skipped / cancelled). (2) In `on_start_search()`, on snapshot failure NEVER fall back to live `orig_doc` (`Grok-E02`) — skip and report it; also snapshot open plain-text buffers and normalize lookup keys via `Path.resolve()`. (3) Add monotonic `self._search_seq` generation guard and block re-entrant `<Return>` while searching. (4) In `search_file()` raw-text fallback, do NOT fabricate `(0, len(box.clean_text))` — map raw spans accurately or mark as approximate raw match (`QW-E06`).

### C. **BUG-23 (`misora.py` — `GEM-N01`):** Replace (NEVER append indefinitely) project roots whenever `project_folder` changes; stop auto-injecting unrelated local `input`/`output`. Resolve Project Search cleanly into explicit bounded `(Text, RedirectedResources)` directories (never scanning `BepInEx/plugins/` or `config/`), while XUAT text roots resolve strictly to `BepInEx\Translation\en\Text`.

### D. **BUG-30 (`misora.py`):** Remove erroneous `self.txt_continuous.focus_set()` after `_focus_continuous_box()` for bundle Continuous View in `_select_result_index()`. Call `self._update_gutter_clean()` inside `_on_dialogue_edited()` so Page View line numbers update on Enter/Delete/Paste. Return `bool` from `_on_card_text_edited()` and `_on_box0_metadata_edited()` so `_commit_widget_edit()` skips `_dirty_state_changed()` on no-op arrow keys.

### E. **`CHANGELOG.md`:** Append `### S08` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s08_search_roots_focus.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s08_search_roots_focus` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-21] Match Case ON + Ignore Whitespace ON matches `'Hero'` and rejects `'hero'` with exact span equivalence to `norm_search()`.
2. [Probe 2 — BUG-22] Corrupt/unreadable file appears in skipped list (never silently 0); failed AST snapshot skips file instead of passing live `orig_doc`; stale `search_seq` messages are discarded; raw-text fallback never fabricates full-box clean spans.
3. [Probe 3 — BUG-23] Switching `project_folder` from ProjA to ProjB removes ProjA completely; selecting a `BepInEx` root scans only `Text` & `RedirectedResources` (ignores `plugins/`).
4. [Probe 4 — BUG-30] Search jump in Continuous View focuses active card widget (NOT `txt_continuous`); Enter in Page View updates `gutter_clean`; arrow-key `<KeyRelease>` in card & Box 0 triggers 0 `_refresh_opened_files_list()` calls.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_s6_threading_decoupling` and `tests.test_s9a_search_unicode` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT rewrite `on_replace_all` (S09) or build `core/xuat_index.py` (S22).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s08_search_roots_focus.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s08_search_roots_focus -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s08_search_roots_focus` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s08_search_roots_focus -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
