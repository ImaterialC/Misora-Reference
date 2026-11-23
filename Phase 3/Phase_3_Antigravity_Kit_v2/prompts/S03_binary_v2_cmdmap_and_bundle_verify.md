/plan Implement S03: Strict Binary Parse, Lossless v2 + \b64:, Command Map/Breakers (Guard 35/32) & Fixture-Gated Bundle Verify in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/story_ast.py @core/bundle_io.py @misora.py @tests/test_misora_core.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **BUG-01, BUG-03, BUG-04, BUG-09** (Track 1 · Group B1 (DEP-5 part 1)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S03` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/story_ast.py (from_binary, to_binary, escape_arg, unescape_arg, Record.render_v2, from_v2_text, _CMD_MAP, _INV_CMD_MAP, DEFAULT_BREAKERS, _rebuild_boxes)`
  * `core/bundle_io.py (save_bundle_story non-target verification)`
  * `misora.py (ONLY `_update_raw_view()` Box 0 `cmd_id == 0` highlight condition)`
  * `tests/test_p3_s03_binary_v2.py (NEW)`
  * `CHANGELOG.md (append `### S03` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/script_codec.py`
  * `core/undo_journal.py`
  * `core/search_engine.py`
  * `misora.py (all methods outside `_update_raw_view`)`
5. **Changelog & Version Contract:**
   - Append `### S03` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S03`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Bind by symbol name in `core/story_ast.py`: `from_binary`, `to_binary`, `escape_arg`, `unescape_arg`, `Record.render_v2`, `from_v2_text`, `_CMD_MAP`, `_INV_CMD_MAP`, `DEFAULT_BREAKERS`, `_rebuild_boxes`.
2. Inspect `save_bundle_story` in `core/bundle_io.py` and check whether any real production `.unity3d` fixture exists locally on disk (do NOT invent one).
3. Inspect `_update_raw_view` Box 0 highlight condition in `misora.py`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-01, BUG-03, BUG-04, BUG-09)
==================================================
### A. **BUG-01 (`core/story_ast.py:from_binary()`):** Strictly validate every 2-byte command header, 4-byte arg length, exact arg payload bytes, and terminating 0-length marker. Raise `ValueError` (wrapped as `BundleIOError` by `bundle_io.py`) on truncated header, partial arg length, payload overrun, or missing terminator instead of silent `break`. Refuse to produce/save an incomplete document. Do NOT add command-specific arity checks (`NO-07` / §8.4).

### B. **BUG-03 (`core/story_ast.py` + `misora.py:_update_raw_view()`):** (1) Remove the legacy `cmd_id == 0` remapping branch in `to_binary()` (`AGENTS.md` §8). (2) In `escape_arg()`, escape trailing/whitespace-only spaces (`\s` for ASCII space, `\S` for `U+3000` so `' '` never becomes a blank terminator line), prefix a backslash on `DEFAULT_CATEGORIES` collisions (`\<Cat>`), and emit `\b64:<base64>` whenever an arg contains `surrogateescape` non-UTF-8 bytes (`0xDC80..0xDCFF`); reverse ALL three losslessly in `unescape_arg()`. (3) Fix dead `if self.cmd_name in _CMD_MAP:` branch in `Record.render_v2()` so v2 emits unambiguous `name#id` headers. (4) In `misora.py:_update_raw_view()`, fix Box 0 highlight for `cmd_id == 0` to check `len(r.args) > 0 and r.args[0]` (matching `get_metadata()`). Note: `_INV_CMD_MAP` disambiguation is owned solely by `BUG-04` below.

### C. **BUG-04 (`core/story_ast.py` — SOLE OWNER of `_INV_CMD_MAP` disambiguation):** Separate readable `Raw Commands` display labels from canonical binary/inverse ID resolution so display cleanup NEVER changes numeric IDs; ambiguous plain-name v2 headers without `#id` must not silently pick last-wins. Classify structural breakers in `_rebuild_boxes()` by verified numeric `cmd_id` (`0=title`, `1=outline`, `4=type`, `10=goto`, `36=situation`), NEVER by shared name and NEVER treating `cmd_id == 12` (`vo_` cue) as a breaker; preserve `cmd_id == 6` dialogue projection. **HARD GUARDRAIL (Lead Ruling (a)):** NEVER alter binary `cmd_id == 35` (narration) or `cmd_id == 32` (subtitle) on any path (`_CMD_MAP`, `_INV_CMD_MAP`, `set_box_kind`, `get_metadata`, `to_binary`, v2).

### D. **BUG-09 (`core/bundle_io.py:save_bundle_story()` — Fixture-Gated):** Build a deterministic **synthetic** multi-object UnityPy test (or mock object container) to verify per-object non-target raw-data hash verification before `os.replace()`. If a genuine local production `.unity3d` fixture is available, test `packer='original'` invariance on it; if NO real production fixture exists locally, explicitly record the production-bundle compatibility claim as **`BLOCKED (no local production .unity3d fixture)`** in `CHANGELOG.md` and Walkthrough — NEVER mark it `PASS` and NEVER fabricate a fixture.

### E. **`CHANGELOG.md`:** Append `### S03` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s03_binary_v2.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s03_binary_v2` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-01] `from_binary()` raises `ValueError` on: 1-byte trailing header, 2-byte partial arg length, payload shorter than declared length, and missing length-0 terminator.
2. [Probe 2 — BUG-03] `Record(cmd_id=0, cmd_name='title', args=['Ep1'])` serializes via `to_binary()` with `cmd_id == 0` (NOT 30).
3. [Probe 3 — BUG-03] `binary -> v2 -> binary` round-trip preserves whitespace-only arg `' '`, category-colliding args `'Sound'` / `'Other'` / `'Effect'`, and surrogate-escaped invalid UTF-8 bytes `b'\xff\xfe'` via `\b64:`.
4. [Probe 4 — BUG-04] Mid-script `cmd_id` in `(0, 1, 4, 36)` splits adjacent same-speaker boxes into separate boxes.
5. [Probe 5 — BUG-09] Synthetic multi-object verification test fails if a non-target object's raw bytes change during `save_bundle_story()` (passes when non-target objects are preserved).

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1 — Lead Ruling (a)] Records with `cmd_id == 35` (narration) and `cmd_id == 32` (subtitle) retain exact numeric IDs 35 and 32 through `to_binary`/`from_binary` and `to_v2_text`/`from_v2_text` (placed strictly in Guards, NOT Probes, because it already passes on pre-patch `683724e`!).
2. [Guard 2] `cmd_id == 10` tap-breaker splits boxes and `cmd_id == 12` `vo_` cue attaches voice without splitting; `cmd_id == 6` dialogue projects cleanly.
3. [Guard 3] Existing `tests/test_misora_core.py` passes cleanly (record actual observed test count from disk, never hardcode) and empty-arg space sentinel (`DEF-01`) stays untouched.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT alter `set_box_kind`/`inject_box`/`insert_box`/`delete_boxes`/`move_box` (S04), do NOT touch `core/script_codec.py` (S05), do NOT change `cmd_id` 35/32 (`DEF-02`) or empty-arg sentinel (`DEF-01`).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s03_binary_v2.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s03_binary_v2 -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s03_binary_v2` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s03_binary_v2 -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
