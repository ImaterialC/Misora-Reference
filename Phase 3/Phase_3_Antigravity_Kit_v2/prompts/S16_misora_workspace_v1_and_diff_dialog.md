/plan Implement S16: `.misora` v1 Workspace Session (References + State + Stable-Key Locks Only) & Overwrite Diff Dialog in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @misora.py @core/text_encoding.py @tests/test_p3_s06_doc_state_save.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **FEAT-08** (Track 2 · Group G3 (post-DEP-4, DEP-9)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S16` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/workspace.py (NEW pure-Python `.misora` v1 JSON schema, atomic save/load, relative+absolute path resolver, composite lock-key matcher)`
  * `core/__init__.py (export workspace helpers)`
  * `misora.py (File menu Save Project / Open Project `.misora`, DnD `.misora` support, `ProjectDiffDialog` for `U-B18`)`
  * `tests/test_p3_s16_misora_workspace.py (NEW)`
  * `CHANGELOG.md (append `### S16` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/bundle_io.py`
  * `core/script_codec.py`
5. **Changelog & Version Contract:**
   - Append `### S16` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S16`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Inspect S06's per-document state & stable lock-key helpers in `misora.py`.
2. Inspect File menu (`_build_menu`) and `_handle_dropped_paths` in `misora.py`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FEAT-08)
==================================================
### A. **FEAT-08 (`U-B17`, `U-B18` — Lead Ruling #3 & GPT Safety Rule):** Create `core/workspace.py` implementing `.misora` v1 atomic JSON workspace files (`write_atomic_encoded`) storing **STRICTLY references + state + stable-key locks ONLY** (NEVER unsaved story drafts, NEVER `.unity3d` binary blobs, NEVER runtime `Record.uid` — `NO-01`/`NO-12`): `schema_version: 1`, `files: [{rel_path, abs_path, locked_keys: [{box_ordinal, jp_sha256}]}]`, `active_file`, `active_box_idx`, `is_box0_active`, `view_mode`, `search_scope`.

### B. On open `.misora`: (1) If current session has open files (especially dirty files), display **`U-B18` Project Difference Mapping dialog** showing compact old-vs-new file table (Added / Removed / Kept / Dirty markers) + explicit overwrite warning + `Save Current` / `Discard & Open` / `Cancel` (`AGENTS.md` §16). (2) Restore files via staged batched open; report missing files cleanly without crashing. (3) Re-attach Translation Locks ONLY when `(box_ordinal, sha256(original_jp_text))` matches confidently; if any persisted lock cannot be matched, **leave it unresolved and notify the user** (NEVER silently transfer a lock to another box — `NO-12`).

### C. **`CHANGELOG.md`:** Append `### S16` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s16_misora_workspace.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s16_misora_workspace` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1] Saved `.misora` JSON contains `schema_version == 1`, relative+absolute paths, view/scope state, and `(box_ordinal, jp_sha256)` lock keys — with ZERO `Record.uid`, ZERO story text drafts, and ZERO binary blobs.
2. [Probe 2] Reopening `.misora` restores open tabs, active box, and matched locks; when a box's JP text changed on disk, the unmatched lock stays unresolved (NOT transferred) and notifies the user.
3. [Probe 3 — U-B18] Opening another `.misora` while dirty files exist computes exact added/removed/dirty diff and aborts cleanly on Cancel.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_p3_s06_doc_state_save` and `tests.test_p3_s15_selection_drawer_open` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- NO draft snapshots or binary blobs in `.misora` (`NO-01`).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s16_misora_workspace.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s16_misora_workspace -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s16_misora_workspace` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s16_misora_workspace -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
