# T-04 Implementation Plan — Overflow Marker on Line 4+ / >3L & 54/54d Numerator Boundary Audit

> **Phase**: 1b (Read-Only Source Audit & Implementation Plan)
> **Task**: T-04 — Overflow Marker on Line 4+ / >3L & 54/54d Numerator Boundary
> **Date**: 2026-11-28
> **Baseline**: `main` @ `b50c75e7` (post-T-08a closeout)
> **Product**: 1.4.15

---

## 1  Preflight & Baseline Verification

### 1.1  Repository State

| Check | Result |
|---|---|
| Branch | `main` |
| HEAD | `b50c75e7555779cbff0b6821933e11b5f7ef9bf9` |
| `git status --short` | *(empty — clean working tree)* |
| `__init__.__version__` | `1.4.15` ✅ |
| `compileall -q .` exit code | `0` ✅ |

### 1.2  .pyc Invariant

| Metric | Value |
|---|---|
| `pre_pyc_count` (before audit) | 125 |
| `post_pyc_count` (after audit) | 125 ✅ |

> [!NOTE]
> `py -3.12 -B -m compileall -q .` created 2 stale .pyc (the `-B` flag prevents *import*-time bytecode but `compileall` explicitly writes cache). These were:
> - `tools/__pycache__/generate_symbol_index.cpython-312.pyc`
> - `tests/__pycache__/test_t08a_tooltip_clamping.cpython-312.pyc`
>
> Both were removed to restore the invariant. All subsequent probes used `py -3.12 -B` without `compileall` to avoid this.

### 1.3  Test Count Verification (AST-based, no Tk)

| Metric | Value |
|---|---|
| Total `test_*` methods across 64 test files | **504** ✅ |
| Expected breakdown | 461 PASS + 35 SKIP + 6 FAIL + 2 ERROR |

> [!NOTE]
> Live `unittest discover` hangs in the headless sandbox (Tk initialization). The AST-based method count matches the user's stated total of 504.

---

## 2  Verbatim Source Audit

### 2.1  Constants (misora.py L457–L458)

```python
# misora.py:457-458
DIALOGUE_MAX_DIGITS: int = 54
DIALOGUE_MAX_LINES: int = 3
```

### 2.2  Overflow Color Constants

| Location | Light Theme | Dark Theme | Usage |
|---|---|---|---|
| `_update_char_overflow_indicator` L13633 | `#c9184a` | `#ff5c7c` | Label `fg` when overflow |
| `_apply_gutter_overflow_tag` L13681 | `#c9184a` | `#ff5c7c` | Gutter line-number fg L4+ |
| `_configure_editor_rich_tags` L3748–3759 | bg `#ffd6dc`, fg auto-contrast | bg `#4a1c24`, fg auto-contrast | `line_overflow` text tag |
| `_draw_single_pixel_ruler` L13703–13704 | zone `#ffd6dc`, fg `#c9184a` | zone `#4a1c24`, fg `#ff5c7c` | Canvas ruler red zone |

### 2.3  `_measure_dialogue_metrics()` — L13544–L13611

```python
# misora.py:13544-13611 (key excerpts)
def _measure_dialogue_metrics(self, text: str) -> Dict[str, Any]:
    f = self._get_dialogue_measure_font()       # active editor font
    safe_w = self._get_54d_reference_safe_w()    # Nunito Bold constant reference
    digit_w = safe_w / float(DIALOGUE_MAX_DIGITS)
    # ...
    # Per-line: binary-search for overflow_raw_start where pixel_width > safe_w
    if pixel_width > safe_w and units:           # L13585 — strictly greater
        # ...binary search...
        overflow_raw_start = units[lo - 1][0]    # L13594
    # ...
    line_count = len(raw_lines)                  # L13603
    return {
        "safe_w": safe_w,
        "digit_w": digit_w,
        "line_count": line_count,
        "has_line_overflow": line_count >= 4,     # L13608 — ≥4 lines = ≥3 linebreaks
        "has_width_overflow": any(l["overflow_raw_start"] is not None for l in line_metrics),  # L13609
        "lines": line_metrics,
    }
```

**Key design**: Two separate boolean flags — `has_line_overflow` (vertical, ≥4 lines) and `has_width_overflow` (horizontal, any line > safe_w pixels).

### 2.4  `_update_char_overflow_indicator()` — L13613–L13637

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
    d_equiv = int(round(max_px / digit_w))             # ← NUMERATOR FORMULA
    line_count = metrics["line_count"]
    is_ov = bool(metrics["has_width_overflow"] or metrics["has_line_overflow"])  # ← COLOR THRESHOLD
    ov_fg = "#c9184a" if self._is_light_theme() else "#ff5c7c"
    lbl.config(
        text=f"{d_equiv}/{DIALOGUE_MAX_DIGITS}d · {line_count}/{DIALOGUE_MAX_LINES}L",  # ← FORMAT
        fg=ov_fg if is_ov else t["fg_muted"],
    )
```

### 2.5  `_apply_overflow_highlights()` — L13639–L13668

```python
# misora.py:13639-13668 (verbatim)
def _apply_overflow_highlights(self, widget: Optional[tk.Text]) -> None:
    """Apply inline pixel-calibrated horizontal overflow highlights on a Text widget (Box 0 & Preview immune)."""
    # ... guards for None, Preview, Box 0 ...
    try:
        widget.tag_remove("line_overflow", "1.0", tk.END)
        text = widget.get("1.0", "end-1c")
        metrics = self._measure_dialogue_metrics(text)
        for info in metrics["lines"]:
            ov_start = info["overflow_raw_start"]
            if ov_start is not None:                     # ← WIDTH OVERFLOW ONLY
                ln = info["line_no"]
                widget.tag_add("line_overflow", f"{ln}.{ov_start}", f"{ln}.end")
    except Exception:
        pass
```

> [!IMPORTANT]
> **Missing behavior**: `_apply_overflow_highlights` only tags characters past the 54d width boundary. It does NOT apply any visual indicator on lines 4+ (the >3L / `has_line_overflow` case). Lines 4, 5, 6… get NO red text highlight even though they represent overflow.

### 2.6  `_apply_gutter_overflow_tag()` — L13670–L13693

```python
# misora.py:13670-13693 (verbatim)
def _apply_gutter_overflow_tag(self, gutter_widget: Optional[tk.Text]) -> None:
    """Color vertical line-number gutter red from line 4+ (3 or more linebreaks)."""
    # ... guards ...
    try:
        ov_fg = "#ff5c7c" if not self._is_light_theme() else "#c9184a"
        d_sz = self.dialogue_font_size
        gutter_widget.tag_configure(
            "gutter_overflow",
            foreground=ov_fg,
            font=self._get_dialogue_font_tuple(d_sz, "bold"),
        )
        gutter_widget.tag_remove("gutter_overflow", "1.0", tk.END)
        total_lines = int(gutter_widget.index("end-1c").split(".")[0])
        if total_lines >= 4:                              # ← CORRECT threshold
            gutter_widget.tag_add("gutter_overflow", "4.0", tk.END)
    except Exception:
        pass
```

✅ Gutter correctly highlights lines 4+ red. No defect here.

### 2.7  `_draw_single_pixel_ruler()` — L13695–L13746

Canvas ruler renders:
- Tick marks at digit intervals up to `DIALOGUE_MAX_DIGITS` (54) + a few beyond
- Red zone background past 54d (L13717)
- "54d" label at boundary, ">54d" label past it (L13731–13746)

✅ No defect in ruler rendering.

### 2.8  Label Creation (L5656–L5667)

```python
# misora.py:5656-5663
self.lbl_char_overflow = tk.Label(
    gd_header,
    text=f"0/{DIALOGUE_MAX_DIGITS}d · 1/{DIALOGUE_MAX_LINES}L",
    font=("Segoe UI", max(8, u_sz - 1)),
    bg=t["bg_panel"],
    fg=t["fg_muted"],
)
```

Initial text: `"0/54d · 1/3L"` — always starts muted.

### 2.9  Callers of `_update_char_overflow_indicator()`

| Location | Context |
|---|---|
| L3405 | `_apply_theme()` / font change refresh |
| L9986 | `_update_views()` during Box 0 display |
| L10061 | `_update_views()` normal box display |
| L11077 | `_refresh_box_view()` after content load |
| L12330 | All Script Box 0 click (passes `""`) |
| L12353 | All Script card click (passes `box.clean_text`) |
| L12489–12492 | All Script nav scrolling |
| L12874 | Quick Edit commit |
| L13253 | Dialogue edit commit (multi-seg) |
| L13279 | Dialogue edit commit (plain text) |
| L19478 | Auto Word Wrap completion |

### 2.10  Quick Edit — Zero Overflow (L6738)

```python
# misora.py:6738
# Quick Edit Tab Body (Q-22 unified single-box surface parity with Dialogue Editor; zero ruler / red overflow)
```

Quick Edit explicitly has zero overflow markers — no `line_overflow` or `gutter_overflow` tags applied. ✅ No conflict.

### 2.11  All Script Preview Cards — Zero Overflow (L11999)

```python
# misora.py:11999
"""Write read-only 54d x 3 dialogue body with zero red overflow markers."""
# ...
txt.tag_remove("line_overflow", "1.0", tk.END)   # L12025
txt.tag_remove("gutter_overflow", "1.0", tk.END)  # L12026
```

All Script cards explicitly strip overflow markers. ✅ No conflict.

### 2.12  Import Dialog Overflow Badges (L21037–21088, L21447)

The `ImportFromXUATDialog` uses `▼` (line overflow) and `▶` (width overflow) badge labels with its own `lines >= 3 and has_line_overflow` logic. These are display-only badges, not `line_overflow` text tags. ✅ No conflict.

---

## 3  Existing Test Coverage Audit

### 3.1  Tests Directly Covering Overflow Logic

| Test File | Test Method | What It Tests |
|---|---|---|
| `test_p3_s17_pixel_rulers.py` | `test_01_probe_pixel_measure_rulers_and_overflow` | 54d/55d width boundary, `has_width_overflow`, `overflow_raw_start`, kanji overflow, `line_overflow` tag in Dialogue, `gutter_overflow` tag in gutter, All Script zero markers |
| `test_v15_s02_fonts_ruler_metrics.py` | `test_01_probe_pixel_measure_rulers_and_overflow` | Same scope as S17 (re-verification) |
| `test_v15_s09_core_fixes_54d.py` | `test_probe_4_shared_54d_reference_pixel_contract_and_box0_immunity` | 54d reference constant across presets, ruler "54d"/">54d" labels, header indicator "/54d · /3L", Box 0 immunity |
| `test_t02_next_tooltip.py` | `test_probe_1_overflow_tooltip_uses_54d_and_dual_font_wording` | Tooltip wording: 54d, dual-font phrasing |
| `test_t02_next_tooltip.py` | `test_guard_2_overflow_label_initial_text_is_dynamic` | Initial label text `"0/54d · 1/3L"` |
| `test_p3_s18_game_preview.py` | `test_probe_1_dialogue_preview_*` | Dialogue Preview zero `line_overflow`, All Script zero markers |
| `test_v15_s11b_scanner_save_preview.py` | `test_probe_3_q23_*` | Preview zero `line_overflow`; Dialogue Editor retains them |
| `test_v15_s10_all_script_quick_edit.py` | multiple | All Script zero overflow tags, Quick Edit zero overflow tags |
| `test_v15_s11c_quick_edit_unified.py` | multiple | Quick Edit zero `line_overflow`/`gutter_overflow` |

### 3.2  Tests That Will NOT Conflict with T-04

None of the existing tests assert that lines 4+ should have ZERO `line_overflow` tags in the Dialogue Editor. The only tests asserting `line_overflow == ()` do so for:
- All Script cards (by design — zero red markers)
- Dialogue Preview (by design — zero red markers)
- Quick Edit (by design — zero red markers)
- 3-line non-width-overflow content in Dialogue Editor

**Zero-conflict verdict**: Adding `line_overflow` tags to lines 4+ in the Dialogue Editor text widget will not break any existing test. ✅

---

## 4  Root-Cause Analysis

### 4.1  Defect A — Line 4+ (>3L) Missing Red Inline Marker

**AGENTS.md §7 requirement** (L13608 implementation note):
> "54 digit-widths or 3+ hard linebreaks (4+ lines)"

**Current behavior**:
1. ✅ `_measure_dialogue_metrics` correctly sets `has_line_overflow = line_count >= 4` (L13608)
2. ✅ `_update_char_overflow_indicator` correctly turns the header label RED when `has_line_overflow` (L13632)
3. ✅ `_apply_gutter_overflow_tag` correctly turns line numbers 4+ RED in the gutter (L13690–13691)
4. ❌ `_apply_overflow_highlights` does NOT add `line_overflow` text tag to lines 4+ — only to width-overflowing characters (L13662–13666)

**Root cause**: `_apply_overflow_highlights()` at L13662–13666 iterates `metrics["lines"]` but only tags characters where `overflow_raw_start is not None` (width overflow). It never checks `metrics["has_line_overflow"]` or the line_count. Lines 4+ get no red background highlight in the dialogue text widget.

**Minimal fix**: After the existing width-overflow loop in `_apply_overflow_highlights()`, add a check: if `metrics["has_line_overflow"]`, tag the entire text content of lines 4+ with `line_overflow`. This gives lines 4, 5, 6, … the same red background + underline treatment as width-overflowing characters.

### 4.2  Defect B — 54/54d Numerator Display at Boundary

**T-02 M-4 QA observation**: "hitting the boundary turned `lbl_char_overflow` red while displaying `54/54d · 1/3L` instead of `>54/54d`."

**Analysis of the numerator formula** (L13628–13635):

```python
digit_w = max(1e-6, float(metrics["digit_w"]))      # digit_w = safe_w / 54
max_px = max((l["pixel_width"] for l in metrics["lines"]), default=0)
d_equiv = int(round(max_px / digit_w))               # numerator
```

**Key architectural insight**: `safe_w` is measured with the **ruler font** (Nunito Bold, constant), but `max_px` is measured with the **dialogue font** (active editor font, variable). These are intentionally different fonts.

**Case analysis for exactly 54 digits of `"1234567890"×5+"1234"`**:

| Scenario | `safe_w` (Nunito Bold) | `pixel_width` (dialogue font) | `has_width_overflow` | `d_equiv` | Label Color |
|---|---|---|---|---|---|
| Dialogue font narrower than Nunito Bold | e.g. 500px | e.g. 480px | `False` (480 ≤ 500) | `int(round(480/9.26))` ≈ 52 | MUTED ✅ |
| Dialogue font matches Nunito Bold | 500px | 500px | `False` (500 ≤ 500, strict >) | `int(round(500/9.26))` = 54 | MUTED ✅ |
| Dialogue font wider than Nunito Bold | 500px | 510px | `True` (510 > 500) | `int(round(510/9.26))` ≈ 55 | RED ✅ |

**The T-02 M-4 observation** ("54/54d red") occurs when the dialogue font renders 54 characters to a pixel width that is:
- Slightly wider than `safe_w` (triggering `has_width_overflow = True`, making label RED)
- But `d_equiv = int(round(max_px / digit_w))` rounds down to exactly 54

This is a **rounding-precision boundary** issue. When the dialogue font is slightly wider than Nunito Bold for the same 54 digits:
- `max_px` = e.g. 501px vs `safe_w` = 500px → `has_width_overflow = True`
- `d_equiv = int(round(501 / (500/54)))` = `int(round(54.108))` = 54

**The label shows "54/54d" in RED** — technically correct (the content DOES overflow the reference boundary), but visually confusing because "54/54d" looks like it's at the limit, not over it.

**Root cause**: The numerator `d_equiv` uses `int(round(...))` which can round to 54 even when `has_width_overflow` is True. The format string `f"{d_equiv}/{DIALOGUE_MAX_DIGITS}d"` never prefixes ">" to indicate overflow.

**Minimal fix**: When `has_width_overflow` is True AND `d_equiv <= DIALOGUE_MAX_DIGITS`, either:
- **(Option A — Recommended)**: Clamp numerator to `max(d_equiv, DIALOGUE_MAX_DIGITS + 1)` when `has_width_overflow` is True, so it always shows ≥55 when overflowing. This may be misleading for the sub-digit precision case.
- **(Option B — Preferred)**: Prefix ">" when `has_width_overflow` and `d_equiv == DIALOGUE_MAX_DIGITS`: display `">54/54d"` instead of `"54/54d"`. This is consistent with the ruler's `">54d"` label.

**Recommended**: **Option B** — prefix `">"` for the width-overflow boundary edge case.

---

## 5  Minimal Unified Diff Against Current HEAD

### 5.1  Diff for `_apply_overflow_highlights()` (Defect A)

```diff
--- a/misora.py
+++ b/misora.py
@@ -13658,6 +13658,13 @@
         try:
             widget.tag_remove("line_overflow", "1.0", tk.END)
             text = widget.get("1.0", "end-1c")
             metrics = self._measure_dialogue_metrics(text)
             for info in metrics["lines"]:
                 ov_start = info["overflow_raw_start"]
                 if ov_start is not None:
                     ln = info["line_no"]
                     widget.tag_add("line_overflow", f"{ln}.{ov_start}", f"{ln}.end")
+            # Tag entire content of lines 4+ (>3L overflow) with line_overflow
+            if metrics["has_line_overflow"]:
+                for info in metrics["lines"]:
+                    if info["line_no"] >= 4:
+                        ln = info["line_no"]
+                        if info["overflow_raw_start"] is None:  # not already tagged by width overflow
+                            widget.tag_add("line_overflow", f"{ln}.0", f"{ln}.end")
         except Exception:
             pass
```

### 5.2  Diff for `_update_char_overflow_indicator()` (Defect B)

```diff
--- a/misora.py
+++ b/misora.py
@@ -13630,8 +13630,13 @@
         d_equiv = int(round(max_px / digit_w))
         line_count = metrics["line_count"]
         is_ov = bool(metrics["has_width_overflow"] or metrics["has_line_overflow"])
         ov_fg = "#c9184a" if self._is_light_theme() else "#ff5c7c"
+        # Prefix ">" when width overflows but d_equiv rounds to boundary
+        d_prefix = ""
+        if metrics["has_width_overflow"] and d_equiv <= DIALOGUE_MAX_DIGITS:
+            d_prefix = ">"
         lbl.config(
-            text=f"{d_equiv}/{DIALOGUE_MAX_DIGITS}d · {line_count}/{DIALOGUE_MAX_LINES}L",
+            text=f"{d_prefix}{d_equiv}/{DIALOGUE_MAX_DIGITS}d · {line_count}/{DIALOGUE_MAX_LINES}L",
             fg=ov_fg if is_ov else t["fg_muted"],
         )
```

---

## 6  Strict File Ownership Matrix

| File | Access | Scope |
|---|---|---|
| `misora.py` | **READ-WRITE** (ENV-01 exception required) | 2 surgical edits: `_apply_overflow_highlights` + `_update_char_overflow_indicator` |
| `tests/test_t04_overflow_line4_numerator.py` | **CREATE** | New test file for T-04 probes + guards |
| All other files | **READ-ONLY** | No modifications permitted |

> [!WARNING]
> `misora.py` is ENV-01 READ-ONLY. T-04 implementation requires explicit Project Lead authorization to modify it.

---

## 7  Zero-.pyc TDD Plan

### 7.1  Test File

**New file**: `tests/test_t04_overflow_line4_numerator.py`

### 7.2  Probes (Failing-First, Pass After Patch)

| ID | Test Method | What It Tests |
|---|---|---|
| P1 | `test_probe_1_line4_gets_line_overflow_tag_in_dialogue` | 4-line text in Dialogue Editor → `line_overflow` tag ranges include line 4 characters |
| P2 | `test_probe_2_line5_gets_line_overflow_tag_in_dialogue` | 5-line text → lines 4 AND 5 both get `line_overflow` tags |
| P3 | `test_probe_3_boundary_54d_numerator_shows_gt_prefix` | Exactly-54-digits in a wider-than-Nunito font → label shows `">54/54d"` when `has_width_overflow` is True but `d_equiv` rounds to 54 |
| P4 | `test_probe_4_line3_no_overflow_tag` | 3-line text (no width overflow) → `line_overflow` tag ranges are empty (lines 1–3 are within limits) |

### 7.3  Guards (Pass Both Before and After Patch)

| ID | Test Method | What It Tests |
|---|---|---|
| G1 | `test_guard_1_width_overflow_55d_still_tagged` | 55-digit line → `line_overflow` tag present (width overflow unbroken) |
| G2 | `test_guard_2_gutter_overflow_line4_still_tagged` | 4-line text → `gutter_overflow` tag on lines 4+ (gutter unbroken) |
| G3 | `test_guard_3_all_script_cards_zero_overflow` | All Script cards remain zero `line_overflow` / `gutter_overflow` |
| G4 | `test_guard_4_preview_zero_overflow` | Dialogue Preview remains zero `line_overflow` |
| G5 | `test_guard_5_quick_edit_zero_overflow` | Quick Edit remains zero `line_overflow` / `gutter_overflow` |
| G6 | `test_guard_6_box0_immune` | Box 0 → "Metadata (unmeasured)", zero overflow tags |
| G7 | `test_guard_7_header_label_muted_at_exactly_54d_no_width_overflow` | Exactly 54 digits in Nunito Bold (same font = no width overflow) → label MUTED, no ">" prefix |

### 7.4  Locked Suite Arithmetic

| Metric | Count |
|---|---|
| Pre-T-04 total | 504 |
| New Probes | +4 |
| New Guards | +7 |
| **Post-T-04 total** | **515** |

Breakdown: 504 + 11 = **515 test methods**.

> [!IMPORTANT]
> All probes run with `py -3.12 -B`. The `.pyc` invariant must hold: `pre_pyc_count == post_pyc_count` after every test run.

---

## 8  Rollback Commands

If any step fails and needs to be reverted:

```powershell
# Revert misora.py to HEAD (safe — git checkout of a single tracked file)
cd D:\Misora-Editor
git checkout HEAD -- misora.py

# Remove new test file (not yet tracked)
Remove-Item tests\test_t04_overflow_line4_numerator.py -Force -ErrorAction SilentlyContinue
```

> [!CAUTION]
> Do NOT use `git reset --hard`, `git clean`, or blanket `git checkout`. These are forbidden by AGENTS.md §2 and the safety rules.

---

## 9  Windows Manual QA Checklist

### M-1: Line 4+ Red Inline Marker (Defect A)

1. Open any `.unity3d` story file
2. Navigate to a dialogue box
3. Enter text with 4+ lines (3+ hard linebreaks): `Line 1\nLine 2\nLine 3\nLine 4`
4. **Verify**: Lines 4+ in `txt_dialogue` have red background highlight (`line_overflow` tag)
5. **Verify**: Gutter line numbers 4+ are red bold
6. **Verify**: Header label shows `N/54d · 4/3L` in RED

### M-2: Width Overflow Still Works

1. Enter 55+ digits on a single line: `1234567890` × 6
2. **Verify**: Characters past the 54d boundary have red background highlight
3. **Verify**: Header label shows `>54/54d · 1/3L` in RED (or `55/54d` if `d_equiv` rounds to 55)

### M-3: Combined Width + Line Overflow

1. Enter 55+ digits on line 1, with 4+ lines total
2. **Verify**: Line 1 has width-overflow red highlight past 54d
3. **Verify**: Lines 4+ have full-line red highlight
4. **Verify**: Header label RED, both overflow indicators active

### M-4: 54/54d Numerator Boundary (Defect B)

1. Enter exactly 54 digits: `12345678901234567890123456789012345678901234567890` + `1234`
2. Switch to a dialogue font where 54 chars slightly exceeds the Nunito Bold reference width
3. **Verify**: If `has_width_overflow` triggers, label shows `">54/54d · 1/3L"` (not `"54/54d"`)
4. **Verify**: If no width overflow (font narrower or equal), label shows `"54/54d · 1/3L"` MUTED (no ">" prefix)

### M-5: Box 0 Immunity

1. Navigate to Box 0 (metadata)
2. **Verify**: Header shows "Metadata (unmeasured)" in muted color
3. **Verify**: No `line_overflow` or `gutter_overflow` tags on metadata text

### M-6: All Script Zero Markers

1. Switch to All Script view
2. Load a document with 55-digit + 4-line overflow boxes
3. **Verify**: All Script card bodies have ZERO `line_overflow` and `gutter_overflow` tags
4. **Verify**: Overflow badges (▼▶) display correctly on card headers

### M-7: Dialogue Preview Zero Markers

1. Toggle Preview ON (compiled mode)
2. **Verify**: `txt_dialogue_preview` has ZERO `line_overflow` tags

### M-8: Quick Edit Zero Markers

1. Switch to Quick Edit tab
2. **Verify**: `txt_quick_edit` has ZERO `line_overflow` and `gutter_overflow` tags

### M-9: Theme Toggle Persistence

1. Switch between Light and Dark themes
2. **Verify**: Overflow colors update correctly for both themes
3. **Verify**: Gutter overflow, text overflow, and header label all use correct theme colors

---

## STOP — WAITING FOR FINAL CLEARANCE

> [!IMPORTANT]
> This plan requires:
> 1. **ENV-01 write authorization** for `misora.py` (2 surgical edits)
> 2. **Project Lead approval** of the proposed diffs in §5
> 3. **Explicit "Proceed"** to begin Phase 2 implementation
>
> No files in `D:\Misora-Editor` have been modified. This plan was written to `D:\Reference\Misora-Reference\T-04_Implementation_Plan.md` only.
