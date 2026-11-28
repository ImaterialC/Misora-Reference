# T-02 (`u-08`) Execution Walkthrough

**Task:** T-02 (legacy ref `u-08`) — Stale `50 x 3` / `50 digit-widths` overflow indicator tooltip & docstrings  
**Charter:** T-02 Execution Charter (Rev 3) on `v1.4.15`, baseline HEAD `8b75b9e61728f4a5a78d06901b7e7e5006343122`  
**Product version:** `1.4.15` (`__init__.py` unchanged; `v1.5.0` remains `CANCELLED / NOT RELEASED / VERSION PROMOTION NOT AUTHORIZED`)  
**Date:** 2026-11-28

---

## 1. Summary of Changes

1. **`misora.py`** (`5	5	misora.py`, `23912` lines preserved, pure CRLF `23911 == 23911`):
   - **Lines 5577–5578 (`lbl_char_overflow` tooltip):** Converted hardcoded `"Native 50 x 3 dialogue rule: <= 50 digit-widths..."` to dynamic f-string using `DIALOGUE_MAX_DIGITS` (`54`) and `DIALOGUE_MAX_LINES` (`3`), and updated line 5578 (plain string, no `f` prefix) to describe the dual-font measurement scheme accurately:
     `"Line widths measured in the active editor font against a fixed reference boundary calibrated to the in-game box (NGUI tags excluded)."`
   - **Line 13423 (`_get_ruler_measure_font` docstring):** Updated `50d` → `54d`.
   - **Line 13525 (`_update_char_overflow_indicator` docstring):** Updated `50d` → `54d`.
   - **Line 13607 (`_draw_single_pixel_ruler` docstring):** Updated `50 digit-width` → `54 digit-width`.
2. **`tests/test_t02_next_tooltip.py`** (NEW — 8 stdlib `unittest` tests: 4 Defect Probes + 4 Regression Guards):
   - Uses deterministic `widget._tooltip.text` (no `gc.get_objects()`), zero `.unity3d` fixtures, zero `skipTest()`, `app.destroy()` + temp dir cleanup in `tearDown`.
3. **`docs/project/OPEN_ISSUES.md`:** Updated T-02 row ONLY (`Evidence: CONFIRMED`, `Lifecycle: ACTIVE`, automated TDD `PASS (8/8)`, Windows hover QA `M-1..M-4: MANUAL-PENDING`, S09 calibration note, N-4 transient `--check` note). T-01's completed `M-1..M-12` closeout was left untouched.
4. **`PROJECT_STATE.md`:** Updated discovery count `486` → `494` (`451 PASS + 35 SKIP + 6 FAIL + 2 ERROR`, `0` new T-02 regressions), added T-02 status + N-4 transient `--check` note.

---

## 2. Verbatim Verification Transcript

### 2.1 Preflight (at HEAD `8b75b9e61728f4a5a78d06901b7e7e5006343122`)

```
8b75b9e61728f4a5a78d06901b7e7e5006343122
pre_pyc_count: 123
countTestCases: 486
CHECK PASS: docs/architecture/MISORA_SYMBOL_INDEX.md
SYM_EXIT:0
```

### 2.2 Pre-Patch Zero-`.pyc` TDD (4 Probes FAIL, 4 Guards PASS)

```
COMPILE_OK: 87
pyc_count: 123
countTestCases: 494
...
Ran 8 tests in 31.059s

FAILED (failures=4)
```

All 4 defect probes (`test_probe_1`..`test_probe_4`) failed pre-patch on the stale `50`/`50d` strings; all 4 regression guards (`test_guard_1`..`test_guard_4`) passed.

### 2.3 Post-Patch Locks & T-02 Suite

```
COMPILE_OK: 87
pyc_count: 123
lines: 23911 CRLF: 23911 LF: 23911
misora_lines: 23912
5	5	misora.py
...
Ran 8 tests in 28.288s

OK
```

### 2.4 Targeted UI Suites (`test_v15_s11e_polish_splash_menu_tooltips`, `test_v15_s02_fonts_ruler_metrics`)

```
Ran 17 tests in 43.247s

OK
```

### 2.5 Full Discovery Suite (`py -3.12 -B -m unittest discover -s tests -v`)

```
Ran 494 tests in 850.967s

FAILED (failures=6, errors=2, skipped=35)
```

Exact breakdown: **494 total = 451 PASS + 35 SKIP + 6 FAIL + 2 ERROR** (`+8 PASS` over T-01 baseline `486`; `0` new failures, errors, or skips).

---

## 3. Rollback Notes

If rollback is required before commit, restore the 3 tracked files from verified pre-edit HEAD `8b75b9e61728f4a5a78d06901b7e7e5006343122` and remove the untracked test file:

```powershell
py -3.12 -B -c "import subprocess; h=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(); assert h=='8b75b9e61728f4a5a78d06901b7e7e5006343122'"
git checkout 8b75b9e61728f4a5a78d06901b7e7e5006343122 -- misora.py
Remove-Item -Path tests\test_t02_next_tooltip.py -ErrorAction SilentlyContinue
git checkout 8b75b9e61728f4a5a78d06901b7e7e5006343122 -- docs/project/OPEN_ISSUES.md
git checkout 8b75b9e61728f4a5a78d06901b7e7e5006343122 -- PROJECT_STATE.md
```

---

## 4. Manual Windows QA Checklist (`MANUAL-PENDING`)

| ID | Check | DPI | Steps | Expected | Status |
|----|-------|-----|-------|----------|--------|
| **M-1** | Tooltip text at 100% DPI | 100% | Hover over `lbl_char_overflow` (`0/54d · 1/3L` indicator) for >350ms | Tooltip reads: `"Native 54d x 3 dialogue rule: <= 54 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines)."` + `"\nLine widths measured in the active editor font against a fixed reference boundary calibrated to the in-game box (NGUI tags excluded)."` | `MANUAL-PENDING` |
| **M-2** | Tooltip text at 125% DPI | 125% | Same as M-1 | Same expected text as M-1 | `MANUAL-PENDING` |
| **M-3** | Next/Prev tooltips unaffected | 100% | Hover over Next button, then Prev button | `"Next Dialogue Box (Alt+Right / Alt+Down)"` / `"Previous Dialogue Box (Alt+Left / Alt+Up)"` unchanged | `MANUAL-PENDING` |
| **M-4** | Label text dynamic update | 100% | Type >54 characters in dialogue; verify label turns red and shows `>54/54d` | Label updates correctly; tooltip unchanged | `MANUAL-PENDING` |
