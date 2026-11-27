# Historical Archive Policy

The archive preserves evidence and project history without making it part of every AI task's context.

## Required preservation

- Preserve the complete pre-ENV-01 `PROJECT_STATE.md` byte-for-byte as a dated archive.
- Preserve the complete pre-ENV-01 `AGENTS.md` byte-for-byte as a dated archive.
- Preserve S01–S11e implementation plans, closure reports, manual QA records, release-gate discussions, and Gemini/ChatGPT/Qwen reviews.
- Keep original dates, commit SHAs, test outputs, status labels and source citations.

## Lifecycle labels

- `ACTIVE`: still governs current work.
- `SUPERSEDED`: replaced by a newer decision; retain the old entry for provenance.
- `DEFERRED`: intentionally postponed, not resolved.
- `RETRACTED`: formally withdrawn because it was incorrect or unsupported.
- `HISTORICAL-REFERENCE`: completed record; useful only for provenance.

## Archive safety

- Do not silently delete or compress away canonical IDs.
- Do not edit historical closure reports to make them match current status. Add a correction/supersession note instead.
- Do not instruct agents to read this folder by default.
