# ENV-01 Migration Map — Required Output Template

Generate the final file at `docs/ai/ENV01_MIGRATION_MAP.md` from the exact local bytes at HEAD `ead65077a2a6cf3a664543cfb50f855268a29e2a`. This template is not the completed migration proof.

## Metadata

- Baseline HEAD:
- Branch:
- Original AGENTS bytes / lines / SHA-256:
- Original PROJECT_STATE bytes / lines / SHA-256:
- Archive byte/hash parity:
- AGENTS numbered sections found / mapped: must be 29 / 29.
- PROJECT_STATE headings levels 1–6 found / mapped: must match exactly.
- Canonical IDs/slugs extracted / mapped / intentionally historical:

## A. AGENTS.md — exhaustive 29-section retention map

One row per existing numbered section. Use exact heading text and source line ranges. Do not aggregate rows.

| # | Original heading | Source lines | Core invariant / meaning | New destination | Lifecycle | Retained/condensed rule | Validation |
|---:|---|---:|---|---|---|---|---|
| 1 | `Source of truth` | | | | | | |
| 2 | `Verification gate` | | | | | | |
| 3 | `Tkinter architecture` | | | | | | |
| 4 | `AST identity` | | | | | | |
| 5 | `Box model safety` | | | | | | |
| 6 | `Structural edits` | | | | | | |
| 7 | `Argument integrity` | | | | | | |
| 8 | `v2 text safety` | | | | | | |
| 9 | `Bundle save safety` | | | | | | |
| 10 | `XUAT dictionary safety` | | | | | | |
| 11 | `Central edit commit` | | | | | | |
| 12 | `Shortcut router` | | | | | | |
| 13 | `Undo and dirty state` | | | | | | |
| 14 | `Clipboard` | | | | | | |
| 15 | `Workers and search` | | | | | | |
| 16 | `Document lifecycle` | | | | | | |
| 17 | `Config and secrets` | | | | | | |
| 18 | `Network safety` | | | | | | |
| 19 | `NGUI single source` | | | | | | |
| 20 | `CSIF rules` | | | | | | |
| 21 | `UI safety` | | | | | | |
| 22 | `Startup` | | | | | | |
| 23 | `Disk and logging` | | | | | | |
| 24 | `Scope discipline` | | | | | | |
| 25 | `Delivery` | | | | | | |
| 26 | `Box clipboard contract` | | | | | | |
| 27 | `No broken intermediate state` | | | | | | |
| 28 | `Helpers before callers, and visible failures` | | | | | | |
| 29 | `Machine-confirmed release blockers` | | | | | | |

## B. PROJECT_STATE.md — exhaustive heading and ID lifecycle map

Parse every line matching `^#{1,6}\s+` in archived source. For every heading, compute exact source line and deterministic Markdown anchor/slug; maintain parent-heading stack. Also extract canonical IDs from each section (B1–B20, BUG-01..41, FEAT-01..14, HYG-01..08, DEF-01..10, NO-01..12, T-01..14, S-series, Q-series, issue slugs). If an ID occurs in body but not heading, list it on its section row or a companion ID row.

| Source line | Level | Exact heading text | Slug | Parent path | IDs/slugs in section | Destination | Lifecycle | Rationale / evidence |
|---:|---:|---|---|---|---|---|---|---|
| `<one row for every heading>` | | | | | | | | |

No `TBD`, `UNMAPPED`, missing source heading, or silent merge is allowed at acceptance. Multiple historical headings may point to the same archive, but each still needs its own row/lifecycle.

## C. Canonical ID reconciliation

| ID family / slug | Source location(s) | Active destination | Lifecycle | Evidence status | Historical archive pointer |
|---|---|---|---|---|---|
| T-01..T-14 | | `docs/project/OPEN_ISSUES.md` | | | |
| DEF-01..DEF-10 | | `docs/project/OPEN_ISSUES.md` | | | |
| B1..B20 | | archive/history | `HISTORICAL-REFERENCE` | | |
| BUG-01..BUG-41 | | resolved/history or active issue where applicable | | | |
| FEAT-01..FEAT-14 | | history/decisions as applicable | | | |
| HYG-01..HYG-08 | | history/decisions as applicable | | | |
| NO-01..NO-12 | | history/decisions as applicable | | | |
| MANUAL-PENDING / Q-series / S-series | | issue ledger or archive as applicable | | | |

## D. Reconciliation and STOP conditions

Record every source statement contradicted by newer authority (especially old `v1.5.0 ON HOLD` wording), its superseding decision, and archive pointer. Preserve exact old wording in verbatim archive. Do not change completed historical S15 to cancelled. Stop if any section or ID cannot be classified reliably.
