/plan Implement S04: Kind-Conversion Box Separation, Voice/Breaker Ownership, Multi-Segment Undo/Paste, UID Coalesce & Tombstones in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/story_ast.py @core/undo_journal.py @misora.py @tests/test_misora_core.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-02, BUG-05, BUG-06, BUG-17, HYG-04** (Track 1 · Group B2 (DEP-5 part 2)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S04` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/story_ast.py (`set_box_kind`, `inject_box`, `insert_box`, `delete_boxes`, `move_box`, `removed_records`)`
  * `core/undo_journal.py (`BoxEditDelta`, `BoxStructuralDelta`, `MasterUndoJournal.record`)`
  * `misora.py (ONLY `on_box_paste` internal `BoxSnapshot` preservation, `_apply_delta` `BoxEditDelta` segment restore, and non-blocking `'N segs'` badge)`
  * `tests/test_p3_s04_ast_mutations.py (NEW)`
  * `CHANGELOG.md (append `### S04` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/script_codec.py`
  * `core/search_engine.py`
  * `core/bundle_io.py`
  * `misora.py (on_box_cut, on_save, search/replace, toolbars)`
5. **Changelog & Version Contract:**
   - Append `### S04` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S04`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name in `core/story_ast.py`: `set_box_kind`, `inject_box`, `insert_box`, `delete_boxes`, `move_box`, `removed_records`.
2. Inspect `BoxEditDelta`, `BoxStructuralDelta`, and `MasterUndoJournal.record` in `core/undo_journal.py`.
3. Inspect `on_box_paste` and `_apply_delta` (`BoxEditDelta` branch) in `misora.py`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-02, BUG-05, BUG-06, BUG-17, HYG-04)
==================================================
### A. **BUG-02 (`core/story_ast.py` — Lead Ruling (b)):** In `inject_box()` / `set_box_kind()`, capture the target box's primary `Record.uid` BEFORE mutation. Whenever converting `print <-> tag` (e.g., clearing a speaker adjacent to narration box(es)) would cause `_rebuild_boxes()` to collapse adjacent boxes, insert the minimum valid empty boundary breaker (`cmd_id=10`) so they remain **separate boxes** (NEVER implicitly merge). Rebuild projection ONLY after full speaker + text record write (fixing stale `tag->print` speaker projection). Resolve target box by captured `Record.uid` instead of stale `box_index`.

### B. **BUG-05 (`core/story_ast.py` — Unified Structural Ownership `CLAUDE-N09`):** Across `insert_box()`, `delete_boxes()`, and `move_box()`: (1) A `cmd_id == 12` record with `vo_` argument immediately preceding a box's first segment is owned by that box — it moves with the box in `move_box()` and is handled/snapshotted consistently in `delete_boxes()`. (2) Remove ONLY positively identified empty projected tap-breakers (`cmd_id == 10` with empty args); NEVER remove `vo_` cues or unknown/meaningful interstitial commands. (3) Prevent double breakers and unintended box merges across moves/deletes. (4) Snapshot all affected structural records for exact Undo/Redo.

### C. **BUG-06 (`core/story_ast.py`, `core/undo_journal.py`, `misora.py` — Delegated Multi-Segment Policy):** Allow normal non-blocking typing on multi-segment boxes + show a small non-blocking `'N segs'` badge when `len(box.segs) > 1`. Extend `BoxEditDelta` with optional `old_seg_texts: Optional[List[str]] = None` and `new_seg_texts: Optional[List[str]] = None` so Undo/Redo restores original segment splits losslessly via `inject_box(..., seg_texts=...)`. In `misora.py:on_box_paste()`, when internal `self._box_clipboard` matches system clipboard text, insert deep-copied `BoxSnapshot` objects directly (preserving `seg_texts`, `voice_cue`, `extra_args`) instead of flattening through `DialogueBlock`.

### D. **BUG-17 (`core/undo_journal.py:record()`):** When BOTH `prev_delta.box_uid` and `delta.box_uid` are non-`None`, REQUIRE `prev_delta.box_uid == delta.box_uid`; fall back to `box_index` ONLY when at least one `box_uid` is `None`. Propagate `new_seg_texts` on coalescing so multi-seg undo restores initial pre-coalesce segments.

### E. **HYG-04 (`core/story_ast.py`):** Clean/bound `StoryDocument.removed_records` once deleted records are physically removed from `self.records` and confirmed unreferenced by active undo/rollback paths.

### F. **`CHANGELOG.md`:** Append `### S04` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s04_ast_mutations.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s04_ast_mutations` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-02] `[tag A][print B][tag C]` (no breakers) -> `inject_box(1, '', 'new B')` keeps 3 separate boxes with zero `IndexError`, surviving binary round-trip and Undo/Redo.
2. [Probe 2 — BUG-05] `move_box()` moves attached `cmd_id=12 vo_` cue with its box, preserves unknown interstitial commands, never merges same-speaker boxes; `delete_boxes()` removes only empty tap-breaker (no double `touch` stacking across binary round-trip).
3. [Probe 3 — BUG-06] Editing a 2-segment box then Undo restores BOTH original segments verbatim; internal `on_box_paste()` preserves `seg_texts`, `voice_cue`, and `extra_args`.
4. [Probe 4 — BUG-17] Two `BoxEditDelta` ops with different non-`None` `box_uid` at the same `box_index` within 2s MUST NOT coalesce; coalesced multi-seg edits keep initial `old_seg_texts` and final `new_seg_texts`.
5. [Probe 5 — HYG-04] Repeated insert/delete cycles do not grow `doc.removed_records` unboundedly.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_p3_s03_binary_v2` and `tests.test_misora_core` pass; `cmd_id` 35 & 32 remain unchanged.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT touch `core/script_codec.py` (S05) or `on_box_cut` non-contiguous undo (S07).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s04_ast_mutations.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s04_ast_mutations -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s04_ast_mutations` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s04_ast_mutations -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
