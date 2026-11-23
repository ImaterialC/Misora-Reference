/plan Implement S09: Multi-File Replace-All Cache Keys/Shared Matcher/Closed-File Undo & Collision-Resistant Backups in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @misora.py @core/search_engine.py @tests/test_s5_bulk_replace_safety.py @tests/test_s9b_replace_all_bundle_safety.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-24, BUG-20** (Track 1 · Group D2).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S09` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (`on_replace_next`, `on_replace_all`, `_apply_delta` `BulkFileDelta`, shared collision-resistant backup path helper used by `on_save` and `on_replace_all`)`
  * `tests/test_p3_s09_replace_all_backups.py (NEW)`
  * `CHANGELOG.md (append `### S09` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/search_engine.py`
  * `core/xunity_sync.py`
  * `core/mtl_engine.py`
5. **Changelog & Version Contract:**
   - Append `### S09` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S09`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name in `misora.py`: `on_replace_next`, `on_replace_all`, `_apply_delta` (`BulkFileDelta` branch), and `on_save` backup creation lines.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-24, BUG-20)
==================================================
### A. **BUG-24 (`misora.py`):** (1) Fix `_apply_delta(BulkFileDelta)` and its rollback block to use canonical `open_documents` keys `'env'` and `'obj'` (NEVER `'bundle_env'`/`'target_object'`) and dispose old `env` properly. (2) Refresh/invalidate ALL affected open document caches (not only `current_file_path`); refuse/prompt before overwriting dirty open documents from disk; do NOT mark disk-saved files dirty; resolve & deduplicate candidate paths. (3) Share ONE compiled matcher (honoring `Match Case`, `Regex`, `Ignore Whitespace`, preserving `break_char` per `QW-R06`) and Translation Lock policy across Find, `on_replace_next()` (skip locked boxes in advance loop!), and `on_replace_all()` (current-file already checks locks; enforce in multi-file too). (4) Multi-file `BulkFileDelta` Undo/Redo must NEVER silently reopen closed tabs (`AGENTS.md` §16) — display an explicit confirmation listing all affected paths (including currently closed disk files) before touching disk.

### B. **BUG-20 (`misora.py` — `QW-B17` + `Grok-N03`):** Create ONE collision-resistant backup path helper using microsecond timestamp (`%Y%m%d_%H%M%S_%f`) + short deterministic SHA-256 prefix of the normalized full source path (and disambiguating if the target backup path already exists), and use it across BOTH normal `on_save()` AND `on_replace_all()` (text & bundle).

### C. **`CHANGELOG.md`:** Append `### S09` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s09_replace_all_backups.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s09_replace_all_backups` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-24] Multi-file Replace-All + Undo refreshes inactive open bundle cache via `'env'`/`'obj'`, disposes old `env` (`weakref`), respects Regex/Match Case/Locks, skips locked boxes in `on_replace_next()` advance loop, and prompts before touching closed disk paths on Undo.
2. [Probe 2 — BUG-20] Two same-stem files (`dir1/story.txt` & `dir2/story.txt`) saved or bulk-replaced within the same second produce two distinct backup files (zero overwrite).

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_s5_bulk_replace_safety` and `tests.test_s9b_replace_all_bundle_safety` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT build Replace-All dry-run diff pane (`DEF-09`) or background bulk-replace worker (`DEF-07`).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s09_replace_all_backups.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s09_replace_all_backups -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s09_replace_all_backups` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s09_replace_all_backups -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
