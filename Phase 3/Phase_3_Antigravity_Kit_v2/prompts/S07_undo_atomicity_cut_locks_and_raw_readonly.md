/plan Implement S07: Caret Paste Dirty/Lock, Mutate-Before-Undo, Non-Contiguous Cut Undo, Lock Enforcement & Read-Only Raw in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/undo_journal.py @misora.py @tests/test_s7_undo_speaker_safety.py @tests/test_phase5_mtl_security_preview.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-10, BUG-13, BUG-15, BUG-16, BUG-37** (Track 1 · Group C2 (post-DEP-4)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S07` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/undo_journal.py (`BoxStructuralDelta` optional `indices` field)`
  * `misora.py (`_on_card_paste_caret`, `_on_dialogue_edited`, `_on_card_text_edited`, `_flush_continuous_card_edits`, `on_replace_next` undo order, `on_box_cut`, `_apply_delta` `BoxStructuralDelta`, `on_clear_dialogue_skeleton`, `TranslatorAssistantDialog._on_apply`, `txt_raw` read-only)`
  * `tests/test_p3_s07_undo_locks_raw.py (NEW)`
  * `CHANGELOG.md (append `### S07` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/script_codec.py`
  * `core/search_engine.py`
  * `core/mtl_engine.py`
5. **Changelog & Version Contract:**
   - Append `### S07` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S07`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name in `misora.py`: `_on_card_paste_caret`, `_on_dialogue_edited`, `_on_card_text_edited`, `_flush_continuous_card_edits`, `on_replace_next`, `on_box_cut`, `_apply_delta`, `on_clear_dialogue_skeleton`, `TranslatorAssistantDialog._on_apply`, `txt_raw`, `_update_raw_view`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-10, BUG-13, BUG-15, BUG-16, BUG-37)
==================================================
### A. **BUG-10 (`misora.py:_on_card_paste_caret()`):** Call `self._mark_document_dirty(self.current_file_path)` BEFORE `self._dirty_state_changed()` so S2 mirroring preserves `is_dirty=True` and title `*`. Check `self.is_box_locked(target_idx)` on every target box in the `\n\n\n` paste loop and skip locked boxes.

### B. **BUG-13 (`misora.py`):** In `_on_dialogue_edited()`, `_on_card_text_edited()`, `_flush_continuous_card_edits()`, and `on_replace_next()`, apply `inject_box()` to the model FIRST; record `BoxEditDelta` and mark dirty ONLY on success. Replace silent `except Exception: pass` with `self.logger.exception(...)` + `self.set_status(..., is_error=True)` (`AGENTS.md` §28).

### C. **BUG-15 (`core/undo_journal.py` + `misora.py`):** Add optional `indices: Optional[List[int]] = None` on `BoxStructuralDelta`. In `on_box_cut()`, refuse/skip locked boxes and store exact sorted target indices. In `_apply_delta(BoxStructuralDelta)`, restore each snapshot at its exact original index (ascending) on Undo and delete those exact indices on Redo.

### D. **BUG-16 (`misora.py`):** Enforce `is_box_locked()` at model/application level in `on_clear_dialogue_skeleton()` (skip locked boxes and report preserved count) AND `TranslatorAssistantDialog._on_apply()` (block with toast on locked box; read `txt_trans.get('1.0', 'end-1c')` without destructive `.strip()`).

### E. **BUG-37 (`misora.py:txt_raw`):** Keep `txt_raw` strictly read-only (`state='disabled'`, toggled to `'normal'` only inside `_update_raw_view()` then restored to `'disabled'`) until `FEAT-11` (`S19`) ships.

### F. **`CHANGELOG.md`:** Append `### S07` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s07_undo_locks_raw.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s07_undo_locks_raw` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-10] `\n\n\n` caret paste leaves `open_documents[p]['dirty'] == True` and `app.is_dirty == True` after `_dirty_state_changed()`, and skips locked boxes.
2. [Probe 2 — BUG-13] Mocking `inject_box` to raise `RuntimeError` during `_on_dialogue_edited()` leaves `undo_depth == 0`, `is_dirty == False`, and surfaces error on `lbl_status`.
3. [Probe 3 — BUG-15] Cutting non-contiguous boxes `[1, 4]` -> Undo -> Redo restores exact original order of all boxes; locked box cannot be cut.
4. [Probe 4 — BUG-16] `on_clear_dialogue_skeleton()` preserves locked boxes; `TranslatorAssistantDialog._on_apply()` refuses locked box and preserves leading/trailing whitespace & newlines.
5. [Probe 5 — BUG-37] `txt_raw.cget('state') == 'disabled'` after load and after `_update_raw_view()`.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_s7_undo_speaker_safety` and `tests.test_phase5_mtl_security_preview` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT implement editable Raw Commands (S19) or Replace-All overhaul (S09).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s07_undo_locks_raw.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s07_undo_locks_raw -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s07_undo_locks_raw` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s07_undo_locks_raw -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
