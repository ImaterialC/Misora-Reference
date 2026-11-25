---
name: misora-verify
description: Verifies Misora: Story Editor code health, Windows Python 3.12 compilation, targeted failing-first unit tests, full regression suite, version parity, and clean workspace hygiene after any code edit.
---

# Misora Verification Skill

Run these exact checks on Windows (`D:\Misora-Editor`) before producing a Walkthrough artifact:

1. **Workspace & Python Preflight:**
   ```powershell
   git branch --show-current
   git rev-parse HEAD
   git status --short
   py -3.12 -c "import sys; print(sys.executable); print(sys.version)"
   ```
2. **Bytecode Compilation Gate:**
   ```powershell
   py -3.12 -m compileall -q misora.py core assets tests
   ```
   Must exit `0` with zero syntax/compile errors.
3. **Targeted Session Test Module:**
   ```powershell
   py -3.12 -m unittest tests.<session_test_module> -v
   ```
   Verify all Defect/Behavior Probes failed BEFORE patching (recorded in Walkthrough) and pass AFTER patching, and all Regression Guards passed both before and after.
4. **Full Project Test Suite:**
   ```powershell
   py -3.12 -m unittest discover -s tests -v
   ```
   Report exact observed counts (`Ran N tests`, passes, skips, failures, errors) and note any known fixture-gated `storydata_1001005.unity3d` skips/failures honestly without weakening or skipping tests.
5. **Version & Hygiene Check:**
   - Verify root `__init__.__version__` matches `misora.__version__`, `assets/splash.py`, `core/mtl_engine.py`, and `CHANGELOG.md`.
   - Verify `git status --short` lists ONLY the current session's Allowed Files (no leaked files in `backups/`, no modified untracked `misora_config.json`, no proprietary font files staged/added).
