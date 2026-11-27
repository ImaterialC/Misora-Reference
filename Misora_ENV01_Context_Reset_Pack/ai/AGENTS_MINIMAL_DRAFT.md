# Misora — Agent Rules (ENV-01 compact draft)

> Proposed replacement for the always-loaded root `AGENTS.md`. Do not install until Project Lead approves the ENV-01 migration.

## 1. Authority and evidence

1. Read this file and the compact `PROJECT_STATE.md` before work. Then use `CONTEXT_ROUTER.md` to load only task-relevant material.
2. Authority order: current explicit Project Lead instruction/approval; current local source, tests and Git state; current canonical decision register/state; approved implementation plan; archived reports/transcripts. Older AI reports are claims, not authority.
3. Label findings `CONFIRMED`, `REPORTED`, `NEEDS-REPRO`, `DEFERRED`, or `RETRACTED`. Never present reported test output as your own execution.
4. Read actual source and tests at the current local HEAD. Do not infer local state from public GitHub when changes are unpushed.
5. Do not invent paths, symbols, caller relationships, test outcomes, fixture availability, or Windows behavior.

## 2. Git and workspace safety

1. Before any edit, record branch, `git rev-parse HEAD`, `git status --short`, and the task's exact allowed-file list.
2. Never run destructive Git commands: `reset`, `clean`, `stash`, `checkout`, `restore`, or force operations. Never overwrite pre-existing/untracked files, local config, backups, or user data.
3. Do not commit or push unless the Project Lead explicitly authorizes that exact action. A plan clearance is not commit/push authorization.
4. Edit only files explicitly listed in the current approved scope. Treat all other files as forbidden/inspect-only.
5. No version promotion unless the Project Lead explicitly authorizes the final release gate's promotion step.

## 3. Misora architecture invariants

1. One `tk.Tk()` root (`MisoraApp`); splash/dialogs are `Toplevel`. Every Tk variable has an explicit `master`.
2. Workers never call Tk, mutate live documents, or mutate Undo state. Capture immutable snapshots on the UI thread; deliver completion/error through a main-thread queue.
3. `StoryDocument.records` is source of truth; `Box` is a projection. Preserve record identity and unknown commands. Structural edits use document APIs and rebuild projections.
4. `Box.clean_text`, `.text`, and `.raw` are read-only. Snapshots preserve segments. Preserve `extra_args`, speaker, voice cue, kind, and command ownership.
5. `inject_box`/`set_metadata` may only replace owned arguments. Do not silently flatten multi-segment content. Keep the DEF-01 single-space sentinel behavior unchanged unless a separate core decision authorizes a fix.
6. Flush pending edits before Undo, Redo, Save, Close, navigation, view rebuild, and external mutation. Undo batches must close in `finally`; model mutation precedes one UI refresh.
7. Preserve immutable Japanese XUAT source keys per Box UID. Preserve encoding, BOM, line endings, key whitespace, and untouched dictionary lines. Never replace malformed decode data and rewrite the entire file.
8. Bundle save must verify the temporary bundle and target TextAsset before replacing the original. Failed save aborts close.
9. `__version__` in root `__init__.py` is the single version source. Version/session numbers and release tags are distinct; do not promote versions casually.
10. Core modules remain UI-independent: no `tkinter` or `misora` imports in `core/` unless an approved architecture decision changes this invariant.

## 4. Test and delivery discipline

1. Establish the actual baseline before editing. Record OS, Python, dependencies, discovery count, PASS/SKIP/FAIL/ERROR and fixture blockers.
2. Use strict TDD when the approved plan requires it. Do not weaken assertions, normalize away defects, delete tests, or convert SKIP/NOT TESTED into PASS.
3. Run focused tests first, then required integration/full suites. Report the literal command and observed output. Clearly disclose interrupted or disjoint-batch coverage.
4. Manual Windows QA is separate from automated tests. Preserve `MANUAL-PENDING` until observed or explicitly waived by the Project Lead.
5. Every delivery states changed files, tests and actual results, limitations, risks, rollback notes, and state/document updates.

## 5. Scope control

- No new feature work while ENV-01 migration is in progress, except explicitly approved documentation tooling.
- Triage findings before implementation. A backlog entry is not permission to implement.
- P0/P1 source fixes require a dedicated approved scope; do not smuggle them into an audit-only task.
- Do not read the entire historical Project State, full `misora.py`, or archived transcripts by default. Use the task router and symbol index.
