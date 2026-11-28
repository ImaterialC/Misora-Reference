# T-02 Implementation Plan — Stale Overflow Tooltip String

**Task:** T-02 (legacy ref `u-08`)  
**Product version:** `1.4.15` (root `__init__.py` authoritative; UNCHANGED)  
**Prepared:** 2026-11-28  
**Status:** STOP — WAITING FOR INDEPENDENT REVIEW

---

## 1. Preflight Transcript

```
> git rev-parse --show-toplevel
D:/Misora-Editor

> git branch --show-current
main

> git rev-parse HEAD
33b6f7dc10dcb86b853aa71ab833864eeb843dfa

> git status --short --untracked-files=all
(empty — clean working tree)

> py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"
countTestCases: 486

> py -3.12 -B tools/generate_symbol_index.py --check
CHECK PASS: docs/architecture/MISORA_SYMBOL_INDEX.md
EXIT_CODE: 0
```

**Baseline verified:** branch `main`, HEAD `33b6f7d`, clean tree, 486 discovered tests, symbol index CHECK PASS.

---

## 2. Source Audit & Runtime Reproduction

### 2.1 Original Report Clarification

The T-02 report (OPEN_ISSUES.md §A) states:

> Report: Next-button tooltip displays stale `50x3` instead of `54d x 3`.

**Clarification from source & runtime evidence:** The stale `50 x 3` tooltip is NOT on `btn_next` (the Next Dialogue Box button). It is on `lbl_char_overflow` — the overflow indicator label positioned immediately to the left of the Next button in the dialogue header. The Next button's own tooltip is correct: `"Next Dialogue Box (Alt+Right / Alt+Down)"`.

### 2.2 Grep Enumeration — Stale `50` References in `misora.py`

```
grep -n for '50 x 3', '50d', '50 digit-widths', '50 chars' in misora.py:
```

| Line | Context | Stale? | Action |
|-----:|---------|--------|--------|
| **5577** | `"Native 50 x 3 dialogue rule: <= 50 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines).\n"` | **YES — hardcoded tooltip string** | **FIX** |
| **13525** | `"""Update pixel-calibrated 50d x 3L indicator in dialogue header (U06, DEF-04)."""` | **YES — stale docstring** | **FIX** |
| 13423 | `"""Return a cached tkfont.Font locked to Nunito Bold for constant 50d ruler calibration (U19)."""` | Stale docstring (refers to 50d calibration, actual calibration produces 54d) | FIX (same scope) |
| 13607 | `"""Render tick marks and constant 50 digit-width overflow zone on a Canvas ruler (U19)."""` | Stale docstring (refers to 50 digit-width, actual ruler renders 54d) | FIX (same scope) |

**Total stale `50`-based strings in `misora.py`:** 4 occurrences (1 user-visible tooltip + 3 internal docstrings).

**All other `54d` / `DIALOGUE_MAX_DIGITS` references are dynamic** (using f-strings with `{DIALOGUE_MAX_DIGITS}`) and are already correct.

### 2.3 Constant Verification

```python
# misora.py:368-369
DIALOGUE_MAX_DIGITS: int = 54
DIALOGUE_MAX_LINES: int = 3
```

The authoritative constants are `54` and `3`. The f-string label at line 5569 correctly reads `f"0/{DIALOGUE_MAX_DIGITS}d · 1/{DIALOGUE_MAX_LINES}L"` → renders as `"0/54d · 1/3L"`. Only the hardcoded tooltip string at line 5577 and three docstrings are stale.

### 2.4 Runtime Reproduction (Genuine `MisoraApp` Instance)

```
> py -3.12 -B -c "<probe script with CONFIG_PATH = Path(tempdir) / 'misora_config.json'>"

lbl_char_overflow: tooltip_text = 'Native 50 x 3 dialogue rule: <= 50 digit-widths
  without linebreak AND < 3 linebreaks (<= 3 lines).\nMeasured using the active
  editor font as an estimate of the in-game font (NGUI tags excluded).'
btn_next: tooltip_text = 'Next Dialogue Box (Alt+Right / Alt+Down)'
btn_prev: tooltip_text = 'Previous Dialogue Box (Alt+Left / Alt+Up)'
PROBE COMPLETE
```

**Runtime CONFIRMED:** `lbl_char_overflow` tooltip displays `"Native 50 x 3"` and `"<= 50 digit-widths"` at runtime on `v1.4.15`. The Next/Prev button tooltips are correct and unaffected.

### 2.5 Evidence Upgrade

**T-02 evidence:** `REPORTED + NEEDS-REPRO` → **`CONFIRMED`** (runtime reproduction on `v1.4.15`, HEAD `33b6f7d`).

### 2.6 Adjacent Read-Only Notes

> [!NOTE]
> **AGENTS.md §7 line 40** contains: `"Native overflow: 50 digit-widths or 3+ hard linebreaks (4+ lines)"`.
> This is also stale (should reference 54), but `AGENTS.md` is **strictly READ-ONLY** under ENV-01 / T-02 scope.
> Recorded as a separate observation for Project Lead disposition. NOT part of T-02 fix scope.

> [!NOTE]
> **Tests grep:** `test_v15_s02_fonts_ruler_metrics.py:253` contains `"""Guard 2: Box 0 Summary does not trigger dialogue 50x3 red overflow violation (DEF-04)."""` — this is a docstring in an existing test file. Existing test files are READ-ONLY under T-02 scope. Recorded for Project Lead awareness.

---

## 3. Root Cause Fix Design

### 3.1 Root Cause

A single hardcoded tooltip string at `misora.py:5577` was written when the native overflow threshold was 50 digit-widths and was never updated when the threshold was changed to 54 (`DIALOGUE_MAX_DIGITS = 54`, established in S09). Three internal docstrings (lines 13423, 13525, 13607) have the same stale `50`/`50d` references.

### 3.2 Fix: Convert Hardcoded Tooltip to Dynamic f-string + Update Docstrings

**Change 1 — Line 5577-5578 (tooltip string):**

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
+            f"Measured using the active editor font as an estimate of the in-game font (NGUI tags excluded)."
         )
```

This renders at runtime as:
```
Native 54d x 3 dialogue rule: <= 54 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines).
Measured using the active editor font as an estimate of the in-game font (NGUI tags excluded).
```

The fix is **future-proof**: if `DIALOGUE_MAX_DIGITS` or `DIALOGUE_MAX_LINES` ever changes again, the tooltip updates automatically.

**Change 2 — Line 13423 (docstring):**

```diff
@@ -13420,7 +13420,7 @@
     def _get_dialogue_measure_font(self) -> tkfont.Font:
-        """Return a cached tkfont.Font locked to Nunito Bold for constant 50d ruler calibration (U19)."""
+        """Return a cached tkfont.Font locked to Nunito Bold for constant 54d ruler calibration (U19)."""
```

**Change 3 — Line 13525 (docstring):**

```diff
@@ -13524,7 +13524,7 @@
     def _update_char_overflow_indicator(self, text: Optional[str] = None) -> None:
-        """Update pixel-calibrated 50d x 3L indicator in dialogue header (U06, DEF-04)."""
+        """Update pixel-calibrated 54d x 3L indicator in dialogue header (U06, DEF-04)."""
```

**Change 4 — Line 13607 (docstring):**

```diff
@@ -13607,7 +13607,7 @@
     def _draw_ruler(self, canvas: tk.Canvas) -> None:
-        """Render tick marks and constant 50 digit-width overflow zone on a Canvas ruler (U19)."""
+        """Render tick marks and constant 54 digit-width overflow zone on a Canvas ruler (U19)."""
```

### 3.3 Change Metrics

| Metric | Value |
|--------|-------|
| Files changed | 1 (`misora.py`) |
| Lines changed (tooltip) | 2 modified (line 5577-5578) |
| Lines changed (docstrings) | 3 modified (lines 13423, 13525, 13607) |
| Total lines added | 0 |
| Total lines deleted | 0 |
| Expected `git diff --numstat` | `5	5	misora.py` |
| Total line count | 23912 (unchanged) |

### 3.4 Verification Locks

- **V-1 (Context Lock):** Each diff hunk has verbatim surrounding context. Apply with `git apply --check` before execution. Reject fuzzy/offset matches.
- **V-2 (Line Count Invariance):** `wc -l misora.py` must remain exactly `23912` before and after.
- **C-5 (EOL Preservation):** `misora.py` uses CRLF line endings. All edits must preserve CRLF. Verify with `file misora.py` or `xxd` spot check post-edit.

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
| `PROJECT_STATE.md` | Update test discovery count `486 + N`, N-4 transient `--check` note, stay ≤ 15,360 bytes | MODIFY |

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
# BOM-safe (utf-8-sig) in-memory compile check
import os, importlib.util
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
assert pyc_before == pyc_after, f".pyc count changed: {pyc_before} -> {pyc_after}"
```

### 5.2 Test File: `tests/test_t02_next_tooltip.py`

**New test file contents (draft — exact code finalized at execution):**

- **Defect Probe 1 (pre-patch MUST FAIL, post-patch MUST PASS):** Instantiate `MisoraApp(restore_session=False, show_splash=False)` with redirected `CONFIG_PATH`, find the `ToolTip` instance for `lbl_char_overflow` via `gc.get_objects()`, assert tooltip text contains `f"{DIALOGUE_MAX_DIGITS}"` (i.e. `"54"`) and does NOT contain the stale literal `"50 x 3"` or `"50 digit-widths"`.

- **Defect Probe 2 (pre-patch MUST FAIL, post-patch MUST PASS):** Assert `_update_char_overflow_indicator.__doc__` contains `"54d"` and does not contain `"50d"`.

- **Defect Probe 3 (pre-patch MUST FAIL, post-patch MUST PASS):** Assert `_get_dialogue_measure_font.__doc__` contains `"54d"` and does not contain `"50d"`.

- **Defect Probe 4 (pre-patch MUST FAIL, post-patch MUST PASS):** Assert `_draw_ruler.__doc__` contains `"54 digit-width"` and does not contain `"50 digit-width"`.

- **Regression Guard 1 (MUST PASS before AND after patch):** Verify `DIALOGUE_MAX_DIGITS == 54` and `DIALOGUE_MAX_LINES == 3`.

- **Regression Guard 2 (MUST PASS before AND after patch):** Verify `lbl_char_overflow` initial label text uses f-string format `f"0/{DIALOGUE_MAX_DIGITS}d · 1/{DIALOGUE_MAX_LINES}L"` → exact string `"0/54d · 1/3L"`.

- **Regression Guard 3 (MUST PASS before AND after patch):** Verify `btn_next` tooltip is `"Next Dialogue Box (Alt+Right / Alt+Down)"` (unchanged, unaffected by fix).

- **Regression Guard 4 (MUST PASS before AND after patch):** Verify `btn_prev` tooltip is `"Previous Dialogue Box (Alt+Left / Alt+Up)"` (unchanged, unaffected by fix).

All tests use `app.destroy()` in `tearDown` + `shutil.rmtree(tmpdir)` cleanup. Zero external dependencies, zero `.unity3d` fixtures, zero `skipTest()`, zero `pytest`.

**N-3 Guard Re-Label Rule:** If any Guard already passes pre-patch and also passes post-patch, it stays a Guard. If a Probe unexpectedly passes pre-patch, STOP and record `ALREADY PASSING / NOT REPRODUCED` — never plant a fake bug.

### 5.3 Discovery Arithmetic

```
Current:  486 total discovered tests
New:      tests/test_t02_next_tooltip.py adds N tests (expected N = 8: 4 Probes + 4 Guards)
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
7. **Verify** `wc -l misora.py` → must be `23912` (line count invariance V-2).
8. **Post-patch run — T-02 suite:**
   - `py -3.12 -B -m unittest tests.test_t02_next_tooltip -v`
   - Expected: **All 8 tests PASS** (Probes + Guards).
9. **Post-patch run — targeted existing UI suites:**
   - `py -3.12 -B -m unittest tests.test_v15_s11e_polish_splash_menu_tooltips -v`
   - `py -3.12 -B -m unittest tests.test_v15_s02_fonts_ruler_metrics -v`
   - Expected: same PASS/SKIP/FAIL profile as pre-T-02 baseline (no new failures).
10. **Post-patch full discovery:**
    - `py -3.12 -B -m unittest discover -s tests -v`
    - Report exact `Ran N / PASS / SKIP / FAIL / ERROR`.
    - Expected: `Ran 494` with 0 new failures beyond the existing 8 baseline debt items (6 FAIL + 2 ERROR).
11. **Verify** `git diff --numstat -- misora.py` → must be `5	5	misora.py`.
12. **Verify** `git status --short --untracked-files=all` — only expected modified/new files.

---

## 6. Rollback Steps

If any post-patch check fails:

```bash
# Revert misora.py to pre-patch state
git checkout -- misora.py

# Remove new test file
rm tests/test_t02_next_tooltip.py

# Verify clean state
git status --short --untracked-files=all
# Expected: empty (clean working tree)

# Verify original test count restored
py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"
# Expected: 486
```

---

## 7. Manual Windows QA Checklist

All items are `MANUAL-PENDING` until operator confirmation.

| ID | Check | DPI | Steps | Expected | Status |
|----|-------|-----|-------|----------|--------|
| **M-1** | Tooltip text at 100% DPI | 100% | Hover over `lbl_char_overflow` (the `0/54d · 1/3L` indicator label) for >350ms | Tooltip reads `"Native 54d x 3 dialogue rule: <= 54 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines).\nMeasured using the active editor font as an estimate of the in-game font (NGUI tags excluded)."` | `MANUAL-PENDING` |
| **M-2** | Tooltip text at 125% DPI | 125% | Same as M-1 | Same expected text as M-1 | `MANUAL-PENDING` |
| **M-3** | Next/Prev tooltips unaffected | 100% | Hover over Next button, then Prev button | `"Next Dialogue Box (Alt+Right / Alt+Down)"` / `"Previous Dialogue Box (Alt+Left / Alt+Up)"` unchanged | `MANUAL-PENDING` |
| **M-4** | Label text dynamic update | 100% | Type >54 characters in dialogue, verify label turns red and shows `>54/54d` | Label updates correctly, tooltip unchanged | `MANUAL-PENDING` |

---

## 8. OPEN_ISSUES.md Update (Draft)

T-02 row in §A table, after execution:

```markdown
| **T-02** | `u-08` | `CONFIRMED` | `ACTIVE` | **Report:** Overflow indicator tooltip (`lbl_char_overflow`) displayed stale `"50 x 3"` / `"50 digit-widths"` instead of `"54d x 3"` / `"54 digit-widths"`. **Root cause:** hardcoded tooltip string not updated when `DIALOGUE_MAX_DIGITS` changed from 50 to 54 (S09). **Fix:** converted to dynamic f-string using `DIALOGUE_MAX_DIGITS`/`DIALOGUE_MAX_LINES` constants; updated 3 stale docstrings. Protected by `tests/test_t02_next_tooltip.py` (4 Probes + 4 Guards). **Automated TDD: `PASS`.** Windows QA `M-1..M-4`: `MANUAL-PENDING` (keep `ACTIVE` until manual QA passes). **Note:** original report said "Next-button tooltip" but the stale string was on `lbl_char_overflow`, the overflow indicator label adjacent to the Next button. The Next button's own tooltip was always correct. |
```

---

## 9. PROJECT_STATE.md Update (Draft)

After execution, update §2:

- Test discovery count: `486` → `494` (`486` baseline + `8` in `tests/test_t02_next_tooltip.py`).
- Add T-02 status row similar to T-01 row.
- Maintain N-4 transient `--check` note (symbol index expected non-zero until regeneration).
- Stay ≤ 15,360 bytes.

---

## 10. Stale `AGENTS.md` §7 Observation (READ-ONLY — Separate From T-02)

> [!NOTE]
> `AGENTS.md` line 40 reads: `"Native overflow: 50 digit-widths or 3+ hard linebreaks (4+ lines)"`.
> This should be `54 digit-widths` to match `DIALOGUE_MAX_DIGITS = 54`.
> **`AGENTS.md` is strictly READ-ONLY under ENV-01 and T-02 scope.**
> Recorded for Project Lead disposition in a separate future edit.

---

## STOP — WAITING FOR INDEPENDENT REVIEW
