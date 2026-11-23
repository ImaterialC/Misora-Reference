/plan Implement S21: Right-Side MTL Drawer — `All Script` Mode (Exact 2 `tk.Text` Widgets + 5 Static Status Tags) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @misora.py @tests/test_p3_s20_mtl_drawer_dialogue.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **FEAT-13** (Track 2 · Group G6b (post-S20)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S21` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (`All Script` mode view inside MTL right drawer: top single-engine selector, exact 2 `tk.Text` widgets, 5 static theme-aware status tags, Refresh Selected / Apply Selected / Translate All / Apply All)`
  * `tests/test_p3_s21_mtl_drawer_all_script.py (NEW)`
  * `CHANGELOG.md (append `### S21` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/xunity_sync.py`
  * `core/script_codec.py`
5. **Changelog & Version Contract:**
   - Append `### S21` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S21`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Inspect S20's MTL right drawer implementation in `misora.py` and verify mode switching when `var_continuous_view` toggles.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FEAT-13)
==================================================
### A. **FEAT-13 (`U-B33` — LOCKED Lead Ruling #8, `NO-03`):** When `All Script` mode is active, switch the MTL right drawer to ONE single-engine selector at top + **EXACTLY 2 `tk.Text` widgets**: (1) ONE read-only multi-line `tk.Text` list of clickable per-box tagged blocks (preserving full 2–3 line dialogues without `Treeview` truncation) + (2) ONE shared bottom editable `tk.Text` scratchpad synced to the clicked box. Configure **5 shared static theme-aware status tags**: `✓` Ready, `⏳` Translating, `⚠` Error/Timeout, `🔒` Locked (grayed via theme `fg_muted`), `-` Untranslated/Empty/Punct-only (grayed via theme `fg_muted`). Provide Refresh Selected, Apply Selected, Translate All, and Apply All (reusing lock-skipping main-thread queue/batch pipeline; target box by stable `box.uid`; enforce Translation Lock at model/application layer, NO `.strip()`). ZERO `ttk.Treeview` and ZERO per-box Text editors (`NO-03`).

### B. **`CHANGELOG.md`:** Append `### S21` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s21_mtl_drawer_all_script.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s21_mtl_drawer_all_script` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — FEAT-13] In `All Script` mode, MTL drawer contains EXACTLY 2 `tk.Text` widgets (read-only multi-line list + bottom scratchpad), ZERO `ttk.Treeview`, ZERO per-box Text widgets; all 5 static status tags exist (`✓`, `⏳`, `⚠`, `🔒`, `-`) with locked/empty styled via `fg_muted`.
2. [Probe 2 — FEAT-13] Translate All and Apply All skip locked boxes at the model layer and target unlocked boxes by stable `box.uid` cleanly.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_p3_s20_mtl_drawer_dialogue` and `tests.test_p3_s11_mtl_threading` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- NO `ttk.Treeview`, NO 142 separate `tk.Text` editors (`NO-03`), NO `Import from XUAT` inside MTL (`NO-09`).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s21_mtl_drawer_all_script.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s21_mtl_drawer_all_script -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s21_mtl_drawer_all_script` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s21_mtl_drawer_all_script -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
