# Misora — Master Triage Ledger T-01..T-14 (Post-S11e)

**Triage status:** preliminary independent assessment based on the Project Lead's supplied ledger and S11e reports. Except where explicitly noted, I have not reproduced these items on the current local HEAD. A triage ID is not authorization to implement.

## Severity definitions

- **P1:** potential data loss, editor obstruction, or state corruption; reproduce and prioritize.
- **P2:** functional inconsistency or meaningful UX defect; schedule after P1.
- **P3:** polish or convenience; only after correctness and design are stable.
- **PROPOSAL:** feature/design request, not an existing bug.
- **TRACK B:** larger architectural work; separate plan and risk review.

| ID | Original | Type | My preliminary view | Evidence status | Recommended disposition |
|---|---|---|---|---|---|
| T-01 | BUG-UI-EMPTY-STATE-01 | UI bug, proposed P1 | Important: overlay obscures dialogue editor and horizontal scrollbar while documents are open. First suspect is mismatch between pack-managed state and `winfo_ismapped()`/parent mapping, but this is only a hypothesis. | REPORTED Windows observation; root cause NEEDS-REPRO. | First reproduction. Test 0/1/2 open documents, close one/last, and Dialogue/All Script switching. Inspect `winfo_manager`, `winfo_ismapped`, parent mapping, and geometry manager. Fix only after root cause is proven. |
| T-02 | U-08 | Tooltip defect, P2 | Likely small correction if the stale `50x3` wording still exists. Verify all user-visible references; do not update unrelated historical docs indiscriminately. | REPORTED; NEEDS-SOURCE-CHECK. | Search source for `50x3`, `50 x 3`, and related tooltip strings. Compare with canonical 54d × 3 rule. Add a targeted test for the live Next tooltip. |
| T-03 | U-05 | Selection/state bug, P1 if reproduced; otherwise P2 | Pin Speaker should navigate without turning all intervening cards into selected boxes. But `current_box_idx`, active-card highlight, and `_selected_boxes` are distinct concepts; the exact unwanted state must be identified. | REPORTED; NEEDS-REPRO. | Reproduce in All Script with one selection, then pin/jump across several speakers. Record `_selected_boxes`, active UID/index, anchor, and visible card flags before/after. Test Ctrl/Shift selection semantics separately. |
| T-04 | U-02 | Overflow indicator gap, P2 | The stated rule is 54 digit-widths OR 4+ rendered lines (3+ line breaks). A red marker should reflect the same canonical predicate in Dialogue and All Script; beware counting raw newlines when wrapping can be visual-only. | REPORTED/spec mismatch; NEEDS-SOURCE-AND-VISUAL-VERIFY. | Audit the shared metrics function and every marker caller. Use test cases: 3 lines, 4 lines, long 54d line, explicit breaks, automatic wrap. Define whether the marker signals a box-level violation or points to only lines 4+. |
| T-05 | U-01 | Config/path UX redesign, P2/large | Strong proposal. Distinguish Game Folder, loaded RedirectedResources, and XUnity AutoTranslator text dictionary directory. XUnity.AutoTranslator is a plugin, not a framework. Avoid framework-specific hardcoding. | PROPOSAL; requires current config/source audit. | Design a path model first: autodetection is a suggestion, each path manually editable, multi-framework/multi-language supported, deterministic precedence, path validation and missing-path messaging. Clarify whether RedirectedResources is input data or only an optional discovery root. |
| T-06 | U-03a | Save-dialog UX, P2 | Separate remembered directories for `.misora` workspace save and bundle/patch save is sensible; they represent different resource types. | PROPOSAL; NEEDS-REPRO of current directory behavior. | Document exact dialogs, initial-directory rules, persistence scope, and cancellation behavior. Keep local config safety constraints. |
| T-07 | U-07 | Tooltip coverage, P3 | Useful but broad. Tooltip proliferation can create noise and duplicate existing S11e 350 ms coverage. Labels should only get tooltips when their meaning is not self-evident. | PROPOSAL; inventory required. | Create a coverage matrix of widget → current tooltip → missing information → proposed text. Prioritize Voice Cue, segments badge, Box counter, Opened Files and genuinely opaque controls. Do not blanket-bind every label. |
| T-08 | U-11 | Ribbon redesign | Major UI redesign, not a small bug fix. Four rows and hide/show dependencies can affect responsive layouts, snap layouts, and view discoverability. | PROPOSAL; requires design decision. | Produce a static mockup and interaction spec first. Define narrow-window behavior, ordering, menu toggle dependencies, persistence, keyboard access, and no-overlap rules. Prototype separately; don't combine with P1 fixes. |
| T-09 | U-12 | Toolbar/selection UX | Partly overlaps S11e: BoxInsert/BoxReplace paste-mode chooser and three-icon selection trio were reported implemented. The remaining request for explicit Insert/Replace/tri-state controls may duplicate current affordances. | PARTIALLY IMPLEMENTED per S11e report; local source not inspected here. | Audit current UI before planning. Specify whether these are commands, persistent modes, or chooser buttons. Do not build duplicate controls. |
| T-10 | U-06 | All Script selection UX | Selected-card highlighting and Excel-like Ctrl/Shift semantics are valuable but can be expensive or error-prone with a virtualized card pool. | PROPOSAL; performance-sensitive. | Define selection contract and anchor semantics first. Benchmark visible-pool updates at 150/300/1000 boxes. Test virtualization/recycling, view switches, locks, active card vs selected card, Ctrl toggle, Shift range. |
| T-11 | U-03b | Original source/reference panel | High-value concept, but “permanent Master Undo” is misleading. An immutable original snapshot is not an Undo operation and must survive save/reopen. | PROPOSAL / TRACK B. | Reframe as “Original Source Snapshot”. Decide capture point, storage (sidecar/backup/versioned snapshot), identity mapping, actor metadata, privacy/size, restore workflow, and behavior after external file replacement. Keep separate from Undo Journal. |
| T-12 | U-04 | Async XUAT disk I/O | Potential UI responsiveness improvement; S11b2 accepted 2.899 s and deferred async work. Moving disk work to a worker requires immutable targets, freshness checks, cancellation, queue-only UI completion and partial-failure semantics. | DEFERRED proposal; existing accepted latency waiver. | Track B. Benchmark components first (scan vs decode vs write). Never promise “0 ms”; define UI responsiveness target and data-race/atomic-write behavior. |
| T-13 | U-10/U-13 | Text XUAT backup/revert | Important safety proposal. Must distinguish original datamine dictionary from generated/updated plugin translations and preserve enough provenance to restore the right revision. | PROPOSAL; design needed. | Define backup manifest, source fingerprint, timestamp, file path mapping, encoding/BOM/newline preservation, collision-resistant names, retention, restore preview, and import compatibility. Do not assume a text copy alone is a safe restore mechanism. |
| T-14 | U-09/U-13 | CI/CD release artifacts | Useful when release process is mature, but premature while release target and packaging contract are paused. A ZIP is materially simpler than a signed Windows EXE. | PROPOSAL; later infrastructure track. | Defer until release is reinstated. Decide reproducible build, Python/Tk/UnityPy packaging, licensing, AV false positives, signing, checksums, version metadata, rollback and artifact retention. |

## Recommended order

1. **T-01 first** — UI obstruction and scrollbar overlap.
2. **T-03 and T-04** — editor selection correctness and overflow-contract consistency.
3. **T-02** — stale tooltip correction (low cost, after source confirmation).
4. **T-05 and T-06** — config/path and save-location UX, with separate design review.
5. **T-07** — measured tooltip gaps only.
6. **T-08, T-09, T-10** — UI design cluster; first check overlap with implemented S11e behavior.
7. **T-11, T-12, T-13, T-14** — separate architecture/Track B proposals; no implementation until individually scoped.

## Cross-cutting cautions

- Do not treat all T-01..T-14 as bugs. Most are proposals or UX requests.
- Do not use P1 label as proof. Severity is provisional until impact and reproduction are confirmed.
- Do not combine independent issues into a single large session.
- For every confirmed bug, record exact local HEAD, reproduction steps, source symbol/line, expected/actual result, regression test, manual QA and closure evidence.
