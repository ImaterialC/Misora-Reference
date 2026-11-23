---
name: misora-verify
description: Runs the canonical Misora-Editor Windows Python 3.12 verification suite for a specific session test module, full test discovery, git status hygiene, and backups/ pollution check. Invoke as `/misora-verify tests.test_p3_sXX_<name>` (or `/misora-verify --docs-only` for S01).
---

# Misora Verification SOP (`/misora-verify`)

**CRITICAL ARGUMENT RULE:** This skill MUST receive the **real** Python unittest module name for the active session (for example: `/misora-verify tests.test_p3_s03_binary_v2`, or `--docs-only` for S01). If no real module name was supplied, STOP and ask/read the active session prompt — **NEVER run a placeholder string**, and treat `Ran 0 tests` as a hard **FAILURE**.

Execute these steps in order on Windows (`D:\Misora-Editor`) and paste exact observed stdout + exit codes into the Walkthrough Artifact:

1. **Read-Only Workspace & Environment Snapshot:**
   - `git rev-parse --abbrev-ref HEAD`
   - `git rev-parse HEAD`
   - `git status --short`
   - `py -3.12 -c "import sys; print(sys.executable); print(sys.version)"`
2. **Bytecode Compilation Check:**
   - `py -3.12 -m compileall -q misora.py core assets tests` (must exit 0).
3. **Targeted Session Test Module (skip ONLY if `--docs-only` in S01):**
   - `py -3.12 -m unittest <REAL_MODULE_NAME> -v`
   - Confirm `Ran N tests` with `N > 0`, 0 failures, 0 errors, 0 skips (unless a fixture-gated item is explicitly marked `BLOCKED` per the session prompt).
4. **Full Regression Discovery:**
   - `py -3.12 -m unittest discover -s tests -v`
   - Record exact total test count, duration, failures, errors, skips (`Ran 0 tests` = FAIL).
5. **Hygiene & Pollution Audit:**
   - Verify `git status --short` lists ONLY files inside the current session's Allowed Files (plus `CHANGELOG.md` and `PROJECT_STATE.md`).
   - Verify repo root `backups/` gained ZERO new `.bak_*` files during testing.
   - Verify untracked `misora_config.json` was not modified or staged.
