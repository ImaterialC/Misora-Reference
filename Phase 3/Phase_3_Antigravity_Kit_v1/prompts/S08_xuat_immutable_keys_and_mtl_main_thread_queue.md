<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S08
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> Proceed
- Model & Effort : Claude Sonnet 4.6 (Thread safety & XUAT sync integrity)
- Cheap-Model OK : NO — Recommended Claude Sonnet 4.6
- Ledger Coverage: BUG-14, BUG-25, BUG-26, BUG-27, HYG-06 (Group E + F1 (DEP-6, DEP-7))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S08: Immutable XUAT JP Keys, Conflict Gate, Atomic XUAT Writes & Main-Thread Async MTL Queue in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/xunity_sync.py @core/mtl_engine.py @misora.py @tests/test_s6_threading_decoupling.py @tests/test_phase5_mtl_security_preview.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S08`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/xunity_sync.py (find_and_update atomic write via write_atomic_encoded, jp_source_cache usage)`
  * `core/mtl_engine.py (translate_async Tk-free worker contract, shared version constant for DeepL UA)`
  * `misora.py (on_save XUAT sync + conflict gate, open_file JP key registration, on_translate_current_box queue + stale guard, TranslatorAssistantDialog queue, MTLSettingsDialog._on_test_connection queue, BatchTranslateDialog._on_close/_poll_worker_queue)`
  * `tests/test_p3_s08_xuat_mtl_threading.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/security.py`
  * `core/logger.py`
  * `misora.py (toolbar, preview, search — owned by other sessions)`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S08`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `core/xunity_sync.py` (`jp_source_cache`, `preview_matches`, `find_and_update` lines 222-230).
2. Inspect `core/mtl_engine.py` (`_translate_deepl` line 212, `_test_deepl_usage` line 309, `translate_async` 337-355).
3. Inspect `misora.py`: `on_save` XUAT block (8568-8595), `on_translate_current_box` (10501-10561), `MTLSettingsDialog._on_test_connection` (11395-11411), `TranslatorAssistantDialog._on_translate/_on_fetch_all` (11750-11835), `BatchTranslateDialog._on_close/_poll_worker_queue` (11958-12118).
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-14, BUG-25, BUG-26, BUG-27, HYG-06)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-14, BUG-25, BUG-26, BUG-27, HYG-06**

### A. **BUG-25 (`misora.py` + `core/xunity_sync.py` — DEP-7):** Register immutable Japanese source keys by `box.uid` (wired to per-doc `original_jp_by_uid` from S05 and `XUnitySyncManager.register_jp_key()`/`get_jp_key()`); NEVER overwrite JP keys with saved English text after save and NEVER fall back to current edited text. Before `find_and_update()` in `on_save()`, run `preview_matches()` and prompt user ONLY when genuine `is_conflict=True` duplicates exist.

### B. **BUG-26 (`core/xunity_sync.py:find_and_update()`):** Delegate atomic dictionary writes to `core.text_encoding.write_atomic_encoded()` (unique temp filename + bounded Windows retry, preserving BOM/encoding/newlines).

### C. **BUG-27 (`core/mtl_engine.py` + `misora.py` — DEP-6):** Eliminate ALL worker-thread `self.after_idle(...)` calls across all 4 async paths (`on_translate_current_box`, `TranslatorAssistantDialog._on_translate`, `TranslatorAssistantDialog._on_fetch_all`, `MTLSettingsDialog._on_test_connection`). Deliver all results strictly via main-thread-polled `queue.Queue` (`AGENTS.md` §15). Capture `(file_path, doc_id, box_uid, source_hash, req_seq)` on dispatch; re-resolve target by `box_uid` and discard stale results if document, box, or source text changed while in flight.

### D. **BUG-14 (`misora.py:BatchTranslateDialog` — DEP-6):** Track `_batch_open: bool`. On close/cancel while `_is_running`, set `_cancelled = True` ONLY, keep polling until worker emits `('done', ...)`, execute `undo_journal.end_batch()` strictly ONCE on the UI thread, update dirty/view state, and only then destroy the dialog.

### E. **HYG-06 (`core/mtl_engine.py`):** Replace hardcoded `Misora-Story-Editor/1.3` User-Agent (lines 212 & 309) with a single shared version constant (e.g., reading root `__version__` cleanly without circularly importing `misora.py`).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s08_xuat_mtl_threading.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-25] Save box twice (EN1 -> EN2): 2nd save still queries original JP key (never EN1); inserting a box before it does not shift JP key; conflicting XUAT lines trigger conflict confirmation gate while non-conflicting matches sync smoothly.
2. [Probe 2 — BUG-26] `find_and_update()` uses `write_atomic_encoded()` preserving UTF-8 BOM & CRLF.
3. [Probe 3 — BUG-27] AST/mock test confirms ZERO `after_idle` calls from worker threads across all 4 async MTL/connection-test paths; switching active document or inserting a box before async F8 reply arrives discards the stale translation cleanly.
4. [Probe 4 — BUG-14] Closing `BatchTranslateDialog` mid-run sets `_cancelled=True` and calls `end_batch()` strictly ONCE upon `('done', ...)` with zero unbalanced batches.
5. [Probe 5 — HYG-06] DeepL request User-Agent matches root `__version__` (`1.4.0`), never hardcoded `1.3`.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_s6_threading_decoupling.py` and `tests/test_phase5_mtl_security_preview.py` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT build the new MTL Right Drawer UI (S16) or `core/xuat_index.py` / Import from XUAT UI (S17).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s08_xuat_mtl_threading.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s08_xuat_mtl_threading -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s08_xuat_mtl_threading -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
