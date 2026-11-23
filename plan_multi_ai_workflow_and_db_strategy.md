# Multi-AI Engineering Workflow and `master.db` Handling Strategy

**Document status:** Recommended operating design  
**Research snapshot:** 2026-11-23  
**Project repositories:** [Misora-Editor](https://github.com/ImaterialC/Misora-Editor) · [Misora-Reference](https://github.com/ImaterialC/Misora-Reference)

## Executive recommendation

Keep the current no-API, browser-based council as an independent review layer, but stop making every model debate every task until it agrees. Use a short evidence-led process with explicit disagreement records and a human decision gate. Keep Antigravity as the primary local implementation agent because it can inspect the working checkout and run the project's tests. Use its Orchestrator, `/swarm`, `/boost`, `/teamwork`, or `/run-workflow` only when the task fits the feature and the account has access.

Do not build an API council or database downloader as the next step. Neither is necessary to fix the current workflow, and both add maintenance or cost.

## 1. Recommended workflow

### Stage 0 — Intake and repository truth

The secretary creates a short task brief with:

- The question or bug to resolve.
- Target repository and exact branch/commit SHA.
- Relevant file paths, tests, and project-state documents.
- What is in scope and explicitly out of scope.
- What decision the owner needs to make.
- What evidence would prove or disprove the main assumptions.

For a Misora-Editor task, start with `AGENTS.md`, `PROJECT_STATE.md`, `docs/COPILOT_WORKFLOW.md` (when relevant), the task brief, then the actual source and tests. For a Misora-Reference task, start with this repository's `AGENTS.md`, `README.md`, `SECRETARY_PLAYBOOK.md`, and relevant prototype/reference files.

A GitHub URL is a navigation aid, not proof that a model has read every file. Ask the reviewer to list the files it actually inspected and any files it could not access. For a specific snapshot, provide a ZIP or selected source files only when the receiving product actually supports them.

### Stage 1 — Independent first-pass reviews

Send the same compact brief to two reviewers independently. Do not show them each other's answers yet. Prefer different providers or different model families when practical.

Ask each reviewer to return:

1. Findings with file path and line/function where applicable.
2. Evidence and a reproducible test or inspection method.
3. Assumptions and unknowns.
4. Potential regressions and edge cases.
5. A recommended next step, not an implementation prompt yet.

This reduces anchoring: a model that reads another model's answer first may simply repeat it.

### Stage 2 — Adversarial review

Give the independent findings to one strong critic (often ChatGPT Thinking for a high-risk question, or Claude/Gemini when available). Ask it to attack the evidence, not to attack the author. It must identify which findings are confirmed, contradicted, duplicated, or still unknown.

Do not ask “make everyone agree”. Ask “what evidence would settle the disagreement?”

### Stage 3 — Evidence gate and decision record

The secretary puts each important statement into one category:

- `SOURCE-VERIFIED`: seen in current source or current official documentation.
- `REPRODUCED`: demonstrated by a test or controlled run.
- `USER-OBSERVATION`: experience reported by the owner.
- `INFERENCE`: plausible conclusion, not yet proven.
- `PROPOSAL`: future design suggestion.
- `UNKNOWN`: unresolved.

A finding is not accepted because two or more models repeat it. Require source paths, line references, official URLs, test logs, or a small experiment. Preserve unresolved dissent in the decision record.

The owner approves, rejects, or defers the proposal. Unanimous AI agreement is not a gate.

### Stage 4 — One bounded implementation brief

Only after the decision gate, create one self-contained execution prompt for Antigravity (or a bounded Copilot task). Every prompt must contain:

- Target repository, branch, and starting SHA.
- Problem and supporting evidence.
- Exact goal and expected behavior.
- Allowed files and forbidden files.
- Constraints and compatibility requirements.
- Acceptance criteria and exact test commands.
- Data-preservation and rollback rules.
- Stop conditions.
- Required completion report with changed files, diff summary, test output, and unverified items.

Do not make another AI rewrite the prompt indefinitely. Allow one critique pass and one correction pass. If a real issue remains, revise the brief; otherwise stop.

### Stage 5 — Local implementation and verification

Antigravity is the primary writer for normal Misora changes. Use its local checkout as the implementation source of truth. One agent should own a given file at a time. Parallel workers should be read-only or assigned clearly disjoint files/workspaces.

Before implementation, the agent must report working directory, branch, HEAD, and `git status`. Review the diff before accepting it. Run the stated tests and record actual output. Never treat a test count copied from an old transcript as a current result.

Do not commit or push unless the owner requests it.

### Stage 6 — Record and archive

Keep a concise task brief, review findings, decision, and final execution brief in the active debate folder. Store raw transcripts as historical evidence; archive them after a milestone is closed. Do not let a huge transcript become the only source of current project state.

Suggested files for a task folder:

```text
active_debates/<topic>/
  BRIEF.md
  REVIEW_01_<reviewer>.md
  REVIEW_02_<reviewer>.md
  ADVERSARIAL_REVIEW.md
  DECISION.md
  EXECUTION_BRIEF.md
  VERIFICATION.md
```

These are suggested files, not existing automated features. Copy the templates from `templates/` as needed.

## 2. Which Antigravity feature should be used?

The official Antigravity documentation distinguishes these features (availability and quota consumption can change; check the account UI before a run):

| Feature | Documented purpose | Best fit for Misora |
|---|---|---|
| Orchestrator | A planner explores the code, plans and reviews; an executor searches, edits, builds, and tests | Normal multi-file feature work when the account exposes it |
| `/boost` | Multi-agent deep reasoning with iterative challenge and verification | Difficult root-cause, algorithm, or concurrency investigation |
| `/swarm` | Named workers and a verifier coordinate on a shared message board | Read-only parallel audit or independent work on disjoint files |
| `/teamwork` | Longer-horizon multi-agent project with milestones and review gates | Large, multi-day integration/migration or deep research |
| `/run-workflow` | A generated workflow script runs agents in parallel/sequential phases | Repeatable multi-step audit or test/fix pipeline |

Practical starting point: use ordinary Plan mode for small/medium changes; use Orchestrator for a well-scoped coding task; use `/swarm` for a read-only multi-perspective audit. Try `/teamwork` only for a genuinely large project. `/boost` is not a substitute for clear task scope. `/run-workflow` creates a script and asks for approval before running unless permissions already allow it; read that generated script before approving.

Official references (accessed 2026-11-23):

- [Choose a model and Orchestrator](https://antigravity.google/docs/models)
- [Slash commands overview](https://antigravity.google/docs/slash-commands)
- [Boost](https://antigravity.google/docs/boost/)
- [Swarm](https://antigravity.google/docs/swarm/)
- [Teamwork](https://antigravity.google/docs/teamwork/)
- [Dynamic Workflows](https://antigravity.google/docs/dynamic-workflows/)

Important distinctions: `/swarm` is the command explicitly documented as using a shared message board; `/teamwork` has Sentinel, a Project Orchestrator, auditors, and milestone handoffs. `/teamwork` is a paid-plan feature; `/swarm` and `/run-workflow` are documented for all plans; `/boost` is paid-plan only. Check current availability inside the app because preview status and plan tables can change.

## 3. Master database (`master.db`) strategy

### What the current repository actually shows

- No `master.db`, `.db`, or `.sqlite` file is tracked in the current `Misora-Reference` main-branch tree inspected on 2026-11-23.
- `extractor_prototype/db_metadata.py` looks for a local database at `D:\\Kyouka-Asset-Explorer\\master.db`, `D:\\Reference\\Misora-Reference\\master.db`, or `.`/`master.db`.
- The current `DatabaseMetadata` connection uses SQLite read-only mode (`mode=ro`) and has static fallbacks when the database is absent.
- The code does not implement an upstream download or automatic update operation.

Therefore the database is currently an optional local dependency, not a source file that the repository must contain. Keep that arrangement unless the owner explicitly approves a different distribution design.

### Recommended policy

1. Keep the real database outside Git and outside the replacement archive.
2. Add `.gitignore` rules for `*.db`, `*.sqlite`, `*.sqlite3`, and SQLite sidecars. The package includes these rules.
3. Do not invent or hardcode an upstream URL, 51.4 MB size, update cadence, ETag behavior, or checksum. Verify the actual source and current file metadata first.
4. Do not make legal conclusions from the database's presumed contents. Treat raw game data as third-party material and do not redistribute it without an established right to do so.
5. If a future downloader is approved, require a documented legitimate source, explicit user consent, timeout/retry behavior, temporary-file download, checksum or trusted signature, SQLite `PRAGMA integrity_check`, rollback on failure, and a clear opt-out. Do not silently overwrite a working database.
6. If a developer must share a permitted large database, use an approved file-distribution mechanism rather than ordinary Git history. GitHub warns above 50 MiB and blocks regular Git files above 100 MiB; its documentation specifically says Git is not designed for large SQL files.

Official reference: [About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), accessed 2026-11-23.

### One repository hygiene issue

The current reference tree contains a tracked `tests/__pycache__/test_extractor_prototype.cpython-312.pyc`, and the repository root had no `.gitignore` at the time of this audit. Adding `.gitignore` does not remove an already tracked file from Git history or the index. Ask the local coding agent to remove the tracked bytecode from the index in a separate, reviewed cleanup task; do not run a broad destructive clean command.

## 4. Secretary CLI: current behavior versus future ideas

The current `tools/secretary.py` implements only:

- `status`: prints a basic repository status summary.
- `verify-zips`: checks ZIP integrity in `archives/` and `reference_toolchains/archives/`.
- `ingest <file>`: counts lines, reports Markdown headers, and lists possible `LOCK` keywords.

It does **not** currently append an opinion to a dossier, synthesize a consensus, generate a prompt, create a decision record, or archive/delete files automatically. Any such behavior must be clearly marked as a future feature until code and tests exist.

Recommended priority:

1. Adopt the templates and evidence-led process now (no code changes required).
2. Later, if manual filing remains painful, add a small `record-opinion` command that copies a selected response into a dated file without trying to interpret it.
3. Only later consider synthesis automation. Keep AI judgment visible and reviewable; never silently turn AI opinions into approved decisions.

## 5. Stop conditions and quality gates

Stop and return to the owner when:

- The requested change touches files outside the approved scope.
- The current branch or working tree contains unexplained changes.
- A critical claim has no source or reproducible experiment.
- Two reviewers disagree on a high-impact fact and no safe experiment is available.
- A test cannot run because a dependency/fixture/platform is missing. Report the blocker; do not invent a pass.
- A proposed database operation would distribute or overwrite third-party data without a verified source and explicit approval.

A successful debate is not “all AIs agree”. It is “the owner understands the evidence, risks, unresolved questions, and the next reversible step”.
