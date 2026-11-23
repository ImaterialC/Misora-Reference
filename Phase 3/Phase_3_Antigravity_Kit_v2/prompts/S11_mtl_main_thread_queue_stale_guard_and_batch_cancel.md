/plan Implement S11: Main-Thread Queue-Only Async MTL, Stale-Result Identity Guard & Safe Batch Cancel in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/mtl_engine.py @misora.py @tests/test_s6_threading_decoupling.py @tests/test_phase5_mtl_security_preview.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-14, BUG-27** (Track 1 · Group F1 (DEP-6 — Split from XUAT per Grok R1)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S11` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/mtl_engine.py (`translate_async` Tk-free worker contract)`
  * `misora.py (`on_translate_current_box`, `TranslatorAssistantDialog._on_translate/_on_fetch_all`, `MTLSettingsDialog._on_test_connection`, `BatchTranslateDialog._on_close/_poll_worker_queue`)`
  * `tests/test_p3_s11_mtl_threading.py (NEW)`
  * `CHANGELOG.md (append `### S11` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/xunity_sync.py`
  * `core/story_ast.py`
  * `core/security.py`
  * `core/logger.py`
5. **Changelog & Version Contract:**
   - Append `### S11` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S11`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name: `translate_async` in `core/mtl_engine.py`; `on_translate_current_box`, `MTLSettingsDialog._on_test_connection`, `TranslatorAssistantDialog._on_translate/_on_fetch_all`, `BatchTranslateDialog._on_close/_poll_worker_queue` in `misora.py`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-14, BUG-27)
==================================================
### A. **BUG-27 (`core/mtl_engine.py` + `misora.py` — DEP-6):** Eliminate ALL worker-thread `self.after_idle(...)` calls across all 4 async paths (`on_translate_current_box`, `TranslatorAssistantDialog._on_translate`, `TranslatorAssistantDialog._on_fetch_all`, `MTLSettingsDialog._on_test_connection`). Deliver all results strictly via main-thread-polled `queue.Queue` (`AGENTS.md` §15). Capture `(file_path, doc_id, box_uid, source_hash, req_seq)` on dispatch; re-resolve target by `box_uid` and discard stale results if document, box, or source text changed while in flight.

### B. **BUG-14 (`misora.py:BatchTranslateDialog` — DEP-6):** Track `_batch_open: bool`. On close/cancel while `_is_running`, set `_cancelled = True` ONLY, keep polling until worker emits `('done', ...)`, execute `undo_journal.end_batch()` strictly ONCE on the UI thread, update dirty/view state, and only then destroy the dialog.

### C. **`CHANGELOG.md`:** Append `### S11` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s11_mtl_threading.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s11_mtl_threading` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-27] AST/mock test confirms ZERO `after_idle` calls from background worker threads across all 4 async MTL/connection-test paths; switching active document or inserting a box before an async F8 reply arrives discards the stale result cleanly.
2. [Probe 2 — BUG-14] Closing `BatchTranslateDialog` mid-run sets `_cancelled=True`, waits for `('done', ...)`, and calls `end_batch()` strictly ONCE with zero unbalanced undo batches.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_s6_threading_decoupling` and `tests.test_phase5_mtl_security_preview` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT build the new MTL Right Drawer UI yet (S20/S21).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s11_mtl_threading.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s11_mtl_threading -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s11_mtl_threading` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s11_mtl_threading -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
