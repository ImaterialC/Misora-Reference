# T-02 Implementation Plan — Stale Overflow Tooltip String (Rev 3)

**Task:** T-02 (legacy ref `u-08`)  
**Product version:** `1.4.15` (root `__init__.py` authoritative; UNCHANGED)  
**Prepared:** 2026-11-28 · Rev 3  
**Rev 1 reviewers:** GPT-6 (CONDITIONAL APPROVE), Qwen (CONDITIONAL APPROVE)  
**Rev 2 reviewers:** Qwen (CLEARED FOR PROCEED), GPT-6 (APPROVED 9/9 technical areas; baseline HEAD update requested)  
**Status:** STOP — WAITING FOR FINAL CLEARANCE

---

## Revision History

| Rev | Date | Summary |
|-----|------|---------|
| 1 | 2026-11-28 | Initial plan. SHA-256 `E27D3455...` |
| 2 | 2026-11-28 | Addresses GPT-6 Blockers 1-2, Recs 1-4 and Qwen F-1..F-5. Fixed method names `_get_ruler_measure_font` (§3.2 Change 2, Probe 3), `_draw_single_pixel_ruler` (§3.2 Change 4, Probe 4). Aligned tooltip line 5578 to describe dual-font measurement (`active editor font` line widths against `fixed reference boundary`), removed unnecessary `f` prefix, replaced `gc.get_objects()` with `widget._tooltip.text`, updated rollback across all 4 authorized files, replaced Unix-only checks with Python 3.12 one-liners, added exact post-T-02 full-suite breakdown `494 = 451 PASS + 35 SKIP + 6 FAIL + 2 ERROR`. SHA-256 `A1AFBD51...` |
| 3 | 2026-11-28 | Baseline HEAD reconciliation after T-01 M-1..M-12 closeout commit (`8b75b9e61728f4a5a78d06901b7e7e5006343122`). Updated §1 Preflight Transcript, noted `misora.py` byte-identity between `33b6f7d` and `8b75b9e6` in §2.5/§2.7, and updated §6 rollback HEAD gate/restore target to `8b75b9e61728f4a5a78d06901b7e7e5006343122`. Technical design, 5-line diff, 8-test TDD suite, and ownership matrix unchanged. |

---

## 1. Preflight Transcript

```
> git rev-parse --show-toplevel
D:/Misora-Editor

> git branch --show-current
main

> git rev-parse HEAD
8b75b9e61728f4a5a78d06901b7e7e5006343122

> git status --short --untracked-files=all
(empty — clean working tree)

> py -3.12 -B -c "import __init__; print('__version__:', __init__.__version__)"
__version__: 1.4.15

> py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"
countTestCases: 486

> py -3.12 -B tools/generate_symbol_index.py --check
CHECK PASS: docs/architecture/MISORA_SYMBOL_INDEX.md
EXIT_CODE: 0
```

**Baseline verified:** branch `main`, HEAD `8b75b9e6`, product version `1.4.15`, clean tree, 486 discovered tests, symbol index CHECK PASS.

---

## 2. Source Audit & Runtime Reproduction

### 2.1 Original Report Clarification

The T-02 report (OPEN_ISSUES.md §A) states:

> Report: Next-button tooltip displays stale `50x3` instead of `54d x 3`.

**Clarification from source & runtime evidence:** The stale `50 x 3` tooltip is NOT on `btn_next` (the Next Dialogue Box button). It is on `lbl_char_overflow` — the overflow indicator label positioned immediately to the left of the Next button in the dialogue header. The Next button's own tooltip is correct: `"Next Dialogue Box (Alt+Right / Alt+Down)"`.

### 2.2 Grep Enumeration — Stale `50` References in `misora.py`

| Line | Exact Source Text | Stale? | Action |
|-----:|-------------------|--------|--------|
| **5577** | `"Native 50 x 3 dialogue rule: <= 50 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines).\n"` | **YES — hardcoded tooltip string** | **FIX (f-string)** |
| **13423** | `"""Return a cached tkfont.Font locked to Nunito Bold for constant 50d ruler calibration (U19)."""` — method `_get_ruler_measure_font` | **YES — stale docstring** | **FIX** |
| **13525** | `"""Update pixel-calibrated 50d x 3L indicator in dialogue header (U06, DEF-04)."""` — method `_update_char_overflow_indicator` | **YES — stale docstring** | **FIX** |
| **13607** | `"""Render tick marks and constant 50 digit-width overflow zone on a Canvas ruler (U19)."""` — method `_draw_single_pixel_ruler` | **YES — stale docstring** | **FIX** |

**Total stale `50`-based strings in `misora.py`:** 4 occurrences (1 user-visible tooltip + 3 internal docstrings).

**All other `54d` / `DIALOGUE_MAX_DIGITS` references are dynamic** (using f-strings with `{DIALOGUE_MAX_DIGITS}`) and are already correct.

### 2.3 Constant Verification

```python
# misora.py:368-369
DIALOGUE_MAX_DIGITS: int = 54
DIALOGUE_MAX_LINES: int = 3
```

The authoritative constants are `54` and `3`. The f-string label at line 5569 correctly reads `f"0/{DIALOGUE_MAX_DIGITS}d · 1/{DIALOGUE_MAX_LINES}L"` → renders as `"0/54d · 1/3L"`. Only the hardcoded tooltip string at line 5577 and three docstrings are stale.

### 2.4 Tooltip Line 5578 — Measurement Semantics Verification

The tooltip's second line (line 5578) states: `"Measured using the active editor font as an estimate of the in-game font (NGUI tags excluded)."`. Verification of what `_update_char_overflow_indicator` actually measures:

- `_update_char_overflow_indicator` (`misora.py:13524-13548`) calls `_measure_dialogue_metrics(text)` at line 13538.
- `_measure_dialogue_metrics` (`misora.py:13455-13522`) uses **two** fonts:
  - **Active editor font** (`_get_dialogue_measure_font()`, line 13462) — used to measure rendered pixel width of each line (`f.measure(full_rendered)`, line 13493; binary-search overflow boundary, line 13500).
  - **Locked Nunito Bold ruler font** (via `_get_54d_reference_safe_w()`, line 13463 → `_get_ruler_measure_font()`, line 13451) — used to compute the constant 54-digit-width pixel threshold (`safe_w`).
- The `d_equiv` shown in the label (line 13541) divides the **active-font-measured** pixel width by the **ruler-font-calibrated** digit width.

**Conclusion:** The tooltip says "active editor font" but this is a simplification — the threshold boundary (54d) is calibrated against the locked Nunito Bold reference, while only rendered line widths use the active editor font. The second line will be updated to describe the dual-font scheme accurately.

**Evidence:** `misora.py:13455-13464` (`SOURCE-OBSERVED`, `CONFIRMED` via read-only inspection).

### 2.5 Runtime Reproduction (Genuine `MisoraApp` Instance)

```
> py -3.12 -B -c "<probe script with CONFIG_PATH = Path(tempdir) / 'misora_config.json'>"

lbl_char_overflow: tooltip_text = 'Native 50 x 3 dialogue rule: <= 50 digit-widths
  without linebreak AND < 3 linebreaks (<= 3 lines).\nMeasured using the active
  editor font as an estimate of the in-game font (NGUI tags excluded).'
btn_next: tooltip_text = 'Next Dialogue Box (Alt+Right / Alt+Down)'
btn_prev: tooltip_text = 'Previous Dialogue Box (Alt+Left / Alt+Up)'
PROBE COMPLETE
```

**Runtime CONFIRMED:** `lbl_char_overflow` tooltip displays `"Native 50 x 3"` and `"<= 50 digit-widths"` at runtime on `v1.4.15`, historical reproduction HEAD `33b6f7d` (`misora.py` is byte-identical between `33b6f7d` and current baseline HEAD `8b75b9e6`, verified via `git diff --quiet 33b6f7d 8b75b9e6 -- misora.py` exit `0`). The Next/Prev button tooltips are correct and unaffected.

### 2.6 `ToolTip._tooltip` Attribute Verification

`ToolTip.__init__` (`misora.py:212`) executes `setattr(self.widget, "_tooltip", self)`, storing the `ToolTip` instance directly on the widget. Tests can access `widget._tooltip.text` without `gc.get_objects()`.

### 2.7 Evidence Upgrade

**T-02 evidence:** `REPORTED + NEEDS-REPRO` → **`CONFIRMED`** (runtime reproduction on `v1.4.15`, historical HEAD `33b6f7d`; `misora.py` unchanged at current baseline HEAD `8b75b9e6`).

### 2.8 Adjacent Read-Only Notes

> [!NOTE]
> **AGENTS.md §7 line 40** contains: `"Native overflow: 50 digit-widths or 3+ hard linebreaks (4+ lines)"`.
> This is also stale (should reference 54), but `AGENTS.md` is **strictly READ-ONLY** under ENV-01 / T-02 scope.
> Recorded as a separate observation for Project Lead disposition. NOT part of T-02 fix scope.

> [!NOTE]
> **Tests grep:** `test_v15_s02_fonts_ruler_metrics.py:253` contains `"""Guard 2: Box 0 Summary does not trigger dialogue 50x3 red overflow violation (DEF-04)."""` — this is a docstring in an existing test file. Existing test files are READ-ONLY under T-02 scope. Recorded for Project Lead awareness.

---

## 3. Root Cause Fix Design

### 3.1 Root Cause

A single hardcoded tooltip string at `misora.py:5577` was written when the native overflow threshold was 50 digit-widths and was never updated when the threshold was changed to 54 (`DIALOGUE_MAX_DIGITS = 54`, established in S09). Three internal docstrings (`_get_ruler_measure_font` at line 13423, `_update_char_overflow_indicator` at line 13525, `_draw_single_pixel_ruler` at line 13607) have the same stale `50`/`50d` references.

### 3.2 Fix: Convert Hardcoded Tooltip to Dynamic f-string + Update Docstrings + Clarify Measurement

**Change 1 — Lines 5577-5578 (tooltip string):**

```diff
--- a/misora.py
+++ b/misora.py
@@ -5574,8 +5574,8 @@
         self.lbl_char_overflow.pack(side="right", padx=(4, 2))
         create_tooltip(
             self.lbl_char_overflow,
-            "Native 50 x 3 dialogue rule: <= 50 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines).\n"
-            "Measured using the active editor font as an estimate of the in-game font (NGUI tags excluded)."
+            f"Native {DIALOGUE_MAX_DIGITS}d x {DIALOGUE_MAX_LINES} dialogue rule: <= {DIALOGUE_MAX_DIGITS} digit-widths without linebreak AND < {DIALOGUE_MAX_LINES} linebreaks (<= {DIALOGUE_MAX_LINES} lines).\n"
+            "Line widths measured in the active editor font against a fixed reference boundary calibrated to the in-game box (NGUI tags excluded)."
         )
```

This renders at runtime as:
```
Native 54d x 3 dialogue rule: <= 54 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines).
Line widths measured in the active editor font against a fixed reference boundary calibrated to the in-game box (NGUI tags excluded).
```

Line 5577 uses `f"..."` to interpolate `DIALOGUE_MAX_DIGITS` and `DIALOGUE_MAX_LINES` (future-proof). Line 5578 is a plain string (no `f` prefix) — it describes the dual-font measurement truthfully without interpolation: rendered line widths use the active editor font (`_get_dialogue_measure_font`, `misora.py:13462`/`13493`), while the 54d boundary (`safe_w`) is calibrated from the locked Nunito Bold ruler font (`_get_ruler_measure_font` → `_get_54d_reference_safe_w`, `misora.py:13449-13463`).

**Change 2 — Line 13423 (docstring of `_get_ruler_measure_font`):**

```diff
@@ -13422,7 +13422,7 @@
     def _get_ruler_measure_font(self) -> tkfont.Font:
-        """Return a cached tkfont.Font locked to Nunito Bold for constant 50d ruler calibration (U19)."""
+        """Return a cached tkfont.Font locked to Nunito Bold for constant 54d ruler calibration (U19)."""
```

**Change 3 — Line 13525 (docstring of `_update_char_overflow_indicator`):**

```diff
@@ -13524,7 +13524,7 @@
     def _update_char_overflow_indicator(self, text: Optional[str] = None) -> None:
-        """Update pixel-calibrated 50d x 3L indicator in dialogue header (U06, DEF-04)."""
+        """Update pixel-calibrated 54d x 3L indicator in dialogue header (U06, DEF-04)."""
```

**Change 4 — Line 13607 (docstring of `_draw_single_pixel_ruler`):**

```diff
@@ -13606,7 +13606,7 @@
     def _draw_single_pixel_ruler(self, canvas: tk.Canvas, x0: int) -> None:
-        """Render tick marks and constant 50 digit-width overflow zone on a Canvas ruler (U19)."""
+        """Render tick marks and constant 54 digit-width overflow zone on a Canvas ruler (U19)."""
```

### 3.3 Change Metrics

| Metric | Value |
|--------|-------|
| Files changed | 1 (`misora.py`) |
| Lines changed (tooltip) | 2 modified (lines 5577-5578) |
| Lines changed (docstrings) | 3 modified (lines 13423, 13525, 13607) |
| Total lines added | 0 |
| Total lines deleted | 0 |
| Expected `git diff --numstat` | `5	5	misora.py` |
| Total line count | 23912 (unchanged) |

### 3.4 Verification Locks

- **V-1 (Context Lock):** Each diff hunk has verbatim surrounding context. Apply with `git apply --check` before execution. Reject fuzzy/offset matches.
- **V-2 (Line Count Invariance):**
  ```
  py -3.12 -B -c "print(sum(1 for _ in open('misora.py','rb')))"
  ```
  Must report exactly `23912` before and after.
- **C-5 (EOL Preservation — CRLF):** `misora.py` uses CRLF line endings. All edits must preserve CRLF. Verify with:
  ```
  py -3.12 -B -c "d=open('misora.py','rb').read(); cr=d.count(b'\r\n'); lf=d.count(b'\n'); print('CRLF:', cr, 'LF:', lf); assert cr == lf, f'Mixed EOL: {cr} CRLF vs {lf} LF'"
  ```

---

## 4. File Ownership Matrix — T-02 Execution Charter

> [!IMPORTANT]
> This charter is DISTINCT from ENV-01. Execution requires explicit Project Lead `Proceed` authorization.

### 4.1 Allowed Files (after explicit `Proceed` only)

| File | Scope | Action |
|------|-------|--------|
| `misora.py` | Lines 5577-5578 tooltip string fix + lines 13423, 13525, 13607 docstring fixes ONLY | MODIFY |
| `tests/test_t02_next_tooltip.py` | NEW file — stdlib `unittest`, zero `pytest`, zero `.unity3d` fixtures, zero `skipTest()` | CREATE |
| `docs/project/OPEN_ISSUES.md` | T-02 evidence → `CONFIRMED`, TDD `PASS`, Windows hover check `MANUAL-PENDING`, lifecycle stays `ACTIVE` | MODIFY |
| `PROJECT_STATE.md` | Update test discovery count `486 + 8 = 494`, N-4 transient `--check` note, stay ≤ 15,360 bytes | MODIFY |

### 4.2 Strictly Forbidden / READ-ONLY

| Path | Reason |
|------|--------|
| `__init__.py` | ENV-01 §2 READ-ONLY; version `1.4.15` UNCHANGED |
| `core/**` | ENV-01 §2 READ-ONLY |
| `assets/**` | ENV-01 §2 READ-ONLY |
| All existing `tests/*.py` | ENV-01 §2 READ-ONLY; no weakening/modifying existing tests |
| `AGENTS.md` | READ-ONLY under T-02 scope (stale §7 `50 digit-widths` noted but NOT fixed here) |
| `docs/archive/**` | Layer 3 — not loaded, not modified |
| `tools/generate_symbol_index.py` | READ-ONLY |
| `docs/architecture/MISORA_SYMBOL_INDEX.md` | Deferred to Project Lead post-commit regeneration |
| `misora.bat`, `requirements.txt`, `misora_config.json`, `backups/**`, `README.md` | ENV-01 §2 READ-ONLY |

---

## 5. TDD Verification Plan

### 5.1 Zero-`.pyc` Compile Check

Before and after patching:

```python
py -3.12 -B -c "
import os
pyc_before = sum(1 for root, _, files in os.walk('.') for f in files if f.endswith('.pyc'))

targets = ['__init__.py', 'misora.py']
targets += [os.path.join('core', f) for f in os.listdir('core') if f.endswith('.py')]
targets += [os.path.join('assets', f) for f in os.listdir('assets') if f.endswith('.py')]
targets += [os.path.join('tests', f) for f in os.listdir('tests') if f.endswith('.py')]

for path in targets:
    with open(path, 'rb') as fh:
        src = fh.read()
    if src.startswith(b'\xef\xbb\xbf'):
        src = src[3:]
    compile(src, path, 'exec')  # SyntaxError = STOP

pyc_after = sum(1 for root, _, files in os.walk('.') for f in files if f.endswith('.pyc'))
assert pyc_before == pyc_after, f'.pyc count changed: {pyc_before} -> {pyc_after}'
print('COMPILE CHECK: PASS')
"
```

### 5.2 Test File: `tests/test_t02_next_tooltip.py`

**New test file contents (draft — exact code finalized at execution):**

All Probes and Guards instantiate `MisoraApp(restore_session=False, show_splash=False)` with `CONFIG_PATH` redirected to a `tempfile.mkdtemp()` via `pathlib.Path`. Tooltip text is accessed via `widget._tooltip.text` (confirmed: `ToolTip.__init__` stores `setattr(self.widget, "_tooltip", self)` at `misora.py:212`). No `gc.get_objects()` scan.

**Defect Probes (pre-patch MUST FAIL, post-patch MUST PASS):**

- **Probe 1 — Tooltip string uses dynamic constants:** Access `self.app.lbl_char_overflow._tooltip.text`. Assert it contains `str(DIALOGUE_MAX_DIGITS)` (i.e. `"54"`) and does NOT contain the stale literal `"50 x 3"` or `"50 digit-widths"`. Also assert it contains both `"active editor font"` and `"fixed reference boundary"` (updated line 5578 wording).

- **Probe 2 — `_update_char_overflow_indicator` docstring:** Assert `self.app._update_char_overflow_indicator.__doc__` contains `"54d"` and does not contain `"50d"`.

- **Probe 3 — `_get_ruler_measure_font` docstring:** Assert `self.app._get_ruler_measure_font.__doc__` contains `"54d"` and does not contain `"50d"`.

- **Probe 4 — `_draw_single_pixel_ruler` docstring:** Assert `self.app._draw_single_pixel_ruler.__doc__` contains `"54 digit-width"` and does not contain `"50 digit-width"`.

**Regression Guards (MUST PASS before AND after patch):**

- **Guard 1 — Constants are 54 and 3:** Assert `DIALOGUE_MAX_DIGITS == 54` and `DIALOGUE_MAX_LINES == 3`.

- **Guard 2 — Label initial text is dynamic:** Assert `self.app.lbl_char_overflow.cget("text")` matches `"0/54d · 1/3L"` (i.e. `f"0/{DIALOGUE_MAX_DIGITS}d · 1/{DIALOGUE_MAX_LINES}L"`).

- **Guard 3 — `btn_next` tooltip unchanged:** Assert `self.app.btn_next._tooltip.text == "Next Dialogue Box (Alt+Right / Alt+Down)"`.

- **Guard 4 — `btn_prev` tooltip unchanged:** Assert `self.app.btn_prev._tooltip.text == "Previous Dialogue Box (Alt+Left / Alt+Up)"`.

All tests use `app.destroy()` in `tearDown` + `shutil.rmtree(tmpdir)` cleanup. Zero external dependencies, zero `.unity3d` fixtures, zero `skipTest()`, zero `pytest`.

**N-3 Guard Re-Label Rule:** If any Guard already passes pre-patch and also passes post-patch, it stays a Guard. If a Probe unexpectedly passes pre-patch, STOP and record `ALREADY PASSING / NOT REPRODUCED` — never plant a fake bug.

### 5.3 Discovery Arithmetic

```
Current:  486 total discovered tests
New:      tests/test_t02_next_tooltip.py adds 8 tests (4 Probes + 4 Guards)
Target:   486 + 8 = 494

Any count ≠ 494 = STOP.
```

### 5.4 TDD Execution Sequence

1. **Create** `tests/test_t02_next_tooltip.py` (but do NOT patch `misora.py` yet).
2. **Compile check** (§5.1) — all files must compile cleanly.
3. **Discover:** `py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"` → must report `494`.
4. **Pre-patch run:**
   - `py -3.12 -B -m unittest tests.test_t02_next_tooltip -v`
   - Expected: **Probes 1-4 FAIL** (stale `50` strings detected), **Guards 1-4 PASS**.
   - If any Probe passes pre-patch → **STOP** (`ALREADY PASSING / NOT REPRODUCED`).
   - If any Guard fails pre-patch → **STOP** (pre-existing unrelated regression).
5. **Apply patch** (§3.2 — all 5 line changes in `misora.py`).
6. **Compile check** (§5.1) — all files must compile cleanly. `.pyc` count unchanged.
7. **Verify line count invariance (V-2):**
   ```
   py -3.12 -B -c "print(sum(1 for _ in open('misora.py','rb')))"
   ```
   Must report `23912`.
8. **Verify CRLF preservation (C-5):**
   ```
   py -3.12 -B -c "d=open('misora.py','rb').read(); cr=d.count(b'\r\n'); lf=d.count(b'\n'); print('CRLF:', cr, 'LF:', lf); assert cr == lf"
   ```
9. **Post-patch run — T-02 suite:**
   - `py -3.12 -B -m unittest tests.test_t02_next_tooltip -v`
   - Expected: **All 8 tests PASS** (Probes + Guards).
10. **Post-patch run — targeted existing UI suites:**
    - `py -3.12 -B -m unittest tests.test_v15_s11e_polish_splash_menu_tooltips -v`
    - `py -3.12 -B -m unittest tests.test_v15_s02_fonts_ruler_metrics -v`
    - Expected: same PASS/SKIP/FAIL profile as pre-T-02 baseline (no new failures).
11. **Post-patch full discovery:**
    - `py -3.12 -B -m unittest discover -s tests -v`
    - Report exact `Ran N / PASS / SKIP / FAIL / ERROR`.
    - **Expected exact profile:** `Ran 494` = **451 PASS + 35 SKIP + 6 FAIL + 2 ERROR** (`+8 PASS` over T-01 baseline of `486 = 443 PASS + 35 SKIP + 6 FAIL + 2 ERROR`; `0` new failures/errors/skips).
    - Any deviation from this profile = **STOP**.
12. **Verify** `git diff --numstat -- misora.py` → must be `5	5	misora.py`.
13. **Verify** `git status --short --untracked-files=all` — only expected modified/new files.

---

## 6. Rollback Steps

> [!IMPORTANT]
> Rollback covers ALL 4 authorized files. Steps are gated on verified pre-edit HEAD.

If any post-patch check fails:

```powershell
# 0. Verify we are still on the correct commit (pre-edit HEAD)
py -3.12 -B -c "import subprocess; h=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(); assert h=='8b75b9e61728f4a5a78d06901b7e7e5006343122', f'HEAD mismatch: {h}'; print('HEAD OK:', h)"

# 1. Revert misora.py (only file with committed baseline — targeted restore from HEAD)
git checkout 8b75b9e61728f4a5a78d06901b7e7e5006343122 -- misora.py

# 2. Remove new test file (untracked — never committed)
Remove-Item -Path tests\test_t02_next_tooltip.py -ErrorAction SilentlyContinue

# 3. Revert docs/project/OPEN_ISSUES.md (restore from HEAD if modified)
git checkout 8b75b9e61728f4a5a78d06901b7e7e5006343122 -- docs/project/OPEN_ISSUES.md

# 4. Revert PROJECT_STATE.md (restore from HEAD if modified)
git checkout 8b75b9e61728f4a5a78d06901b7e7e5006343122 -- PROJECT_STATE.md

# 5. Verify clean state
git status --short --untracked-files=all
# Expected: empty (clean working tree)

# 6. Verify original test count restored
py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"
# Expected: 486

# 7. Verify line count invariance
py -3.12 -B -c "print(sum(1 for _ in open('misora.py','rb')))"
# Expected: 23912
```

---

## 7. Manual Windows QA Checklist

All items are `MANUAL-PENDING` until operator confirmation.

| ID | Check | DPI | Steps | Expected | Status |
|----|-------|-----|-------|----------|--------|
| **M-1** | Tooltip text at 100% DPI | 100% | Hover over `lbl_char_overflow` (the `0/54d · 1/3L` indicator label) for >350ms | Tooltip reads: `"Native 54d x 3 dialogue rule: <= 54 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines)."` + `"\nLine widths measured in the active editor font against a fixed reference boundary calibrated to the in-game box (NGUI tags excluded)."` | `MANUAL-PENDING` |
| **M-2** | Tooltip text at 125% DPI | 125% | Same as M-1 | Same expected text as M-1 | `MANUAL-PENDING` |
| **M-3** | Next/Prev tooltips unaffected | 100% | Hover over Next button, then Prev button | `"Next Dialogue Box (Alt+Right / Alt+Down)"` / `"Previous Dialogue Box (Alt+Left / Alt+Up)"` unchanged | `MANUAL-PENDING` |
| **M-4** | Label text dynamic update | 100% | Type >54 characters in dialogue, verify label turns red and shows `>54/54d` | Label updates correctly, tooltip unchanged | `MANUAL-PENDING` |

---

## 8. OPEN_ISSUES.md Update (Draft)

T-02 row in §A table, after execution:

```markdown
| **T-02** | `u-08` | `CONFIRMED` | `ACTIVE` | **Report:** Overflow indicator tooltip (`lbl_char_overflow`) displayed stale `"50 x 3"` / `"50 digit-widths"` instead of dynamic `"54d x 3"` / `"54 digit-widths"`. **Root cause:** hardcoded tooltip string not updated when `DIALOGUE_MAX_DIGITS` changed from 50 to 54 in S09 (font calibration established constant Nunito Bold 54d reference, superseding the earlier 50-digit figure). **Fix:** line 5577 converted to dynamic f-string using `DIALOGUE_MAX_DIGITS`/`DIALOGUE_MAX_LINES` constants; line 5578 updated to describe the dual-font scheme (active editor font widths against fixed reference boundary) accurately; 3 stale docstrings (`_get_ruler_measure_font`, `_update_char_overflow_indicator`, `_draw_single_pixel_ruler`) corrected from `50d`/`50` to `54d`/`54`. Protected by `tests/test_t02_next_tooltip.py` (4 Probes + 4 Guards). **Automated TDD: `PASS`.** Windows QA `M-1..M-4`: `MANUAL-PENDING` (keep `ACTIVE` until manual QA passes). **Clarification:** original report said "Next-button tooltip" but the stale string was on `lbl_char_overflow`, the overflow indicator label adjacent to the Next button; the Next button's own tooltip was always correct. **Note:** T-01 `M-1..M-12` closeout is tracked separately under T-01 and is not gated by T-02. |
```

---

## 9. PROJECT_STATE.md Update (Draft)

After execution, update §2:

- Test discovery count: `486` → `494` (`486` baseline + `8` in `tests/test_t02_next_tooltip.py`).
- Exact profile: `494 total = 451 PASS + 35 SKIP + 6 FAIL + 2 ERROR`.
- Add T-02 status row similar to T-01 row.
- Maintain N-4 transient `--check` note (symbol index expected non-zero until regeneration).
- Stay ≤ 15,360 bytes.

---

## 10. Stale `AGENTS.md` §7 Observation (READ-ONLY — Separate From T-02)

> [!NOTE]
> `AGENTS.md` line 40 reads: `"Native overflow: 50 digit-widths or 3+ hard linebreaks (4+ lines)"`.
> This should be `54 digit-widths` to match `DIALOGUE_MAX_DIGITS = 54` (established by S09 font calibration).
> **`AGENTS.md` is strictly READ-ONLY under ENV-01 and T-02 scope.**
> Recorded for Project Lead disposition in a separate future edit.

---

## STOP — WAITING FOR FINAL CLEARANCE
