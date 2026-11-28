# T-01 (`BUG-UI-EMPTY-STATE-01`) Execution Walkthrough

- **Product:** Misora: Story Editor (`__version__ == "1.4.15"` unchanged; `v1.5.0` remains `CANCELLED / NOT RELEASED / VERSION PROMOTION NOT AUTHORIZED`)
- **Repository:** `D:\Misora-Editor` (`main` @ `648cb52b0fccda5e46e26eecf90e3f1dbd719a75`)
- **Plan Reference:** `D:\Reference\Misora-Reference\T-01_Implementation_Plan.md` (Rev 3)
- **Status:** Automated fix & TDD `PASS` (`11/11`); Windows Manual QA `M-1..M-12` `MANUAL-PENDING`; T-01 Lifecycle remains `ACTIVE` until manual QA passes.

---

## 1. Root Cause & Surgical Fix

- **Root Cause (`CONFIRMED`):** In `MisoraApp._update_empty_state_visibility()` (`misora.py:9763-9786`), all 8 container-visibility checks used `winfo_ismapped()`. Whenever the root `Tk` window is withdrawn (initial startup, splash screen, `_deferred_restore()`), `winfo_ismapped()` returns `0` for all descendants regardless of whether they are packed. This caused `pack_forget()` to be skipped and redundant `pack()` calls to leave `gd_scroll_wrap` and `empty_state_frame` dual-packed inside `top_view`.
- **Fix Applied (`misora.py:9767-9785`):** Replaced all 8 `winfo_ismapped()` calls with explicit `winfo_manager() == "pack"` / `!= "pack"` checks.
- **V-2 / C-5 / C-6 Checks:**
  - `git diff --numstat -- misora.py`: `8	8	misora.py`
  - `misora.py` line count: `23912` (preserved)
  - C-6 3-container check (`empty_state_frame`, `gd_scroll_wrap`, `continuous_wrap`): `29` matching lines, `0` `.grid`/`.place` calls (`pack`-only invariant intact).

---

## 2. Files Changed (Strict 4-File Ownership)

1. `misora.py` — 8-line fix in `_update_empty_state_visibility()` (`8	8	misora.py`).
2. `tests/test_t01_empty_state_overlay.py` — created 11 stdlib `unittest` methods (4 real-`MisoraApp` Defect Probes + 7 Regression Guards, synthetic `.v2.txt` fixtures, zero `.unity3d` dependency, zero `skipTest()`).
3. `docs/project/OPEN_ISSUES.md` — updated T-01 (`CONFIRMED`, automated `PASS`, `M-1..M-12` `MANUAL-PENDING`, `ACTIVE`, N-4 transient `--check` note).
4. `PROJECT_STATE.md` — updated verification baseline (`486 = 475 + 11`), T-01 status, `MANUAL-PENDING` QA, and N-4 note.

---

## 3. Verbatim Verification Outputs

### 3.1 Pre-Patch Baseline & Failing-First TDD Gate
- `pre_pyc_count: 123`
- `IN-MEMORY COMPILE OK: 86 files` (BOM-safe `utf-8-sig`, zero `.pyc` emitted)
- `countTestCases: 486` (`475` baseline + `11` new T-01 tests)
- `py -3.12 -B -m unittest tests.test_t01_empty_state_overlay.TestT01DefectProbes -v`:
  ```text
  Ran 4 tests in 13.695s

  FAILED (failures=4)
  ```
  (All 4 probes failed on exact `AssertionError: 'pack' != ''`, 0 errors.)
- `py -3.12 -B -m unittest tests.test_t01_empty_state_overlay.TestT01RegressionGuards -v`:
  ```text
  Ran 7 tests in 19.917s

  OK
  ```

### 3.2 Post-Patch Verification
- `git diff --numstat -- misora.py`:
  ```text
  8	8	misora.py
  ```
- `misora.py lines: 23912`
- Broad BOM-safe in-memory compile check (C-3):
  ```text
  IN-MEMORY COMPILE OK: 86 files
  ```
- `py -3.12 -B -m unittest tests.test_t01_empty_state_overlay -v`:
  ```text
  Ran 11 tests in 25.548s

  OK
  ```
- Targeted UI regression suites (`tests.test_p3_s15_selection_drawer_open`, `tests.test_v15_s11e_polish_splash_menu_tooltips`, `tests.test_p3_s04_ast_mutations`, `tests.test_v15_s04_layout_drawer_controls`, `tests.test_t01_empty_state_overlay`):
  ```text
  Ran 38 tests in 67.224s

  OK
  ```
- Full test suite (`py -3.12 -B -m unittest discover -s tests -v`):
  ```text
  Ran 486 tests in 599.467s

  FAILED (failures=6, errors=2, skipped=35)
  ```
  - Exact breakdown: `486 total = 443 PASS + 35 SKIP + 6 FAIL + 2 ERROR` (`+11 PASS` over S11e baseline `475 = 432 PASS + 35 SKIP + 6 FAIL + 2 ERROR`; `0` new failures, errors, or skips; monolithic discovery completed with zero `Tcl_AsyncDelete` abort).
  - Pre-existing baseline debt unchanged:
    - 3 non-fixture hygiene failures: `test_phase3_performance_config.py::test_05`, `test_s9c_workspace_safety.py::test_04`, `test_v15_s01_stability_remediation.py::test_probe_8`
    - 3 fixture failures + 2 fixture errors in `test_s8b2_memory_guards.py::test_01..test_05` + 35 fixture skips (missing `storydata_1001005.unity3d`).
- `countTestCases: 486`
- `post_pyc_count: 123` (`== pre_pyc_count`, `0` new `.pyc` files).

---

## 4. Limitations, N-4 Note & Rollback

- **Compile check scope (C-3):** In-memory `compile()` verifies syntax without writing `.pyc` files; it does not emit `compileall` `SyntaxWarning`s.
- **N-4 Symbol Index Note:** `tools/generate_symbol_index.py --check` was NOT run post-patch because `misora.py` has uncommitted edits; `--check` is expected to exit non-zero until Project Lead commits T-01 and regenerates `docs/architecture/MISORA_SYMBOL_INDEX.md`.
- **Rollback:** Revert the 8 lines in `misora.py:9767-9785` back to `winfo_ismapped()`, remove `tests/test_t01_empty_state_overlay.py`, and restore `docs/project/OPEN_ISSUES.md` / `PROJECT_STATE.md`.

---

## 5. Manual Windows QA Checklist (`M-1..M-12` — `MANUAL-PENDING`)

T-01 remains `ACTIVE` until a Windows operator verifies on `v1.4.15`:
- [pass] `M-1`: Launch with 0 open docs (`show_splash=False`) -> only centered Open Files empty state visible; no lower purple button bleed.
- [pass] `M-2`: Launch with splash (`show_splash=True`) and 0 open docs -> empty state visible after reveal.
- [pass] `M-3`: Launch with splash + 2 saved session docs (`_deferred_restore()`) -> Dialogue editor + `clean_scroll_x` cleanly visible, empty state completely hidden.
- [pass] `M-4`: Open 1 doc from empty state -> Box 1 Dialogue + `clean_scroll_x` visible, no empty-state overlap.
- [pass] `M-5`: Open 2nd doc, switch between docs, close 1st doc -> active editor remains clean.
- [pass] `M-6`: Close last doc from Dialogue view -> empty state cleanly returns.
- [pass] `M-7`: Switch Dialogue -> All Script -> Dialogue with open doc -> clean mutual exclusion.
- [pass] `M-8`: Close last doc from All Script view -> empty state cleanly returns.
- [pass] `M-9`: Resize window / snap half-screen in 0-doc and 1-doc states -> no overlap or clipping.
- [pass] `M-10`: Open Box 0 Summary vs Box 1 Dialogue -> lower `clean_scroll_x` border unobscured.
- [pass] `M-11`: Verify 125% DPI scaling on Windows -> empty state centered, no bleed.
- [ ] `M-12`: Record OS, DPI, build (`1.4.15`), and operator sign-off in `docs/project/OPEN_ISSUES.md`.


## Tester environtment:
- W11 Microsoft Windows [Version 10.0.26100.6725]
- DPI 125 (1920x1080)
- 1.4.15
- Project lead
