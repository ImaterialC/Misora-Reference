<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S05
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> Proceed
- Model & Effort : Claude Sonnet 4.6 (Core document lifecycle & save safety)
- Cheap-Model OK : NO — Recommended Claude Sonnet 4.6
- Ledger Coverage: BUG-11, BUG-12, BUG-18, BUG-19, BUG-20 (Group C1 (DEP-2, DEP-4))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S05: Per-Document State/Stable Locks, Plain-Text Preview Save, Atomic LF Writes, 0-Box Save & Backups in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/text_encoding.py @misora.py @tests/test_s1_open_file_safety.py @tests/test_s2_dirty_contract.py @tests/test_s3_document_close.py @tests/test_s8b3_encoding_detection.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S05`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/text_encoding.py (write_atomic_encoded)`
  * `misora.py (open_file, close_file, _on_app_exit, new _save_document_entry helper, on_save, on_export_script, backup filename helper)`
  * `tests/test_p3_s05_doc_lifecycle_save.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/script_codec.py`
  * `core/search_engine.py`
  * `core/mtl_engine.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S05`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `write_atomic_encoded()` (180-215) in `core/text_encoding.py`.
2. Inspect `open_file()` (6495-6669), `on_save()` (8475-8610), `on_export_script()`, `close_file()` (9865-9930), `_on_app_exit()`, and Replace-All backup naming (9440-9472) in `misora.py`.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-11, BUG-12, BUG-18, BUG-19, BUG-20)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-11, BUG-12, BUG-18, BUG-19, BUG-20**

### A. **BUG-11 (`misora.py:on_save()` — DEP-2):** For plain-text files (`not self.is_bundle_file and not self.current_doc`), save authoritative `self._plain_text_content` — NEVER read stripped compiled text from `txt_dialogue` or `txt_continuous` while `var_preview_compiled` is True. Flush the editor widget into `_plain_text_content` ONLY when Preview is OFF.

### B. **BUG-12 (`misora.py` — DEP-4):** Store per-document state inside each `open_documents[path]` entry (`locked_box_uids: Set[int]`, `modified_box_uids: Set[int]`, immutable `original_jp_by_uid: Dict[int, str]`, `current_box_idx: int`, `is_box0_active: bool`) and restore it on every tab switch (including cache hits) instead of wiping them in `open_file()`. Keep `is_box_locked(box_idx)` resolving via `box.uid` (maintaining compatibility with existing callers/tests). Add a non-switching `_save_document_entry(path)` helper used by `close_file()` and `_on_app_exit()` so saving inactive dirty tabs does not call `open_file(p)` and wipe state. Also add pure helper functions for the stable persisted lock key `(box_ordinal, sha256(original_jp_text))` so `FEAT-08` (`.misora`) can reuse them cleanly without serializing runtime `Record.uid`.

### C. **BUG-18 (`core/text_encoding.py` + `misora.py:on_export_script()`):** Remove the `tmp_file.write_text(content)` branch in `write_atomic_encoded()` (lines 189-190); ALWAYS write pre-encoded `data` via `tmp_file.write_bytes(data)` so LF-only files stay LF on Windows. Update `on_export_script()` to write via `write_atomic_encoded(..., newline='\n')`.

### D. **BUG-19 (`misora.py:on_save()`):** Guard ALL three branches (preview at 8519, continuous at 8524, and page `inject_box()` call at 8529) when `not self.current_doc.boxes`, so saving a 0-box metadata-only story succeeds cleanly without `IndexError`.

### E. **BUG-20 (`misora.py` — `QW-B17` + `Grok-N03`):** Introduce one shared collision-resistant backup path helper using microsecond timestamp (`%Y%m%d_%H%M%S_%f`) + short deterministic SHA-256 prefix of the normalized full source path (and ensuring non-existence before copy) and use it across BOTH normal `on_save()` (8494-8495, 8550-8551) AND `on_replace_all()` (9467-9468).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s05_doc_lifecycle_save.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-11] Open `.txt` containing `[FF0000]Red[-]`, toggle `var_preview_compiled=True`, call `on_save()` -> disk file retains exact `[FF0000]Red[-]` tags.
2. [Probe 2 — BUG-12] Open Doc A, lock Box 2 & navigate to Box 4 -> switch to Doc B -> switch back to Doc A -> Box 2 is STILL locked, active box is Box 4, modified set & JP snapshot intact; closing dirty inactive Doc A saves without wiping Doc A's state.
3. [Probe 3 — BUG-18] `write_atomic_encoded()` with `newline='\n'` writes raw `b'a\nb'` (zero `\r\n`) on Windows; `on_export_script()` writes LF-only atomically.
4. [Probe 4 — BUG-19] Saving a 0-box metadata-only `StoryDocument` succeeds in Page, Continuous, and Preview modes with zero `IndexError`.
5. [Probe 5 — BUG-20] Saving two same-stem files (`dir1/story.txt` & `dir2/story.txt`) within the same second produces two distinct backup files (zero overwrite).

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_s1_open_file_safety.py`, `test_s2_dirty_contract.py`, `test_s3_document_close.py`, `test_s8b3_encoding_detection.py` all pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT implement `.misora` workspace file I/O (S13) or `on_replace_all` cache/matcher overhaul (S07).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s05_doc_lifecycle_save.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s05_doc_lifecycle_save -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s05_doc_lifecycle_save -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
