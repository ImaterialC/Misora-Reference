<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S03
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> /boost (after Proceed)
- Model & Effort : Claude Opus 4.6 (HIGH risk: AST structural mutations & undo integrity — DO NOT use Flash or GPT-OSS 120B)
- Cheap-Model OK : NO — Use Claude Opus 4.6 (or Claude Sonnet 4.6 minimum)
- Ledger Coverage: BUG-02, BUG-05, BUG-06, BUG-17, HYG-04 (Group B2 (DEP-5 part 2))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S03: Kind-Conversion Box Separation, Structural Breaker/Voice Ownership, Multi-Segment Undo & Tombstones in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/story_ast.py @core/undo_journal.py @misora.py @tests/test_misora_core.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S03`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/story_ast.py (set_box_kind, inject_box, insert_box, delete_boxes, move_box, removed_records)`
  * `core/undo_journal.py (BoxEditDelta, BoxStructuralDelta, MasterUndoJournal.record)`
  * `misora.py (ONLY on_box_paste snapshot preservation, _apply_delta BoxEditDelta segment restore, and non-blocking 'N segs' badge in _update_views/_sync_clean_view_to_current_box)`
  * `tests/test_p3_s03_ast_mutations.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/script_codec.py`
  * `core/search_engine.py`
  * `core/bundle_io.py`
  * `misora.py (on_box_cut, on_save, search/replace, toolbars — owned by later sessions)`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S03`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `set_box_kind()` (409-449), `inject_box()` (451-526), `insert_box()` (530-587), `delete_boxes()` (589-612), `move_box()` (614-644) in `core/story_ast.py`.
2. Inspect `BoxEditDelta`, `BoxStructuralDelta`, and `MasterUndoJournal.record()` (215-218) in `core/undo_journal.py`.
3. Inspect `on_box_paste()` (7456-7498) and `_apply_delta()` (`BoxEditDelta` branch) in `misora.py`.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-02, BUG-05, BUG-06, BUG-17, HYG-04)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-02, BUG-05, BUG-06, BUG-17, HYG-04**

### A. **BUG-02 (`core/story_ast.py` — Lead Ruling (b)):** In `inject_box()` / `set_box_kind()`, capture the target box's primary `Record.uid` BEFORE mutation. Whenever converting `print <-> tag` (e.g., clearing speaker on a dialogue box adjacent to narration box(es)) would cause `_rebuild_boxes()` to merge adjacent boxes, insert the minimum valid empty boundary breaker (`cmd_id=10`) so they remain **separate boxes** (NEVER implicitly merge). Rebuild projection ONLY after full speaker + text record mutation (fixing stale `tag->print` speaker projection). Resolve target box by captured `Record.uid` instead of stale `box_index`.

### B. **BUG-05 (`core/story_ast.py` — Unified Structural Ownership `CLAUDE-N09`):** Across `insert_box()`, `delete_boxes()`, and `move_box()`: (1) A `cmd_id == 12` record with `vo_` argument immediately preceding a box's first segment is owned by that box — it moves with the box in `move_box()` and is handled/snapshotted consistently in `delete_boxes()`. (2) Remove ONLY positively identified empty projected tap-breakers (`cmd_id == 10` with empty args); NEVER delete `vo_` cues or unknown/meaningful interstitial commands. (3) Ensure `move_box()` inserts/preserves separating boundary breakers so moving never merges same-speaker boxes or stacks double breakers. (4) Snapshot all removed/moved structural records (including voice cues & boundary breakers) for exact Undo/Redo.

### C. **BUG-06 (`core/story_ast.py`, `core/undo_journal.py`, `misora.py` — Delegated Multi-Segment Policy):** Allow normal non-blocking typing on multi-segment boxes and show a small non-blocking `'N segs'` indicator badge when `len(box.segs) > 1`. Extend `BoxEditDelta` with optional `old_seg_texts: Optional[List[str]] = None` and `new_seg_texts: Optional[List[str]] = None` so Undo/Redo restores original segment splits losslessly via `inject_box(..., seg_texts=...)`. In `misora.py:on_box_paste()`, when internal `self._box_clipboard` matches system clipboard text, insert deep-copied `BoxSnapshot` objects directly (preserving `seg_texts`, `voice_cue`, `extra_args`) instead of flattening through `DialogueBlock`.

### D. **BUG-17 (`core/undo_journal.py:record()`):** Fix coalescing `same_box`: when BOTH `prev_delta.box_uid` and `delta.box_uid` are non-`None`, REQUIRE `prev_delta.box_uid == delta.box_uid`; fall back to `box_index` ONLY when at least one `box_uid` is `None`. When coalescing `BoxEditDelta`, also update `prev_delta.new_seg_texts = delta.new_seg_texts` so multi-seg undo restores the initial pre-coalesce segments.

### E. **HYG-04 (`core/story_ast.py`):** Clean/bound `StoryDocument.removed_records` once deleted records are physically removed from `self.records` and verify no active undo/serialization path depends on stale tombstones.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s03_ast_mutations.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-02] `[tag A][print B][tag C]` (no breakers) -> `inject_box(1, '', 'new B')` keeps 3 separate boxes, zero `IndexError`, survives `to_binary()`/`from_binary()` and Undo/Redo.
2. [Probe 2 — BUG-05] `move_box()` moves attached `cmd_id=12 vo_` cue with its box, preserves unknown interstitial commands, never merges same-speaker boxes, and `delete_boxes()` removes only empty tap-breaker (no double `touch` stacking across binary round-trip).
3. [Probe 3 — BUG-06] Editing a 2-segment box then Undo restores BOTH original segments verbatim; internal `on_box_paste()` preserves `seg_texts`, `voice_cue`, and `extra_args`.
4. [Probe 4 — BUG-17] Two `BoxEditDelta` records with different non-`None` `box_uid` values at the same `box_index` within 2s MUST NOT coalesce; coalesced multi-seg edits preserve `old_seg_texts` from the first edit and `new_seg_texts` from the last.
5. [Probe 5 — HYG-04] Repeated insert/delete cycles do not grow `doc.removed_records` unboundedly.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_p3_s02_ast_codec.py` and `tests/test_misora_core.py` pass with 0 failures.
2. [Guard 2] `cmd_id == 35` and `cmd_id == 32` remain unchanged.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT touch `core/script_codec.py` (S04) or `on_box_cut()` non-contiguous undo (S06).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s03_ast_mutations.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s03_ast_mutations -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s03_ast_mutations -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
