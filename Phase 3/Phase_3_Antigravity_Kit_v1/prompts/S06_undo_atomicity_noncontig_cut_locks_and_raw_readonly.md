<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S06
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> Proceed
- Model & Effort : Claude Sonnet 4.6
- Cheap-Model OK : NO — Recommended Claude Sonnet 4.6 (undo/lock integrity in misora.py)
- Ledger Coverage: BUG-10, BUG-13, BUG-15, BUG-16, BUG-37 (Group C2 (post-DEP-4))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S06: Mutate-Before-Undo, Caret Paste Dirty/Lock, Non-Contiguous Cut Undo, Lock Enforcement & Read-Only Raw in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/undo_journal.py @misora.py @tests/test_s7_undo_speaker_safety.py @tests/test_phase5_mtl_security_preview.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S06`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/undo_journal.py (BoxStructuralDelta optional exact `indices` field)`
  * `misora.py (_on_card_paste_caret, _on_dialogue_edited, _on_card_text_edited, _flush_continuous_card_edits, on_replace_next undo order, on_box_cut, _apply_delta BoxStructuralDelta, on_clear_dialogue_skeleton, TranslatorAssistantDialog._on_apply, txt_raw read-only)`
  * `tests/test_p3_s06_undo_locks_raw.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/script_codec.py`
  * `core/search_engine.py`
  * `core/mtl_engine.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S06`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `_on_card_paste_caret()` (7560-7620), `_on_dialogue_edited()` (8278-8344), `_on_card_text_edited()`, `_flush_continuous_card_edits()` (6870-6915), `on_box_cut()` (7415-7442), `_apply_delta(BoxStructuralDelta)` (9621-9629), `on_clear_dialogue_skeleton()` (10867-10904), `TranslatorAssistantDialog._on_apply()` (11839-11867), and `txt_raw` (4689-4703, `_update_raw_view`) in `misora.py`.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-10, BUG-13, BUG-15, BUG-16, BUG-37)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-10, BUG-13, BUG-15, BUG-16, BUG-37**

### A. **BUG-10 (`misora.py:_on_card_paste_caret()`):** Call `self._mark_document_dirty(self.current_file_path)` BEFORE `self._dirty_state_changed()` so S2 mirroring preserves `is_dirty=True` and title `*`. Check `self.is_box_locked(target_idx)` on every target box in the `\n\n\n` paste loop and skip locked boxes.

### B. **BUG-13 (`misora.py`):** In `_on_dialogue_edited()`, `_on_card_text_edited()`, `_flush_continuous_card_edits()`, and `on_replace_next()`, apply `inject_box()` to the model FIRST; record `BoxEditDelta` and mark dirty ONLY if `inject_box()` succeeds. Replace silent `except Exception: pass` with `self.logger.exception(...)` + `self.set_status(..., is_error=True)` (`AGENTS.md` §28).

### C. **BUG-15 (`core/undo_journal.py` + `misora.py`):** Extend `BoxStructuralDelta` with optional `indices: Optional[List[int]] = None` (backward-compatible default). In `on_box_cut()`, skip/refuse locked boxes and store exact sorted target indices on `BoxStructuralDelta`. In `_apply_delta(BoxStructuralDelta)`, restore each snapshot at its exact original index (ascending) on Undo and delete those exact indices on Redo.

### D. **BUG-16 (`misora.py`):** Enforce `is_box_locked()` at the model/application layer in `on_clear_dialogue_skeleton()` (skip locked boxes and report preserved count) AND `TranslatorAssistantDialog._on_apply()` (block with toast on locked box; read `txt_trans.get('1.0', 'end-1c')` without destructive `.strip()`).

### E. **BUG-37 (`misora.py:txt_raw`):** Keep `txt_raw` strictly read-only (`state='disabled'`, briefly toggled to `'normal'` only inside `_update_raw_view()` then returned to `'disabled'`) until `FEAT-11` (`S15`) ships.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s06_undo_locks_raw.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-10] `\n\n\n` caret paste marks `open_documents[p]['dirty'] == True`, keeps `app.is_dirty == True` after `_dirty_state_changed()`, and skips locked target boxes.
2. [Probe 2 — BUG-13] Mocking `inject_box` to raise `RuntimeError` during `_on_dialogue_edited()` leaves `undo_journal.undo_depth == 0`, `is_dirty == False`, and surfaces error on `lbl_status`.
3. [Probe 3 — BUG-15] Cutting non-contiguous boxes `[1, 4]` -> Undo -> Redo restores exact original order of all 6 boxes; attempting to cut a locked box preserves it.
4. [Probe 4 — BUG-16] `on_clear_dialogue_skeleton()` preserves locked boxes and clears unlocked ones; `TranslatorAssistantDialog._on_apply()` refuses locked box and preserves leading/trailing whitespace & newlines on unlocked box.
5. [Probe 5 — BUG-37] `txt_raw.cget('state') == 'disabled'` after load and after `_update_raw_view()`.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_s7_undo_speaker_safety.py` and `tests/test_phase5_mtl_security_preview.py` pass unchanged.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT implement editable Raw Commands (S15) or Replace-All multi-file rewrite (S07).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s06_undo_locks_raw.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s06_undo_locks_raw -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s06_undo_locks_raw -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
