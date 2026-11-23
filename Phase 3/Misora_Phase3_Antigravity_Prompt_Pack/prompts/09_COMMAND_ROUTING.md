# ANTIGRAVITY COMMAND ROUTING — MISORA PHASE 3

## 1. First-time setup

Run these as separate commands if the command exists in your App/CLI:

```text
/antigravity-guide
```

Use to make Antigravity check its current official documentation. Then:

```text
/agy-customizations
```

Use before authoring workspace Rules, Skills, hooks, or custom agents. Do not assume the customizations reference has loaded just because a prompt mentions it.

## 2. Main project orchestrator

```text
/teamwork
```

Use `prompts/00_PHASE3_TEAMWORK_START.md`. Teamwork is the primary choice for a long-running, multi-milestone project. Review its prompt artifact before approval. Teamwork's own project directory is isolated; verify how the local repository snapshot and dirty files are handled.

## 3. Commands by job shape

### `/plan`
Use for one bounded milestone or a re-plan. Require a reviewable plan, explicit scope, tests, and pause before edits. Do not use `/grill-me` to reopen decisions already locked in the ledger.

### `/boost`
Use for one tightly coupled high-risk defect where iterative challenge is valuable. Good candidates:
- BUG-02 AST kind-conversion/box identity.
- BUG-07 transactional sparse CSIF.
- BUG-14 batch cancellation/Undo lifecycle.
- BUG-27 asynchronous MTL stale-result/thread ownership.
- BUG-33 DPAPI failure behavior.

Use this form:

```text
/boost Investigate and fix [ONE canonical BUG-ID] from the locked Misora ledger. First reproduce the defect, preserve the exact ledger invariants, add a failing regression test, implement the smallest root-cause fix, and have the challenge agent attempt to break it. Report exact commands and real output. Do not touch unrelated canonical IDs.
```

### `/swarm`
Use for broad tasks separable by file/package when you are NOT already using Teamwork for that same task. Assign non-overlapping file ownership. Always include an independent verifier using a different available model if supported. Do not have two workers edit `misora.py` simultaneously.

### `/run-workflow`
Use for structured, repeatable, mostly read-only fan-out:
- map canonical ledger IDs to source paths/tests;
- inspect changed files and report regression risks;
- generate JSON verdicts with exact evidence;
- run independent read-only test discovery.
Ask the workflow to save its Python orchestration script (e.g. `scripts/phase3_ledger_audit.py`) and a machine-readable result. Do not create automated parallel edits to overlapping files.

### `/goal`
Use only for one bounded objective with command-verifiable Done criteria, such as a final acceptance audit or one small independent verification pass. Never give it “finish all Phase 3” without explicit stop gates. There is no iteration cap.

### `/compact`
Use after a completed milestone. It must be the first token in the message, for example:

```text
/compact Preserve the pinned target HEAD, locked ledger decisions, completed canonical IDs, exact test commands/results, blocked fixture requirements, changed files, and remaining milestones. Continue with Milestone C only; do not reopen completed gates.
```

### `/btw`
Use for a tangential read-only question that should not pollute the main implementation context. Never use it to make a project decision or change code.

### `/learn`
Use only after a repeated mistake has been corrected and the Project Lead approves turning the correction into a persistent rule or skill. Review the proposed customization before installing it.

## 4. Commands intentionally not forced

- `/browser`: Misora is a Tkinter desktop application. Browser subagent testing is not a valid replacement for running the Windows desktop app. Use only for an actual browser-based website/documentation task.
- `/schedule` and `/automation`: not needed for code implementation. Use only for a user-requested reminder or scheduled check.
- `/generative_ui` and `/mcp-app-development`: unrelated to this code stabilization cycle.
- `/grill-me`: do not reopen locked product decisions. The main prompt allows one question only for an essential local fact that cannot be discovered safely.
- `/clear` or `/new`: avoid until a useful `/compact` checkpoint has been created.

## 5. CLI monitoring (only if using `agy`)

- `/agents`: inspect subagents and pending approvals.
- `/tasks`: inspect background tasks.
- `/context`: inspect token/context usage.
- `/diff`: inspect current changes.
- `/model` and `/effort`: inspect/select available model and effort; do not invent model IDs.
- `/permissions`: check tool permissions before shell or file operations.
- `/usage`: inspect quota usage.
- `/rewind`: recover from an unwanted recent interaction when appropriate; prefer reviewing actual Git diffs before discarding file edits.
- `/fork`: explore a separate approach without overwriting the accepted plan.

Avoid headless `agy -p` for the main Phase 3 implementation because it bypasses the interactive artifact/review workflow that this project needs.
