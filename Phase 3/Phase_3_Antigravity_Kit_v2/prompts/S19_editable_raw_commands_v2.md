/plan Implement S19: Whole-File Editable `Raw Commands` (Lossless v2, Confirm, `DocumentRecordsDelta` Undo & Lock/JP Remap) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/story_ast.py @core/undo_journal.py @misora.py @tests/test_p3_s03_binary_v2.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **FEAT-11** (Track 2 · Group G5 (post-DEP-5)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S19` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/undo_journal.py (new `DocumentRecordsDelta` holding before/after deep Record list snapshots)`
  * `core/__init__.py (export `DocumentRecordsDelta`)`
  * `misora.py (`Raw Commands` v2 edit mode toggle + Apply/Revert, `Yes/No` confirmation, structural+binary validation, atomic commit + stable-key lock/JP remap, `_apply_delta` `DocumentRecordsDelta`)`
  * `tests/test_p3_s19_raw_commands_edit.py (NEW)`
  * `CHANGELOG.md (append `### S19` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/story_ast.py (v2 codec already finalized in S03/S04 — do NOT weaken!)`
  * `core/script_codec.py`
  * `core/mtl_engine.py`
5. **Changelog & Version Contract:**
   - Append `### S19` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S19`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Verify `DEP-5` (S03 `BUG-01/03/04` and S04 `BUG-02/05/06`) are green before enabling editing.
2. Bind by symbol name: `txt_raw`, `_update_raw_view`, `_apply_delta` in `misora.py`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FEAT-11)
==================================================
### A. **FEAT-11 (`U-B31` — DEP-5):** Enable whole-file editing in **`Raw Commands`** strictly via lossless v2 text (`doc.to_v2_text()` / `StoryDocument.from_v2_text()`) for sensitive edits like `vo_` voice cues. Keep `txt_raw` read-only outside explicit Edit Raw mode (`BUG-37`). On Apply: (1) Show explicit `Yes/No` confirmation prompt warning that `Raw Commands` will replace workspace records. (2) On `Yes`, parse into a candidate `StoryDocument` and validate structurally (valid numeric command IDs, length-field integrity, `to_binary()` + `from_binary()` round-trip; NO command-specific arity checks `NO-07`; preserve `cmd_id` 35 & 32 unchanged). (3) Commit atomically as ONE `DocumentRecordsDelta` holding before/after deep Record snapshots (NEVER rely on v2 round-trip for Undo!), remap Translation Locks & immutable JP keys via stable composite keys (`CLAUDE-N02`), mark dirty, and refresh all views. (4) On ANY parse/validation failure, abort, revert `txt_raw`, and show a clear error with zero document mutation.

### B. **`CHANGELOG.md`:** Append `### S19` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s19_raw_commands_edit.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s19_raw_commands_edit` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1] Editing a `vo_` cue in `Raw Commands` -> Confirm `Yes` updates AST, refreshes views, preserves locks via stable key remap, and Undo (`DocumentRecordsDelta`) restores exact prior Record list.
2. [Probe 2] Corrupted/unparseable v2 text -> Confirm `Yes` aborts cleanly, reverts `txt_raw`, surfaces error, and leaves `current_doc`, `is_dirty`, and `undo_journal` unchanged.
3. [Probe 3] Clicking `No` leaves document unchanged.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_p3_s03_binary_v2` and `tests.test_p3_s06_doc_state_save` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- NO command-specific arity checks (`NO-07`), NO changes to `cmd_id` 35/32 (`DEF-02`).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s19_raw_commands_edit.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s19_raw_commands_edit -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s19_raw_commands_edit` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s19_raw_commands_edit -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
