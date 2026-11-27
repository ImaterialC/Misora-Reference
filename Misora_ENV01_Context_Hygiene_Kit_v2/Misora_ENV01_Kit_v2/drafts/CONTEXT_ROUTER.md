# Misora — Context Router

This file routes from the two mandatory Layer 0 documents to the smallest relevant context. Do not load the whole repository history or issue ledger by default.

## Context layers

| Layer | Load rule | Contents |
|---|---|---|
| **0 — Always** | Every task | `AGENTS.md`, `PROJECT_STATE.md` |
| **1 — Task context** | Read this router, then choose only 1–3 relevant documents | `docs/project/OPEN_ISSUES.md`, `docs/project/DECISIONS.md`, `docs/ai/ENV01_MIGRATION_MAP.md`, `docs/architecture/MISORA_SYMBOL_INDEX.md` |
| **2 — Source evidence** | After identifying the precise question | Focused slices of actual source and relevant tests; inspect/reproduce as authorized |
| **3 — History** | Opt-in for chronology, prior reasoning, or disputed provenance | `docs/archive/HISTORY_INDEX.md`, verbatim archive files, explicitly superseded plans |

Never read all Layer 1 documents automatically. A normal code task should usually need Router + one issue/decision reference, then a few source/test files. Layer 3 is not part of routine context.

## Task-to-source routing

| User task | Layer 1 references | Layer 2 evidence | Layer 3? |
|---|---|---|---|
| Current version, release authority, S12/S15 status | `PROJECT_STATE.md` (Layer 0), `docs/project/DECISIONS.md` | `__init__.py` only to verify runtime version; no release code unless separately authorized | Only if historical rationale requested |
| Reported defect T-01..T-04 | `docs/project/OPEN_ISSUES.md` | Relevant GUI/source symbols and narrow tests via symbol index; current-version reproduction | No, unless provenance disputed |
| T-05..T-10 UI/config proposal | `docs/project/OPEN_ISSUES.md`, `docs/project/DECISIONS.md` | Relevant GUI/config code, UX behavior, test coverage; obtain design sign-off before implementation | No |
| T-11..T-14 / Track B proposals | `docs/project/OPEN_ISSUES.md`, `docs/project/DECISIONS.md` | Relevant source only after new scope/charter is approved | No |
| DEF-01..DEF-10 / architecture limitation | `docs/project/OPEN_ISSUES.md`, `docs/project/DECISIONS.md` | Exact core/module/test slices; verify missing canonical references before interpreting | Only to resolve old decisions/provenance |
| Test baseline or fixture issue | `PROJECT_STATE.md`, `docs/project/OPEN_ISSUES.md` | Actual test files, fixture path, Python/dependency environment; distinguish discovery from execution | No |
| Permanent coding invariant | `AGENTS.md`, then relevant `docs/project/DECISIONS.md` | Source + tests for the touched invariant | No |
| ENV-01 migration/audit | `docs/ai/ENV01_MIGRATION_MAP.md`, `docs/project/DECISIONS.md` | Original root docs and generated hashes; exact heading/ID extraction | Yes, for byte provenance only |
| Symbol/function lookup | `docs/architecture/MISORA_SYMBOL_INDEX.md` | Open actual source around symbol and inspect helpers/callers/tests where required | No |
| Historical milestone or why an old plan was paused | `docs/archive/HISTORY_INDEX.md` first | Only relevant archived section/plan | Yes |

## Source navigation policy

- `MISORA_SYMBOL_INDEX.md` is generated from AST and is a locator only. It can show declared functions/classes/methods and line numbers; it does not prove use, deadness, safety, or correctness.
- Verify claims against current source and tests. The index may become stale; check its embedded HEAD and per-file SHA-256 before relying on it.
- Do not guess source symbols from a bug title. If the index/source does not establish a symbol, say `UNKNOWN` and search narrowly.
- Keep source reads narrow: target method, direct helpers/callers if necessary, and smallest relevant tests.

## Evidence and response contract

For every nontrivial technical answer, identify:
1. baseline / branch / version when relevant;
2. evidence label: `REPORTED`, `SOURCE-OBSERVED`, `CONFIRMED`, `NEEDS-REPRO`, `PROPOSAL`, or `DEFERRED`;
3. lifecycle separately: `ACTIVE`, `SUPERSEDED`, `DEFERRED`, `RETRACTED`, or `HISTORICAL-REFERENCE`;
4. exact file/symbol/test evidence and what was not checked;
5. scope/risks and actual tests run/output (never infer);
6. next safe action and STOP conditions.

The router does not authorize edits. Planning is read-only; implementation requires an independently reviewed plan and explicit Project Lead authorization.
