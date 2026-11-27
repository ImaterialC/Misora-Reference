# Implementation Plan (Rev 3) — S11c (`v1.4.13`): Unified Single-Box Quick Edit (`Q-22` Only)

> [!IMPORTANT]
> **Planning-First Gate:** No repository files have been modified. Waiting for independent review (ChatGPT & Qwen) and explicit Project Lead **`Proceed`** before writing tests or patching `misora.py`.

---

## 1. Pre-Proceed Git Prerequisite & Observed Baseline

### 1.1 Mandatory Pre-Proceed Commit Gate

> [!CAUTION]
> **Mandatory Pre-Proceed Gate:** The following **8 uncommitted S11b2 (v1.4.12) files** in the working tree MUST be locally committed into HEAD by the Project Lead before S11c edits begin, so that S11b2 and S11c diffs never mix:
>
> | Status | File |
> |--------|------|
> | `M` | `CHANGELOG.md` |
> | `M` | `PROJECT_STATE.md` |
> | `M` | `__init__.py` (currently `"1.4.12"`) |
> | `M` | `core/xunity_sync.py` |
> | `M` | `misora.py` |
> | `M` | `tests/test_p3_s10_xuat_integrity.py` |
> | `M` | `tests/test_s2_dirty_contract.py` |
> | `??` | `tests/test_v15_s11b2_xuat_batch_sync.py` |
>
> **After commit:** Only `M assets/icons/BoxInsert.png` and `?? assets/icons/BoxReplace.png` should remain uncommitted (unrelated icon assets).
>
> S11c edits will NOT begin until the Project Lead confirms that this commit has been made.

### 1.2 Environment Snapshot

- **Git `HEAD` (pre-S11b2 commit):** `f2ab4a15a82754970309b1f9965a66407cab03b8` (`S11b closure (v1.4.11)`)
- **Git `HEAD` (post-S11b2 commit, expected):** To be recorded on `Proceed` after the commit gate is satisfied.
- **Python Version:** `Python 3.12.10` (`py -3.12`)

### 1.3 Observed Test Baseline (Post-S11b2 Committed HEAD)

| Metric | Count |
|--------|-------|
| **Total tests discovered** | 451 |
| **Passed** | 408 |
| **Fixture-skipped** (`@unittest.skipUnless`) | 35 |
| **Pre-existing failures** (not introduced by S11c) | 6 |
| **Pre-existing fixture errors** | 2 |

This baseline will be re-verified against the **committed S11b2 HEAD** immediately upon `Proceed` (before any S11c edits). Full discovery must match 451 tests. Any deviation is a STOP gate.

### 1.4 Version Target

Live `__init__.py` on disk is currently `"1.4.12"` (occupied by S11b2). Following the sequential patch rule, S11c will bump `__init__.__version__` to **`"1.4.13"`**. Release `v1.5.0` remains **ON HOLD**.

---

## 2. `qe_canvas` / `qe_inner_frame` Reference Audit (Removal Inventory)

Replacing the nested scrollable canvas with a single persistent `txt_quick_edit` requires updating/removing every reference to the old multi-segment infrastructure. Complete grep-verified inventory across `misora.py` and all `tests/`:

### 2.1 `misora.py` — Old Canvas/Frame References to Remove/Replace

| Line(s) | Symbol | Current Purpose | S11c Action |
|----------|--------|-----------------|-------------|
| L6553-6554 | `self.qe_canvas = tk.Canvas(...)` | Scrollable container for per-seg editors | **Replace** with `self.txt_quick_edit = tk.Text(qe_body_wrap, wrap="none", ...)` + `self.qe_scroll_x` |
| L6555-6556 | `self.qe_scroll_y` config tied to `qe_canvas` | Vertical scrollbar for canvas | **Rebind** to `txt_quick_edit` |
| L6557-6558 | `self.qe_inner_frame = tk.Frame(qe_canvas, ...)` | Container for per-segment `tk.Text` editors | **Remove** entirely |
| L6559 | `self._qe_canvas_win = qe_canvas.create_window(...)` | Canvas window embedding `qe_inner_frame` | **Remove** |
| L6560-6563 | `<Configure>` bindings on `qe_inner_frame` and `qe_canvas` | Scroll region updates | **Remove** |
| L6564-6566 | Mousewheel bindings on `qe_canvas` | Scroll via mousewheel | **Replace** with standard `txt_quick_edit` scroll (native `tk.Text` scroll) |
| L12213-12216 | `_update_bottom_tab_styles()` | Configures `qe_canvas["bg"]` and `qe_inner_frame["bg"]` | **Replace** with `txt_quick_edit["bg"]`, `lbl_qe_placeholder["bg"]` |
| L12241-12244 | `_rebuild_quick_edit_widgets()` | Checks `qe_inner_frame.winfo_exists()`, destroys its children | **Replace** with `txt_quick_edit.delete("1.0", tk.END)` and show/hide logic |
| L12257, 12270 | Placeholder labels | Children of `qe_inner_frame` | **Replace** with `self.lbl_qe_placeholder` (sibling of `txt_quick_edit`) |
| L12290, 12304 | Per-segment `tk.Text` widgets | Parented to `qe_inner_frame` (or row frames) | **Remove** — single `txt_quick_edit` replaces all |

### 2.2 `misora.py` — Old Multi-Segment Widget References to Update

| Line(s) | Symbol | S11c Action |
|----------|--------|-------------|
| L2688-2690 | `destroy()` clears `_qe_seg_widgets` | **Keep** — clears `[self.txt_quick_edit]` / `[]` and `_qe_session` |
| L3264-3277 | `_apply_theme_and_fonts_live()` styles `_qe_seg_widgets` | **Update** to also style `txt_quick_edit`, `lbl_qe_segs_badge`, `lbl_qe_placeholder` |
| L12364 | `_refresh_quick_edit_pane()` fast path: `len(self._qe_seg_widgets) == max(1, len(box.segs))` | **Change** to `len(self._qe_seg_widgets) == 1` (always 1 when editable) |
| L12367-12374 | Fast path: per-segment text sync | **Replace** with single `txt_quick_edit` ↔ `box.clean_text` comparison |
| L12391 | `_on_quick_edit_focus_out`: `focused in ... _qe_seg_widgets` | **Keep** — checks `[txt_quick_edit]` |
| L12399-12479 | `_on_quick_edit_changed()`: reads from `_qe_seg_widgets` | **Replace** with read from single `txt_quick_edit` |
| L12481-12531 | `_flush_quick_edit_session()` | **Update** post-flush refresh with doc identity guard (§3.5) |
| L12682-12685 | `_commit_widget_edit()`: `if w in self._qe_seg_widgets` | **Keep** — `txt_quick_edit` is `_qe_seg_widgets[0]` |

### 2.3 `tests/` — Old Multi-Segment References Audited

| File | Line(s) | Current Reference | S11c Action |
|------|---------|-------------------|-------------|
| `tests/test_v15_s10_all_script_quick_edit.py` | L389-390 | `len(seg_widgets) == 4` | **Change** to `len(seg_widgets) == 1` |
| `tests/test_v15_s10_all_script_quick_edit.py` | L391-406 | Individual seg widget edits | **Replace** with single `txt_quick_edit` edits |
| `tests/test_v15_s08_release_gate_stress.py` | L339-345 | `self.app._qe_seg_widgets[0]` | **Inspect-only / Untouched** — compatibility alias `_qe_seg_widgets = [txt_quick_edit]` preserves `[0]` seamlessly |

### 2.4 Mousewheel / Canvas Scroll Helpers to Audit

Any bound `_on_qe_canvas_scroll` or `_qe_canvas_configure` helper referenced in `_build_ui` is removed (`<Configure>` lambdas on `qe_canvas` / `qe_inner_frame` at L6560-6566). The persistent `txt_quick_edit` uses native `tk.Text` horizontal/vertical scrolling (`qe_scroll_x`, `qe_scroll_y`).

---

## 3. Exact Planned Changes (Strict File Ownership)

### Allowed Files to Modify/Create
- `__init__.py`: Bump `__version__` from `"1.4.12"` → `"1.4.13"`.
- `misora.py`: Strictly scoped to `Q-22` Quick Edit single-box unification, pre-first-mutation snapshot safety, canonical `inject_box(idx, None, new_tx)` mutation, flush guards, and `qe_canvas`/`qe_inner_frame` removal.
- `tests/test_v15_s11c_quick_edit_unified.py` (**NEW**): 4 failing-first Defect/Behavior Probes + 2 Regression Guards.
- `tests/test_v15_s10_all_script_quick_edit.py`: Migrate `test_probe_5` to 1 unified Quick Edit box (`box.clean_text`, `[4 segs]` badge, canonical `inject_box`, 1-op Undo/Redo restoring 4 segments, binary round-trip, View-Aware sync, S09b Lock parity) + add Manual-Dialogue-vs-Quick-Edit AST & binary parity assertion.
- `CHANGELOG.md` & `PROJECT_STATE.md`: Record S11c (`v1.4.13`) summary, S08/S10 verification counts, and Manual Windows QA checklist.

*(Inspect-only / **UNTOUCHED**: `tests/test_v15_s08_release_gate_stress.py` — audited and verified compatible via `_qe_seg_widgets = [self.txt_quick_edit]`; still executed in targeted verification.)*
*(Strictly Forbidden: `core/*.py`, `assets/*`, `requirements.txt`, `misora_config.json`, `backups/`.)*

---

### 3.1 Single Persistent Unified Quick Edit Surface (`_build_ui`, L6539-6567)

**Replace** the current `qe_canvas` + `qe_inner_frame` + per-segment `tk.Text` editors with:

```python
# Inside qe_header (existing lbl_qe_title):
self.lbl_qe_segs_badge = tk.Label(
    qe_header, text="", font=("Segoe UI", 9),
    fg=t["fg_muted"], bg=t["bg_panel"],
    anchor="e",
)
self.lbl_qe_segs_badge.pack(side="right", padx=(0, 6))

# Inside qe_body_wrap (replace qe_canvas + qe_inner_frame):
self.qe_scroll_y = tk.Scrollbar(qe_body_wrap, orient="vertical")
self.qe_scroll_x = tk.Scrollbar(qe_body_wrap, orient="horizontal")
self.txt_quick_edit = tk.Text(
    qe_body_wrap,
    wrap="none",          # Matches Q-03/C-3 wrap contract (alongside qe_scroll_x)
    undo=False,
    exportselection=True,
    xscrollcommand=self.qe_scroll_x.set,
    yscrollcommand=self.qe_scroll_y.set,
)
self.qe_scroll_y.config(command=self.txt_quick_edit.yview)
self.qe_scroll_x.config(command=self.txt_quick_edit.xview)

# Placeholder label (shown when no editable box)
self.lbl_qe_placeholder = tk.Label(
    qe_body_wrap, text="Select a dialogue box to edit",
    font=("Segoe UI", 10), fg=t["fg_muted"], bg=t["bg_panel"],
    anchor="center",
)

# Bindings (verified against misora.py L12327-12331 & L6154-6157):
self._install_shortcuts_bindtag(self.txt_quick_edit)
self.txt_quick_edit.bind("<KeyRelease>", lambda _e: self._on_quick_edit_changed())
self.txt_quick_edit.bind("<<Paste>>", lambda _e: self.after_idle(self._on_quick_edit_changed))
self.txt_quick_edit.bind("<<Cut>>", lambda _e: self.after_idle(self._on_quick_edit_changed))
self.txt_quick_edit.bind("<FocusOut>", self._on_quick_edit_focus_out)
# Ctrl+Z / Ctrl+Y safety bindings (matching txt_dialogue L6154-6157)
self.txt_quick_edit.bind("<Control-z>", lambda e: self._shortcut_undo())
self.txt_quick_edit.bind("<Control-y>", lambda e: self._shortcut_redo())
self.txt_quick_edit.bind("<Control-Shift-Z>", lambda e: self._shortcut_redo())
self.txt_quick_edit.bind("<Control-Shift-z>", lambda e: self._shortcut_redo())

# Compatibility alias (AGENTS.md §3: never reassign widget attribute)
self._qe_seg_widgets: List[tk.Text] = []  # Set to [txt_quick_edit] when active, [] for placeholder
```

> [!NOTE]
> **Live Code Verification — KeyRelease & Undo/Redo Single-Fire Guarantee:**
> 1. **`<KeyRelease>` Handler:** Verified on disk that `_on_quick_edit_key_release` does NOT exist in `misora.py` (L12328 uses `lambda _e: self._on_quick_edit_changed()`). Keeping `lambda _e: self._on_quick_edit_changed()` avoids introducing a nonexistent symbol.
> 2. **No Double-Fire on `Ctrl+Z` / `Ctrl+Y` / `Ctrl+Shift+Z`:** `_install_shortcuts_bindtag(self.txt_quick_edit)` places `"MisoraShortcuts"` **first** in `bindtags()` (`("MisoraShortcuts", w, "Text", self, "all")`).
>    - On real keystrokes, `MisoraShortcuts`'s `<KeyPress>` dispatcher (`_on_misora_shortcut`, L8998-9003, L9029-9031) calls `self.on_undo()` / `self.on_redo()` and returns `"break"`, halting propagation before the widget instance binding or root `self.bind("<Control-z>")` (L9235) can fire.
>    - If an event bypasses `MisoraShortcuts` `<KeyPress>` (e.g., virtual/widget-direct dispatch), the widget's `<Control-z>`/`<Control-y>` binding calls `self._shortcut_undo()`/`self._shortcut_redo()` (L7341-7347), which calls `self.on_undo()`/`self.on_redo()` and returns `"break"`, blocking root `self.bind(...)` from double-firing.
>    - On the subsequent `<KeyRelease>`, `_on_quick_edit_changed()` sees `new_tx == box.clean_text` (already synced by `on_undo()`/`on_redo()` → `_update_views()` → `_refresh_quick_edit_pane()`) and exits immediately as a no-op (`False`).
> 3. **Dialogue-Parity Word-Wrap Contract:** `txt_quick_edit` uses `wrap="none"` with `qe_scroll_x` + `qe_scroll_y`, zero red overflow tags (`line_overflow`, `gutter_overflow`), zero ruler widget, and zero NGUI rich-text decorators (`_highlight_ngui_tags_for_widget` is NOT called on `txt_quick_edit`).

---

### 3.2 `_rebuild_quick_edit_widgets(self, box, box_idx)` (L12240-12344)

**Placeholder path** (no doc, no boxes, Box 0 active, `box is None`):
- Hide `txt_quick_edit`, `qe_scroll_y`, `qe_scroll_x`; show `lbl_qe_placeholder` with appropriate message.
- Clear `lbl_qe_segs_badge` text (`""`).
- Set `self._qe_seg_widgets = []`.
- Set `self._qe_session = None`.

**Active box path** (editable box):
- Hide `lbl_qe_placeholder`.
- Pack `qe_scroll_x` (`side="bottom"`, `fill="x"`), `qe_scroll_y` (`side="right"`, `fill="y"`), `txt_quick_edit` (`side="left"`, `fill="both"`, `expand=True`).
- Set `self._qe_seg_widgets = [self.txt_quick_edit]`.
- Set `lbl_qe_title` to `f"Quick Edit — Box #{box_idx + 1}: {sp_disp}"`.
- Set `lbl_qe_segs_badge` to `f"[{n_segs} segs]"` if `len(box.segs) > 1`, else `""`.
- Under `self._suppress_qe_events = True`:
  1. `self.txt_quick_edit.delete("1.0", tk.END)`
  2. `self.txt_quick_edit.insert("1.0", box.clean_text)` — exact same projection as `txt_dialogue`.
  3. Capture `old_snapshot = BoxSnapshot.from_box(box)` **strictly before any live mutation**.
  4. Set `self._qe_session = {"file_path": str(self.current_file_path or ""), "doc": self.current_doc, "box_uid": box_uid, "box_index": box_idx, "old_snapshot": old_snapshot, "dirty": False}`.
  5. Set `self._qe_stale = False`.
- Under `finally: self._suppress_qe_events = False`.

---

### 3.3 `_refresh_quick_edit_pane(self, force=False)` (L12346-12380) — Flush-Before-Sync & Detached-Dict Fix

> [!WARNING]
> **Silent Undo Loss & Detached-Dict Fix:**
> 1. The current fast path (L12369-12376) overwrites `sess["old_snapshot"]` and sets `sess["dirty"] = False` even when `sess["dirty"]` is `True`, silently discarding the pending undo snapshot.
> 2. Simply calling `self._flush_quick_edit_session()` and then mutating the local `sess` variable risks writing to a **detached dictionary** if `_flush_quick_edit_session()` cleared or replaced `self._qe_session`. Therefore, we MUST re-read `self._qe_session` after flushing (and re-create it if `None` / mismatched).

**Revised fast-path logic** (same doc, same `box_uid`, `len(self._qe_seg_widgets) == 1`):

```python
# Fast path: same doc, same box_uid, single txt_quick_edit
widget_text = self.txt_quick_edit.get("1.0", "end-1c")
model_text = box.clean_text

if widget_text != model_text:
    # External mutation detected (Dialogue typing, MTL apply, Replace All, Undo/Redo, etc.)
    # CRITICAL: If session is dirty, flush FIRST to record the pending undo delta
    if sess.get("dirty"):
        self._flush_quick_edit_session()

    # Now sync widget to the externally-updated model and update LIVE self._qe_session
    self._suppress_qe_events = True
    try:
        self.txt_quick_edit.delete("1.0", tk.END)
        self.txt_quick_edit.insert("1.0", model_text)

        # Re-read live _qe_session (never mutate potentially detached local `sess`!)
        live_sess = getattr(self, "_qe_session", None)
        snap = BoxSnapshot.from_box(box)
        if (
            live_sess is None
            or live_sess.get("doc") is not self.current_doc
            or live_sess.get("box_uid") != b_uid
        ):
            self._qe_session = {
                "file_path": str(self.current_file_path or ""),
                "doc": self.current_doc,
                "box_uid": b_uid,
                "box_index": idx,
                "old_snapshot": snap,
                "dirty": False,
            }
        else:
            live_sess["old_snapshot"] = snap
            live_sess["box_index"] = idx
            live_sess["dirty"] = False
    finally:
        self._suppress_qe_events = False

# Always refresh badge and title (seg count or speaker may have changed)
sp_disp = box.speaker if box.speaker else "(Narration)"
n_segs = len(box.segs)
self.lbl_qe_title.config(text=f"Quick Edit — Box #{idx + 1}: {sp_disp}")
self.lbl_qe_segs_badge.config(text=f"[{n_segs} segs]" if n_segs > 1 else "")
```

---

### 3.4 `_on_quick_edit_changed(self)` (L12399-12479) — Lazy Session Init & Canonical Mutation

**Guard** against `_suppress_qe_events`, missing `self.current_doc`, `is_box0_active`, and invalid/missing `self.txt_quick_edit` (`not self._qe_seg_widgets or not self.txt_quick_edit.winfo_exists()`).

**Resolve active box & lazily initialize `_qe_session` if `None` or stale-doc:**
```python
box_idx = self.current_box_idx
if sess is not None and sess.get("doc") is self.current_doc and sess.get("box_uid") is not None:
    found_idx = next(
        (i for i, b in enumerate(self.current_doc.boxes) if _get_box_uid(b) == sess.get("box_uid")),
        None,
    )
    if found_idx is not None:
        box_idx = found_idx
if not (0 <= box_idx < len(self.current_doc.boxes)):
    return False

box = self.current_doc.boxes[box_idx]
box_uid = _get_box_uid(box)

# Lazily initialize session BEFORE inject_box if _qe_session is None
# (or mismatched) while typing resumes on an active box:
if sess is None or sess.get("doc") is not self.current_doc or sess.get("box_uid") != box_uid:
    sess = {
        "file_path": str(self.current_file_path or ""),
        "doc": self.current_doc,
        "box_uid": box_uid,
        "box_index": box_idx,
        "old_snapshot": BoxSnapshot.from_box(box),
        "dirty": False,
    }
    self._qe_session = sess
```

**Canonical mutation path (aligned with `_on_dialogue_edited`, L12801):**
1. Read `new_tx = self.txt_quick_edit.get("1.0", "end-1c")`.
2. If `new_tx == box.clean_text`: return `False`.
3. Ensure `sess["old_snapshot"]` was captured prior to mutation (`if sess.get("old_snapshot") is None: sess["old_snapshot"] = BoxSnapshot.from_box(box)`).
4. Mutate via canonical **`self.current_doc.inject_box(box_idx, None, new_tx)`** — **NO `seg_texts`** — identical to `_on_dialogue_edited`. *(Note: manual typing does NOT block on `is_box_locked(box_idx)` per S09b Matrix Row 1; see §3.8.)*
5. Set `sess["dirty"] = True`, `sess["box_index"] = box_idx`, `_modified_boxes.add(box_idx)`, `_modified_box_uids.add(box_uid)`.
6. On first clean→dirty transition: `_mark_document_dirty(...)` + `_dirty_state_changed()`.
7. View-Aware Live Sync (preserve exactly):
   - `_patch_as_visible_card_body(box_idx)` in All Script with **0 `_render_continuous_view` calls**.
   - `_render_dialogue_preview_frame(updated_box.speaker, updated_box.clean_text)` when Dialogue Preview is ON.
   - `txt_dialogue` sync under `_suppress_continuous_events=True` + `edit_modified(False)` when Dialogue Preview is OFF.
   - `_update_char_overflow_indicator(updated_box.clean_text)`.
   - `_update_raw_view()`.

---

### 3.5 `_flush_quick_edit_session(self)` (L12481-12531) & Doc-Identity-Guarded Post-Flush Refresh

**Existing flush logic** (unchanged):
- If `sess is None`: return `True`.
- If `bottom_tab == "quick_edit"` and `_qe_seg_widgets` and `sess.get("doc") is self.current_doc`: run `self._on_quick_edit_changed()` to capture un-committed paste/edit text.
- If `not sess.get("dirty")`: return `True`.
- Validate `doc = sess.get("doc")` is `self.current_doc` and resolve `box_idx` by `box_uid`.
- Capture `new_snap = BoxSnapshot.from_box(updated_box)` and record **ONE** `BoxSnapshotReplaceDelta(old_snap → new_snap, source="quick_edit")` if `new_snap != old_snap`.

**Post-flush session refresh (with `doc is self.current_doc` guard):**
```python
# Refresh session baseline ONLY if the flushed doc is still active,
# Quick Edit widget is active/valid, and the same box remains active:
if (
    sess.get("doc") is self.current_doc
    and self._qe_seg_widgets
    and hasattr(self, "txt_quick_edit")
    and self.txt_quick_edit.winfo_exists()
    and box_idx == self.current_box_idx
):
    sess["old_snapshot"] = BoxSnapshot.from_box(updated_box)
    sess["box_index"] = box_idx
    sess["dirty"] = False
else:
    self._qe_session = None
```

This guarantees:
- **Multiple keystrokes in Session 1 → Flush 1 → Session 2 (same box) → Flush 2** produces **EXACTLY TWO** `BoxSnapshotReplaceDelta` entries (`undo_depth == 2`, zero per-keypress undo spam).
- **Undo #1** reverts Session 2 only.
- **Undo #2** restores the exact original 4-segment state via `replace_box`.

---

### 3.6 Complete Mandatory Flush Matrix

Every code path that modifies `current_doc` while Quick Edit may hold a dirty session must call `_flush_quick_edit_session()` **before** mutating the document:

| Method | Line | Current Status | S11c Action |
|--------|------|----------------|-------------|
| `_on_toggle_preview_compiled` | L7621 | ✅ Direct `_flush_quick_edit_session()` | No change |
| `_on_toggle_continuous_view` | L8780, L8805 | ✅ Direct | No change |
| `_flush_active_widget` | L9300 | ✅ Direct (central dispatch) | No change |
| `on_enter_raw_edit_mode` | L9862 | ✅ Via `_flush_active_widget()` | No change |
| `open_file` | L9453 | ✅ Via `_flush_active_widget()` | No change |
| `on_box_new` | L10726 | ✅ Direct | No change |
| `on_box_cut` | L10791 | ✅ Direct | No change |
| `on_box_paste` | L10988 | ✅ Direct | No change |
| `_on_as_card_lock_click` | L11923 | ✅ Direct | No change |
| `_on_as_box0_click` | L11941 | ✅ Direct | No change |
| `_on_as_box0_double_click` | L11954 | ✅ Direct | No change |
| `_on_as_card_click` | L11963 | ✅ Direct | No change |
| `_on_as_card_double_click` | L11978 | ✅ Direct | No change |
| `_switch_bottom_tab` | L12221 | ✅ Direct | No change |
| `_commit_speaker_edit` | L12541 | ✅ Direct | No change |
| `_navigate_pinned_speaker` | L12915 | ✅ Direct | No change |
| `on_prev_box` | L12952 | ✅ Direct | No change |
| `on_next_box` | L12977 | ✅ Direct | No change |
| `on_save` | L13548 | ✅ Direct | No change |
| `_jump_to_search_result` | L14337 | ✅ Direct | No change |
| `on_undo` / `on_redo` | L15164 / L15193 | ✅ Direct | No change |
| `close_file` | L15838 | ✅ Via `_flush_active_widget()` | No change |
| `on_reload` / `on_revert_box` | L13837 / L13359 | ✅ Via `open_file()` → `_flush_active_widget()` | No change |
| `_clear_card_registry` | L10240 | ✅ Sets `_qe_session = None` | No change |
| `on_toggle_lock_current_box` | L13016 | ✅ Calls `_update_views()` → `_refresh_quick_edit_pane()` (§3.3 flushes if dirty) | No change |
| **`on_paste_cross_box`** | **L18531** | ❌ Missing unconditional flush (`_commit_widget_edit` at L18418 is focus-dependent) | **ADD** `self._flush_quick_edit_session()` at entry |
| **`on_import_script`** | **L18544** | ❌ Missing unconditional flush | **ADD** `self._flush_quick_edit_session()` at entry |
| **`apply_auto_word_wrap`** | **L18877** | ⚠️ `_commit_widget_edit()` at L18889 is focus-dependent | **ADD** `self._flush_quick_edit_session()` after `_commit_widget_edit()` at L18889 |
| **`on_replace_next`** | **L14696** | ⚠️ Indirect (`_update_views()` runs *after* `inject_box` at L14741) | **ADD** `self._flush_quick_edit_session()` before mutating `current_doc` at L14726 |
| **`on_replace_all`** | **L14812** | ⚠️ Indirect (`_update_views()` runs *after* loop at L14877) | **ADD** `self._flush_quick_edit_session()` before loop at L14846 |
| **`on_clear_dialogue_skeleton`** | **L19024** | ⚠️ Indirect (`_update_views()` runs *after* loop at L19077) | **ADD** `self._flush_quick_edit_session()` before loop at L19041 |
| **`_on_mtl_drawer_apply_engine`** | **L17506** | ⚠️ Indirect | **ADD** `self._flush_quick_edit_session()` at entry |
| **`_on_mtl_all_script_apply_selected`** | **L17847** | ⚠️ Indirect | **ADD** `self._flush_quick_edit_session()` at entry |
| **`_on_mtl_all_script_apply_all`** | **L18031** | ⚠️ Indirect | **ADD** `self._flush_quick_edit_session()` at entry |
| **`ImportFromXUATDialog._on_apply_import`** | **L20767** | ⚠️ `self.app._commit_widget_edit()` at L20867 is focus-dependent (focus is in modal dialog) | **ADD** `self.app._flush_quick_edit_session()` right alongside `self.app._commit_widget_edit()` at L20867 |
| `_on_mtl_all_script_translate_all` | L17898 | ✅ OK (worker submit only; apply handlers flush) | No change |
| `_close_all_documents_without_prompt` | L15936 | ✅ OK (post-diff confirmation; clears registry/session) | No change |

---

### 3.7 Additional `misora.py` Updates

| Area | Current | S11c Change |
|------|---------|-------------|
| `destroy()` (L2688-2690) | Clears `_qe_seg_widgets`, `_qe_session` | **Keep** |
| `_apply_theme_and_fonts_live()` (L3264-3277) | Styles `_qe_seg_widgets` | **Update** to style `txt_quick_edit`, `lbl_qe_segs_badge`, `lbl_qe_placeholder` |
| `_update_bottom_tab_styles()` (L12213-12216) | Configures `qe_canvas["bg"]`, `qe_inner_frame["bg"]` | **Replace** with `txt_quick_edit["bg"]`, `lbl_qe_placeholder["bg"]` |

---

### 3.8 Post-Undo/Redo UI Refresh & S09b Lock-Parity Semantics

**Undo/Redo refresh path:**
- `on_undo()` (L15162) and `on_redo()` (L15193) call `_flush_quick_edit_session()`, apply the delta via `_apply_delta()`, and call `_update_views()` → `_refresh_quick_edit_pane()`.
- `_refresh_quick_edit_pane()` (§3.3) detects external model updates, syncs `txt_quick_edit` to `box.clean_text`, re-aligns `self._qe_session` safely, and updates `lbl_qe_segs_badge` (e.g., `"[4 segs]"` reappears when Undo restores a 4-segment split).

**S09b Translation Lock Matrix Parity (Row 1 = `ALLOWED`):**
- `on_toggle_lock_current_box()` (L13016-13055) only updates `_locked_boxes` / `_locked_box_uids` and refreshes views. Neither `txt_dialogue` nor `txt_quick_edit` is set to `state="disabled"`.
- **Manual typing in BOTH `_on_dialogue_edited` AND `_on_quick_edit_changed` is ALLOWED on a locked box** (`is_box_locked(idx) == True`), per the live-verified 12-row Translation Lock Operation Matrix in `PROJECT_STATE.md` (Row 1). Neither `_on_dialogue_edited` nor `_on_quick_edit_changed` blocks edits via `is_box_locked()`.
- Model/application-layer lock guards (`is_box_locked()`) apply exclusively to **automated, batch, and structural operations**: Speaker Rename (`_commit_speaker_edit`), Paste Replace (`on_paste_cross_box` / `_show_paste_preview_and_apply`), Cut Box (`on_box_cut`), MTL Apply (`_on_mtl_drawer_apply_engine`, `_on_mtl_all_script_apply_selected`, `_on_mtl_all_script_apply_all`, `on_translate_current_box`), Auto Word Wrap (`apply_auto_word_wrap`), Clear Dialogue Skeleton (`on_clear_dialogue_skeleton`), Replace Next/All (`on_replace_next`, `on_replace_all`), and XUAT Import (`ImportFromXUATDialog._on_apply_import`).
- **Pin ⊥ Lock independence preserved:** `_is_speaker_pinned` / `_pinned_speaker` and `_locked_box_uids` are strictly independent; toggling Lock never changes Pin and toggling Pin never changes Lock.

---

## 4. Explicit Test Matrix

### 4.1 `tests/test_v15_s11c_quick_edit_unified.py` (**NEW**)

> [!IMPORTANT]
> **Execution Order:** Created FIRST. All 4 Defect/Behavior Probes must **FAIL** and both Regression Guards must **PASS** against the unpatched codebase before patching `misora.py`. After patching, all 6 must **PASS**.

#### Probe 1: `test_probe_1_quick_edit_uses_single_unified_textbox_with_box_clean_text`

- **Type:** Failing-first Defect Probe (`FAIL` pre-patch, `PASS` post-patch)
- **Setup:** Open a 4-segment box, switch to Quick Edit tab.
- **Assertions:**
  1. `hasattr(self.app, "txt_quick_edit")` and `self.app.txt_quick_edit.winfo_exists()`
  2. `str(self.app.txt_quick_edit.cget("wrap")) == "none"` (matches Q-03/C-3 wrap contract alongside `qe_scroll_x`)
  3. `str(self.app.txt_quick_edit.cget("state")) == "normal"`
  4. `len(self.app._qe_seg_widgets) == 1` and `self.app._qe_seg_widgets[0] is self.app.txt_quick_edit`
  5. `self.app.txt_quick_edit.get("1.0", "end-1c") == box.clean_text`
  6. `self.app.lbl_qe_segs_badge.cget("text") == "[4 segs]"` (and `""` on a 1-segment box)
  7. Zero `line_overflow` / `gutter_overflow` tags on `txt_quick_edit`, and no `qe_canvas` / `qe_inner_frame` attributes.

#### Probe 2: `test_probe_2_manual_dialogue_vs_quick_edit_ast_and_binary_parity`

- **Type:** Failing-first Behavior Probe (`FAIL` pre-patch, `PASS` post-patch)
- **Setup:** Build identical binary-backed 4-segment documents containing **`{playername}`** (`{0}`), **`voice_cue`**, **`extra_args`** (`["ex0"]..["ex3"]`), and **`raw_breaks`** (`\n` across segments). Edit Doc A via Main Dialogue (`txt_dialogue` + `_on_dialogue_edited()`) and Doc B via Quick Edit (`txt_quick_edit` + `_on_quick_edit_changed()` + `_flush_quick_edit_session()`) with the same replacement text containing `{playername}` and multiline breaks.
- **Assertions:**
  1. `doc_a.boxes[idx].clean_text == doc_b.boxes[idx].clean_text`
  2. `doc_a.boxes[idx].speaker == doc_b.boxes[idx].speaker` and `doc_a.boxes[idx].voice_cue == doc_b.boxes[idx].voice_cue`
  3. Normalized `{playername}` → `{0}` in rendered records and binary output in both paths.
  4. Identical **`raw_breaks`** (`[s.raw for s in doc_a.boxes[idx].segs] == [s.raw for s in doc_b.boxes[idx].segs]`) and **`extra_args`** (`[s.record.args[2:] for s in doc_a.boxes[idx].segs] == [s.record.args[2:] for s in doc_b.boxes[idx].segs]`).
  5. **Full `StoryDocument.records` equality:** `len(doc_a.records) == len(doc_b.records)` and `[(r.cmd_id, r.cmd_name, r.category, r.args) for r in doc_a.records] == [(r.cmd_id, r.cmd_name, r.category, r.args) for r in doc_b.records]`.
  6. **Byte-identical binary output:** `doc_a.to_binary() == doc_b.to_binary()`.

#### Probe 3: `test_probe_3_pre_mutation_snapshot_undo_restores_exact_4_segments_and_binary_roundtrip`

- **Type:** Failing-first Behavior Probe (`FAIL` pre-patch, `PASS` post-patch)
- **Setup:** Open a 4-segment box + neighbor box (lock the neighbor box so `_locked_box_uids` has a known entry; record `orig_binary = doc.to_binary()`, `orig_segs = [s.text for s in box.segs]`, `orig_jp_map = dict(self.app._original_jp_by_uid)`, `orig_cache = dict(self.app.sync_manager.jp_source_cache)`, `orig_locked = set(self.app._locked_box_uids)`).
- **Sequence & Assertions (sequential-session):**
  1. **Session 1 (multiple keystrokes before flush):**
     - Keystroke 1a (`"Step 1"` → `_on_quick_edit_changed()`) → `undo_depth == 0`.
     - Keystroke 1b (`"Step 1 + 2"` → `_on_quick_edit_changed()`) → `undo_depth == 0`.
     - Keystroke 1c (`"Session 1 Final"` → `_on_quick_edit_changed()`) → `undo_depth == 0` (**zero per-keypress undo spam**).
  2. **Flush 1:** `_flush_quick_edit_session()` → **`undo_depth == 1`** (exact equality). Inspect `doc.records` directly for edited args and **no stale `raw_breaks`**.
  3. **Session 2 (same box, no navigation):** Edit text to `"Session 2 Final"` → `_on_quick_edit_changed()` → **Flush 2** (`_flush_quick_edit_session()`) → **`undo_depth == 2`** (exact equality, not `>= 2`). Inspect `doc.records` directly.
  4. **Undo #1:** Reverts Session 2 only → `box.clean_text == "Session 1 Final"`, `doc.records` matches Session 1 state.
  5. **Undo #2:** Restores exact original state:
     - `[s.text for s in box.segs] == orig_segs` and `len(box.segs) == 4`
     - `doc.records` raw strings (`s.raw` / `r.args`) match original 4 records with zero stale breaks
     - `doc.to_binary() == orig_binary`
     - `lbl_qe_segs_badge.cget("text") == "[4 segs]"`
  6. **Redo #1 → Redo #2:** `doc.to_binary()` matches post-Session-2 binary and `doc.records` matches post-Session-2 state.
  7. **Metadata & Cache Survival:** Assert `self.app._original_jp_by_uid == orig_jp_map`, `self.app.sync_manager.jp_source_cache` still contains all original keys/values intact, and `self.app._locked_box_uids == orig_locked` after Edit, Undo #1, Undo #2, Redo #1, and Redo #2.

#### Probe 4: `test_probe_4_s09b_lock_parity_and_view_aware_sync_preserved`

- **Type:** Failing-first Behavior Probe (`FAIL` pre-patch, `PASS` post-patch)
- **Setup:** Open a multi-segment box, switch to All Script + Quick Edit tab.
- **Assertions:**
  1. **Lock-Toggle & Live Locked-Box Typing Parity (S09b Row 1 ALLOWED):**
     - Toggle Translation Lock ON (`on_toggle_lock_current_box()`).
     - Assert `self.app.is_box_locked(idx) is True`, `str(self.app.txt_quick_edit.cget("state")) == "normal"`, and `str(self.app.txt_dialogue.cget("state")) == "normal"`.
     - **Actually type via Quick Edit while locked:** edit `txt_quick_edit` to `"Locked Quick Edit"` → `_on_quick_edit_changed()` → `_flush_quick_edit_session()`. Assert `doc.boxes[idx].clean_text == "Locked Quick Edit"` and `self.app.is_box_locked(idx) is True`.
     - **Actually type via Main Dialogue while locked:** switch to Dialogue mode (Preview OFF), edit `txt_dialogue` to `"Locked Dialogue Edit"` → `_on_dialogue_edited()`. Assert `doc.boxes[idx].clean_text == "Locked Dialogue Edit"` and `self.app.is_box_locked(idx) is True`.
     - Undo both edits; assert `is_box_locked(idx)` remains `True`.
     - Verify blocked automated op on locked box (e.g., speaker rename `_commit_speaker_edit()` returns `False`).
  2. **Pin ⊥ Lock Independence:**
     - Toggle Lock ON/OFF while `_is_speaker_pinned` is toggled ON/OFF; verify Pin state/target and Lock state never interfere.
  3. **View-Aware Sync:**
     - In All Script: edit `txt_quick_edit` → card body updates in-place with **0 `_render_continuous_view` calls**.
     - Dialogue Preview ON / OFF: syncs `txt_dialogue_preview` (`state="disabled"`) and `txt_dialogue` without All Script rebuilds.
  4. **Ctrl+Z / Ctrl+Y Single-Fire & Flush Verification:**
     - With a dirty (unflushed) Quick Edit session in `txt_quick_edit`, dispatch `<Control-z>` via widget / `MisoraShortcuts` with `patch.object(self.app, "on_undo", wraps=self.app.on_undo)` and `<Control-y>` with `patch.object(self.app, "on_redo", wraps=self.app.on_redo)`: assert each handler executes **exactly once (`call_count == 1`)** per shortcut (no double-fire between `MisoraShortcuts` bindtag, widget `<Control-z>`/`<Control-y>`, and root bindings), flushes cleanly, and leaves `txt_quick_edit` synced.

#### Guard 1: `test_guard_1_raw_commands_tab_name_and_box0_quick_edit_safety`

- **Type:** Regression Guard (**MUST PASS both pre-patch AND post-patch**)
- **Assertions:**
  1. `self.app.btn_tab_raw_commands.cget("text") == "Raw Commands"` and `self.app.lbl_raw_title.cget("text") == "Raw Commands"`.
  2. Activate Box 0 (`is_box0_active = True`) on Quick Edit tab:
     - Assert `len(self.app._qe_seg_widgets) == 0` (works on both pre-patch multi-seg code and post-patch unified code).
     - Conditionally **only if `hasattr(self.app, "txt_quick_edit")`**: assert `not self.app.txt_quick_edit.winfo_ismapped()` and `bool(self.app.lbl_qe_placeholder.winfo_ismapped())` (and `self.app.lbl_qe_segs_badge.cget("text") == ""`).
  3. Binary round-trip (`StoryDocument.from_binary(doc.to_binary())`) preserves Box 0 metadata and all story records.

#### Guard 2: `test_guard_2_s08_stress_quick_edit_benchmark_compatibility`

- **Type:** Regression Guard (**MUST PASS both pre-patch AND post-patch**)
- **Assertions:**
  1. Open multi-box document in All Script + Quick Edit tab.
  2. Assert `len(self.app._qe_seg_widgets) >= 1` and `isinstance(self.app._qe_seg_widgets[0], tk.Text)`.
  3. Conditionally **only if `hasattr(self.app, "txt_quick_edit")`**: assert `self.app._qe_seg_widgets[0] is self.app.txt_quick_edit`.
  4. Edit via `self.app._qe_seg_widgets[0]`, call `self.app._on_quick_edit_changed()`, assert active All Script card body contains the edited text, call `self.app._flush_quick_edit_session()`, and assert completion well within the stress timing envelope.

---

### 4.2 `tests/test_v15_s10_all_script_quick_edit.py` — `test_probe_5` Migration

**Line-level migration plan (zero assertion weakening):**

| Current Line(s) | Current Code | Migrated Code | Rationale |
|-----------------|--------------|---------------|-----------|
| L389-392 | `len(seg_widgets) == 4`, per-seg `line_overflow` check | `self.assertEqual(len(seg_widgets), 1, ...)`, single `txt_quick_edit` `line_overflow` check + `[4 segs]` badge check | 4 split widgets → 1 unified widget |
| L396-406 | Edit `seg_widgets[0]`, `[1]`, `[3]` individually | Edit `seg_widgets[0]` (`txt_quick_edit`) with unified edited string (including `{playername}` & `\n`) | Single unified box |
| L410-416 | Card body verification + `undo_depth == 0` before flush + `undo_depth == 1` after `on_next_box()` | **Keep unchanged** | No weakening |
| L419-434 | Per-seg record & binary round-trip inspection (assuming `seg_texts` distribution) | **Update** expected `box0_recs` & `StoryDocument.from_binary()` segment args to match canonical `inject_box(0, None, new_tx)` parity with `_on_dialogue_edited` (and add cross-check against a second doc edited via `txt_dialogue`) | Canonical `inject_box` parity |
| L436-443 | `on_undo()` restores `orig_bin`; `on_redo()` restores edited binary | **Keep `on_undo()` == `orig_bin` unchanged**; update `on_redo()` expected segment args to match canonical `inject_box` | Exact `BoxSnapshotReplaceDelta` restoration |
| L449-475 | Dialogue Preview sync, View-Aware sync (`spy_render == 0`), `_rebuild_quick_edit_widgets` spy on Raw tab | **Keep unchanged** | No weakening |
| L478-504 | S09b Lock parity + Pin ⊥ Lock independence + locked Quick Edit typing + locked Undo + blocked speaker rename | **Keep unchanged** (`self.app._qe_seg_widgets[0]` resolves to `txt_quick_edit` cleanly) | No weakening |

---

### 4.3 `tests/test_v15_s08_release_gate_stress.py` — `test_stress_4` (**Inspect-Only / Untouched**)

`test_stress_4` (L339-345) uses `self.app._qe_seg_widgets[0]`, `_on_quick_edit_changed()`, card body verification, and `_flush_quick_edit_session()`. With `self._qe_seg_widgets = [self.txt_quick_edit]`, **zero lines in `tests/test_v15_s08_release_gate_stress.py` need modification**. It remains **inspect-only / untouched** and will be run unmodified during verification.

---

## 5. Verification Plan (Post-`Proceed`)

### 5.1 Execution Order

1. **Confirm S11b2 Commit Gate & Record Baseline:** Verify clean pre-S11c `HEAD` (`git rev-parse HEAD`, `git status --short`), re-run `py -3.12 -m unittest discover -s tests -v` to confirm 451 tests matching §1.3.
2. **Create `tests/test_v15_s11c_quick_edit_unified.py` FIRST** and run:
   `py -3.12 -m unittest tests.test_v15_s11c_quick_edit_unified -v`
   - Confirm all 4 probes **FAIL** and both guards **PASS** pre-patch.
3. **Patch** `__init__.py` (`"1.4.13"`), `misora.py`, and migrate `tests/test_v15_s10_all_script_quick_edit.py` (`tests/test_v15_s08_release_gate_stress.py` remains untouched).
4. **Verify targeted suites + `compileall`:**
   ```
   py -3.12 -m compileall -q __init__.py misora.py core assets tests
   py -3.12 -m unittest tests.test_v15_s11c_quick_edit_unified tests.test_v15_s10_all_script_quick_edit tests.test_v15_s08_release_gate_stress tests.test_v15_s09_core_fixes_54d -v
   ```
5. **Run full discovery:** `py -3.12 -m unittest discover -s tests -v` (confirm new tests pass and zero regressions against the committed S11b2 baseline).
6. **Close Out:** Update `CHANGELOG.md` and `PROJECT_STATE.md` with exact counts, updated S08/S10 benchmarks, and Manual Windows QA checklist.

### 5.2 Manual Windows QA Checklist (Post-Implementation)

- [ ] Open a multi-segment bundle file → Quick Edit tab shows single `txt_quick_edit` (`wrap="none"`) with `box.clean_text`
- [ ] `lbl_qe_segs_badge` shows `"[4 segs]"` for 4-segment box, `""` for 1-segment box
- [ ] Type in `txt_quick_edit` → All Script card body updates live (no full rebuild)
- [ ] Type in `txt_quick_edit` → `txt_dialogue` syncs immediately
- [ ] Horizontal scrollbar (`qe_scroll_x`) appears when text exceeds widget width
- [ ] Type multiple keystrokes in `txt_quick_edit` → `Ctrl+Z` flushes + undoes as 1 transaction (`on_undo` runs once, no double-undo)
- [ ] Edit 1 → Flush (focus out) → Edit 2 (same box, no navigation) → `Ctrl+Z` → Edit 2 reverted → `Ctrl+Z` → original 4 segments restored (`"[4 segs]"` badge reappears)
- [ ] Toggle Translation Lock ON → `txt_quick_edit` and `txt_dialogue` remain `state="normal"` and editable; Pin ⊥ Lock remain independent
- [ ] Box 0 active → Quick Edit hides `txt_quick_edit` and shows `lbl_qe_placeholder`
- [ ] Replace Next / Replace All / MTL Apply / Paste Across Boxes / Auto Word Wrap / Clear Skeleton / XUAT Import → pending Quick Edit edits flush cleanly before batch edits and UI syncs afterward

---

## 6. Forbidden Files & Out-of-Scope Reminders

**Forbidden Files (DO NOT MODIFY):** `core/*.py`, `assets/*`, `requirements.txt`, `misora_config.json`, `backups/`.

**Out of Scope (DEFER):**
- `Q-06`–`Q-12` Import UX (`S11d`)
- `Q-03`/`Q-05`/`Q-13`–`Q-17` UI Polish (`S11e`)
- `S12` Release Gate
- Track B
- `v1.5.0` release (`ON HOLD`)
