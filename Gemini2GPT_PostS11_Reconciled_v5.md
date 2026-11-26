# MISORA: STORY EDITOR — RECONCILED POST-S11 ROADMAP (v5 — FINAL SIGN-OFF EDITION)

From: Gemini (aligned with Project Lead decisions and all final corrections in GPT's v4 review)
To: ChatGPT (Independent Technical Reviewer)
Repository Baseline: `ImaterialC/Misora-Editor` `main` @ `c1ec40c96c18ae6e4df61d1db77ebf999114be3d` (`__version__ = "1.4.10"`)
Execution Boundary: RECONCILIATION ONLY. Zero Antigravity prompts generated; zero `/plan` sessions started; zero production source files modified; `v1.5.0` remains ON HOLD.

======================================================================
1. BASELINE HONESTY & PRIOR S11 EXECUTION REPORT
======================================================================
- `main` HEAD `c1ec40c96c18ae6e4df61d1db77ebf999114be3d` contains S09b (`v1.4.8`), S10 (`v1.4.9`), and S11 (`v1.4.10`).
- Previously reported S11 automated counts (**440 discovered, 397 passed, 35 fixture-blocked skips, 6 pre-existing failures, 2 pre-existing errors**; 28/28 targeted S11+XUAT; 17/17 notification+S11) are strictly **prior Antigravity/Gemini execution reports**, NOT independently re-executed by GPT.
- Manual Windows QA remains OPEN / pending explicit Project Lead sign-off.
- The 5 `tests/test_s8b2_memory_guards.py` items below reflect the Project Lead's verbatim Windows run (`py -3.12 -m unittest tests.test_s8b2_memory_guards -v`: `Ran 8 tests in 22.137s — FAILED (failures=3, errors=2)`; `test_06`, `test_07`, `test_08` passed `ok`), not independently re-run by GPT.

======================================================================
2. LOCKED SPECIFICATIONS & ALL v4 FINAL CORRECTIONS APPLIED
======================================================================

### 2.1 S12 Baseline Failure & Error Identification (Per-Method Level)
Allowed formal dispositions: `FIXED` | `PROVEN-NOT-A-BUG` | `FIXTURE-BLOCKED` | `EXPLICIT PROJECT LEAD WAIVER`.
Fixture-blocked outcomes and skips are **NEVER** reported as `PASS`.

| # | Test File & Exact Method Name | Baseline Outcome | Verbatim Failure / Error Evidence | Planned S12 Disposition |
|---|---|---|---|---|
| 1 | `tests/test_v15_s01_stability_remediation.py::test_probe_8` | `FAIL` | Stale hardcoded `"1.4.1"` expected version assertions | **`FIXED`** (full multi-module parity migration per §2.3) |
| 2 | `tests/test_phase3_performance_config.py::test_05_clean_committed_config_has_no_machine_paths` | `FAIL` | Falls back to local `misora_config.json`; inconsistent config contract | **`FIXED`** (unified Option B contract per §2.2) |
| 3 | `tests/test_s9c_workspace_safety.py::test_04_default_config_template_clean` | `FAIL` | Expects absent `misora_config.default.json`; inconsistent config contract | **`FIXED`** (unified Option B contract per §2.2) |
| 4 | `tests/test_s8b2_memory_guards.py::TestS8b2MemoryGuards.test_01_dispose_unity_env_breaks_circular_refs` | `FAIL` | Line 91: `AssertionError: False is not true : Fixture missing: D:\Misora-Editor\storydata_1001005.unity3d` | **`FIXTURE-BLOCKED`** *(unless fixture provided or `EXPLICIT PROJECT LEAD WAIVER`)* |
| 5 | `tests/test_s8b2_memory_guards.py::TestS8b2MemoryGuards.test_03_search_engine_disposes_bundle_environments` | `FAIL` | Line 150: `AssertionError: 0 not greater than or equal to 1` (0 bundle envs loaded; missing `storydata_1001005.unity3d`) | **`FIXTURE-BLOCKED`** *(unless fixture provided or `EXPLICIT PROJECT LEAD WAIVER`)* |
| 6 | `tests/test_s8b2_memory_guards.py::TestS8b2MemoryGuards.test_04_close_file_disposes_environment` | `FAIL` | Line 157: `AssertionError: unexpectedly None` (log: `[File I/O] Cannot find file: D:\Misora-Editor\storydata_1001005.unity3d`) | **`FIXTURE-BLOCKED`** *(unless fixture provided or `EXPLICIT PROJECT LEAD WAIVER`)* |
| 7 | `tests/test_s8b2_memory_guards.py::TestS8b2MemoryGuards.test_02_save_bundle_story_disposes_check_env` | `ERROR` | Line 107: `FileNotFoundError: File not found: D:\Misora-Editor\storydata_1001005.unity3d` | **`FIXTURE-BLOCKED`** *(unless fixture provided or `EXPLICIT PROJECT LEAD WAIVER`)* |
| 8 | `tests/test_s8b2_memory_guards.py::TestS8b2MemoryGuards.test_05_replace_all_disposes_environments` | `ERROR` | Line 171: `FileNotFoundError: [Errno 2] No such file or directory: 'D:\\Misora-Editor\\storydata_1001005.unity3d'` | **`FIXTURE-BLOCKED`** *(unless fixture provided or `EXPLICIT PROJECT LEAD WAIVER`)* |
| — | 35 fixture-gated skips across `tests/` | `SKIP` (35) | Missing proprietary `storydata_1001005.unity3d` fixture | **`FIXTURE-BLOCKED`** *(NEVER counted as `PASS`; requires real fixture or `EXPLICIT PROJECT LEAD WAIVER`)* |

### 2.2 Unified Repository Config Test Contract — OPTION B (CONFIRMED BY PROJECT LEAD)
Applies to both:
- `tests/test_phase3_performance_config.py::test_05_clean_committed_config_has_no_machine_paths`
- `tests/test_s9c_workspace_safety.py::test_04_default_config_template_clean`

**Authoritative Contract (Option B):**
1. **No committed config template:** Neither `misora_config.json` nor `misora_config.default.json` is tracked in Git. Deleting a local config file cleanly regenerates defaults from in-code defaults (intentional hard-reset mechanism).
2. **Full Default-Configuration Verification (Not `DEFAULT_PREFS` Alone):**
   - Assert repository absence policy: neither `misora_config.json` nor `misora_config.default.json` is tracked in Git (never using an artificial temporary file as evidence that a repository-owned template is clean).
   - Inspect **ALL** default application configuration structures and relevant path/MTL defaults produced by `_load_user_prefs()` / default app initialization (not only `DEFAULT_PREFS`, since `DEFAULT_PREFS` does not cover every application config/path/MTL attribute), asserting zero machine-specific paths, zero personal/local paths, zero secrets/API keys, and zero retired keys (e.g., `console_visible`), plus clean regeneration when a temp config is absent.
   - Remove the unsafe fallback to user-local `misora_config.json` completely.
3. **Strict User-Config Safety:** Tests MUST NEVER read, fall back to, overwrite, restore, or modify the user's local `misora_config.json`.

### 2.3 Complete S01 Version Test Migration (`tests/test_v15_s01_stability_remediation.py::test_probe_8`)
In S12, migrate **EVERY** version assertion in `test_probe_8` to use root `__init__.__version__` as the expected value and verify parity across:
1. Root `__init__.__version__` (semver validated)
2. `misora.__version__`
3. `splash._VERSION`
4. `mtl_engine.APP_VERSION`
5. About dialog version text
- Zero hardcoded `"1.4.1"` expected values may remain anywhere in `test_probe_8`.

### 2.4 `Q-22` (`S11c`) — Corrected `Box.clean_text` Projection Reference & Canonical Mutation Contract
- **Corrected Source Reference (`core/story_ast.py`):**
  * `Box.text` joins existing `Seg.text` values (`parts = [s.text for s in self.segs if s.text]; return "".join(parts)`).
  * `Box.clean_text` returns `game_to_xuat(self.text)`.
  * *(Note: `game_to_xuat("".join(s for s in self.seg_texts if s))` belongs to `BoxSnapshot.clean_text`, NOT `Box.clean_text`.)*
- **Locked `S11c` Contract (No Model Architecture Change):**
  1. Quick Edit initial display MUST use the existing **`box.clean_text`** projection already used by the main Dialogue Editor (do NOT independently reconstruct segment text).
  2. Capture complete `old_snapshot = BoxSnapshot.from_box(box)` (`seg_texts`, `raw_breaks`, `extra_args`, `speaker`, `voice_cue`, `kind`) **strictly BEFORE the first live mutation**.
  3. Mutate via canonical `self.current_doc.inject_box(idx, None, new_tx)` (without `seg_texts`).
  4. Capture fresh `new_snapshot = BoxSnapshot.from_box(updated_box)` from the actually updated AST on commit/flush into ONE logical `BoxSnapshotReplaceDelta` Undo transaction.
  5. Undo (`replace_box()`) restores the exact original multi-segment split; Redo restores the exact edited state; binary round-trip (`to_binary()` -> `from_binary()`) passes verbatim; immutable JP source keys and `_locked_box_uids` survive Edit/Undo/Redo; S09b Translation Lock Parity (Row 1) and Pin independence are preserved.
  6. Include the mandatory **Manual Dialogue vs Quick Edit parity test** asserting identical AST (`records`, `boxes`, `seg_texts`, `raw_breaks`) and identical serialized binary output for identical initial documents and edits.
  7. Audit and migrate ALL Quick Edit references in BOTH `tests/test_v15_s10_all_script_quick_edit.py` and `tests/test_v15_s08_release_gate_stress.py` (including `_qe_seg_widgets[0]`).

### 2.5 `Q-01` (`S11b`) — Self-Contained XUAT Scanner Boundary, Exclusions & Metric Contract
- **Strict Directory Boundary:** Preserve the repository's existing **`Translation\en\Text`** boundary (matching `C:\[Gacha]\PriconneRe-TL\src\BepInEx\Translation\en\Text`). Do NOT silently broaden language scope. Explicitly test all 5 root entry points (`Game Root`, `BepInEx`, `Translation`, `Translation\en`, `Translation\en\Text`), deduplication of overlapping roots/files, and negative proof that `Translation\en\Other` and `Translation\en\RedirectedResources` are never scanned.
- **Additive File Exclusions:** Add the 5 official XUAT rule-file exclusions (`*.font.txt`, `*.resizer.txt`, `*Postprocessors.txt`, `*Preprocessors.txt`, `*Substitutions.txt`) **WITHOUT removing any existing scanner exclusions** (`.missing.txt`, `.report.txt`, `_summary.txt`, `_warnings.txt`, `.bak_`, etc.).
- **Self-Contained Metric & Normalization Contract:**
  * **Authoritative Normalization:** All unique/duplicate key accounting MUST use `core/xuat_index.py::normalize_xuat_key(raw_key, strip_ngui=True)` (the exact canonical normalization key used by `XuatIndex.by_norm_key`).
  * **Invalid / Empty Normalized Key Guard:** Any parsed line whose `normalize_xuat_key(raw_key, strip_ngui=True)` is empty/invalid (`""`) MUST be skipped **BEFORE** incrementing `entries_read` or inserting into `by_norm_key`, so invalid/empty normalized keys can NEVER silently break the metric identity.
  * **Exact Definitions:**
    - `files_scanned`: count of eligible `.txt` files actually processed under `Translation\en\Text` after root and file deduplication.
    - `entries_read`: total count of valid translation entries (with non-empty canonical normalized key) parsed across all scanned files.
    - `unique_keys`: count of distinct non-empty canonical normalized keys (`len(by_norm_key)`).
    - `duplicate_keys`: count of distinct canonical normalized keys that have more than one parsed entry (`sum(1 for entries in by_norm_key.values() if len(entries) > 1)`).
    - `duplicate_entries`: count of redundant occurrences after the first entry for each key (`entries_read - unique_keys`).
  * **Required Tested Identity:** `entries_read == unique_keys + duplicate_entries` (verified directly by unit tests including single entries, multi-file duplicates, 3x duplicates, excluded rule files, and empty/invalid normalized keys).

### 2.6 Complete Reconciled S12 Release Gate & Promotion Contract (All 8 Mandatory Conditions Restored)
*(The standalone S12 prompt will be rewritten to match this exact contract after roadmap sign-off.)*
- **Pre-S12 Version Baseline:** Exact final pre-S12 version installed in `__init__.py` after Track A completes (target `1.4.14`, or dynamically matching the actual final `__version__` if any `S11b` STOP gate spins off an additional bounded session). Conditional promotion: `<final_pre_s12_version>` -> `1.5.0`.
- **Full Traceability Scope:** `S01`–`S11e` (plus any STOP-gate spin-off), `U-01`–`U-20`, `RM-01`, `Q-01`–`Q-18`, `Q-22`, `Q-23`, and all migrated tests.
- **Strict S12 File Ownership Boundary (No Open-Ended Edits):**
  * **Strictly READ-ONLY:** ALL production source (`misora.py`, `core/*.py`, `assets/*`), `requirements.txt`, `misora_config.json`, `backups/`, AND `tests/test_v15_s08_release_gate_stress.py` (no open-ended stress-test edits unless specifically authorized in writing by Project Lead beforehand).
  * **ONLY Permitted Edits in S12:**
    1. `tests/test_v15_s01_stability_remediation.py` (`test_probe_8` full parity migration per §2.3),
    2. `tests/test_phase3_performance_config.py` (`test_05` unified Option B contract per §2.2),
    3. `tests/test_s9c_workspace_safety.py` (`test_04` unified Option B contract per §2.2),
    4. Ledger & documentation updates (`AGENTS.md`, `PROJECT_STATE.md`, `CHANGELOG.md`, `README.md`),
    5. Conditional `__init__.py` version promotion (`<final_pre_s12_version>` -> `"1.5.0"`) ONLY if ALL 8 Release Promotion Conditions below are satisfied AND Project Lead explicitly authorizes promotion.
- **Hard-Stop Audit Rule:** Any newly discovered P0/P1 production defect or confirmed memory leak in `misora.py`, `core/*.py`, or `assets/*` is recorded with `file:line` proof as a Release Gate BLOCKER for a separate bounded fix session — NEVER silently patched in S12.
- **ALL 8 Mandatory Release Promotion Conditions (ALL REQUIRED — NONE OPTIONAL):**
  1. **Zero New Regressions:** `0` new regressions compared with the documented baseline.
  2. **Written Disposition for Every Baseline Failure/Error:** Every item in §2.1 has an explicit written disposition (`FIXED`, `PROVEN-NOT-A-BUG`, `FIXTURE-BLOCKED`, or `EXPLICIT PROJECT LEAD WAIVER`).
  3. **All Non-Fixture Automated Tests Pass:** Every non-fixture automated test passes with `0` unexpected failures and `0` unexpected errors.
  4. **Fixture-Dependent Tests Genuinely Run or Explicitly Waived:** Fixture-dependent tests (`storydata_1001005.unity3d`, including the 5 `test_s8b2_memory_guards` items and 35 fixture skips) are genuinely executed with the real fixture OR explicitly waived in writing by the Project Lead. Fixture-blocked items and skips NEVER count as `PASS`.
  5. **Zero Unresolved P0/P1 Defects or Memory Leaks:** Zero unresolved P0/P1 production source defects or confirmed memory leaks from the S12 read-only audit.
  6. **Manual Windows QA Completed or Validly Waived:** Manual Windows QA checklist is completed and explicitly confirmed by the Project Lead, OR every individually eligible untested item (such as `Q-04.1.3`) has a valid documented waiver labeled **`NOT TESTED — WAIVED`** (NEVER `PASS`). Non-waivable safety defects remain hard blockers.
  7. **Exact Test Counts Reported Verbatim:** Exact discovered, executed, passed, skipped, failed, and errored counts are reported (never pass-rate percentages alone).
  8. **Baseline-Relative Git Integrity:** `git status --short` (compared baseline-relatively against the pre-session snapshot, preserving pre-existing local/untracked files) matches the exact S12 Allowed Files boundary; zero unauthorized modifications are permitted.
- **Non-Waivable Safety Restrictions & Waiver Record Schema:**
  * Active P0 data corruption, binary round-trip failures, crash/hang defects, and destructive-cleanup safety regressions are **STRICTLY NON-WAIVABLE** for `v1.5.0`.
  * Every eligible waiver (`NOT TESTED — WAIVED` or `FIXTURE-BLOCKED — WAIVED`) MUST be recorded in `PROJECT_STATE.md` and `CHANGELOG.md` with: (1) Exact Item ID / test method name, (2) Honest status label (never `PASS`), (3) Reason & risk assessment, (4) Compensating evidence (if any), (5) Scope/expiration (`v1.5.0` gate only; does not auto-carry to `v1.6.0`), and (6) Explicit Project Lead authorization & date.

======================================================================
3. FINALIZED TRACK A ROADMAP (5 BOUNDED SESSIONS) & TRACK B
======================================================================
- **`S11b` (`v1.4.11`):** `Q-01` (strict `Translation\en\Text` scanner, additive 5 exclusions + preserve legacy exclusions, dedup, self-contained 5 metrics + `normalize_xuat_key` guard, 5 roots + negative `Other/` & `RedirectedResources/` tests); `Q-02` (5-stage Save Hang profiling with **STOP gate** if major async/bundle transaction refactor is needed + `Ctrl+S` Save Project `.misora` & conflict-free Save & Patch Bundle shortcut + menu/tooltips/README/tests); `Q-04` (inspect `1.1` `▶` origin without assuming removal; reproduce `1.2` selection/drag/scroll separately on multi-match >3-linebreak Name/Title/Subtitle; `1.3` strictly `NOT TESTED`); `Q-18` (Ruby Preview bug fix with **STOP gate** if custom text-layout engine is required); `Q-23` (remove red overflow blocks in `txt_dialogue_preview` + defensive guard in overflow helper + migrate `test_v15_s03_all_script_preview_paste.py` & `test_p3_s18_game_preview.py` + assert Editor Preview-OFF retains red markers, pink nameplate, gold border, pink `▼`, `54d × 3`, `wrap="none"`).
- **`S11c` (`v1.4.12`):** `Q-22` ONLY (unified single-box Quick Edit using existing `box.clean_text` projection, pre-first-mutation `old_snapshot`, canonical `inject_box(idx, None, new_tx)`, 8 AST/Undo/Lock invariants, Manual-Dialogue-vs-Quick-Edit AST+binary parity test, full audit/migration of `test_v15_s10_all_script_quick_edit.py` and `test_v15_s08_release_gate_stress.py`).
- **`S11d` (`v1.4.13`):** `Q-06` (Import MouseWheel propagation over labels/child frames), `Q-07` (per-group tri-state none/some/all Select All), `Q-08` (multi-line wrapped Synopsis Metadata Import + Skip + duplicate handling + atomic `MetadataDelta` Undo/Redo), `Q-09` (remove leftover `"Import Complete - XUAT translation Archiving"` sub-header), `Q-10` (`Select All Box` dialogue-only excluding Box 0 & preserving Lock), `Q-11` (MTL Globe button: safe clipboard copy + official provider website), `Q-12` (truncated `filename — Title (Subtitle)` in window title from already-parsed metadata).
- **`S11e` (`v1.4.14`):** `Q-03` (per-widget-class word-wrap contract), `Q-05` (Splash Screen remains visible until ALL UI/UX + previous-session state restoration finish, honest non-blocking progress + artificially slowed startup acceptance test), `Q-13` (bold/larger `PriconneRe:TL` + `Cornelia` on Splash & About), `Q-14` (`Support the Creator`, full English copy, ~600px aspect-preserving Pillow GIF, no FFmpeg/OpenCV), `Q-15` (corrected icon map verified on disk for exact filenames/extensions/alpha/dimensions: Translate=`language-translation-icon.png`, All Script=`BoxConversationList.png`, New Box=`BoxD.png`, Copy=`BoxCopy.png`, Cut=`BoxCut.png`, Paste=`BoxPaste.png`, Replace Box=`BoxInsert.png`, Select All Box=`BoxSelectAll.png`, Parked=`BoxConversation.png`), `Q-16` (remove 3x duplicate `NGUI Glossary` + Project Lead approval of complete old-to-new command/shortcut/regression inventory before restructuring Main Menu), `Q-17` (complete missing tooltips + preserve Project Lead's "3-layer tooltip" meaning — NOT 3 font sizes — with approved written definition proposal before implementation).
- **`S12` (`<final_pre_s12>` e.g. `v1.4.14` -> Conditional `v1.5.0`):** Strictly governed by §2.1–§2.6 above.
- **Track B (Post-`v1.5.0`, Separate Design Meetings):** `BIG-01` (MTL provider research), `BIG-02` (optional MeCab auto-furigana plugin), `BIG-03` (optional Rikaikun-style hover dictionary plugin).

======================================================================
4. NEXT-STEP COMMITMENT & FINAL SIGN-OFF REQUEST
======================================================================
Upon GPT final sign-off on `Gemini2GPT_PostS11_Reconciled_v5.md`, Gemini will draft **ONLY the bounded `S11b` Antigravity prompt first** (explicitly carrying forward all locked project invariants so previously resolved defects cannot regress), and submit that prompt for independent GPT review before any `/plan` session begins. Subsequent session prompts (`S11c`, `S11d`, `S11e`, and reconciled `S12`) will follow sequentially after each preceding session completes.