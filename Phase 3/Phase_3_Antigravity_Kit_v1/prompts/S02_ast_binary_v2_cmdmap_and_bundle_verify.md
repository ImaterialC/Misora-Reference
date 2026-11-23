<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S02
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> /boost (after Proceed)
- Model & Effort : Claude Opus 4.6 (HIGH risk: binary format & v2 codec — DO NOT use Flash or GPT-OSS 120B)
- Cheap-Model OK : NO — Use Claude Opus 4.6 (or Claude Sonnet 4.6 minimum)
- Ledger Coverage: BUG-01, BUG-03, BUG-04, BUG-09 (Group B1 (DEP-5 part 1))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S02: Strict Binary Parse, Lossless v2 + \b64:, Command Map/Breakers (Guard 35/32) & Bundle Verify in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/story_ast.py @core/bundle_io.py @misora.py @tests/test_misora_core.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S02`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/story_ast.py (from_binary, to_binary, escape_arg, unescape_arg, render_v2, from_v2_text, _CMD_MAP, _INV_CMD_MAP, DEFAULT_BREAKERS, _rebuild_boxes)`
  * `core/bundle_io.py (save_bundle_story non-target verification)`
  * `misora.py (ONLY _update_raw_view Box 0 cmd_id==0 highlight at ~line 6825)`
  * `tests/test_p3_s02_ast_codec.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/script_codec.py`
  * `core/undo_journal.py`
  * `core/search_engine.py`
  * `core/mtl_engine.py`
  * `misora.py (all methods outside _update_raw_view)`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S02`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect exact line ranges of `from_binary()`, `to_binary()`, `escape_arg()`, `unescape_arg()`, `Record.render_v2()`, `from_v2_text()`, `_CMD_MAP`, `_INV_CMD_MAP`, `DEFAULT_BREAKERS`, `_rebuild_boxes()` in `core/story_ast.py`.
2. Inspect `save_bundle_story()` in `core/bundle_io.py` and check whether any `.unity3d` fixture is available on disk to empirically test non-target object `get_raw_data()` invariance under `packer='original'`.
3. Inspect `_update_raw_view()` Box 0 highlight in `misora.py` (~line 6825).
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-01, BUG-03, BUG-04, BUG-09)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-01, BUG-03, BUG-04, BUG-09**

### A. **BUG-01 (`core/story_ast.py:from_binary()`):** Strictly validate every 2-byte command header, 4-byte arg length, exact arg payload bytes, and terminating 0-length marker. Raise `ValueError` (caught/wrapped as `BundleIOError` in `bundle_io.py`) on any truncated header, incomplete arg length, payload overrun, or missing terminator instead of silent `break`. Do NOT add command-specific arity checks (`PROJECT_STATE.md` §8.4). Track parse completeness so incomplete docs cannot be saved.

### B. **BUG-03 (`core/story_ast.py` + `misora.py:_update_raw_view()`):** (1) Remove legacy `if cid == 0 and r.cmd_name != 'fade' and r.cmd_name in _INV_CMD_MAP:` remapping in `to_binary()` (`AGENTS.md` §8). (2) In `escape_arg()`, escape trailing/whitespace-only args (e.g. `\s`/`\S` protection so `' '` never becomes a blank terminator line), escape `DEFAULT_CATEGORIES` collisions (`\<Category>`), and emit `\b64:<base64>` whenever an arg contains `surrogateescape` characters (`0xDC80..0xDCFF`), reversing all three losslessly in `unescape_arg()`. (3) Fix dead `if self.cmd_name in _CMD_MAP:` branch in `Record.render_v2()` (always preserve unambiguous `#<cmd_id>` or match `cmd_id` against canonical map). (4) In `misora.py:_update_raw_view()`, fix Box 0 highlight for `cmd_id == 0` to check `len(r.args) > 0 and r.args[0]` (matching `get_metadata()`). Note: this also makes S2 `to_v2_text()` dirty checkpoints lossless (`CLAUDE-N08`).

### C. **BUG-04 (`core/story_ast.py` — SOLE OWNER of `_INV_CMD_MAP` disambiguation):** Separate human-readable display labels (for `Raw Commands`) from canonical binary/inverse ID resolution so display cleanup NEVER alters numeric IDs. Classify structural breakers in `_rebuild_boxes()` by verified numeric `cmd_id` (`0`, `1`, `4`, `10`, `36`), NEVER by shared ambiguous command name and NEVER treating `cmd_id == 12` (`vo_` cue) as a breaker; preserve `cmd_id == 6` dialogue projection. **HARD GUARDRAIL (Lead Ruling (a)):** NEVER alter binary `cmd_id == 35` (narration) or `cmd_id == 32` (subtitle) on any path (`_CMD_MAP`, `_INV_CMD_MAP`, `set_box_kind`, `get_metadata`, `to_binary`, v2).

### D. **BUG-09 (`core/bundle_io.py:save_bundle_story()`):** Test on a real `.unity3d` fixture (if present; or synthetic multi-object UnityPy bundle test) whether per-object raw data hashes of non-target objects remain identical under `packer='original'`. If invariant, enforce per-object non-target hash verification in `save_bundle_story()` before `os.replace()`; if UnityPy legitimately re-serializes harmless container headers, document exact observed evidence in `PROJECT_STATE.md` and refine `AGENTS.md` §9 honestly without breaking valid saves.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s02_ast_codec.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — BUG-01] Truncated binary streams (1-byte trailing header, 2-byte partial arg len, payload shorter than declared len, missing len-0 terminator) MUST raise `ValueError`/`BundleIOError`.
2. [Probe 2 — BUG-03] `Record(cmd_id=0, cmd_name='title', args=['Ep1'])` serializes to binary with `cmd_id == 0` (NOT 30).
3. [Probe 3 — BUG-03] v2 round-trip preserves whitespace-only arg `' '`, category-colliding args `'Sound'` / `'Other'` / `'Effect'`, and surrogate-escaped invalid UTF-8 bytes `b'\xff\xfe'` via `\b64:` across `binary -> v2 -> binary`.
4. [Probe 4 — BUG-04] Numeric `cmd_id == 35` (narration) and `cmd_id == 32` (subtitle) survive binary and v2 round-trips unchanged; mid-script `cmd_id` in `(0, 1, 4, 36)` splits adjacent same-speaker boxes; `cmd_id == 12` `vo_` cue is never treated as a breaker.
5. [Probe 5 — BUG-09] Non-target object preservation check verified on bundle repack (failing if a non-target object payload is altered).

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] Existing `tests/test_misora_core.py` (20 tests) passes unchanged.
2. [Guard 2] Empty binary arg space sentinel (`DEF-01` / `to_binary` line 725) stays untouched.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT alter `set_box_kind`/`inject_box`/`insert_box`/`delete_boxes`/`move_box` (S03), do NOT touch `core/script_codec.py` (S04), do NOT change `cmd_id` 35 or 32 (`DEF-02`), do NOT alter empty-arg space sentinel (`DEF-01`).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s02_ast_codec.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s02_ast_codec -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s02_ast_codec -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
