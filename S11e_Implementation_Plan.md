# S11e Implementation Plan — Rev 3 (`v1.4.15`) — UI Polish, Branding & Usability (`Q-03`, `Q-05`, `Q-13`..`Q-17`)

**Status:** `/plan` Rev 3 — ready for GPT-6 & Qwen review and explicit Project Lead **Proceed** (zero repository files modified).
**Version Target:** `__init__.__version__` `"1.4.14"` → `"1.4.15"` (`v1.5.0` remains strictly **ON HOLD**).

---

## 0. Measured Baseline & Confirmed Rulings (Read Directly From Disk)

- **Committed S11d `HEAD`:** `da74305dda9fc09b669f78258357e4e5b0e0782e`
- **Pre-existing local working tree status (`git status --short`):**
  - ` M assets/icons/BoxInsert.png`
  - `?? assets/icons/BoxReplace.png`
  - `?? assets/icons/BoxSelectNone.png`
  - `?? assets/icons/BoxSelectOne.png`
- **Python Version:** `Python 3.12.10` (Windows)
- **Test Discovery Baseline:** `countTestCases() == 466` (`423 PASS, 35 SKIP, 6 pre-existing FAIL, 2 pre-existing ERROR`)
- **Canonical Module Paths Confirmed:**
  - Splash module: `assets/splash.py` (there is NO root `splash.py`).
  - Icon manager: `assets/icon.py` (`get_icon`, `prune_icon_cache`, `clear_icon_cache`, `_ICON_CACHE`, `MAX_ICON_CACHE = 128`).
  - Launcher (`misora.bat`): Lines 7–11 already pin `py -3.12 "%~dp0misora.py" %*` first, falling back only if Python 3.12 is absent. **No edits needed to `misora.bat` in S11e.**
- **Project Lead Confirmations Recorded:**
  1. **`BoxInsert.png` vs `BoxReplace.png`:** Wire `BoxInsert.png` → Insert (`btn_ins`) and `BoxReplace.png` → Replace (`btn_rep`) inside `_show_box_paste_mode_dialog()`, keeping `actions_bar` at its existing 4 box buttons (no 5th `btn_box_replace` button) to preserve `960x720` responsive width compliance.
  2. **Menu Dedup:** Remove BOTH the top-level `NGUI Glossary` cascade (moving `Reset Color Tag ([-])` to `Edit`) AND `Help > NGUI & Ruby Glossary (F1)`, leaving `View > Toggle NGUI Glossary Panel (F1)` as the single canonical entry and `Help` with `Support the Creator...` + `About Misora: Story Editor`.

---

## 1. File Ownership Boundaries (Post-Proceed Only)

### Allowed Files
- `__init__.py` (`"1.4.14"` → `"1.4.15"`)
- `misora.py` (`Q-03`, `Q-05` wiring, `Q-13` About branding, `Q-14` Support EN + ~600px GIF, `Q-15` icon & 3-icon selection trio wiring, `Q-16` Main Menu dedup, `Q-17` 3-layer tooltips)
- `assets/splash.py` (`Q-05` non-blocking splash event pumping & lifecycle, `Q-13` `PriconneRe:TL` bold/larger + `Cornelia` branding, single-source `_VERSION` parity)
- `assets/icon.py` (`Q-15` DPI-aware Pillow `LANCZOS` load-time resizing & `PhotoImage` cache)
- `CHANGELOG.md` & `PROJECT_STATE.md`
- `tests/test_v15_s11e_polish_splash_menu_tooltips.py` (**NEW** — 7 failing-first probes + 2 regression guards = 9 tests)
- Existing test migrations (strictly equal-strength, `0` extra `test_*` methods, zero assertion weakening):
  - `tests/test_v15_s11d_import_ux_productivity.py` (`Q-07` tri-state text assertions → 3-icon trio + accessible fallback + tooltip + `Q-10` icon checks)
  - `tests/test_v15_s05_speaker_console_about.py` (`test_probe_5` Indonesian caption / `240.0` scale → English `PriconneRe:TL`/`Cornelia` caption + `~600px` GIF scale + About branding)

### Strictly Forbidden & Asset Commit Ruling
- **Forbidden for Antigravity to Modify:** `core/*.py`, `requirements.txt`, `misora_config.json`, `backups/`, and all PNG artwork under `assets/icons/` (strictly read-only source assets; load-time resize via `assets/icon.py` only), plus zero `git commit`, `git push`, `git reset`, or destructive git commands.
- **Local Working-Tree Asset Commit Note:** The 4 pre-existing local working-tree icon files (`assets/icons/BoxInsert.png`, `assets/icons/BoxReplace.png`, `assets/icons/BoxSelectNone.png`, `assets/icons/BoxSelectOne.png`) stay untouched by Antigravity and will be included by the Project Lead in the S11e local commit per Qwen/ChatGPT rulings (`git push` remains excluded; `v1.5.0` remains **ON HOLD**).

---

## 2. `Q-03` — Per-Widget Word-Wrap Audit & `clean_scroll_x` Mutual Exclusion (`misora.py`)

### 2.1 Existing Test Audit (`tests/`)
Direct grep across all `tests/test_*.py` confirmed:
- `txt_dialogue.cget("wrap")`: **0 hits** (all 4 `wrap` hits on dialogue widgets assert `self.app.txt_dialogue_preview.cget("wrap") == "none"` across `test_p3_s18`, `test_v15_s03`, `test_v15_s08`, `test_v15_s11b`).
- `_auto_resize_dialogue_box`: **1 hit** (`test_s4_view_model_sync.py:234`, which mocks `app._auto_resize_dialogue_box = MagicMock()` and does not depend on the internal line-estimation formula).
- `clean_editor_row`: **0 hits**.
- `_on_toggle_line_numbers`: tested directly by `test_misora_ui_integration.py::test_08_line_numbers_and_ruler_toggles` (`L183-208`), which toggles `var_show_line_numbers` OFF/ON and asserts `self.app._is_widget_packed(self.app.gutter_clean)`.

### 2.2 Complete Audit of All 22 `tk.Text(...)` Widgets in `misora.py`

| # | Line | Symbol / Widget | Current `wrap` | Target `wrap` | Rationale / Action |
|---|---|---|---|---|---|
| 1 | `L1572` | `_AllScriptPoolCard.txt_body` | `"none"` | `"none"` | Keep (`54d x 3` horizontal bleed + Shift+Wheel/arrow scroll) |
| 2 | `L1656` | `_AllScriptBox0Card.txt_summary` | `"word"` | `"word"` | Keep (full-width auto-wrapped Box 0 block) |
| 3 | `L5280` | `MisoraApp.txt_results` | `"none"` | `"none"` | Keep (search results pane with horizontal scrollbar) |
| 4 | `L5366` | `MisoraApp.txt_opened_files` | `"none"` | `"none"` | Keep (opened files list with horizontal scrollbar) |
| 5 | `L6147` | `MisoraApp.gutter_clean` | `"none"` | `"none"` | Keep (line number gutter) |
| **6** | **`L6167`** | **`MisoraApp.txt_dialogue`** | **`"word"`** | **`"none"`** | **CHANGE `"word"` → `"none"`** (see §2.3 below) |
| 7 | `L6209` / `L7675` | `MisoraApp.txt_dialogue_preview` | `"none"` | `"none"` | Keep (visible bleed in Dialogue Preview) |
| 8 | `L6348` | `MisoraApp.txt_box0_summary` | `"word"` | `"word"` | Keep (Box 0 Synopsis editor, U-18 exempt) |
| 9 | `L6418` | `MisoraApp.gutter_cont` | `"none"` | `"none"` | Keep (legacy fallback gutter) |
| 10 | `L6436` | `MisoraApp.txt_continuous` | `"word"` | `"word"` | Keep (plain-text fallback pane) |
| 11 | `L6456` | `MisoraApp.txt_all_script` | `"word"` | `"word"` | Keep (retired unmapped Technique A widget) |
| 12 | `L6606` | `MisoraApp.txt_quick_edit` | `"none"` | `"none"` | Keep (S11c `Q-22` unified Quick Edit with `qe_scroll_x`) |
| 13 | `L6719` | `MisoraApp.txt_raw` | `"none"` | `"none"` | Keep (Raw Commands v2 code view with `raw_scroll_x`) |
| 14 | `L8246` | `MisoraApp.txt_glossary` | `"word"` | `"word"` | Keep (NGUI Glossary drawer) |
| 15 | `L17200` | `MisoraApp.txt_mtl_all_list` | `"word"` | `"word"` | Keep (All Script MTL list) |
| 16 | `L17228` | `MisoraApp.txt_mtl_all_scratchpad` | `"word"` | `"word"` | Keep (All Script MTL scratchpad) |
| 17 | `L17444` | `MisoraApp._rebuild_mtl_drawer_cards` `scratch` | `"word"` | `"word"` | Keep (per-engine MTL scratchpads) |
| 18 | `L20786` | `ImportFromXUATDialog` `txt_left` | `wrap_mode` (`"none"` / `"word"` for Synopsis) | Keep | Keep (`1x54d` / `3x54d` = `"none"`; `summary` = `"word"`) |
| 19 | `L20827` | `ImportFromXUATDialog` `txt_right` | `wrap_mode` (`"none"` / `"word"` for Synopsis) | Keep | Keep (`1x54d` / `3x54d` = `"none"`; `summary` = `"word"`) |
| 20 | `L22928` | `AIPromptSettingsDialog.txt_prompt` | `"word"` | `"word"` | Keep (AI prompt header/notes editor) |
| 21 | `L23063` | `TranslatorAssistantDialog.txt_orig` | `"word"` | `"word"` | Keep (floating MTL original text) |
| 22 | `L23081` | `TranslatorAssistantDialog.txt_trans` | `"word"` | `"word"` | Keep (floating MTL translated text) |

### 2.3 Strictly `pack`-Managed `clean_editor_row` + `clean_scroll_x` Mutual Exclusion (`misora.py`)
Live inspection of `_on_toggle_line_numbers()` (`misora.py:7291-7308`) confirms `self.clean_editor_row` MUST remain strictly **`pack`-managed** (NEVER `.grid()`, which would trigger a `TclError` when `gutter_clean` toggles!):
```python
# misora.py:7296-7308 (verified live on disk)
        # Clean View gutter
        if hasattr(self, "gutter_clean"):
            if visible:
                if hasattr(self, "txt_dialogue") and not self._is_widget_packed(self.gutter_clean):
                    try:
                        self.gutter_clean.pack(before=self.txt_dialogue, side="left", fill="y", padx=(0, 2))
                    except Exception:
                        self.gutter_clean.pack(side="left", fill="y", padx=(0, 2))
                self._update_gutter_clean()
            else:
                if self._is_widget_packed(self.gutter_clean):
                    self.gutter_clean.pack_forget()
```
All other `clean_editor_row` callers (`L6142-6186`, `L7350-7352` `ruler_clean.pack(before=self.clean_editor_row)`, `L7551-7556` `_hide_dialogue_preview_and_restore_editor`, `L9797-9798` Box 0, `L9823-9824` Dialogue Preview) also use `.pack()` / `.pack_forget()` exclusively.

Therefore, inside `self.clean_editor_row` (`L6142-6186`), keep 100% `pack` geometry:
1. Pack `self.clean_scroll_x = tk.Scrollbar(self.clean_editor_row, orient="horizontal")` **first** via `self.clean_scroll_x.pack(side="bottom", fill="x")`.
2. Pack `self.gutter_clean` (`side="left", fill="y", padx=(0, 2)`) when `self.show_line_numbers` is True.
3. Pack `self.txt_dialogue` (`wrap="none"`, `xscrollcommand=self.clean_scroll_x.set`) via `self.txt_dialogue.pack(side="left", fill="both", expand=True)` and configure `self.clean_scroll_x.config(command=self.txt_dialogue.xview)`.
- **Guarantees:**
  - Zero `pack`-vs-`grid` conflict in `_on_toggle_line_numbers()` (`gutter_clean.pack(before=self.txt_dialogue, side="left", fill="y", padx=(0, 2))` and `gutter_clean.pack_forget()` work identically, and `test_misora_ui_integration::test_08` passes untouched).
  - `self.clean_scroll_x` is a direct child of `self.clean_editor_row`, so `_update_views()` (`L9797-9798`, `L9823-9824`) and `_hide_dialogue_preview_and_restore_editor()` (`L7547-7556`) hide/show `clean_scroll_x` atomically — impossible to orphan a horizontal scrollbar on Box 0 or Dialogue Preview.
- Update `_auto_resize_dialogue_box()` (`L8852`) to count logical `\n`-delimited lines (`len(lines)` instead of `len(ln) // 68` soft-wrap estimation): `target_lines = max(7, min(32, len(lines) + 1))`.

---

## 3. `Q-05` — Full Non-Blocking Splash Startup Lifecycle (`assets/splash.py`, `misora.py`)

### Current Defect
- `MisoraApp.__init__` (`misora.py:2295-2366`) emits duplicate `0.85` (`Applying theme...` and `Enabling drag & drop...`), calls `_rpt(1.00, "Ready!")`, closes `splash`, and calls `self.deiconify()` **before** `_deferred_restore()` even starts.
- `MisoraSplashScreen.process_events()` (`assets/splash.py:176-181`) only calls `self._root.update_idletasks()`, which does not pump Win32 input/paint messages, so Windows can flag `"Not Responding"` during multi-second startup or session bundle restore.

### Planned Changes
1. **`assets/splash.py::MisoraSplashScreen`:**
   - Add `_closed: bool = False` and `_pumping: bool = False` re-entrancy guards.
   - Update `process_events(self)` to guard `if self._closed or self._pumping: return`, verify `self._root.winfo_exists()`, call `self._root.update_idletasks()`, and safely drain pending Tk/Win32 messages non-blockingly via bounded `self._root.tk.dooneevent(_tkinter.DONT_WAIT)` (up to 24 events per tick, never blocking when empty).
   - Guard `set_progress()` against `_closed` / destroyed canvas; make `close()` idempotent (`if self._closed: return`).
2. **`misora.py::MisoraApp.__init__`, `withdraw()`, & `_deferred_restore`:**
   - Store `self._splash = splash` and track `self._caller_withdrew = False` (overriding `withdraw()` to mark `_caller_withdrew = True` when called externally after `__init__`, while calling `super().withdraw()` at `L2015`).
   - Wrap the post-splash initialization body (`L2038-2366`) in `try ... except Exception:` so **any startup exception while `self._splash` is open immediately closes `self._splash`** (`self._splash.close(); self._splash = None`) before re-raising — preventing any orphaned `overrideredirect(True)` topmost splash window.
   - Use strictly monotonic startup progress stages in `__init__`:
     - `0.08` `"Loading core modules…"`
     - `0.22` `"Loading saved preferences…"`
     - `0.40` `"Building UI layout…"`
     - `0.55` `"Initializing editor panels…"`
     - `0.68` `"Applying theme and fonts…"`
     - `0.76` `"Enabling drag & drop…"`
   - **Branch cleanly on splash presence (preserving `test_p3_s12::test_04` `show_splash=False` invariant & `test_misora_ui_integration::test_22` / `test_v15_s05::test_guard_2` single-root compliance!):**
     - When `splash is None` (`show_splash=False`): keep `self.deiconify()` at the end of `__init__` and schedule `self.after_idle(_deferred_restore)` (`['deiconify', 'open_file']` invariant preserved).
     - When `splash is not None` (`show_splash=True`): keep main window `withdraw()`n at the end of `__init__`, show `0.80` `"Restoring workspace…"`, and schedule `self.after_idle(_deferred_restore)`. Inside `_deferred_restore`:
       - Compute restore targets (`initial_path` or `self._saved_opened_files` + `self._saved_active_file`).
       - Advance splash progress monotonically `0.82` → `0.98` per restored item (`f"Restoring file ({idx}/{total}): {name}…"`) and call `splash.process_events()` between items.
       - In `finally:` of `_deferred_restore`: emit `_rpt(1.00, "Ready!")`, close `self._splash` (`self._splash = None`), and call `self.deiconify()` ONLY if `self.winfo_exists()` and `not getattr(self, "_destroyed", False)` and `not getattr(self, "_caller_withdrew", False)` (ensuring `test_misora_ui_integration::test_22`'s `splash_app.withdraw()` stays honored and single `tk.Tk()` root is never duplicated).
   - Ensure `_on_root_destroy()` / `_on_app_exit()` also closes any active `self._splash`.

---

## 4. `Q-13` — `PriconneRe:TL` & Creator `Cornelia` Branding (`assets/splash.py`, `misora.py`)

1. **`assets/splash.py::MisoraSplashScreen.__init__`:**
   - Expand bottom dark glass bar from `80px` (`SPLASH_H - 80`) to `96px` (`SPLASH_H - 96`, keeping `600x400` window size) for clean typography hierarchy:
     - Top row: **`PriconneRe:TL`** (`("Segoe UI", 14, "bold")` + shadow, accent `#e8dbfa`/`#ffffff`) + right-aligned **`Created by Cornelia · v{_VERSION}`** (`("Segoe UI", 9, "bold")`).
     - Middle row: `"Misora: Story Editor"` (`("Segoe UI", 16, "bold")`) + right-aligned `"Priconne Unity3D Story Tool"` (`("Segoe UI", 8)`).
     - Bottom row: `self._msg_id` (`"Starting…"`, `("Segoe UI", 8)`), above the `4px` progress bar.
   - Preserve `_VERSION = _load_app_version()` single-source parity with zero hardcoded version literals.
2. **`misora.py::MisoraApp.on_about` (`L19439-19540`):**
   - Prominently display **`PriconneRe:TL`** (larger & bold: `("Segoe UI", 16, "bold")`, `fg=t["misora_pink"]`) above `"Misora: Story Editor"` (`("Segoe UI", 13, "bold")`).
   - Display `f"v{__version__}"` (preserving single-source `__init__.__version__` parity and `test_v15_s08::test_stress_5` AST rule).
   - Display creator **`Cornelia`** (`"Created by Cornelia · PriconneRe:TL\nMIT License — Built for the Princess Connect! Re:Dive Modding Community."`).
   - Keep `"Support Me"` button text (`test_v15_s05::test_probe_5` L292 compatibility) and `"Close"` button.

---

## 5. `Q-14` — Support the Creator EN + `~600px` GIF (`misora.py`)

1. **English Copy, Titles, & Help Menu Consistency (`misora.py:148-151`, `4987-4992`, `19514`, `19578`):**
   - `SupportMeDialog` window title (`L19578`): `"Support the Creator — Misora: Story Editor"`.
   - `Help` menu item (`Q-16`): `"Support the Creator..."` (`command=self.on_support_me`).
   - `on_about()` launch button (`L19514`): keep `"Support Me"` (preserves `test_v15_s05::test_probe_5` L292 assertion cleanly).
   - Replace `SUPPORT_CAPTION_ID` Indonesian copy with natural, humble English referencing `PriconneRe:TL` and `Cornelia`:
     ```python
     SUPPORT_CAPTION_EN: str = (
         "Thank you for using Misora: Story Editor! I'm Cornelia from PriconneRe:TL — "
         "any support, no matter how small, is deeply appreciated and helps cover development and AI translation costs."
     )
     SUPPORT_CAPTION_ID = SUPPORT_CAPTION_EN  # backwards-compatible attribute alias
     ```
   - Update caption `wraplength` from `420` → `580` to match the `~600px` GIF container.
   - Keep `SHOW_PAYPAL_BUTTON`, `SUPPORT_URL_KOFI`, `SUPPORT_URL_PATREON`, `SUPPORT_URL_PAYPAL`, and `"Links open in your browser. Misora does not process payments."` intact.
2. **`~600px` GIF Scaling with Both Width & Height Screen Clamping (`SupportMeDialog._render_gif_frame`, `L19724-19729`):**
   - `assets/Service.gif` is `600x338`, mode `P`, `n_frames=72`.
   - Bound scaling to BOTH screen width AND screen height so 720p / 125%-DPI displays never clip the caption, Ko-fi/Patreon/PayPal buttons, or Close button off-screen:
     ```python
     sw = self.winfo_screenwidth()
     sh = self.winfo_screenheight()
     screen_max_w = max(320, sw - 80) if sw > 0 else 600
     screen_max_h = max(220, sh - 260) if sh > 0 else 360
     target_w = min(600, screen_max_w)
     scale = min(float(target_w) / max(1, w), float(screen_max_h) / max(1, h))
     ```
   - On `1920x1080` (`100%` DPI), `600x338` renders at exact `600x338`. On `1280x720` (`720p`), `screen_max_h = 460` → `600x338` fits cleanly; on `1280x720` at `125%` DPI (`~576px` logical height), `screen_max_h = 316` → `561x316` fits without clipping bottom buttons.
   - Keep sequential single-`PhotoImage` reuse (`paste(composite)`), `_close_gif_handle()` / `_cleanup_resources()`, and `_render_static_fallback()`.

---

## 6. `Q-15` — Verified Icon Overhaul & Approved 3-Icon Selection Trio (`assets/icon.py`, `misora.py`)

### 6.1 Complete Read-Only Alpha-Pixel Audit of All 53 PNGs in `assets/icons/`

Every PNG under `assets/icons/` was inspected directly on disk via Pillow (`RGBA` alpha channel histogram):

| Filename | Dimensions | Mode | Alpha `(min, max)` | `alpha=0` px | `1..254` px | `255` px | SHA-256 (12) | Status / Role |
|---|---|---|---|---|---|---|---|---|
| `BoxConversation.png` | `600x600` | `RGBA` | `(0, 255)` | 149,879 | 208,210 | 1,911 | `9e20553a0692` | **Parked (unused)** |
| `BoxConversationList.png` | `600x600` | `RGBA` | `(0, 255)` | 27,275 | 13,167 | 319,558 | `33da4f52aeb9` | **All Script** (`cb_cont`) |
| `BoxCopy.png` | `600x600` | `RGBA` | `(0, 255)` | 139,197 | 4,689 | 216,114 | `96dcae566f8d` | **Copy Box** (`btn_box_copy`) |
| `BoxCut.png` | `600x600` | `RGBA` | `(0, 255)` | 138,505 | 5,343 | 216,152 | `7f235c51bc1b` | **Cut Box** (`btn_box_cut`) |
| `BoxD.png` | `600x600` | `RGBA` | `(0, 255)` | 172,674 | 3,868 | 183,458 | `cf8c3e5eb8c4` | **New Box** (`btn_box_new`) |
| `BoxInsert.png` | `600x600` | `RGBA` | `(0, 255)` | 156,853 | 4,234 | 198,913 | `a7e4987b327c` | **Insert** (`btn_ins` in Paste Mode) |
| `BoxPaste.png` | `600x600` | `RGBA` | `(0, 255)` | 134,112 | 4,433 | 221,455 | `82071cfbe076` | **Paste Box** (`btn_box_paste`) |
| `BoxReplace.png` | `600x600` | `RGBA` | `(0, 255)` | 146,598 | 5,161 | 208,241 | `de03381658d6` | **Replace** (`btn_rep` in Paste Mode) |
| `BoxSelectAll.png` | `600x600` | `RGBA` | `(0, 255)` | 192,751 | 126,143 | 41,106 | `43e333c4d7bc` | **Q-07 `"all"` & Q-10 Select All** |
| `BoxSelectNone.png` | `600x600` | `RGBA` | `(0, 255)` | 310,892 | 9,020 | 40,088 | `4edeb88637bf` | **Q-07 `"none"` & Q-10 Deselect All** |
| `BoxSelectOne.png` | `600x600` | `RGBA` | `(0, 255)` | 221,501 | 10,378 | 128,121 | `a5f844fd41e3` | **Q-07 `"partial"` ("Some selected")** |
| `language-translation-icon.png` | `512x512` | `RGBA` | `(0, 255)` | 125,992 | 2,494 | 133,658 | `2639a5e20e30` | **Translate / MTL** (`btn_translate`) |
| `ai.png` | `72x72` | `RGBA` | `(0, 255)` | 1,071 | 105 | 4,008 | `b743f8d0d852` | Existing (`btn_ai_prompt`) |
| `box.png` | `72x72` | `RGBA` | `(0, 255)` | 2,222 | 147 | 2,815 | `112be984f305` | Existing (`cb_sel_box`) |
| `box_copy.png` | `72x72` | `RGBA` | `(0, 255)` | 1,881 | 383 | 2,920 | `5834da767690` | Legacy (superseded by `BoxCopy.png`) |
| `box_cut.png` | `72x72` | `RGBA` | `(0, 255)` | 2,041 | 714 | 2,429 | `af9b2308da39` | Legacy (superseded by `BoxCut.png`) |
| `box_paste.png` | `72x72` | `RGBA` | `(0, 255)` | 1,944 | 423 | 2,817 | `6bb0f493020a` | Legacy (superseded by `BoxPaste.png`) |
| `cancel.png` | `72x72` | `RGBA` | `(0, 255)` | 1,816 | 640 | 2,728 | `0d4ad83cd2a9` | Existing (`btn_cancel`) |
| `caravan_buddy_icon_100101.png` .. `133101.png` (7 files) | `128x128` | `RGBA` | `(0, 255)` | 3,593 | 347 | 12,444 | `f5bf33eb5d76`.. | Existing buddy assets |
| `check.png` | `72x72` | `RGBA` | `(0, 255)` | 32 | 36 | 5,116 | `5ae37edcb286` | Existing asset |
| `close.png` | `72x72` | `RGBA` | `(0, 255)` | 3,228 | 446 | 1,510 | `c6f4fa790e82` | Existing (`btn_close_search`) |
| `copy.png` | `72x72` | `RGBA` | `(0, 255)` | 1,506 | 44 | 3,634 | `e89dd81b812e` | Existing (`btn_copy`) |
| `cut.png` | `72x72` | `RGBA` | `(0, 255)` | 3,420 | 424 | 1,340 | `cc3f2e3c848f` | Existing (`btn_cut`) |
| `eyedropper.png` | `72x72` | `RGBA` | `(0, 255)` | 4,284 | 244 | 656 | `9b28e872b326` | Existing (`btn_eyedropper`) |
| `folder.png` | `72x72` | `RGBA` | `(0, 255)` | 1,520 | 61 | 3,603 | `6d837ffc38ec` | Existing (`btn_open_more`) |
| `kofi.png` | `32x32` | `RGBA` | `(0, 255)` | 150 | 278 | 596 | `f67b785a5df3` | Existing (`SupportMeDialog`) |
| `mtl.png` | `72x72` | `RGBA` | `(0, 255)` | 2,626 | 558 | 2,000 | `071d9ae36a3e` | Legacy (superseded by `language-translation-icon.png`) |
| `nav_next.png` | `72x72` | `RGBA` | `(0, 255)` | 32 | 36 | 5,116 | `cef17dde7a30` | Existing (`btn_next`) |
| `nav_prev.png` | `72x72` | `RGBA` | `(0, 255)` | 32 | 36 | 5,116 | `57be75ca7f4e` | Existing (`btn_prev`) |
| `palette.png` | `72x72` | `RGBA` | `(0, 255)` | 1,861 | 261 | 3,062 | `a86cb0ef251a` | Existing (`btn_color`) |
| `paste.png` | `72x72` | `RGBA` | `(0, 255)` | 2,134 | 97 | 2,953 | `8ef65a98429a` | Existing (`btn_paste`) |
| `patreon.png` | `32x32` | `RGBA` | `(0, 255)` | 150 | 278 | 596 | `5244ef4fec1f` | Existing (`SupportMeDialog`) |
| `paypal.png` | `32x32` | `RGBA` | `(0, 255)` | 150 | 278 | 596 | `97c0bce2aaa7` | Existing (`SupportMeDialog`) |
| `pin.png` | `72x72` | `RGBA` | `(0, 255)` | 2,975 | 249 | 1,960 | `68cc30da33ec` | Existing (`btn_pin_speaker`) |
| `player.png` | `72x72` | `RGBA` | `(0, 255)` | 2,191 | 179 | 2,814 | `72f9b6f004f2` | Existing (`btn_player`) |
| `plus.png` | `72x72` | `RGBA` | `(0, 255)` | 3,812 | 76 | 1,296 | `947d13afeb09` | Legacy (superseded for `btn_box_new` by `BoxD.png`) |
| `preview.png` | `72x72` | `RGBA` | `(0, 255)` | 2,868 | 154 | 2,162 | `8e59427dec39` | Existing (`cb_compiled`) |
| `redo.png` | `72x72` | `RGBA` | `(0, 255)` | 32 | 36 | 5,116 | `e78e290be35d` | Existing (`btn_ribbon_redo`) |
| `refresh.png` | `32x32` | `RGBA` | `(0, 255)` | 681 | 271 | 72 | `ee28f6f38bbf` | Existing (`btn_mtl_refresh_*`) |
| `replace.png` | `72x72` | `RGBA` | `(0, 255)` | 3,742 | 780 | 662 | `50d5f75e114e` | Existing (`btn_replace`) |
| `replace_all.png` | `72x72` | `RGBA` | `(0, 255)` | 3,420 | 1,008 | 756 | `c4959f068668` | Existing (`btn_replace_all`) |
| `revert.png` | `72x72` | `RGBA` | `(0, 255)` | 32 | 36 | 5,116 | `51e3d8f746c1` | Existing (`btn_revert`) |
| `save.png` | `72x72` | `RGBA` | `(0, 255)` | 65 | 40 | 5,079 | `c9cf4ea9c1fc` | Existing (`btn_save`) |
| `search.png` | `72x72` | `RGBA` | `(0, 255)` | 2,277 | 246 | 2,661 | `f111830bd2b2` | Existing (`btn_find`) |
| `select_story.png` | `72x72` | `RGBA` | `(0, 255)` | 1,076 | 51 | 4,057 | `af3448fe7183` | Existing (`btn_sel_story`) |
| `sparkle.png` | `72x72` | `RGBA` | `(0, 255)` | 3,482 | 303 | 1,399 | `42a030cce313` | Existing (`SupportMeDialog` fallback) |
| `undo.png` | `72x72` | `RGBA` | `(0, 255)` | 32 | 36 | 5,116 | `8e92ff933c42` | Existing (`btn_ribbon_undo`) |

*(All 53 PNGs have genuine `RGBA` alpha transparency with `alpha=(0, 255)` — zero opaque fake-RGBA boxes.)*

### 6.2 `assets/icon.py` DPI-Aware Load-Time Resizing & Cache
- Add `get_dpi_scale(master: Optional[tk.Misc] = None) -> float` (`root.winfo_fpixels("1i") / 96.0`, clamped `[1.0, 2.5]`, safe fallback `1.0`).
- Add `scale_icon_size(size: Tuple[int, int], master: Optional[tk.Misc] = None) -> Tuple[int, int]`.
- Extend `get_icon(name, size=(20, 20), master=None, dpi_aware: bool = False)` using Pillow `Image.Resampling.LANCZOS`, cached by `(root_id, name, eff_w, eff_h)` inside `_ICON_CACHE` (`MAX_ICON_CACHE = 128`). Keeping `dpi_aware=False` as default ensures `test_v15_s04::test_probe_5` (`refresh.png` at `(14, 14)`) and `test_s8b2` (`search` at `(16, 16)`) remain 100% unaffected.
- `MisoraApp.get_icon(self, name: str, size: Tuple[int, int] = (20, 20), dpi_aware: bool = True)` calls `get_icon(name, size, master=self, dpi_aware=dpi_aware)`.
- `ImportFromXUATDialog` loads the 3-icon selection trio through `self.app.get_icon(..., (20, 20), dpi_aware=True)` (identical DPI-aware path, cached cleanly by `(root_id, name, eff_w, eff_h)`).

### 6.3 `ToolTip.set_text()` & Exact Icon Wiring (`misora.py`)
- **`ToolTip` dynamic update (`misora.py:199-284`):** Store `self._label: Optional[tk.Label] = None` in `show_tip()` (cleared in `hide_tip()`) and add `ToolTip.set_text(self, text: str) -> None` updating `self.text = text` AND `self._label.configure(text=text)` if visible, so Q-07 tri-state buttons update both `btn._tooltip.text` and any open hover tooltip live.
- **Main Toolbar / Header (`(20, 20)` logical, `dpi_aware=True`):**
  - `btn_translate`: `self.get_icon("language-translation-icon", (20, 20))` (`text="MTL"`, `compound="none" if ico else "left"`)
  - `cb_cont`: `self.get_icon("BoxConversationList", (20, 20))` (`text=" All Script"`, `compound="left" if ico else "none"`)
  - `btn_box_new`: `self.get_icon("BoxD", (20, 20))` (`text="➕"` fallback)
  - `btn_box_cut`: `self.get_icon("BoxCut", (20, 20))` (`text="✂📦"` fallback)
  - `btn_box_copy`: `self.get_icon("BoxCopy", (20, 20))` (`text="📋📦"` fallback)
  - `btn_box_paste`: `self.get_icon("BoxPaste", (20, 20))` (`text="📥📦"` fallback)
  - `_show_box_paste_mode_dialog()` (`btn_ins` / `btn_rep`): `self.get_icon("BoxInsert", (20, 20))` / `self.get_icon("BoxReplace", (20, 20))` (`compound="left"` when image present, `PhotoImage` refs retained on `dlg._paste_mode_icons`).
  - `BoxConversation.png`: **Parked (unused)**.
- **Q-10 `gd_header` Select All / Deselect All (`btn_select_all_boxes`, `btn_deselect_all_boxes`):**
  - `btn_select_all_boxes`: `image=self.ico_box_select_all` (`BoxSelectAll`, `(20, 20)`), `text="All"`, `compound="none" if self.ico_box_select_all else "left"`, `width=3 if self.ico_box_select_all else 4`.
  - `btn_deselect_all_boxes`: `image=self.ico_box_select_none` (`BoxSelectNone`, `(20, 20)`), `text="None"`, `compound="none" if self.ico_box_select_none else "left"`, `width=3 if self.ico_box_select_none else 5`.
- **Q-07 `ImportFromXUATDialog` Tri-State Group Headers (`_make_tristate_group_header`, `_update_group_header_state`):**
  - Load & retain `self._group_select_icons = {"none": self.app.get_icon("BoxSelectNone", (20, 20), dpi_aware=True), "partial": self.app.get_icon("BoxSelectOne", (20, 20), dpi_aware=True), "all": self.app.get_icon("BoxSelectAll", (20, 20), dpi_aware=True)}` (and keep ref on each button via `setattr(btn, "_state_icons", self._group_select_icons)`).
  - State mapping (constant `compound="none"` with `width=3` when icon is present, `compound="left"` with `width=14` fallback when `icon is None`, ensuring **0px** geometry shift across all 3 states):
    - `"none"` → icon `BoxSelectNone`, fallback `text="Select All"`, tooltip `"No items selected — click to select all eligible rows in group (all filters)"`
    - `"partial"` → icon `BoxSelectOne`, fallback `text="Some selected"` (**NEVER `"One selected"`**), tooltip `"Some selected (partially selected) — click to deselect all eligible rows in group (all filters)"`
    - `"all"` → icon `BoxSelectAll`, fallback `text="Deselect All"`, tooltip `"All eligible items selected — click to deselect all eligible rows in group (all filters)"`
  - `_update_group_header_state()` updates `image`, `compound`, `text`, `width`, `state`, and `btn._tooltip.set_text(...)` across row toggles, `_on_group_select_all()`, `_set_filter()`, and `_on_reload_index()` / `_populate_rows()`.

---

## 7. `Q-16` — Main Menu Inventory, Dedup & Existing Test Audit (`misora.py`)

### 7.1 Existing Menu Test Audit (`tests/`)
Direct grep across all `tests/test_*.py` confirmed **0 hits** for `"NGUI Glossary"`, `"Display & Theme"`, `"Prompt Settings"`, `menu_help`, `menu_customize`, `help_menu`, and `cust_menu` (`test_v15_s06::test_probe_3` only checks `labels.index("Tools") == labels.index("View") + 1`, and `test_p3_s14::test_probe_04` checks `View > Toggle NGUI Ribbon`, both preserved). Zero additional menu test migrations are needed.

### 7.2 Confirmed Main Menu Changes (`misora.py:4561-4994`)
- **Remove BOTH:**
  1. Top-level `NGUI Glossary` cascade (`L4718-4752`), moving its sole unique command **`Reset Color Tag ([-])`** into `Edit` (after `NGUI Color & Gradient Picker...`).
  2. `Help > NGUI & Ruby Glossary` (`L4988`).
- **Remove redundant `Customize` items:**
  - Remove `Display & Theme Settings... (Ctrl+,)` (canonical entry is `View > Toggle Customization Panel (Ctrl+,)`).
  - Remove `AI / LLM Translation Prompt Settings...` (canonical entry is `Translator > Configure AI / LLM Prompt Header...`).
  - `Customize` retains: `Increase Dialogue Font Size`, `Decrease Dialogue Font Size`, `Theme Presets` cascade, `Reset Display & Colors to Default`.
- **Canonical `View` & `Help` menus:**
  - `View` retains `Toggle Customization Panel (Ctrl+,)` and `Toggle NGUI Glossary Panel (F1)` as the sole canonical drawer menu toggles.
  - `Help` becomes: `Support the Creator...` (`command=self.on_support_me`), separator, `About Misora: Story Editor` (`command=self.on_about`).
- Menubar shrinks cleanly from **12 → 11** top-level cascades (`File | Edit | View | Tools | Search | Customize | Folders & Files | Translator | Datamine | Debug | Help`) with zero lost actions or shortcuts.

---

## 8. `Q-17` — Complete 3-Layer Tooltips & Existing Tooltip Test Audit (`misora.py`)

### 8.1 Existing Tooltip Test Audit (`tests/`)
Direct grep across `tests/test_*.py` (`22` `_tooltip` hits, `8` `ToolTip` hits) confirmed all existing assertions check `delay_ms == 350`, `"Ctrl+T"` (`btn_translate`), `"Ctrl+Shift+T"` (`btn_ai_prompt`), `"{playername}"` (`btn_player`), `"Jump to Speaker Box"` (`btn_speaker_dropdown`), `"all filters"` (`_group_select_buttons`), and `btn_save` tooltip — all 100% preserved.

### 8.2 Missing Tooltip Coverage Added (`ToolTip(..., delay_ms=350)`)
- **Layer 1 (Main Workspace / Search / Header / Bottom Tabs):**
  - Search Bar: `btn_replace`, `btn_replace_all`, `cb_case`, `cb_rx`, `cb_ws`, `rb_proj`, `rb_folder`, `rb_cur`, `cb_bdl`, `cb_txt`, `btn_browse_search_folder`
  - Left Dock: `btn_tab_search`, `btn_open_more`
  - Header / Workspace / Bottom Tabs: `cb_dialogue_select`, `btn_empty_open`, `btn_tab_quick_edit`, `btn_tab_raw_commands`
  - Status Bar: `cb_sync`, `btn_revert`, `btn_save` (verified complete)
- **Layer 2 (Right Side Drawer — `Customize`, `NGUI Glossary`, `MTL`):**
  - `Customize`: `cb_custom_font`, `btn_refresh_fonts`, `btn_open_fonts_folder`, `cb_preset`, `btn_apply_preset`, `btn_reset_custom`
  - `NGUI Glossary`: `ent_filter`, `btn_insert_glossary`
  - `MTL`: verify all mode/header/card/globe tooltips
- **Layer 3 (Import & Archiving Dialogs — `ImportFromXUATDialog`, `XuatCleanupDialog`):**
  - `ImportFromXUATDialog`: `btn_reload_xuat`, `_filter_buttons` (`all`/`duplicates`/`missing`/`matched`), `cb_arch`, `cb_wrap`, `btn_cancel`, `btn_apply`, dynamic tri-state `_group_select_buttons`, plus per-row `cb_skip`, `scope_cmb`, `btn_prev`, `btn_next`.
  - `XuatCleanupDialog`: `cb_include_applied`, `btn_select_all`, `btn_deselect_all`, `btn_execute`, `btn_close`.

---

## 9. Verification & Test Plan (`tests/`)

### 9.1 New Suite: `tests/test_v15_s11e_polish_splash_menu_tooltips.py` (9 Tests)
- **7 Failing-First Probes (MUST FAIL pre-patch, PASS post-patch):**
  1. `test_probe_1_q03_per_widget_word_wrap_contract` — verifies `wrap="none"` vs `wrap="word"` across all 22 `tk.Text` widgets, `clean_scroll_x` inside pack-managed `clean_editor_row` (mutual exclusion on Box 0 & Dialogue Preview + `_on_toggle_line_numbers()` safety), and `_auto_resize_dialogue_box()` logical-line height.
  2. `test_probe_2_q05_splash_lifecycle_waits_for_deferred_restore_and_pumps_ticks` — injects an artificially slowed session-restore hook under `show_splash=True` and asserts: (a) splash remains alive/visible while UI construction and slowed restore are still running, (b) progress never reports `1.00` / `"Ready!"` before restore completes, (c) splash closes cleanly and main window deiconifies once restore finishes, (d) startup-exception `try/except` closes splash without leaving an orphan, and (e) `show_splash=False` preserves `deiconify`-before-`after_idle` (`test_p3_s12::test_04`) + single `tk.Tk()` root.
  3. `test_probe_3_q13_priconneretl_and_cornelia_branding_splash_and_about` — verifies `PriconneRe:TL` (larger, bold) and `Cornelia` on both `MisoraSplashScreen` and `on_about()`, and asserts `__init__.__version__ == "1.4.15"` alongside parity with `misora.__version__`, `assets.splash._VERSION`, and `core.mtl_engine.APP_VERSION`.
  4. `test_probe_4_q14_support_dialog_english_and_600px_gif` — verifies 100% English `PriconneRe:TL`/`Cornelia` copy (zero Indonesian text), `~600px` GIF scaling, screen-width & screen-height clamping (simulating 720p/125%-DPI), window title `"Support the Creator — Misora: Story Editor"`, and clean cleanup/fallback.
  5. `test_probe_5_q15_verified_icons_dpi_lanczos_and_3icon_selection_trio` — verifies DPI-aware LANCZOS resizing & cache retention for `language-translation-icon`, `BoxConversationList`, `BoxD`, `BoxCopy`, `BoxCut`, `BoxPaste`, `BoxInsert`, `BoxReplace`, `BoxSelectNone`, `BoxSelectOne`, `BoxSelectAll` (`BoxConversation.png` unused); verifies Q-07 tri-state icons, dynamic `ToolTip.set_text()`, zero header geometry shift across `none`/`partial`/`all`, filter switches, and `_on_reload_index()`; verifies Q-10 `gd_header` icons; and **explicitly mocks `get_icon -> None`** to verify accessible fallback text (`"Select All"`, `"Some selected"` with zero `"One selected"`, `"Deselect All"`, `"All"`, `"None"`) and clean fallback geometry.
  6. `test_probe_6_q16_main_menu_inventory_and_ngui_glossary_dedup` — verifies `NGUI Glossary` top-level cascade & `Help > NGUI & Ruby Glossary` & duplicate `Customize` items are removed, `Edit` contains `Reset Color Tag ([-])`, `View > Toggle NGUI Glossary Panel (F1)` is the single glossary menu entry, and `Help` contains `Support the Creator...` + `About Misora: Story Editor`.
  7. `test_probe_7_q17_complete_3_layer_tooltips` — audits all newly covered Layer 1 / Layer 2 / Layer 3 controls for non-empty `ToolTip` with `delay_ms == 350`.
- **2 Regression Guards (MUST PASS both pre-patch and post-patch):**
  8. `test_guard_1_headless_show_splash_false_and_single_source_version_parity` — verifies `MisoraApp(show_splash=False)` creates zero splash windows and verifies dynamic single-source version **parity** across `__init__.__version__`, `misora.__version__`, `assets.splash._VERSION`, and `core.mtl_engine.APP_VERSION` (without hardcoding `"1.4.15"`, so it passes cleanly both pre-patch at `"1.4.14"` and post-patch at `"1.4.15"`).
  9. `test_guard_2_s11d_s04_and_s8b4_invariants_intact` — verifies `Q-06`, `Q-10` Box 0/Lock safety, `Q-11`, `Q-12`, `test_v15_s04::test_probe_5` (`refresh.png`), and `S8b4` paned minsize/fallback contracts remain intact.

### 9.2 Existing Test Migrations (`0` Extra `test_*` Methods, Zero Assertion Weakening)
- `tests/test_v15_s11d_import_ux_productivity.py` (`test_probe_1` & `test_probe_3`): migrate ASCII `"[x]"`/`"[ ]"`/`"[-]"` assertions to verify Q-07 3-icon states, retained `PhotoImage`s, fallback text (`"Deselect All"`, `"Select All"`, `"Some selected"` / zero `"One selected"`), dynamic tooltips, filter/`_on_reload_index()` stability, and Q-10 `BoxSelectAll`/`BoxSelectNone` icons.
- `tests/test_v15_s05_speaker_console_about.py` (`test_probe_5`): migrate About & Support assertions to `"PriconneRe:TL"` (larger, bold), `"Cornelia"`, English caption (zero Indonesian text), and `~600px` GIF target scale (preserving `"Support Me"` button & URL checks).

### 9.3 Exact Post-S11e Baseline Math
- **Pre-S11e Baseline (`da74305`):** **`466`** tests (`423 PASS, 35 SKIP, 6 pre-existing FAIL, 2 pre-existing ERROR`)
- **Post-S11e Expected:** **`475`** tests (`+9` new methods in `tests/test_v15_s11e_polish_splash_menu_tooltips.py`; `0` extra `test_*` methods in migrated `test_v15_s11d_import_ux_productivity.py` / `test_v15_s05_speaker_console_about.py` → **`432 PASS, 35 SKIP, 6 pre-existing FAIL, 2 pre-existing ERROR`**, `0` new regressions).

---

## 10. Verification Commands (Execution Gate After Proceed)

1. **Pre-Patch TDD Gate (new suite written BEFORE patching production files):**
   ```powershell
   py -3.12 -m unittest tests.test_v15_s11e_polish_splash_menu_tooltips -v
   ```
   *(Expected pre-patch: 7 Probes FAIL, 2 Guards PASS — `test_guard_1` & `test_guard_2` OK.)*

2. **Compile Check (after implementation):**
   ```powershell
   py -3.12 -m compileall -q __init__.py misora.py core assets tests
   ```

3. **Targeted Regression & S11e Suites:**
   ```powershell
   py -3.12 -m unittest tests.test_v15_s11e_polish_splash_menu_tooltips tests.test_v15_s11d_import_ux_productivity tests.test_v15_s05_speaker_console_about tests.test_v15_s04_layout_drawer_controls tests.test_v15_s08_release_gate_stress tests.test_v15_s03_all_script_preview_paste tests.test_p3_s12_lifecycle_security tests.test_p3_s14_toolbar_search_ui tests.test_p3_s18_game_preview tests.test_misora_ui_integration tests.test_s8b4_ui_polishing -v
   ```

4. **Test Count & Full Discovery / Disjoint Reconciliation:**
   ```powershell
   py -3.12 -c "import unittest; s=unittest.defaultTestLoader.discover('tests'); print('countTestCases:', s.countTestCases())"
   py -3.12 -m unittest discover -s tests -v
   ```
   *(Expected `countTestCases: 475`. If monolithic `discover` hits the pre-existing cross-test `Tcl_AsyncDelete` GC race mid-run, record the exact failing/stopping test honestly and run the strictly disjoint remaining tail module manifest so all `475` tests are accounted for without overlap or masking.)*

---

## 11. Manual Windows QA Checklist (`MANUAL-PENDING`)

1. **`Q-03` Per-Widget Word Wrap & `clean_scroll_x`:** Open a story with >54d dialogue lines in Dialogue view -> verify `txt_dialogue` does NOT soft-wrap (`wrap="none"`), aligns 1:1 with `gutter_clean` and `ruler_clean`, scrolls horizontally via `clean_scroll_x`, and `clean_scroll_x` disappears cleanly on Box 0 & Dialogue Preview; toggle `View > Show Line Numbers` OFF/ON cleanly.
2. **`Q-05` Non-Blocking Splash Lifecycle:** Launch via `misora.bat` with multiple previous-session `.unity3d` / `.v2.txt` tabs -> verify splash stays visible through UI build AND session restore, updates progress monotonically without `"Not Responding"`, closes cleanly only at `100% / Ready!`, and reveals the main window with restored tabs intact.
3. **`Q-13` Branding (`PriconneRe:TL` & `Cornelia`):** Verify splash screen and `Help > About Misora: Story Editor` prominently display bold/larger **`PriconneRe:TL`**, creator **`Cornelia`**, and **`v1.4.15`**.
4. **`Q-14` Support the Creator EN + `~600px` GIF:** Open `Help > Support the Creator...` (and `About -> Support Me`) -> verify 100% English copy referencing `PriconneRe:TL` and `Cornelia`, `Service.gif` plays smoothly near `600px` width without clipping buttons on 720p/125% DPI, and closes cleanly with zero timer leaks.
5. **`Q-15` Verified Icons, 3-Icon Trio & Paste Mode Chooser:** Verify toolbar/header icons (`language-translation-icon`, `BoxConversationList`, `BoxD`, `BoxCut`, `BoxCopy`, `BoxPaste`), `BoxInsert`/`BoxReplace` icons inside Paste Box mode chooser, `All`/`None` (`BoxSelectAll`/`BoxSelectNone`) in `gd_header` when `Select Box` is ON, and `Import from XUAT...` tri-state group headers (`BoxSelectNone` / `BoxSelectOne` with `"Some selected"` tooltip / `BoxSelectAll`) staying crisp and synced across filter switches and `Reload XUAT Index`.
6. **`Q-16` Main Menu Dedup:** Inspect menubar -> confirm `NGUI Glossary` top-level menu and `Help > NGUI & Ruby Glossary` are gone, `Edit > Reset Color Tag ([-])` works, `View > Toggle NGUI Glossary Panel (F1)` works, and `Help > Support the Creator...` opens Support dialog.
7. **`Q-17` 3-Layer Tooltips:** Hover across Search/Replace controls, Left Dock tabs, header/editor tabs, Customize/Glossary/MTL drawer controls, and `Import from XUAT...` / `XUAT Translation Archiving` controls -> verify crisp 350ms tooltips appear and vanish cleanly.
