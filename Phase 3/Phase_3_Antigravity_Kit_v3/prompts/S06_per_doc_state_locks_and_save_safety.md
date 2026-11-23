/plan Implement S06: Per-Document State/Stable Locks, Plain-Text Preview Save, Windows LF Writes & 0-Box Save in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/text_encoding.py @misora.py @tests/test_s1_open_file_safety.py @tests/test_s2_dirty_contract.py @tests/test_s3_document_close.py @tests/test_s8b3_encoding_detection.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-11, BUG-12, BUG-18, BUG-19** (Track 1 · Group C1 (DEP-2, DEP-4)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S06` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/text_encoding.py (`write_atomic_encoded`)`
  * `misora.py (`open_file`, `close_file`, `_on_app_exit`, new `_save_document_entry`, stable lock-key helpers, `on_save`, `on_export_script`)`
  * `tests/test_p3_s06_doc_state_save.py (NEW)`
  * `CHANGELOG.md (append `### S06` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/script_codec.py`
  * `core/search_engine.py`
  * `core/mtl_engine.py`
5. **Changelog & Version Contract:**
   - Append `### S06` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S06`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name: `write_atomic_encoded` in `core/text_encoding.py`; `open_file`, `on_save`, `on_export_script`, `close_file`, `_on_app_exit`, `is_box_locked` in `misora.py`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-11, BUG-12, BUG-18, BUG-19)
==================================================
### A. **BUG-11 (`misora.py:on_save()` — DEP-2):** Plain-text `on_save()` MUST save authoritative `self._plain_text_content` — NEVER read stripped compiled text from `txt_dialogue` or `txt_continuous` while `var_preview_compiled` is True. Flush widget into `_plain_text_content` ONLY when Preview is OFF.

### B. **BUG-12 (`misora.py` — DEP-4):** Persist per-document state inside each `open_documents[path]` entry (`locked_box_uids`, `modified_box_uids`, immutable `original_jp_by_uid`, `current_box_idx`, `is_box0_active`) and restore on every tab switch (including cache hits) instead of clearing them in `open_file()`. Keep `is_box_locked(box_idx)` resolving via `box.uid` for backward compatibility. Add non-switching `_save_document_entry(path)` for saving inactive dirty docs during `close_file()` and `_on_app_exit()`. Provide reusable helpers for stable persisted lock identity `(box_ordinal, sha256(original_jp_text))` (never serializing runtime `Record.uid`).

### C. **BUG-18 (`core/text_encoding.py` + `misora.py:on_export_script()`):** Remove the `tmp_file.write_text(content)` branch in `write_atomic_encoded()`; ALWAYS write pre-encoded `data` via `tmp_file.write_bytes(data)` so LF-only files stay LF on Windows. Update `on_export_script()` to write atomically via `write_atomic_encoded(..., newline='\n')`.

### D. **BUG-19 (`misora.py:on_save()`):** Guard ALL three branches (preview, continuous, and page `inject_box()` call) when `not self.current_doc.boxes`, so 0-box metadata-only stories save cleanly without `IndexError`.

### E. **`CHANGELOG.md`:** Append `### S06` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s06_doc_state_save.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s06_doc_state_save` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-11] Save `.txt` containing `[FF0000]Red[-]` while `var_preview_compiled=True` -> disk file preserves exact `[FF0000]Red[-]` markup.
2. [Probe 2 — BUG-12] Doc A lock Box 2 + navigate Box 4 -> switch Doc B -> back to Doc A -> Box 2 STILL locked, active box 4, JP snapshot intact; closing dirty inactive Doc A saves without wiping its state.
3. [Probe 3 — BUG-18] `write_atomic_encoded()` with `newline='\n'` writes raw `b'a\nb'` (zero `\r\n`) on Windows; `on_export_script()` writes LF-only atomically.
4. [Probe 4 — BUG-19] Saving a 0-box metadata-only `StoryDocument` succeeds across Page, Continuous, and Preview modes with zero `IndexError`.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_s1_open_file_safety`, `tests.test_s2_dirty_contract`, `tests.test_s3_document_close`, and `tests.test_s8b3_encoding_detection` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT implement `.misora` workspace I/O (S16) or backup naming collisions (S09).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s06_doc_state_save.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s06_doc_state_save -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s06_doc_state_save` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s06_doc_state_save -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
