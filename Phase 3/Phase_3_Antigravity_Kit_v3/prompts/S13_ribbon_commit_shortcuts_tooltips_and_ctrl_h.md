/plan Implement S13: Continuous Ribbon/Size/Dirty Sync, Shortcut Conflicts, Complete Tooltips & `Ctrl+H` Hygiene (TRACK 1 FINAL GATE) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @misora.py @tests/test_s4_view_model_sync.py @tests/test_s8b4_ui_polishing.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-28, BUG-29, HYG-03, HYG-07** (Track 1 · Group F3 (DEP-3 — Completes all non-fixture Track 1 P0/P1 bugs; real production `.unity3d` verification for `BUG-09` stays explicitly `BLOCKED` if no local production fixture exists)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S13` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (`_insert_text_wrapper`, `apply_ngui_wrapper`, `on_insert_ruby`, `on_insert_font_size`, `_on_misora_shortcut`, `_bind_shortcuts`, missing ribbon tooltips + Unicode fallbacks)`
  * `tests/test_p3_s13_ribbon_shortcuts.py (NEW)`
  * `CHANGELOG.md (append `### S13` under `## [Unreleased]` + Track 1 Complete milestone note)`
  * `PROJECT_STATE.md (mark Track 1 automated stabilization gate COMPLETE while explicitly recording `BUG-09` production-fixture status as `PASS` or `BLOCKED`)`
   - DO NOT modify:
  * `core/*.py`
  * `assets/*.py`
  * `misora.py (dead-code removal `HYG-08` is strictly in S23!)`
5. **Changelog & Version Contract:**
   - Append `### S13` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S13`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name in `misora.py`: `_insert_text_wrapper`, `apply_ngui_wrapper`, `on_insert_ruby`, `on_insert_font_size`, `_on_misora_shortcut`, `_bind_shortcuts`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-28, BUG-29, HYG-03, HYG-07)
==================================================
### A. **BUG-28 (`misora.py` — DEP-3):** Resolve active card editor via `_get_card_text_widget(self.current_box_idx)` inside `_insert_text_wrapper()` and `on_insert_ruby()` (never target hidden `txt_continuous` for bundles). Remove redundant `_on_dialogue_edited()` inside `_insert_text_wrapper()` so `apply_ngui_wrapper()`'s `_commit_widget_edit()` commits ONCE and triggers `_dirty_state_changed()` (fixing stale `*` title & Undo menu in Page View). Call `_commit_widget_edit(target)` in `on_insert_font_size()`.

### B. **BUG-29 + HYG-07 (`misora.py`):** Reconcile one canonical shortcut table across `_on_misora_shortcut()`, `_bind_shortcuts()`, menus, and tooltips: fix `Ctrl+T` conflict (editor vs root), fix `<Control-C>` vs `<Control-Shift-C>` collision, add missing `Ctrl+R` (Ruby) in `MisoraShortcuts` bindtag router, allow safe `Ctrl+Alt` app accelerators (`X/C/V/A`) without breaking AltGr, and ensure `bind_all('<Control-h>', ...)` returns `'break'` (`HYG-07`).

### C. **HYG-03 (`misora.py` — DEP-3):** Attach single-timer `ToolTip` (350ms) and Unicode fallback text to every ribbon/toolbar control currently lacking them (`Ruby`, `Player`, `B/I/U/S/Sub/Sup`, `Preview`, `All Script`, `Select Box`, etc.) per `AGENTS.md` §21.

### D. **`CHANGELOG.md`:** Append `### S13` under `## [Unreleased] (Target: v1.4.1)` noting **Track 1 Automated Stabilization Gate (S01..S13) COMPLETE** (unlocks Track 2 `S14..S23` and `AGENTS.md` §24 MTL Drawer gate), AND explicitly stating whether `BUG-09` real production `.unity3d` verification is `PASS` or remains `BLOCKED` (synthetic check passed; production fixture pending).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s13_ribbon_shortcuts.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s13_ribbon_shortcuts` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-28] Bold/Ruby/Size wrappers in Continuous View mutate active card widget AND AST; Bold in Page View updates window title `*` and `_dirty_state_changed()` on first click.
2. [Probe 2 — BUG-29 & HYG-07] `Ctrl+T`, `Ctrl+Shift+C`, `Ctrl+R`, `Ctrl+Alt+C/V` dispatch single canonical handlers with zero collisions; `bind_all('<Control-h>')` returns `'break'`.
3. [Probe 3 — HYG-03] Every ribbon/icon button has a `_tooltip` attribute and Unicode fallback.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] Full `py -3.12 -m unittest discover -s tests -v` passes 100% green -> Track 1 automated gate COMPLETE (with `BUG-09` production-fixture status explicitly recorded as `PASS` or `BLOCKED`, never silently assumed `PASS`)! (Optional: run Read-Only `/swarm` Track 1 Audit from `OPERATOR_GUIDE.md` before starting S14.)

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT delete dead code (`HYG-08` is strictly in S23). Do NOT begin toolbar re-layout/renaming (S14).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s13_ribbon_shortcuts.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s13_ribbon_shortcuts -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s13_ribbon_shortcuts` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s13_ribbon_shortcuts -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
