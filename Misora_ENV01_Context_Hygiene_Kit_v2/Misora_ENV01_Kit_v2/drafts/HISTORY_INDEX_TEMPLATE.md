# Misora — History Index (Template)

This is a separate searchable index. **Do not add a header, TOC, annotation, newline, or edit to the verbatim archived files themselves.** Archive files must remain byte-identical to their source files at the pinned pre-ENV-01 HEAD.

## Archive provenance

| Source path | Source HEAD | Source bytes | Source SHA-256 | Archive path | Archive bytes | Archive SHA-256 | Byte-equal |
|---|---|---:|---|---|---:|---|---|
| `AGENTS.md` | `<exact source HEAD>` | `<bytes>` | `<sha256>` | `docs/archive/AGENTS_v1.4_PRE_ENV01.md` | `<bytes>` | `<sha256>` | `YES/NO` |
| `PROJECT_STATE.md` | `<exact source HEAD>` | `<bytes>` | `<sha256>` | `docs/archive/PROJECT_STATE_v1.4_PRE_ENV01.md` | `<bytes>` | `<sha256>` | `YES/NO` |

Archive proof must be established before root replacement. `ARCHIVE_SHA256SUMS.txt` contains the two archived-file hashes in SHA256 manifest format. After replacement, re-verify archive files against that manifest; never compare archives to the rewritten root files.

## Heading / canonical-ID index

Create one row for **every** Markdown heading level 1–6 from archived `PROJECT_STATE.md`. Preserve source order. Include IDs nested in each section, including B1–B20, BUG, FEAT, HYG, DEF, NO, T, S-series, Q-series, and issue slugs when present.

| Source line | Heading level | Original heading | Computed slug | Parent heading path | Canonical IDs/slugs | Lifecycle | Destination / current home | Archive pointer | Notes |
|---:|---:|---|---|---|---|---|---|---|---|
| `<line>` | `<1–6>` | `<exact text>` | `<anchor>` | `<parent chain>` | `<IDs>` | `ACTIVE / SUPERSEDED / DEFERRED / RETRACTED / HISTORICAL-REFERENCE` | `<target doc/section>` | `PROJECT_STATE_v1.4_PRE_ENV01.md#<slug>` | `<rationale>` |

Also index all 29 numbered AGENTS sections in the migration map; do not duplicate the old rule text here.

## Suggested grouping guide

- Current S11e version/test facts and present next action: `PROJECT_STATE.md`.
- T-01..T-14, MANUAL-PENDING, fixture/test debt, DEF-01..DEF-10: `docs/project/OPEN_ISSUES.md`.
- Binding decisions, release status, cancellation/supersession, architectural decisions: `docs/project/DECISIONS.md` and concise rules in `AGENTS.md`.
- Task routing: `docs/ai/CONTEXT_ROUTER.md`.
- Source navigation: `docs/architecture/MISORA_SYMBOL_INDEX.md`.
- Completed milestones, historical baselines, B1–B20, resolved tables, retracted claims, old roadmap/audit details: verbatim archive + this index as `HISTORICAL-REFERENCE`, unless a row is explicitly `SUPERSEDED`, `RETRACTED`, or `DEFERRED`.

Do not mark old material deleted. Summaries are not substitutes for preserving source bytes.
