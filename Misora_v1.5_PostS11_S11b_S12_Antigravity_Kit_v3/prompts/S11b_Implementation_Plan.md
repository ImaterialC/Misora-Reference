# S11b (v1.4.11) — Implementation Plan (Revised)

> **Status:** 🛑 **AWAITING INDEPENDENT REVIEW & PROJECT LEAD `Proceed`** — ZERO repository source, test, or pre-existing working-tree files have been modified.

---

## 0. Pre-Session Environment Snapshot & Baseline Provenance

| Item | Value |
|---|---|
| **Branch** | `main` |
| **HEAD** | `c1ec40c96c18ae6e4df61d1db77ebf999114be3d` |
| **Pre-Existing Working Tree** | `M assets/icons/BoxInsert.png`, `?? assets/icons/BoxReplace.png` (user local work — MUST be preserved untouched) |
| **Python / Tk / OS** | `Python 3.12.10` · `Tk 8.6` · `Windows-11-10.0.26100-SP0` |
| **`__version__`** | `"1.4.10"` (target `"1.4.11"` after `Proceed`; `v1.5.0` remains **ON HOLD**) |
| **Production Bundle Fixture** | `storydata_1001005.unity3d` is **NOT** present on disk in repo root (`BLOCKED` per `AGENTS.md` §2) |
| **Historical S11 Baseline** | *Previously reported by Project Lead in `PROJECT_STATE.md` (not re-run in this `/plan` turn):* `440` discovered · `397` pass · `35` fixture-skipped · `6` failed (`3` fixture-blocked + `3` pre-existing hygiene) · `2` error (fixture-blocked) |

---

## 1. Project Lead Locked Rulings

1. **Ruling 1 (`Ctrl+S` Data Safety — CONFIRMED):**
   - `Ctrl+S` MUST save **ONLY** the `.misora` workspace (`on_save_project()`), never patching `.unity3d` on muscle memory (protecting original JP text/cues/waits from accidental overwrite).
   - `on_save_project()` / `save_project()` MUST **NEVER** clear dirty flags (`is_dirty`, `open_documents[p]["dirty"]`) or call `undo_journal.mark_saved()` on dirty story documents.
   - Emit explicit honest post-`Ctrl+S` toast: `"Project (.misora) saved — story edits are not yet written to bundle/XUAT (use Ctrl+Shift+S to save file)."`
   - Keep dirty-close Save/Discard/Cancel prompt (`AGENTS.md` §16) intact, and clearly distinguish both save commands in `README.md` (removing stale `"Ctrl+Shift+S | Save As"`), File menu items, toolbar button/tooltip, and tab context menu.
2. **Ruling 2 (`Q-18` Ruby Preview — STOP Gate B):**
   - Formally **`DEFERRED`** to post-`v1.5.0` (Track B, prerequisite to `BIG-02` MeCab).
   - Will be recorded explicitly as **`DEFERRED`** in `PROJECT_STATE.md` and `S12` traceability (never silently dropped). Auto-Furigana (MeCab) remains out of scope (`BIG-02`).
3. **Ruling 3 (`Q-04.1.2` & Box 0):**
   - Box 0 stays excluded from ordinary dialogue rows in Import; multi-line Synopsis import is scheduled in `S11d` (`Q-08`).
   - Record `Q-04.1.2` honestly as **`NOT REPRODUCED — NEEDS USER REPRODUCTION DETAILS`** (do NOT manufacture a failing-first test).

---

## 2. STOP Gate Decisions & Measured Profiling Evidence

### STOP Gate A (`Q-02` Save Hang Profiling — `PENDING` -> Measured -> Bounded Remap Approved)

> [!NOTE]
> Initial plan status was `PENDING — measured profiling evidence required`. Real `time.perf_counter()` measurements were executed on temporary test copies (`Windows-11-10.0.26100-SP0`, `Python 3.12.10`, `Tk 8.6`, 5 repeated runs per path; zero user game files, `misora_config.json`, or `backups/` touched).

#### Measured Profiling Results (`5` repeated iterations per path)

**Path A — `Ctrl+S` (`save_project` `.misora`, 3 open `.v2.txt` docs × 50 boxes, 2 stable locks/doc, `.misora` output = `1,558` bytes):**

| Stage | Code Site (`misora.py`) | Median (ms) | Min–Max Range (ms) | 5 Runs (ms) |
|---|---|---|---|---|
| **1. Widget Flush** | `_flush_active_widget()` (incl. `_flush_quick_edit_session()`) | `8.223` | `7.371 – 10.220` | `[8.223, 10.220, 7.371, 8.158, 8.839]` |
| **2. Workspace Collect** | `_save_active_document_state()`, `_exit_raw_edit_mode()`, `_cancel_mtl_all_batch()`, `get_document_stable_locks()`, `WorkspaceSession` | `1.371` | `1.175 – 1.879` | `[1.879, 1.507, 1.175, 1.371, 1.200]` |
| **3. `.misora` Write** | `save_workspace()` (`core/workspace.py` JSON + `write_atomic_encoded`) | `0.797` | `0.673 – 9.894` | `[9.894, 0.826, 0.674, 0.797, 0.673]` |
| **4. Status & Toast** | `lbl_status.config()` + `show_toast()` | `0.087` | `0.079 – 0.523` | `[0.103, 0.523, 0.079, 0.087, 0.084]` |
| **Total Path A** | End-to-end `save_project()` | **`10.797`** | `9.299 – 20.100` | `[20.100, 13.076, 9.299, 10.414, 10.797]` |

**Path B — `Ctrl+Shift+S` (`on_save()` Active File / Patch Bundle):**

- **Path B1 (`.v2.txt`, 50 boxes = `3,021` bytes, `var_sync_xuat=True` on 10-file / `1,000`-entry synthetic `Translation\en\Text` tree, 6 modified boxes):**

| Stage | Code Site (`misora.py`) | Median (ms) | Min–Max Range (ms) | 5 Runs (ms) |
|---|---|---|---|---|
| **1. Widget Flush & AST Sync** | `_flush_quick_edit_session()` + `inject_box()` | `0.128` | `0.117 – 0.167` | `[0.165, 0.123, 0.128, 0.167, 0.117]` |
| **2 & 4. Backup + `.v2.txt` Write** | `shutil.copy2()` backup + `to_v2_text()` + `write_atomic_utf8()` | `1.677` | `1.610 – 4.058` | `[4.058, 1.993, 1.677, 1.610, 1.674]` |
| **3. XUAT Sync (DOMINANT)** | `_sync_modified_boxes_to_xuat()` (`preview_matches` + `find_and_update` per box) | **`93.725`** | `85.615 – 186.703` | `[186.703, 85.615, 93.725, 86.293, 101.292]` |
| **5. Post-Save UI Refresh** | `_record_saved_checkpoint()`, `mark_saved()`, `_dirty_state_changed()`, `lbl_status.config()` | `0.684` | `0.653 – 1.084` | `[0.684, 0.653, 0.704, 0.676, 1.084]` |
| **Total Path B1** | End-to-end `on_save()` with XUAT sync | **`96.234`** | `88.384 – 191.610` | `[191.610, 88.384, 96.234, 88.746, 104.166]` |

- **Path B1-No-XUAT (`.v2.txt`, 50 boxes = `3,021` bytes, `var_sync_xuat=False`):**
  - Total: median **`2.553 ms`**, range `[2.399, 2.826] ms` (`[2.826, 2.553, 2.650, 2.399, 2.467]`).
- **Path B2 (Plain `.txt`, `350` bytes):**
  - Total: median **`1.421 ms`**, range `[1.295, 1.600] ms` (`[1.600, 1.510, 1.421, 1.295, 1.328]`).
- **Path B3 (Real `.unity3d` Bundle Serialization — `save_bundle_story()`):**
  - **`UNMEASURED / BLOCKED (missing production fixture)`**: `storydata_1001005.unity3d` is not present in the repository root, and `backups/` is off-limits. Real-bundle save timing is added to the **Manual Windows QA Checklist** in `PROJECT_STATE.md`.

#### STOP Gate A Decision
- **Measured Bottleneck Identified:**
  1. In Path B1, Stage 3 (`_sync_modified_boxes_to_xuat()` calling `core/xunity_sync.py::preview_matches()` and `find_and_update()` per modified box, each performing full `rglob("*.txt")` + disk decode) accounts for **`97.4%` (`93.725 ms / 96.234 ms`)** of save time even on just 6 boxes / 10 files (`1,000` entries), scaling $O(\text{modified\_boxes} \times \text{xuat\_files})$.
  2. In Path B3, `save_bundle_story()` (`core/bundle_io.py`) performs synchronous UnityPy save + tmp reopen verification.
- **Forbidden Core Boundary:** Both `core/xunity_sync.py` and `core/bundle_io.py` are **Forbidden Files** in S11b.
- **Gate A Outcome:**
  - **CLEAR for bounded `Ctrl+S` -> Save Project (`.misora`) shortcut remap** inside S11b Allowed Files (`10.797 ms` median, never touches `core/bundle_io.py` or `core/xunity_sync.py`, eliminates accidental/slow bundle+XUAT saves on `Ctrl+S`).
  - **Real-bundle hang timing (`UNMEASURED`) & multi-box XUAT sync / async bundle-save overhaul remain DEFERRED** to their own separately approved session if the Project Lead observes `Ctrl+Shift+S` hangs on real bundles/large XUAT trees during Manual Windows QA.

---

### STOP Gate B (`Q-18` Ruby Preview — 🛑 TRIGGERED & FORMALLY `DEFERRED`)

- **Code Inspection (`misora.py::_insert_compiled_ngui_text`, lines `7708–7775`, and `compiled_ruby` tag, lines `3538–3543`):**
  - `[rub:ruby]base[/rub]` emits `base_txt` via `emit_styled_run(base_txt)` and then appends `ruby_txt` inline after it with `compiled_ruby` (`offset=5`, smaller bold font).
  - `tk.Text` lacks native above-base ruby positioning; `offset=5` shifts baseline vertically on the same horizontal run (`願いめいれい`), not centered above `願い`.
- **Gate B Outcome:** Proper ruby display requires building a new custom Canvas text-layout engine. Per STOP Gate B & **Ruling 2**, `Q-18` is **STOPPED & FORMALLY `DEFERRED`** to post-`v1.5.0` (Track B, prerequisite to `BIG-02` MeCab), recorded in `PROJECT_STATE.md` and `S12` traceability, with no implementation-specific failing-first test manufactured in S11b.

---

## 3. `Q-01` — Strict XUAT English Text Scanner, Additive Rule Exclusions & Canonical Metrics

### 3A. Strict Canonical Root Boundary (`core/xuat_index.py::resolve_xuat_text_roots()`, lines `134–181`)

Close ALL 3 current permissive bypasses (unvalidated direct `.txt`, cascading `p / "en" / "Text"` and `p / "Text"`, and bare `low_name == "text"` fallback):
- **ONLY Permitted Dictionary Subtree:** Canonical `Translation\en\Text` (case-insensitive segment suffix on Windows).
- **Supported User-Selected Entry Points (5 user entry-point categories, 6 concrete path forms):**
  1. **Game Root (2 path forms):** `<GameRoot>\src\BepInEx\Translation\en\Text` (Project Lead's `PriconneRe-TL\src\BepInEx\...` hierarchy) **AND** `<GameRoot>\BepInEx\Translation\en\Text`.
  2. **`BepInEx` folder:** `<BepInEx>\Translation\en\Text`.
  3. **`Translation` folder:** `<Translation>\en\Text`.
  4. **`Translation\en` folder:** `<Translation\en>\Text`.
  5. **`Translation\en\Text` folder:** accepted directly ONLY when trailing 3 path parts equal `("translation", "en", "text")` (case-insensitive).
- **Direct `.txt` Selection:** Accepted ONLY when resolved parent lies strictly inside a canonical `Translation\en\Text` subtree (`_is_inside_canonical_en_text(p.parent)`) AND `not _is_excluded_xuat_file(p)`.
- **Explicitly Rejected Locations:** `Translation\ja\Text` (and any non-`en` language), arbitrary `Text/` outside `Translation\en\Text`, standalone `.txt` outside `Translation\en\Text`, `Translation\en\Other`, `Translation\en\RedirectedResources`.
- **MisoraApp Root Alignment (`misora.py:4057` `_resolve_xuat_text_root`):** Add `proj_dir / "src" / "BepInEx" / "Translation" / "en" / "Text"` as first candidate in `_resolve_xuat_text_root()` so `_set_project_folder(<GameRoot>)` directly discovers `src\BepInEx\...` without breaking `_resolve_project_search_roots()` (`test_p3_s08`).
- **Pre-Check on Existing Tests:** Inspected `test_p3_s22_import_xuat.py`, `test_v15_s07_xuat_cleanup_archive.py`, and `test_v15_s11_xuat_archiving_progress.py` — all already construct `BepInEx/Translation/en/Text`. Zero existing XUAT test fixtures need path edits.

### 3B. Additive File Exclusions (`m-1` — Case-Insensitive `endswith` Only)

In `core/xuat_index.py::_is_excluded_xuat_file(path: Path)`:
- Preserve all legacy exclusions via `endswith` (`".missing.txt"`, `".report.txt"`, `"_summary.txt"`, `"_warnings.txt"`) and `".bak_" in low`.
- Add ALL 5 XUnity AutoTranslator non-dictionary rule patterns using **case-insensitive `endswith` ONLY** (NOT `contains`):
  - `".font.txt"`, `".resizer.txt"`, `"postprocessors.txt"`, `"preprocessors.txt"`, `"substitutions.txt"`.

### 3C. Complete Repository-Wide Caller Inventory (`len`, `bool`, `.entry_count`, `.entries`, `files_indexed`, `skipped_files`)

| File : Line | Symbol / Context | Call Form | Purpose | Impact of Valid-Entry-Only `entry_count` |
|---|---|---|---|---|
| `core/xuat_index.py:228-236` | `XuatIndex.__init__` | `files_indexed`, `skipped_files`, `entry_count`, `entries`, `_norm_stripped_map` | Index storage | Add `self.files_scanned: int = 0` + `@property entries_read -> entry_count` |
| `core/xuat_index.py:238-250` | `XuatIndex.add_entry` | `self.entries.append`, `_exact_map`, `_norm_stripped_map`, `_value_map`, `self.entry_count += 1` | Populate lookup tiers & counts | Guard `self.entry_count += 1` on `if k_norm_stripped:` ONLY; keep `entries`/`_exact_map`/`_value_map` unchanged (zero silent dropping) |
| `core/xuat_index.py:314-315` | `XuatIndex.__bool__` | `return bool(self.entries)` *(updated from `self.entry_count > 0`)* | Truthiness check | **Critical Fix:** Prevents `bool(idx)` from returning `False` when an index contains ONLY empty-normalized-key entries (`entries` / `_exact_map` / `_value_map` non-empty while `entry_count == 0`), so `MTLEngine.translate()` still reaches exact-tier lookup |
| `core/xuat_index.py:317-318` | `XuatIndex.__len__` | `return self.entry_count` | Count of indexed valid entries | Reflects canonical `entry_count` (`entries_read`: valid entries with non-empty `normalize_xuat_key(..., strip_ngui=True)`) |
| `core/xuat_index.py:320-333` | `__contains__`, `__getitem__`, `get` | Delegates to `lookup_translation()` | Dict-like MTL interface | Unaffected (lookup reads `_exact_map` / `_norm_exact_map` / `_norm_stripped_map`) |
| `core/mtl_engine.py:153-163` | `MTLEngine.translate` (cache hit) | `if cfg.use_xuat_cache and xuat_cache:` (`__bool__`) -> `lookup_translation()` | Instant XUAT cache check | Safe with `XuatIndex.__bool__() -> bool(self.entries)` (exact-tier lookup still executes even when only empty-normalized-key entries exist; `core/mtl_engine.py` remains untouched) |
| `core/mtl_engine.py:183-190` | `MTLEngine.translate` (`"XUAT Cache"` engine) | `if xuat_cache:` (`__bool__`) -> `lookup_translation()` | XUAT Cache MTL lookup | Safe with `XuatIndex.__bool__() -> bool(self.entries)` (`core/mtl_engine.py` remains untouched) |
| `core/xuat_cleanup.py:510-511` | `classify_cleanup_candidates` | `entries = getattr(xuat_index, "entries", ())`; `len(entries)` | Iterate all parsed entries across Pass 1/2/3 | Unaffected: `XuatIndex.entries` is preserved untouched |
| `core/xuat_cleanup.py:689-691` | `classify_cleanup_candidates` | `file_fingerprints`, `files_indexed` | Source SHA-256 fingerprint capture | Unaffected |
| `misora.py:2094-2095` | `MisoraApp.__init__` | `self.xuat_index = None`, `self.xuat_entries = None` | Cache + alias for MTL | Alias stays synchronized on every rebuild |
| `misora.py:2329, 4054, 18444-18543, 18555, 19786, 19994, 21080, 21431, 21546-21549, 22164` | `MisoraApp`, `ImportFromXUATDialog`, `XuatCleanupDialog`, `MTLSettingsDialog` | `is None`, `isinstance(..., XuatIndex)`, `.roots == strict_roots` | Lifecycle & lazy/async build | Unaffected (none call `len`/`bool` on index) |
| `misora.py:17244, 17659, 17765, 17818, 17825, 17988, 22625, 22683, 22915, 22937` | MTL Drawer, `Translate All`, `on_translate_current_box`, `TranslatorAssistantDialog`, `BatchTranslateDialog` | `xuat_cache=getattr(..., "xuat_entries", None)` passed to `MTLEngine` | Pass index into `MTLEngine.translate()` | Safe: `MTLEngine` checks `bool(xuat_cache)` + `lookup_translation()` |
| `misora.py:18511-18512` | `_poll_xuat_index_queue` | `n_files = len(getattr(payload, "files_indexed", ()))` | Status bar progress completion message | **Update (`m-2`):** surface `Scanned X | Indexed Y | Skipped Z` + `Entries / Unique / Duplicates` clearly |
| `misora.py:20325` | `ImportFromXUATDialog._populate_rows` | `f"Files indexed: {len(self.xuat_index.files_indexed)}"` | Summary label in Import dialog | **Update (`m-2`):** distinguish `Scanned: X | Indexed: Y` (+ `Skipped: Z` if >0) and canonical entry/unique/duplicate metrics |
| `tests/test_p3_s22_import_xuat.py:137-173` | `test_probe_1_xuat_index...` | `build_xuat_index([proj_dir])`, `MTLEngine.translate(..., xuat_cache=idx)` | Core index + MTL tests | Unaffected |
| `tests/test_v15_s07_xuat_cleanup_archive.py:740-742` | `test_guard_2...` | `len(idx.skipped_files) == 1` | Corrupted file skipping check | Unaffected |
| `tests/test_v15_s11_xuat_archiving_progress.py:595-597` | `test_probe_5...` | `len(partial_idx.files_indexed) < 15` | Cancellable `os.walk` check | Unaffected |

### 3D. Canonical Metric Contract & `m-2` UI Distinction (`core/xuat_index.py`, `misora.py`)

- **No New Parallel Maps:** Use existing `XuatIndex._norm_stripped_map`, `_norm_exact_map`, `_exact_map`, `_value_map`, `entries`, `files_indexed`, `skipped_files`.
- **Properties & Attributes on `XuatIndex`:**
  - `files_scanned: int`: unique, eligible, non-excluded `.txt` files actually attempted after deduplication. In `build_xuat_index()`, increment `idx.files_scanned += 1` immediately upon attempting each deduplicated non-excluded file (ensuring completed-scan identity `idx.files_scanned == len(idx.files_indexed) + len(idx.skipped_files)`).
  - `entry_count: int` and synchronized `@property def entries_read(self) -> int: return self.entry_count` — incremented in `add_entry()` **ONLY** when `k_norm_stripped != ""` (empty normalized keys NEVER enter `_norm_stripped_map` and NEVER increment `entry_count`/`entries_read`, while still entering `entries`, `_exact_map`, `_value_map`).
  - `__bool__(self) -> bool: return bool(self.entries)` (so an index holding only empty-normalized-key entries stays truthy for `MTLEngine.translate()` exact lookup without modifying forbidden `core/mtl_engine.py`), while `__len__(self) -> int: return self.entry_count`.
  - `@property def unique_keys(self) -> int: return len(self._norm_stripped_map)`
  - `@property def duplicate_keys(self) -> int: return sum(1 for v in self._norm_stripped_map.values() if len(v) > 1)`
  - `@property def duplicate_entries(self) -> int: return self.entries_read - self.unique_keys`
- **`m-2` UI / Status Display (`misora.py:18511-18512` & `20325`):**
  - `_poll_xuat_index_queue()` completion message: `f"XUAT index reloaded (Scanned: {n_scanned}, Indexed: {n_indexed}" + (f", Skipped: {n_skipped}" if n_skipped else "") + f" | Entries: {n_entries}, Unique: {n_unique}, Dup: {n_dup})."`
  - `ImportFromXUATDialog._populate_rows()` summary label: includes `Files scanned: {idx.files_scanned} | Files indexed: {len(idx.files_indexed)}` (+ `Skipped: {len(idx.skipped_files)}` if non-zero) and `Entries: {idx.entries_read} (Unique: {idx.unique_keys}, Dup: {idx.duplicate_entries})`.

---

## 4. `Q-02` — `Ctrl+S` Save Project Remap, Data-Safety Safeguards & `_current_project_path` Lifecycle

### 4A. Shortcut & UI Surface Migration (`misora.py`, `README.md`)

- **Conflict Check Confirmed:** `Ctrl+Shift+S` is currently unbound in `_on_misora_shortcut()` (lines `9015–9033`), `_bind_shortcuts()` (lines `9196–9253`), and menus (`4530–4860`). No `"Save As"` command exists in the app.
- **Shortcuts Help & Existing Tests Audit:**
  - Inspected `misora.py` (`help_menu` lines `4955–4960` and `on_about()` lines `18973–19060`): there is NO separate Shortcuts Help dialog or in-app shortcut reference text mentioning `Ctrl+S`. All in-app `Ctrl+S` references are in `file_menu`, `btn_save`, `_show_file_context_menu`, `_on_misora_shortcut`, and `_bind_shortcuts` (covered below).
  - Inspected `tests/test_p3_s13_ribbon_shortcuts.py`: it does **NOT** lock `Ctrl+S -> on_save()` and **MUST remain untouched** in S11b.
- **Single-Fire `"break"` Requirement:** `_on_misora_shortcut()` MUST return `"break"` for both `Ctrl+S` (`on_save_project()`) and `Ctrl+Shift+S` (`on_save()`) so focused editor widgets with the `MisoraShortcuts` bindtag never fall through to root `<Control-s>` / `<Control-Shift-S>` bindings and never double-fire either save handler.
- **Exact Surface Updates:**

| Surface (`file:line`) | Current | New |
|---|---|---|
| `misora.py:8976-8978` (`_on_misora_shortcut`) | `Ctrl+S` -> `self.on_save()` (`return "break"`) | `Ctrl+S` -> `self.on_save_project()` + `return "break"` |
| `misora.py:9015-9034` (`_on_misora_shortcut` shift) | *(no `s`)* | `Ctrl+Shift+S` -> `self.on_save()` + `return "break"` |
| `misora.py:9211` (`_bind_shortcuts` root bind) | `self.bind("<Control-s>", lambda e: self.on_save())` | `self.bind("<Control-s>", lambda e: self.on_save_project())` + `<Control-Shift-S>` / `<Control-Shift-s>` -> `self.on_save()` |
| `misora.py:4541` (`file_menu`) | `"Save Project (.misora)..."` (no accelerator) | `"Save Project (.misora)"`, `command=self.on_save_project`, `accelerator="Ctrl+S"` + new `"Save Project As (.misora)..."`, `command=lambda: self.on_save_project(save_as=True)` |
| `misora.py:4543` (`file_menu`) | `"Save & Patch Bundle"`, `accelerator="Ctrl+S"` | `"Save File / Patch Bundle"`, `command=self.on_save`, `accelerator="Ctrl+Shift+S"` |
| `misora.py:8864` (`btn_save` toolbar) | `text=" Save & Patch Bundle (Ctrl+S)"` | `text=" Save File / Patch Bundle (Ctrl+Shift+S)"` + explicit tooltip distinguishing `Ctrl+Shift+S` (Save File / Patch Bundle + XUAT sync) from `Ctrl+S` (Save Project `.misora`) |
| `misora.py:16106` (tab context menu) | `label="Save File (Ctrl+S)"` | Type-aware dynamic label inspecting the **right-clicked tab's file type** (`doc_info = self.open_documents.get(target_path, {})`; `is_bundle_target = bool(doc_info.get("is_bundle", False)) or target_path.suffix.lower() == ".unity3d"` — NOT active tab's `self.is_bundle_file`): `"Save & Patch Bundle (Ctrl+Shift+S)"` if `is_bundle_target` else `"Save File (Ctrl+Shift+S)"` |
| `README.md:30, 37, 72–73` | `Ctrl+S` = Save & Patch; `Ctrl+Shift+S` = Save As (stale) | `Ctrl+S` = **Save Project (`.misora`)** (saves workspace session refs/state/locks ONLY); `Ctrl+Shift+S` = **Save File / Patch Bundle** (saves/patches active `.unity3d`/`.v2.txt`/`.txt` + optional XUAT sync); remove stale `"Save As"` |

### 4B. Data-Safety Safeguards & Full `_current_project_path` Lifecycle (`misora.py`)

- **Data-Safety Invariants (`Ruling 1`):**
  1. `save_project()` / `on_save_project()` **NEVER** clears `self.is_dirty`, `open_documents[p]["dirty"]`, or calls `self.undo_journal.mark_saved(...)`.
  2. `save_project()` emits honest post-save status & toast:
     - Status: `f"Saved project '{ws_path.name}' ({len(file_entries)} file(s)) — story edits not yet written to bundle/XUAT (Ctrl+Shift+S to save file)."`
     - Toast: `"Project (.misora) saved — story edits are not yet written to bundle/XUAT (use Ctrl+Shift+S to save file)."`
  3. Dirty-close (`close_file`, `_on_app_exit`) continues prompting Save/Discard/Cancel (`AGENTS.md` §16) even immediately after `Ctrl+S`.
  4. `save_project()` preserves and runs `self._flush_active_widget()` (which calls `self._flush_quick_edit_session()`) cleanly without clearing dirty flags.

- **Explicit `_current_project_path: Optional[Path]` Lifecycle (Cases `a`–`g`):**
  - Initialize `self._current_project_path: Optional[Path] = None` in `MisoraApp.__init__`.
  - **(a) First `Ctrl+S` (`_current_project_path is None`):** `on_save_project(save_as=False)` prompts `filedialog.asksaveasfilename(...)`; if user selects `target`, calls `save_project(Path(target))`.
  - **(b) Subsequent `Ctrl+S` (`_current_project_path is not None`):** `on_save_project(save_as=False)` calls `save_project(self._current_project_path)` directly without reopening `asksaveasfilename()`.
  - **(c) After `open_project(ws_path)` (with >=1 resolved file):** sets `self._current_project_path = ws_path.resolve()` so subsequent `Ctrl+S` updates that loaded `.misora` path.
  - **(d) Cancelled or Failed Saves:** If `asksaveasfilename()` returns empty (`""`/`None`) OR `save_project()` returns `False`, `_current_project_path` is **NEVER** set or overwritten (retains its prior value). Only on `save_project()` returning `True` is `self._current_project_path = ws_path.resolve()` assigned.
  - **(e) Close-All / Last-File-Close / All-Missing Workspace:**
    - When `close_file()` closes the last document (`not self.open_documents`), or `_close_all_documents_without_prompt()` runs, reset `self._current_project_path = None`.
    - When `open_project(ws_path)` loads a workspace whose referenced files are **ALL missing** (`not opened_entries`), keep `self._current_project_path = None` so subsequent edits on unrelated newly opened files never silently overwrite the broken `.misora` without prompting.
  - **(f) Separate `"Save Project As (.misora)..."`:** Menu command calls `on_save_project(save_as=True)` which ALWAYS prompts `asksaveasfilename()`, updating `_current_project_path` only if `save_project()` succeeds.
  - **(g) Active Widget & Quick Edit Flush on `Ctrl+S`:** `save_project()` continues calling `self._flush_active_widget()` (which calls `self._flush_quick_edit_session()`), tested explicitly with dirty state preserved afterward.

---

## 5. `Q-04` — Manual S10/S11 Investigation Items (`1.1`, `1.2`, `1.3`)

- **`1.1` (`▶` icon above >54-char textboxes):** Confirmed in `misora.py` (`_AllScriptPoolCard` active highlight: `▶ [BOX #NNN]` vs `◆ [BOX #NNN]`). It is the intended Active Box header indicator, not a separate broken control. Document in `PROJECT_STATE.md`; **no code change, no manufactured test**.
- **`1.2` (Multi-match Name / Title / Subtitle boxes with >3 linebreaks — text selection, drag, and scrolling):**
  - *Correction applied:* `state="disabled"` on `tk.Text` prevents editing **only** — it does **not** disable selection, copy, drag, or scrolling.
  - *Empirical check run during `/plan` (`ImportFromXUATDialog` & Main View):*
    - **Text selection (`tag_add("sel", ...)` & `<ButtonPress-1>` + `<B1-Motion>` drag):** Works in both `ImportFromXUATDialog` (`txt_right` on `meta`, `actor`, `dialogue`) and Main View (`txt_dialogue`, `txt_box0_summary`).
    - **Scrolling:** `<MouseWheel>` scrolls 3-line `dialogue` rows when `has_line_overflow=True`, while 1-line `meta`/`actor` rows (`lines=1`) gate `has_v` via `lines >= 3` (`misora.py:20274-20275`) and delegate wheel events to the outer canvas; in Main View, `entry_speaker` and `entry_box0_title`/`subtitle` are single-line `tk.Entry` widgets (cannot hold `>3` linebreaks).
  - **Status (`Ruling 3`):** Recorded honestly as **`NOT REPRODUCED — NEEDS USER REPRODUCTION DETAILS`** in `PROJECT_STATE.md`. Box 0 stays excluded from ordinary dialogue rows (`S11d` `Q-08` handles multi-line Synopsis import). Zero manufactured failing tests.
- **`1.3`:** Strictly labeled **`NOT TESTED`** everywhere.

---

## 6. `Q-23` — Remove Red Overflow Highlight Blocks in Dialogue Preview (`misora.py`, Tests)

- Remove `if not getattr(self, "is_box0_active", False): self._apply_overflow_highlights(txt_w)` from `misora.py::_render_dialogue_preview_frame()` (lines `7594–7595`).
- Add defensive guard at top of `misora.py::_apply_overflow_highlights()` (line `13206`):
  ```python
  if widget is getattr(self, "txt_dialogue_preview", None):
      try:
          widget.tag_remove("line_overflow", "1.0", tk.END)
      except Exception:
          pass
      return
  ```
- Preserve `wrap="none"` native bleed, `54d × 3` calibration, pink `#C24270` nameplate with WCAG contrast, gold border, unclipped pink `▼`, and read-only non-save behavior; Dialogue Editor (`Preview OFF`) retains red overflow markers unchanged.
- **Test Migrations (`m-5`):**
  - `tests/test_v15_s03_all_script_preview_paste.py::test_probe_3`: change `>= 2` `line_overflow` ranges on `txt_dialogue_preview` -> `== ()`, and assert Dialogue Editor (`Preview OFF`) retains red `line_overflow` markers.
  - `tests/test_p3_s18_game_preview.py::test_01`: add `self.assertEqual(self.app.txt_dialogue_preview.tag_ranges("line_overflow"), ())` (`m-5`).

---

## 7. Test Plan (`tests/test_v15_s11b_scanner_save_preview.py`)

### Confirmed Failing-First Probes (3 — MUST FAIL pre-patch, PASS post-patch):
1. `test_probe_1_xuat_strict_en_text_roots_exclusions_and_canonical_metrics`:
   - Tests all 5 user entry-point categories (6 concrete path forms: `<GameRoot>\src\BepInEx\Translation\en\Text`, `<GameRoot>\BepInEx\Translation\en\Text`, `<BepInEx>\Translation\en\Text`, `<Translation>\en\Text`, `<Translation\en>\Text`, `<Translation\en\Text>`) + valid direct `.txt` inside `Translation\en\Text`.
   - Rejects all 5 forbidden locations (`Translation\ja\Text`, arbitrary `Text/`, standalone `.txt` outside, `Translation\en\Other`, `Translation\en\RedirectedResources`).
   - Verifies all 5 new rule exclusions via `endswith` (`*.font.txt`, `*.resizer.txt`, `*Postprocessors.txt`, `*Preprocessors.txt`, `*Substitutions.txt`) + legacy exclusions, AND verifies a valid file containing e.g. `substitutions` mid-stem (if not ending in `substitutions.txt`) or verifying strict tail match.
   - Verifies root/file deduplication + **`m-2`** simulated read/decode failure (invalid bytes / `OSError`) confirming `files_scanned == len(files_indexed) + len(skipped_files)` (failed file counted in `files_scanned` & `skipped_files`, excluded/duplicate NOT counted) and visually distinguished in status & `ImportFromXUATDialog` summary labels.
   - Verifies metric math backed by `_norm_stripped_map` (`entries_read == entry_count == unique_keys + duplicate_entries`, `unique_keys == len(_norm_stripped_map)`, `duplicate_keys`) across single, 2x, 3x duplicates and empty/invalid normalized keys.
   - Verifies `_exact_map` & `_value_map` lookup parity including an explicit regression test constructing a `XuatIndex` containing **ONLY** an empty-normalized-key entry (e.g., `"[FF0000][-]=TagOnlyVal"`): asserts `bool(idx) is True`, `len(idx) == 0`, `idx.entry_count == 0`, `idx.entries_read == 0`, `len(idx._norm_stripped_map) == 0`, AND `MTLEngine(MTLConfig(active_engine="XUAT Cache", use_xuat_cache=True)).translate("[FF0000][-]", xuat_cache=idx) == "TagOnlyVal"`.
2. `test_probe_2_ctrl_s_saves_project_and_bundle_patch_has_dedicated_shortcut`:
   - Tests `Ctrl+S` -> `on_save_project()` (not `on_save()`) and `Ctrl+Shift+S` -> `on_save()` across `_on_misora_shortcut` & root binds; verifies `_on_misora_shortcut()` returns `"break"` for both `Ctrl+S` and `Ctrl+Shift+S` AND real keypress dispatch on a `MisoraShortcuts`-bound editor widget fires `on_save_project` / `on_save` **exactly once** (zero double-fire).
   - Verifies File menu (`Save Project (.misora)` `Ctrl+S`, `Save Project As (.misora)...`, `Save File / Patch Bundle` `Ctrl+Shift+S`), `btn_save` (`Save File / Patch Bundle (Ctrl+Shift+S)` + tooltip), type-aware tab context menu inspecting the **right-clicked tab's file type** across **bundle** (`Save & Patch Bundle (Ctrl+Shift+S)`), **`.v2.txt`** (`Save File (Ctrl+Shift+S)`), and **plain `.txt`** (`Save File (Ctrl+Shift+S)`), and `README.md` (no stale `"Save As"` for `Ctrl+Shift+S`). (Confirms `tests/test_p3_s13_ribbon_shortcuts.py` remains untouched.)
   - Tests all 7 `_current_project_path` lifecycle & data-safety cases `(a)`–`(g)`:
     - `(a)` first `Ctrl+S` prompts `asksaveasfilename()`,
     - `(b)` subsequent `Ctrl+S` saves directly without prompt,
     - `(c)` `open_project()` binds `_current_project_path` so `Ctrl+S` updates it,
     - `(d)` cancelled or failed save never sets/overwrites `_current_project_path`,
     - `(e)` closing last/all docs OR `open_project()` with all files missing resets `_current_project_path` to `None`,
     - `(f)` `"Save Project As (.misora)..."` (`save_as=True`) always prompts,
     - `(g)` `Ctrl+S` runs `_flush_active_widget()` (and `_flush_quick_edit_session()`), keeps `is_dirty=True` and `undo_journal` unsaved, emits honest post-`Ctrl+S` toast, and dirty-close still prompts Save/Discard/Cancel.
3. `test_probe_3_dialogue_preview_has_zero_red_blocks_while_editor_keeps_markers`:
   - `txt_dialogue_preview.tag_ranges("line_overflow") == ()` on >54d / 4-line text; direct `_apply_overflow_highlights(app.txt_dialogue_preview)` still returns `()`; `wrap="none"`, pink nameplate, gold border, pink `▼`, `54d × 3` intact; Dialogue Editor (`Preview OFF`) keeps red markers.

### Regression Guards (2 — MUST PASS pre-patch and post-patch):
1. `test_guard_1_core_xuat_index_free_of_tkinter_and_misora_imports`
2. `test_guard_2_dialogue_preview_readonly_non_save_and_box0_exemption_intact`

---

## 8. File Change Matrix (Authorized Only After `Proceed`)

| File | Action | Exact Changes |
|---|---|---|
| `__init__.py` | Modify | Bump `"1.4.10"` -> `"1.4.11"` |
| `core/xuat_index.py` | Modify | Strict `resolve_xuat_text_roots()`, `m-1` `endswith` exclusions, `files_scanned` + `entries_read`/`unique_keys`/`duplicate_keys`/`duplicate_entries`, `entry_count` valid-key guard, `__bool__() -> bool(self.entries)` |
| `misora.py` | Modify | `_resolve_xuat_text_root` `src/BepInEx`, `m-2` status/Import labels, `Ctrl+S` -> `on_save_project()` (`"break"`), `Ctrl+Shift+S` -> `on_save()` (`"break"`), `_current_project_path` lifecycle (a–g) + honest toast, File menu (`"Save File / Patch Bundle"`) / `btn_save` (`"Save File / Patch Bundle (Ctrl+Shift+S)"`) / right-clicked-tab-aware context menu, `Q-23` preview highlight removal + defensive guard |
| `README.md` | Modify | Update `Ctrl+S` -> Save Project (`.misora`), replace stale `Ctrl+Shift+S = Save As` with `Save File / Patch Bundle` |
| `CHANGELOG.md` | Modify | Add `### S11b (v1.4.11)` |
| `PROJECT_STATE.md` | Modify | Record 5-stage profiling, `Q-04` (`1.1` intended, `1.2` `NOT REPRODUCED — NEEDS USER REPRODUCTION DETAILS`, `1.3` `NOT TESTED`), `Q-18` `DEFERRED`, test baseline, Manual Windows QA checklist (incl. real `.unity3d` save timing) |
| `tests/test_v15_s11b_scanner_save_preview.py` | Create | 3 failing-first probes + 2 regression guards |
| `tests/test_v15_s03_all_script_preview_paste.py` | Modify | Migrate `txt_dialogue_preview` `line_overflow` assertion (`>= 2` -> `()`) + assert Editor retains markers |
| `tests/test_p3_s18_game_preview.py` | Modify | Add `m-5` `self.assertEqual(self.app.txt_dialogue_preview.tag_ranges("line_overflow"), ())` inside `test_01` |

**Untouched Existing Shortcut Suite:** `tests/test_p3_s13_ribbon_shortcuts.py` (does NOT lock `Ctrl+S -> on_save()`).
**Forbidden Files (Strictly Untouched):** `core/story_ast.py`, `core/bundle_io.py`, `core/script_codec.py`, `core/xuat_cleanup.py`, `core/xunity_sync.py`, `core/word_wrap.py`, `core/mtl_engine.py`, `core/undo_journal.py`, `assets/*`, `requirements.txt`, `misora_config.json`, `backups/`.
