# Misora — Project State (Layer 0 Dashboard)

**Last reconciled:** 2026-11-28 (ENV-01 target draft; re-verify at implementation)  
**Repository:** `ImaterialC/Misora-Editor` · **Branch:** `main`  
**Baseline:** `ead65077a2a6cf3a664543cfb50f855268a29e2a` (S11e)  
**Current product version:** `1.4.15` (root `__init__.py` is authoritative)

## 1. Release and roadmap authority

- **v1.5.0 release campaign: CANCELLED.** Release status: **NOT RELEASED**. Version promotion: **NOT AUTHORIZED**.
- Old S12 release audit: **PAUSED / SUPERSEDED**. Do not execute its historical plan as-is.
- Future S15 work proposal: **CANCELLED**. The completed historical milestone `S15 Select Box Both Views + Reserved Lock Slot, Collapsible Left Drawer, Empty State & Batched Multi-Open` (2026-11-25) remains **HISTORICAL-REFERENCE**.
- ENV-01 is the current authorized documentation/context-hygiene task. It does not authorize product changes, defect fixes, release actions, commits, or pushes.

## 2. S11e verification baseline (recorded; not rerun by ENV-01)

The S11e project record reports `countTestCases() == 475` and completed monolithic discovery:

| Result | Count |
|---|---:|
| Total tests | 475 |
| PASS | 432 |
| SKIP | 35 |
| FAIL | 6 |
| ERROR | 2 |
| New S11e regressions reported | 0 |

**475 is the total discovered/executed count, not 475 passing tests.** The 6 failures comprise 3 fixture-related failures and 3 non-fixture hygiene failures. The 2 errors are fixture-related in `test_s8b2_memory_guards`. Thirty-five tests were skipped because the proprietary `storydata_1001005.unity3d` fixture was unavailable in the recorded environment. Recheck local conditions before relying on these counts.

Three non-fixture test-hygiene failures recorded:
1. `tests/test_phase3_performance_config.py::test_05` — local `misora_config.json` isolation hygiene.
2. `tests/test_s9c_workspace_safety.py::test_04` — default config template contract hygiene.
3. `tests/test_v15_s01_stability_remediation.py::test_probe_8` — hard-coded expected version `1.4.1` conflicts with `1.4.15`.

Fixture-related debt: `tests/test_s8b2_memory_guards.py::test_01..test_05` depend on missing `storydata_1001005.unity3d` (recorded as 3 FAIL + 2 ERROR); 35 fixture-dependent skips are also recorded. Do not invent fixture outcomes or weaken tests.

## 3. Current issue and QA posture

- T-01..T-04 are reports requiring current-version reproduction/source inspection; they are not confirmed defects merely because they appear in the backlog.
- T-05..T-10 are configuration/UX/UI proposals requiring triage or design sign-off.
- T-11..T-14 are future/unscheduled proposals or deferred work; none is authorized by this dashboard.
- MANUAL-PENDING/revalidation items are tracked in `docs/project/OPEN_ISSUES.md`, including legacy Ribbon Cut/Paste Box checks, S11c/S11d undo/redo and MTL/Box 0 checks, DPI/snapped layout, and Import from XUAT smoke test.
- `Tcl_AsyncDelete` cross-test teardown is a watch item: seen in earlier S11c/S11d runs, while S11e monolithic discovery completed. Do not report it as a current confirmed failure without reproduction.
- DEF-01 single-space sentinel is an accepted/deferred compatibility limitation; do not change without a new decision.

## 4. ENV-01 target state

Keep Layer 0 lean: this file plus `AGENTS.md` only. Route deeper questions through `docs/ai/CONTEXT_ROUTER.md`. Detailed issue evidence, decisions, migration proof, symbol navigation, and history belong in on-demand documents. Before replacement, copy old root docs as raw bytes and verify SHA-256 plus byte equality; never add a header/TOC or normalize archives.

For ENV-01, these paths are absolutely READ-ONLY: `__init__.py`, `misora.py`, `core/**`, `assets/**`, `tests/**`, `misora.bat`, `requirements.txt`, `misora_config.json`, `backups/**`, and `README.md`. No dependency, release, commit, tag, or push operation is authorized.

Hard size caps: `AGENTS.md` <= 6 KiB (6144 bytes); `PROJECT_STATE.md` <= 15 KiB (15360 bytes). Preferred targets: AGENTS 3–5 KiB; Project State 8–10 KiB. Byte counts, not token estimates, are the acceptance measure.

## 5. Next authorized action

1. Verify local `main` at exact S11e HEAD and clean working tree.
2. Run Antigravity `/plan` in read-only mode; it must STOP before edits.
3. Obtain independent reviews from Gemini, GPT-6, and Qwen.
4. Execute only after explicit Project Lead Proceed authorization.
5. Verify all 11 ENV-01 acceptance gates and the four-AI validation experiment.

Any baseline mismatch, target collision, archive hash mismatch, incomplete migration row, test count other than 475, or request to edit a forbidden path is a STOP condition.
