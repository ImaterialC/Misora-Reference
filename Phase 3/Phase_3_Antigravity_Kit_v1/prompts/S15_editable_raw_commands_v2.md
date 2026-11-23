<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S15
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> Proceed
- Model & Effort : Claude Sonnet 4.6
- Cheap-Model OK : NO — Recommended Claude Sonnet 4.6 (whole-doc transaction, binary validation & UID lock/JP remap)
- Ledger Coverage: FEAT-11 (Group G5 (post-DEP-5))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S15: Whole-File Editable `Raw Commands` (Lossless v2 Transaction, Confirm, Undo & Lock/JP Remap) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/story_ast.py @core/undo_journal.py @misora.py @tests/test_p3_s02_ast_codec.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S15`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/undo_journal.py (new DocumentRecordsDelta holding before/after deep Record snapshots)`
  * `core/__init__.py (export DocumentRecordsDelta)`
  * `misora.py (Raw Commands v2 display/edit toggle or Apply/Revert controls, Yes/No confirmation, structural+binary validation, atomic commit + lock/JP key remap, _apply_delta DocumentRecordsDelta)`
  * `tests/test_p3_s15_raw_commands_edit.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/story_ast.py (v2 codec already finalized in S02/S03 — do NOT weaken!)`
  * `core/script_codec.py`
  * `core/mtl_engine.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S15`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Verify S02 (`BUG-01`, `BUG-03`, `BUG-04`) and S03 (`BUG-02`, `BUG-05`) are green before starting (`DEP-5`).
2. Inspect `txt_raw`, `_update_raw_view()`, and `_apply_delta()` in `misora.py`.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FEAT-11)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **FEAT-11**

### A. **FEAT-11 (`U-B31` — DEP-5):** Enable whole-file editing in the bottom **`Raw Commands`** pane strictly via lossless v2 text representation (`doc.to_v2_text()` / `StoryDocument.from_v2_text()`), supporting sensitive edits like voice cues (`vo_...`).

### B. Safety workflow: (1) Provide explicit Edit/Apply & Revert controls (keeping `txt_raw` read-only outside Edit Raw mode so accidental typing stays impossible). (2) On Apply, show an explicit `Yes/No` confirmation prompt warning that `Raw Commands` will replace workspace records. (3) On `Yes`, parse into a candidate `StoryDocument` and validate structurally: valid numeric command IDs, length-field integrity, and `to_binary()` + `from_binary()` round-trip (NO command-specific arity checks per `NO-07` / §8.4; `cmd_id` 35 & 32 preserved unchanged). (4) If valid, commit atomically as ONE `DocumentRecordsDelta` holding before/after deep Record list snapshots (NEVER rely on v2 round-trip for Undo!), remap Translation Locks & immutable JP keys via stable composite keys (`CLAUDE-N02`), mark dirty, and refresh all views. (5) On ANY parse/validation failure, abort, revert `txt_raw`, and show a clear error message with zero document mutation.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s15_raw_commands_edit.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1] Editing a `vo_` voice cue in `Raw Commands` -> Confirm `Yes` updates AST, refreshes Dialogue/All Script views, preserves locks via stable key remap, and Undo (`DocumentRecordsDelta`) restores exact prior Record list.
2. [Probe 2] Injecting corrupted/unparseable syntax -> Confirm `Yes` aborts cleanly, reverts `txt_raw`, surfaces error, and leaves `current_doc`, `is_dirty`, and `undo_journal` untouched.
3. [Probe 3] Clicking `No` on confirmation leaves document unchanged.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_p3_s02_ast_codec.py` and `tests/test_p3_s05_doc_lifecycle_save.py` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT add command-specific arity checks (`NO-07`). Do NOT alter `cmd_id` 35/32 (`DEF-02`).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s15_raw_commands_edit.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s15_raw_commands_edit -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s15_raw_commands_edit -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
