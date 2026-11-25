---
name: misora-verify
description: Verifies Misora: Story Editor code health on Windows Python 3.12 (compileall including root __init__.py, targeted real session test module, full unittest discovery, version-source parity without hardcoded duplicates, and diff against pre-session git status). Invoke as `/misora-verify tests.test_v15_sXX_<name>`.
---

# Misora Verification Skill (`/misora-verify`)

**CRITICAL ARGUMENT RULE:** You MUST pass the **real** Python unittest module name for the active session (e.g., `/misora-verify tests.test_v15_s01_stability_remediation`). NEVER run a placeholder string. `Ran 0 tests` is ALWAYS a hard **FAILURE**.

Run these exact checks on Windows (`D:\Misora-Editor`) and record actual observed stdout + exit codes in the Walkthrough artifact:

1. **Pre-Session Baseline Snapshot (Record BEFORE Editing):**
   ```powershell
   git branch --show-current
   git rev-parse HEAD
   git status --short
   py -3.12 -c "import sys; print(sys.executable); print(sys.version)"
   ```
   Preserve all pre-existing user modifications and untracked local files — NEVER reset, clean, stash, or overwrite them.

2. **Bytecode Compilation Gate (Explicitly Including Root `__init__.py`):**
   ```powershell
   py -3.12 -m compileall -q __init__.py misora.py core assets tests
   ```
   Must exit `0` with zero syntax/compile errors.

3. **Targeted Session Test Module (Categorized Verification):**
   ```powershell
   py -3.12 -m unittest <real_session_test_module> -v
   ```
   Verify and report honestly by test category:
   - **Failing-First Defect Probes (S01–S07):** MUST fail BEFORE patching (quote pre-patch failure output) and PASS afterward. If a Defect Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` — NEVER invent a fake failure.
   - **Regression Guards:** MUST pass both BEFORE and AFTER patching.
   - **Acceptance / Stress Tests (S08):** Evaluated on their post-implementation acceptance/plateau criteria (not forced to fail beforehand).
   - **Proprietary Fixture-Gated Tests:** Missing `storydata_1001005.unity3d` stays `BLOCKED`, NEVER `PASS` or weakened/skipped to fake green.

4. **Full Project Regression Discovery:**
   ```powershell
   py -3.12 -m unittest discover -s tests -v
   ```
   Report exact observed totals (`Ran N tests`, passed, skipped, failures, errors), distinguishing any known fixture-blocked `storydata_1001005.unity3d` items from new regressions.

5. **Single-Source Version Parity & Pre-Session Diff Hygiene:**
   - Verify root `__init__.__version__` is the sole authoritative version literal and that `misora.py`, `assets/splash.py`, and `core/mtl_engine.py` derive/import from it (do NOT add hardcoded version duplicates).
   - Run `git status --short` and compare against the **Step 1 pre-session snapshot**: confirm this session introduced NO unauthorized file edits outside its Allowed Files, preserved all pre-existing local work, wrote ZERO files into repo `backups/`, kept `misora_config.json` untouched, and staged/added ZERO proprietary font binaries.
