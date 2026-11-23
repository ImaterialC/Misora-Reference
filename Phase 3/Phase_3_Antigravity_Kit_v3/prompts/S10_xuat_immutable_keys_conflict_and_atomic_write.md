/plan Implement S10: Immutable `box.uid` XUAT JP Keys, Save Conflict Preview Gate & Atomic XUAT Dictionary Writes in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/xunity_sync.py @core/text_encoding.py @misora.py @tests/test_misora_core.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-25, BUG-26** (Track 1 · Group E (DEP-7 part 2 — Split from MTL per Grok R1)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S10` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/xunity_sync.py (`find_and_update` atomic write via `write_atomic_encoded`, `jp_source_cache` helpers)`
  * `misora.py (`open_file` JP key registration, `on_save` XUAT sync + conflict preview gate)`
  * `tests/test_p3_s10_xuat_integrity.py (NEW)`
  * `CHANGELOG.md (append `### S10` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/mtl_engine.py`
  * `core/story_ast.py`
  * `core/search_engine.py`
  * `misora.py (MTL handlers — owned by S11)`
5. **Changelog & Version Contract:**
   - Append `### S10` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S10`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name: `jp_source_cache`, `register_jp_key`, `get_jp_key`, `preview_matches`, `find_and_update` in `core/xunity_sync.py`; `on_save` XUAT sync block and `open_file` JP snapshot in `misora.py`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-25, BUG-26)
==================================================
### A. **BUG-25 (`misora.py` + `core/xunity_sync.py` — DEP-7):** Register immutable Japanese source keys by `box.uid` (backed by S06's per-doc `original_jp_by_uid` and `XUnitySyncManager.register_jp_key()`/`get_jp_key()`); NEVER overwrite JP keys with saved English text after save and NEVER fall back to current edited text. Before calling `find_and_update()` in `on_save()`, run `preview_matches()` and prompt user ONLY when genuine `is_conflict=True` duplicate translations exist.

### B. **BUG-26 (`core/xunity_sync.py:find_and_update()`):** Replace non-unique `f'{tf.name}.{os.getpid()}.tmp'` + bare `os.replace` with `core.text_encoding.write_atomic_encoded()` (unique temp name + bounded Windows retry, preserving BOM/encoding/CRLF/LF).

### C. **`CHANGELOG.md`:** Append `### S10` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s10_xuat_integrity.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s10_xuat_integrity` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-25] Save box twice (`EN1 -> EN2`): 2nd save still matches original JP key (never `EN1`); inserting a box before it does not shift JP key; conflicting XUAT entries trigger conflict confirmation prompt while clean non-conflicting matches sync without extra modal friction.
2. [Probe 2 — BUG-26] `find_and_update()` delegates to `write_atomic_encoded()` preserving UTF-8 BOM and CRLF/LF.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_misora_core` and `tests.test_p3_s06_doc_state_save` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT modify async MTL / BatchTranslateDialog (S11) or create `core/xuat_index.py` (S22).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s10_xuat_integrity.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s10_xuat_integrity -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s10_xuat_integrity` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s10_xuat_integrity -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
