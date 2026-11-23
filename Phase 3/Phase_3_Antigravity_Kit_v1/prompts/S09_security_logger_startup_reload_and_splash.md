<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S09
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (or /swarm with exclusive file workers + cross-model @verifier)
- Model & Effort : Gemini 3.8 Flash (workers on isolated files) + Claude Sonnet 4.6 (@verifier) — SAFE for cheap workers!
- Cheap-Model OK : YES (cleanly isolated small modules — ideal /swarm: Flash workers + Sonnet @verifier)
- Ledger Coverage: BUG-32, BUG-33, BUG-34, BUG-35, BUG-36 (Group F2 (DEP-9 part 1))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S09: DPAPI Fail-Closed, Logger Flush Barrier, Reload Env Disposal, Deferred Startup & Splash Safety in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/security.py @core/logger.py @assets/splash.py @misora.py @tests/test_phase3_performance_config.py @tests/test_s8b2_memory_guards.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S09`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/security.py (protect_secret, unprotect_secret)`
  * `core/mtl_engine.py (ONLY MTLConfig.to_dict secure failure propagation)`
  * `core/logger.py (MisoraLogger.flush, clear_log_file)`
  * `assets/splash.py (SPLASH_IMAGES sorting)`
  * `misora.py (ONLY MisoraApp.__init__ deferred restore, open_file reload_from_disk env disposal, _save_user_prefs DPAPI error handling, destroy/_on_app_exit logger.close + after info sweep)`
  * `tests/test_p3_s09_lifecycle_security.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/script_codec.py`
  * `core/search_engine.py`
  * `core/xunity_sync.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S09`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `core/security.py` (`protect_secret` 28-61, `unprotect_secret` 64-99).
2. Inspect `core/logger.py` (`MisoraLogger.flush` 97-101, `close` 103, `clear_log_file` 250-260).
3. Inspect `assets/splash.py` (`SPLASH_IMAGES` 41-43).
4. Inspect `misora.py`: `__init__` session restore (1376-1390), `destroy`/`_on_app_exit` (1493-1546), `open_file` reload cache write (6650).
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-32, BUG-33, BUG-34, BUG-35, BUG-36)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-32, BUG-33, BUG-34, BUG-35, BUG-36**

### A. **BUG-32 (`core/logger.py` + `misora.py`):** In `MisoraLogger.flush()`, replace `queue.empty()` polling with a true completion barrier (`task_done()` / `join()` or completion `threading.Event` with bounded timeout) so `clear_log_file()` never races an in-flight disk write. In `misora.py:destroy()` and `_on_app_exit()`, call `self.logger.close()` and sweep dangling Tk `after` jobs via `self.tk.call('after', 'info')`.

### B. **BUG-33 (`core/security.py` + `core/mtl_engine.py` + `misora.py` — P1):** Fail closed on Windows DPAPI encryption failure: raise an explicit `SecurityError`/`RuntimeError` instead of silently returning plaintext to `misora_config.json`, and surface a clear UI warning in `_save_user_prefs()` (while preserving read compatibility for legacy plaintext configs). On DPAPI decryption failure in `unprotect_secret()`, warn explicitly and preserve the encrypted blob instead of silently returning `''` and wiping the stored key on next save.

### C. **BUG-34 (`misora.py:open_file()`):** During `reload_from_disk=True`, dispose the previous `open_documents[file_path]['env']` via `dispose_unity_env()` BEFORE overwriting the cache entry.

### D. **BUG-35 (`misora.py:MisoraApp.__init__()` — DEP-9):** Defer `initial_path` and `_saved_opened_files` session restoration via `self.after_idle(...)` AFTER `self.deiconify()` (`AGENTS.md` §22) so the main window displays immediately without startup freeze.

### E. **BUG-36 (`assets/splash.py`):** Guard `SPLASH_IMAGES` sorting against non-numeric `Splash_*.jpg` filenames (e.g., regex numeric key with lexical fallback) so unexpected filenames never raise `ValueError` at import time.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s09_lifecycle_security.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-32] Simulated slow disk write in `MisoraLogger` finishes before `flush()` returns and before `clear_log_file()` truncates (0 stale trailing lines); `app.destroy()` calls `logger.close()` and cancels scheduled `after` jobs.
2. [Probe 2 — BUG-33] Mocked DPAPI `CryptProtectData` failure raises and refuses to write plaintext API key to `misora_config.json`; mocked `CryptUnprotectData` failure warns and does not silently wipe the encrypted value.
3. [Probe 3 — BUG-34] `weakref.ref(old_env)` is garbage-collected after `open_file(path, reload_from_disk=True)`.
4. [Probe 4 — BUG-35] During `MisoraApp.__init__`, `deiconify()` occurs BEFORE session files are loaded via `after_idle`.
5. [Probe 5 — BUG-36] Sorting helper handles `['Splash_10.jpg', 'Splash_2.jpg', 'Splash_custom.jpg']` cleanly without `ValueError`.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_phase3_performance_config.py`, `test_phase5_mtl_security_preview.py`, and `test_s8b2_memory_guards.py` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT touch `core/story_ast.py` or UI layout.
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s09_lifecycle_security.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s09_lifecycle_security -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s09_lifecycle_security -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
