<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S01
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (then /goal after Proceed)
- Model & Effort : Gemini 3.8 Flash (Plan + Execute) — SAFE for cheap model (zero production code edits)
- Cheap-Model OK : YES (Gemini 3.8 Flash / GPT-OSS 120B safe)
- Ledger Coverage: HYG-01, HYG-02 (Group A (DEP-10))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S01: Docs/Ledger Reconciliation, AGENTS.md Update & Test Backup Isolation in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @README.md @tests/

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S01`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `PROJECT_STATE.md`
  * `README.md`
  * `AGENTS.md`
  * `tests/*.py (only adding temp-dir isolation for app.backup_folder in setUp/tearDown)`
   - DO NOT modify:
  * `misora.py`
  * `core/*.py`
  * `assets/*.py`
  * `misora_config.json`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S01`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Confirm current local Git branch, exact HEAD (`683724edaf2afac89d2695a80e30a471a0da9195`), `git status --short`, and active `py -3.12` version.
2. Audit `PROJECT_STATE.md` §2/§4/§7/§9, `README.md`, and `AGENTS.md` §19/§24/§29 against live HEAD.
3. Grep `tests/*.py` for `MisoraApp(` and `on_save` / `backup_folder` to list every test file that can write into repo `backups/`.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (HYG-01, HYG-02)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **HYG-01, HYG-02**

### A. **HYG-01 (`PROJECT_STATE.md`, `README.md`, `AGENTS.md`):** Reconcile all stale docs against pinned HEAD `683724e`: downgrade contradicted `RESOLVED` ledger claims (`CMD0-SPECIAL-CASE`, `FIND-REPLACE-UI-ASYMMETRY`, `CONTINUOUS-RIBBON-TARGET-STALE`, `SIZE-RIBBON-NO-COMMIT`, `TRANSLATION-LOCK`, `CTRL-ALT-HOTKEYS-BLOCKED`, `BOX0-NO-SELECT-CHECKBOX`, `V2-ROUNDTRIP-LOSS`, `GAME-BOX-PREVIEW`, `MULTI-TEXTASSET-TARGET`); fix §2 per-suite test-count arithmetic (`238` vs `234`) and mismatched test filenames; record intentional local deletion + `.gitignore` of `docs/` and `storydata_1001005.unity3d`; update `AGENTS.md` §19/`D13` (calibrated pixel overflow `50x3` estimate), §24 (remove already-shipped CSIF; tie MTL Drawer gate to Phase 2.5 P0/P1 stabilization closure `S01..S10`), and §29 (mark `Ctrl+H` verified fixed on Windows v1.4.0). Do NOT fabricate unrun test counts.

### B. **HYG-02 (`tests/*.py`):** Ensure every test class instantiating `MisoraApp` or invoking `on_save()`/`on_replace_all()` redirects `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp()` and cleans up in `tearDown()` (alongside existing `misora.CONFIG_PATH` isolation) so `unittest discover` writes ZERO files into `D:\Misora-Editor\backups\`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s01_hygiene_backup_isolation.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1] Snapshot `backups/` directory file list before running `tests.test_s2_dirty_contract` and `tests.test_s3_document_close`; assert zero new `.bak_*` files are created inside repo root `backups/`.
2. [Probe 2] Assert `AGENTS.md` §24 does not list CSIF as unshipped and ties MTL Drawer to stabilization closure; assert `PROJECT_STATE.md` records pinned baseline `683724edaf2afac89d2695a80e30a471a0da9195`.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] Full existing `py -3.12 -m unittest discover -s tests -v` passes with 0 failures, 0 errors, 0 skips.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- NO edits to `misora.py`, `core/*.py`, or `assets/*.py`. All production bug fixes begin in S02.
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s01_hygiene_backup_isolation.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s01_hygiene_backup_isolation -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s01_hygiene_backup_isolation -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
