# MISORA: STORY EDITOR — RECONCILED POST-S11 ROADMAP (v3 — FINAL SIGN-OFF CANDIDATE)

From: Gemini (aligned with Project Lead decisions and GPT's 4 mandatory v2 revisions + Q-01/Q-22 clarifications)
To: ChatGPT (Independent Technical Reviewer)
Repository Baseline: `ImaterialC/Misora-Editor` `main` @ `c1ec40c` (`__version__ = "1.4.10"`)
Execution Boundary: ROADMAP RECONCILIATION ONLY. Zero Antigravity prompts generated; zero `/plan` sessions started; zero source files modified; `v1.5.0` remains ON HOLD until Track A completes, Manual Windows QA is completed or formally waived by Project Lead, and S12 Release Gate passes all criteria.

======================================================================
1. BASELINE HONESTY & PRIOR S11 EXECUTION REPORT
======================================================================
- `main` contains S09b (`v1.4.8`), S10 (`v1.4.9`), and S11 (`v1.4.10`, commit `c1ec40c`).
- Previously reported S11 automated counts (**440 discovered, 397 passed, 35 fixture-blocked skips, 6 pre-existing failures, 2 pre-existing errors**; 28/28 targeted S11+XUAT; 17/17 notification+S11) are strictly **prior Antigravity/Gemini execution reports**, NOT independently re-executed by GPT.
- Manual Windows QA remains OPEN / pending explicit Project Lead sign-off.

======================================================================
2. ALL 4 MANDATORY v2 REVISIONS + Q-01 & Q-22 CLARIFICATIONS APPLIED
======================================================================

### Revision A — Explicit S12 Test-Failure Taxonomy & Acceptance Criteria
Every non-passing item from the prior S11 baseline report (`6` failures, `2` errors, `35` skips) is explicitly accounted for below:

| Baseline Item | Count | Classification | Planned S12 Disposition |
|---|---:|---|---|
| `tests/test_v15_s01_stability_remediation.py::test_probe_8` | 1 fail | Pre-existing non-fixture hygiene (stale hardcoded `"1.4.1"` version assertion) | **FIX IN S12** -> migrate to dynamic root `__init__.__version__` parity |
| `tests/test_phase3_performance_config.py::test_05` | 1 fail | Pre-existing non-fixture hygiene (reads machine-local untracked `misora_config.json`) | **FIX IN S12** -> isolate via temporary test-owned fixture; never read/overwrite user config |
| `tests/test_s9c_workspace_safety.py::test_04` | 1 fail | Pre-existing non-fixture hygiene (expects `misora_config.default.json`) | **FIX IN S12** -> test repo-owned clean template OR test-owned temp fixture / explicit absence policy; never fall back to user config |
| `tests/test_s8b2_memory_guards.py` (missing `storydata_1001005.unity3d`) | 3 fail + 2 error | **Fixture-Blocked** (proprietary production bundle absent in repo) | Remains explicitly **`BLOCKED`** unless real fixture is supplied OR Project Lead signs an explicit written waiver/exception |
| Fixture-gated skips across `tests/` (missing `storydata_1001005.unity3d`) | 35 skip | **Fixture-Blocked Skips** | **NEVER counted as `PASS`.** Remains explicitly `SKIPPED (FIXTURE-BLOCKED)` and requires either real-fixture execution or explicit written Project Lead waiver at Release Gate |

**Mandatory S12 Release Gate Acceptance Criteria (ALL 4 REQUIRED):**
1. **Zero New Regressions:** `0` unexpected failures or errors relative to the documented baseline.
2. **Written Disposition for Every Baseline Failure/Error:** Every failure and error has an explicit final disposition recorded in `PROJECT_STATE.md` (`FIXED`, `PROVEN-NOT-A-BUG`, or `EXPLICIT PROJECT LEAD WAIVER`). S12 MUST NOT declare `PASS` merely because the failure count did not increase.
3. **Honest Skip Accounting:** Fixture-blocked skips (`35`) are NEVER counted as `PASS`.
4. **Exact Execution Counts:** Report exact discovered, executed, passed, skipped, failed, and errored counts (never pass-rate percentages alone).

### Revision B — Explicit S12 Read-Only Audit Boundary (No Ambiguity)
- **Strictly READ-ONLY in S12 (ZERO edits permitted):** ALL production source code and user data — `misora.py`, `core/*.py`, `assets/*`, `requirements.txt`, `misora_config.json`, `backups/`.
- **ONLY Modifications Permitted in S12 (Pre-Identified & Pre-Approved Scope):**
  1. The **3 pre-identified non-fixture test-hygiene files** listed in Revision A (`tests/test_v15_s01_stability_remediation.py`, `tests/test_phase3_performance_config.py`, `tests/test_s9c_workspace_safety.py`),
  2. Optional S12 stress/leak regression guards in `tests/test_v15_s08_release_gate_stress.py`,
  3. Documentation & ledger updates (`AGENTS.md`, `PROJECT_STATE.md`, `CHANGELOG.md`, `README.md`),
  4. Conditional `__init__.py` version promotion (`<final_pre_s12_version>` -> `"1.5.0"`) ONLY if ALL Release Gate conditions pass AND Project Lead explicitly authorizes promotion.
- **Hard-Stop Defect Rule:** If the S12 read-only audit discovers ANY new P0/P1 source bug, memory leak, or production defect in `misora.py`, `core/*.py`, or `assets/*`, S12 MUST NOT silently patch it — record it with `file:line` evidence as a Release Gate BLOCKER, hold version at `<final_pre_s12_version>`, and spin off a separate bounded fix session.

### Revision C — Explicit `Q-04.1.3` Waiver Status Taxonomy
`Q-04.1.3` MUST distinguish strictly between untested, waived, and passed states:
- **`NOT TESTED`** — Not yet tested and no written Project Lead waiver exists (blocks QA completion).
- **`NOT TESTED — WAIVED`** — Not tested, with an explicit written Project Lead approval accepting the exception.
- **Honesty Guard:** A waived item MUST NEVER be relabeled `PASS`, and QA reports MUST NEVER claim that a waived test was executed or completed. Release Gate may consider an approved `NOT TESTED — WAIVED` decision only with explicit Project Lead sign-off recorded in `PROJECT_STATE.md`.

### Revision D — Complete `Q-05` Splash Screen Acceptance Contract (`S11e`)
- **Full Startup Visibility Requirement:** The Splash Screen MUST remain visible until **ALL UI/UX construction AND full previous-session state restoration** (`_deferred_restore`, saved config/UI component loading, document restore) have completely finished — NOT merely until the main window is instantiated.
- **Non-Blocking Honest Progress:** Display real startup progress stages without freezing the main thread or claiming work is complete before it actually finishes.
- **Mandatory Automated Acceptance Test:** Include an automated test with an **artificially slowed startup/restore phase** verifying that:
  1. The splash screen does NOT close prematurely while UI/session restoration is still running,
  2. Progress indicators accurately reflect incomplete vs completed state (never prematurely reporting 100% / ready), and
  3. The splash closes cleanly once restoration finishes.

### Additional Refinement 1 — `Q-01` XUAT Scanner Existing Filters & Exact Metric Definitions (`S11b`)
- **Additive Exclusions Only:** Add the 5 official XUAT rule-file exclusions (`*.font.txt`, `*.resizer.txt`, `*Postprocessors.txt`, `*Preprocessors.txt`, `*Substitutions.txt`) **WITHOUT removing any existing scanner exclusions** already in `core/xuat_index.py` (such as `.missing.txt`, `.report.txt`, `_summary.txt`, `_warnings.txt`, `.bak_`, etc.).
- **Unambiguous, Mathematically Consistent Metric Definitions (verified by unit tests):**
  * `files_scanned`: count of deduplicated eligible `.txt` files actually scanned under `Translation\<lang>\Text`.
  * `entries_read`: total count of valid `key=value` translation entries parsed across all scanned files (including duplicates).
  * `unique_keys`: count of distinct normalized keys (`len(by_norm_key)`).
  * `duplicate_keys`: count of **distinct normalized keys** that have more than one parsed entry (`sum(1 for entries in by_norm_key.values() if len(entries) > 1)`).
  * `duplicate_entries`: count of **redundant occurrences after the first** (`entries_read - unique_keys`), guaranteeing the exact tested identity `entries_read == unique_keys + duplicate_entries`.
- Test all 5 root configurations (`Game Root`, `BepInEx`, `Translation`, `Translation\en`, `Translation\en\Text`), deduplication of overlapping roots/files, preservation of legacy exclusions, and explicit negative proof that `Other\` and `RedirectedResources\` are not scanned.

### Additional Refinement 2 — `Q-22` Quick Edit Pre-Mutation Snapshot & Projection Parity (`S11c`)
- **Pre-Mutation Snapshot Timing:** Capture `old_snapshot = BoxSnapshot.from_box(box)` (full `seg_texts`, `raw_breaks`, `extra_args`, `speaker`, `voice_cue`, `kind`) **strictly BEFORE the first live mutation** when a Quick Edit session begins — NEVER after edits have started or at session commit.
- **Identical Unified Text Projection:** Construct the unified single-box display string using the **exact same text projection helper/path** used by the main Dialogue Editor (`txt_dialogue` / `box.clean_text`) so initial display, editing, and canonical `inject_box(idx, None, new_tx)` behavior have zero divergence between the two editors.
- Retain all 8 safety invariants, the **Manual-Dialogue-vs-Quick-Edit AST & binary parity test**, S09b Lock Parity (Row 1), and full audit/migration of BOTH `tests/test_v15_s10_all_script_quick_edit.py` and `tests/test_v15_s08_release_gate_stress.py` (including `_qe_seg_widgets[0]`).

======================================================================
3. FINALIZED TRACK A ROADMAP (5 BOUNDED SESSIONS) & TRACK B
======================================================================
*(Note: If any `S11b` STOP gate spins off a dedicated session, subsequent target versions increment sequentially and `S12` tracks the exact final `__init__.__version__` installed on disk.)*

| Step | Session | Target Version | Bounded Scope & Gates |
|---|---|---|---|
| 1 | **`S11b`** | `v1.4.11` | **`Q-01`** (XUAT scanner: additive 5 official exclusions + preserve existing filters, strict `Translation\<lang>\Text`, root/file dedup, unambiguous metrics `files_scanned`/`entries_read`/`unique_keys`/`duplicate_keys`/`duplicate_entries`, 5 root entry points + negative `Other/` & `RedirectedResources/` tests); **`Q-02`** (Save Hang profiling across all 5 stages with **STOP gate** if major async/bundle transaction refactor is required + `Ctrl+S` Save Project `.misora` & conflict-free Save & Patch Bundle shortcut + menu/tooltips/README/tests); **`Q-04`** (inspect `1.1` `▶` origin without assuming removal; reproduce `1.2` selection/drag/scroll separately on multi-match >3-linebreak Name/Title/Subtitle; `1.3` strictly `NOT TESTED`); **`Q-18`** (Ruby Preview bug fix with **STOP gate** if custom text-layout engine is required); **`Q-23`** (remove red overflow blocks in `txt_dialogue_preview` + defensive guard in overflow helper + migrate `test_v15_s03_all_script_preview_paste.py` & `test_p3_s18_game_preview.py` + assert Editor Preview-OFF retains red markers, pink nameplate, gold border, pink `▼`, `54d × 3`, `wrap="none"`). |
| 2 | **`S11c`** | `v1.4.12` | **`Q-22` ONLY** (Quick Edit unified single-box UX matching main Dialogue Editor text projection, pre-first-mutation `old_snapshot`, canonical `inject_box(idx, None, new_tx)`, fresh `new_snapshot`, 8 AST/Undo/Lock invariants, Manual-Dialogue-vs-Quick-Edit AST+binary parity test, full audit/migration of `test_v15_s10_all_script_quick_edit.py` and `test_v15_s08_release_gate_stress.py`). |
| 3 | **`S11d`** | `v1.4.13` | **`Q-06`** (Import MouseWheel propagation over labels/child frames); **`Q-07`** (per-group tri-state none/some/all Select All); **`Q-08`** (multi-line wrapped Synopsis Metadata Import — NOT 1-line `54d` — with Skip, duplicate handling, atomic `MetadataDelta` Undo/Redo); **`Q-09`** (fix leftover `"Import Complete - XUAT translation Archiving"` sub-header); **`Q-10`** (`Select All Box` button/checkbutton: dialogue boxes only, Box 0 excluded, Translation Lock unchanged); **`Q-11`** (MTL Globe button: safe copy active text to clipboard + open official website; no unverified deep-link claims); **`Q-12`** (truncated `filename — Title (Subtitle)` in window title from already-parsed metadata). |
| 4 | **`S11e`** | `v1.4.14` | **`Q-03`** (per-widget-class word-wrap contract across all audited textboxes); **`Q-05`** (Splash Screen stays visible until ALL UI/UX + previous-session state restoration finish, honest non-blocking progress + slowed-startup acceptance test); **`Q-13`** (bold/larger `PriconneRe:TL` + `Cornelia` on Splash & About); **`Q-14`** (`Support the Creator`, full English copy, ~600px aspect-preserving Pillow GIF, no FFmpeg/OpenCV); **`Q-15`** (corrected icon map verified on disk for filenames/extensions/alpha/dimensions: Translate=`language-translation-icon.png`, All Script=`BoxConversationList.png`, New Box=`BoxD.png`, Copy=`BoxCopy.png`, Cut=`BoxCut.png`, Paste=`BoxPaste.png`, Replace Box=`BoxInsert.png`, Select All Box=`BoxSelectAll.png`, Parked=`BoxConversation.png`); **`Q-16`** (remove 3x duplicate `NGUI Glossary` + Project Lead approval of full old-to-new command/shortcut/regression inventory BEFORE restructuring Main Menu); **`Q-17`** (complete missing tooltips + preserve Project Lead's "3-layer tooltip" meaning — NOT 3 font sizes — with approved written definition proposal before implementation). |
| 5 | **`S12`** | `<final_pre_s12>` (e.g. `v1.4.14`) -> `v1.5.0` (Conditional) | Strictly read-only audit of production source (`misora.py`, `core/*.py`, `assets/*`); ONLY the 3 pre-approved non-fixture test-hygiene fixes + optional stress guards + docs; full `S01`–`S11e` traceability (`U-01`..`U-20`, `Q-01`..`Q-18`, `Q-22`..`Q-23`); `Q-04.1.3` honest `NOT TESTED` / `NOT TESTED — WAIVED` taxonomy; baseline-relative Git verification; full 4-criterion Release Gate (Revision A). |

- **Track B (Post-`v1.5.0`, Separate Design Meetings):** `BIG-01` (MTL provider research), `BIG-02` (optional MeCab auto-furigana plugin), `BIG-03` (optional Rikaikun-style Japanese hover dictionary plugin).

======================================================================
4. FINAL SIGN-OFF REQUEST
======================================================================
Please confirm final sign-off on `Gemini2GPT_PostS11_Reconciled_v3.md`.
Upon GPT final sign-off (and Project Lead approval), Gemini will draft the bounded Antigravity prompt for `S11b` first (or the full `S11b`–`S12` prompt set) for independent prompt review before any `/plan` execution starts.