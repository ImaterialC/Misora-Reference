# OPTIONAL POST-PROCEED SNIPPETS (DO NOT PASTE IN INITIAL `/plan` MESSAGE)

Use these ONLY AFTER you have reviewed the Implementation Plan artifact and clicked `Proceed`.
- `/goal` has NO iteration cap: monitor the session and cancel if it loops.
- `/boost` is optional ONLY on high-risk sessions (`S03`, `S04`, `S09`, `S11`, `S22`) if a Probe proves tricky.
- `/swarm` is **READ-ONLY AUDIT ONLY** (never parallel code editing on `misora.py`) after Track 1 (`S13`) and Track 2 (`S23`).

## A. Optional Read-Only `/swarm` Cross-Model Audit (After S13 Track 1 & After S23 Track 2)
```text
/swarm Perform a READ-ONLY audit of the completed Misora-Editor Track against the locked Phase 2.5 Canonical Ledger (SHA-256 73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd). DO NOT edit any files.
- @core-auditor (Gemini 3.8 Flash): read-only inspection of changed files under @core/ and @assets/.
- @gui-auditor (Gemini 3.8 Flash): read-only inspection of changed regions in @misora.py.
- @test-auditor (GPT-OSS 120B): read-only adversarial review of new probes/guards under @tests/ and @CHANGELOG.md; challenge any weak assertions or missing failure paths.
- @lead-verifier (Claude Sonnet 4.6): synthesize findings, verify zero DEF-*/NO-* violations, confirm real `py -3.12 -m unittest discover -s tests -v` output, and report PASS/FAIL/BLOCKED per ID. If per-worker model routing is unavailable in this UI, state that limitation honestly.
```

## B. Optional Per-Session `/goal` Snippets (ONLY if agent stops early after `Proceed`)

### S01 — Docs, Ledger & AGENTS.md Topic-Safe Reconciliation + Initialize CHANGELOG.md
```text
/goal Complete approved S01 plan ONLY (HYG-01). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest discover -s tests -v` exits 0 ONCE with `Ran N tests` (`N > 0`, 0 failures, 0 errors, 0 unexpected skips; `Ran 0 tests` = FAIL); (3) `git status --short` lists ONLY `PROJECT_STATE.md`, `README.md`, `AGENTS.md`, and `CHANGELOG.md` (ZERO `.py` edits, ZERO new files in `backups/`, ZERO git commits/pushes); (4) `AGENTS.md` preserves `## 19. NGUI single source` heading + first 3 bullets and records exact overflow wording under `UI safety`; (5) `CHANGELOG.md` exists with `## [Unreleased] (Target: v1.4.1)` and `### S01`.
```

### S02 — Test `backups/` Isolation, `search_engine.py` `Any` Import & Single-Version DeepL User-Agent
```text
/goal Complete approved S02 plan ONLY (HYG-02, HYG-05, HYG-06). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s02_hygiene -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S02` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S02` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S03 — Strict Binary Parse, Lossless v2 + \b64:, Command Map/Breakers (Guard 35/32) & Fixture-Gated Bundle Verify
```text
/goal Complete approved S03 plan ONLY (BUG-01, BUG-03, BUG-04, BUG-09). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s03_binary_v2 -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S03` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S03` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S04 — Kind-Conversion Box Separation, Voice/Breaker Ownership, Multi-Segment Undo/Paste, UID Coalesce & Tombstones
```text
/goal Complete approved S04 plan ONLY (BUG-02, BUG-05, BUG-06, BUG-17, HYG-04). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s04_ast_mutations -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S04` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S04` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S05 — Dark-Theme Treeview Contrast (DEP-1 FIRST), Atomic Sparse CSIF/Metadata & Backslash Parity
```text
/goal Complete approved S05 plan ONLY (BUG-31, BUG-07, BUG-08). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s05_treeview_csif -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S05` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S05` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S06 — Per-Document State/Stable Locks, Plain-Text Preview Save, Windows LF Writes & 0-Box Save
```text
/goal Complete approved S06 plan ONLY (BUG-11, BUG-12, BUG-18, BUG-19). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s06_doc_state_save -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S06` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S06` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S07 — Caret Paste Dirty/Lock, Mutate-Before-Undo, Non-Contiguous Cut Undo, Lock Enforcement & Read-Only Raw
```text
/goal Complete approved S07 plan ONLY (BUG-10, BUG-13, BUG-15, BUG-16, BUG-37). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s07_undo_locks_raw -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S07` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S07` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S08 — Search Match-Case/Errors/Snapshots/Spans, Bounded Project Roots & Search Focus/Gutter/No-Op KeyRelease
```text
/goal Complete approved S08 plan ONLY (BUG-21, BUG-22, BUG-23, BUG-30). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s08_search_roots_focus -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S08` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S08` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S09 — Multi-File Replace-All Cache Keys/Shared Matcher/Closed-File Undo & Collision-Resistant Backups
```text
/goal Complete approved S09 plan ONLY (BUG-24, BUG-20). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s09_replace_all_backups -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S09` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S09` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S10 — Immutable `box.uid` XUAT JP Keys, Save Conflict Preview Gate & Atomic XUAT Dictionary Writes
```text
/goal Complete approved S10 plan ONLY (BUG-25, BUG-26). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s10_xuat_integrity -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S10` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S10` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S11 — Main-Thread Queue-Only Async MTL, Stale-Result Identity Guard & Safe Batch Cancel
```text
/goal Complete approved S11 plan ONLY (BUG-14, BUG-27). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s11_mtl_threading -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S11` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S11` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S12 — Logger Flush Barrier/Teardown, DPAPI Fail-Closed, Reload Env Disposal, Deferred Startup & Splash Safety
```text
/goal Complete approved S12 plan ONLY (BUG-32, BUG-33, BUG-34, BUG-35, BUG-36). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s12_lifecycle_security -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S12` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S12` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S13 — Continuous Ribbon/Size/Dirty Sync, Shortcut Conflicts, Complete Tooltips & `Ctrl+H` Hygiene (TRACK 1 FINAL GATE)
```text
/goal Complete approved S13 plan ONLY (BUG-28, BUG-29, HYG-03, HYG-07). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s13_ribbon_shortcuts -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S13` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S13` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S14 — Search Bar 5-Col Grid, Hide Current Dir, Player Icon/No `[-]`, VIEW Group, Toggle NGUI Ribbon & `Raw Commands`
```text
/goal Complete approved S14 plan ONLY (BUG-38, BUG-39, FEAT-01, FEAT-02, FEAT-03, FEAT-04). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s14_toolbar_search_ui -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S14` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S14` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S15 — Select Box Both Views + Reserved Lock Slot, Collapsible Left Drawer, Empty State & Batched Multi-Open
```text
/goal Complete approved S15 plan ONLY (BUG-41, FEAT-05, FEAT-06, FEAT-07). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s15_selection_drawer_open -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S15` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S15` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S16 — `.misora` v1 Workspace Session (References + State + Stable-Key Locks Only) & Overwrite Diff Dialog
```text
/goal Complete approved S16 plan ONLY (FEAT-08). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s16_misora_workspace -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S16` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S16` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S17 — Shared Pixel-Measure Helper, Calibrated Rulers (50 Digit-Widths / Line 4+) & Remove Char Counter
```text
/goal Complete approved S17 plan ONLY (BUG-40, FEAT-09). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s17_pixel_rulers -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S17` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S17` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S18 — Code-Drawn Game-Style `Dialogue Preview` & `All Script Preview` (Native Bleed, `wrap='none'`, No `AtlasAdv`)
```text
/goal Complete approved S18 plan ONLY (FEAT-10). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s18_game_preview -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S18` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S18` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S19 — Whole-File Editable `Raw Commands` (Lossless v2, Confirm, `DocumentRecordsDelta` Undo & Lock/JP Remap)
```text
/goal Complete approved S19 plan ONLY (FEAT-11). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s19_raw_commands_edit -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S19` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S19` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S20 — Docked Right-Side MTL Drawer — Tab Infrastructure & `Dialogue` Multi-Engine Stack
```text
/goal Complete approved S20 plan ONLY (FEAT-12). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s20_mtl_drawer_dialogue -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S20` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S20` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S21 — Right-Side MTL Drawer — `All Script` Mode (Exact 2 `tk.Text` Widgets + 5 Static Status Tags)
```text
/goal Complete approved S21 plan ONLY (FEAT-13). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s21_mtl_drawer_all_script -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S21` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S21` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S22 — Unified `core/xuat_index.py` & Separate Floating `Import from XUAT` Resolver (Paired Fixed `3×50` Read-Only)
```text
/goal Complete approved S22 plan ONLY (FEAT-14). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s22_import_xuat -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S22` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S22` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S23 — Final Grep-Proven Dead Code & Misleading Label Cleanup (Standalone Final Implementation Session)
```text
/goal Complete approved S23 plan ONLY (HYG-08). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `py -3.12 -m unittest tests.test_p3_s23_dead_code_cleanup -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors; `Ran 0 tests` = FAIL); (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`); (4) `git status --short` lists ONLY `S23` Allowed Files + `CHANGELOG.md` + `PROJECT_STATE.md`, with ZERO new files in `backups/` and ZERO git commits/pushes; (5) `CHANGELOG.md` has `### S23` recorded accurately. If any Defect Probe already passed pre-patch, STOP and report `ALREADY PASSING / NOT REPRODUCED` instead of weakening tests.
```

### S24 — Final Acceptance Audit Matrix (All 63 IDs + DEF/NO) & Single `v1.4.1` Version/Changelog Release Stamp
```text
/goal Complete approved S24 plan ONLY (Final Acceptance Audit & Release Gate). Done means ALL of these are proven with real stdout in the Walkthrough: (1) `py -3.12 -m compileall -q misora.py core assets tests` exits 0; (2) `tests/test_phase4_import_export_preview.py::test_01_version_unification` derives `expected_version` from root `__init__.__version__` and passes; (3) `py -3.12 -m unittest discover -s tests -v` exits 0 with `Ran N tests` (`N > 0`, 0 failures, 0 errors, 0 unexpected skips; any skip explicitly documented as fixture-`BLOCKED`); (4) Complete 85-ID matrix (41 BUG + 14 FEAT + 8 HYG + 10 DEF + 12 NO) is recorded with real evidence; (5) `__version__` is bumped to `'1.4.1'` and `CHANGELOG.md` promotes `## [Unreleased]` to `## [1.4.1]` (including `### S24`) ONLY if zero unwaived `BLOCKED` P0/P1 items remain AND all mandatory manual Windows blockers (`AGENTS.md` §29) are confirmed PASS or explicitly risk-waived by the Project Lead (otherwise STOP cleanly at `'1.4.0'` with `### S24` under `## [Unreleased]`); (6) `git status --short` lists ONLY S24 Allowed Files with ZERO new files in `backups/` and ZERO git commits/pushes.
```
