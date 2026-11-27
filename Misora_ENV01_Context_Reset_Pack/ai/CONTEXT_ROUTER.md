# Misora — Task-Based Context Router

> Load only the layers needed for the active task. The router is deliberately small.

## Layer 0 — Always read

- `AGENTS.md`
- `PROJECT_STATE.md`

Target combined size: approximately 12 KB or less after migration. These files contain current rules and current state, not milestone history.

## Layer 1 — Select by task

| Task type | Load these references | Source-first targets |
|---|---|---|
| ENV-01 / documentation | `docs/ai/ENV01_BLUEPRINT.md`, `DECISION_REGISTER.md`, `OPEN_ISSUES.md` | `AGENTS.md`, `PROJECT_STATE.md`, current docs tree, repo README |
| Tkinter UI / layout | `docs/architecture/UI_TKINTER.md`, relevant issue | Exact class/method in `misora.py`; relevant UI tests; theme/icon helpers only if used |
| AST / binary / Box / metadata | `docs/architecture/AST_BINARY_CONTRACT.md` | Relevant `core/story_ast.py`, codec/bundle module, tests; do not load whole `misora.py` |
| Undo / dirty / document lifecycle | `docs/architecture/UNDO_DOCUMENT_LIFECYCLE.md` | `core/undo_journal.py`, relevant `misora.py` methods and lifecycle tests |
| XUAT import / scan / sync / cleanup | `docs/architecture/XUAT_CONTRACT.md` | `core/xuat_index.py`, `core/xunity_sync.py`, `core/xuat_cleanup.py`, matching tests and exact dialog methods |
| Performance / memory / workers | `docs/architecture/WORKERS_MEMORY.md` | Worker, queue, cache, timer and destroy methods; stress tests |
| Release gate | `docs/release/V1_5_0_GATE.md` | Current `__init__.py`, full test inventory/output, QA evidence, Git state |
| Icon / splash / tooltip | Relevant UI issue and `docs/architecture/ASSETS_UI.md` | `assets/icon.py`, `assets/splash.py`, exact `misora.py` call sites, asset tests |

Only create architecture references after auditing the current source. Do not fill them with remembered or speculative contracts.

## Layer 2 — Source navigation protocol

For a large `misora.py` task:

1. Search exact symbol and all definitions/references.
2. Read the complete target method, not only a matching line.
3. Read directly called helpers and all relevant mutation callers.
4. Read the existing tests that protect the behavior.
5. Read one level of adjacent lifecycle/view code if state or widget ownership crosses methods.
6. Expand scope only when evidence requires it.

Target a small, relevant source slice (often 100–500 lines), not the full 1 MB file. For cross-cutting work, build a temporary call graph in memory or generate a committed symbol index; do not create untracked scratch files without approval.

## Layer 3 — Historical context (opt-in only)

Read `docs/history/` only when a task needs provenance, a previous regression explanation, a superseded decision, or the original manual QA record. Cite the exact archived source/section. Never treat an archived plan as current authorization.

## Output contract for every AI reviewer

- Scope reviewed and exact base HEAD.
- Source/test evidence inspected.
- Findings classified by evidence status and severity.
- Blockers vs non-blockers.
- What was not verified.
- Explicit recommendation; no automatic Proceed/commit/push authority.
