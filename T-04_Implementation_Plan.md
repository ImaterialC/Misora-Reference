# T-04 Implementation Plan (Rev 2) — Overflow Marker on Line 4+ / >3L & 54/54d Numerator Boundary Audit

> **Phase**: 1b (Strict Read-Only Source Audit & Implementation Plan — Rev 2)
> **Task**: T-04 (`u-02`) — Overflow Marker on Line 4+ / >3L & 54/54d Numerator Boundary
> **Date**: 2026-11-28
> **Baseline**: `main` @ `b50c75e7555779cbff0b6821933e11b5f7ef9bf9` (post-T-08a closeout)
> **Product**: `1.4.15`

---

## 1  Preflight & Baseline Verification

### 1.1  Repository State & Live Discovery

| Check | Command | Verbatim Result |
|---|---|---|
| Branch | `git rev-parse --abbrev-ref HEAD` | `main` |
| HEAD | `git rev-parse HEAD` | `b50c75e7555779cbff0b6821933e11b5f7ef9bf9` |
| Working tree | `git status --short --untracked-files=all` | *(empty — clean working tree)* |
| Version source | `py -3.12 -c "import __init__; print(__init__.__version__)"` | `1.4.15` |
| Live test discovery | `py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"` | `countTestCases: 504` |
| Symbol index check | `py -3.12 -B tools/generate_symbol_index.py --check` | `CHECK PASS: docs/architecture/MISORA_SYMBOL_INDEX.md` (exit `0`) |
| Suite baseline (locked) | `504` total | `461 PASS + 35 SKIP + 6 FAIL + 2 ERROR` |

### 1.2  EOL, Line Count, & Zero-`.pyc` / NO-`compileall` Syntax Gates

| Metric | Value |
|---|---|
| `misora.py` pre-edit logical lines | `24,001` |
| `misora.py` pre-edit CRLF terminators | `24,000` (`bare_LF == 0`, `bare_CR == 0`) |
| `pre_pyc_count` | `125` |
| `post_pyc_count` | `125` (`pre_pyc_count == post_pyc_count`) |
| BOM-safe in-memory `compile()` | `IN_MEMORY_COMPILE_OK: 88` (`__init__.py`, `misora.py`, `core/*.py`, `assets/*.py`, `tests/*.py` via `raw.removeprefix(bytes([239,187,191]))`) |

> [!IMPORTANT]
> `compileall` is **excluded** from all T-04 verification gates because `python -B -m compileall` still writes `.pyc` files to `__pycache__`. All syntax checks use BOM-safe in-memory `compile()` under `py -3.12 -B` only.

---

## 2  Verbatim Source Audit (`misora.py` @ `b50c75e7`)

### 2.1  Constants (`misora.py:457–458`)

```python
# misora.py:457-458
DIALOGUE_MAX_DIGITS: int = 54
DIALOGUE_MAX_LINES: int = 3
```

### 2.2  Overflow Color Constants

| Location | Light Theme | Dark Theme | Usage |
|---|---|---|---|
| `_update_char_overflow_indicator` `L13633` | `#c9184a` | `#ff5c7c` | Label `fg` when overflow |
| `_apply_gutter_overflow_tag` `L13681` | `#c9184a` | `#ff5c7c` | Gutter line-number `fg` L4+ |
| `_configure_editor_rich_tags` `L3748–3759` | bg `#ffd6dc`, fg auto-contrast | bg `#4a1c24`, fg auto-contrast | `line_overflow` text tag (`underline=True`) |
| `_draw_single_pixel_ruler` `L13703–13704` | zone `#ffd6dc`, fg `#c9184a` | zone `#4a1c24`, fg `#ff5c7c` | Canvas ruler red zone |

### 2.3  `_measure_dialogue_metrics()` (`misora.py:13544–13611`)

```python
# misora.py:13544-13611 (excerpts)
        f = self._get_dialogue_measure_font()       # active editor font
        safe_w = self._get_54d_reference_safe_w()    # Nunito Bold constant reference
        digit_w = safe_w / float(DIALOGUE_MAX_DIGITS)
        ...
            if pixel_width > safe_w and units:       # L13585 — strictly greater
                lo, hi = 1, len(units)
                while lo < hi:
                    mid = (lo + hi) // 2
                    w_mid = int(f.measure("".join(piece for _, piece in units[:mid])))
                    if w_mid > safe_w:
                        hi = mid
                    else:
                        lo = mid + 1
                overflow_raw_start = units[lo - 1][0]  # L13594
        ...
        line_count = len(raw_lines)                  # L13603
        return {
            "safe_w": safe_w,
            "digit_w": digit_w,
            "line_count": line_count,
            "has_line_overflow": line_count >= 4,     # L13608 — >= 4 lines (>= 3 linebreaks)
            "has_width_overflow": any(l["overflow_raw_start"] is not None for l in line_metrics),  # L13609
            "lines": line_metrics,
        }
```

### 2.4  `_update_char_overflow_indicator()` (`misora.py:13613–13637`)

```python
# misora.py:13613-13637 (verbatim)
    def _update_char_overflow_indicator(self, text: Optional[str] = None) -> None:
        """Update pixel-calibrated 54d x 3L indicator in dialogue header (U06, DEF-04)."""
        lbl = getattr(self, "lbl_char_overflow", None)
        if not lbl or not lbl.winfo_exists():
            return
        t = self.theme
        if getattr(self, "is_box0_active", False):
            lbl.config(text="Metadata (unmeasured)", fg=t["fg_muted"])
            return
        if text is None:
            if hasattr(self, "txt_dialogue") and self.txt_dialogue.winfo_exists():
                text = self.txt_dialogue.get("1.0", "end-1c")
            else:
                text = ""
        metrics = self._measure_dialogue_metrics(text)
        digit_w = max(1e-6, float(metrics["digit_w"]))
        max_px = max((l["pixel_width"] for l in metrics["lines"]), default=0)
        d_equiv = int(round(max_px / digit_w))
        line_count = metrics["line_count"]
        is_ov = bool(metrics["has_width_overflow"] or metrics["has_line_overflow"])
        ov_fg = "#c9184a" if self._is_light_theme() else "#ff5c7c"
        lbl.config(
            text=f"{d_equiv}/{DIALOGUE_MAX_DIGITS}d · {line_count}/{DIALOGUE_MAX_LINES}L",
            fg=ov_fg if is_ov else t["fg_muted"],
        )
```

### 2.5  `_apply_overflow_highlights()` (`misora.py:13639–13668`)

```python
# misora.py:13639-13668 (verbatim)
    def _apply_overflow_highlights(self, widget: Optional[tk.Text]) -> None:
        """Apply inline pixel-calibrated horizontal overflow highlights on a Text widget (Box 0 & Preview immune)."""
        if not widget or not widget.winfo_exists():
            return
        if widget is getattr(self, "txt_dialogue_preview", None):
            try:
                widget.tag_remove("line_overflow", "1.0", tk.END)
            except Exception:
                pass
            return
        if getattr(self, "is_box0_active", False) and widget in (
            getattr(self, "txt_dialogue", None),
            getattr(self, "txt_dialogue_preview", None),
        ):
            try:
                widget.tag_remove("line_overflow", "1.0", tk.END)
            except Exception:
                pass
            return
        try:
            widget.tag_remove("line_overflow", "1.0", tk.END)
            text = widget.get("1.0", "end-1c")
            metrics = self._measure_dialogue_metrics(text)
            for info in metrics["lines"]:
                ov_start = info["overflow_raw_start"]
                if ov_start is not None:
                    ln = info["line_no"]
                    widget.tag_add("line_overflow", f"{ln}.{ov_start}", f"{ln}.end")
        except Exception:
            pass
```

### 2.6  `_apply_gutter_overflow_tag()` & `_draw_single_pixel_ruler()` (`misora.py:13670–13746`)

- `_apply_gutter_overflow_tag()` (`L13670–13693`): configures `gutter_overflow` and tags `"4.0"` to `tk.END` when `total_lines >= 4` (with Box 0 immunity). Already highlights lines 4+ red in the gutter.
- `_draw_single_pixel_ruler()` (`L13695–13746`): renders `54d` boundary and red `>54d` zone past `ov_x = x0 + safe_w` on Canvas rulers `ruler_clean` and `ruler_cont`.

### 2.7  Direct Callers of `_apply_overflow_highlights()` & Real-Time Edit Path

| Line | Caller / Hook | Context |
|---|---|---|
| `misora.py:3403` | `_apply_theme()` | Re-applies overflow highlights on theme/font change |
| `misora.py:8958` | `_highlight_ngui_tags()` | Applies NGUI + overflow highlights to `txt_dialogue` |
| `misora.py:10657` | `_highlight_ngui_tags_for_widget(w)` | Preview-mode cleanup (`tag_remove`) |
| `misora.py:10663` | `_highlight_ngui_tags_for_widget(w)` | Widget-targeted NGUI + overflow highlight |
| **Real-time edit path** | `6345 (<KeyRelease>)` -> `13085 (_commit_widget_edit)` -> `13193 (_on_dialogue_edited)` -> `13250 (_highlight_ngui_tags)` -> `8958 (_apply_overflow_highlights)` | Recomputes `line_overflow` on every keystroke in `txt_dialogue` |

### 2.8  Callers of `_update_char_overflow_indicator()`

`3405` (`_apply_theme`), `9986` (`_update_views` Box 0), `10061` (`_update_views` normal box), `11077` (`_refresh_box_view`), `12330` (All Script Box 0 click), `12353` (All Script card click), `12489`/`12492` (All Script nav), `12874` (Quick Edit commit), `13253`/`13279` (`_on_dialogue_edited`), `19478` (Auto Word Wrap).

### 2.9  Exempt Surfaces & Import Dialog Badges

- **Dialogue Preview (`txt_dialogue_preview`)**: explicitly cleared at `L13643–13648`; zero `line_overflow` blocks (`Q-23`).
- **Quick Edit (`txt_quick_edit`)**: unified single-box surface with zero ruler / red overflow (`L6738`).
- **All Script Cards (`_AllScriptPoolCard`)**: `_populate_as_card_body()` (`L11998–12026`) strips `line_overflow` & `gutter_overflow`; `_apply_as_card_visual_state()` (`L11957`) renders `▶ [BOX #NNN]` (active) / `◆ [BOX #NNN]` (inactive) — **no** `▼▶` badges on All Script card headers.
- **`ImportFromXUATDialog`**: renders `▼`/`▶` overflow badge labels on import preview rows (`L21035–21088`, `L21447`), separate from `line_overflow` text tags.

---

## 3  Existing Test Coverage Audit

| Test File | Scope Checked | Conflict with T-04? |
|---|---|---|
| `tests/test_p3_s17_pixel_rulers.py` | 54d/55d metrics, `line_overflow`, `gutter_overflow` on L4+, All Script zero tags | None — only asserts L4+ `line_overflow >= 2` |
| `tests/test_v15_s02_fonts_ruler_metrics.py` | Font policy, constant ruler, fast metrics | None |
| `tests/test_v15_s09_core_fixes_54d.py` | 54d reference invariance, ruler labels `54d`/`>54d`, `/54d · 1/3L`, Box 0 immunity | None |
| `tests/test_t02_next_tooltip.py` | `lbl_char_overflow` tooltip wording, `"0/54d · 1/3L"` initial label, `btn_next` tooltip | None |
| `tests/test_p3_s18_game_preview.py` & `test_v15_s11b_scanner_save_preview.py` | Dialogue Preview zero `line_overflow`, Editor retains red tags | None |
| `tests/test_v15_s10_all_script_quick_edit.py` & `test_v15_s11c_quick_edit_unified.py` | All Script & Quick Edit zero overflow tags | None |

---

## 4  Root-Cause Analysis

### 4.1  Defect A — Line 4+ (>3L) Missing Red Inline Marker

- **Rule (`AGENTS.md §7`)**: Native overflow triggers at **54 digit-widths or 3+ hard linebreaks (4+ lines)**.
- **Observed**: `_measure_dialogue_metrics()` sets `has_line_overflow = line_count >= 4` (`L13608`), `_update_char_overflow_indicator()` turns `lbl_char_overflow` red (`L13632–13636`), and `_apply_gutter_overflow_tag()` turns gutter line numbers 4+ red bold (`L13690–13691`). However, `_apply_overflow_highlights()` (`L13662–13666`) ONLY checks `if ov_start is not None:`, so lines 4+ in `txt_dialogue` receive zero `line_overflow` text highlight unless they also individually exceed 54d width (and even then, characters `0..ov_start-1` on line 4+ are unhighlighted).
- **Fix**: Single-loop branch inside `_apply_overflow_highlights()`:
  - `if ln >= 4:` tag full line `f"{ln}.0"` .. `f"{ln}.end"` with `"line_overflow"` (regardless of whether line 4+ also exceeds 54d width).
  - `elif ov_start is not None:` tag horizontal overflow tail `f"{ln}.{ov_start}"` .. `f"{ln}.end"` on lines 1–3.
  - Update `_apply_overflow_highlights()` docstring to reflect combined horizontal (`>54d`) + full-line vertical (`>= 4` lines) overflow.

### 4.2  Defect B — `54/54d` Red Numerator at Boundary (T-02 M-4 QA)

- **Formula (`misora.py:13628–13635`)**:
  - `safe_w` is measured with the constant **ruler font** (Nunito Bold), while `pixel_width` / `max_px` is measured with the active **dialogue font** (`_get_dialogue_measure_font()`).
  - Overflow threshold (`L13585`): strictly `pixel_width > safe_w` -> sets `has_width_overflow = True` -> `is_ov = True` (RED label).
  - Numerator (`L13630`): `d_equiv = int(round(max_px / digit_w))` where `digit_w = safe_w / 54.0`.
- **Root Cause**: When a line's rendered `pixel_width` strictly exceeds `safe_w` by less than `0.5 * digit_w` (e.g., `safe_w = 540`, `digit_w = 10`, `pixel_width = 541` -> `541 / 10.0 = 54.1`), `has_width_overflow` is `True` (turning `lbl_char_overflow` RED), yet `int(round(54.1))` yields `54`, displaying `"54/54d · 1/3L"` in red — visually contradicting the `>54d` overflow boundary.
- **Line-count numerator check**: `line_count = metrics["line_count"]` is **not** clamped; `"4/3L"`, `"5/3L"`, etc. already display the true line count.
- **Fix**: Prefix `">"` whenever width overflows while `d_equiv <= DIALOGUE_MAX_DIGITS`:
  `d_prefix = ">" if (metrics["has_width_overflow"] and d_equiv <= DIALOGUE_MAX_DIGITS) else ""`
  - Sub-digit width overflow (`d_equiv == 54`, `has_width_overflow == True`) -> `">54/54d · ..."` in RED.
  - Normal width overflow (`d_equiv >= 55`) -> `"55/54d · ..."` in RED (no `">"` prefix).
  - Line-only overflow (`has_line_overflow == True`, `has_width_overflow == False`) -> `"2/54d · 4/3L"` in RED (no `">"` prefix).

---

## 5  Minimal Unified Diff Against `HEAD` (`b50c75e7555779cbff0b6821933e11b5f7ef9bf9`)

Pre-validated read-only via `git -C D:\Misora-Editor apply --check` -> **exit `0`**.

```diff
--- a/misora.py
+++ b/misora.py
@@ -13631,13 +13631,14 @@
         line_count = metrics["line_count"]
         is_ov = bool(metrics["has_width_overflow"] or metrics["has_line_overflow"])
         ov_fg = "#c9184a" if self._is_light_theme() else "#ff5c7c"
+        d_prefix = ">" if (metrics["has_width_overflow"] and d_equiv <= DIALOGUE_MAX_DIGITS) else ""
         lbl.config(
-            text=f"{d_equiv}/{DIALOGUE_MAX_DIGITS}d · {line_count}/{DIALOGUE_MAX_LINES}L",
+            text=f"{d_prefix}{d_equiv}/{DIALOGUE_MAX_DIGITS}d · {line_count}/{DIALOGUE_MAX_LINES}L",
             fg=ov_fg if is_ov else t["fg_muted"],
         )
 
     def _apply_overflow_highlights(self, widget: Optional[tk.Text]) -> None:
-        """Apply inline pixel-calibrated horizontal overflow highlights on a Text widget (Box 0 & Preview immune)."""
+        """Apply inline horizontal (>54d) and full-line vertical (>= 4 lines) overflow highlights (Box 0 & Preview immune)."""
         if not widget or not widget.winfo_exists():
             return
         if widget is getattr(self, "txt_dialogue_preview", None):
@@ -13660,9 +13661,11 @@
             text = widget.get("1.0", "end-1c")
             metrics = self._measure_dialogue_metrics(text)
             for info in metrics["lines"]:
+                ln = info["line_no"]
                 ov_start = info["overflow_raw_start"]
-                if ov_start is not None:
-                    ln = info["line_no"]
+                if ln >= 4:
+                    widget.tag_add("line_overflow", f"{ln}.0", f"{ln}.end")
+                elif ov_start is not None:
                     widget.tag_add("line_overflow", f"{ln}.{ov_start}", f"{ln}.end")
         except Exception:
             pass
```

### 5.1  Expected Post-Patch `misora.py` Metrics

| Metric | Pre-Edit (`b50c75e7`) | Post-Edit (Projected) |
|---|---|---|
| `git diff HEAD --numstat -- misora.py` | — | `7	4	misora.py` |
| Logical lines | `24,001` | `24,004` (`+3` net lines) |
| CRLF terminators | `24,000` | `24,003` |
| `bare_LF` / `bare_CR` | `0` / `0` | `0` / `0` |

---

## 6  Strict 4-File Ownership Matrix & Charter Gate

> [!WARNING]
> `misora.py` and `tests/**` are **ENV-01 READ-ONLY**. Executing T-04 Phase 2 requires a dedicated **one-time Project Lead T-04 Execution Charter** (explicitly distinct from ENV-01's docs-only READ-ONLY rules) authorizing ONLY the 4 files below.

| File | Action | Authorized Scope |
|---|---|---|
| `misora.py` | **MODIFY** | Surgical edit (`7	4`) to `_update_char_overflow_indicator` & `_apply_overflow_highlights` only |
| `tests/test_t04_overflow_line4_numerator.py` | **CREATE** | T-04 TDD suite: 4 failing-first Probes + 8 Regression Guards = 12 tests |
| `docs/project/OPEN_ISSUES.md` | **MODIFY** | Update T-04 row only (`MANUAL-PENDING` after TDD PASS; `Lifecycle: ACTIVE`) |
| `PROJECT_STATE.md` | **MODIFY** | Closeout baseline update (`<= 15,360` bytes; fix stale `Next planned task` & neutral wording) |
| All other repository files | **READ-ONLY** | Zero modifications permitted |

---

## 7  Zero-`.pyc` TDD Plan (`tests/test_t04_overflow_line4_numerator.py`)

### 7.1  Test Harness Isolation

- Pure stdlib `unittest` + `unittest.mock.patch` (zero `pytest`, zero `.unity3d` fixtures, zero `skipTest()`).
- In `setUp()`:
  1. Create temp dir via `tempfile.mkdtemp(prefix="misora_t04_")` and immediately register `self.addCleanup(shutil.rmtree, self.temp_dir, True)`.
  2. Patch `misora.CONFIG_PATH` to a fresh `{}` inside `self.temp_dir` (via `patch.object` + `self.addCleanup(...)`).
  3. Patch `misora.messagebox` (via `patch.object` + `self.addCleanup(...)`).
  4. Instantiate `self.app = MisoraApp(restore_session=False, show_splash=False)` and immediately register `self.addCleanup(...)` to safely destroy `self.app` so partial `setUp()` failures cannot leak Tk roots or temp directories.

### 7.2  Failing-First Probes (4 Probes — MUST fail pre-patch `FAILED (failures=4)`, `0` errors)

| ID | Method | Specification |
|---|---|---|
| **P1** | `test_probe_1_line4_gets_line_overflow_tag_in_dialogue` | 4-line short text (`"L1\nL2\nL3\nLine 4"`) in `txt_dialogue` -> `line_overflow` covers `"4.0"`..`"4.end"` and header shows `"4/3L"` in RED |
| **P2** | `test_probe_2_line5_gets_line_overflow_tag_in_dialogue` | 5-line short text -> `line_overflow` covers BOTH line 4 (`"4.0"`..`"4.end"`) and line 5 (`"5.0"`..`"5.end"`) and header shows `"5/3L"` in RED |
| **P3** | `test_probe_3_boundary_54d_numerator_shows_gt_prefix` | Deterministically mock `_measure_dialogue_metrics()` (DPI/font-independent) for BOTH sub-cases: (a) sub-digit overflow (`safe_w=540`, `digit_w=10`, `pixel_width=541`, `has_width_overflow=True` -> `round==54`) MUST display `">54/54d · 1/3L"` in RED; (b) normal `>= 55` overflow (`pixel_width=546` -> `round==55`) MUST display `"55/54d · 1/3L"` in RED (NOT `">55/54d"`) |
| **P4** | `test_probe_4_line4_with_width_overflow_highlights_full_line` | 4-line text where line 4 ALSO exceeds 54d width -> asserts `line_overflow` covers full `"4.0"`..`"4.end"` (genuinely fails pre-patch because pre-patch tags only `"4.<ov_start>"`..`"4.end"`) |

### 7.3  Regression Guards (8 Guards — MUST pass both pre-patch and post-patch)

| ID | Method | Specification |
|---|---|---|
| **G1** | `test_guard_1_width_overflow_55d_still_tagged` | 55-digit single line -> `line_overflow` tag present from `1.54`..`1.end` |
| **G2** | `test_guard_2_gutter_overflow_line4_still_tagged` | 4-line text -> `gutter_overflow` tag covers `"4.0"`..`tk.END` |
| **G3** | `test_guard_3_all_script_cards_zero_overflow` | All Script view cards remain zero `line_overflow` / `gutter_overflow` |
| **G4** | `test_guard_4_preview_zero_overflow` | Dialogue Preview remains zero `line_overflow` |
| **G5** | `test_guard_5_quick_edit_zero_overflow` | Quick Edit remains zero `line_overflow` / `gutter_overflow` |
| **G6** | `test_guard_6_box0_immune` | Box 0 shows `"Metadata (unmeasured)"` with zero overflow tags |
| **G7** | `test_guard_7_header_label_muted_at_54d_no_width_overflow` | Deterministic mock `safe_w=540`, `digit_w=10`, `pixel_width=540`, `has_width_overflow=False`, `has_line_overflow=False` -> `"54/54d · 1/3L"` in MUTED color (no `">"`) |
| **G8** | `test_guard_8_line3_no_overflow_tag` | 3-line non-width-overflow text -> `line_overflow` tag ranges empty (`()`) |

### 7.4  Locked Suite Arithmetic & Verification Gates

| Stage | Command / Metric | Locked Expected Result |
|---|---|---|
| Pre-T-04 baseline | `TestLoader().discover('tests').countTestCases()` | `504` |
| Pre-patch T-04 run | `py -3.12 -B -m unittest tests/test_t04_overflow_line4_numerator.py` | `Ran 12 tests ... FAILED (failures=4)` (`0` errors) |
| Post-patch T-04 run | `py -3.12 -B -m unittest tests/test_t04_overflow_line4_numerator.py` | `Ran 12 tests ... OK` (`12/12 PASS`) |
| Post-patch targeted suites | `test_p3_s17_pixel_rulers`, `test_v15_s02_fonts_ruler_metrics`, `test_v15_s09_core_fixes_54d`, `test_t02_next_tooltip` | All `OK` (`0` new regressions) |
| Post-patch discovery | `TestLoader().discover('tests').countTestCases()` | `504 + 12 = 516` (`4 Probes + 8 Guards`) |
| Post-patch full suite | `py -3.12 -B -m unittest discover -s tests -t .` | **`516 = 473 PASS + 35 SKIP + 6 FAIL + 2 ERROR`** (`+12 PASS`, `0` new regressions) |
| Syntax & `.pyc` gate | BOM-safe in-memory `compile()` (`89` `.py` files) + `.pyc` count check | `IN_MEMORY_COMPILE_OK: 89`; `pre_pyc_count == post_pyc_count` (`125 == 125`) |

---

## 8  Pinned Rollback Commands

All rollback commands are pinned to exact baseline SHA `b50c75e7555779cbff0b6821933e11b5f7ef9bf9` (NO `HEAD`, NO `git reset --hard`, NO `git clean`, NO blanket `git checkout`):

```powershell
cd D:\Misora-Editor
git checkout b50c75e7555779cbff0b6821933e11b5f7ef9bf9 -- misora.py docs/project/OPEN_ISSUES.md PROJECT_STATE.md
Remove-Item tests\test_t04_overflow_line4_numerator.py -Force -ErrorAction SilentlyContinue

# Post-rollback verification
git status --short --untracked-files=all
py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"
py -3.12 -B -c "raw=open('misora.py','rb').read(); crlf=raw.count(b'\r\n'); print('lines=', len(raw.decode('utf-8').splitlines()), 'crlf=', crlf, 'bare_lf=', raw.count(b'\n')-crlf, 'bare_cr=', raw.count(b'\r')-crlf)"
```

Expected rollback verification: clean `git status`, `countTestCases: 504`, `lines= 24001 crlf= 24000 bare_lf= 0 bare_cr= 0`.

---

## 9  Windows Manual QA Checklist (`M-1..M-9`)

### M-1: Line 4+ Red Inline Marker (Defect A)
1. Open any `.unity3d` story file and navigate to an ordinary dialogue box (Box ≥ 1).
2. Enter 4 lines (`Line 1\nLine 2\nLine 3\nLine 4`).
3. **Verify**: Line 4 text in `txt_dialogue` has red background + underline (`line_overflow` tag); gutter line `4` is red bold; header label displays `N/54d · 4/3L` in RED.

### M-2: Line 4+ Combined Width + Vertical Overflow
1. Enter 4 lines where line 4 also exceeds 54 digit-widths (`"1234567890"*6` on line 4).
2. **Verify**: The **entire** line 4 (characters `0` through end, not just past `54d`) has red background + underline.

### M-3: Horizontal Width Overflow Only (Lines 1–3)
1. Enter 55+ digits on line 1 within `<= 3` lines.
2. **Verify**: Characters past `54d` have red background + underline; lines 1–3 within `54d` remain unhighlighted; header label displays `55/54d · 1/3L` (or `>54/54d · 1/3L` if sub-digit) in RED.

### M-4: `54/54d` Boundary Numerator (Defect B)
1. Enter exactly 54 digits (`"1234567890"*5 + "1234"`) in a font slightly wider than Nunito Bold where `has_width_overflow` triggers at `round == 54`.
2. **Verify**: RED header label displays `">54/54d · 1/3L"` (never `"54/54d · 1/3L"` in red).
3. Switch to Global preset (Nunito Bold) with exact 54 digits.
4. **Verify**: Header label displays `"54/54d · 1/3L"` in MUTED color (no `">"`).

### M-5: Box 0 Immunity
1. Navigate to Box 0 (metadata).
2. **Verify**: Header displays `"Metadata (unmeasured)"` in muted color; zero overflow tags on metadata fields.

### M-6: All Script Zero Markers
1. Switch to All Script view on a document containing 55d + 4L overflow boxes.
2. **Verify**: All Script card bodies have ZERO `line_overflow` and ZERO `gutter_overflow` tags while normal card headers (`▶ [BOX #NNN]` active / `◆ [BOX #NNN]` inactive) remain intact.

### M-7: Dialogue Preview Zero Markers
1. Toggle Preview ON (compiled mode) on an overflowing box.
2. **Verify**: `txt_dialogue_preview` has ZERO `line_overflow` blocks.

### M-8: Quick Edit Zero Markers
1. Switch to Quick Edit tab on an overflowing box.
2. **Verify**: `txt_quick_edit` has ZERO `line_overflow` and ZERO `gutter_overflow` tags.

### M-9: Theme Toggle Persistence
1. Toggle between Light and Dark themes while viewing a 4-line overflowing box.
2. **Verify**: `line_overflow`, `gutter_overflow`, and `lbl_char_overflow` update immediately with theme-appropriate contrast colors.

---

## 10  Closeout Docs Hygiene (`PROJECT_STATE.md`, `OPEN_ISSUES.md`, & N-4 Note)

1. **`PROJECT_STATE.md`** (must stay `<= 15,360` bytes; currently `6,469` bytes):
   - Update §2 verification table to `516` total (`473 PASS + 35 SKIP + 6 FAIL + 2 ERROR`, `0` new T-04 regressions) using neutral wording (`"516 methods: 473 PASS, 35 SKIP, 6 FAIL, and 2 ERROR; existing failures and errors remain baseline debt"` — never `"completed cleanly"`).
   - Fix the stale §5 `Next planned task` line (which currently still says T-08a `M-1..M-6 MANUAL-PENDING`) to reflect T-04 (`MANUAL-PENDING`), while preserving T-08a as `Lifecycle: ACTIVE` for its open main-window off-screen `_deferred_restore()` / `sanitize_window_geometry` sub-item.
2. **`docs/project/OPEN_ISSUES.md`**:
   - Update the T-04 row only to record TDD `12/12 PASS`, `MANUAL-PENDING` (Windows Manual QA `M-1..M-9`), and `Lifecycle: ACTIVE`.
3. **N-4 Transient `--check` Note**:
   - Because T-04 modifies `misora.py` without changing top-level symbol names/signatures (`+3` net lines inside existing methods), line numbers in `docs/architecture/MISORA_SYMBOL_INDEX.md` may shift if audited post-patch; any resulting `tools/generate_symbol_index.py --check` drift is **transient N-4**, with symbol-index regeneration deferred to the Project Lead post-commit.

---

STOP — WAITING FOR FINAL CLEARANCE
