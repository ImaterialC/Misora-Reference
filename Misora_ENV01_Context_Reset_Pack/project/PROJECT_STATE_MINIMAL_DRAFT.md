# Misora — Current Project State (ENV-01 compact draft)

> Proposed replacement for the root `PROJECT_STATE.md`. This is a snapshot, not a historical ledger. Update only after checking the local repository.

## Current identity

- Product: Misora: Story Editor (PriconneRe:TL).
- Editor repository: `ImaterialC/Misora-Editor`.
- Reference repository: `ImaterialC/Misora-Reference`.
- Last reported version: `1.4.15` (S11e).
- Last reported local commit: `ead65077a2a6cf3a664543cfb50f855268a29e2a`.
- Push status: Project Lead reports not pushed.
- Post-commit working-tree cleanliness: **NOT VERIFIED**; run `git status --short` locally.

## Current strategic decision

- Council decision: cancel/pause the current `v1.5.0` release effort and the planned S15 work; do not continue S12 under the old release plan.
- Immediate priority: **ENV-01 — audit and layer the agent/project documentation and context-loading workflow**.
- Next priority: triage T-01..T-14, verify evidence, then authorize specific fixes/design sessions.
- `v1.5.0`: **HOLD / NOT AUTHORIZED**. No version promotion, release packaging, or release declaration.
- Historical caution: the old Project State contains an earlier completed milestone also called S15. Do not rewrite that historical entry until Project Lead clarifies whether the cancelled S15 is a newer planned work item or a separate session label.

## Latest reported test baseline (S11e)

| Metric | Count |
|---|---:|
| Discovered/executed | 475 |
| PASS | 432 |
| SKIP | 35 |
| Pre-existing FAIL | 6 |
| Pre-existing ERROR | 2 |
| New S11e regressions reported | 0 |

Full single-process discovery completed in the S11e report. This result is Project-Lead/Gemini-reported, not independently rerun here. Re-establish the baseline before future code changes.

### Known baseline failures/errors

- `test_phase3_performance_config::test_05` — local config isolation/hygiene.
- `test_s9c_workspace_safety::test_04` — default config template/absence-policy test.
- `test_v15_s01_stability_remediation::test_probe_8` — hardcoded version expectation (`1.4.1`).
- `test_s8b2_memory_guards` — three fixture-dependent failures and two fixture-dependent errors because proprietary `storydata_1001005.unity3d` is absent.

Do not weaken tests or use the user's local configuration to make these pass.

## Current open work

1. ENV-01 documentation/context restructuring — proposed; requires Project Lead approval and source-preserving migration.
2. Bug/UI triage T-01..T-14 — see `triage/MASTER_BACKLOG_T01_T14.md`.
3. BUG-UI-EMPTY-STATE-01 — Windows-observed P1 report; root cause not independently established.
4. Revalidate Ribbon Cut and Paste Box manual blockers from `AGENTS.md` §29.
5. DEF-01 sentinel leakage remains deferred; no core fix authorized.

## Current S11e checkpoint

- S11e local commit reported as `ead65077a2a6cf3a664543cfb50f855268a29e2a`.
- 13 files reported committed: nine S11e source/test/doc files plus four icons.
- No push shown in the supplied terminal transcript.
- Manual S11e QA reported PASS for Q-03, Q-05, Q-13..Q-17, with BUG-UI-EMPTY-STATE-01 subsequently observed.
- This state must be refreshed against local Git before any work begins.

## Deferred / explicitly not authorized

- DEF-01 binary empty-argument sentinel behavior.
- Async XUAT disk I/O (S11b2 Option A accepted 2.899 s; async design deferred to a separate track).
- S12 Final Release Audit and v1.5.0 promotion.
- S15 as described by the latest council decision (clarify identity against the historical S15 entry).
- T-11..T-14 large feature/infrastructure proposals until separately designed and approved.

## Working rule

The next authorized task is ENV-01 planning/audit only. Do not edit product source, change version, commit, push, or delete historical records under this state draft. Wait for explicit Project Lead authorization for the exact file scope.
