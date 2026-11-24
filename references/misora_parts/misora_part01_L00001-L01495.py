# ======================================================================
# FILE: misora.py — PART 01 / 10
# ORIGINAL LINE RANGE : L1 .. L1495 (total 1495 lines of 12835)
# SOURCE SHA-256      : d23baae2be82fe93a18da7d3769af30d19ebe02a8b5f6a3645d56a6f53c0710e
# NOTE FOR AI REVIEWER: Cite ORIGINAL line numbers (L1..L1495) and symbol names.
# SYMBOLS IN THIS PART (with exact original line numbers):
#   L00087: def _get_app_version()
#   L00110: class ToolTip
#   L00113:   ToolTip.__init__ (def)
#   L00126:   ToolTip.on_enter (def)
#   L00135:   ToolTip.on_leave (def)
#   L00139:   ToolTip.on_destroy (def)
#   L00143:   ToolTip.cancel_timer (def)
#   L00151:   ToolTip.widget_exists (def)
#   L00157:   ToolTip.show_tip (def)
#   L00183:   ToolTip.hide_tip (def)
#   L00193: def create_tooltip()
#   L00442: def wcag_relative_luminance()
#   L00457: def wcag_contrast_ratio()
#   L00465: def best_contrast_fg()
#   L00478: def init_process_dpi_awareness()
#   L00503: def sanitize_window_geometry()
#   L00531: class NguiColorPickerPopup
#   L00539:   NguiColorPickerPopup.__init__ (def)
#   L00600:   NguiColorPickerPopup._build_ui (def)
#   L00814:   NguiColorPickerPopup._select_stop (def)
#   L00824:   NguiColorPickerPopup._render_hue_bar (def)
#   L00857:   NguiColorPickerPopup._render_sv_map (def)
#   L00895:   NguiColorPickerPopup._render_gradient_preview (def)
#   L00933:   NguiColorPickerPopup._sync_ui_from_hsv (def)
#   L00971:   NguiColorPickerPopup._on_sv_drag (def)
#   L00978:   NguiColorPickerPopup._on_hue_drag (def)
#   L00984:   NguiColorPickerPopup._set_color_hex (def)
#   L00998:   NguiColorPickerPopup._on_hex_entry_commit (def)
#   L01007:   NguiColorPickerPopup._toggle_eyedropper (def)
#   L01026:   NguiColorPickerPopup._poll_eyedropper (def)
#   L01088:   NguiColorPickerPopup._stop_eyedropper (def)
#   L01105:   NguiColorPickerPopup._commit_single_color (def)
#   L01111:   NguiColorPickerPopup._commit_gradient_color (def)
#   L01118:   NguiColorPickerPopup._on_escape (def)
#   L01124:   NguiColorPickerPopup._on_close (def)
#   L01140: def safe_grab_release()
#   L01150: def write_atomic_utf8()
#   L01161: def _get_box_uid()
#   L01173: def compute_stable_lock_key()
#   L01178: def get_document_stable_locks()
#   L01195: def restore_stable_locks()
#   L01221: class MisoraApp
#   L01224:   MisoraApp.__init__ (def)
#   L01464:   MisoraApp.get_icon (def)
#   L01468:   MisoraApp.safe_clipboard_get (def)
#   L01480:   MisoraApp.safe_clipboard_set (def)
# ======================================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Misora: Unity3D Revision Tool & Story Editor
=============================================
A specialized GUI text editor for inspecting, searching, and in-place patching
of Princess Connect! Re:Dive Unity3D story bundles (.unity3d) and XUAT translation files.
"""
from __future__ import annotations

import collections
import colorsys
import ctypes
import hashlib
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import colorchooser, filedialog, messagebox, ttk
from typing import Any, Dict, List, Optional, Set, Tuple, Union

try:
    from PIL import Image, ImageGrab, ImageTk
except ImportError:
    Image = None  # type: ignore
    ImageTk = None  # type: ignore
    ImageGrab = None  # type: ignore

if sys.platform == "win32":
    import winreg
    from ctypes import wintypes

# Ensure both Misora root and toolkit parent are in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR.parent))

try:
    from misora.assets.icon import THEME, apply_window_icon, get_icon, prune_icon_cache
    from misora.assets.splash import MisoraSplashScreen
    from misora.core import (
        ALWAYS_ON_CATEGORY, LOG_CATEGORIES, LOG_LEVELS, Box, BoxSnapshot, BundleIOError,
        BoxEditDelta, BoxStructuralDelta, BulkFileDelta, MetadataDelta, LogEntry, MasterUndoJournal, MisoraLogger,
        PlainTextDelta, ProjectSearchEngine, Record, SearchOptions, SearchResult,
        StoryDocument, UndoOperation, XUnitySyncManager, load_bundle_story,
        save_bundle_story, dispose_unity_env,
        MTLConfig, MTLEngine, TagMasker, translate_async, MTL_ENGINES, DEFAULT_LLM_PROMPT,
        serialize, parse, sniff_format, apply_to_document, sanitize_speaker,
        DialogueBlock, MetadataBlock, ParseResult,
        NGUI_TAG_RE, NGUI_TOKEN_RE, normalize_gradient_syntax, strip_tags, get_rendered_length, measure_line_lengths,
        protect_secret, unprotect_secret, redact_secret,
        DecodedText, detect_encoding_and_decode, encode_with_metadata,
        read_text_file_strictly, write_atomic_encoded,
    )
except ImportError:
    from assets.icon import THEME, apply_window_icon, get_icon, prune_icon_cache
    from assets.splash import MisoraSplashScreen
    from core import (
        ALWAYS_ON_CATEGORY, LOG_CATEGORIES, LOG_LEVELS, Box, BoxSnapshot, BundleIOError,
        BoxEditDelta, BoxStructuralDelta, BulkFileDelta, MetadataDelta, LogEntry, MasterUndoJournal, MisoraLogger,
        PlainTextDelta, ProjectSearchEngine, Record, SearchOptions, SearchResult,
        StoryDocument, UndoOperation, XUnitySyncManager, load_bundle_story,
        save_bundle_story, dispose_unity_env,
        MTLConfig, MTLEngine, TagMasker, translate_async, MTL_ENGINES, DEFAULT_LLM_PROMPT,
        serialize, parse, sniff_format, apply_to_document, sanitize_speaker,
        DialogueBlock, MetadataBlock, ParseResult,
        NGUI_TAG_RE, NGUI_TOKEN_RE, normalize_gradient_syntax, strip_tags, get_rendered_length, measure_line_lengths,
        protect_secret, unprotect_secret, redact_secret,
        DecodedText, detect_encoding_and_decode, encode_with_metadata,
        read_text_file_strictly, write_atomic_encoded,
    )

CONFIG_PATH = SCRIPT_DIR / "misora_config.json"
DEBUG_LOG_PATH = SCRIPT_DIR / "misora_debug.log"
HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

def _get_app_version() -> str:
    """Retrieve application version string from root __init__.py as single source of truth (Rule 21)."""
    try:
        import __init__ as _root_init
        if hasattr(_root_init, "__version__"):
            return _root_init.__version__
    except Exception:
        pass
    try:
        init_file = SCRIPT_DIR / "__init__.py"
        if init_file.is_file():
            for line in init_file.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("__version__"):
                    parts = line.split("=")
                    if len(parts) == 2:
                        return parts[1].strip().strip('"\'')
    except Exception:
        pass
    return "1.4.0"

__version__ = _get_app_version()


class ToolTip:
    """Robust hover tooltip for Tkinter widgets with delayed display and safe lifecycle (Part C.5 / TOOLTIP-LIFECYCLE)."""

    def __init__(self, widget: tk.Widget, text: str, delay_ms: int = 350):
        self.widget = widget
        self.text = text
        self.delay_ms = delay_ms
        self.tip_window: Optional[tk.Toplevel] = None
        self._after_id: Optional[str] = None
        setattr(self.widget, "_tooltip", self)

        if hasattr(self.widget, "bind"):
            self.widget.bind("<Enter>", self.on_enter, add="+")
            self.widget.bind("<Leave>", self.on_leave, add="+")
            self.widget.bind("<Destroy>", self.on_destroy, add="+")

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
        except Exception:
            self.hide_tip()

    def hide_tip(self, _event=None) -> None:
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




THEME_PRESETS: Dict[str, Dict[str, str]] = {
    "Misora Purple & White": {
        "bg_dark": "#f3eefb",
        "bg_panel": "#ffffff",
        "bg_editor": "#faf8fe",
        "border": "#d4c4ec",
        "fg_text": "#221833",
        "fg_muted": "#6b5a88",
        "misora_pink": "#7b42bc",
        "misora_pink_hover": "#9056d2",
        "misora_pink_active": "#612ea0",
        "accent_blue": "#536dfe",
        "accent_green": "#2e7d32",
        "accent_yellow": "#8e24aa",
        "highlight_bg": "#e8dbfa",
    },
    "Misora Classic (Dark)": {
        "bg_dark": "#14141a",
        "bg_panel": "#1e1e26",
        "bg_editor": "#181820",
        "border": "#30303e",
        "fg_text": "#f0f0f5",
        "fg_muted": "#9898a8",
        "misora_pink": "#ff7da7",
        "misora_pink_hover": "#ff99ba",
        "misora_pink_active": "#e05a87",
        "accent_blue": "#68b5f3",
        "accent_green": "#6ad18a",
        "accent_yellow": "#f5c26b",
        "highlight_bg": "#382433",
    },
    "Midnight Violet": {
        "bg_dark": "#161224",
        "bg_panel": "#201a33",
        "bg_editor": "#130f20",
        "border": "#3a2f5c",
        "fg_text": "#f1ecfa",
        "fg_muted": "#9c8ec0",
        "misora_pink": "#a66cff",
        "misora_pink_hover": "#b98aff",
        "misora_pink_active": "#894be8",
        "accent_blue": "#79c0ff",
        "accent_green": "#7ee787",
        "accent_yellow": "#e3b341",
        "highlight_bg": "#362459",
    },
    "Clean Daylight": {
        "bg_dark": "#eceef2",
        "bg_panel": "#ffffff",
        "bg_editor": "#f8f9fb",
        "border": "#cfd5e0",
        "fg_text": "#1f2430",
        "fg_muted": "#606a7e",
        "misora_pink": "#6f42c1",
        "misora_pink_hover": "#8458d4",
        "misora_pink_active": "#5932a3",
        "accent_blue": "#0969da",
        "accent_green": "#1a7f37",
        "accent_yellow": "#9a6700",
        "highlight_bg": "#e6dcf8",
    },
}

DEFAULT_PREFS: Dict[str, Any] = {
    "dialogue_font_family": "Segoe UI",
    "dialogue_font_size": 11,
    "raw_font_size": 9,
    "ui_font_size": 9,
    "theme": dict(THEME_PRESETS["Misora Purple & White"]),
    "debug": {
        "console_visible": False,
        "log_to_file": False,
        "level": "Info",
        "categories": {cat: True for cat in LOG_CATEGORIES},
    },
}

PRICONNE_SWATCHES: List[Tuple[str, str]] = [
    ("Misora Purple", "#7b42bc"),
    ("Misora Pink", "#ff7da7"),
    ("Astrum Blue", "#4a90e2"),
    ("Pecorine Gold", "#e5a93b"),
    ("Kokkoro Mint", "#2e9e5b"),
    ("Kyaru Violet", "#8e44ad"),
    ("Crimson Alert", "#d94862"),
    ("Pure White", "#ffffff"),
    ("Deep Plum", "#221833"),
    ("Soft Silver", "#9aa3b2"),
]

NGUI_GLOSSARY_ITEMS: List[Dict[str, str]] = [
    {
        "tag": "[rub:ruby]base[/rub]",
        "title": "Ruby / Furigana Text (Priconne NGUI)",
        "syntax": "[rub:Command]Wish[/rub]",
        "insert_open": "[rub:]",
        "insert_close": "[/rub]",
        "action": "ruby",
        "desc": "Cygames' custom Priconne NGUI tag. Renders 'ruby' in small text centered directly above 'base' (e.g., [rub:めいれい]願い[/rub]). Double-click or press Ctrl+R to wrap selected text.",
    },
    {
        "tag": "[RRGGBB]",
        "title": "Hex RGB Text Color",
        "syntax": "[7B42BC]Colored text[-]",
        "insert_open": "[7B42BC]",
        "insert_close": "[-]",
        "desc": "Changes text color starting at the tag using a 6-digit hexadecimal RGB code. Always close with [-] to restore default label color.",
    },
    {
        "tag": "[RRGGBBAA]",
        "title": "Hex RGBA Color + Alpha",
        "syntax": "[FFFFFF80]Semi-transparent[-]",
        "insert_open": "[FFFFFF80]",
        "insert_close": "[-]",
        "desc": "Sets both RGB color and alpha opacity (00 = invisible, FF = opaque) in NGUI UILabel.",
    },
    {
        "tag": "[RRGGBB-RRGGBB]",
        "title": "Vertical Gradient Color (Top-Bottom)",
        "syntax": "[7B42BC-FF7DA7]Gradient text[-]",
        "insert_open": "[7B42BC-FF7DA7]",
        "insert_close": "[-]",
        "desc": "Applies a top-to-bottom vertical gradient using a hyphen (-) between top and bottom hex colors. Note: NGUI requires '-' (comma syntax displays as literal text). Close with [-].",
    },
    {
        "tag": "[RRGGBBAA-RRGGBBAA]",
        "title": "Vertical Gradient Color + Alpha",
        "syntax": "[FF7DA7FF-68B5F380]Alpha gradient[-]",
        "insert_open": "[FF7DA7FF-68B5F380]",
        "insert_close": "[-]",
        "desc": "Applies a top-to-bottom vertical gradient with per-stop alpha opacity (00 = invisible, FF = opaque). Close with [-].",
    },
    {
        "tag": "[-]",
        "title": "Reset / Close Color Tag",
        "syntax": "[68B5F3]Blue[-] Normal",
        "insert_open": "[-]",
        "insert_close": "",
        "desc": "Pops the active [RRGGBB] or gradient color override and returns to the default dialogue text color.",
    },
    {
        "tag": "[/]",
        "title": "Reset / Close Style Tag (Shorthand)",
        "syntax": "[b][i]Bold italic[/] Normal",
        "insert_open": "[/]",
        "insert_close": "",
        "desc": "NGUI shorthand tag that closes active text formatting styles ([b], [i], [u], [s], [sub], [sup]).",
    },
    {
        "tag": "[b]...[/b]",
        "title": "Bold Style",
        "syntax": "[b]Emphasized text[/b]",
        "insert_open": "[b]",
        "insert_close": "[/b]",
        "desc": "Renders enclosed text in bold weight inside NGUI rich-text labels.",
    },
    {
        "tag": "[i]...[/i]",
        "title": "Italic Style",
        "syntax": "[i]Whispered thought[/i]",
        "insert_open": "[i]",
        "insert_close": "[/i]",
        "desc": "Slants enclosed text in italics for inner monologues, emphasis, or foreign terms.",
    },
    {
        "tag": "[u]...[/u]",
        "title": "Underline Style",
        "syntax": "[u]Underlined phrase[/u]",
        "insert_open": "[u]",
        "insert_close": "[/u]",
        "desc": "Draws an underline beneath the enclosed characters.",
    },
    {
        "tag": "[s]...[/s]",
        "title": "Strikethrough Style",
        "syntax": "[s]Crossed-out text[/s]",
        "insert_open": "[s]",
        "insert_close": "[/s]",
        "desc": "Draws a horizontal strikethrough line across the enclosed text.",
    },
    {
        "tag": "[sub]...[/sub]",
        "title": "Subscript Text",
        "syntax": "H[sub]2[/sub]O",
        "insert_open": "[sub]",
        "insert_close": "[/sub]",
        "desc": "Shrinks and lowers enclosed characters below the text baseline.",
    },
    {
        "tag": "[sup]...[/sup]",
        "title": "Superscript Text",
        "syntax": "10[sup]th[/sup] Anniversary",
        "insert_open": "[sup]",
        "insert_close": "[/sup]",
        "desc": "Shrinks and raises enclosed characters above the text baseline.",
    },
    {
        "tag": "[url=...]...[/url]",
        "title": "Clickable URL / Link Tag",
        "syntax": "[url=https://example.com]Link[/url]",
        "insert_open": "[url=]",
        "insert_close": "[/url]",
        "desc": "Marks a clickable text span retrievable via NGUI UILabel.GetUrlAtPosition().",
    },
    {
        "tag": "[c]...[/c]",
        "title": "Ignore Label Tint",
        "syntax": "[c]Untinted text[/c]",
        "insert_open": "[c]",
        "insert_close": "[/c]",
        "desc": "Prevents NGUI's widget color multiplier from tinting the enclosed characters.",
    },
    {
        "tag": "{playername}",
        "title": "Player Name Placeholder",
        "syntax": "Good morning, {playername}!",
        "insert_open": "{playername}",
        "insert_close": "",
        "desc": "Represents the protagonist's name in Misora & XUAT .txt dictionaries. Automatically compiled to {0} when saving .unity3d bundles.",
    },
    {
        "tag": "\\n",
        "title": "Explicit Line Break",
        "syntax": "First line\\nSecond line",
        "insert_open": "\\n",
        "insert_close": "",
        "desc": "Forces a line break inside the ADV dialogue box. Pressing Enter in the editor automatically serializes the bundle's line break format.",
    },
    {
        "tag": "──",
        "title": "ADV Dialogue Pause / Dash",
        "syntax": "──Wait right there!",
        "insert_open": "──",
        "insert_close": "",
        "desc": "Standard double box-drawing horizontal dash used at the start of Priconne dialogue interruptions.",
    },
]


# -----------------------------------------------------------------------------
# WCAG 2.1 Contrast-Safe Color Utilities (#13)
# -----------------------------------------------------------------------------
def wcag_relative_luminance(hex_color: str) -> float:
    """Compute WCAG 2.1 relative luminance in [0.0, 1.0] for a #RRGGBB hex string."""
    if not HEX_COLOR_RE.match(hex_color):
        return 0.0

    def _lin(c8: int) -> float:
        s = c8 / 255.0
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

    r = _lin(int(hex_color[1:3], 16))
    g = _lin(int(hex_color[3:5], 16))
    b = _lin(int(hex_color[5:7], 16))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def wcag_contrast_ratio(hex_a: str, hex_b: str) -> float:
    """Compute WCAG 2.1 contrast ratio in [1.0, 21.0] between two #RRGGBB colors."""
    la = wcag_relative_luminance(hex_a)
    lb = wcag_relative_luminance(hex_b)
    hi, lo = (la, lb) if la >= lb else (lb, la)
    return (hi + 0.05) / (lo + 0.05)


def best_contrast_fg(
    bg_hex: str,
    dark_fg: str = "#14141a",
    light_fg: str = "#ffffff",
) -> str:
    """Pick whichever of `dark_fg` or `light_fg` maximizes WCAG contrast on `bg_hex`."""
    if not HEX_COLOR_RE.match(bg_hex):
        return light_fg
    c_dark = wcag_contrast_ratio(bg_hex, dark_fg)
    c_light = wcag_contrast_ratio(bg_hex, light_fg)
    return light_fg if c_light >= c_dark else dark_fg


def init_process_dpi_awareness() -> None:
    """Set process DPI awareness once at application startup before creating Tk root (Rule 23).

    Ensures consistent rendering scale across displays without mutating process DPI
    awareness dynamically during GUI execution.
    """
    if sys.platform != "win32":
        return
    try:
        # Try SetProcessDpiAwarenessContext (Windows 10 1703+)
        # -2 = DPI_AWARENESS_CONTEXT_SYSTEM_AWARE
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-2))
    except Exception:
        try:
            # Fallback to shcore (Windows 8.1+)
            # 1 = PROCESS_SYSTEM_DPI_AWARE
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                # Fallback to user32 (Vista+)
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


def sanitize_window_geometry(geom_str: str, screen_w: int, screen_h: int) -> str:
    """Validate and clamp a Tk geometry string to ensure it is within visible screen bounds (S9c)."""
    if not isinstance(geom_str, str) or not geom_str.strip():
        return ""
    m = re.match(r"^(\d+)x(\d+)([+-]\d+)([+-]\d+)$", geom_str.strip())
    if not m:
        return geom_str.strip()
    w, h, x, y = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))

    # Bound dimensions to screen limits
    if screen_w > 0:
        w = max(400, min(w, screen_w))
    if screen_h > 0:
        h = max(300, min(h, screen_h))

    # Clamp x coordinate so at least 120px is within screen bounds
    if screen_w > 0:
        if x + 120 > screen_w or x < 0:
            x = max(0, min(x, max(0, screen_w - w)))

    # Clamp y coordinate so title bar (top 50px) is visible
    if screen_h > 0:
        if y + 50 > screen_h or y < 0:
            y = max(0, min(y, max(0, screen_h - h)))

    return f"{w}x{h}+{x}+{y}"


class NguiColorPickerPopup(tk.Toplevel):
    """Mini texture-editor style Color Picker & Gradient Builder with Screen Eyedropper."""

    SV_W = 180
    SV_H = 140
    HUE_W = 20
    HUE_H = 140

    def __init__(
        self,
        parent: "MisoraApp",
        primary_hex: str = "#7b42bc",
        secondary_hex: str = "#ff7da7",
    ):
        super().__init__(parent)
        self.app = parent
        self.theme = parent.theme
        self.title(f"NGUI Color & Gradient Picker (v{__version__})")
        self.configure(bg=self.theme["bg_panel"])
        self.transient(parent)

        try:
            self.stop_colors: List[str] = [
                primary_hex.lower() if HEX_COLOR_RE.match(primary_hex) else "#7b42bc",
                secondary_hex.lower() if HEX_COLOR_RE.match(secondary_hex) else "#ff7da7",
            ]
            self.active_stop: int = 0
            self._eyedropper_active: bool = False
            self._eyedropper_after_id: Optional[str] = None
            self._mouse_was_down: bool = False

            r = int(self.stop_colors[0][1:3], 16) / 255.0
            g = int(self.stop_colors[0][3:5], 16) / 255.0
            b = int(self.stop_colors[0][5:7], 16) / 255.0
            self._h, self._s, self._v = colorsys.rgb_to_hsv(r, g, b)

            self._sv_photo: Any = None
            self._hue_photo: Any = None
            self._grad_photo: Any = None

            self._build_ui()
            self._render_hue_bar()
            self._render_sv_map()
            self._sync_ui_from_hsv()

            self.update_idletasks()
            req_w = max(420, self.winfo_reqwidth())
            req_h = max(340, self.winfo_reqheight())
            px = parent.winfo_rootx() + (parent.winfo_width() // 2) - (req_w // 2)
            py = parent.winfo_rooty() + (parent.winfo_height() // 2) - (req_h // 2)
            self.geometry(f"{req_w}x{req_h}+{max(20, px)}+{max(20, py)}")
            self.minsize(req_w, req_h)
            self.resizable(False, False)
            self.app.logger.info("UI / Theme / Config", f"NguiColorPickerPopup initialized ({req_w}x{req_h})")
        except Exception:
            import traceback
            err = traceback.format_exc()
            try:
                self.app.logger.exception(f"NguiColorPickerPopup initialization failed:\n{err}")
            except Exception:
                pass
            with open("picker_error.log", "w", encoding="utf-8") as f:
                f.write(err)
            messagebox.showerror("Color Picker Init Error", err)
            raise

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.bind("<Escape>", self._on_escape)

    def _build_ui(self) -> None:
        t = self.theme
        accent_fg = best_contrast_fg(t["misora_pink"])
        accent_hover_fg = best_contrast_fg(t["misora_pink_hover"])
        editor_fg = best_contrast_fg(t["bg_editor"], t["fg_text"], "#ffffff")

        stop_bar = tk.Frame(self, bg=t["bg_panel"])
        stop_bar.pack(fill="x", padx=12, pady=(10, 6))

        tk.Label(
            stop_bar,
            text="Target Stop:",
            font=("Segoe UI", 9, "bold"),
            bg=t["bg_panel"],
            fg=best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff"),
        ).pack(side="left", padx=(0, 6))

        self.btn_stop0 = tk.Button(
            stop_bar,
            text="1: Primary / Top",
            font=("Segoe UI", 8, "bold"),
            relief="solid",
            bd=1,
            cursor="hand2",
            command=lambda: self._select_stop(0),
        )
        self.btn_stop0.pack(side="left", padx=(0, 4))

        self.btn_stop1 = tk.Button(
            stop_bar,
            text="2: Gradient Bottom",
            font=("Segoe UI", 8, "bold"),
            relief="solid",
            bd=1,
            cursor="hand2",
            command=lambda: self._select_stop(1),
        )
        self.btn_stop1.pack(side="left")

        map_row = tk.Frame(self, bg=t["bg_panel"])
        map_row.pack(fill="x", padx=12, pady=4)

        self.canvas_sv = tk.Canvas(
            map_row,
            width=self.SV_W,
            height=self.SV_H,
            bd=1,
            relief="solid",
            highlightthickness=0,
            cursor="crosshair",
        )
        self.canvas_sv.pack(side="left")
        self.canvas_sv.bind("<Button-1>", self._on_sv_drag)
        self.canvas_sv.bind("<B1-Motion>", self._on_sv_drag)

        self.canvas_hue = tk.Canvas(
            map_row,
            width=self.HUE_W,
            height=self.HUE_H,
            bd=1,
            relief="solid",
            highlightthickness=0,
            cursor="sb_v_double_arrow",
        )
        self.canvas_hue.pack(side="left", padx=(8, 10))
        self.canvas_hue.bind("<Button-1>", self._on_hue_drag)
        self.canvas_hue.bind("<B1-Motion>", self._on_hue_drag)

        side_col = tk.Frame(map_row, bg=t["bg_panel"])
        side_col.pack(side="left", fill="y")

        swatch_pair = tk.Frame(side_col, bg=t["bg_panel"])
        swatch_pair.pack(fill="x", pady=(0, 6))

        self.lbl_swatch_active = tk.Label(
            swatch_pair,
            width=7,
            height=2,
            bg=self.stop_colors[0],
            relief="solid",
            bd=1,
        )
        self.lbl_swatch_active.pack(side="left")

        self.canvas_grad_preview = tk.Canvas(
            swatch_pair,
            width=46,
            height=34,
            bd=1,
            relief="solid",
            highlightthickness=0,
        )
        self.canvas_grad_preview.pack(side="left", padx=(6, 0))

        hex_row = tk.Frame(side_col, bg=t["bg_panel"])
        hex_row.pack(fill="x", pady=2)
        tk.Label(hex_row, text="Hex:", font=("Segoe UI", 8, "bold"), bg=t["bg_panel"], fg=t["fg_muted"]).pack(side="left")
        self.var_hex = tk.StringVar(master=self, value=self.stop_colors[0].upper())
        ent_hex = tk.Entry(
            hex_row,
            textvariable=self.var_hex,
            width=9,
            font=("Consolas", 9, "bold"),
            bg=t["bg_editor"],
            fg=editor_fg,
            insertbackground=t["misora_pink"],
            bd=1,
            relief="solid",
            highlightthickness=0,
        )
        ent_hex.pack(side="right")
        ent_hex.bind("<Return>", self._on_hex_entry_commit)
        ent_hex.bind("<FocusOut>", self._on_hex_entry_commit)

        self.lbl_rgb = tk.Label(
            side_col,
            text="RGB: 123, 66, 188",
            font=("Consolas", 8),
            bg=t["bg_panel"],
            fg=t["fg_muted"],
            anchor="w",
        )
        self.lbl_rgb.pack(fill="x", pady=(2, 6))

        self.btn_eyedropper = tk.Button(
            side_col,
            text="💧 Eyedropper",
            font=("Segoe UI", 8, "bold"),
            bg=t["bg_editor"],
            fg=editor_fg,
            activebackground=t["highlight_bg"],
            activeforeground=best_contrast_fg(t["highlight_bg"]),
            relief="solid",
            bd=1,
            padx=6,
            pady=3,
            cursor="hand2",
            command=self._toggle_eyedropper,
        )
        self.btn_eyedropper.pack(fill="x")

        self.lbl_eye_hint = tk.Label(
            side_col,
            text="",
            font=("Segoe UI", 7),
            bg=t["bg_panel"],
            fg=t["accent_blue"],
            wraplength=112,
            justify="left",
        )
        self.lbl_eye_hint.pack(fill="x", pady=(3, 0))

        sw_frame = tk.Frame(self, bg=t["bg_panel"])
        sw_frame.pack(fill="x", padx=12, pady=(6, 4))
        tk.Label(
            sw_frame,
            text="Quick Swatches:",
            font=("Segoe UI", 8),
            bg=t["bg_panel"],
            fg=t["fg_muted"],
        ).pack(side="left", padx=(0, 6))

        for _name, hex_c in PRICONNE_SWATCHES:
            sb = tk.Button(
                sw_frame,
                width=2,
                height=1,
                bg=hex_c,
                activebackground=hex_c,
                relief="solid",
                bd=1,
                cursor="hand2",
                command=lambda c=hex_c: self._set_color_hex(c),
            )
            sb.pack(side="left", padx=1)

        act_bar = tk.Frame(self, bg=t["bg_panel"])
        act_bar.pack(fill="x", padx=12, pady=(8, 12))

        self.btn_insert_single = tk.Button(
            act_bar,
            text=f"Insert [{self.stop_colors[0][1:].upper()}]",
            font=("Segoe UI", 9, "bold"),
            bg=t["misora_pink"],
            fg=accent_fg,
            activebackground=t["misora_pink_hover"],
            activeforeground=accent_hover_fg,
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self._commit_single_color,
        )
        self.btn_insert_single.pack(side="left", padx=(0, 6))

        self.btn_insert_grad = tk.Button(
            act_bar,
            text="Insert Gradient [1-2]",
            font=("Segoe UI", 9, "bold"),
            bg=t["bg_editor"],
            fg=editor_fg,
            activebackground=t["highlight_bg"],
            activeforeground=best_contrast_fg(t["highlight_bg"]),
            relief="solid",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self._commit_gradient_color,
        )
        self.btn_insert_grad.pack(side="left")

        ttk.Button(act_bar, text="Close", style="TButton", command=self._on_close).pack(side="right")

    def _select_stop(self, stop_idx: int) -> None:
        self.active_stop = stop_idx
        hex_c = self.stop_colors[stop_idx]
        r = int(hex_c[1:3], 16) / 255.0
        g = int(hex_c[3:5], 16) / 255.0
        b = int(hex_c[5:7], 16) / 255.0
        self._h, self._s, self._v = colorsys.rgb_to_hsv(r, g, b)
        self._render_sv_map()
        self._sync_ui_from_hsv()

    def _render_hue_bar(self) -> None:
        w, h = self.HUE_W, self.HUE_H
        if Image is not None and ImageTk is not None:
            raw = bytearray(w * h * 3)
            h_denom = max(1, h - 1)
            idx = 0
            for y in range(h):
                hue = y / h_denom
                r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                rb = int(r * 255)
                gb = int(g * 255)
                bb = int(b * 255)
                for _ in range(w):
                    raw[idx] = rb
                    raw[idx + 1] = gb
                    raw[idx + 2] = bb
                    idx += 3
            im = Image.frombytes("RGB", (w, h), bytes(raw))
            img = ImageTk.PhotoImage(im, master=self)
        else:
            img = tk.PhotoImage(master=self, width=w, height=h)
            rows: List[str] = []
            for y in range(h):
                hue = y / max(1, h - 1)
                r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                hx = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"
                rows.append("{" + " ".join([hx] * w) + "}")
            img.put(" ".join(rows))
        self._hue_photo = img
        self.canvas_hue.image = img
        self.canvas_hue.delete("all")
        self.canvas_hue.create_image(0, 0, anchor="nw", image=img)

    def _render_sv_map(self) -> None:
        w, h = self.SV_W, self.SV_H
        hue = self._h
        if Image is not None and ImageTk is not None:
            raw = bytearray(w * h * 3)
            w_denom = max(1, w - 1)
            h_denom = max(1, h - 1)
            idx = 0
            for y in range(h):
                v = 1.0 - (y / h_denom)
                for x in range(w):
                    s = x / w_denom
                    r, g, b = colorsys.hsv_to_rgb(hue, s, v)
                    raw[idx] = int(r * 255)
                    raw[idx + 1] = int(g * 255)
                    raw[idx + 2] = int(b * 255)
                    idx += 3
            im = Image.frombytes("RGB", (w, h), bytes(raw))
            img = ImageTk.PhotoImage(im, master=self)
        else:
            img = tk.PhotoImage(master=self, width=w, height=h)
            rows = []
            w_denom = max(1, w - 1)
            h_denom = max(1, h - 1)
            for y in range(h):
                v = 1.0 - (y / h_denom)
                row_colors: List[str] = []
                for x in range(w):
                    s = x / w_denom
                    r, g, b = colorsys.hsv_to_rgb(hue, s, v)
                    row_colors.append(f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}")
                rows.append("{" + " ".join(row_colors) + "}")
            img.put(" ".join(rows))
        self._sv_photo = img
        self.canvas_sv.image = img
        self.canvas_sv.delete("all")
        self.canvas_sv.create_image(0, 0, anchor="nw", image=img)

    def _render_gradient_preview(self) -> None:
        w, h = 46, 34
        c1, c2 = self.stop_colors[0], self.stop_colors[1]
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        if Image is not None and ImageTk is not None:
            raw = bytearray(w * h * 3)
            denom = max(1, h - 1)
            idx = 0
            for y in range(h):
                t = y / denom
                r = int(r1 + (r2 - r1) * t)
                g = int(g1 + (g2 - g1) * t)
                b = int(b1 + (b2 - b1) * t)
                for _ in range(w):
                    raw[idx] = r
                    raw[idx + 1] = g
                    raw[idx + 2] = b
                    idx += 3
            im = Image.frombytes("RGB", (w, h), bytes(raw))
            img = ImageTk.PhotoImage(im, master=self)
        else:
            img = tk.PhotoImage(master=self, width=w, height=h)
            rows = []
            denom = max(1, h - 1)
            for y in range(h):
                t = y / denom
                r = int(r1 + (r2 - r1) * t)
                g = int(g1 + (g2 - g1) * t)
                b = int(b1 + (b2 - b1) * t)
                hx = f"#{r:02x}{g:02x}{b:02x}"
                rows.append("{" + " ".join([hx] * w) + "}")
            img.put(" ".join(rows))
        self._grad_photo = img
        self.canvas_grad_preview.image = img
        self.canvas_grad_preview.delete("all")
        self.canvas_grad_preview.create_image(0, 0, anchor="nw", image=img)

    def _sync_ui_from_hsv(self) -> None:
        t = self.theme
        r_f, g_f, b_f = colorsys.hsv_to_rgb(self._h, self._s, self._v)
        r_i, g_i, b_i = int(round(r_f * 255)), int(round(g_f * 255)), int(round(b_f * 255))
        hex_c = f"#{r_i:02x}{g_i:02x}{b_i:02x}"
        self.stop_colors[self.active_stop] = hex_c

        cx = int(round(self._s * (self.SV_W - 1)))
        cy = int(round((1.0 - self._v) * (self.SV_H - 1)))
        self.canvas_sv.delete("cursor")
        ring_color = best_contrast_fg(hex_c)
        self.canvas_sv.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, outline=ring_color, width=2, tags="cursor")

        hy = int(round(self._h * (self.HUE_H - 1)))
        self.canvas_hue.delete("cursor")
        self.canvas_hue.create_rectangle(0, max(0, hy - 2), self.HUE_W, min(self.HUE_H, hy + 2), outline="#ffffff", width=2, tags="cursor")

        self.lbl_swatch_active.configure(bg=hex_c)
        self.var_hex.set(hex_c.upper())
        self.lbl_rgb.configure(text=f"RGB: {r_i}, {g_i}, {b_i}")
        self._render_gradient_preview()

        accent_fg = best_contrast_fg(t["misora_pink"])
        inactive_fg = best_contrast_fg(t["bg_editor"], t["fg_text"], "#ffffff")
        if self.active_stop == 0:
            self.btn_stop0.configure(bg=t["misora_pink"], fg=accent_fg)
            self.btn_stop1.configure(bg=t["bg_editor"], fg=inactive_fg)
        else:
            self.btn_stop0.configure(bg=t["bg_editor"], fg=inactive_fg)
            self.btn_stop1.configure(bg=t["misora_pink"], fg=accent_fg)

        c0_code = self.stop_colors[0][1:].upper()
        c1_code = self.stop_colors[1][1:].upper()
        self.btn_insert_single.configure(text=f"Insert [{c0_code}]")
        self.btn_insert_grad.configure(text=f"Insert [{c0_code},{c1_code}]")

        self.app._set_ribbon_colors(self.stop_colors[0], self.stop_colors[1])

    def _on_sv_drag(self, event: tk.Event) -> None:
        x = max(0, min(self.SV_W - 1, event.x))
        y = max(0, min(self.SV_H - 1, event.y))
        self._s = x / max(1, self.SV_W - 1)
        self._v = 1.0 - (y / max(1, self.SV_H - 1))
        self._sync_ui_from_hsv()

    def _on_hue_drag(self, event: tk.Event) -> None:
        y = max(0, min(self.HUE_H - 1, event.y))
        self._h = y / max(1, self.HUE_H - 1)
        self._render_sv_map()
        self._sync_ui_from_hsv()

    def _set_color_hex(self, hex_str: str) -> None:
        val = hex_str.strip()
        if not val.startswith("#"):
            val = "#" + val
        if not HEX_COLOR_RE.match(val):
            return
        val = val.lower()
        r = int(val[1:3], 16) / 255.0
        g = int(val[3:5], 16) / 255.0
        b = int(val[5:7], 16) / 255.0
        self._h, self._s, self._v = colorsys.rgb_to_hsv(r, g, b)
        self._render_sv_map()
        self._sync_ui_from_hsv()

    def _on_hex_entry_commit(self, _event: Optional[tk.Event] = None) -> None:
        val = self.var_hex.get().strip()
        if not val.startswith("#"):
            val = "#" + val
        if HEX_COLOR_RE.match(val):
            self._set_color_hex(val)
        else:
            self.var_hex.set(self.stop_colors[self.active_stop].upper())

    def _toggle_eyedropper(self) -> None:
        if self._eyedropper_active:
            self._stop_eyedropper()
            return

        if sys.platform != "win32":
            self.lbl_eye_hint.configure(text="Screen eyedropper requires Windows; use map or swatches.")
            return

        self._eyedropper_active = True
        self._waiting_for_release = True
        self.btn_eyedropper.configure(
            text="Sampling... (Click)",
            bg=self.theme["misora_pink"],
            fg=best_contrast_fg(self.theme["misora_pink"]),
        )
        self.lbl_eye_hint.configure(text="Move cursor over any pixel on screen & Left-Click (Esc to cancel).")
        self._poll_eyedropper()

    def _poll_eyedropper(self) -> None:
        if not self._eyedropper_active or not self.winfo_exists():
            return

        try:
            user32 = ctypes.windll.user32
            gdi32 = ctypes.windll.gdi32

            pt = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))

            sampled_hex = None
            if ImageGrab is not None:
                try:
                    px = ImageGrab.grab(bbox=(pt.x, pt.y, pt.x + 1, pt.y + 1)).getpixel((0, 0))
                    sampled_hex = f"#{px[0]:02x}{px[1]:02x}{px[2]:02x}"
                except Exception:
                    pass

            if not sampled_hex:
                # Strict 64-bit safe signatures fallback
                user32.GetDC.restype = wintypes.HDC
                user32.GetDC.argtypes = [wintypes.HWND]
                user32.ReleaseDC.restype = ctypes.c_int
                user32.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
                gdi32.GetPixel.restype = wintypes.COLORREF
                gdi32.GetPixel.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int]

                hdc = user32.GetDC(0)
                try:
                    colorref = gdi32.GetPixel(hdc, pt.x, pt.y)
                finally:
                    user32.ReleaseDC(0, hdc)

                if colorref != -1 and colorref != 0xFFFFFFFF:
                    r = colorref & 0xFF
                    g = (colorref >> 8) & 0xFF
                    b = (colorref >> 16) & 0xFF
                    sampled_hex = f"#{r:02x}{g:02x}{b:02x}"

            if sampled_hex:
                self._set_color_hex(sampled_hex)

            if user32.GetAsyncKeyState(0x1B) & 0x8000:
                self._stop_eyedropper()
                return

            mouse_down = bool(user32.GetAsyncKeyState(0x01) & 0x8000)
            if self._waiting_for_release:
                if not mouse_down:
                    self._waiting_for_release = False
            else:
                if mouse_down:
                    self._stop_eyedropper()
                    self.lift()
                    return
        except Exception:
            self._stop_eyedropper()
            return

        self._eyedropper_after_id = self.after(35, self._poll_eyedropper)

    def _stop_eyedropper(self) -> None:
        self._eyedropper_active = False
        self._waiting_for_release = False
        if self._eyedropper_after_id is not None:
            try:
                self.after_cancel(self._eyedropper_after_id)
            except Exception:
                pass
            self._eyedropper_after_id = None
        if self.winfo_exists():
            self.btn_eyedropper.configure(
                text="💧 Eyedropper",
                bg=self.theme["bg_editor"],
                fg=best_contrast_fg(self.theme["bg_editor"], self.theme["fg_text"], "#ffffff"),
            )
            self.lbl_eye_hint.configure(text="")

    def _commit_single_color(self) -> None:
        self._stop_eyedropper()
        code = self.stop_colors[0][1:].upper()
        self.app.apply_ngui_wrapper(f"[{code}]", "[-]")
        self._on_close()

    def _commit_gradient_color(self) -> None:
        self._stop_eyedropper()
        c0 = self.stop_colors[0][1:].upper()
        c1 = self.stop_colors[1][1:].upper()
        self.app.apply_ngui_wrapper(f"[{c0}-{c1}]", "[-]")
        self._on_close()

    def _on_escape(self, _event: Optional[tk.Event] = None) -> None:
        if self._eyedropper_active:
            self._stop_eyedropper()
        else:
            self._on_close()

    def _on_close(self) -> None:
        self._stop_eyedropper()
        safe_grab_release(self)
        try:
            if hasattr(self, "app") and getattr(self.app, "_color_picker_win", None) is self:
                self.app._color_picker_win = None
            self._sv_photo = None
            self._hue_photo = None
            self._grad_photo = None
            if hasattr(self, "canvas_grad_preview"):
                self.canvas_grad_preview.image = None
        except Exception:
            pass
        self.destroy()


def safe_grab_release(dialog: Optional[tk.Toplevel]) -> None:
    """Safely release modal grab on a Toplevel dialog before destruction (Rule 3, S8a)."""
    if dialog is not None:
        try:
            if dialog.winfo_exists():
                dialog.grab_release()
        except Exception:
            pass


def write_atomic_utf8(
    path: Union[str, Path],
    content: str,
    encoding: str = "utf-8",
    has_bom: bool = False,
    newline: Optional[str] = None,
) -> None:
    """Write text content atomically: delegates to write_atomic_encoded (S3 / S8b-3)."""
    write_atomic_encoded(path, content, encoding=encoding, has_bom=has_bom, newline=newline)


def _get_box_uid(box: Any) -> Optional[int]:
    """Get runtime UID from a Box, falling back to its primary segment record UID (S06 / BUG-12)."""
    if box is None:
        return None
    uid = getattr(box, "uid", None)
    if uid is not None and uid != 0:
        return uid
    if hasattr(box, "segs") and box.segs and getattr(box.segs[0], "record", None):
        return getattr(box.segs[0].record, "uid", None)
    return uid


def compute_stable_lock_key(box_ordinal: int, original_jp_text: str) -> Tuple[int, str]:
    """Compute stable lock identity (box_ordinal, sha256(original_jp_text)) (S06 / BUG-12 / Invariant 6)."""
    return (box_ordinal, hashlib.sha256(original_jp_text.encode("utf-8")).hexdigest())


def get_document_stable_locks(
    doc: Any,
    locked_uids: Set[int],
    original_jp_by_uid: Dict[int, str],
) -> List[Tuple[int, str]]:
    """Extract list of stable lock keys (box_ordinal, sha256(jp)) for locked boxes in doc."""
    if not doc or not getattr(doc, "boxes", None):
        return []
    stable_locks: List[Tuple[int, str]] = []
    for i, box in enumerate(doc.boxes):
        b_uid = _get_box_uid(box)
        if b_uid is not None and b_uid in locked_uids:
            jp_text = original_jp_by_uid.get(b_uid, box.clean_text)
            stable_locks.append(compute_stable_lock_key(i, jp_text))
    return stable_locks


def restore_stable_locks(
    doc: Any,
    stable_locks: Iterable[Tuple[int, str]],
    original_jp_by_uid: Optional[Dict[int, str]] = None,
) -> Tuple[Set[int], List[Tuple[int, str]]]:
    """Restore stable lock keys against doc.boxes, returning (matched_uids, unresolved_locks) (S06 / BUG-12)."""
    matched_uids: Set[int] = set()
    unresolved: List[Tuple[int, str]] = []
    if not doc or not getattr(doc, "boxes", None):
        return matched_uids, list(stable_locks)

    orig_map = original_jp_by_uid or {}
    for ordinal, expected_hash in stable_locks:
        if 0 <= ordinal < len(doc.boxes):
            box = doc.boxes[ordinal]
            b_uid = _get_box_uid(box)
            jp_text = orig_map.get(b_uid, box.clean_text)
            actual_hash = hashlib.sha256(jp_text.encode("utf-8")).hexdigest()
            if actual_hash == expected_hash:
                if b_uid is not None:
                    matched_uids.add(b_uid)
                continue
        unresolved.append((ordinal, expected_hash))
    return matched_uids, unresolved


class MisoraApp(tk.Tk):
    """Main Application Window for Misora: Unity3D Revision Tool."""

    def __init__(self, initial_path: Optional[str] = None, show_splash: bool = True, _progress_callback=None, restore_session: bool = True):
        super().__init__()
        self.title("Misora Editor: Unity3D Revision Tool & Story Editor")
        self.geometry("1280x820")
        self.minsize(980, 620)
        self.withdraw()   # stay hidden until splash closes or ready

        splash = None
        if show_splash and _progress_callback is None:
            try:
                splash = MisoraSplashScreen(parent=self)
                splash.process_events()
            except Exception:
                splash = None

        def _rpt(val: float, msg: str = ""):
            if splash:
                try:
                    splash.set_progress(val, msg)
                    splash.process_events()
                except Exception:
                    pass
            elif _progress_callback:
                try:
                    _progress_callback(val, msg)
                except Exception:
                    pass

        _rpt(0.10, "Loading core modules…")
        # Central Logger initialized early so startup & config load are recorded
        self.logger = MisoraLogger(DEBUG_LOG_PATH)
        self._install_exception_hooks()

        # Path config & persistent workspace states (initialized before _load_user_prefs)
        self.backup_folder: Optional[Path] = None
        self.project_folder: Optional[Path] = None
        self.bepinex_project_folder: Optional[Path] = None  # Backward-compatible alias
        self.datamine_exe: Optional[Path] = None
        self.external_editor_path: Optional[Path] = None
        self.notepadpp_path: Optional[Path] = None
        self._datamine_confirm_skip: bool = False
        self._left_dock_tab: str = "search"
        self._left_dock_width: int = 340
        self._dock_collapsed: bool = False
        self.show_line_numbers: bool = True
        self.show_column_ruler: bool = False
        self.mtl_config: MTLConfig = MTLConfig()
        self._translator_dialog: Optional[Any] = None
        self._side_drawer_pinned: bool = False
        self.dnd_batch_threshold: int = 10
        self.dnd_size_threshold_mb: float = 25.0
        self.dnd_filter_binary: bool = True

        _rpt(0.25, "Loading saved preferences…")
        # Load persistent user preferences (fonts, theme colors, paths, mtl settings)
        self.prefs: Dict[str, Any] = self._load_user_prefs()
        self.theme: Dict[str, str] = dict(self.prefs["theme"])
        THEME.update(self.theme)

        dbg_cfg = self.prefs.get("debug", {})
        self.logger.configure(
            level_name=dbg_cfg.get("level", "Info"),
            log_to_file=bool(dbg_cfg.get("log_to_file", False)),
            categories=dbg_cfg.get("categories"),
            log_file_path=DEBUG_LOG_PATH,
        )

        self.configure(bg=self.theme["bg_dark"])
        apply_window_icon(self)

        # State Variables
        self.current_file_path: Optional[Path] = None
        self.current_doc: Optional[StoryDocument] = None
        self.current_unity_env: Any = None
        self.current_text_obj: Any = None
        self.current_box_idx: int = 0
        self.is_box0_active: bool = False
        self.var_box0_title: tk.StringVar = tk.StringVar(master=self, value="")
        self.var_box0_subtitle: tk.StringVar = tk.StringVar(master=self, value="")
        self.is_bundle_file: bool = False
        self.is_dirty: bool = False
        self._plain_text_content: str = ""
        self.xuat_search_roots: List[Path] = []
        self.selected_search_folder: Optional[Path] = None

        # Steps 3-4: Undo journal & opened-files cache
        self.undo_journal: MasterUndoJournal = MasterUndoJournal()
        self.open_documents: Dict[Path, Any] = {}   # path -> open doc info dict

        # Active NGUI Ribbon color state
        self._active_ngui_color: str = "#7b42bc"
        self._active_ngui_grad_end: str = "#ff7da7"
        self._color_picker_win: Optional[NguiColorPickerPopup] = None

        # Multi-box edit tracking for Continuous View & XUAT sync
        self._original_box_texts: Dict[int, str] = {}
        self._modified_boxes: Set[int] = set()
        # S2: Per-document saved-state checkpoint map (SHA-256 fingerprints keyed by resolved str(path))
        self._saved_state_checkpoints: Dict[str, str] = {}
        self._cont_header_spans: Dict[int, Tuple[str, str]] = {}
        self._suppress_continuous_events: bool = False
        self._card_widgets: Dict[int, Dict[str, Any]] = {}
        self.var_select_box_mode: tk.BooleanVar = tk.BooleanVar(master=self, value=False)
        self._selected_boxes: Set[int] = set()
        self._locked_boxes: Set[int] = set()
        self._locked_box_uids: Set[int] = set()
        self._modified_box_uids: Set[int] = set()
        self._original_jp_by_uid: Dict[int, str] = {}
        self._box_clipboard: List[Any] = []
        self._is_speaker_pinned: bool = False
        self._icon_cache: dict = {}
        self._cont_resize_job: Optional[str] = None

        # S8b-1: Toast & Status Notification Manager state
        self._toast_queue: collections.deque = collections.deque()
        self._toast_active: bool = False
        self._toast_after_id: Optional[str] = None
        self._status_after_id: Optional[str] = None
        self._default_status_text: str = "Ready. Drag & Drop or open a .unity3d bundle or folder to begin."
        self._toast_widget: Optional[tk.Label] = None

        # Side Drawer (Customization & NGUI Glossary) state
        self._side_drawer_visible: bool = False
        self._side_drawer_tab: str = "customize"
        self._theme_swatch_buttons: Dict[str, tk.Button] = {}
        self._theme_hex_vars: Dict[str, tk.StringVar] = {}
        self._glossary_line_map: Dict[int, int] = {}
        self._selected_glossary_idx: int = 0
        self._filtered_glossary_items: List[Dict[str, str]] = list(NGUI_GLOSSARY_ITEMS)

        # Native Win32 Drag & Drop references (kept alive to prevent GC)
        self._wndprocs: Dict[int, Tuple[Any, Any]] = {}
        self._drop_hwnd: Any = None
        self._dnd_in_progress: bool = False

        # Debug Console state
        self._console_visible: bool = bool(dbg_cfg.get("console_visible", False))
        self.var_console_visible = tk.BooleanVar(master=self, value=self._console_visible)
        self.var_log_to_file = tk.BooleanVar(master=self, value=bool(dbg_cfg.get("log_to_file", False)))
        self.var_log_level = tk.StringVar(master=self, value=str(dbg_cfg.get("level", "Info")))
        self.var_console_autoscroll = tk.BooleanVar(master=self, value=True)
        self.var_log_categories: Dict[str, tk.BooleanVar] = {}
        saved_cats = dbg_cfg.get("categories", {}) if isinstance(dbg_cfg.get("categories"), dict) else {}
        for cat in LOG_CATEGORIES:
            enabled = True if cat == ALWAYS_ON_CATEGORY else bool(saved_cats.get(cat, True))
            self.var_log_categories[cat] = tk.BooleanVar(master=self, value=enabled)

        # Background search worker & highlighting state
        self.search_engine = ProjectSearchEngine()
        self.sync_manager = XUnitySyncManager()
        self.search_queue: queue.Queue = queue.Queue()
        self.search_cancel_flag: bool = False
        self.active_search_results: List[SearchResult] = []
        self.active_search_options: Optional[SearchOptions] = None
        self.search_file_groups: List[Dict[str, Any]] = []
        self._file_group_lookup: Dict[str, Dict[str, Any]] = {}
        self._result_line_map: Dict[int, Tuple[str, Any]] = {}
        self._result_idx_to_line: Dict[int, int] = {}
        self._selected_result_idx: Optional[int] = None

        # Auto-detect project paths
        self._detect_environment()

        _rpt(0.55, "Building UI layout…")
        # Build UI
        self._apply_styles()
        self._build_menu()
        self._build_search_bar()

        _rpt(0.70, "Initializing editor panels…")
        self._build_main_panels()
        self._build_side_drawer()
        self._build_status_bar()
        self._bind_shortcuts()

        _rpt(0.85, "Applying theme and fonts…")
        # Sync initial widget fonts & colors with saved preferences
        self._apply_theme_and_fonts_live(save=False)

        # Flush config on exit and unhook Win32 WNDPROC cleanly
        self.protocol("WM_DELETE_WINDOW", self._on_app_exit)
        self.bind("<Destroy>", self._on_root_destroy)

        _rpt(0.85, "Enabling drag & drop…")
        # Enable native OS Drag & Drop safely on the outer frame HWND
        self._init_drag_and_drop()

        # Start periodic poll for background tasks
        self._search_poll_job = self.after(100, self._process_search_queue)

        # Restore saved window geometry and view toggles (Bug #2 / S9c)
        if hasattr(self, "_saved_geometry") and self._saved_geometry:
            try:
                sw = self.winfo_screenwidth()
                sh = self.winfo_screenheight()
                safe_geom = sanitize_window_geometry(self._saved_geometry, sw, sh)
                self.geometry(safe_geom)
            except Exception:
                pass
        if hasattr(self, "_saved_continuous_view") and hasattr(self, "var_continuous_view"):
            if self._saved_continuous_view:
                self.var_continuous_view.set(True)
                self._on_toggle_continuous_view()
            else:
                self.var_continuous_view.set(False)
        if hasattr(self, "_saved_sync_xuat") and hasattr(self, "var_sync_xuat"):
            self.var_sync_xuat.set(self._saved_sync_xuat)

        # Restore previous session files during splash so startup never freezes
        if initial_path and os.path.exists(initial_path):
            _rpt(0.92, f"Opening {Path(initial_path).name}…")
            try:
                self.open_file(initial_path)
            except Exception:
                pass
        elif restore_session and hasattr(self, "_saved_opened_files") and self._saved_opened_files:
            tot = len(self._saved_opened_files)
            for idx, fp in enumerate(self._saved_opened_files):
                if fp.exists():
                    prog = 0.85 + (0.13 * ((idx + 1) / max(1, tot)))
                    _rpt(prog, f"Restoring ({idx + 1}/{tot}): {fp.name}…")
                    try:
                        self.open_file(fp)
                    except Exception:
                        pass
            if hasattr(self, "_saved_active_file") and self._saved_active_file and self._saved_active_file.exists():
                try:
                    self.open_file(self._saved_active_file)
                except Exception:
                    pass

        _rpt(1.00, "Ready!")
        self.logger.info("UI / Theme / Config", f"Misora initialized. Config path: {CONFIG_PATH}")

        if splash:
            splash.close()

        # Reveal the main window (was hidden during splash)
        self.deiconify()

    def get_icon(self, name: str, size: Tuple[int, int] = (18, 18)) -> Optional[tk.PhotoImage]:
        """Retrieve an illustrated icon PhotoImage bound to this MisoraApp Tk instance."""
        return get_icon(name, size, master=self)

    def safe_clipboard_get(self) -> str:
        """Read text from clipboard with retry on TclError and CRLF/CR normalization (AGENTS.md Rule 14)."""
        for _ in range(5):
            try:
                val = self.clipboard_get()
                return val.replace("\r\n", "\n").replace("\r", "\n")
            except tk.TclError:
                time.sleep(0.05)
            except Exception:
                break
        return ""

    def safe_clipboard_set(self, text: str) -> None:
        """Write text to clipboard with retry on TclError (AGENTS.md Rule 14)."""
        for _ in range(5):
            try:
                self.clipboard_clear()
                self.clipboard_append(text)
                self.update_idletasks()
                return
            except tk.TclError:
                time.sleep(0.05)
            except Exception:
                break

    # -------------------------------------------------------------------------
    # Global Exception Hooks & Exit Lifecycle
    # -------------------------------------------------------------------------
