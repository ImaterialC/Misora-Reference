# Misora — Open Issues, Test Debt & Manual QA Ledger

**Baseline context:** S11e `v1.4.15`, HEAD `ead65077a2a6cf3a664543cfb50f855268a29e2a`  
**Purpose:** Preserve reports, proposals, test debt, fixture blockers, manual QA, and deferred limitations without conflating them.

## Status model — separate axes

**Evidence labels:** `REPORTED` (not independently reproduced); `SOURCE-OBSERVED` (seen in source/recorded evidence, runtime may be unverified); `CONFIRMED` (current reproducible or direct verified evidence); `NEEDS-REPRO` (requires a current-version repro); `PROPOSAL` (suggested feature/design, not a proven defect); `DEFERRED` (intentionally unscheduled or not implemented).

**Lifecycle labels:** `ACTIVE`, `SUPERSEDED`, `DEFERRED`, `RETRACTED`, `HISTORICAL-REFERENCE`.

An item may carry multiple evidence notes, e.g. `REPORTED + NEEDS-REPRO`. Do not promote evidence based on repetition in documents. Lifecycle is not an evidence grade.

## A. T-01..T-04 — reported behavior requiring reproduction

| ID | Legacy ref | Evidence | Lifecycle | Description / closure criteria |
|---|---|---|---|---|
| **T-01** | `BUG-UI-EMPTY-STATE-01` | `REPORTED` + `NEEDS-REPRO` | `ACTIVE` | Report: purple Open Files empty-state button/caption remains below `txt_dialogue` while bundles are open, obscuring lower border / `clean_scroll_x`. Reproduce on v1.4.15 with 0/1/2 open docs; open/close one/last doc; switch Dialogue/All Script; check `_deferred_restore()`. Inspect `empty_state_frame.winfo_manager()` as well as `winfo_ismapped()`, parent mapping, and `_update_empty_state_visibility()` lifecycle. Root cause is not established. |
| **T-02** | `u-08` | `REPORTED` + `NEEDS-REPRO` | `ACTIVE` | Report: Next-button tooltip displays stale `50x3` instead of `54d x 3`. Verify current runtime text and source of the tooltip. |
| **T-03** | `u-05` | `REPORTED` + `NEEDS-REPRO` | `ACTIVE` | Report: Pin in All Script appears to turn speaker jumps into multi-select. Reproduce; distinguish active box, `_selected_boxes`, and selection anchor. Do not assume root cause. |
| **T-04** | `u-02` | `REPORTED` + `NEEDS-REPRO` | `ACTIVE` | Report: red overflow marker may not cover line 4+ (`>3L`) as well as horizontal `>54d`. Verify the current contract and visual behavior. Do not confuse raw newline count with visual wrapping; retain hard-linebreak and rendered-width rules. |

T-01..T-04 are **not CONFIRMED** at ledger creation. Confirmation requires current-version reproduction or direct source+runtime evidence with exact build, steps, and result.

## B. T-05..T-10 — proposals requiring triage/design sign-off

| ID | Legacy ref | Evidence | Lifecycle | Summary / gate |
|---|---|---|---|---|
| **T-05** | `u-01` | `PROPOSAL` | `ACTIVE` | Path/naming redesign: rename Project Folder to Game Folder; expose separate Game Folder, RedirectedResources folder, and XUnity.AutoTranslator Text Folder paths; avoid hardcoded framework assumptions. BepInEx/Daring Tact are possible frameworks; XUnity.AutoTranslator is a plugin, not a framework. Validate auto-detection and multi-language/multi-framework behavior first. |
| **T-06** | `u-03a` | `PROPOSAL` | `ACTIVE` | Remember separate default Save directories for `.misora` project save vs Save/Patch Bundle (`Ctrl+Shift+S`). Confirm UX and persistence semantics. |
| **T-07** | `u-07` | `PROPOSAL` | `ACTIVE` | Extend lazy 350 ms tooltips to selected informative labels/panels: voice cue filename, segment count, Opened Files drawer, Box count, Customize/NGUI Glossary, Search Results, Import from XUAT. Avoid noisy blanket coverage. |
| **T-08** | `u-11` | `PROPOSAL` | `ACTIVE` | Ribbon redesign: stabilize Prev/Next positions; evaluate four rows (Info / View Nav / MTL-AI-Edit / NGUI), including select/lock/count/title/subtitle/char-line/selection controls. View-type label default OFF; Title/Subtitle visibility is coupled (turning Title off also hides Subtitle, Title-only remains allowed). Consider removing ribbon Select Box toggle because card checkboxes remain available and can be hidden in View. Measure impact at 768p / 125% DPI. Requires approved mockup and usability sign-off. |
| **T-09** | `u-12` | `PROPOSAL` | `ACTIVE` | Explicit Insert Box / Replace Box / tri-state Select All Box controls. Check overlap with shipped S11e controls before suggesting duplicates. |
| **T-10** | `u-06` | `PROPOSAL` | `ACTIVE` | Selected-box card-level visual highlight in All Script, alongside active-box highlight; measure virtualized card-pool impact. |

## C. T-11..T-14 — future / unscheduled proposals

| ID | Legacy ref | Evidence | Lifecycle | Summary / constraint |
|---|---|---|---|---|
| **T-11** | `u-03b` | `PROPOSAL` + `DEFERRED` | `DEFERRED` | Read-only Original Data panel beside Raw Commands, preserving original speaker/actor/text as durable reference across save/reopen. Not yet an approved “Master Undo” design. Requires identity, provenance, snapshot persistence, and restore semantics. |
| **T-12** | `U-04` / S11b2 | `SOURCE-OBSERVED` + `DEFERRED` | `DEFERRED` | XUnity.AutoTranslator sync disk scan/write was recorded at ~2.899 s on 1,814 files / 243k lines and accepted via S11b2 Option A waiver. Async worker IO is deferred; do not promise 0 ms without measurement. Any worker must obey Tk/main-thread and immutable-snapshot rules. |
| **T-13** | `u-10` | `PROPOSAL` + `DEFERRED` | `DEFERRED` | Human-readable XUAT-format backup/revert with provenance, source attribution, encoding/fingerprint, path mapping, preview, and selective re-import. Do not confuse datamine and plugin-generated backups. |
| **T-14** | `u-09` / `u-13` | `PROPOSAL` + `DEFERRED` | `DEFERRED` | GitHub Actions release `.zip` + `.exe` pipeline. Deferred because current v1.5.0 campaign is cancelled. Reconsider only with a new release charter covering build, signing, licensing, AV, reproducibility, and rollback. |

## D. Revalidation and MANUAL-PENDING QA

### D.1 Legacy release-blocker observations — current status must be rechecked

- **AGENTS.md §29 Ribbon Cut:** legacy user verification on Windows v1.4.0 reported Ribbon Cut reverted after navigation. Current v1.4.15 status: `NEEDS-REPRO`; explicit manual Windows test required.
- **AGENTS.md §29 Paste Box:** legacy user verification on Windows v1.4.0 reported Paste Box did nothing in Dialogue and All Script. Current v1.4.15 status: `NEEDS-REPRO`; test both views and Insert/Replace semantics.
- **Q-04.1.2 / Q-04.1.3:** `NEEDS-REPRO`; Project Lead reproduction confirmation needed if still applicable.
- **T-01:** reproduce the current empty-state behavior using the sequence in section A.

### D.2 MANUAL-PENDING

- S11c: Ctrl+Z Undo after Import from XUAT following a Quick Edit change.
- S11d Q-08: post-import Synopsis Undo/Redo.
- S11d Q-11: DeepL Globe check on the DeepL card and while Box 0 is active.
- Windows DPI and snapped half-screen layout (`BUG-39` / `FEAT-04`) current-build confirmation.
- Import from XUAT smoke test on `BepInEx\Translation\en\Text` or the approved equivalent real local layout.
- Ribbon Cut after navigation and Paste Box in both Dialogue and All Script views.
- Q-04.1.2 / Q-04.1.3 Project Lead reproduction confirmation.

Manual results must record exact version, OS/DPI, steps, expected vs actual, fixture/path context, and operator confirmation. Unit tests alone do not close manual QA.

## E. Automated test hygiene debt — recorded S11e baseline

**Three non-fixture failures recorded:**
1. `tests/test_phase3_performance_config.py::test_05` — local `misora_config.json` isolation hygiene.
2. `tests/test_s9c_workspace_safety.py::test_04` — default config template contract hygiene.
3. `tests/test_v15_s01_stability_remediation.py::test_probe_8` — hard-coded expected version `1.4.1` vs current `1.4.15`.

**Fixture-dependent failures/errors and skips:**
- Missing proprietary `storydata_1001005.unity3d` was recorded as causing 3 failures + 2 errors in `tests/test_s8b2_memory_guards.py::test_01..test_05`, and 35 skips across fixture-gated tests.
- These are recorded S11e findings, not a fresh reproduction in this ledger. Recheck fixture availability/current environment. Never invent a fixture result or weaken tests.

**Recorded S11e totals:** 475 total = 432 PASS + 35 SKIP + 6 FAIL + 2 ERROR. This is not a clean suite and not 475 passing tests.

### E.1 Cross-test Tk teardown watch

`Tcl_AsyncDelete` cross-test GC/teardown abort was observed during older S11c/S11d monolithic discovery, while S11e monolithic discovery completed cleanly. Evidence: `SOURCE-OBSERVED` historically + `NEEDS-REPRO` current. Lifecycle: `ACTIVE` watch item. Do not call it a current deterministic failure without reproducing on the current environment.

## F. DEF-01..DEF-10 — deferred core limitations / blocked definitions

| ID | Evidence | Lifecycle | Recorded definition / constraint |
|---|---|---|---|
| **DEF-01** | `SOURCE-OBSERVED` + `DEFERRED` | `DEFERRED` | `core/story_ast.py:to_binary()` preserves empty binary-argument arity with a sentinel containing exactly one ASCII space (`" "`). Accepted under S11c Option A. Do not change, strip, or replace without a new decision and live-client evidence. |
| **DEF-02** | `SOURCE-OBSERVED` + `DEFERRED` | `DEFERRED` | Numeric command IDs 35/32 have synthetic binary/v2 test coverage, but real production bundle verification remains blocked by unavailable `storydata_1001005.unity3d`. Require the real fixture or written Project Lead waiver. |
| **DEF-03** | `SOURCE-OBSERVED` + `DEFERRED` | `DEFERRED` | Multi-TextAsset target selector remains deferred; recorded `load_bundle_story` behavior selects a single primary story TextAsset. Requires fixture-backed specification. |
| **DEF-04** | `SOURCE-OBSERVED` + `DEFERRED` | `DEFERRED` | Box 0 Summary overflow was unmeasured/deferred in the recorded ledger. Do not assume ordinary dialogue overflow rules apply without a specific decision/test. |
| **DEF-05** | `SOURCE-OBSERVED` + `NEEDS-REPRO` | `DEFERRED` | Definition unavailable because `Phase_2.5_Canonical_Ledger_LOCKED.md` was missing from recorded disk/Git object store. Do not invent meaning; search authoritative source/history. |
| **DEF-06** | `SOURCE-OBSERVED` + `DEFERRED` | `DEFERRED` | `_is_speaker_pinned` was recorded as preserved/untouched. Keep behavior until named scope authorizes change; confirm current implementation before acting. |
| **DEF-07** | `SOURCE-OBSERVED` + `NEEDS-REPRO` | `DEFERRED` | Definition unavailable in the recorded missing Phase 2.5 canonical ledger. Do not guess. |
| **DEF-08** | `SOURCE-OBSERVED` + `NEEDS-REPRO` | `DEFERRED` | Definition unavailable in the recorded missing Phase 2.5 canonical ledger. Do not guess. |
| **DEF-09** | `SOURCE-OBSERVED` + `NEEDS-REPRO` | `DEFERRED` | Definition unavailable in the recorded missing Phase 2.5 canonical ledger. Do not guess. |
| **DEF-10** | `SOURCE-OBSERVED` + `DEFERRED` | `DEFERRED` | Modular decomposition of the ~1.03 MB / ~17k-line `misora.py` was deferred. Cancellation of v1.5.0 removes any implied “after release” date. Future refactor is unscheduled and requires a separate architecture charter. |

## G. Historical and retracted claims

Preserve the full canonical defect ledger, B1–B20, BUG-01..BUG-41, FEAT-01..FEAT-14, HYG-01..HYG-08, NO-01..NO-12, and retracted claims in the verbatim archive + `HISTORY_INDEX.md`. The compact active ledger must not repeat every resolved issue as current work. Keep retractions as `RETRACTED` / `HISTORICAL-REFERENCE`; never reopen without new evidence.

## H. Triage rule

No issue in this ledger authorizes implementation. A new task requires exact baseline, scope, evidence/repro, affected symbols/tests, acceptance criteria, rollback, and explicit Project Lead approval. Track B is unscheduled; “deferred” does not mean automatically queued.
