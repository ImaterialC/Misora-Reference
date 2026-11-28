# T-08a Implementation Plan (Rev 3) — `BUG-UI-TOOLTIP-CLIP-01` ToolTip Screen-Edge Clipping

**Task:** T-08a (split from T-08/`BUG-39`/`FEAT-04`)
**Revision:** Rev 3 (addresses GPT-6 blockers W1 & W2, design notes W3, and Qwen execution notes E-1..E-4; Qwen CLEARED on Rev 2)
**Evidence:** `CONFIRMED` + `ROOT-CAUSE: SOURCE-OBSERVED`
**Lifecycle:** `ACTIVE`
**Version:** `1.4.15` (UNCHANGED — no version promotion authorized)
**Branch:** `main`

> [!IMPORTANT]
> This plan is **READ-ONLY** and authorizes **ZERO file modifications** inside `D:\Misora-Editor`.
> Implementation requires final clearance and explicit Project Lead `Proceed`.

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

### 2.1 Module-Level Imports & Windows `ctypes` Prototype Verification (Read-Only)

| Symbol | Exact `file:line` | Scope | Notes |
|---|---|---|---|
| `ctypes` | `misora.py:15` | Unconditional module scope | `import ctypes` |
| `sys` | `misora.py:24` | Unconditional module scope | `import sys` |
| `Optional`, `Tuple` | `misora.py:33` | Unconditional module scope | `from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, Union` |
| `wintypes` | `misora.py:42-44` | **Conditional** (`if sys.platform == "win32":`) | `from ctypes import wintypes` |

Because `wintypes` at `misora.py:44` is conditionally imported inside `if sys.platform == "win32":`, `_get_work_area()` explicitly performs `from ctypes import wintypes as _wt` inside `if sys.platform == "win32":`. Live Windows Python 3.12 probe verified:
- `hasattr(wintypes, "HMONITOR") == True`, `HANDLE == True`, `POINT == True`, `DWORD == True`, `BOOL == True`.
- `ctypes.WinDLL("user32", use_last_error=True)` returns a dedicated `WinDLL` instance (`user32 is ctypes.windll.user32 == False`), so setting explicit `argtypes`/`restype` inside `_get_work_area()` never mutates the shared `ctypes.windll.user32` object used elsewhere in `misora.py`.
- `MonitorFromPoint(POINT(100, 100), 2)` returned `65719` and `GetMonitorInfoW(hmon, byref(mi))` returned `1` with `rcWork = (0, 0, 1920, 1050)`.

### 2.2 Complete `ToolTip` class (`misora.py:202–295`) & `create_tooltip` (`misora.py:298–300`)

```python
# misora.py:202-300  (verbatim at 9fa26637)
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


def create_tooltip(widget: tk.Widget, text: str, delay_ms: int = 350) -> ToolTip:
    """Convenience helper to attach a hover tooltip to a widget."""
    return ToolTip(widget, text, delay_ms=delay_ms)
```

### 2.3 Existing `_get_monitor_work_area` (`misora.py:7043–7078`) & DPI Awareness (`misora.py:620–642`)

- `MisoraApp._get_monitor_work_area(self, x: int, y: int)` (`misora.py:7043–7078`) serves `MisoraApp._refresh_speaker_autocomplete()` (`misora.py:7109–7112`).
- `init_process_dpi_awareness()` (`misora.py:620–642`) runs once before Tk root creation. Per `AGENTS.md` §7, DPI awareness MUST NOT be mutated at runtime.

### 2.4 `S11e` & `T-02` Tooltip Test Compatibility Verification

- `tests/test_v15_s11e_polish_splash_menu_tooltips.py` inspects `w._tooltip`, `w._tooltip.text`, and `w._tooltip.delay_ms` (`L535`, `L537`, `L618–L685`). It never mocks `tk.Toplevel`, `withdraw`, `deiconify`, or `update_idletasks` globally or on `ToolTip`, and never invokes `ToolTip.show_tip()`.
- `tests/test_t02_next_tooltip.py` only inspects `lbl_char_overflow._tooltip.text`, `btn_next._tooltip.text`, and `btn_prev._tooltip.text` (`L41`, `L78`, `L84`).
- Zero conflict with either suite.

---

## 3. Root-Cause Analysis & Read-Only Probes

### 3.1 Source-Level Root Cause — `SOURCE-OBSERVED`

`ToolTip.show_tip()` (`misora.py:260–285`) has three defects:
1. **No screen/work-area clamping (`L265–266, L269`):** Sets `x = self.widget.winfo_rootx() + 8` and `y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4`, applying `tw.wm_geometry(f"+{x}+{y}")` unchecked against monitor bounds.
2. **Dimensions unmeasured before positioning (`L269` before `L270–282`):** `wm_geometry()` is called before `tk.Label` is constructed and packed.
3. **No monitor work-area query:** `ToolTip` is a standalone class (`L202`) without access to `MisoraApp._get_monitor_work_area` (`L7043`).

### 3.2 Read-Only Runtime Probe Output (Genuine `MisoraApp` + Windows Tk 8.6)

**Probe 1 — Genuine `MisoraApp` (`CONFIG_PATH` patched to temp dir, `restore_session=False, show_splash=False`):**
```
=== ToolTip text: 'Native 54d x 3 dialogue rule: <= 54 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines).\nLine widths measured'
=== Monitor work area: left=0, top=0, right=1920, bottom=1050
=== Tooltip reqwidth=702, reqheight=34
=== SIMULATION: Widget at x=1870, tooltip at x=1878, tip_w=702 -> right edge overflow = 660px
=== SIMULATION: Widget at y=1030, tooltip at y=1035, tip_h=34 -> bottom edge overflow = 19px
```

**Probe 2 — Windows Tk 8.6 Negative-Coordinate & `update_idletasks()` Behavior (`py -3.12 -B -c`):**
```
geom1: '76x23+-704+50'  x1: -704  y1: 50
geom2: '76x23+-1500+200' x2: -1500 y2: 200
geom3: '76x23+100+-50'  x3: 100   y3: -50
```

**Probe 3 — Live `misora.ToolTip.show_tip()` Pre-Patch Reading Timing (`py -3.12 -B -c`):**
```
BEFORE update_idletasks: wm_geometry= '1x1+-92+74' winfo_x= 0 winfo_y= 0 reqw= 200
AFTER  update_idletasks: wm_geometry= '523x34+-92+74' winfo_x= -92 winfo_y= 74 reqw= 523
TOP-LEFT unclamped: wm_geometry= '523x34+-12+-6' winfo_x= -12 winfo_y= -6 reqw= 523 reqh= 34
```
Calling `tip.tip_window.update_idletasks()` inside tests immediately after `tip.show_tip()` makes `winfo_x()`, `winfo_y()`, `winfo_reqwidth()`, and `winfo_reqheight()` 100% deterministic in both pre-patch and post-patch runs, including negative multi-monitor coordinates on single-monitor machines.

### 3.3 Why `MisoraApp._get_monitor_work_area` (`misora.py:7043`) Is Left Untouched

`MisoraApp._get_monitor_work_area` (`misora.py:7043–7078`) already serves `MisoraApp._refresh_speaker_autocomplete()` (`misora.py:7109`). Leaving it untouched keeps the T-08a diff strictly scoped to lines `199–376` of `misora.py` with zero regression risk to speaker autocomplete.

---

## 4. Minimal Root-Cause Fix Design

### 4.1 Standalone Helper `_get_work_area()` — Explicit `ctypes` Prototypes & Clean Failure vs Fallback Distinction

```python
def _get_work_area(x: int, y: int, fallback_widget: Optional[tk.Widget] = None) -> Tuple[int, int, int, int]:
    """Return (work_left, work_top, work_right, work_bottom) for the monitor containing (x, y).

    Uses Win32 MonitorFromPoint/GetMonitorInfoW on Windows with explicit ctypes
    prototypes (use_last_error=True) for taskbar-excluded multi-monitor bounds.
    Falls back to Tk primary screen dimensions (not per-monitor/taskbar-excluded)
    when non-Windows, Win32 DLL is unavailable, or Win32 API returns failure.
    ZERO changes to DPI awareness (Rule 23).
    """
    if sys.platform == "win32":
        from ctypes import wintypes as _wt

        class _RECT(ctypes.Structure):
            _fields_ = [
                ("left", _wt.LONG),
                ("top", _wt.LONG),
                ("right", _wt.LONG),
                ("bottom", _wt.LONG),
            ]

        class _MONITORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", _wt.DWORD),
                ("rcMonitor", _RECT),
                ("rcWork", _RECT),
                ("dwFlags", _wt.DWORD),
            ]

        try:
            user32 = ctypes.WinDLL("user32", use_last_error=True)
        except OSError:
            user32 = None

        if user32 is not None:
            hmonitor_type = getattr(_wt, "HMONITOR", _wt.HANDLE)
            monitor_from_point = user32.MonitorFromPoint
            monitor_from_point.argtypes = [_wt.POINT, _wt.DWORD]
            monitor_from_point.restype = hmonitor_type

            get_monitor_info = user32.GetMonitorInfoW
            get_monitor_info.argtypes = [hmonitor_type, ctypes.POINTER(_MONITORINFO)]
            get_monitor_info.restype = _wt.BOOL

            pt = _wt.POINT(int(x), int(y))
            hmon = monitor_from_point(pt, 2)  # MONITOR_DEFAULTTONEAREST = 2
            if hmon:
                mi = _MONITORINFO()
                mi.cbSize = ctypes.sizeof(_MONITORINFO)
                if get_monitor_info(hmon, ctypes.byref(mi)):
                    r = mi.rcWork
                    return (int(r.left), int(r.top), int(r.right), int(r.bottom))
    try:
        if fallback_widget is not None:
            sw = int(fallback_widget.winfo_screenwidth() or 1920)
            sh = int(fallback_widget.winfo_screenheight() or 1080)
            return (0, 0, sw, sh)
    except (tk.TclError, ValueError, TypeError, AttributeError):
        pass
    return (0, 0, 1920, 1080)
```

**Win32 failure/unavailable vs signature-error distinction (GPT-6 W1):**
- Only `OSError` when loading `ctypes.WinDLL("user32", use_last_error=True)` (unavailable DLL) and falsy API returns (`hmon == 0` / `GetMonitorInfoW(...) == 0`) trigger fallback.
- There is **no** blanket `except Exception: pass` around prototype configuration or Win32 invocation, so `ctypes.ArgumentError`, `TypeError`, or `AttributeError` on `MonitorFromPoint`/`GetMonitorInfoW` are **never silently masked**.
- Tk fallback is narrowed to `(tk.TclError, ValueError, TypeError, AttributeError)`.

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

### 4.3 Explicit Edge-Case, Oversized-Tooltip, and Fallback Guarantees (GPT-6 W3)

- **All 4 edges enforced:** Right (`work_right - tip_w - margin`), Left (`work_left + margin`), Bottom (flip above widget, then post-flip clamp `work_bottom - tip_h - margin`), and Top (`work_top + margin`). Multi-monitor negative coordinates (e.g., `[-1920, 0)`) are handled symmetrically without clamping to `0`.
- **Oversized tooltips (`tip_w > (work_right - work_left) - 2 * margin`):** **Left-clamped** (`x = work_left + margin` runs after right-clamp) rather than dynamically adding `wraplength` + re-measurement, preserving the author's exact single-line / explicit-`\n` layout (`lbl_char_overflow` is `702px` wide, fitting 100%, 125%, and 150% DPI at `1920x1080` and `1366x768`).
- **Fallback honesty:** On non-Windows platforms or when Win32 `MonitorFromPoint`/`GetMonitorInfoW` returns failure or `WinDLL` raises `OSError`, the Tk fallback (`winfo_screenwidth()` / `winfo_screenheight()`, or `(0, 0, 1920, 1080)`) returns **primary screen dimensions only** — it is **not** full taskbar-excluded or multi-monitor work area. Only the Windows Win32 `MonitorFromPoint` + `GetMonitorInfoW` (`rcWork`) path provides per-monitor taskbar-excluded work area.
- **Preserved contracts:** `setattr(self.widget, "_tooltip", self)`, `delay_ms = 350`, `set_text()`, `hide_tip()`, and label styling/text remain untouched.

---

## 5. Exact Unified Diff & Exact `V-1` / `V-2` / `C-5` Verification Gates

Generated directly against `misora.py` at `9fa266375caf0994e49c9ed5ce8b7b1203b28f3c` and pre-validated with `git -C D:\Misora-Editor apply --check` (`exit 0`).

```diff
--- a/misora.py
+++ b/misora.py
@@ -199,6 +199,67 @@
 __version__ = _get_app_version()
 
 
+def _get_work_area(x: int, y: int, fallback_widget: Optional[tk.Widget] = None) -> Tuple[int, int, int, int]:
+    """Return (work_left, work_top, work_right, work_bottom) for the monitor containing (x, y).
+
+    Uses Win32 MonitorFromPoint/GetMonitorInfoW on Windows with explicit ctypes
+    prototypes (use_last_error=True) for taskbar-excluded multi-monitor bounds.
+    Falls back to Tk primary screen dimensions (not per-monitor/taskbar-excluded)
+    when non-Windows, Win32 DLL is unavailable, or Win32 API returns failure.
+    ZERO changes to DPI awareness (Rule 23).
+    """
+    if sys.platform == "win32":
+        from ctypes import wintypes as _wt
+
+        class _RECT(ctypes.Structure):
+            _fields_ = [
+                ("left", _wt.LONG),
+                ("top", _wt.LONG),
+                ("right", _wt.LONG),
+                ("bottom", _wt.LONG),
+            ]
+
+        class _MONITORINFO(ctypes.Structure):
+            _fields_ = [
+                ("cbSize", _wt.DWORD),
+                ("rcMonitor", _RECT),
+                ("rcWork", _RECT),
+                ("dwFlags", _wt.DWORD),
+            ]
+
+        try:
+            user32 = ctypes.WinDLL("user32", use_last_error=True)
+        except OSError:
+            user32 = None
+
+        if user32 is not None:
+            hmonitor_type = getattr(_wt, "HMONITOR", _wt.HANDLE)
+            monitor_from_point = user32.MonitorFromPoint
+            monitor_from_point.argtypes = [_wt.POINT, _wt.DWORD]
+            monitor_from_point.restype = hmonitor_type
+
+            get_monitor_info = user32.GetMonitorInfoW
+            get_monitor_info.argtypes = [hmonitor_type, ctypes.POINTER(_MONITORINFO)]
+            get_monitor_info.restype = _wt.BOOL
+
+            pt = _wt.POINT(int(x), int(y))
+            hmon = monitor_from_point(pt, 2)  # MONITOR_DEFAULTTONEAREST = 2
+            if hmon:
+                mi = _MONITORINFO()
+                mi.cbSize = ctypes.sizeof(_MONITORINFO)
+                if get_monitor_info(hmon, ctypes.byref(mi)):
+                    r = mi.rcWork
+                    return (int(r.left), int(r.top), int(r.right), int(r.bottom))
+    try:
+        if fallback_widget is not None:
+            sw = int(fallback_widget.winfo_screenwidth() or 1920)
+            sh = int(fallback_widget.winfo_screenheight() or 1080)
+            return (0, 0, sw, sh)
+    except (tk.TclError, ValueError, TypeError, AttributeError):
+        pass
+    return (0, 0, 1920, 1080)
+
+
 class ToolTip:
     """Robust hover tooltip for Tkinter widgets with delayed display and safe lifecycle (Part C.5 / TOOLTIP-LIFECYCLE)."""
 
@@ -262,11 +323,9 @@
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
@@ -281,6 +340,36 @@
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
- Added lines: `+92` (`+61` for `_get_work_area` + 2 blank lines; `+1` `tw.withdraw()`; `+30` measurement + 4-edge clamping + `deiconify()`)
- Deleted lines: `-3`
- Net delta: `+89` lines
- Exact post-edit `misora.py`: **`24,001` logical lines** (`24,000` CRLF terminators, `bare_LF == 0`, `bare_CR == 0`)
- Exact `git diff HEAD --numstat -- misora.py`: **`92	3	misora.py`**

### Exact Verification Gates:
- **Pre-apply (`V-1`):** `git -C D:\Misora-Editor apply --check <patch_file>` → `exit 0` (already verified in Rev 3 planning)
- **Post-edit (`V-1` / whitespace):** `git -C D:\Misora-Editor diff HEAD --check` → `exit 0` (empty output)
- **Post-edit (`V-2` / numstat):** `git -C D:\Misora-Editor diff HEAD --numstat -- misora.py` → `92	3	misora.py`
- **Post-edit (`C-5` / EOL):** `splitlines(True) == 24,001`, `CRLF == 24,000`, `bare_LF == 0`, `bare_CR == 0`

---

## 6. Strict File Ownership Matrix (T-08a Execution Charter)

### Allowed ONLY after explicit Project Lead `Proceed`:

| File | Scope | Notes |
|---|---|---|
| `misora.py` | Add `_get_work_area()` before `ToolTip`; update `ToolTip.show_tip()` ONLY | `92	3	misora.py`; `24,001` logical lines |
| `tests/test_t08a_tooltip_clamping.py` | **NEW** — stdlib `unittest` (`10` tests: `7` Probes + `3` Guards) | Zero `pytest`, zero `.unity3d`, zero `skipTest()`, `CONFIG_PATH` & `messagebox` patched to temp dir, clean `app.destroy()` + `shutil.rmtree` |
| `docs/project/OPEN_ISSUES.md` | T-08a row ONLY (Qwen E-1 preservation rule) | Update T-08a row to record `BUG-UI-TOOLTIP-CLIP-01` (`ToolTip.show_tip()` + `_get_work_area()`) automated TDD `10/10 PASS` (within `504 = 461 PASS + 35 SKIP + 6 FAIL + 2 ERROR`) and Windows QA `M-1..M-6` `MANUAL-PENDING`; **explicitly preserve the existing main-window off-screen report (`_deferred_restore()` / `sanitize_window_geometry` at 100% DPI) as an open sub-item/note inside the T-08a row**; keep Lifecycle `ACTIVE`; include N-4 transient `--check` note |
| `PROJECT_STATE.md` | Test count & T-08a section ONLY | Exact `504 = 461 PASS + 35 SKIP + 6 FAIL + 2 ERROR`, N-4 transient `--check` note, stay `<= 15,360` bytes |

### Strictly FORBIDDEN / READ-ONLY:

`__init__.py`, `core/**`, `assets/**`, all existing `tests/*.py`, `AGENTS.md`, `docs/archive/**`, `tools/generate_symbol_index.py`, `docs/architecture/MISORA_SYMBOL_INDEX.md` (deferred to Project Lead post-commit regeneration), `misora.bat`, `requirements.txt`, `misora_config.json`, `backups/**`, `README.md`.

---

## 7. Zero-`.pyc` Windows-Safe TDD Verification Plan

### 7.1 Test File Design: `tests/test_t08a_tooltip_clamping.py` (`10` tests total)

**Pre-patch `AttributeError` Prevention & Deterministic Coordinate Reading:**
- Probes 1–5 and Guard 1 mock `misora._get_work_area` using **`mock.patch.object(misora, "_get_work_area", create=True, ...)`** so pre-patch execution never raises `AttributeError`.
- Probes 6–7 test `misora._get_work_area` directly and obtain it via `fn = getattr(misora, "_get_work_area", None); self.assertIsNotNone(fn, "_get_work_area not implemented")` so pre-patch execution raises `AssertionError` (counted as `FAIL`, **0 errors**).
- Probes 1–5 and Guard 1 call **`tip.tip_window.update_idletasks()`** immediately after `tip.show_tip()` before reading `winfo_reqwidth()`, `winfo_reqheight()`, `winfo_x()`, and `winfo_y()`.

**7.1.1 Defect Probes (`7` tests — MUST FAIL pre-patch with `0` errors, PASS post-patch):**

| ID | Setup | Assertions | Pre-patch | Post-patch |
|---|---|---|---|---|
| `test_probe_1_right_edge_clamp` | `_get_work_area(create=True) -> (0, 0, 1920, 1050)`, `winfo_rootx -> 1800`, `winfo_rooty -> 100`, `winfo_height -> 20` | `x + tip_w <= 1918` and `x >= 2` | FAIL | PASS |
| `test_probe_2_bottom_edge_flip` | `_get_work_area(create=True) -> (0, 0, 1920, 1050)`, `winfo_rootx -> 200`, `winfo_rooty -> 1020`, `winfo_height -> 25` | `y < 1020`, `y + tip_h <= 1048`, `y >= 2` | FAIL | PASS |
| `test_probe_3_left_edge_clamp` | `_get_work_area(create=True) -> (0, 0, 1920, 1050)`, `winfo_rootx -> -20`, `winfo_rooty -> 200`, `winfo_height -> 20` | `x >= 2` | FAIL | PASS |
| `test_probe_4_top_edge_clamp` | `_get_work_area(create=True) -> (0, 0, 1920, 1050)`, `winfo_rootx -> 200`, `winfo_rooty -> -20`, `winfo_height -> 10` | `y >= 2` and `y + tip_h <= 1048` | FAIL | PASS |
| `test_probe_5_multi_monitor_negative` | `_get_work_area(create=True) -> (-1920, 0, 0, 1050)`, `winfo_rootx -> -100`, `winfo_rooty -> 100`, `winfo_height -> 20` | `x >= -1918`, `x + tip_w <= -2`, and `x < 0` | FAIL | PASS |
| `test_probe_6_work_area_win32_prototypes_and_negative_monitor` | `fn = getattr(misora, "_get_work_area", None)`; assert not None; mock `sys.platform == "win32"` and `ctypes.WinDLL("user32", use_last_error=True)` with fake `MonitorFromPoint` returning `0x1234` and `GetMonitorInfoW` setting `rcWork = (-1920, 0, 0, 1040)` | `WinDLL("user32", use_last_error=True)` called; explicit `argtypes`/`restype` set on both `MonitorFromPoint` (`[POINT, DWORD]` -> `HMONITOR/HANDLE`) and `GetMonitorInfoW` (`[hmonitor_type, POINTER(_MONITORINFO)]` -> `BOOL`); returns `(-1920, 0, 0, 1040)` | FAIL | PASS |
| `test_probe_7_work_area_fallback_on_win32_failure_and_non_win32` | `fn = getattr(misora, "_get_work_area", None)`; assert not None; mock `fallback_widget` (`winfo_screenwidth() -> 1280`, `winfo_screenheight() -> 720`); test: (a) `MonitorFromPoint` returns `0`, (b) `GetMonitorInfoW` returns `0`, (c) `WinDLL` raises `OSError`, (d) `sys.platform == "linux"` | All 4 cases return `(0, 0, 1280, 720)`; `fallback_widget=None` on `"linux"` returns `(0, 0, 1920, 1080)`; `TypeError`/`ArgumentError` is NOT swallowed when raised by Win32 call | FAIL | PASS |

**7.1.2 Regression Guards (`3` tests — MUST PASS both pre-patch AND post-patch; N-3 Guard Re-Label Rule):**

| ID | Setup | Assertions | Pre | Post |
|---|---|---|---|---|
| `test_guard_1_center_screen_standard_position` | `_get_work_area(create=True) -> (0, 0, 1920, 1050)`, `winfo_rootx -> 500`, `winfo_rooty -> 300`, `winfo_height -> 22` | `x == 508` and `y == 326` | PASS | PASS |
| `test_guard_2_tooltip_text_preserved` | Inspect `self.app.lbl_char_overflow._tooltip.text` | Contains `"54"`, `"digit-widths"`, `"active editor font"`, `"fixed reference boundary"` | PASS | PASS |
| `test_guard_3_hide_tip_destroys_cleanly` | Call `show_tip()`, verify `tip_window.winfo_exists()`, call `hide_tip()` | `tip_window is None` and no `TclError` | PASS | PASS |

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

### 7.3 Exact Locked Discovery & Execution Arithmetic (`N = 10`, `P = 7`)

| Phase | Total | PASS | SKIP | FAIL | ERROR |
|---|---:|---:|---:|---:|---:|
| Baseline (`9fa26637`) | `494` | `451` | `35` | `6` | `2` |
| Pre-patch `tests/test_t08a_tooltip_clamping.py` | `10` | `3` | `0` | `7` | `0` |
| Post-patch `tests/test_t08a_tooltip_clamping.py` | `10` | `10` | `0` | `0` | `0` |
| Post-patch `tests/test_t02_next_tooltip.py` | `8` | `8` | `0` | `0` | `0` |
| Post-patch `tests/test_v15_s11e_polish_splash_menu_tooltips.py` | `9` | `9` | `0` | `0` | `0` |
| **Post-patch full `discover -s tests -v`** | **`504`** | **`461`** | **`35`** | **`6`** | **`2`** |

- Any discovery count other than **`504`** (`494 + 10`) is a hard **STOP**.
- Pre-patch T-08a run MUST report **`Ran 10 tests ... FAILED (failures=7)`** with **`0 errors`**.
- Post-patch full suite MUST report exact **`504 = 461 PASS + 35 SKIP + 6 FAIL + 2 ERROR`** (`+10 PASS`, `0` new failures/errors/skips).

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
| **M-5** | Multi-monitor: hover tooltip-bearing widget on secondary monitor (**if only 1 monitor is present during QA, MUST be marked `NOT RUN` / `UNVERIFIED`, never `PASS`**) | Any | Any | Tooltip stays within secondary monitor bounds, never jumps to primary | `MANUAL-PENDING` |
| **M-6** | Operator sign-off | — | — | M-1..M-4 pass (and M-5 verified or explicitly `NOT RUN` on single-monitor setups), zero visual regressions | `MANUAL-PENDING` |

---

## 10. N-4 Transient `--check` Note

Adding module-level `_get_work_area()` to `misora.py` makes `docs/architecture/MISORA_SYMBOL_INDEX.md` transiently stale (`tools/generate_symbol_index.py --check` exits non-zero until regenerated). Per Charter §6, do NOT modify `tools/generate_symbol_index.py` or `docs/architecture/MISORA_SYMBOL_INDEX.md`; regeneration is deferred to the Project Lead post-commit.

---

## 11. Plan Verification (Live Verified at Rev 3 Write)

| Check | Result |
|---|---|
| `git -C D:\Misora-Editor status --short --untracked-files=all` | **Empty (0 modified, 0 untracked)** |
| `git -C D:\Misora-Editor apply --check t08a_rev3.patch` | **`exit 0`** (`92	3	misora.py`, `24,001` logical lines) |
| Written path | `D:\Reference\Misora-Reference\T-08a_Implementation_Plan.md` |
| SHA-256 | Reported in final response (computed immediately after writing this file) |

---

**STOP — WAITING FOR FINAL CLEARANCE**
