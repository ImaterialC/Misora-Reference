# MISORA: STORY EDITOR — RECONCILED POST-S11 ROADMAP (v4 — FINAL CONSISTENCY & TEST-CONTRACT LOCK)

From: Gemini (with Project Lead confirmation of Option B and verbatim `tests.test_s8b2_memory_guards` execution log)
To: ChatGPT (Independent Technical Reviewer)
Repository Baseline: `ImaterialC/Misora-Editor` `main` @ `c1ec40c` (`__version__ = "1.4.10"`)
Execution Boundary: RECONCILIATION ONLY. Zero Antigravity prompts generated; zero `/plan` sessions started; zero source files modified; `v1.5.0` remains ON HOLD until Track A completes, Manual Windows QA is completed or formally waived under Section 2.5, and S12 Release Gate satisfies every criterion.

======================================================================
1. BASELINE HONESTY & PRIOR S11 EXECUTION REPORT
======================================================================
- `main` contains S09b (`v1.4.8`), S10 (`v1.4.9`), and S11 (`v1.4.10`, commit `c1ec40c`).
- Previously reported S11 automated counts (**440 discovered, 397 passed, 35 fixture-blocked skips, 6 pre-existing failures, 2 pre-existing errors**; 28/28 targeted S11+XUAT; 17/17 notification+S11) are strictly **prior Antigravity/Gemini execution reports**, NOT independently re-executed by GPT.
- Manual Windows QA remains OPEN / pending explicit Project Lead sign-off.
- The 5 `tests/test_s8b2_memory_guards.py` items in Section 2.1 below were freshly verified verbatim on Windows by the Project Lead (`py -3.12 -m unittest tests.test_s8b2_memory_guards -v`: `Ran 8 tests in 22.137s — FAILED (failures=3, errors=2)`; `test_06`, `test_07`, `test_08` passed `ok`).

======================================================================
2. ALL 5 FINAL REFINEMENTS FROM `GPT2Gwmini5.txt` APPLIED
======================================================================

### 2.1 S12 Baseline Failure & Error Identification (Per-Method Level — Verbatim Evidence)
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

*(Exact 3 FAIL + 2 ERROR distinction in `tests/test_s8b2_memory_guards.py`: FAILs = `test_01`, `test_03`, `test_04`; ERRORs = `test_02`, `test_05`; PASS = `test_06`, `test_07`, `test_08`.)*

### 2.2 Unified Repository Config Test Contract — OPTION B CONFIRMED BY PROJECT LEAD
Both config tests previously conflicted because neither `misora_config.default.json` nor `misora_config.json` is committed to the repository, and `test_05` could fall back to reading a user's local `misora_config.json`:
- `tests/test_phase3_performance_config.py::test_05_clean_committed_config_has_no_machine_paths`
- `tests/test_s9c_workspace_safety.py::test_04_default_config_template_clean`

**Authoritative Contract — OPTION B (CONFIRMED BY PROJECT LEAD):**
1. **No committed config template is intended:** Neither `misora_config.json` nor `misora_config.default.json` is tracked in Git. When no local config file exists, Misora automatically generates clean defaults from in-code `misora.DEFAULT_PREFS` — which also serves intentionally as a clean **user hard-reset mechanism** (deleting `misora_config.json` cleanly resets configuration if a user encounters issues).
2. **Unified test contract enforced by BOTH tests:**
   - Assert the explicit repository absence policy: neither `misora_config.json` nor `misora_config.default.json` is tracked/committed in Git (e.g., via `git ls-files` / absence policy check — NEVER using an artificial temporary file as evidence that a repository-owned template is clean).
   - Assert clean in-code default generation: `misora.DEFAULT_PREFS` and freshly generated default config objects contain zero machine-specific paths, zero personal/local paths, zero secrets/API keys, and zero retired keys (such as `console_visible`), and deleting a temp config cleanly regenerates defaults.
   - Remove the unsafe fallback to local `misora_config.json` completely.
3. **Strict User-Config Safety:** Tests MUST NEVER read, fall back to, overwrite, restore, or modify the user's local `misora_config.json`.

### 2.3 Complete S01 Version Test Migration (`tests/test_v15_s01_stability_remediation.py::test_probe_8`)
In S12, migrate **EVERY** version assertion inside `test_probe_8` (not only `_read_root_version()`) to compare against root `__init__.__version__`, verifying exact parity across all five surfaces:
1. Root `__init__.__version__` (expected source of truth, semver validated)
2. `misora.__version__`
3. `splash._VERSION`
4. `mtl_engine.APP_VERSION`
5. About dialog rendered version text
- **Hard Requirement:** Zero hardcoded `"1.4.1"` expected version literals may remain anywhere in `test_probe_8`.

### 2.4 Reconciled S12 Acceptance Contract (Aligned with v3 Revisions A–D & v4)
*(The standalone S12 Antigravity prompt file will be rewritten to match this exact contract ONLY after GPT gives final sign-off on v4.)*
- **Pre-S12 Version Baseline:** Exact final pre-S12 version installed in `__init__.py` after Track A completes (target `1.4.14`, or dynamically matching the actual final `__version__` if any `S11b` STOP gate spins off an additional bounded session). Conditional promotion: `<final_pre_s12_version>` -> `1.5.0`.
- **Full Traceability Scope:** `S01`–`S11e` (plus any STOP-gate spin-off), `U-01`–`U-20`, `RM-01`, `Q-01`–`Q-18`, `Q-22`, `Q-23`, and all migrated tests (`S03`, `S06`, `S07`, `S08`, `S10`, `S13`, `S14`, `S15`, `S17`, `S18`, `S22`, plus any tests migrated in `S11b`–`S11e`).
- **Strict S12 File Ownership Boundary (No Open-Ended Edits):**
  * **Strictly READ-ONLY:** ALL production source (`misora.py`, `core/*.py`, `assets/*`), `requirements.txt`, `misora_config.json`, `backups/`, AND **`tests/test_v15_s08_release_gate_stress.py`** (removed from open-ended S12 optional edits; may only be modified if specifically authorized in writing by Project Lead beforehand).
  * **ONLY Permitted Edits in S12:**
    1. `tests/test_v15_s01_stability_remediation.py` (`test_probe_8` full parity migration per §2.3),
    2. `tests/test_phase3_performance_config.py` (`test_05` unified Option B contract per §2.2),
    3. `tests/test_s9c_workspace_safety.py` (`test_04` unified Option B contract per §2.2),
    4. Ledger & documentation updates (`AGENTS.md`, `PROJECT_STATE.md`, `CHANGELOG.md`, `README.md`),
    5. Conditional `__init__.py` version promotion (`<final_pre_s12_version>` -> `"1.5.0"`) ONLY if all 4 Release Gate criteria pass AND Project Lead explicitly authorizes promotion.
- **Hard-Stop Audit Rule:** Any newly discovered P0/P1 source bug or memory leak in `misora.py`, `core/*.py`, or `assets/*` is recorded with `file:line` proof as a Release Gate BLOCKER for a separate bounded fix session — NEVER silently patched in S12.
- **4 Mandatory S12 Release Gate Criteria (ALL REQUIRED):**
  1. `0` new regressions relative to baseline.
  2. Explicit written disposition (`FIXED`, `PROVEN-NOT-A-BUG`, `FIXTURE-BLOCKED`, or `EXPLICIT PROJECT LEAD WAIVER`) for every single baseline failure/error in §2.1.
  3. Fixture-blocked skips (`35`) are NEVER counted as `PASS`.
  4. Exact discovered, executed, passed, skipped, failed, and errored test counts reported verbatim (never percentages alone), alongside baseline-relative `git status --short` verification.

### 2.5 Closure of Remaining Scope Ambiguities
1. **Removed Open-Ended Optional S12 Stress-Test Edits:** Locked in §2.4 above (`tests/test_v15_s08_release_gate_stress.py` is read-only in S12 unless explicitly authorized by Project Lead).
2. **Explicit Manual Windows QA Waiver Policy & Documentation Schema:**
   - **Eligible Scope:** Manual QA items that cannot be executed prior to release (e.g., `Q-04.1.3`) or missing proprietary fixture tests (`storydata_1001005.unity3d`).
   - **Non-Waivable Scope:** Active P0 data-corruption, binary-roundtrip failure, crash/hang defects, or unverified destructive-cleanup safety regressions may NOT be waived for `v1.5.0`.
   - **Mandatory Written Record (in `PROJECT_STATE.md` and `CHANGELOG.md` Release Notes):** Every waiver MUST record:
     1. Exact Item ID (`Q-04.1.3`, or exact test method name from §2.1),
     2. Honest status label: **`NOT TESTED — WAIVED`** (for manual QA) or **`FIXTURE-BLOCKED — WAIVED`** (for fixture tests) — **NEVER `PASS`**,
     3. Explicit reason for waiver & risk assessment,
     4. Compensating automated or prior evidence (if any),
     5. Waiver scope/expiration (valid for `v1.5.0` release gate only; does not auto-carry to `v1.6.0`),
     6. Explicit Project Lead authorization statement & date.
3. **Preserve Exact XUAT `Translation\en\Text` Boundary (`Q-01`):**
   - `Q-01` MUST strictly preserve the repository's existing **`Translation\en\Text`** boundary (matching current `core/xuat_index.py` resolver and Project Lead's game path `C:\[Gacha]\PriconneRe-TL\src\BepInEx\Translation\en\Text`).
   - Do **NOT** silently broaden language scope to arbitrary `Translation\<lang>\Text` directories in `Q-01`.
   - Additive exclusions (`*.font.txt`, `*.resizer.txt`, `*Postprocessors.txt`, `*Preprocessors.txt`, `*Substitutions.txt`) are added WITHOUT removing existing exclusions (`.missing.txt`, `.report.txt`, `_summary.txt`, `_warnings.txt`, `.bak_`).
   - Test all 5 root entry points (`Game Root`, `BepInEx`, `Translation`, `Translation\en`, `Translation\en\Text`), overlapping root/file deduplication, exact metrics (`files_scanned`, `entries_read`, `unique_keys`, `duplicate_keys`, `duplicate_entries` with `entries_read == unique_keys + duplicate_entries`), and negative proof that `Translation\en\Other` and `Translation\en\RedirectedResources` are never scanned.
4. **Exact Canonical Text-Projection Helper for `Q-22` (`S11c`):**
   - The canonical model-layer unified text projection is **`core/story_ast.py::Box.clean_text`** (`game_to_xuat("".join(s for s in self.seg_texts if s))`), which is the exact source rendered into `txt_dialogue` and checked by `on_save()`.
   - `Quick Edit` MUST populate its single unified `tk.Text` through the **exact same single projection helper** used by the main Dialogue Editor (`box.clean_text`, verified on disk during `S11c` `/plan` so zero divergence exists between `txt_dialogue` and `Quick Edit`), capture `old_snapshot = BoxSnapshot.from_box(box)` **strictly before the first live mutation**, mutate via canonical `self.current_doc.inject_box(idx, None, new_tx)` (without `seg_texts`), capture fresh `new_snapshot = BoxSnapshot.from_box(updated_box)` on commit/flush into ONE logical `BoxSnapshotReplaceDelta`, verify Manual-Dialogue-vs-Quick-Edit AST & binary parity, and audit/migrate BOTH `tests/test_v15_s10_all_script_quick_edit.py` and `tests/test_v15_s08_release_gate_stress.py`.

======================================================================
3. FINALIZED TRACK A ROADMAP (5 BOUNDED SESSIONS) & TRACK B
======================================================================
- **`S11b` (`v1.4.11`):** `Q-01` (strict `Translation\en\Text` scanner, additive 5 exclusions + preserve legacy exclusions, dedup, exact 5 metrics, 5 roots + negative `Other/` & `RedirectedResources/` tests); `Q-02` (5-stage Save Hang profiling with **STOP gate** if major async/bundle transaction refactor is needed + `Ctrl+S` Save Project `.misora` & conflict-free Save & Patch Bundle shortcut + menu/tooltips/README/tests); `Q-04` (inspect `1.1` `▶` origin without assuming removal; reproduce `1.2` selection/drag/scroll separately on multi-match >3-linebreak Name/Title/Subtitle; `1.3` strictly `NOT TESTED`); `Q-18` (Ruby Preview bug fix with **STOP gate** if custom text-layout engine is required); `Q-23` (remove red overflow blocks in `txt_dialogue_preview` + defensive guard in overflow helper + migrate `test_v15_s03_all_script_preview_paste.py` & `test_p3_s18_game_preview.py` + assert Editor Preview-OFF retains red markers, pink nameplate, gold border, pink `▼`, `54d × 3`, `wrap="none"`).
- **`S11c` (`v1.4.12`):** `Q-22` ONLY (unified single-box Quick Edit using canonical `Box.clean_text` projection, pre-first-mutation `old_snapshot`, canonical `inject_box(idx, None, new_tx)`, 8 AST/Undo/Lock invariants, Manual-Dialogue-vs-Quick-Edit AST+binary parity test, full audit/migration of `test_v15_s10_all_script_quick_edit.py` and `test_v15_s08_release_gate_stress.py`).
- **`S11d` (`v1.4.13`):** `Q-06` (Import MouseWheel propagation over labels/child frames), `Q-07` (per-group tri-state none/some/all Select All), `Q-08` (multi-line wrapped Synopsis Metadata Import + Skip + duplicate handling + atomic `MetadataDelta` Undo/Redo), `Q-09` (remove leftover `"Import Complete - XUAT translation Archiving"` sub-header), `Q-10` (`Select All Box` dialogue-only excluding Box 0 & preserving Lock), `Q-11` (MTL Globe button: safe clipboard copy + official provider website), `Q-12` (truncated `filename — Title (Subtitle)` in window title from already-parsed metadata).
- **`S11e` (`v1.4.14`):** `Q-03` (per-widget-class word-wrap contract), `Q-05` (Splash Screen remains visible until ALL UI/UX + previous-session state restoration finish, honest non-blocking progress + artificially slowed startup acceptance test), `Q-13` (bold/larger `PriconneRe:TL` + `Cornelia` on Splash & About), `Q-14` (`Support the Creator`, full English copy, ~600px aspect-preserving Pillow GIF, no FFmpeg/OpenCV), `Q-15` (corrected icon map verified on disk for exact filenames/extensions/alpha/dimensions: Translate=`language-translation-icon.png`, All Script=`BoxConversationList.png`, New Box=`BoxD.png`, Copy=`BoxCopy.png`, Cut=`BoxCut.png`, Paste=`BoxPaste.png`, Replace Box=`BoxInsert.png`, Select All Box=`BoxSelectAll.png`, Parked=`BoxConversation.png`), `Q-16` (remove 3x duplicate `NGUI Glossary` + Project Lead approval of complete old-to-new command/shortcut/regression inventory before restructuring Main Menu), `Q-17` (complete missing tooltips + preserve Project Lead's "3-layer tooltip" meaning — NOT 3 font sizes — with approved written definition proposal before implementation).
- **`S12` (`<final_pre_s12>` e.g. `v1.4.14` -> Conditional `v1.5.0`):** Strictly governed by §2.1–§2.5 above.
- **Track B (Post-`v1.5.0`, Separate Design Meetings):** `BIG-01` (MTL provider research), `BIG-02` (optional MeCab auto-furigana plugin), `BIG-03` (optional Rikaikun-style hover dictionary plugin).

======================================================================
4. FINAL SIGN-OFF REQUEST
======================================================================
All 5 refinements from `GPT2Gwmini5.txt` are now locked with verbatim test-method evidence and Project Lead confirmation of Option B. Please provide final independent sign-off on `Gemini2GPT_PostS11_Reconciled_v4.md` so Gemini may draft the bounded Antigravity prompts (`S11b`–`S11e` and reconciled `S12`) for independent prompt review before any `/plan` execution begins.