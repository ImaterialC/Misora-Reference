/plan Implement S12: Logger Flush Barrier/Teardown, DPAPI Fail-Closed, Reload Env Disposal, Deferred Startup & Splash Safety in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/security.py @core/logger.py @assets/splash.py @misora.py @tests/test_phase3_performance_config.py @tests/test_s8b2_memory_guards.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-32, BUG-33, BUG-34, BUG-35, BUG-36** (Track 1 · Group F2 (DEP-9 part 1 — Split from Ribbon per Grok R2)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S12` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/security.py (`protect_secret`, `unprotect_secret`)`
  * `core/mtl_engine.py (ONLY `MTLConfig.to_dict` secure failure propagation)`
  * `core/logger.py (`MisoraLogger.flush`, `clear_log_file`)`
  * `assets/splash.py (`SPLASH_IMAGES` sorting)`
  * `misora.py (ONLY `MisoraApp.__init__` deferred restore, `open_file` reload `env` disposal, `_save_user_prefs` DPAPI warning, `destroy`/`_on_app_exit` `logger.close()` + `after info` sweep)`
  * `tests/test_p3_s12_lifecycle_security.py (NEW)`
  * `CHANGELOG.md (append `### S12` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/script_codec.py`
  * `core/search_engine.py`
  * `misora.py (ribbon, shortcuts, tooltips — owned by S13)`
5. **Changelog & Version Contract:**
   - Append `### S12` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S12`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name: `protect_secret`/`unprotect_secret` in `core/security.py`; `MisoraLogger.flush`/`close`/`clear_log_file` in `core/logger.py`; `SPLASH_IMAGES` in `assets/splash.py`; `__init__` session restore, `open_file` reload, `_save_user_prefs`, `destroy`/`_on_app_exit` in `misora.py`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-32, BUG-33, BUG-34, BUG-35, BUG-36)
==================================================
### A. **BUG-32 (`core/logger.py` + `misora.py`):** Note canonical class name is `MisoraLogger`. Replace `queue.empty()` polling in `flush()` with a true completion barrier (`task_done()`/`join()` or completion `threading.Event` with bounded timeout) so `clear_log_file()` never races an in-flight write. In `misora.py:destroy()` and `_on_app_exit()`, call `self.logger.close()` and sweep pending Tk `after` jobs via `self.tk.call('after', 'info')`.

### B. **BUG-33 (`core/security.py` + `core/mtl_engine.py` + `misora.py` — P1):** Fail closed on Windows DPAPI encryption failure: raise an explicit security error instead of silently returning plaintext to `misora_config.json`, and surface a clear UI warning in `_save_user_prefs()` (while retaining read compatibility for legacy plaintext configs). On DPAPI decryption failure in `unprotect_secret()`, warn explicitly and preserve the stored encrypted value instead of silently returning `''` and wiping the key.

### C. **BUG-34 (`misora.py:open_file()`):** During `reload_from_disk=True`, dispose prior `open_documents[file_path]['env']` via `dispose_unity_env()` BEFORE overwriting the cache entry.

### D. **BUG-35 (`misora.py:MisoraApp.__init__()` — DEP-9):** Defer `initial_path` and `_saved_opened_files` restoration via `self.after_idle(...)` AFTER `self.deiconify()` (`AGENTS.md` §22).

### E. **BUG-36 (`assets/splash.py`):** Guard `SPLASH_IMAGES` sorting against non-numeric `Splash_*.jpg` filenames so unexpected filenames never crash import/startup.

### F. **`CHANGELOG.md`:** Append `### S12` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s12_lifecycle_security.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s12_lifecycle_security` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-32] Slow disk write in `MisoraLogger` completes before `flush()` returns and before `clear_log_file()` truncates (0 stale lines); `app.destroy()` calls `logger.close()` and cancels scheduled `after` jobs.
2. [Probe 2 — BUG-33] Mocked DPAPI `CryptProtectData` failure raises and refuses silent plaintext write to `misora_config.json`; mocked `CryptUnprotectData` failure warns and preserves encrypted blob.
3. [Probe 3 — BUG-34] `weakref.ref(old_env)` is collected after `open_file(path, reload_from_disk=True)`.
4. [Probe 4 — BUG-35] During `MisoraApp.__init__`, `deiconify()` occurs BEFORE deferred session files load via `after_idle`.
5. [Probe 5 — BUG-36] Sorting handles `['Splash_10.jpg', 'Splash_2.jpg', 'Splash_custom.jpg']` without `ValueError`.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_phase3_performance_config`, `tests.test_phase5_mtl_security_preview`, and `tests.test_s8b2_memory_guards` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT touch ribbon/shortcuts/tooltips (S13).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s12_lifecycle_security.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s12_lifecycle_security -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s12_lifecycle_security` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s12_lifecycle_security -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
