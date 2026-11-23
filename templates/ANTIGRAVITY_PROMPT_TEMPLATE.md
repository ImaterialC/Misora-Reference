# Google Antigravity Prompt Template (Phase 3 Output)

Every finalized session prompt produced in Phase 3 MUST follow this structure (adapted per session):

```text
/plan Implement <Session ID>: <Concise Session Title> in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @misora.py @<other_target_files> @tests/

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. Planning-First Gate (STRICT):
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for user approval (`Proceed`) before editing any file.
   - After approval (`Proceed`), execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. Workspace & Git Hygiene:
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active Python 3.12 interpreter path/version.
   - If unexpected uncommitted modifications conflict with this session, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. Allowed File Ownership (after approval):
   - Allowed to create/modify:
     * `<exact_file_1>` (scoped strictly to <scope>)
     * `tests/<test_file>.py`
     * `PROJECT_STATE.md` (measured verification update only)
   - DO NOT modify:
     * `<explicitly_excluded_files_or_modules>`
4. No new external dependencies. Follow all `AGENTS.md` invariants (main-thread Tkinter safety, atomic writes, undo integrity).
5. Never remove, skip, weaken, or silently mock existing tests. Never perform live network/API calls in unit tests.
6. Stop strictly after <Session ID>. Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. <Target component / method 1>
2. <Target component / method 2>
3. Any discrepancy between assumptions and live disk code (STOP and surface before editing).

==================================================
PART 2 — REQUIRED IMPLEMENTATION (<Ledger IDs Covered>)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: <BUG-01, FEAT-01, ...>

### A. <Subtask 1 — Ledger ID>
- <Exact requirement, edge cases, and invariant checks>

### B. <Subtask 2 — Ledger ID>
- <Exact requirement, edge cases, and invariant checks>

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/<test_file>.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` in `setUp`/`tearDown`, suppress modal `messagebox` calls during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
  1. [Probe 1] <Exact scenario & assertions>
  2. [Probe 2] <Exact scenario & assertions>
- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
  1. [Guard 1] <Exact scenario & assertions>

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- <Items owned by later sessions>
- <Explicit user non-goals from Phase 2.5 NO-*>

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. Now (`/plan` — ZERO file edits): Deliver Implementation Plan artifact and WAIT for `Proceed`.
2. After `Proceed`:
   - Write tests -> run pre-fix (record Probes failing, Guards passing) -> implement changes -> run:
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.<test_file> -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver Walkthrough artifact with exact commands, real outputs, `git status --short`, concise diff summary, and handoff status for the next session.
```
