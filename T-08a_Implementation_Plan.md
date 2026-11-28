# T-08a Implementation Plan — `BUG-UI-TOOLTIP-CLIP-01` ToolTip Screen-Edge Clipping

**Task:** T-08a (split from T-08/`BUG-39`/`FEAT-04`)
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
| `git rev-parse --show-toplevel` | `D:/Misora-Editor` |
| `git branch --show-current` | `main` |
| `git rev-parse HEAD` | `9fa266375caf0994e49c9ed5ce8b7b1203b28f3c` (**POST_DOCS01_HEAD**) |
| `git status --short --untracked-files=all` | **(empty — clean tree)** |
| `py -3.12 -B -c "import __init__; print(__init__.__version__)"` | `1.4.15` |
| `py -3.12 -B tools/generate_symbol_index.py --check` | `CHECK PASS: docs/architecture/MISORA_SYMBOL_INDEX.md` |
| `py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"` | `countTestCases: 494` |
| `misora.py` logical lines (LF count) | `23911` |
| `misora.py` CRLF count | `23911` |
| `misora.py` bare LF | `0` |
| `misora.py` bare CR | `0` |
| `misora.py` total bytes | `1100212` |

**Prerequisite Gate — DOCS-01 COMMITTED:**
- AGENTS.md §7 line 40: `"Native overflow: 54 digit-widths or 3+ hard linebreaks (4+ lines)"` ✅
- OPEN_ISSUES.md line 32 contains `T-08a` (`BUG-UI-TOOLTIP-CLIP-01`) ✅
- HEAD `9fa26637` is commit `"DOCS-01: Close T-02 QA, sync ledgers & Option A roadmap, fix AGENTS.md §7 50->54 (docs-only, 0 .py)"` — post-DOCS-01 ✅

---

## 2. Verbatim ToolTip Source Audit

### 2.1 Complete `ToolTip` class — `misora.py:202–295`

```python
# misora.py:202-295  (verbatim, line numbers exact at 9fa26637)
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

    def show_tip(self) -> None:                               # LINE 260
        self._after_id = None
        if self.tip_window or not self.text or not self.widget_exists():
            return
        try:
            x = self.widget.winfo_rootx() + 8                 # LINE 265
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4  # LINE 266
            self.tip_window = tw = tk.Toplevel(self.widget)    # LINE 267
            tw.wm_overrideredirect(True)                       # LINE 268
            tw.wm_geometry(f"+{x}+{y}")                        # LINE 269  ← NO CLAMPING
            label = tk.Label(                                  # LINE 270
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
            label.pack(ipadx=1)                                # LINE 282
            self._label = label                                # LINE 283
        except Exception:
            self.hide_tip()

    def hide_tip(self, _event=None) -> None:                   # LINE 287
        self._label = None
        if self.tip_window:
            try:
                if self.tip_window.winfo_exists():
                    self.tip_window.destroy()
            except Exception:
                pass
            self.tip_window = None
```

### 2.2 `create_tooltip` function — `misora.py:298–300`

```python
# misora.py:298-300
def create_tooltip(widget: tk.Widget, text: str, delay_ms: int = 350) -> ToolTip:
    """Convenience helper to attach a hover tooltip to a widget."""
    return ToolTip(widget, text, delay_ms=delay_ms)
```

### 2.3 Existing `_get_monitor_work_area` — `misora.py:7043–7078` (MisoraApp method)

```python
# misora.py:7043-7078  (verbatim)
def _get_monitor_work_area(self, x: int, y: int) -> Tuple[int, int, int, int]:
    """Return (work_left, work_top, work_right, work_bottom) for the monitor containing (x, y)."""
    if sys.platform == "win32" and hasattr(ctypes, "windll"):
        try:
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

            pt = wintypes.POINT(int(x), int(y))
            hmon = ctypes.windll.user32.MonitorFromPoint(pt, 2)  # MONITOR_DEFAULTTONEAREST = 2
            if hmon:
                mi = _MONITORINFO()
                mi.cbSize = ctypes.sizeof(_MONITORINFO)
                if ctypes.windll.user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
                    r = mi.rcWork
                    return (int(r.left), int(r.top), int(r.right), int(r.bottom))
        except Exception:
            pass
    try:
        sw = int(self.winfo_screenwidth() or 1920)
        sh = int(self.winfo_screenheight() or 1080)
    except Exception:
        sw, sh = 1920, 1080
    return (0, 0, sw, sh)
```

### 2.4 Existing usage pattern — speaker autocomplete popup `misora.py:7102–7116`

```python
# misora.py:7102-7116  (verbatim — the existing clamp pattern)
        try:
            self.entry_speaker.update_idletasks()
            raw_x = int(self.entry_speaker.winfo_rootx())
            raw_y = int(self.entry_speaker.winfo_rooty() + self.entry_speaker.winfo_height() + 1)
            w = max(220, int(self.entry_speaker.winfo_width()))
            row_h = 20
            h = min(8, len(candidates)) * row_h + 6
            work_left, work_top, work_right, work_bottom = self._get_monitor_work_area(raw_x, raw_y)
            x = max(work_left, min(raw_x, work_right - w))
            y = max(work_top, min(raw_y, work_bottom - h))
            popup.geometry(f"{w}x{h}+{x}+{y}")
            popup.deiconify()
            popup.lift()
        except Exception:
            pass
```

### 2.5 DPI awareness — `misora.py:620–642` (READ-ONLY — NEVER MODIFY)

The `init_process_dpi_awareness()` function is called once at startup before Tk root creation. It sets `DPI_AWARENESS_CONTEXT_SYSTEM_AWARE` (-2) or falls back. **Rule 23: NEVER mutate DPI awareness at runtime.** The fix MUST NOT call any `SetProcessDpi*` functions.

---

## 3. Root-Cause Analysis

### 3.1 Source-Level Root Cause — `SOURCE-OBSERVED`

`ToolTip.show_tip()` (lines 260–285) has **three defects:**

1. **No screen-edge clamping.** Lines 265–266 compute `x = widget.winfo_rootx() + 8`, `y = widget.winfo_rooty() + widget.winfo_height() + 4` and line 269 applies `tw.wm_geometry(f"+{x}+{y}")` **without checking against monitor/work-area bounds**. If the trigger widget is near the right, bottom, or any edge of the screen, the tooltip window extends past the visible area.

2. **Tooltip dimensions unknown at positioning time.** Line 269 sets `wm_geometry` BEFORE line 282 packs the label content. At the time `wm_geometry` is called, `tw.winfo_reqwidth()` / `tw.winfo_reqheight()` are not yet meaningful because the label hasn't been packed. Even if clamping were added at line 269, the tooltip's actual dimensions would be unknown.

3. **No monitor work-area awareness.** `ToolTip` is a standalone class (not a `MisoraApp` method), so it has no access to `self._get_monitor_work_area()`. It uses `self.widget.winfo_rootx()` for position but never queries screen or work-area bounds.

### 3.2 Read-Only Runtime Probe Output

```
=== ToolTip text: 'Native 54d x 3 dialogue rule: <= 54 digit-widths without linebreak AND < 3 linebreaks (<= 3 lines).\nLine widths measured'
=== Widget: .!panedwindow.!frame2.!panedwindow.!frame.!frame.!label3
=== Widget class: Label
=== Widget rootx=0, rooty=0, width=1, height=1
=== ToolTip unclamped position: x=8, y=5
=== Screen: 1920x1080
=== Monitor work area: left=0, top=0, right=1920, bottom=1050
=== Tooltip reqwidth=702, reqheight=34
=== Right overflow: tip_x(8) + tip_w(702) = 710 vs work_right(1920) -> overflow=-1210
--- No right overflow in current window position (widget may not be near edge)
=== SIMULATION: Widget at x=1870, tooltip at x=1878, tip_w=702 -> right edge overflow = 660px
=== SIMULATION: Widget at y=1030, tooltip at y=1035, tip_h=34 -> bottom edge overflow = 19px
```

**Key findings:**
- The `lbl_char_overflow` tooltip is **702px wide** × **34px tall** (2-line text at Segoe UI 8pt).
- Monitor work area: `(0, 0, 1920, 1050)` — taskbar consumes bottom 30px.
- When the window is **maximized** and `lbl_char_overflow` is near the right edge of the ribbon, the tooltip's 702px width **overflows past the right screen edge by up to 660px** (simulated with widget at x=1870).
- Bottom overflow is also possible for bottom-bar widgets (Save, Revert, etc.) near `y=1050`.
- The actual visual symptom was `CONFIRMED` by the Project Lead on Windows 11 at 100% and 125% DPI with maximized window.

### 3.3 Why the fix is minimal and safe

- `ToolTip` is a **self-contained class** at lines 202–295 with **zero callers** besides `create_tooltip` (line 298) and direct `ToolTip(...)` construction.
- The fix touches ONLY `show_tip()` and adds one new module-level helper function.
- The existing `_get_monitor_work_area` on `MisoraApp` (line 7043) cannot be reused directly since `ToolTip` is not a method of `MisoraApp`. The fix extracts monitor work-area query into a standalone pure function `_get_work_area(x, y)` placed before the `ToolTip` class (helpers precede callers per AGENTS.md §3).
- **ZERO DPI awareness changes** (Rule 23). The fix only reads monitor geometry via `MonitorFromPoint` / `GetMonitorInfoW`, identical to the existing `_get_monitor_work_area` implementation.

---

## 4. Minimal Root-Cause Fix Design

### 4.1 New standalone helper: `_get_work_area(x, y)` — insert before `class ToolTip` (before line 202)

```python
def _get_work_area(x: int, y: int, fallback_widget: Optional[tk.Widget] = None) -> Tuple[int, int, int, int]:
    """Return (work_left, work_top, work_right, work_bottom) for the monitor containing (x, y).

    Uses Win32 MonitorFromPoint/GetMonitorInfoW on Windows for accurate multi-monitor
    work-area bounds (excluding taskbar). Falls back to Tk screen dimensions on
    non-Windows platforms or on error. ZERO changes to DPI awareness (Rule 23).
    """
    if sys.platform == "win32" and hasattr(ctypes, "windll"):
        try:
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

            pt = wintypes.POINT(int(x), int(y))
            hmon = ctypes.windll.user32.MonitorFromPoint(pt, 2)  # MONITOR_DEFAULTTONEAREST
            if hmon:
                mi = _MONITORINFO()
                mi.cbSize = ctypes.sizeof(_MONITORINFO)
                if ctypes.windll.user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
                    r = mi.rcWork
                    return (int(r.left), int(r.top), int(r.right), int(r.bottom))
        except Exception:
            pass
    # Tk fallback
    try:
        if fallback_widget is not None:
            sw = int(fallback_widget.winfo_screenwidth() or 1920)
            sh = int(fallback_widget.winfo_screenheight() or 1080)
            return (0, 0, sw, sh)
    except Exception:
        pass
    return (0, 0, 1920, 1080)
```

### 4.2 Modified `show_tip()` — replace lines 260–285

```python
    def show_tip(self) -> None:
        self._after_id = None
        if self.tip_window or not self.text or not self.widget_exists():
            return
        try:
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.withdraw()  # Prevent flicker: create hidden, measure, then position & show
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

            # Default position: below and to the right of trigger widget
            x = widget_x + 8
            y = widget_y + widget_h + 4

            # Right-edge clamp
            if x + tip_w > work_right - margin:
                x = work_right - tip_w - margin

            # Left-edge clamp (including negative coordinates on secondary monitors)
            if x < work_left + margin:
                x = work_left + margin

            # Bottom-edge: flip above trigger widget if overflow
            if y + tip_h > work_bottom - margin:
                y = widget_y - tip_h - 4
                # If still overflowing after flip, clamp to work area
                if y < work_top + margin:
                    y = work_top + margin

            tw.wm_geometry(f"+{x}+{y}")
            tw.deiconify()
        except Exception:
            self.hide_tip()
```

### 4.3 Design rationale

| Property | Current (line 260–285) | Fixed |
|---|---|---|
| Tooltip dimensions known? | No — `wm_geometry` before `label.pack()` | Yes — `withdraw()` → pack → `update_idletasks()` → measure `winfo_reqwidth/reqheight` |
| Flicker prevention? | No — tooltip appears at unclamped position first | Yes — `withdraw()` → measure → `wm_geometry(+x+y)` → `deiconify()` |
| Right-edge clamping? | None | Clamp `x` so `x + tip_w <= work_right - margin` |
| Bottom-edge clamping? | None | Flip above widget; if still overflowing, clamp to `work_top + margin` |
| Left-edge clamping? | None | Clamp `x >= work_left + margin` (supports negative coordinates) |
| Multi-monitor? | Not considered | `MonitorFromPoint` with `MONITOR_DEFAULTTONEAREST` handles negative X/Y correctly; `work_left` may be negative (e.g., `-1920`) and is preserved as-is |
| DPI changes? | N/A | ZERO — only reads monitor geometry, never calls `SetProcessDpi*` |
| Existing behavior preserved? | N/A | `setattr(self.widget, "_tooltip", self)` ✅, 350ms delay ✅, tooltip text/wrapping ✅, `hide_tip()` ✅ |

### 4.4 Existing pattern precedent

The speaker autocomplete popup (`misora.py:7102–7116`) already implements this exact clamping pattern using `_get_monitor_work_area`:
```python
x = max(work_left, min(raw_x, work_right - w))
y = max(work_top, min(raw_y, work_bottom - h))
popup.geometry(f"{w}x{h}+{x}+{y}")
popup.deiconify()
```

The `ToolTip` fix follows the same approach with the addition of bottom-edge flip-above behavior (since tooltips default below the widget but should flip above when near the screen bottom).

---

## 5. Exact Unified Diff (Provisional)

> [!NOTE]
> The diff below is the **planned** diff. The exact line numbers will be verified at execution time.
> `V-1`: `git apply --check` on this diff must pass.
> `V-2`: Post-edit `misora.py` logical line count must be reported exactly.
> `C-5`: Post-edit `CRLF == logical_lines`, `bare_LF == 0`, `bare_CR == 0`.

```diff
--- a/misora.py
+++ b/misora.py
@@ -199,6 +199,43 @@
 __version__ = _get_app_version()
 
 
+def _get_work_area(x: int, y: int, fallback_widget: Optional[tk.Widget] = None) -> Tuple[int, int, int, int]:
+    """Return (work_left, work_top, work_right, work_bottom) for the monitor containing (x, y).
+
+    Uses Win32 MonitorFromPoint/GetMonitorInfoW on Windows for accurate multi-monitor
+    work-area bounds (excluding taskbar). Falls back to Tk screen dimensions on
+    non-Windows platforms or on error. ZERO changes to DPI awareness (Rule 23).
+    """
+    if sys.platform == "win32" and hasattr(ctypes, "windll"):
+        try:
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
+            pt = wintypes.POINT(int(x), int(y))
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
 
@@ -260,17 +297,37 @@
     def show_tip(self) -> None:
         self._after_id = None
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
                 justify="left",
                 background="#201a33",
@@ -280,8 +337,30 @@
                 font=("Segoe UI", 8),
                 padx=6,
                 pady=3,
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
+                if y < work_top + margin:
+                    y = work_top + margin
+
+            tw.wm_geometry(f"+{x}+{y}")
+            tw.deiconify()
         except Exception:
             self.hide_tip()
```

**Estimated post-edit line count:** `23911 + 37 (new _get_work_area) + 20 (expanded show_tip) - 3 (removed old lines) = ~23965` (exact count to be verified at execution time).

**Verification commands (at execution):**
- `V-1`: `git diff misora.py | git apply --check` → must exit 0
- `V-2`: Exact post-edit `misora.py` logical line count → report
- `C-5`: `CRLF == logical_lines`, `bare_LF == 0`, `bare_CR == 0`
- `git diff --numstat -- misora.py` → report exact `A\tD\tfile`

---

## 6. Strict File Ownership Matrix (T-08a Execution Charter)

### Allowed ONLY after explicit `Proceed`:

| File | Scope | Notes |
|---|---|---|
| `misora.py` | Add `_get_work_area()` function; modify `ToolTip.show_tip()` ONLY | Minimal tooltip positioning + work-area helper |
| `tests/test_t08a_tooltip_clamping.py` | **NEW** — stdlib `unittest` | Zero `pytest`, zero `.unity3d`, zero `skipTest()`, `CONFIG_PATH` patched to temp dir, clean `app.destroy()` + `shutil.rmtree` in `tearDown` |
| `docs/project/OPEN_ISSUES.md` | T-08a row ONLY | Automated TDD result; Windows QA `M-1..M-6` stays `MANUAL-PENDING`; Lifecycle stays `ACTIVE` |
| `PROJECT_STATE.md` | Test count update ONLY | Exact `494 + N = (451 + N) PASS + 35 SKIP + 6 FAIL + 2 ERROR`; N-4 transient `--check` note; stay ≤ 15,360 bytes |

### Strictly FORBIDDEN / READ-ONLY:

| Path | Reason |
|---|---|
| `__init__.py` | Version source — NEVER modify |
| `core/**` | ENV-01 READ-ONLY |
| `assets/**` | ENV-01 READ-ONLY |
| All existing `tests/*.py` | Cannot modify existing tests |
| `AGENTS.md` | Layer 0 — read-only |
| `docs/archive/**` | History — never load or modify |
| `tools/generate_symbol_index.py` | Tooling — read-only |
| `docs/architecture/MISORA_SYMBOL_INDEX.md` | Deferred to Project Lead post-commit regeneration |
| `misora.bat`, `requirements.txt`, `misora_config.json` | Config/launcher — read-only |
| `backups/**`, `README.md` | Protected paths |

---

## 7. Zero-`.pyc` Windows-Safe TDD Verification Plan

### 7.1 New test file: `tests/test_t08a_tooltip_clamping.py`

**Test harness** (matches T-02 pattern):
- `CONFIG_PATH` patched to `tempfile.mkdtemp()` temp dir
- `misora.messagebox` patched
- `MisoraApp(restore_session=False, show_splash=False)` with `app.update_idletasks()`
- `tearDown`: `app.destroy()` in `try`, `misora.CONFIG_PATH` restore in `finally`, `shutil.rmtree` temp dir

**7.1.1 Defect Probes (MUST FAIL pre-patch with 0 errors, PASS post-patch):**

| ID | Test | Pre-patch | Post-patch |
|---|---|---|---|
| `test_probe_1_right_edge_clamp` | Tooltip on `lbl_char_overflow` with widget positioned near right edge: mock `_get_work_area` to return `(0, 0, 1920, 1050)`, mock `widget.winfo_rootx()` → `1800`. Assert `x + tip_w <= 1918` (work_right - margin). Pre-patch: tooltip at `x=1808` with `tip_w=702` → `x+tip_w=2510 > 1920` → FAIL. | FAIL | PASS |
| `test_probe_2_bottom_edge_flip` | Widget near bottom: mock `widget.winfo_rooty()` → `1020`, `widget.winfo_height()` → `25`. Default `y = 1020 + 25 + 4 = 1049`, `tip_h ≈ 34` → `y+tip_h = 1083 > 1050`. Assert tooltip flips above widget (`y < widget_y`). Pre-patch: tooltip at `y=1049` overflows. | FAIL | PASS |
| `test_probe_3_left_edge_clamp` | Mock work area `(0, 0, 1920, 1050)`, widget at `winfo_rootx()` → `-20`. Assert `x >= 0 + margin`. Pre-patch: tooltip at `x = -20 + 8 = -12` → FAIL. | FAIL | PASS |
| `test_probe_4_multi_monitor_negative` | Mock `_get_work_area` returning `(-1920, 0, 0, 1050)` (secondary monitor left of primary). Widget at `winfo_rootx()` → `-100`. Assert tooltip stays within `[-1918, -margin]`, not clamped to `0`. Pre-patch: tooltip at unclamped `x=-92`, but test specifically checks `x >= -1920 + margin = -1918` AND `x + tip_w <= 0 - margin = -2`. | FAIL | PASS |

**7.1.2 Regression Guards (MUST PASS pre- AND post-patch; N-3 Guard Re-Label Rule):**

| ID | Test | Pre | Post |
|---|---|---|---|
| `test_guard_1_center_screen_standard_position` | Widget at center of screen (e.g., `winfo_rootx()=500`, `winfo_rooty()=300`). Assert tooltip at `x = 508`, `y = widget_y + widget_h + 4` (standard near-widget position preserved). | PASS | PASS |
| `test_guard_2_tooltip_text_preserved` | `self.app.lbl_char_overflow._tooltip.text` contains `"54"` and `"digit-widths"`. T-02 2-line tooltip text unchanged. | PASS | PASS |
| `test_guard_3_hide_tip_destroys_cleanly` | Call `show_tip()`, verify `tip_window` exists, call `hide_tip()`, verify `tip_window is None` and no TclError. | PASS | PASS |

**7.1.3 Testing approach for pre-patch fail verification:**

The Defect Probes will test `ToolTip.show_tip()` by:
1. Creating a real `MisoraApp` instance.
2. Patching `_get_work_area` to return controlled work-area bounds.
3. Patching `self.widget.winfo_rootx()` / `winfo_rooty()` / `winfo_height()` to simulate edge positions.
4. Calling `tooltip.show_tip()`.
5. Asserting the resulting `tip_window.winfo_x()` / `winfo_y()` are within work-area bounds.

Pre-patch, `show_tip()` does not call `_get_work_area` and applies no clamping, so the tooltip appears at the unclamped position → assertions FAIL.
Post-patch, `show_tip()` calls `_get_work_area` and clamps → assertions PASS.

### 7.2 Broad BOM-safe compile check

```python
# In test setUp or a dedicated test:
bom = bytes([239, 187, 191])
for py_file in (repo / p for p in [
    "__init__.py", "misora.py",
    *sorted((repo / "core").glob("*.py")),
    *sorted((repo / "assets").glob("*.py")),
    *sorted((repo / "tests").glob("*.py")),
]):
    raw = py_file.read_bytes()
    src = raw.lstrip(bom).decode("utf-8")
    compile(src, str(py_file), "exec")  # NO compileall, NO .pyc
```

Plus: `pre_pyc_count == post_pyc_count` (count all `.pyc` files in repo before and after test run).

### 7.3 Discovery math

| Phase | Total | PASS | SKIP | FAIL | ERROR |
|---|---|---|---|---|---|
| Pre-patch (baseline) | 494 | 451 | 35 | 6 | 2 |
| Post-patch (T-08a adds N tests) | 494 + N | 451 + N | 35 | 6 | 2 |

- Pre-patch run of T-08a suite: **exactly `FAILED (failures=P)` with 0 errors** (Probes fail, Guards pass).
- Post-patch T-08a suite: `N/N OK`.
- Post-patch targeted suites: `test_t02_next_tooltip` (8/8), `test_v15_s11e_polish_splash_menu_tooltips` (9/9).
- Post-patch full discovery: `py -3.12 -B -m unittest discover -s tests -v` → exact `(494 + N) = (451 + N) PASS + 35 SKIP + 6 FAIL + 2 ERROR`.

---

## 8. Complete 4-File Rollback Steps

Pinned to exact `POST_DOCS01_HEAD = 9fa266375caf0994e49c9ed5ce8b7b1203b28f3c`.

> [!WARNING]
> NEVER use `git reset --hard`, `git clean`, or blanket `git checkout`.

```powershell
# 1. Restore misora.py to exact POST_DOCS01_HEAD content
cd D:\Misora-Editor
git checkout 9fa266375caf0994e49c9ed5ce8b7b1203b28f3c -- misora.py

# 2. Restore docs/project/OPEN_ISSUES.md
git checkout 9fa266375caf0994e49c9ed5ce8b7b1203b28f3c -- docs/project/OPEN_ISSUES.md

# 3. Restore PROJECT_STATE.md
git checkout 9fa266375caf0994e49c9ed5ce8b7b1203b28f3c -- PROJECT_STATE.md

# 4. Remove new test file
Remove-Item -Path tests\test_t08a_tooltip_clamping.py -ErrorAction SilentlyContinue

# 5. Verify clean tree
git status --short --untracked-files=all
# Expected: (empty)

# 6. Verify test count restored
py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"
# Expected: countTestCases: 494

# 7. Verify misora.py line count restored
py -3.12 -B -c "data=open('misora.py','rb').read(); print(data.count(bytes([10])))"
# Expected: 23911
```

---

## 9. Manual Windows QA Checklist (`M-1..M-6`) — `MANUAL-PENDING`

| ID | Test | DPI | Window State | Expected | Status |
|---|---|---|---|---|---|
| **M-1** | Hover `lbl_char_overflow` with maximized window at 1920×1080 | 100% | Maximized | Tooltip fully visible, clamped inside right screen edge | `MANUAL-PENDING` |
| **M-2** | Same as M-1 | 125% | Maximized | Tooltip fully visible, clamped inside right screen edge | `MANUAL-PENDING` |
| **M-3** | Hover bottom-bar widget (e.g., Save/Revert) near screen bottom | 100% | Maximized | Tooltip flips above widget, fully visible | `MANUAL-PENDING` |
| **M-4** | Hover widget near left edge (e.g., after dragging window so ribbon starts at x≈0) | 100% | Windowed | Tooltip clamped at left edge, not clipped | `MANUAL-PENDING` |
| **M-5** | Multi-monitor: hover tooltip-bearing widget on secondary monitor (if available) | Any | Any | Tooltip stays within secondary monitor bounds, never jumps to primary | `MANUAL-PENDING` |
| **M-6** | Operator sign-off | — | — | All M-1..M-5 pass, no visual regressions in tooltip appearance/timing | `MANUAL-PENDING` |

---

## 10. N-4 Transient `--check` Note

After adding `_get_work_area()` as a module-level function in `misora.py`, the symbol index (`docs/architecture/MISORA_SYMBOL_INDEX.md`) will become stale. `tools/generate_symbol_index.py --check` will FAIL transiently until the Project Lead runs regeneration post-commit. This is the same N-4 pattern as T-01 and T-02.

Do NOT modify `tools/generate_symbol_index.py` or `docs/architecture/MISORA_SYMBOL_INDEX.md` — these are deferred to Project Lead post-commit regeneration.

---

## 11. Plan Verification

| Check | Result |
|---|---|
| `git status --short --untracked-files=all` (D:\Misora-Editor) | **(to be verified at plan write time — must be empty)** |
| Written to | `D:\Reference\Misora-Reference\T-08a_Implementation_Plan.md` |
| SHA-256 | **(to be computed after write)** |

---

**STOP — WAITING FOR INDEPENDENT REVIEW**
