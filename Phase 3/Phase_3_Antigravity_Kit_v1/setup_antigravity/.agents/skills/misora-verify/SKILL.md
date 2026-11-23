---
name: misora-verify
description: Runs the canonical Misora-Editor Windows Python 3.12 verification suite (compileall, targeted unittest, full unittest discovery, git status hygiene, and backups/ pollution check). Use after completing any implementation session or before declaring a Walkthrough ready.
---

# Misora Verification SOP (`/misora-verify`)

Execute these verification steps in order on Windows (`D:\Misora-Editor`) and report the EXACT observed output for each step:

1. **Record Environment & Git State (Read-Only):**
   - `git rev-parse --abbrev-ref HEAD`
   - `git rev-parse HEAD`
   - `git status --short`
   - `py -3.12 --version`
2. **Bytecode Compilation Check:**
   - `py -3.12 -m compileall -q misora.py core assets tests` (must exit 0).
3. **Targeted Session Suite:**
   - `py -3.12 -m unittest tests.<session_test_module> -v` (must pass 100%, 0 failures, 0 errors, 0 skips).
4. **Full Regression Suite:**
   - `py -3.12 -m unittest discover -s tests -v` (record exact test count, runtime, failures, errors, skips).
5. **Backup & Config Pollution Audit:**
   - Confirm `git status --short` shows ONLY files within the session's Allowed Files list.
   - Confirm `backups/` gained ZERO new test `.bak_*` files during the test run.
   - Confirm `misora_config.json` was not modified or staged.
