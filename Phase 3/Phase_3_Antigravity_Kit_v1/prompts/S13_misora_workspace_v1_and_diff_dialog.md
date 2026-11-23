<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S13
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> Proceed
- Model & Effort : Claude Sonnet 4.6
- Cheap-Model OK : BORDERLINE — Recommended Claude Sonnet 4.6 (schema validation, composite lock matching & diff modal)
- Ledger Coverage: FEAT-08 (Group G3 (post-DEP-4, DEP-9))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S13: `.misora` v1 Workspace Session (References + State + Stable-Key Locks) & Overwrite Diff Dialog in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @misora.py @core/text_encoding.py @tests/test_p3_s05_doc_lifecycle_save.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S13`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/workspace.py (NEW pure-Python .misora v1 JSON schema, atomic save/load, relative+absolute path resolver, composite lock key matcher)`
  * `core/__init__.py (export workspace helpers)`
  * `misora.py (File menu Save Project / Open Project .misora, DnD .misora support, ProjectDiffDialog for U-B18)`
  * `tests/test_p3_s13_misora_workspace.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/bundle_io.py`
  * `core/script_codec.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S13`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect S05's per-document state & stable lock-key helpers in `misora.py`.
2. Inspect File menu (`_build_menu`) and `_handle_dropped_paths()` in `misora.py`.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FEAT-08)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **FEAT-08**

### A. **FEAT-08 (`U-B17`, `U-B18` — Lead Ruling #3 & GPT Safety Rule):** Create `core/workspace.py` implementing `.misora` v1 atomic JSON workspace files (`write_atomic_encoded`) storing **STRICTLY references + state + stable-key locks ONLY** (NEVER unsaved story drafts, NEVER `.unity3d` binary blobs, NEVER runtime `Record.uid` — `NO-01`/`NO-12`): `schema_version: 1`, `files: [{rel_path, abs_path, locked_keys: [{box_ordinal, jp_sha256}]}]`, `active_file`, `active_box_idx`, `is_box0_active`, `view_mode`, and `search_scope`.

### B. On open `.misora`: (1) If current session has open files (especially dirty files), display the **`U-B18` Project Difference Mapping dialog** showing compact old-vs-new file table (Added / Removed / Kept / Dirty markers) + explicit overwrite warning + `Save Current` / `Discard & Open` / `Cancel` (`AGENTS.md` §16). (2) Restore files via S01/S12 staged batched open; report missing files clearly without crashing. (3) Re-attach Translation Locks ONLY when `(box_ordinal, sha256(original_jp_text))` matches confidently; if any persisted lock cannot be matched, **leave it unresolved and notify the user** (NEVER silently transfer a lock to another box — `NO-12`).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s13_misora_workspace.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1] Saved `.misora` JSON contains `schema_version == 1`, relative+absolute paths, view/scope state, and `(box_ordinal, jp_sha256)` lock keys — and contains ZERO `Record.uid` fields, ZERO story text drafts, and ZERO binary blobs.
2. [Probe 2] Reopening `.misora` restores open tabs, active box, and exact matched locks; when a box's JP text changed on disk, the unmatched lock stays unresolved (NOT transferred to another box) and surfaces a user warning.
3. [Probe 3 — U-B18] Opening a new `.misora` while current session has dirty files computes exact added/removed/dirty diff and aborts cleanly on Cancel.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_p3_s05_doc_lifecycle_save.py` and `tests/test_p3_s12_selection_drawer_open.py` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- NO draft snapshots or binary blobs in `.misora` (`NO-01`).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s13_misora_workspace.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s13_misora_workspace -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s13_misora_workspace -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
