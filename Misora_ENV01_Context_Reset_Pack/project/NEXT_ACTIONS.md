# Misora — What the Project Lead Should Do Next

## Phase 0 — Establish the real local baseline (no edits)

Run in the local Misora-Editor root and preserve the output:

```powershell
git branch --show-current
git rev-parse HEAD
git status --short
git log -5 --oneline
py -3.12 -c "from pathlib import Path; files=['AGENTS.md','PROJECT_STATE.md','misora.py']; [(print(f'{f}: exists={Path(f).exists()} bytes={Path(f).stat().st_size if Path(f).exists() else 0} lines={len(Path(f).read_text(encoding=\"utf-8\").splitlines()) if Path(f).exists() else 0}')) for f in files]"
```

Confirm the S11e commit and verify whether the working tree is clean. Do not push unless separately decided. Do not run destructive Git commands.

## Phase 1 — Approve ENV-01 scope

1. Treat this package as a proposal, not as permission to edit.
2. Decide whether `ENV-01` is strictly documentation/context layering or also includes a symbol-index generator.
3. Lock the exact allowed files. Recommended first ENV-01 scope: root `AGENTS.md`, root `PROJECT_STATE.md`, `docs/ai/*`, `docs/project/*`, `docs/history/*`, and a stdlib-only symbol index tool only if explicitly approved.
4. Explicitly forbid product source, tests, assets, config, backups and version changes.
5. Confirm how the new council decision refers to “S15”; preserve the old completed S15 history unless it is definitely a different planned session.

## Phase 2 — Audit before summarizing

1. Inventory the entire Project State by headings, tables, IDs, dates and cross-links.
2. Inventory all requirements/defects/decisions in AGENTS, Project State, wishlist, changelog, S11 closure docs and release plans.
3. Build a migration matrix: original section/ID → new location → lifecycle label → evidence/provenance.
4. Reconcile current HEAD/version/test baseline and all recent S11e changes locally.
5. Identify contradictions (especially S12 old v1.4.10 instructions, historical S15, release target, and pending Windows QA).
6. Have one agent draft; independent reviewers audit omissions and meaning changes. Do not let multiple agents edit the same root file concurrently.

## Phase 3 — Migrate safely

1. Preserve the complete old Project State and old Agent rules in a dated history archive before replacing root docs.
2. Write the compact Agent rules and state dashboard.
3. Add the context router and active decision/issue registers.
4. Generate a `misora.py` symbol index from the verified local HEAD. Do not split source modules in this phase.
5. Search every old canonical ID and decision to prove it has a new location or an explicit retraction/supersession.
6. Compare old/new root docs and review line-by-line for lost constraints.

## Phase 4 — Validate the new environment

Give each AI the same small read-only task using only Layer 0 + router, such as: “Explain current release status, top three open issues, exact base HEAD, and which files are permitted for an ENV-01 documentation task.”

Success means the agents agree on:
- current version/HEAD and push status (after local verification),
- v1.5.0 and S12 status,
- active ENV-01 scope,
- T-01..T-14 classification,
- source/test evidence limits,
- prohibited edits and required approvals.

Measure prompt tokens and time-to-correct-source, but prioritize agreement and factual accuracy over a target token count.

## Phase 5 — Post-ENV-01 triage

Recommended triage order: T-01, T-03, T-04, T-02, T-05/T-06, T-07, T-08..T-10, then T-11..T-14 as separate tracks. Each issue requires a reproduction/evidence package and a separately approved implementation scope.

## Do not do yet

- Do not start S12 or the old v1.5.0 release gate.
- Do not promote `__version__`.
- Do not implement all T-01..T-14 in one mega-session.
- Do not split `misora.py` yet.
- Do not rewrite or delete old milestone history.
- Do not push the local S11e commit merely as part of ENV-01 unless the Project Lead explicitly wants that.
