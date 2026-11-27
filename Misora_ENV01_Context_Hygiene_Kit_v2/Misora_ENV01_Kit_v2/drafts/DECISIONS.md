# Misora — Project Lead Decisions Ledger

**Purpose:** Current binding decisions. Older or conflicting wording remains in the verbatim archive and is marked superseded here.

| ID | Date | Lifecycle | Area | Binding decision |
|---|---|---|---|---|
| DEC-01A | 2026-11-28 | `ACTIVE` | Release authority | Current product version is `1.4.15`. The `v1.5.0` release campaign is `CANCELLED`; release status is `NOT RELEASED`; version promotion is `NOT AUTHORIZED`. Reconsideration requires a new explicit Project Lead-approved release charter and new gates. |
| DEC-01 | 2026-11-28 | `SUPERSEDED` | Historical release gate | Old wording “v1.5.0 STRICTLY ON HOLD” is superseded as current status by DEC-01A. Preserve it in the verbatim S11e `PROJECT_STATE.md` archive; do not display it as active authority. |
| DEC-02 | 2026-11-28 | `ACTIVE` | Documentation layers | Maintain lean Layer 0 (`AGENTS.md` <= 6 KiB, `PROJECT_STATE.md` <= 15 KiB), on-demand router/ledgers/index, and opt-in verbatim history. Never delete history or load archives by default. |
| DEC-03 | 2026-11-28 | `ACTIVE` | Q-17 tooltips | Single-box 350 ms `ToolTip` with concise `Name — Action (Shortcut)` across approved coverage tiers. Multi-stage timed tooltips remain rejected due to timer/lifecycle risk. |
| DEC-04 | 2026-11-28 | `ACTIVE` | Q-15 icons | Preserve verified Insert/Replace mappings and approved selection trio. Partial-state label must say “Some selected”, never “One selected”. Load-time DPI-aware scaling belongs in `assets/icon.py`; do not overwrite source PNGs. |
| DEC-05 | 2026-11-27 | `ACTIVE` | Module/interpreter paths | Canonical splash/icon modules are `assets/splash.py` and `assets/icon.py`; no root `splash.py`. Launcher pins `py -3.12` as documented baseline. Recheck local runtime rather than relying on machine-default Python. |
| DEC-06 | 2026-11-27 | `DEFERRED` | S11b2 XUAT sync | Recorded 2.899 s sync over 1,814 files / 243k lines was accepted under explicit Option A waiver despite >2 s target. Async disk IO remains deferred as T-12; do not claim 0 ms without measurement. |
| DEC-07 | 2026-11-27 | `ACTIVE` | DEF-01 sentinel | Preserve the single ASCII space empty-argument sentinel from S11c Option A. Core serialization change is not authorized without live-client proof and a new decision. |
| DEC-08 | 2026-11-28 | `ACTIVE` | Core/UI invariants | Preserve established AST, Box 0, lock, Preview, virtualized All Script, and bounded MTL widget invariants. Keep the native 50-digit-width/3+-line rule distinct from the reported 54d UI marker until source evidence reconciles them; verify exact current code before modification. |
| DEC-09 | 2026-11-28 | `DEFERRED` | DEF-10 decomposition | Modular decomposition of monolithic `misora.py` is unscheduled. Old “after v1.5.0 ships” timing is superseded because the v1.5.0 campaign is cancelled. A new architecture charter is required. |
| DEC-10 | 2026-11-28 | `ACTIVE` | Old S12 audit | Old S12 release audit is `PAUSED / SUPERSEDED`. Do not execute its plan or use its old release assumptions. A future release initiative must start with a new charter. |
| DEC-11 | 2026-11-28 | `ACTIVE` | S15 naming | Future S15 work proposal is `CANCELLED`; the completed historical S15 milestone remains `HISTORICAL-REFERENCE` and must not be deleted or renamed. |
| DEC-12 | 2026-11-28 | `ACTIVE` | ENV-01 boundary | ENV-01 is docs-only plus a stdlib, read-only AST symbol-index generator. Production code, tests, assets, config, backups, README, and dependency files are read-only. No version bump, commit, or push. |
| DEC-13 | 2026-11-28 | `ACTIVE` | Evidence/lifecycle model | Evidence and lifecycle labels are separate axes. A repeated report is not confirmation. T-01..T-04 remain REPORTED / NEEDS-REPRO until current-version evidence exists. |
| DEC-14 | 2026-11-28 | `ACTIVE` | Context loading | Layer 0 always contains AGENTS and Project State. Router selects only 1–3 relevant Layer 1 references. Source slices are Layer 2; archives are Layer 3 opt-in. |
| DEC-15 | 2026-11-28 | `ACTIVE` | Archive integrity | Old root AGENTS and Project State are copied as raw bytes before root replacement; archives are not decorated or normalized. Record SHA-256/byte parity separately; keep HISTORY_INDEX outside the verbatim files. |

## Decision status vocabulary

- `ACTIVE`: currently binding.
- `DEFERRED`: retained but unscheduled; not permission to start later automatically.
- `SUPERSEDED`: historical decision replaced by a newer ruling.
- `REJECTED`: explicit non-goal.
- `RETRACTED`: withdrawn factual claim, not a current issue.

## Reopening a decision

A deferred/cancelled/rejected item may be reconsidered only with an explicit Project Lead request, fresh scope/charter, baseline verification, trade-off analysis, acceptance criteria, and rollback plan. Do not infer authorization from backlog presence or old roadmap dates.
