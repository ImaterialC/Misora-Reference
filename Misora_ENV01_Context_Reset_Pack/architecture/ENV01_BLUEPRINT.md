# ENV-01 — AI Environment and Documentation Layering Blueprint

**Status:** recommended design for Project Lead approval. A formal `ENV-01` spec was not found in the public Reference search during this review; this file therefore defines a proposed scope, not an already-approved project contract.

## 1. Problem statement

The current workflow makes every agent read a long `PROJECT_STATE.md` before task-specific context is selected. Public repository snapshot observed during this review: `AGENTS.md` approximately 10.7 KB, `PROJECT_STATE.md` approximately 223.6 KB / 1,631 lines, and `misora.py` approximately 1.03 MB. Local values must be remeasured because the latest S11e commit is reportedly not pushed.

This causes three risks:

1. Context budget is spent on old milestones unrelated to the current task.
2. Current decisions, superseded plans, deferred work and historic test results can contradict each other.
3. Large monolithic source files are loaded wholesale instead of through symbol-level navigation.

## 2. Target documentation structure

```text
Misora-Editor/
├── AGENTS.md                         # always-read rules; target 3–5 KB
├── PROJECT_STATE.md                  # current dashboard; target 8–15 KB
├── docs/
│   ├── ai/
│   │   ├── CONTEXT_ROUTER.md         # task → exact references/source/test map
│   │   └── ENV01_MIGRATION.md        # migration policy and audit evidence
│   ├── project/
│   │   ├── DECISION_REGISTER.md      # active decisions only
│   │   ├── OPEN_ISSUES.md            # current issue ledger, status/evidence
│   │   ├── TEST_BASELINE.md          # latest observed baseline and known failures
│   │   └── MILESTONE_INDEX.md        # short S01–S11e index, links only
│   ├── architecture/
│   │   ├── AST_BINARY_CONTRACT.md
│   │   ├── UNDO_DOCUMENT_LIFECYCLE.md
│   │   ├── XUAT_CONTRACT.md
│   │   ├── UI_TKINTER.md
│   │   ├── WORKERS_MEMORY.md
│   │   └── ASSETS_UI.md
│   ├── release/
│   │   └── V1_5_0_GATE.md            # create/reconcile only if release is reinstated
│   └── history/
│       ├── PROJECT_STATE_ARCHIVE_*.md
│       ├── S01-S11_CLOSURE_INDEX.md
│       └── superseded-plans/         # preserved, never auto-loaded
└── tools/
    └── generate_symbol_index.py      # optional, stdlib AST-based index generator
```

Do not create empty architecture documents just to match this tree. Create a domain reference only after its contracts have been audited against current source/tests.

## 3. Context layers

- **Layer 0 (every task):** `AGENTS.md` + compact `PROJECT_STATE.md` only.
- **Layer 1 (task-specific):** one router entry and one or two relevant architecture/issue documents.
- **Layer 2 (source evidence):** exact definitions, callers, related tests and directly required helpers.
- **Layer 3 (historical):** only when provenance or an old decision is needed.

Recommended initial budget: no more than approximately 12 KB for Layer 0 and no more than 1–3 supporting documents before the source audit. Measure tokens with the actual target agents; byte limits are only rough proxies for token use.

## 4. Content migration rules

1. Snapshot the current docs before editing. No source files, config, backups, or untracked user assets are touched by ENV-01.
2. Parse every heading, status table and decision in the existing Project State. Assign exactly one lifecycle label: `ACTIVE`, `SUPERSEDED`, `DEFERRED`, `RETRACTED`, or `HISTORICAL-REFERENCE`.
3. Extract current state from local source/Git/test outputs; do not summarize solely from old Project State prose.
4. Keep only the current dashboard and pointers in the root `PROJECT_STATE.md`.
5. Move historical detail into archive documents preserving original text, date, provenance and cross-references. Do not delete it.
6. The new root files must link to relevant reference documents, but links must not imply they are read automatically.
7. Resolve conflicts explicitly. Newer user/Project Lead decision supersedes old AI proposals; actual source/tests establish implementation behavior; tests alone do not prove every Windows manual behavior.
8. Include a generated symbol index for `misora.py` rather than copying the entire file into prompts. It must include class/method line spans and optionally test references; it must be reproducible and marked with the source HEAD used to generate it.
9. Keep a changelog/history of the documentation migration itself.
10. Run a multi-agent validation: give Gemini, ChatGPT, Qwen and Antigravity the same small test task; compare whether they identify the same current HEAD, active scope, blockers and relevant source symbols without loading archives.

## 5. What not to do

- Do not merely ask an AI to “summarize the 250 KB Project State” and replace the original. That risks dropping constraints and preserving false claims.
- Do not delete historical milestone records or old closure reports.
- Do not shorten technical invariants until their meaning changes.
- Do not split `misora.py` during ENV-01. Source decomposition is a separate refactor with its own tests and scope.
- Do not treat token reduction as the only success metric. Correct retrieval, no instruction conflicts, reproducibility and reviewer agreement matter more.
- Do not update `AGENTS.md` automatically from Gemini/Antigravity suggestions. All permanent invariants require Project Lead review.

## 6. ENV-01 acceptance criteria

- Root `AGENTS.md` contains only permanent, current rules and is materially smaller (suggested 3–5 KB).
- Root `PROJECT_STATE.md` contains only current state, active blockers, deferred items, latest baseline, current HEAD/version, and next authorized action (suggested 8–15 KB).
- Full original Project State and closure reports remain archived and retrievable.
- Every existing canonical decision/defect/requirement is accounted for in a migration matrix; none silently disappears.
- Superseded and retracted claims cannot be mistaken for active instructions.
- `CONTEXT_ROUTER.md` selects minimal task-specific material.
- A current, reproducible symbol map makes `misora.py` navigable without loading the entire file.
- Four agents independently identify the same active state and task boundaries from Layer 0 + router.
- No source, tests, version, user config, backup, or product asset changes are made under ENV-01 unless separately authorized.
