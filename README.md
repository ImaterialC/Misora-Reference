# Misora-Reference

**Central reference, evidence library, and multi-AI review protocol for Misora Editor.**

Repository: https://github.com/ImaterialC/Misora-Reference  
Main application: https://github.com/ImaterialC/Misora-Editor

This repository is the shared source of truth for the owner and participating AI reviewers. It separates:
1. **Reference material** — original tools, source files, screenshots, and technical evidence.
2. **Project rules** — scope, workflow, evidence standards, and execution constraints.
3. **Phase instructions** — the exact task to perform in each review phase.
4. **Templates** — consistent report formats so outputs can be compared and audited.

## Start here

- [Quick copy-paste prompts](PROMPTS.md)
- [Phase 0 — access and integrity gate](Phase0.md)
- [Phase 1 — independent research](Phase1.md)
- [Phase 2 — cross-review and decision ledger](Phase2.md)
- [Phase 2.5 — exhaustive reconciliation gate](Phase2.5.md)
- [Phase 3 — implementation plan](Phase3.md)
- [Phase 4 — Antigravity execution feedback](Phase4.md)

## Core rules

- The owner controls phase transitions. An AI must stop at the end of its assigned phase.
- All AI-to-owner conversation is in **Bahasa Indonesia**.
- Technical findings, bug reports, shared council messages, and Antigravity prompts are written in **English**.
- Do not claim to have opened, executed, tested, or extracted anything unless that action actually happened.
- Separate confirmed facts, owner-reported behavior, hypotheses, proposals, and unknowns.
- Phase 1 is independent: do not read or use another AI's Phase 1 report or the owner's private findings.
- Phase 2.5 is a mandatory gate inside the Phase 2 review process.
- Do not begin implementation before the owner approves the Phase 3 plan.

## Current protected reference material

- `references/priconne-adv-tools/` — owner-provided Priconne ADV and related tooling reference. Treat it as read-only and preserve its contents.
- `references/assets/` — owner-provided screenshots and images. Preserve original files.
- Other reference files may be added later. Follow [Reference handling rules](docs/REPOSITORY_LAYOUT.md).

## Important scope distinction

The presence of a reference tool does not mean Misora Editor must reproduce every feature in it. The active Datamine discussion is limited to **game text data and MV/movie subtitle text**, subject to evidence. General-purpose asset extraction is not automatically in scope.

## How to use this repository

1. Give the relevant short prompt from [PROMPTS.md](PROMPTS.md) to each participating AI.
2. Each AI must read the linked phase document and its required project rules.
3. You collect and copy outputs between AI conversations manually.
4. Keep the canonical findings and decisions aligned with the templates in `templates/`.
5. Use Antigravity only after Phase 3 is agreed and approved.

See [Project mandate](docs/PROJECT_MANDATE.md) and [Workflow rules](docs/WORKFLOW_RULES.md) for the full operating agreement.
