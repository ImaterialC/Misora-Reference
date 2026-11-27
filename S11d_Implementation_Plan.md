# S11d (v1.4.14) — Import from XUAT UX & Editor Productivity
## Implementation Plan — Symbol-Bound (Rev 3)

> [!IMPORTANT]
> **Rev 3** — Applies all 5 surgical fixes requested after Rev 2 review for final ChatGPT & Qwen clearance. Requires explicit **`Proceed`** from the Project Lead before ANY file is edited. Version `1.4.14` bumps from verified `1.4.13` (S11c). `v1.5.0` remains ON HOLD.

---

## Pre-Session Snapshot

| Item | Value |
|---|---|
| **HEAD** | `ac61a2407db6e6f418bd99d960cdb15c3e6b63c7` |
| **`git status --short`** | `M assets/icons/BoxInsert.png`, `?? assets/icons/BoxReplace.png` |
| **Python** | 3.12.10 |
| **`__version__`** | `"1.4.13"` (S11c complete) |
| **S11c Baseline** | 460 tests discovered (417 PASS, 35 SKIP, 6 pre-existing FAIL, 2 pre-existing ERROR; 0 regressions) |

---

## Allowed File Ownership (S11d)

| File | Action |
|---|---|
| `__init__.py` | Bump `"1.4.13"` → `"1.4.14"` |
| `misora.py` | Q-06 through Q-12 edits |
| `core/xuat_cleanup.py` | Add `("summary", "Box #0 (Synopsis)")` to Pass 3 `meta_val_to_labels` (L503) and update docstring/comments (L461, L588); **signature of `classify_cleanup_candidates(..., progress_cb)` unchanged** |
| `CHANGELOG.md` | Add `### S11d (v1.4.14)` section |
| `PROJECT_STATE.md` | Record S11d results |
| `tests/test_v15_s11d_import_ux_productivity.py` | NEW — 4 failing-first probes + 2 regression guards |
| `tests/test_v15_s11_xuat_archiving_progress.py` | Update Synopsis assertions inside existing `test_probe_4` (zero extra `test_*` methods) |

**Forbidden:** `core/story_ast.py`, `core/bundle_io.py`, `core/script_codec.py`, `core/xuat_index.py`, `core/xunity_sync.py`, `core/word_wrap.py`, `core/mtl_engine.py`, `core/undo_journal.py`, `assets/*`, `requirements.txt`, `misora_config.json`, `backups/`.

---

## Phase 1 — `Q-06`: MouseWheel Label Propagation in `ImportFromXUATDialog`

### Problem (Verified on Disk)
`_on_outer_mousewheel` is bound on `self.list_canvas` (L20230), `self.rows_frame` (L20231), individual `card` frames (L20408), `hdr` frames (L20412), and `pair_frame` (L20495) — but NOT on:
- `tk.Label` children inside `hdr` (header text L20414, lock badge L20423, `lbl_provenance` L20447, `lbl_dup_counter` L20456)
- `tk.Label` children inside `left_hdr` (L20501) and `right_hdr` (L20536)
- `tk.Checkbutton` `cb_skip` (L20432)
- Section header labels created by `_build_section_header` (inner `tk.Label` at L20358 — only `hdr` gets the bind, not its child label)
- Duplicate controls (`btn_prev`, `btn_next`, `scope_cmb`) and any empty-state / no-match placeholder `tk.Label` created inside `rows_frame`

Tkinter does **not** bubble `<MouseWheel>` events from child labels or widgets up to parent frames (`rows_frame` / `list_canvas`).

### Plan
**Symbol: `_create_paired_box_row()` (L20367), `_build_section_header()` (L20354), `_populate_rows()` (L20597)**

1. **Add recursive mousewheel propagator `_bind_mousewheel_recursive(widget)`**:
   ```python
   def _bind_mousewheel_recursive(self, widget: tk.Misc) -> None:
       # Skip tk.Text so focus-gated inner vertical scroll & Shift+Wheel horizontal
       # scroll from _bind_paired_box_events() on txt_left/txt_right are never clobbered.
       # All other children — including tk.Label, tk.Checkbutton, ttk.Button, and
       # ttk.Combobox (scope_cmb) — bind to _on_outer_mousewheel (returns "break").
       if isinstance(widget, tk.Text):
           return
       widget.bind("<MouseWheel>", self._on_outer_mousewheel)
       for child in widget.winfo_children():
           self._bind_mousewheel_recursive(child)
   ```

2. **`scope_cmb` explicit decision (Rev 3 Fix 3):**
   - `scope_cmb` (`ttk.Combobox`, `state="readonly"`) **IS bound** via `scope_cmb.bind("<MouseWheel>", self._on_outer_mousewheel)`.
   - On Windows, `TCombobox` class bindings change the selected dropdown value (`"This Box"` → `"This Story"` → `"Global"`) when scrolled with the wheel. Because the widget instance bindtag executes before the `TCombobox` class bindtag and `_on_outer_mousewheel` returns `"break"`, binding `scope_cmb` prevents accidental scope mutation while scrolling AND smoothly scrolls the dialog canvas.

3. **Bind all cards, section headers, and empty-state / filter placeholder `tk.Label`s inside `rows_frame`**:
   - In `_create_paired_box_row()`, after building the complete `card` frame and calling `_bind_paired_box_events()` on `txt_left`/`txt_right`, call `self._bind_mousewheel_recursive(card)` (replacing the partial `.bind("<MouseWheel>", ...)` on `card`, `hdr`, `pair_frame`).
   - In `_make_tristate_group_header()` / `_build_section_header()`, after creating `hdr` and its children, call `self._bind_mousewheel_recursive(hdr)`.
   - Explicitly bind any empty-state / no-match placeholder `tk.Label` created inside `self.rows_frame` (and run `self._bind_mousewheel_recursive(child)` on any placeholder label when created in `_populate_rows()` or `_set_filter()`, e.g., when a filter yields zero visible rows or no boxes exist) to `self._on_outer_mousewheel`, since Tkinter does not bubble wheel events from child labels to `rows_frame`.

4. **Cleanup in `_on_close()`**: Existing L21190 unbinds `list_canvas` and `rows_frame`; child widgets are destroyed with the dialog.

### Invariant Check
- `txt_left` / `txt_right` (`tk.Text`) are explicitly skipped by `isinstance(widget, tk.Text)`, preserving S22 focus-gated inner scroll and `Shift+MouseWheel` horizontal scroll. ✓
- `scope_cmb` returns `"break"` via `_on_outer_mousewheel`, preventing accidental dropdown changes while scrolling. ✓
- Empty-state placeholder labels inside `rows_frame` are explicitly bound to `_on_outer_mousewheel`. ✓

---

## Phase 2 — `Q-07`: Per-Group Tri-State Select All Headers

### Plan
**Symbol: `_make_tristate_group_header()`, `_on_group_select_all()`, `_update_group_header_state()`, `_populate_rows()` (L20597), `_create_paired_box_row()` (L20367)**

1. **Inspectable state tracking & re-entrancy guard**:
   ```python
   # In ImportFromXUATDialog.__init__():
   self._group_select_states: Dict[str, str] = {}           # group_key -> "none" | "partial" | "all"
   self._group_select_buttons: Dict[str, ttk.Button] = {}   # group_key -> header toggle button
   self._bulk_updating_group: bool = False                  # O(1) re-entrancy guard
   ```

2. **Clear state at the top of `_populate_rows()` (and in `_on_close()`) (Rev 3 Fix 4)**:
   - Alongside `self._rows.clear()`, `self._metadata_rows.clear()`, and `self._actor_rows.clear()`, explicitly execute:
     ```python
     self._group_select_buttons.clear()
     self._group_select_states.clear()
     ```
   - Guarantees zero stale button references or stale states after `_on_reload_index()`.

3. **Single-visual tri-state group header `_make_tristate_group_header(title, group_key, t)`**:
   - Uses a `ttk.Button` (NOT `tk.Checkbutton`, avoiding double native checkbox + Unicode symbol rendering):
     ```python
     btn_group_sel = ttk.Button(
         hdr,
         text="☐ All",
         style="Small.TButton",
         width=7,
         command=lambda gk=group_key: self._on_group_select_all(gk),
     )
     btn_group_sel.pack(side="right", padx=(4, 8))
     create_tooltip(btn_group_sel, f"Select or deselect all eligible rows in {title}")
     self._group_select_buttons[group_key] = btn_group_sel
     self._group_select_states[group_key] = "none"
     ```
   - `create_tooltip(...)` attached for S8b4 UI-polishing compliance.
   - Calls `self._bind_mousewheel_recursive(hdr)` for Q-06 propagation.

4. **`_on_group_select_all(group_key)` with `O(1)` re-entrancy guard**:
   ```python
   def _on_group_select_all(self, group_key: str) -> None:
       current_state = self._group_select_states.get(group_key, "none")
       rows = self._get_group_rows(group_key)
       # partial/all -> deselect all (var_skip=True); none -> select all (var_skip=False)
       target_skip = current_state != "none"

       self._bulk_updating_group = True
       try:
           for row_dict in rows:
               if row_dict.get("is_locked", False):
                   continue
               if not row_dict.get("candidates"):
                   continue
               row_dict["var_skip"].set(target_skip)
       finally:
           self._bulk_updating_group = False
       self._update_group_header_state(group_key)
   ```

5. **`_update_group_header_state(group_key)` & Missing/Locked/Filter semantics**:
   - **Missing (0-candidate) rows**: Excluded (`not r.get("candidates")`) — never eligible for select/deselect.
   - **Locked rows**: Excluded (`r.get("is_locked", False)`) — always auto-skipped, never toggled or counted.
   - **Active filters**: Operates across **ALL** rows in the owning group regardless of filter visibility (Pre-Apply iterates all non-skipped rows, keeping counts consistent).
   - Cycles visual state strictly via `self._group_select_states[group_key]` ∈ `{"none", "partial", "all"}` and `btn.configure(text=...)` ∈ `{"☐ All", "▣ All", "☑ All"}`; disables button when `eligible` is empty.
   - Individual `var_skip.trace_add("write", ...)` triggers `_update_group_header_state(group_key)` only when `not self._bulk_updating_group`.

---

## Phase 3 — `Q-08`: Multi-Line Synopsis Metadata Import Including Empty Synopsis

### Live Core Signature Audit (Read-Only, Forbidden Files Unmodified)
- **`StoryDocument.get_metadata()`** (`core/story_ast.py` L399–413): Returns `{"title": title, "subtitle": subtitle, "summary": summary}` where `summary = game_to_xuat(r.args[0])` from active `cmd_id == 1` record.
- **`StoryDocument.set_metadata(title=None, subtitle=None, summary=None)`** (`core/story_ast.py` L415–453): All `Optional[str]`; `summary` converts via `xuat_to_game(summary, self.break_char)` and calls `self._rebuild_boxes()`.
- **`MetadataDelta`** (`core/undo_journal.py` L88–97): Fields `(file_path, old_title, new_title, old_subtitle, new_subtitle, old_summary, new_summary)`.
- **`_apply_delta()`** (`misora.py` L15394–15407): Already passes `summary=(delta.old_summary if reverse else delta.new_summary)` into `set_metadata(...)`.

### `_original_metadata_by_path` Lifecycle & Normalized Path Keying (Rev 3 Fix 2)

1. **Normalized key helper `_norm_meta_path_key(file_path)`**:
   - Uses identical normalization as `ImportFromXUATDialog._norm_file_str` (`os.path.normcase(os.path.normpath(str(Path(fp).resolve())))`).
   - Initialized in `MisoraApp.__init__`: `self._original_metadata_by_path: Dict[str, Dict[str, str]] = {}`.

2. **Capture & Cache Lifecycle (strictly preserving immutable JP snapshot)**:
   - **`open_file()` non-cache load / reload** (`staged["kind"] != "cache"` — fresh disk load OR `reload_from_disk=True` including `on_reload()`):
     - `_prune_document_caches()` executes at L9613 (clearing any stale snapshot on `reload_from_disk=True`).
     - Right alongside `self.open_documents[file_path] = staged["cache"]` (L9617), if `doc is not None` and `callable(getattr(doc, "get_metadata", None))`:
       - Compute `orig_meta = dict(doc.get_metadata() or {})`.
       - Store `staged["cache"]["original_metadata"] = dict(orig_meta)`.
       - Store `self._original_metadata_by_path[_norm_meta_path_key(file_path)] = dict(orig_meta)`.
   - **`open_file()` cache-hit tab switch** (`staged["kind"] == "cache"`, L9543):
     - **NEVER overwrite** `_original_metadata_by_path[norm_k]` with live edited `doc.get_metadata()`.
     - Only backfill if missing from cache entry (`if norm_k not in self._original_metadata_by_path and isinstance(entry.get("original_metadata"), dict): self._original_metadata_by_path[norm_k] = dict(entry["original_metadata"])`).
   - **`_save_active_document_state()`** (L13830):
     - Preserves `entry["original_metadata"]` unchanged (or copies `self._original_metadata_by_path.get(norm_k)` if absent — never copies live edited `doc.get_metadata()`).
   - **`close_file()` & `_close_all_documents_without_prompt()` & `_prune_document_caches()`**:
     - `_prune_document_caches(file_path, doc, ...)` pops `_norm_meta_path_key(file_path)` from `self._original_metadata_by_path` (when `fp_str` is non-empty).
     - Prevents unbounded map growth / memory leaks across repeated open/close cycles (e.g., `S08 Stress 1`), while `on_reload()` (`reload_from_disk=True`) prunes then re-captures fresh disk metadata cleanly.

### 4-Tuple `meta_fields` Lookup & Multi-Line Row Plan (Rev 3 Fix 2)

3. **`_populate_rows()` uses a 4-tuple `(field_key, label, display_text, lookup_key)`**:
   ```python
   meta = doc.get_metadata() if callable(getattr(doc, "get_metadata", None)) else {}
   orig_meta_map = getattr(self.app, "_original_metadata_by_path", {})
   norm_fp = self._norm_file_str(self.app.current_file_path)
   orig_meta = orig_meta_map.get(norm_fp, {})
   meta_fields: List[Tuple[str, str, str, str]] = []

   if meta.get("title"):
       meta_fields.append(("title", "Title (Box 0 Metadata)", meta["title"], meta["title"]))
   if meta.get("subtitle"):
       meta_fields.append(("subtitle", "Subtitle / Outline (Box 0 Metadata)", meta["subtitle"], meta["subtitle"]))

   current_summary = meta.get("summary", "") or ""
   original_jp_summary = orig_meta.get("summary", "") or ""
   synopsis_key = original_jp_summary or current_summary
   if synopsis_key:
       meta_fields.append(("summary", "Synopsis (Box 0 Metadata)", current_summary, synopsis_key))
   ```
   - Loop unpacks `for m_field, m_label, m_display, m_lookup_key in meta_fields:`
   - `m_lookup = self.xuat_index.lookup_candidates(m_lookup_key)` — ALWAYS looks up `synopsis_key` (`original_jp_summary` if present, else `current_summary`), even when `current_summary == ""` in-editor!
   - `left_text=m_display`, `norm_key=normalize_xuat_key(m_lookup_key, strip_ngui=True)`, `extra_data={"field": m_field, "orig_value": m_display}`.
   - Case outcomes:
     - **(a)** Genuinely empty synopsis with zero source key (`original_jp_summary == ""` and `current_summary == ""`) → skipped (no row built).
     - **(b)** Non-empty JP synopsis → row built and XUAT match resolved.
     - **(c)** Story opened with JP synopsis then cleared to `""` in-editor → left pane shows `""` (`m_display == ""`), right pane shows XUAT match via `m_lookup_key == original_jp_summary`, and `chosen.value != ""` triggers import!

4. **Multi-line Synopsis UI & U-18 Box 0 Immunity**:
   - `_create_paired_box_row()` accepts `wrap_mode: str = "none"` (lines param already exists).
   - For `m_field == "summary"`, call with `lines=5`, `wrap_mode="word"`, section header `"Story Metadata (Title, Subtitle: 1-line × 54d; Synopsis: multi-line)"`.
   - **U-18 Box 0 Immunity**: Skip 54d red overflow badges / markers (`lbl_left_overflow` / `lbl_right_overflow` stay `""`) when `extra_data.get("field") == "summary"` (including inside `_select_section_candidate()`!). Auto Word Wrap in `_on_apply_import()` strictly applies only to dialogue boxes `0..N-1` (never Box 0 `summary`).
   - Enable focus-gated inner vertical scroll for synopsis rows when content exceeds 5 lines (pass `has_v=(lines >= 3 and left_text.count("\n") >= lines)` or `has_v=(m_field == "summary")` to `_bind_paired_box_events`, which works cleanly with `tk.Text` skipped in `_bind_mousewheel_recursive`).

5. **`_on_apply_import()`**:
   - Pre-Apply summary lists all `meta_plan` keys including `"Summary"`/`"Synopsis"` (`", ".join("Synopsis" if k == "summary" else k.capitalize() for k in meta_plan)`).
   - Pass `new_summary = meta_plan["summary"][1] if "summary" in meta_plan else None` to `doc.set_metadata(title=new_title, subtitle=new_sub, summary=new_summary)`.
   - Record `MetadataDelta(..., old_summary=meta_before.get("summary", ""), new_summary=(new_summary if new_summary is not None else meta_before.get("summary", "")))`.
   - Include Synopsis in `applied_records` (`box_index=-1`) for post-import archiving.

6. **Pass 3 Multiline Synopsis Verification in `core/xuat_cleanup.py` (Rev 3 Fix 1)**:
   - Verified on disk: `StoryDocument.get_metadata()` (`core/story_ast.py` L410) returns `summary = game_to_xuat(r.args[0])`, which normalizes in-game breaks (`\n`, `<br>`) to real newlines `"\n"` (`chr(10)`).
   - Verified on disk: `core/xuat_index.py` L449 computes `entry.value = unescape_xuat_value(v_part)`, converting escaped `\n` (odd backslash parity) in XUAT `.txt` files to real newlines `"\n"` (`chr(10)`).
   - Pass 3 (`core/xuat_cleanup.py` L618, L621) checks `entry.value in meta_val_to_labels` and `xuat_index.lookup_by_value(entry.value)`. Because both `meta["summary"]` and `entry.value` normalize line breaks to real `"\n"`, multi-line Synopsis matches cleanly and deterministically when `("summary", "Box #0 (Synopsis)")` is added to L503! Zero `tkinter`/`misora` imports added.

---

## Phase 4 — `Q-09`: Remove Archiving Sub-Header Leftover & Clarify Pass 1/3–3/3 Progress Labels

### Verified `total_steps` & `_tick` Math in `core/xuat_cleanup.py` (Rev 3 Fix 1)
Quoted from `core/xuat_cleanup.py` L510–524 & L677–680:
```python
entries = getattr(xuat_index, "entries", ())
total_steps = max(1, len(entries) * 3)
processed_steps = 0

def _tick(step_idx: int) -> bool:
    nonlocal processed_steps
    processed_steps += 1
    if cancel_event is not None and cancel_event.is_set():
        return True
    if progress_cb is not None and (step_idx == 0 or (processed_steps % 100 == 0)):
        try:
            progress_cb(processed_steps, total_steps)
        except Exception:
            pass
    return False
```
- Pass 1 loops `for i, entry in enumerate(entries):` calling `_tick(i)` (`processed_steps` = `1..N`, where `N = len(entries)`).
- Pass 2 loops `for i, entry in enumerate(entries):` calling `_tick(i)` (`processed_steps` = `N+1..2N`).
- Pass 3 loops `for i, entry in enumerate(entries):` calling `_tick(i)` (`processed_steps` = `2N+1..3N`).
- L679 invokes final `progress_cb(total_steps, total_steps)`.

**Mathematical check:**
- If `len(entries) == 0`: `total_steps == 1` (`total_steps < 3` and `total_steps % 3 != 0`).
- If `len(entries) >= 1`: `total_steps == 3 * N` strictly, with equal pass boundaries of `N` steps each.
- **Boundary off-by-one fix**: When `N % 100 == 0` (e.g., `N = 100`, `total = 300`), `_tick` fires `progress_cb(100, 300)` at the end of Pass 1. Naive `processed // N` would give `1` (wrongly showing Pass 2/3 at step `0/100`!). Using 1-based `(processed - 1) // entries_per_pass`:
  - `processed = 1..100` → `(processed - 1) // 100 == 0` → **Pass 1/3** (`1/100` .. `100/100`)
  - `processed = 101..200` → `(processed - 1) // 100 == 1` → **Pass 2/3** (`1/100` .. `100/100`)
  - `processed = 201..300` → `(processed - 1) // 100 == 2` → **Pass 3/3** (`1/100` .. `100/100`)

### Plan
1. **Remove sub-header leftover** (`XuatCleanupDialog._build_ui()` L21455–21458):
   Replace conditional with `text="XUAT Translation Archiving",`.
2. **UI-side progress label formatter** (`XuatCleanupDialog._format_scan_progress(processed: int, total: int) -> str`), keeping `classify_cleanup_candidates()` `progress_cb` signature untouched:
   ```python
   @staticmethod
   def _format_scan_progress(processed: int, total: int) -> str:
       if total < 3 or total % 3 != 0:
           return f"Scanning XUAT entries... ({processed}/{total})"
       entries_per_pass = total // 3
       pass_labels = (
           "Pass 1/3 — Matching applied imports",
           "Pass 2/3 — Finding duplicate key occurrences",
           "Pass 3/3 — Identifying translated entries",
       )
       if processed <= 0:
           return f"{pass_labels[0]} (0/{entries_per_pass})..."
       pass_idx = min((processed - 1) // entries_per_pass, 2)
       within_pass = min(processed - (pass_idx * entries_per_pass), entries_per_pass)
       return f"{pass_labels[pass_idx]} ({within_pass}/{entries_per_pass})..."
   ```
3. Wire `_format_scan_progress(proc, tot)` into BOTH `_on_prog()` (L21759 `_mgr_post_prog`) AND `_poll_scan_queue()` (L21833 `lbl_counts.config(...)`).

---

## Phase 5 — `Q-10`: Select All / Deselect All Box Controls Across Both Views

### Verified Layout Architecture (Rev 3 Fix 4)
`gd_header` sits in `top_view` (L5430), making it permanently visible above both Dialogue View (`gd_scroll_wrap`) and All Script View (`continuous_wrap`). Currently `_update_dialogue_select_box_ui()` (L10502) hides `cb_dialogue_select` when `self.var_continuous_view.get()` is `True`.

### Plan
**Symbol: `_build_ui()`, new `_update_select_all_boxes_ui()`, `_on_toggle_select_box_mode()` (L10482), `_update_views()` (L9662), new `_on_select_all_boxes()`, `_on_deselect_all_boxes()`**

1. **Create buttons in `_build_ui()` inside `gd_header`** (initially hidden):
   ```python
   self.btn_select_all_boxes = ttk.Button(
       gd_header, text="All", style="Small.TButton", width=4,
       command=self._on_select_all_boxes,
   )
   self.btn_deselect_all_boxes = ttk.Button(
       gd_header, text="None", style="Small.TButton", width=5,
       command=self._on_deselect_all_boxes,
   )
   create_tooltip(self.btn_select_all_boxes, "Select All Dialogue Boxes (excludes Box 0)")
   create_tooltip(self.btn_deselect_all_boxes, "Deselect All Boxes")
   ```
   Naming `btn_select_all_boxes` / `btn_deselect_all_boxes` stays compatible with S11e's planned `BoxSelectAll.png` icon wiring.

2. **Add idempotent `_update_select_all_boxes_ui()` guarded by `self._is_widget_packed()` (L7268)**:
   - Shown whenever `bool(self.var_select_box_mode.get()) and bool(self.current_doc)` — **stays visible when Select Box mode is ON in BOTH Dialogue View AND All Script View, and when Box 0 is active (`is_box0_active == True`)**.
   - Hidden via `pack_forget()` ONLY when Select Box mode is OFF or `not self.current_doc`.
   - Uses `self._is_widget_packed(btn)` so pack/forget calls are idempotent:
     ```python
     def _update_select_all_boxes_ui(self) -> None:
         if not (hasattr(self, "btn_select_all_boxes") and hasattr(self, "btn_deselect_all_boxes")):
             return
         if not (self.btn_select_all_boxes.winfo_exists() and self.btn_deselect_all_boxes.winfo_exists()):
             return
         show = bool(getattr(self, "var_select_box_mode", None) and self.var_select_box_mode.get()) and bool(self.current_doc)
         if show:
             anchor = (
                 self.cb_dialogue_select
                 if hasattr(self, "cb_dialogue_select") and self._is_widget_packed(self.cb_dialogue_select)
                 else (self.lbl_gd_title if hasattr(self, "lbl_gd_title") and self.lbl_gd_title.winfo_exists() else None)
             )
             if not self._is_widget_packed(self.btn_select_all_boxes):
                 kw = {"side": "left", "padx": (4, 0)}
                 if anchor is not None:
                     kw["after"] = anchor
                 self.btn_select_all_boxes.pack(**kw)
             if not self._is_widget_packed(self.btn_deselect_all_boxes):
                 self.btn_deselect_all_boxes.pack(side="left", padx=(2, 0), after=self.btn_select_all_boxes)
         else:
             if self._is_widget_packed(self.btn_select_all_boxes):
                 self.btn_select_all_boxes.pack_forget()
             if self._is_widget_packed(self.btn_deselect_all_boxes):
                 self.btn_deselect_all_boxes.pack_forget()
     ```
   - When switching between Dialogue View and All Script View inside `_update_views()`, unpacking/repacking `cb_dialogue_select` preserves order; also call `_update_select_all_boxes_ui()` from `_on_toggle_select_box_mode()`, `_update_views()`, `_on_select_all_boxes()`, `_on_deselect_all_boxes()`.

3. **`_on_select_all_boxes()` & `_on_deselect_all_boxes()`**:
   - `_on_select_all_boxes()` sets `self._selected_boxes = set(range(len(self.current_doc.boxes)))` (`-1` never added, even when `is_box0_active == True`), refreshes All Script selection slots (`_refresh_as_visible_selection_slots()`) or Dialogue checkbox (`_update_dialogue_select_box_ui()`), and NEVER alters `_locked_box_uids` / `_locked_boxes`.
   - `_on_deselect_all_boxes()` clears `self._selected_boxes` and refreshes the active view's selection UI.
   - Safe against `test_v15_s04_layout_drawer_controls::test_probe_1` (buttons hidden by default; packed left-side after `lbl_gd_title`/`cb_dialogue_select`) and `test_misora_ui_integration::test_11` (checks ribbon frame width).

---

## Phase 6 — `Q-11`: Safe MTL Globe (`🌐`) Button

1. **Exact live engine keys** (`_MTL_DRAWER_ENGINE_ORDER` L16880–16886 & `core/mtl_engine.py` L26):
   ```python
   _MTL_GLOBE_URLS: Dict[str, str] = {
       "Google": "https://translate.google.com/",
       "DeepL":  "https://www.deepl.com/translator",
       # No web translator URL for "XUAT Cache", "Local / Sugoi", "LLM / OpenAI" -> globe omitted
   }
   ```
2. In `_rebuild_mtl_drawer_cards()`, pack `btn_globe` (`side="right"`, `padx=(2, 2)`, tooltip via `create_tooltip`) ONLY when `eng in self._MTL_GLOBE_URLS`. All Script mode has no per-engine cards and keeps no globe button. Preserves `test_v15_s09_core_fixes_54d::test_probe_7` (`btn_apply` left of `lbl_engine`).
3. `_on_mtl_globe_open(engine_name)` copies `box.clean_text` via clipboard (with `tk.TclError` guard) when `active` is a dialogue box (omits copy on Box 0 / empty doc), shows a descriptive toast, and opens the exact URL via `webbrowser.open(url, new=2)` (`webbrowser` already imported at L28).

---

## Phase 7 — `Q-12`: Window Title Episode Metadata

### Verified Call Sites Including Cache-Hit Tab Switches (Rev 3 Fix 5)
All `MisoraApp.title(...)` call sites in `misora.py`:
- **L2012** (`__init__`): `"Misora: Story Editor"` (no open doc yet — matches `_build_window_title()`).
- **L9596** (`open_file()`): executes on **BOTH** fresh disk loads (`kind in {"bundle", "v2", "text"}`) **AND** cache-hit tab switches (`staged["kind"] == "cache"`, where `current_file_path` and `current_doc` are already updated at L9532–9537). Wait: notice that switching between two already-open **clean** tabs runs L9596 unconditionally (even if `refresh_ui=False`) AND runs `self._dirty_state_changed()` at L9623 (when `refresh_ui=True`). Routing **both** L9596 and L10659 through `self.title(self._build_window_title())` guarantees immediate, zero-stale episode metadata on every clean or dirty tab switch!
- **L10659** (`_dirty_state_changed()`): replace with `self.title(self._build_window_title())`.
- **L16016** (`close_file()` empty-state branch when closing last file): add `self.title(self._build_window_title())`, resetting cleanly to `"Misora: Story Editor"`. (`open_file(next_file)` handles non-empty closes; `_dirty_state_changed()` at L16272 handles empty workspace diff clears.)

### Plan
1. **Add `_build_window_title(self) -> str`**:
   - Base: `"Misora: Story Editor"`.
   - Returns base if `not self.current_file_path`.
   - Appends `f" - {file_name}{dirty_marker}"`.
   - Reads `doc.get_metadata()` in memory (zero disk I/O), sanitizes embedded newlines/tabs/whitespace via `" ".join(val.split())`, formats `"{title} ({subtitle})"` (or whichever is non-empty), truncates `meta_str` cleanly at 65 chars (`meta_str[:62] + "…"`), and appends `f" — {meta_str}"`.
   - Leaves `"Dialogue"` / `"All Script"` (`lbl_gd_title`) untouched.
   - Safe against all existing substring title assertions (`test_s2_dirty_contract` L140/150/406/414/431, `test_v15_s01` L431, `test_v15_s08` L386, `test_p3_s13` L131).

---

## Phase 8 — Tests

### New File: `tests/test_v15_s11d_import_ux_productivity.py`

#### Failing-First Probes (4):
1. **`test_probe_1_import_mousewheel_over_labels_and_tristate_group_select_all`**:
   - **Q-06**: Verifies `<MouseWheel>` bound recursively on section headers, card labels, lock badges, provenance/dup labels, `cb_skip`, `scope_cmb` (returning `"break"`), AND any empty-state / no-match placeholder `tk.Label` inside `rows_frame` scrolls `list_canvas`; confirms `txt_left` / `txt_right` retain focus-gated inner scroll (not clobbered by recursive bind).
   - **Q-07**: Verifies single-visual `ttk.Button` group headers (`"☐ All"` / `"☑ All"` / `"▣ All"`), `_group_select_states`, O(1) `_bulk_updating_group` re-entrancy guard, Missing (0-candidate) exclusion, Locked row preservation, and state clear across `_on_reload_index()`.
2. **`test_probe_2_synopsis_multiline_import_and_archiving_progress_labels`**:
   - **Q-08**: Covers **all 3 Synopsis cases**:
     - **(a)** Genuinely empty synopsis with no source key → skipped cleanly (zero Synopsis row built).
     - **(b)** Non-empty multi-line JP synopsis → 5-line `wrap="word"` Synopsis row, zero 54d red overflow badges (U-18), Pre-Apply summary mentions Synopsis, `MetadataDelta(old_summary, new_summary)` atomic Undo/Redo, and `classify_cleanup_candidates` Pass 3 matches multi-line `\n` Synopsis (`Box #0 (Synopsis)`).
     - **(c)** Story opened with JP synopsis, then cleared to `""` in-editor → 4-tuple `meta_fields` resolves `original_jp_summary` from normalized `_original_metadata_by_path` (surviving tab switch without overwrite, refreshed on `on_reload()`, pruned on `close_file()`) and imports XUAT translation into empty summary!
   - **Q-09**: Zero `"Import Complete —"` strings in `XuatCleanupDialog`; `_format_scan_progress()` (and worker progress display) accurately emit `"Pass 1/3"`, `"Pass 2/3"`, `"Pass 3/3"` descriptions including exact boundary steps (`100/300` → Pass 1/3 `100/100`, `101/300` → Pass 2/3 `1/100`, empty `1/1` fallback).
3. **`test_probe_3_select_all_box_excludes_box0_and_preserves_translation_lock`**:
   - **Q-10**: `_on_select_all_boxes()` selects `set(range(N))`, `-1` never in set (even with `is_box0_active=True`), locked UIDs unchanged, tooltips present, idempotent `_is_widget_packed()` visibility when Select Box mode is ON in **both** Dialogue View and All Script View (and hidden when OFF), `_on_deselect_all_boxes()` clears selection.
4. **`test_probe_4_mtl_globe_copies_clipboard_opens_official_site_and_window_title_metadata`**:
   - **Q-11**: Mocked `webbrowser.open`; globe shown on `"Google"` and `"DeepL"`, omitted on `"XUAT Cache"` / `"Local / Sugoi"` / `"LLM / OpenAI"` and All Script mode; copies active box text on dialogue box, omits clipboard copy on Box 0.
   - **Q-12**: Window title shows filename + newline-sanitized truncated `Title (Subtitle)`, updates live on Box 0 edit, Undo, cache-hit switching between two open clean tabs, and resets to `"Misora: Story Editor"` on `close_file()` of last tab; `"Dialogue"` header untouched.

#### Regression Guards (2 — pass both pre-patch & post-patch):
1. **`test_guard_1_import_document_identity_guard_and_prepass_actor_exclusion_intact`**
2. **`test_guard_2_s11c_unified_quick_edit_and_s11b_strict_en_text_scanner_intact`**

### Updated File: `tests/test_v15_s11_xuat_archiving_progress.py`
- Updates assertions **inside existing `test_probe_4_import_1line_metadata_unique_actors_no_box0_and_pixel_54d_width`** (lines ~412–540) to test both Synopsis skipped (`var_skip=True` → untouched `"あらすじJP"`) and Synopsis imported (`var_skip=False` → `"Should NOT touch synopsis"` + Undo/Redo).
- **Adds zero new `test_*` methods**, preserving exact total test count reconciliation: **460 pre-S11d + 6 new = 466 total discovered** (423 expected PASS, 35 SKIP, 6 pre-existing FAIL, 2 pre-existing ERROR).

---

## Phase 9 — Version, Changelog, Project State

1. `__init__.py`: `__version__ = "1.4.14"`
2. `CHANGELOG.md`: Add `### S11d (v1.4.14)`
3. `PROJECT_STATE.md`: Record S11d results, exact verification counts (466 total), and Manual Windows QA checklist

---

## Verification Commands

```bash
# Pre-patch probes (all 4 FAIL, 2 guards PASS):
py -3.12 -m unittest tests.test_v15_s11d_import_ux_productivity -v

# Post-patch compile:
py -3.12 -m compileall -q __init__.py misora.py core assets tests

# Targeted suites:
py -3.12 -m unittest tests.test_v15_s11d_import_ux_productivity tests.test_v15_s11_xuat_archiving_progress tests.test_p3_s22_import_xuat tests.test_v15_s07_xuat_cleanup_archive tests.test_v15_s04_layout_drawer_controls tests.test_v15_s09_core_fixes_54d tests.test_s2_dirty_contract tests.test_s8b4_ui_polishing -v

# Full discovery (expected 466 total):
py -3.12 -m unittest discover -s tests -v
```

---

## Manual Windows QA Checklist (S11d — `MANUAL-PENDING`)

1. **Q-06:** Open `Import from XUAT` → hover over labels, lock badges, provenance, dup counters, `Skip`, section headers, `scope_cmb`, and empty-state placeholder labels → verify wheel scrolls the dialog smoothly without changing `scope_cmb`; verify clicking/focusing `txt_left`/`txt_right` allows inner scroll & `Shift+Wheel`.
2. **Q-07:** Click `☐ All` on each group → toggles all eligible unlocked/matched rows to `☑ All`; click again → `☐ All`; partial toggle → `▣ All`; reload index rebuilds cleanly; locked and missing rows unaffected.
3. **Q-08:** Open `Import from XUAT` on stories with (a) empty synopsis (skipped), (b) multi-line JP synopsis (5-line `wrap="word"`, focus-gated scroll >5 lines, no 54d red overflow badges, imported & archived in Pass 3, single `Ctrl+Z` undoes atomically), (c) JP synopsis cleared to `""` in-editor (still matched & imported via `_original_metadata_by_path`).
4. **Q-09:** Run `XUAT Translation Archiving` after import → verify header says `"XUAT Translation Archiving"` (no `"Import Complete —"` prefix) and scan progress cycles cleanly through `Pass 1/3`, `Pass 2/3`, `Pass 3/3`.
5. **Q-10:** Enable Select Box mode → verify `All` and `None` buttons appear with tooltips in **both** Dialogue View and All Script View (and when Box 0 is active); `All` selects `0..N-1` excluding Box 0 and preserving locks; `None` clears selection; disabling Select Box mode hides buttons.
6. **Q-11:** Click `🌐` on Google / DeepL card → copies box text to clipboard and opens official site; absent on local/AI cards & All Script mode; Box 0 opens URL without clipboard copy.
7. **Q-12:** Open story with multi-line/long Title & Subtitle → window title shows `Misora: Story Editor - filename — Title (Subtitle)` truncated cleanly with `…` and collapsed newlines; updates on Box 0 edit, Undo, clean tab switch, and resets to `"Misora: Story Editor"` on closing last file.
8. Retain all S11c, S11b2, S11b, S11, S10 & S09b Manual QA items.

> [!CAUTION]
> **STOP — Rev 3 ready for Misora-Reference/main publication & ChatGPT/Qwen clearance. Awaiting explicit `Proceed` before editing any file.**
