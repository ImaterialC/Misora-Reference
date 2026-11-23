/plan Implement S20: Docked Right-Side MTL Drawer — Tab Infrastructure & `Dialogue` Multi-Engine Stack in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/mtl_engine.py @misora.py @tests/test_p3_s11_mtl_threading.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **FEAT-12** (Track 2 · Group G6a (post-DEP-6 — Split from All Script per Grok R1)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S20` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (3rd right-drawer tab `'MTL'` alongside `Customize` | `NGUI Glossary`; retire floating `TranslatorAssistantDialog` entry point; `Dialogue` mode enabled-engine vertical stack, isolated scratchpads, per-card Refresh/Apply, paid-API confirm, session cache, main-thread queue + stale guard)`
  * `tests/test_p3_s20_mtl_drawer_dialogue.py (NEW)`
  * `CHANGELOG.md (append `### S20` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/xunity_sync.py`
  * `core/script_codec.py`
5. **Changelog & Version Contract:**
   - Append `### S20` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S20`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Verify `DEP-6` (S01 `AGENTS.md` §24 update, S11 `BUG-14` & `BUG-27`, and Track 1 completion) are green.
2. Bind by symbol name in `misora.py`: `_build_side_drawer`, `_switch_side_drawer_tab`, `on_open_translator_assistant`, `TranslatorAssistantDialog`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FEAT-12)
==================================================
### A. **FEAT-12 (`U-B9`, `U-B32`):** Add **`MTL`** as the 3rd tab in the right-side drawer (`Customize` | `NGUI Glossary` | `MTL`), routing `Translator -> Translator Assistant...` and the `MTL` button to open/toggle this drawer (retiring the floating `TranslatorAssistantDialog` popup). In **`Dialogue` (1-box) mode**: vertically stack cards ONLY for user-enabled engines (default: `XUAT Cache` + `Google`; opt-in toggles for `DeepL` / `Local / Sugoi` / `LLM / OpenAI`). Each engine card has an editable scratchpad (isolated from story-widget routing + local Ctrl+Z), per-card `↻` Refresh (bypasses session cache), and per-card `→` Apply (enforces Translation Lock at model/application layer, commits via central path `source='mtl'`, NO `.strip()`). Top `Refresh All` refreshes enabled engines only, uses bounded session cache, and confirms before batch-calling paid APIs. ALL worker calls use main-thread `queue.Queue` + stale `(file_path, doc_id, box_uid, seq)` guard (`BUG-27`).

### B. **`CHANGELOG.md`:** Append `### S20` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s20_mtl_drawer_dialogue.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s20_mtl_drawer_dialogue` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — FEAT-12] Opening MTL opens right-side drawer 3rd tab (no floating Toplevel); Dialogue mode stacks only enabled engines; per-card Apply enforces model-level Translation Lock and preserves whitespace; paid engine Refresh All prompts confirmation.
2. [Probe 2] Switching files while an MTL drawer request is in flight discards the stale result cleanly.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_p3_s11_mtl_threading` and `tests.test_s8a_dialog_grab_safety` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT implement `All Script` mode inside MTL Drawer yet (S21) and do NOT merge `Import from XUAT` into MTL (`NO-09`).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s20_mtl_drawer_dialogue.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s20_mtl_drawer_dialogue -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s20_mtl_drawer_dialogue` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s20_mtl_drawer_dialogue -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
