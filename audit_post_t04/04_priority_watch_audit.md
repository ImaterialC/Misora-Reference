# Misora POST-T-04 — Priority Watch & Wave-0/1 Source Audit

**Audit baseline:** `8affb7c53b6af6047ace423c7e4d830a978eb644` on `main`  
**Version:** `1.4.15`  
**Inspection method:** Direct live-source read at `AUDIT_BASELINE_HEAD` with exact `file:line` references  
**Evidence policy:** `SOURCE-OBSERVED + NEEDS-REPRO` unless stated otherwise

---

## Wave 0 — `Tcl_AsyncDelete` Test Teardown Abort

### Evidence: `SOURCE-OBSERVED + NEEDS-REPRO` | Lifecycle: `ACTIVE` (watch item)

**Root cause hypothesis:** Both `test_s8b2_memory_guards` and `test_s8b3_encoding_detection` create a full `MisoraApp()` Tk root per test via `setUp()` / `tearDown()`, creating and destroying dozens of `tk.StringVar`, `tk.BooleanVar`, `tk.IntVar`, and `tk.DoubleVar` instances per test method.

#### Test Tk root lifecycle (both suites identical pattern):

```python
# tests/test_s8b2_memory_guards.py:71-80
def setUp(self):
    clear_icon_cache()
    with patch.object(misora, "CONFIG_PATH", self.config_path):
        self.app = misora.MisoraApp()
    self.app.withdraw()
    self.app.backup_folder = str(self.tmp_dir / "backups")

def tearDown(self):
    try:
        self.app.destroy()
```

```python
# tests/test_s8b3_encoding_detection.py:67-77
def setUp(self):
    with patch.object(misora, "CONFIG_PATH", self.config_path):
        self.app = misora.MisoraApp()
    self.app.withdraw()
    self.app.backup_folder = str(self.tmp_dir / "backups")

def tearDown(self):
    try:
        self.app.destroy()
```

#### MisoraApp Tk Variable creation sites (misora.py):

The `MisoraApp.__init__` creates **80+ Tk Variables** (42 `StringVar`, 39 `BooleanVar`, 3 `IntVar`, 2 `DoubleVar`) all with `master=self`. When `self.destroy()` is called in `tearDown()`, the Tk interpreter destroys the root, but Python's GC may later invoke `Variable.__del__()` on Variables whose `_root` reference is already torn down.

Key variable creation examples:
```python
# misora.py:2207-2208
self.var_box0_title: tk.StringVar = tk.StringVar(master=self, value="")
self.var_box0_subtitle: tk.StringVar = tk.StringVar(master=self, value="")

# misora.py:2272
self.var_select_box_mode: tk.BooleanVar = tk.BooleanVar(master=self, value=False)

# misora.py:8259-8261
self.var_dlg_font_sz = tk.IntVar(master=self, value=int(self.prefs["dialogue_font_size"]))
self.var_raw_font_sz = tk.IntVar(master=self, value=int(self.prefs["raw_font_size"]))
self.var_ui_font_sz = tk.IntVar(master=self, value=int(self.prefs["ui_font_size"]))
```

#### MisoraApp.destroy() teardown sequence (misora.py:2720-2740+):

```python
# misora.py:2720-2740
def destroy(self) -> None:
    self._destroyed = True
    self.search_cancel_flag = True
    # ... cancel search events, MTL batches, sweep after jobs ...
    try:
        for job_id in self.tk.call("after", "info"):
            try:
                self.after_cancel(job_id)
            except Exception:
                pass
    except Exception:
```

The `destroy()` sweeps pending `after` jobs (BUG-32) and cancels search/MTL threads, then calls `super().destroy()` (implicit via Tk). However, there is **no explicit clearing of Tk Variable references** before the Tk interpreter shuts down. The `Variable.__del__` RuntimeError occurs because:

1. `self.destroy()` tears down the Tk interpreter
2. Background GC collects orphaned `Variable` objects from the prior test's `MisoraApp`
3. `Variable.__del__` calls `self._root.tk.call('trace', ...)` on a dead interpreter → `RuntimeError: main thread is not in main loop`

#### Worker thread cleanup in destroy (misora.py:2630-2718):

`_on_root_destroy` (bound to `<Destroy>`) handles:
- Search cancel event set (line 2637)
- MTL batch cancel (line 2642)
- After-job sweep (lines 2646-2652)
- XUAT index cancel event + thread join with 1s timeout (lines 2671-2683)
- Progress manager shutdown (lines 2690-2694)
- Toast/status after-id cancel (lines 2695-2706)
- Speaker autocomplete close (lines 2707-2711)
- DnD cleanup (line 2718)

**Missing from teardown:** No explicit cancellation of `ThreadPoolExecutor` (`self._mtl_all_executor` at misora.py:2329) or daemon threads created at misora.py:18500, 19126, 22454, 23064, 23644, 23905. Daemon threads will die when the process exits but may reference Tk objects during GC.

**Assessment:** The `Tcl_AsyncDelete` / `Variable.__del__` error is a **test-infrastructure issue** (many `Tk()` roots created/destroyed in one process during monolithic `discover`) not a proven application crash. It manifests when GC runs between tests. Split test runs (which avoid cross-test Tk interference) complete cleanly per PROJECT_STATE.md.

---

## Wave 1 — `F-GPT-03` (`_on_app_exit` / `close_file` / `close_all_files`)

### Evidence: `SOURCE-OBSERVED` | Lifecycle: `ACTIVE`

#### `_on_app_exit` multi-dirty-document behavior (misora.py:2585-2628):

```python
# misora.py:2585-2614
def _on_app_exit(self) -> None:
    """Save configuration cleanly on window close and exit (S3).
    Prompts Save/Discard/Cancel per dirty document.
    Aborts exit if Cancel is chosen or if any save fails.
    """
    if not self._flush_active_widget():
        return

    dirty_paths = [
        p for p, d in list(self.open_documents.items())
        if (p == self.current_file_path and self.is_dirty) or d.get("dirty")
    ]
    if self.current_file_path and self.is_dirty:
        cur_p = Path(self.current_file_path).resolve()
        if cur_p not in [p.resolve() for p in dirty_paths]:
            dirty_paths.append(cur_p)

    for p in dirty_paths:
        ans = messagebox.askyesnocancel(
            "Unsaved Changes",
            f"'{p.name}' has unsaved changes.\nSave before exiting?",
            parent=self,
        )
        if ans is None:   # Cancel → abort exit
            return
        if ans:            # Yes → try save
            if not self._save_document_entry(p):
                return     # Save failed → abort exit
```

**Behavior when N > 1 documents are dirty:**
- Iterates `dirty_paths` sequentially, prompting **per-document** Save/Discard/Cancel
- **Cancel on any doc** → immediate `return` (exit aborted, all docs preserved)
- **Save fails on any doc** → immediate `return` (exit aborted, AGENTS.md §6 compliant)
- **Discard on any doc** → continues to next dirty doc
- After all prompts resolved → sweeps `after` jobs, saves config, calls `self.destroy()`

**Observation:** Correctly implements AGENTS.md §6 "Dirty close/exit prompts Save/Discard/Cancel; failed save aborts."

#### `close_file` behavior (misora.py:16260-16342):

```python
# misora.py:16260-16283
def close_file(self, file_path: Path) -> bool:
    """Close an opened file from in-memory cache, prompting if dirty (S3).
    Returns True if the file was closed, False if close was cancelled or aborted.
    """
    file_path = Path(file_path).resolve()
    if file_path == self.current_file_path:
        if not self._flush_active_widget():
            return False
    info = self.open_documents.get(file_path)
    is_dirty = (file_path == self.current_file_path and self.is_dirty) or (info and info.get("dirty", False))
    if is_dirty:
        ans = messagebox.askyesnocancel(...)
        if ans is None:
            return False
        if ans:
            if not self._save_document_entry(file_path):
                return False
```

Returns `False` on Cancel or save failure. Callers (`close_all_files`, `close_others`) break on `False`:

```python
# misora.py:16363-16367
def close_all_files(self) -> None:
    for p in list(self.open_documents.keys()):
        if not self.close_file(p):
            break
```

**SOURCE-OBSERVED:** Correctly aborts remaining closes on Cancel/save-fail. Compliant with AGENTS.md §6.

---

## Wave 1 — `F-GPT-07` (XUAT-JP-KEY-DRIFT) & File/UnityPy Integrity

### Evidence: `SOURCE-OBSERVED + NEEDS-REPRO` | Lifecycle: `ACTIVE`

#### JP key management flow:

**`open_file` → JP key registration (misora.py:9762-9786):**
```python
# misora.py:9762-9786
self._original_jp_by_uid = (
    {_get_box_uid(b): b.clean_text for b in doc.boxes if _get_box_uid(b) is not None}
    if doc is not None and doc.boxes else {}
)
# ...
self._original_box_texts = {i: self._original_jp_by_uid.get(_get_box_uid(b), "")
                            for i, b in enumerate(doc.boxes)}
for b in doc.boxes:
    b_uid = _get_box_uid(b)
    if b_uid is not None:
        if b_uid not in self._original_jp_by_uid:
            self._original_jp_by_uid[b_uid] = b.clean_text
        if hasattr(self, "sync_manager"):
            self.sync_manager.register_jp_key(b_uid, self._original_jp_by_uid[b_uid])
```

**`XUnitySyncManager.register_jp_key` immutability guard (core/xunity_sync.py:168-171):**
```python
# core/xunity_sync.py:168-171
def register_jp_key(self, box_uid: Optional[int], jp_text: str) -> None:
    """Register an immutable Japanese source key for a box to prevent English overwrite."""
    if box_uid is not None and box_uid not in self.jp_source_cache and jp_text:
        self.jp_source_cache[box_uid] = jp_text
```

**Key immutability contract:** `register_jp_key` only registers if `box_uid not in self.jp_source_cache` — once registered, the JP key is **never overwritten** during the session. This prevents English text from being mistakenly used as XUAT dictionary keys.

**Re-sync on structural mutations (misora.py:13475-13487):**
```python
# misora.py:13475-13487
def _resync_box_indices_from_uids(self) -> None:
    """Re-sync positional indices from authoritative UIDs (S06 / S07)."""
    if self.current_doc and self.current_doc.boxes:
        if hasattr(self, "_original_jp_by_uid"):
            self._original_box_texts = {i: self._original_jp_by_uid.get(
                _get_box_uid(b), "") for i, b in enumerate(self.current_doc.boxes)}
```

**Potential drift risk:** If a speaker edit changes `b.clean_text` while `_original_jp_by_uid[uid]` retains the original, the XUAT sync key remains stable. However, if box UIDs are reassigned (e.g., via Insert/Delete/Clone) and a new box gets a UID not yet in `jp_source_cache`, it gets its current `clean_text` as key — which is correct if it's a new JP-only box, but could drift if the box was cloned from one with a prior edit.

**Assessment:** The immutability guard in `register_jp_key` is correct for the open→save→reopen→edit cycle. `F-GPT-07` remains `UNVERIFIED` for edge cases involving box clone/insert with shared UIDs. Requires targeted manual trace.

#### Bundle write atomicity (core/bundle_io.py:176-325):

```python
# core/bundle_io.py:185-287 (summarized pipeline)
# 1. Same-dir .tmp file creation (line 202)
# 2. Record source fingerprint (mtime_ns, size) (line 205)
# 3. Record non-target object SHA-256 hashes (lines 211-216)
# 4. Write to .tmp (line 233)
# 5. Reopen .tmp → verify target TextAsset by path_id/name (lines 236-251)
# 6. Verify repacked bytes match expected binary (lines 253-255)
# 7. Verify object count match (lines 257-260)
# 8. Verify non-target objects SHA-256 unchanged (lines 262-277)
# 9. Backup original if requested (lines 290-295)
# 10. Fingerprint-checked bounded-retry os.replace (lines 297-314)
# 11. Cleanup .tmp in finally (lines 318-325)
```

**Re-entry guard (line 42-43, 190-195):**
```python
# core/bundle_io.py:42-43
_save_lock = threading.Lock()
_is_saving = False
# ... line 192-195:
with _save_lock:
    if _is_saving:
        raise BundleIOError("A bundle save operation is already in progress.")
    _is_saving = True
```

**Assessment:** Bundle save pipeline is robustly defensive with 7 verification gates, non-target preservation SHA-256 checks, source fingerprint concurrency detection, and re-entry guard. Compliant with AGENTS.md §4.

---

## Wave 1/2 — `T-12` (XUAT Sync Threading)

### Evidence: `SOURCE-OBSERVED + DEFERRED` | Lifecycle: `DEFERRED`

**Existing waiver:** S11b2 Option A (~2.899s on 1,814 files / 243k lines)

#### Current sync behavior (core/xunity_sync.py:346-363):

```python
# core/xunity_sync.py:346-363
def batch_sync(
    self,
    targets: List[BatchSyncTarget],
    search_roots: List[Path],
    backup: bool = True,
    # ...
) -> BatchSyncResult:
    """
    Bounded single-pass batched XUAT sync (O(F + E + B + M)).
    Validates roots strictly to Translation\\en\\Text, streams Stage 1+2 retaining
    snapshots ONLY for matched files, runs single-batched conflict confirmation (C1..C4),
    checks pre-write stat freshness, and writes each modified file atomically once.
    """
    t0 = time.perf_counter()
```

**Threading model:** `batch_sync` runs **synchronously on the calling thread**. No `ThreadPoolExecutor`, no `queue.Queue`, no `after_idle` marshalling is used within `xunity_sync.py`. The ~2.899s duration is a synchronous blocking I/O scan on the UI thread.

**XUAT index background worker (misora.py:14403):**
```python
# misora.py:14403
t = threading.Thread(...)
```

The XUAT index rebuild runs in a background thread, but the `batch_sync` call during `on_save` is UI-thread synchronous.

**Assessment:** Current behavior matches the documented S11b2 Option A waiver. The ~2.9s sync is synchronous disk I/O on the UI thread — an accepted trade-off. Async worker IO is explicitly `DEFERRED` per OPEN_ISSUES.md T-12. This is **NOT a new P1 bug** — it is a known accepted limitation.

---

## Wave 2 — `T-03` (All Script Stale Purple Highlight)

### Evidence: `CONFIRMED + ROOT-CAUSE: NEEDS-CODE-VERIFY` | Lifecycle: `ACTIVE`

#### Card highlight/navigation method signatures:

| Method | File:Line | Purpose |
|---|---|---|
| `_apply_as_card_visual_state` | `misora.py:11940` | Apply active/inactive highlight styling to a card |
| `_set_as_active_card` | `misora.py:12087` | Update highlight on old + new visible cards |
| `_on_as_card_click` | `misora.py:12342` | Handle card click → set active card |
| `_layout_as_visible_cards` | `misora.py:12114` | Recycle pool cards onto visible slots |
| `_bind_as_pool_card` | referenced at `misora.py:12207` | Bind card data to pool card |
| `_render_continuous_view` | `misora.py:12367` | Full rebuild of All Script view |
| `_refresh_as_visible_selection_slots` | `misora.py:12077` | Update selection slots on visible cards |
| `_patch_as_visible_card_header` | `misora.py:12070` | Live-sync header of one visible card |

#### `_set_as_active_card` exact implementation (misora.py:12087-12101):

```python
# misora.py:12087-12101
def _set_as_active_card(self, old_idx: Optional[int], new_idx: int) -> None:
    """Update active box highlight in-place on only the old and new visible cards (U-04)."""
    box0 = getattr(self, "_as_box0_card", None)
    if box0 is not None and box0.winfo_exists() and self.current_doc and self.current_doc.has_metadata():
        if old_idx == -1 or new_idx == -1:
            self._bind_as_box0_card()
    vis_cards = getattr(self, "_as_visible_cards", {})
    if old_idx is not None and old_idx >= 0 and old_idx != new_idx:
        old_card = vis_cards.get(old_idx)
        if old_card is not None and old_card.winfo_exists() and old_card.bound_box_idx == old_idx:
            self._apply_as_card_visual_state(old_card, False)
    if new_idx >= 0:
        new_card = vis_cards.get(new_idx)
        if new_card is not None and new_card.winfo_exists() and new_card.bound_box_idx == new_idx:
            self._apply_as_card_visual_state(new_card, True)
```

**Key observation for T-03:** `_set_as_active_card` only unhighlights the **single previous active card** (`old_idx`) and highlights the **single new active card** (`new_idx`). It does **not** clear highlights on any other cards. If navigation occurs via shortcuts (Prev/Next/arrow keys), each step passes only the immediately-previous `old_idx`:

```python
# misora.py:12342-12354
def _on_as_card_click(self, card: _AllScriptPoolCard) -> None:
    box_idx = card.bound_box_idx
    # ...
    old_idx = -1 if getattr(self, "is_box0_active", False) else self.current_box_idx
    self.is_box0_active = False
    self.current_box_idx = box_idx
    self._set_as_active_card(old_idx, box_idx)
```

#### `_apply_as_card_visual_state` styling (misora.py:11940-11967):

```python
# misora.py:11940-11944
def _apply_as_card_visual_state(self, card: _AllScriptPoolCard, is_active: bool) -> None:
    """Apply distinct active highlight vs inactive card styling in-place (U-04)."""
    t = self.theme
    hdr_bg = t["highlight_bg"] if is_active else t["bg_panel"]
    card_bg = t["highlight_bg"] if is_active else t["bg_panel"]
```

The "purple highlight" uses `t["highlight_bg"]` for active cards. When `is_active=False`, cards revert to `t["bg_panel"]`.

**Potential orphan mechanism:** If rapid navigation via keyboard shortcuts moves through cards faster than `_set_as_active_card` can track (or if the card pool recycles a card that was previously highlighted to a different slot without resetting), the intermediate cards retain `highlight_bg` styling. The `_layout_as_visible_cards` method (misora.py:12114-12220) **does not** perform a blanket theme reset on pool cards when rebinding — it only calls `_bind_as_pool_card` on newly bound cards.

**`_selected_boxes` mutation sites** (27 occurrences at misora.py:2273, 10702, 10745, 10756, 10775, 10789, 10791, etc.) are all Select Box mode operations and do not directly interact with the purple highlight mechanism.

**Assessment:** The stale purple highlight is `CONFIRMED` per OPEN_ISSUES.md with 4 reproduction screenshots. The root cause likely lies in `_set_as_active_card` only tracking `old_idx → new_idx` pairs and missing intermediate cards during rapid multi-step navigation. Full root-cause verification requires tracing the exact keyboard shortcut dispatch path and pool card recycling behavior.

---

## Verification Boundary

**Inspected:**
- `misora.py` (24,004 lines) — targeted methods only: `_on_app_exit`, `close_file`, `close_all_files`, `destroy`, `_on_root_destroy`, `open_file` JP key registration, `_resync_box_indices_from_uids`, `on_save`, `_set_as_active_card`, `_on_as_card_click`, `_apply_as_card_visual_state`, `_layout_as_visible_cards`, `_selected_boxes` mutation sites, `winfo_ismapped` calls, Tk Variable creation sites, thread creation sites
- `core/bundle_io.py` (325 lines) — `save_bundle_story` full pipeline
- `core/xunity_sync.py` (612 lines) — `XUnitySyncManager`, `register_jp_key`, `batch_sync`
- `tests/test_s8b2_memory_guards.py` (250 lines) — setUp/tearDown Tk lifecycle
- `tests/test_s8b3_encoding_detection.py` (250 lines) — setUp/tearDown Tk lifecycle

**NOT inspected:**
- Full `_bind_as_pool_card` implementation (referenced at line 12207 but not read)
- Keyboard shortcut dispatch path for Prev/Next in All Script view
- `_on_as_card_body_focus_in` / card focus chain logic
- Full `open_file` method body (only JP key section read)
- `_save_document_entry` implementation
- XUAT cleanup module (`core/xuat_cleanup.py`)
- Full `_on_root_destroy` continuation (lines 2690-2718+ only partial read)
- Dynamic dispatch via `command=`, `.bind(`, `.after(`, `.protocol(` for dead-code verification

---

*End of Priority Watch & Wave-0/1 Source Audit.*
