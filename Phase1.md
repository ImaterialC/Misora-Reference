# Phase 1 — Independent Technical Research

**Purpose:** each AI independently investigates the agreed project scope before seeing other AIs' conclusions or the owner's private findings.

## Required reading

Read:
- `README.md`
- `AGENTS.md`
- `docs/PROJECT_MANDATE.md`
- `docs/WORKFLOW_RULES.md`
- `docs/RESEARCH_AND_EVIDENCE.md`
- `docs/CURRENT_SESSION.md`
- `docs/REPOSITORY_LAYOUT.md`
- `templates/PHASE1_INDEPENDENT_REPORT.md`

Proceed only after the owner has accepted the Phase 0 access report for your AI surface.

## Independence rules

- Work from primary evidence: current repository files, source code, tests, logs, reproducible behavior, and authoritative external documentation.
- Do not request, search for, or rely on another AI's Phase 1 report.
- Do not rely on the owner's private/manual findings unless the owner explicitly releases them in Phase 2.
- Ignore previous assistant claims when they are not independently verified against current evidence.
- Do not copy another model's diagnosis or proposed architecture.
- You may ask the owner essential questions that block accurate investigation. Batch only truly necessary questions; do not ask speculative preference questions.
- Do not prematurely reach consensus. Your independent report is your own technical assessment.

## Investigation objectives

Use `docs/CURRENT_SESSION.md` as the current scope. At a minimum:

1. Inspect the current Misora Editor architecture and identify its actual implemented capabilities.
2. Audit existing bugs, regressions, incomplete workflows, and missing core features relevant to the current owner goal.
3. Map how the existing Priconne ADV reference tool works, but do not assume that it should be copied wholesale.
4. Evaluate the proposed Datamine scope: text data and MV/movie subtitle text only.
5. Identify likely data sources and formats only when supported by actual files, code, or reliable documentation. Candidate sources may include master.db records, Unity TextAsset/ADV content, subtitle-bearing Unity objects, manifests, and metadata mappings; none is confirmed merely by being listed here.
6. Distinguish subtitle metadata from the video/audio payload. Do not assume that a `.usm` movie file itself contains the subtitle text.
7. Identify architectural, compatibility, dependency, licensing, data-integrity, and workflow risks.

## Technical finding format

Use the format in `docs/RESEARCH_AND_EVIDENCE.md`. Write issue blocks and the report in English. Include:
- Stable provisional finding ID.
- Category: BUG, REGRESSION, MISSING_CORE_FEATURE, FEATURE_PROPOSAL, RISK, CONSTRAINT, or OPEN_QUESTION.
- Severity and confidence.
- Exact evidence and source location.
- Reproduction steps when applicable.
- Expected versus actual behavior for bugs.
- Impact and dependencies.
- What remains unverified.

Do not mix a confirmed defect with a future feature suggestion. A proposal is not a bug.

## Required deliverable

Produce a complete report using `templates/PHASE1_INDEPENDENT_REPORT.md`. Include the strongest findings first, source map, unresolved questions, and a clearly separated list of proposals.

Communicate your explanation to the owner in Bahasa Indonesia. The technical report itself must be in English.

## Stop condition

Stop after submitting the independent report and essential blocking questions. Do not cross-review other AIs, build the council ledger, decide implementation order, or write Antigravity implementation prompts. Wait for the owner to begin Phase 2.
