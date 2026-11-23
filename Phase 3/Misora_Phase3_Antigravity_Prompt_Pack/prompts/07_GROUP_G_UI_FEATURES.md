# MILESTONE G — UI BUGS & ACCEPTED FEATURES

```text
/plan

Implement Milestone G only after all required P0/P1 stabilization gates and explicit feature dependencies in the locked ledger pass.

Scope:
A. Remaining UI correctness bugs:
- BUG-38 Find/Replace bar alignment with geometric widget assertions.
- BUG-39 responsive toolbar visibility at 1280x720 and snapped half-screen width.
- BUG-40 remove inaccurate character counters and unify pixel-measure implementation.
- BUG-41 Box 0 Select Box checkbox and correct Dialogue-mode selection behavior.

B. Accepted features:
- FEAT-01 hide directory controls on Current File(s) without clearing stored paths.
- FEAT-02 icon-only Player button, move out of NGUI group, remove standalone redundant [-], preserve glossary entry.
- FEAT-03 All Script naming, unified VIEW group, icons/tooltips/fallbacks, Raw Commands bottom name.
- FEAT-04 Toggle NGUI Ribbon and responsive toolbar layout.
- FEAT-05 Select Box in Dialogue and All Script, stable lock slot.
- FEAT-06 pane-based collapsible left drawer (never place() overlay).
- FEAT-07 empty state, double-click Opened Files, multi-file open with single UI refresh.
- FEAT-08 references/state/stable-key-lock .misora v1 with dirty-aware Save/Discard/Cancel and file-difference map. No drafts or binary blobs.
- FEAT-09 shared pixel measure, 50 digit-width red zone, line 4+ warning, overflow highlight, remove counters.
- FEAT-10 game-style Dialogue and All Script Preview with native bleed, no auto-shrink; pure presentation layer.
- FEAT-11 whole-file Raw Commands editing only after DEP-5 and full lossless/transactional validation. Keep read-only if any gate is not proven.
- FEAT-12 Dialogue MTL drawer only after MTL queue and lock gates pass.
- FEAT-13 All Script MTL drawer must have exactly two Text widgets and five agreed static theme-aware statuses.
- FEAT-14 Import from XUAT floating resolver under Import menu, not MTL drawer, with paired fixed 3x50 read-only boxes, duplicates/provenance, skip/lock/filter handling, exact pre-apply summary and one atomic Undo.

Hygiene:
- HYG-03 tooltips and Unicode fallbacks before/with toolbar changes.
- HYG-08 remove dead code only after zero callers are proven by search; do not delete based on assumptions.

Mandatory dependencies:
- FEAT-10 and FEAT-14 require BUG-11 PASS.
- FEAT-12/13 require BUG-14, BUG-27 and HYG-01/AGENTS §24 amendment PASS.
- FEAT-14 requires BUG-23 and BUG-25 PASS.
- FEAT-08 requires BUG-12 and BUG-35 plus FEAT-07.
- FEAT-11 requires BUG-01..BUG-06 and verified lossless v2 transaction gate.
- FEAT-09/10 must use one shared pixel measurement helper; editor-font estimate must be labeled as such.

Guardrails:
- Do not bundle copyrighted AtlasAdv assets.
- Do not build an emulator, audio/portrait/typewriter system or full reskin.
- Do not implement Box 0 Summary limits until measured in-game.
- Do not use 142 Text widgets or Treeview single-line translation content for FEAT-13.
- Do not use place() overlay for left dock.
- Do not add `.misora` draft or binary persistence.
- Do not silently apply duplicate XUAT translations; keep conflict scope and provenance visible.
- Enforce Translation Lock in model/apply logic, not just UI disabled state.

Verification:
Use actual Tkinter app on Windows for geometry, visibility, focus, preview overflow and input behavior. `/browser` is not a substitute for Tk desktop testing. Capture real screenshots where possible. Add automated tests for layout/state logic, plus a manual Windows QA matrix. No screenshot may be fabricated.

Deliverable:
A feature-by-feature matrix with dependencies, tests, GUI evidence, limitations and independent review. Stop and retain read-only/disabled state for any feature whose data-integrity dependency is not proven.
```
