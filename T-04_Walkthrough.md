# T-04 Walkthrough — Line 4+ Overflow Highlight & `>54/54d` Boundary Fix

> **Task**: T-04 (`u-02`) — Overflow Marker on Line 4+ / >3L & `54/54d` Numerator Boundary
> **Execution Charter**: One-time Project Lead T-04 Execution Charter at `main` @ `b50c75e7555779cbff0b6821933e11b5f7ef9bf9`
> **Product**: `1.4.15` (`v1.5.0` remains `CANCELLED` / `NOT RELEASED` / `VERSION PROMOTION NOT AUTHORIZED`)
> **Date**: 2026-11-28

---

## 1  Preflight Baseline (Before Edits)

| Check | Command | Verbatim Output |
|---|---|---|
| `HEAD` | `git rev-parse HEAD` | `b50c75e7555779cbff0b6821933e11b5f7ef9bf9` |
| Working tree | `git status --short --untracked-files=all` | *(empty — clean)* |
| `.pyc` baseline | recursive `*.pyc` count | `pre_pyc_count=125` |
| Test discovery | `py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"` | `countTestCases: 504` |
| Symbol index check | `py -3.12 -B tools/generate_symbol_index.py --check` | `CHECK PASS: docs/architecture/MISORA_SYMBOL_INDEX.md` |

---

## 2  Changes Applied (Strict 4-File Ownership)

| File | Action | Diff / Summary |
|---|---|---|
| `misora.py` | **MODIFIED** | `7	4	misora.py` (`24,001` -> `24,004` logical lines; `24,003` CRLF, `bare_lf=0`, `bare_cr=0`) |
| `tests/test_t04_overflow_line4_numerator.py` | **CREATED** | 12 stdlib `unittest` tests (`4` failing-first Probes + `8` Regression Guards) with `addCleanup()` isolation |
| `docs/project/OPEN_ISSUES.md` | **MODIFIED** | `1	1	docs/project/OPEN_ISSUES.md` — T-04 row updated (`TDD 12/12 PASS`, `M-1..M-9 MANUAL-PENDING`, `Lifecycle: ACTIVE`, N-4 note) |
| `PROJECT_STATE.md` | **MODIFIED** | `17	11	PROJECT_STATE.md` (`7,439` bytes `<= 15,360` limit) — updated §2 baseline (`516`), §3 status + `Tcl_AsyncDelete` + N-4 notes, §5 `Next planned task` |

### 2.1  Exact `misora.py` Changes

1. **`_update_char_overflow_indicator()` (`misora.py:13633–13638`)**:
   - Added `d_prefix = ">" if (metrics["has_width_overflow"] and d_equiv <= DIALOGUE_MAX_DIGITS) else ""`
   - Updated label format to `f"{d_prefix}{d_equiv}/{DIALOGUE_MAX_DIGITS}d · {line_count}/{DIALOGUE_MAX_LINES}L"`.
   - Sub-digit width overflow (`pixel_width > safe_w` where `round(max_px / digit_w) <= 54`) now displays `">54/54d · ..."` in RED instead of `"54/54d · ..."`, while `>= 55` displays `"55/54d · ..."` (no `">"`), and line-only overflow displays `"N/54d · 4/3L"` (no `">"`).
2. **`_apply_overflow_highlights()` (`misora.py:13640–13672`)**:
   - Updated docstring to cover combined horizontal (`>54d`) + full-line vertical (`>= 4` lines) overflow.
   - Replaced the width-only check with a single-loop branch:
     - `if ln >= 4:` -> `widget.tag_add("line_overflow", f"{ln}.0", f"{ln}.end")` (full-line highlight regardless of whether line 4+ also exceeds 54d width)
     - `elif ov_start is not None:` -> `widget.tag_add("line_overflow", f"{ln}.{ov_start}", f"{ln}.end")` (lines 1–3 horizontal overflow tail)

---

## 3  Zero-`.pyc` TDD & Verification Transcript

### 3.1  Pre-Patch Failing-First Verification (`tests/test_t04_overflow_line4_numerator.py` created BEFORE patching `misora.py`)

- BOM-safe in-memory `compile()` (`89` `.py` files): `IN_MEMORY_COMPILE_OK: 89`
- Discovery count: `countTestCases: 516`
- `py -3.12 -B -m unittest tests.test_t04_overflow_line4_numerator -v`:
  ```text
  Ran 12 tests in 28.620s
  FAILED (failures=4)
  ```
  - Probes `P1`–`P4` all failed with `AssertionError` (`0` errors); Guards `G1`–`G8` all passed (`ok`).

### 3.2  Post-Patch Integrity & Syntax Gates

```text
diff_check_exit=0
 M PROJECT_STATE.md
 M docs/project/OPEN_ISSUES.md
 M misora.py
?? tests/test_t04_overflow_line4_numerator.py
17	11	PROJECT_STATE.md
1	1	docs/project/OPEN_ISSUES.md
7	4	misora.py
lines= 24004 crlf= 24003 bare_lf= 0 bare_cr= 0
IN_MEMORY_COMPILE_OK: 89
PROJECT_STATE_bytes=7439
post_pyc_count=125
```

(`pre_pyc_count == post_pyc_count == 125`; `compileall` and `tools/generate_symbol_index.py` were never executed post-edit.)

### 3.3  Post-Patch T-04 & Targeted Regression Runs

1. **`py -3.12 -B -m unittest tests.test_t04_overflow_line4_numerator -v`** (after fixing `"Line 5"` length `"5.5"` -> `"5.6"` in Probe 2):
   ```text
   Ran 12 tests in 28.911s
   OK
   ```
2. **`py -3.12 -B -m unittest tests.test_p3_s17_pixel_rulers tests.test_v15_s02_fonts_ruler_metrics tests.test_v15_s09_core_fixes_54d tests.test_t02_next_tooltip -v`**:
   ```text
   Ran 31 tests in 51.055s
   OK
   ```

### 3.4  Full Suite Coverage (`516` Tests) & `Tcl_AsyncDelete` Observation

- **Monolithic `py -3.12 -B -m unittest discover -s tests -t . -v`** (Run 1 & Run 2):
  - Both monolithic single-process runs hit the pre-existing `Tcl_AsyncDelete: async handler deleted by the wrong thread` teardown abort (`exit -2147483645`), after `Variable.__del__` `RuntimeError: main thread is not in main loop` warnings began at `tests.test_s8b3_encoding_detection.test_08` (immediately following `test_s8b2_memory_guards`).
  - Run 1 aborted at `test_t08a_tooltip_clamping` (after all 12 `test_t04` tests passed).
  - Run 2 completed all **385** pre-`v15` tests (`test_misora_core`..`test_t08a_tooltip_clamping`: **`343 PASS + 35 SKIP + 5 FAIL + 2 ERROR`**) plus 10 tests of `test_v15_s01` before aborting at `test_v15_s01_stability_remediation::test_probe_8`.
- **Standalone `test_v15_*` run** (all 16 `test_v15_*` modules):
  ```text
  Ran 131 tests in 251.789s
  FAILED (failures=1)
  ```
  - `130 PASS + 1 FAIL` — the sole failure is the pre-existing baseline debt `test_v15_s01_stability_remediation::test_probe_8_rebrand_and_derived_version_1_4_1` (`'1.4.15' != '1.4.1'`).
- **Combined 516-test tally (`385 + 131`)**:
  - **`516 = 473 PASS + 35 SKIP + 6 FAIL + 2 ERROR`** (`0` new T-04 regressions).

---

## 4  Rollback Commands (Pinned to `b50c75e7555779cbff0b6821933e11b5f7ef9bf9`)

```powershell
cd D:\Misora-Editor
git checkout b50c75e7555779cbff0b6821933e11b5f7ef9bf9 -- misora.py docs/project/OPEN_ISSUES.md PROJECT_STATE.md
Remove-Item tests\test_t04_overflow_line4_numerator.py -Force -ErrorAction SilentlyContinue

git status --short --untracked-files=all
py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"
```

---

## 5  Windows Manual QA Checklist (`M-1..M-9` — `ALL PASS — OPERATOR VERIFIED`)

**Operator Sign-Off:** `PASS` (`M-1..M-9` all verified on Windows 11, `v1.4.15` @ `02de57f148747d9dbf71574e0748fa66c80a8925`, Project Lead).

- [pass] **M-1**: Line 4+ short text (`Line 1\nLine 2\nLine 3\nLine 4`) in Dialogue Editor shows red background + underline (`line_overflow`) across line 4, red bold gutter `4`, and red header `N/54d · 4/3L`.
- [pass] **M-2**: Line 4+ text that also exceeds 54d highlights the entire line `4` (`4.0..4.end`), not just past `54d`.
- [pass] **M-3**: Lines 1–3 horizontal overflow (`55+` digits) highlights only past `54d` and updates header (`55/54d · 1/3L` RED).
- [pass] **M-4**: `54/54d` boundary — slightly wider font triggering `has_width_overflow` at `round == 54` displays RED `">54/54d · 1/3L"`; Global preset (Nunito Bold) at exact `54` digits displays MUTED `"54/54d · 1/3L"` (no `">"`).
- [pass] **M-5**: Box 0 displays `"Metadata (unmeasured)"` in muted color with zero overflow tags.
- [pass] **M-6**: All Script card bodies retain zero `line_overflow` and zero `gutter_overflow` tags while normal card headers (`▶ [BOX #NNN]` / `◆ [BOX #NNN]`) remain intact.
- [pass] **M-7**: Dialogue Preview retains zero `line_overflow` blocks.
- [pass] **M-8**: Quick Edit retains zero `line_overflow` and zero `gutter_overflow` tags.
- [pass] **M-9**: Light/Dark theme toggle updates `line_overflow`, `gutter_overflow`, and `lbl_char_overflow` colors cleanly.
