# T-08a Implementation Plan (Rev 2) — `BUG-UI-TOOLTIP-CLIP-01` ToolTip Screen-Edge Clipping

**Task:** T-08a (split from T-08/`BUG-39`/`FEAT-04`)
**Revision:** Rev 2 (addresses all 6 Gemini review hold items prior to GPT-6 / Qwen review)
**Evidence:** `CONFIRMED` + `ROOT-CAUSE: NEEDS-CODE-VERIFY` → upgraded to `ROOT-CAUSE: SOURCE-OBSERVED` by this plan
**Lifecycle:** `ACTIVE`
**Version:** `1.4.15` (UNCHANGED — no version promotion authorized)
**Branch:** `main`

> [!IMPORTANT]
> This plan is **READ-ONLY** and authorizes **ZERO file modifications** inside `D:\Misora-Editor`.
> Implementation requires independent review and explicit Project Lead `Proceed`.

---

## 1. Preflight Transcript

| Check | Result |
|---|---|
| `git -C D:\Misora-Editor rev-parse --show-toplevel` | `D:/Misora-Editor` |
| `git -C D:\Misora-Editor branch --show-current` | `main` |
| `git -C D:\Misora-Editor rev-parse HEAD` | `9fa266375caf0994e49c9ed5ce8b7b1203b28f3c` (**POST_DOCS01_HEAD**) |
| `git -C D:\Misora-Editor status --short --untracked-files=all` | **(empty — clean tree)** |
| `py -3.12 -B -c "import __init__; print(__init__.__version__)"` | `1.4.15` |
| `py -3.12 -B tools/generate_symbol_index.py --check` | `CHECK PASS: docs/architecture/MISORA_SYMBOL_INDEX.md` |
| `py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"` | `countTestCases: 494` |
| `misora.py` logical lines (`splitlines(True)` / 1-based EOF line) | `23,912` (`23,911` CRLF line terminators; final line `23,912` has no trailing newline) |
| `misora.py` `bare_LF` / `bare_CR` | `bare_LF == 0`, `bare_CR == 0` |
| `misora.py` total bytes | `1,100,212` |

**Prerequisite Gate — DOCS-01 COMMITTED:**
- `AGENTS.md` §7 line 40: `"Native overflow: 54 digit-widths or 3+ hard linebreaks (4+ lines); editor font is an estimate. Preserve Box 0 invariants."` ✅
- `docs/project/OPEN_ISSUES.md` line 32 contains `T-08a` (`(split from T-08/BUG-39/FEAT-04)`). ✅
- HEAD `9fa266375caf0994e49c9ed5ce8b7b1203b28f3c` is commit `"DOCS-01: Close T-02 QA, sync ledgers & Option A roadmap, fix AGENTS.md §7 50->54 (docs-only, 0 .py)"`. ✅

---

## 2. Verbatim ToolTip Source Audit & Import / Test-Compatibility Verification

### 2.1 Module-Level Imports Verified in `misora.py` (Read-Only)

| Symbol | Exact `file:line` | Scope | Notes |
|---|---|---|---|
| `ctypes` | `misora.py:15` | Unconditional module scope | `import ctypes` |
| `sys` | `misora.py:24` | Unconditional module scope | `import sys` |
| `Optional`, `Tuple` | `misora.py:33` | Unconditional module scope | `from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, Union` |
| `wintypes` | `misora.py:42-44` | **Conditional** (`if sys.platform == "win32":`) | `from ctypes import wintypes` |

Because `wintypes` at `misora.py:44` is conditionally imported inside `if sys.platform == "win32":`, the new `_get_work_area()` helper explicitly performs `from ctypes import wintypes as _wt` inside `if sys.platform == "win32":` + `try/except`, ensuring `NameError` can **never** occur or trigger silent fallback even if module-scope `wintypes` were absent.

### 2.2 Complete `ToolTip` class — `misora.py:202–295`

```python
# misora.py:202-295  (verbatim at 9fa26637)
class ToolTip:
    """Robust hover tooltip for Tkinter widgets with delayed display and safe lifecycle (Part C.5 / TOOLTIP-LIFECYCLE)."""

    def __init__(self, widget: tk.Widget, text: str, delay_ms: int = 350):
        self.widget = widget
        self.text = text
        self.delay_ms = delay_ms
        self.tip_window: Optional[tk.Toplevel] = None
        self._label: Optional[tk.Label] = None
        self._after_id: Optional[str] = None
        setattr(self.widget, "_tooltip", self)

        if hasattr(self.widget, "bind"):
            self.widget.bind("<Enter>", self.on_enter, add="+")
            self.widget.bind("<Leave>", self.on_leave, add="+")
            self.widget.bind("<Destroy>", self.on_destroy, add="+")

    def set_text(self, text: str) -> None:
        """Update tooltip text dynamically, syncing any visible tooltip label."""
        self.text = text
        if self._label is not None:
            try:
                if self._label.winfo_exists():
                    self._label.configure(text=text)
            except Exception:
                pass

    def on_enter(self, _event=None) -> None:
        self.cancel_timer()
        if not self.text or not self.widget_exists():
            return
        try:
            self._after_id = self.widget.after(self.delay_ms, self.show_tip)
        except Exception:
            pass

    def on_leave(self, _event=None) -> None:
        self.cancel_timer()
        self.hide_tip()

    def on_destroy(self, _event=None) -> None:
        self.cancel_timer()
        self.hide_tip()

    def cancel_timer(self) -> None:
        if self._after_id and self.widget_exists():
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
        self._after_id = None

    def widget_exists(self) -> bool:
        try:
            return bool(self.widget and self.widget.winfo_exists())
        except Exception:
            return False

    def show_tip(self) -> None:
        self._after_id = None
        if self.tip_window or not self.text or not self.widget_exists():
            return
        try:
            x = self.widget.winfo_rootx() + 8
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(
                tw,
                text=self.text,
                justify="left",
                background="#201a33",
                foreground="#ffffff",
                relief="solid",
                borderwidth=1,
                font=("Segoe UI", 8),
                padx=6,
                pady=3,
            )
            label.pack(ipadx=1)
            self._label = label
        except Exception:
            self.hide_tip()

    def hide_tip(self, _event=None) -> None:
        self._label = None
        if self.tip_window:
            try:
                if self.tip_window.winfo_exists():
                    self.tip_window.destroy()
            except Exception:
                pass
            self.tip_window = None
```

### 2.3 `create_tooltip` function — `misora.py:298–300`

```python
# misora.py:298-300
def create_tooltip(widget: tk.Widget, text: str, delay_ms: int = 350) -> ToolTip:
    """Convenience helper to attach a hover tooltip to a widget."""
    return ToolTip(widget, text, delay_ms=delay_ms)
```

### 2.4 Existing `_get_monitor_work_area` (`misora.py:7043–7078`) & Speaker Popup Usage (`misora.py:7102–7116`)

`MisoraApp._get_monitor_work_area(self, x: int, y: int)` (`misora.py:7043–7078`) uses `MonitorFromPoint(..., 2)` (`MONITOR_DEFAULTTONEAREST`) and `GetMonitorInfoW(..., byref(mi))` (`mi.rcWork`), falling back to `(0, 0, winfo_screenwidth(), winfo_screenheight())`. Its only caller is `MisoraApp._refresh_speaker_autocomplete()` (`misora.py:7109–7112`), which clamps the speaker dropdown to `[work_left, work_right - w]` and `[work_top, work_bottom - h]`.

### 2.5 DPI Awareness — `misora.py:620–642` (READ-ONLY — NEVER MODIFY)

`init_process_dpi_awareness()` runs once before Tk root creation. Per `AGENTS.md` §7, DPI awareness MUST NOT be mutated at runtime. The fix only reads monitor work-area geometry and never calls any `SetProcessDpi*` APIs.

### 2.6 `S11e` & `T-02` Tooltip Test Compatibility Verification

Read-only inspection of `tests/test_v15_s11e_polish_splash_menu_tooltips.py` and `tests/test_t02_next_tooltip.py`:
- `tests/test_v15_s11e_polish_splash_menu_tooltips.py` inspects `w._tooltip`, `w._tooltip.text`, and `w._tooltip.delay_ms` (`L535`, `L537`, `L618–L685`). It never mocks `tk.Toplevel`, `withdraw`, `deiconify`, or `update_idletasks` globally or on `ToolTip`, and never invokes `ToolTip.show_tip()` (`withdraw`/`update_idletasks` in `S11e` are called only on `self.app`, `app2`, `app3`, `app_g`, `dlg`, and `dlg_fb`).
- `tests/test_t02_next_tooltip.py` only inspects `self.app.lbl_char_overflow._tooltip.text`, `self.app.btn_next._tooltip.text`, and `self.app.btn_prev._tooltip.text` (`L41`, `L78`, `L84`).
- Therefore, calling `tw.withdraw()` → `tw.update_idletasks()` → `tw.wm_geometry(...)` → `tw.deiconify()` on `ToolTip.tip_window` inside `ToolTip.show_tip()` introduces **zero conflict** with either suite.

---

## 3. Root-Cause Analysis & Read-Only Probes

### 3.1 Source-Level Root Cause — `SOURCE-OBSERVED`

`ToolTip.show_tip()` (`misora.py:260–285`) has three defects:
1. **No screen/work-area clamping (`L265–266, L269`):** Sets `x = self.widget.winfo_rootx() + 8` and `y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4`, applying `tw.wm_geometry(f"+{x}+{y}")` unchecked against any monitor boundary.
2. **Dimensions unmeasured before positioning (`L269` before `L270–282`):** `wm_geometry()` is called before `tk.Label` is constructed and packed, so `tw.winfo_reqwidth()` and `tw.winfo_reqheight()` are unknown at positioning time.
3. **No monitor work-area query:** `ToolTip` is a standalone top-level class (`L202`) without access to `MisoraApp._get_monitor_work_area` (`L7043`).

### 3.2 Read-Only Runtime Probe Output (Genuine `MisoraApp` + Windows Tk 8.6)

**Probe 1 — Genuine `MisoraApp` (`CONFIG_PATH` patched to temp dir, `restore_session=False, show_splash=False`):**
```
=== ToolTip text: 'Native 54d x 3 dialogue rule: <= 54 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines).\nLine widths measured'
=== Widget: .!panedwindow.!frame2.!panedwindow.!frame.!frame.!label3
=== Screen: 1920x1080
=== Monitor work area: left=0, top=0, right=1920, bottom=1050
=== Tooltip reqwidth=702, reqheight=34
=== SIMULATION: Widget at x=1870, tooltip at x=1878, tip_w=702 -> right edge overflow = 660px
=== SIMULATION: Widget at y=1030, tooltip at y=1035, tip_h=34 -> bottom edge overflow = 19px
```

**Probe 2 — Windows Tk 8.6 Negative-Coordinate & `update_idletasks()` Behavior (`py -3.12 -B -c`):**
```
geom1: '76x23+-704+50'
x1: -704
y1: 50
geom2: '76x23+-1500+200'
x2: -1500
y2: 200
geom3: '76x23+100+-50'
x3: 100
y3: -50
```
**Probe 3 — Live `misora.ToolTip.show_tip()` Pre-Patch Reading Timing (`py -3.12 -B -c`):**
```
BEFORE update_idletasks: wm_geometry= '1x1+-92+74' winfo_x= 0 winfo_y= 0 reqw= 200
AFTER  update_idletasks: wm_geometry= '523x34+-92+74' winfo_x= -92 winfo_y= 74 reqw= 523
TOP-LEFT unclamped: wm_geometry= '523x34+-12+-6' winfo_x= -12 winfo_y= -6 reqw= 523 reqh= 34
```
**Deterministic assertion rule derived from Probes 2 & 3:**
- Windows Tk 8.6 preserves negative `wm_geometry(f"+{x}+{y}")` coordinates (both `+-704+50` and `+100+-50`) without single-monitor OS snapping.
- However, BEFORE `tw.update_idletasks()` is called on a newly created pre-patch `Toplevel`, `tw.winfo_x()` / `tw.winfo_y()` return `0, 0` and `tw.winfo_reqwidth()` returns default `200`.
- Calling `tip.tip_window.update_idletasks()` inside tests immediately after `tip.show_tip()` ensures `winfo_x()`, `winfo_y()`, `winfo_reqwidth()`, and `winfo_reqheight()` are 100% populated and deterministic in BOTH pre-patch and post-patch runs on single-monitor Windows machines.

### 3.3 Why `MisoraApp._get_monitor_work_area` (`misora.py:7043`) Is Left Untouched

`MisoraApp._get_monitor_work_area` (`misora.py:7043–7078`) already serves `MisoraApp._refresh_speaker_autocomplete()` (`misora.py:7109`) cleanly. Leaving `MisoraApp._get_monitor_work_area` untouched keeps the T-08a diff strictly scoped to lines `199–362` of `misora.py` with **zero regression risk** to speaker autocomplete (`misora.py:7043–7116`).

---

## 4. Minimal Root-Cause Fix Design

### 4.1 Standalone Helper `_get_work_area()` — Inserted Before `class ToolTip`

```python
def _get_work_area(x: int, y: int, fallback_widget: Optional[tk.Widget] = None) -> Tuple[int, int, int, int]:
    """Return (work_left, work_top, work_right, work_bottom) for the monitor containing (x, y).

    Uses Win32 MonitorFromPoint/GetMonitorInfoW on Windows for accurate multi-monitor
    work-area bounds (excluding taskbar). Falls back to Tk screen dimensions on
    non-Windows platforms or on error. ZERO changes to DPI awareness (Rule 23).
    """
    if sys.platform == "win32":
        try:
            from ctypes import wintypes as _wt

            class _RECT(ctypes.Structure):
                _fields_ = [
                    ("left", ctypes.c_long),
                    ("top", ctypes.c_long),
                    ("right", ctypes.c_long),
                    ("bottom", ctypes.c_long),
                ]

            class _MONITORINFO(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.c_ulong),
                    ("rcMonitor", _RECT),
                    ("rcWork", _RECT),
                    ("dwFlags", ctypes.c_ulong),
                ]

            pt = _wt.POINT(int(x), int(y))
            hmon = ctypes.windll.user32.MonitorFromPoint(pt, 2)  # MONITOR_DEFAULTTONEAREST
            if hmon:
                mi = _MONITORINFO()
                mi.cbSize = ctypes.sizeof(_MONITORINFO)
                if ctypes.windll.user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
                    r = mi.rcWork
                    return (int(r.left), int(r.top), int(r.right), int(r.bottom))
        except Exception:
            pass
    try:
        if fallback_widget is not None:
            sw = int(fallback_widget.winfo_screenwidth() or 1920)
            sh = int(fallback_widget.winfo_screenheight() or 1080)
            return (0, 0, sw, sh)
    except Exception:
        pass
    return (0, 0, 1920, 1080)
```

### 4.2 Modified `ToolTip.show_tip()` — Full 4-Edge Clamping & Bottom Flip

```python
    def show_tip(self) -> None:
        self._after_id = None
        if self.tip_window or not self.text or not self.widget_exists():
            return
        try:
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.withdraw()
            label = tk.Label(
                tw,
                text=self.text,
                justify="left",
                background="#201a33",
                foreground="#ffffff",
                relief="solid",
                borderwidth=1,
                font=("Segoe UI", 8),
                padx=6,
                pady=3,
            )
            label.pack(ipadx=1)
            self._label = label

            tw.update_idletasks()
            tip_w = tw.winfo_reqwidth()
            tip_h = tw.winfo_reqheight()

            widget_x = self.widget.winfo_rootx()
            widget_y = self.widget.winfo_rooty()
            widget_h = self.widget.winfo_height()

            margin = 2
            work_left, work_top, work_right, work_bottom = _get_work_area(
                widget_x, widget_y, fallback_widget=self.widget
            )

            x = widget_x + 8
            y = widget_y + widget_h + 4

            if x + tip_w > work_right - margin:
                x = work_right - tip_w - margin
            if x < work_left + margin:
                x = work_left + margin
            if y + tip_h > work_bottom - margin:
                y = widget_y - tip_h - 4
            if y + tip_h > work_bottom - margin:
                y = work_bottom - tip_h - margin
            if y < work_top + margin:
                y = work_top + margin

            tw.wm_geometry(f"+{x}+{y}")
            tw.deiconify()
        except Exception:
            self.hide_tip()
```

### 4.3 Edge-Case Coverage

- **Right overflow:** Clamped to `work_right - tip_w - margin`.
- **Left overflow (or tooltip wider than monitor):** Clamped to `work_left + margin` (works identically for negative `work_left` such as `-1920`).
- **Bottom overflow:** Flips above widget (`widget_y - tip_h - 4`); if widget is below `work_bottom` so flipped `y` still overflows bottom, clamped to `work_bottom - tip_h - margin`; then if `y < work_top + margin` (short screen or widget above top edge), clamped to `work_top + margin`.
- **Top overflow:** Clamped to `work_top + margin` even when no bottom overflow occurred (e.g., `widget_y = -20`).
- **Preserved contracts:** `setattr(self.widget, "_tooltip", self)`, `delay_ms = 350`, `set_text()`, `hide_tip()`, and label styling/text remain untouched.

---

## 5. Exact Unified Diff & Exact `V-1` / `V-2` / `C-5` Verification Gates

Generated directly against `misora.py` at `9fa266375caf0994e49c9ed5ce8b7b1203b28f3c` and pre-validated with `git -C D:\Misora-Editor apply --check` (`exit 0`).

```diff
--- a/misora.py
+++ b/misora.py
@@ -199,6 +199,53 @@
 __version__ = _get_app_version()
 
 
+def _get_work_area(x: int, y: int, fallback_widget: Optional[tk.Widget] = None) -> Tuple[int, int, int, int]:
+    """Return (work_left, work_top, work_right, work_bottom) for the monitor containing (x, y).
+
+    Uses Win32 MonitorFromPoint/GetMonitorInfoW on Windows for accurate multi-monitor
+    work-area bounds (excluding taskbar). Falls back to Tk screen dimensions on
+    non-Windows platforms or on error. ZERO changes to DPI awareness (Rule 23).
+    """
+    if sys.platform == "win32":
+        try:
+            from ctypes import wintypes as _wt
+
+            class _RECT(ctypes.Structure):
+                _fields_ = [
+                    ("left", ctypes.c_long),
+                    ("top", ctypes.c_long),
+                    ("right", ctypes.c_long),
+                    ("bottom", ctypes.c_long),
+                ]
+
+            class _MONITORINFO(ctypes.Structure):
+                _fields_ = [
+                    ("cbSize", ctypes.c_ulong),
+                    ("rcMonitor", _RECT),
+                    ("rcWork", _RECT),
+                    ("dwFlags", ctypes.c_ulong),
+                ]
+
+            pt = _wt.POINT(int(x), int(y))
+            hmon = ctypes.windll.user32.MonitorFromPoint(pt, 2)  # MONITOR_DEFAULTTONEAREST
+            if hmon:
+                mi = _MONITORINFO()
+                mi.cbSize = ctypes.sizeof(_MONITORINFO)
+                if ctypes.windll.user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
+                    r = mi.rcWork
+                    return (int(r.left), int(r.top), int(r.right), int(r.bottom))
+        except Exception:
+            pass
+    try:
+        if fallback_widget is not None:
+            sw = int(fallback_widget.winfo_screenwidth() or 1920)
+            sh = int(fallback_widget.winfo_screenheight() or 1080)
+            return (0, 0, sw, sh)
+    except Exception:
+        pass
+    return (0, 0, 1920, 1080)
+
+
 class ToolTip:
     """Robust hover tooltip for Tkinter widgets with delayed display and safe lifecycle (Part C.5 / TOOLTIP-LIFECYCLE)."""
 
@@ -262,11 +309,9 @@
         if self.tip_window or not self.text or not self.widget_exists():
             return
         try:
-            x = self.widget.winfo_rootx() + 8
-            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
             self.tip_window = tw = tk.Toplevel(self.widget)
             tw.wm_overrideredirect(True)
-            tw.wm_geometry(f"+{x}+{y}")
+            tw.withdraw()
             label = tk.Label(
                 tw,
                 text=self.text,
@@ -281,6 +326,36 @@
             )
             label.pack(ipadx=1)
             self._label = label
+
+            tw.update_idletasks()
+            tip_w = tw.winfo_reqwidth()
+            tip_h = tw.winfo_reqheight()
+
+            widget_x = self.widget.winfo_rootx()
+            widget_y = self.widget.winfo_rooty()
+            widget_h = self.widget.winfo_height()
+
+            margin = 2
+            work_left, work_top, work_right, work_bottom = _get_work_area(
+                widget_x, widget_y, fallback_widget=self.widget
+            )
+
+            x = widget_x + 8
+            y = widget_y + widget_h + 4
+
+            if x + tip_w > work_right - margin:
+                x = work_right - tip_w - margin
+            if x < work_left + margin:
+                x = work_left + margin
+            if y + tip_h > work_bottom - margin:
+                y = widget_y - tip_h - 4
+            if y + tip_h > work_bottom - margin:
+                y = work_bottom - tip_h - margin
+            if y < work_top + margin:
+                y = work_top + margin
+
+            tw.wm_geometry(f"+{x}+{y}")
+            tw.deiconify()
         except Exception:
             self.hide_tip()
 
```

### Exact Line-Count & Diff Math:
- Pre-edit `misora.py`: `23,912` logical lines (`23,911` CRLF terminators, `bare_LF == 0`, `bare_CR == 0`)
- Added lines: `+78` (`+47` for `_get_work_area` + 2 blank lines; `+1` `tw.withdraw()`; `+30` measurement + 4-edge clamping + `deiconify()`)
- Deleted lines: `-3` (old `x = ...`, `y = ...`, `tw.wm_geometry(...)`)
- Net delta: `+75` lines
- Exact post-edit `misora.py`: **`23,987` logical lines** (`23,986` CRLF terminators, `bare_LF == 0`, `bare_CR == 0`)
- Exact `git diff HEAD --numstat -- misora.py`: **`78	3	misora.py`**

### Exact Verification Gates:
- **Pre-apply (`V-1`):** `git -C D:\Misora-Editor apply --check <patch_file>` → `exit 0` (already verified in Rev 2 planning)
- **Post-edit (`V-1` / whitespace):** `git -C D:\Misora-Editor diff HEAD --check` → `exit 0` (empty output)
- **Post-edit (`V-2` / numstat):** `git -C D:\Misora-Editor diff HEAD --numstat -- misora.py` → `78	3	misora.py`
- **Post-edit (`C-5` / EOL):** `splitlines(True) == 23,987`, `CRLF == 23,986`, `bare_LF == 0`, `bare_CR == 0`

---

## 6. Strict File Ownership Matrix (T-08a Execution Charter)

### Allowed ONLY after explicit Project Lead `Proceed`:

| File | Scope | Notes |
|---|---|---|
| `misora.py` | Add `_get_work_area()` before `ToolTip`; update `ToolTip.show_tip()` ONLY | `78	3	misora.py`; `23,987` logical lines |
| `tests/test_t08a_tooltip_clamping.py` | **NEW** — stdlib `unittest` (`8` tests: `5` Probes + `3` Guards) | Zero `pytest`, zero `.unity3d`, zero `skipTest()`, `CONFIG_PATH` & `messagebox` patched to temp dir, clean `app.destroy()` + `shutil.rmtree` |
| `docs/project/OPEN_ISSUES.md` | T-08a row ONLY | Record automated TDD `502` baseline / `8/8 PASS`; Windows QA `M-1..M-6` stays `MANUAL-PENDING`; Lifecycle stays `ACTIVE`; N-4 `--check` note |
| `PROJECT_STATE.md` | Test count & T-08a section ONLY | Exact `502 = 459 PASS + 35 SKIP + 6 FAIL + 2 ERROR`, N-4 transient `--check` note, stay `<= 15,360` bytes |

### Strictly FORBIDDEN / READ-ONLY:

`__init__.py`, `core/**`, `assets/**`, all existing `tests/*.py`, `AGENTS.md`, `docs/archive/**`, `tools/generate_symbol_index.py`, `docs/architecture/MISORA_SYMBOL_INDEX.md` (deferred to Project Lead post-commit regeneration), `misora.bat`, `requirements.txt`, `misora_config.json`, `backups/**`, `README.md`.

---

## 7. Zero-`.pyc` Windows-Safe TDD Verification Plan

### 7.1 Test File Design: `tests/test_t08a_tooltip_clamping.py` (`8` tests total)

**Pre-patch `AttributeError` Prevention & Deterministic Coordinate Reading:**
- Every Probe (`test_probe_1..test_probe_5`) and `test_guard_1` mocks `misora._get_work_area` using **`mock.patch.object(misora, "_get_work_area", create=True, ...)`** (or `unittest.mock.patch("misora._get_work_area", ..., create=True)`). Because `create=True` is mandatory, running the test file pre-patch when `misora._get_work_area` does not yet exist will **NEVER** raise `AttributeError`, guaranteeing `FAILED (failures=5)` with **`0 errors`**.
- Immediately after calling `tip.show_tip()`, every test calls **`tip.tip_window.update_idletasks()`** before reading `tip_w = tip.tip_window.winfo_reqwidth()`, `tip_h = tip.tip_window.winfo_reqheight()`, `x = tip.tip_window.winfo_x()`, and `y = tip.tip_window.winfo_y()` (verified in §3.2 Probe 3).

**7.1.1 Defect Probes (`5` tests — MUST FAIL pre-patch with `0` errors, PASS post-patch):**

| ID | Setup (on genuine `MisoraApp.lbl_char_overflow._tooltip`) | Assertions | Pre-patch | Post-patch |
|---|---|---|---|---|
| `test_probe_1_right_edge_clamp` | `_get_work_area -> (0, 0, 1920, 1050)`, `winfo_rootx -> 1800`, `winfo_rooty -> 100`, `winfo_height -> 20` | `x + tip_w <= 1918` and `x >= 2` | FAIL | PASS |
| `test_probe_2_bottom_edge_flip` | `_get_work_area -> (0, 0, 1920, 1050)`, `winfo_rootx -> 200`, `winfo_rooty -> 1020`, `winfo_height -> 25` | `y < 1020` (flipped above widget) and `y + tip_h <= 1048` and `y >= 2` | FAIL | PASS |
| `test_probe_3_left_edge_clamp` | `_get_work_area -> (0, 0, 1920, 1050)`, `winfo_rootx -> -20`, `winfo_rooty -> 200`, `winfo_height -> 20` | `x >= 2` | FAIL | PASS |
| `test_probe_4_top_edge_clamp` | `_get_work_area -> (0, 0, 1920, 1050)`, `winfo_rootx -> 200`, `winfo_rooty -> -20`, `winfo_height -> 10` | `y >= 2` and `y + tip_h <= 1048` | FAIL | PASS |
| `test_probe_5_multi_monitor_negative` | `_get_work_area -> (-1920, 0, 0, 1050)`, `winfo_rootx -> -100`, `winfo_rooty -> 100`, `winfo_height -> 20` | `x >= -1918`, `x + tip_w <= -2`, and `x < 0` (stays inside left secondary monitor; never jumps to `0`) | FAIL | PASS |

**7.1.2 Regression Guards (`3` tests — MUST PASS both pre-patch AND post-patch; N-3 Guard Re-Label Rule):**

| ID | Setup | Assertions | Pre | Post |
|---|---|---|---|---|
| `test_guard_1_center_screen_standard_position` | `_get_work_area(create=True) -> (0, 0, 1920, 1050)`, `winfo_rootx -> 500`, `winfo_rooty -> 300`, `winfo_height -> 22` | `x == 508` and `y == 326` (`widget_y + widget_h + 4`) | PASS | PASS |
| `test_guard_2_tooltip_text_preserved` | Inspect `self.app.lbl_char_overflow._tooltip.text` | Contains `"54"`, `"digit-widths"`, `"active editor font"`, `"fixed reference boundary"` | PASS | PASS |
| `test_guard_3_hide_tip_destroys_cleanly` | Call `show_tip()`, verify `tip_window` exists (`winfo_exists()`), call `hide_tip()` | `tip_window is None` and no `TclError` | PASS | PASS |

### 7.2 Broad BOM-Safe In-Memory Compile Check & Zero-`.pyc` Guard

```python
bom = bytes([239, 187, 191])
for py_file in (
    repo / "__init__.py",
    repo / "misora.py",
    *sorted((repo / "core").glob("*.py")),
    *sorted((repo / "assets").glob("*.py")),
    *sorted((repo / "tests").glob("*.py")),
):
    raw = py_file.read_bytes()
    src = raw.removeprefix(bom).decode("utf-8")
    compile(src, str(py_file), "exec")  # NO compileall, NO .pyc written
```
Plus verify `pre_pyc_count == post_pyc_count` across `D:\Misora-Editor`.

### 7.3 Exact Locked Discovery & Execution Arithmetic (`N = 8`, `P = 5`)

| Phase | Total | PASS | SKIP | FAIL | ERROR |
|---|---:|---:|---:|---:|---:|
| Baseline (`9fa26637`) | `494` | `451` | `35` | `6` | `2` |
| Pre-patch `tests/test_t08a_tooltip_clamping.py` | `8` | `3` | `0` | `5` | `0` |
| Post-patch `tests/test_t08a_tooltip_clamping.py` | `8` | `8` | `0` | `0` | `0` |
| Post-patch `tests/test_t02_next_tooltip.py` | `8` | `8` | `0` | `0` | `0` |
| Post-patch `tests/test_v15_s11e_polish_splash_menu_tooltips.py` | `9` | `9` | `0` | `0` | `0` |
| **Post-patch full `discover -s tests -v`** | **`502`** | **`459`** | **`35`** | **`6`** | **`2`** |

- Any discovery count other than `502` (`494 + 8`) is a hard **STOP**.
- Pre-patch T-08a run MUST report **`Ran 8 tests ... FAILED (failures=5)`** with **`0 errors`**.
- Post-patch full suite MUST report exact **`502 = 459 PASS + 35 SKIP + 6 FAIL + 2 ERROR`** (`+8 PASS`, `0` new failures/errors/skips).

---

## 8. Complete 4-File Rollback Steps

Pinned to exact `POST_DOCS01_HEAD = 9fa266375caf0994e49c9ed5ce8b7b1203b28f3c`. NEVER use `git reset --hard`, `git clean`, or blanket `git checkout`.

```powershell
cd D:\Misora-Editor
git checkout 9fa266375caf0994e49c9ed5ce8b7b1203b28f3c -- misora.py
git checkout 9fa266375caf0994e49c9ed5ce8b7b1203b28f3c -- docs/project/OPEN_ISSUES.md
git checkout 9fa266375caf0994e49c9ed5ce8b7b1203b28f3c -- PROJECT_STATE.md
Remove-Item -Path tests\test_t08a_tooltip_clamping.py -ErrorAction SilentlyContinue

git status --short --untracked-files=all
# Expected: (empty)
py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"
# Expected: countTestCases: 494
py -3.12 -B -c "data=open('misora.py','rb').read(); print('lines:', len(data.decode('utf-8').splitlines()), 'crlf:', data.count(bytes([13,10])))"
# Expected: lines: 23912 crlf: 23911
```

---

## 9. Manual Windows QA Checklist (`M-1..M-6`) — `MANUAL-PENDING`

| ID | Test | DPI | Window State | Expected | Status |
|---|---|---|---|---|---|
| **M-1** | Hover `lbl_char_overflow` with maximized window at `1920x1080` | `100%` | Maximized | Tooltip fully visible, clamped inside right screen edge | `MANUAL-PENDING` |
| **M-2** | Same as M-1 | `125%` | Maximized | Tooltip fully visible, clamped inside right screen edge | `MANUAL-PENDING` |
| **M-3** | Hover bottom-bar widget (e.g., Save/Revert) near screen bottom | `100%` | Maximized | Tooltip flips above widget, fully visible | `MANUAL-PENDING` |
| **M-4** | Hover widget near left/top edge of screen | `100%` | Windowed | Tooltip clamped inside left/top work-area bounds, not clipped | `MANUAL-PENDING` |
| **M-5** | Multi-monitor: hover tooltip-bearing widget on secondary monitor (if available) | Any | Any | Tooltip stays within secondary monitor bounds, never jumps to primary | `MANUAL-PENDING` |
| **M-6** | Operator sign-off | — | — | M-1..M-5 pass, zero visual regressions in tooltip appearance/timing | `MANUAL-PENDING` |

---

## 10. N-4 Transient `--check` Note

Adding module-level `_get_work_area()` to `misora.py` makes `docs/architecture/MISORA_SYMBOL_INDEX.md` transiently stale (`tools/generate_symbol_index.py --check` exits non-zero until regenerated). Per Charter §6, do NOT modify `tools/generate_symbol_index.py` or `docs/architecture/MISORA_SYMBOL_INDEX.md`; regeneration is deferred to the Project Lead post-commit.

---

## 11. Plan Verification (Live Verified at Rev 2 Write)

| Check | Result |
|---|---|
| `git -C D:\Misora-Editor status --short --untracked-files=all` | **Empty (0 modified, 0 untracked)** — verified after writing Rev 2 |
| `git -C D:\Misora-Editor apply --check t08a.patch` | **`exit 0`** (provisional patch applies cleanly to `misora.py` @ `9fa26637`) |
| Written path | `D:\Reference\Misora-Reference\T-08a_Implementation_Plan.md` |
| SHA-256 | Reported in final response (computed immediately after writing this file) |

---

**STOP — WAITING FOR INDEPENDENT REVIEW**
