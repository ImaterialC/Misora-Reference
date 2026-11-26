# S11b (v1.4.11) — Implementation Plan

> **Status:** 🛑 **AWAITING PROJECT LEAD `Proceed`** — no files will be modified until explicit approval.

---

## 0. Pre-Session Environment Snapshot

| Item | Value |
|---|---|
| **Branch** | `main` |
| **HEAD** | `c1ec40c96c18ae6e4df61d1db77ebf999114be3d` |
| **Working Tree** | `M assets/icons/BoxInsert.png`, `?? assets/icons/BoxReplace.png` (pre-existing, NOT S11b) |
| **Python** | 3.12.10 |
| **`__version__`** | `"1.4.10"` |
| **Test Baseline** | 440 discovered · 397 pass · 35 fixture-skipped · 6+2 pre-existing · 0 regressions |

---

## 1. STOP Gate Decisions

### STOP Gate A (`Q-02` Save Hang Architecture) — ✅ CLEAR

**5-Stage Save Profiling** (symbol-bound audit of `misora.py::on_save()` lines 13419–13570):

| Stage | Lines | Description | Blocking? |
|---|---|---|---|
| **1. Widget Flush** | 13429, 13459–13491 | `_flush_quick_edit_session()` + `_on_box0_metadata_edited()` + `inject_box()` on current box | ❌ In-memory only, nanoseconds |
| **2. Project `.misora`** | N/A | **Not called by `on_save()`** — `save_project()` is a separate method on line 15862, invoked via `on_save_project()` (line 15847). `Ctrl+S` → `on_save()` does NOT call `save_project()`. | N/A |
| **3. XUAT Sync** | 13530–13557 | `_sync_modified_boxes_to_xuat()` — synchronous file I/O for each modified box, reads XUAT files, finds lines, rewrites atomically. Only runs when `var_sync_xuat` is True AND XUAT roots are set AND boxes were modified. | ⚠️ Proportional to file count/size, but bounded |
| **4. Bundle Serialization** | 13492–13510 | `save_bundle_story()` — imports from `core/bundle_io.py`, serializes UnityPy env, writes `.tmp`, verifies, `os.replace()`. Single synchronous call. | ⚠️ **Main bottleneck** — UnityPy repack + LZ4 compress + disk I/O. Typically 50–300ms for small bundles, can grow for large ones. |
| **5. Post-Save UI** | 13503–13510 | `lbl_status.config()`, `_dirty_state_changed()`, `undo_journal.mark_saved()` | ❌ Trivial |

**Analysis:** The save hang (if present) is dominated by Stage 4 (`save_bundle_story` in `core/bundle_io.py`) which is a **forbidden file**. Making this async would require:
1. Moving `save_bundle_story()` to a worker thread
2. Blocking concurrent document mutations during save
3. Tk-safe completion callback

However, the `Q-02` request is specifically about `Ctrl+S` **shortcut remapping**, not about eliminating the bundle save time. The bounded fix within S11b scope is:
- **Remap `Ctrl+S` → `save_project()` (lightweight `.misora` write)**
- **Give bundle save its own shortcut (`Ctrl+Shift+S`)**
- Stage 3 (XUAT sync) only runs for bundle saves, not project saves

This remap is **fully within S11b Allowed Files** (`misora.py` shortcut router + menu + `README.md`). **No forbidden core file changes required.**

> [!IMPORTANT]
> If the user reports a *measurable* save hang even after the remap (i.e., `save_bundle_story` itself takes seconds), that remediation is deferred to its own async-save session per STOP Gate A rules. S11b only remaps the shortcut and documents the profiling.

### STOP Gate B (`Q-18` Ruby Preview) — 🛑 TRIGGERED → `Q-18` DEFERRED

**Inspection of `_insert_compiled_ngui_text()` (lines 7708–7810):**

The ruby rendering at lines 7770–7775 handles `[rub:ruby]base[/rub]` by:
1. Emitting `base_txt` via `emit_styled_run()` (inherits current style)
2. Appending `ruby_txt` inline with the `compiled_ruby` tag (small bold font, +5px vertical `offset`)

The `compiled_ruby` tag (line 3538–3543) configures:
```python
widget.tag_configure("compiled_ruby",
    foreground=hl_fg, background=t["highlight_bg"],
    font=(d_fam, max(7, d_sz - 3), "bold"), offset=5)
```

**Problem:** `tk.Text` has no native ability to render text *above* other text. The `offset=5` raises the ruby text vertically within the same line, but it still occupies horizontal space inline *after* the base text. This means `[rub:めいれい]願い[/rub]` renders as `願いめいれい` (base then ruby inline), not as:
```
めいれい
 願い
```

**Verdict:** Proper above-text ruby display requires a **custom Canvas-based text layout engine** (computing per-character positions, rendering base text on one line and ruby annotations above each base character/group). This is a significant renderer rewrite, not a bounded bug fix.

> [!CAUTION]
> **`Q-18` is DEFERRED** to its own bounded session per STOP Gate B. No implementation-specific failing-first test will be created for the deferred renderer work. Auto-Furigana (MeCab) remains out of scope (`BIG-02`).

---

## 2. `Q-01` — Strict XUAT English Text Scanner & Canonical Metrics

### 2A. `resolve_xuat_text_roots()` Tightening (`core/xuat_index.py` lines 134–181)

**Current Permissive Bypasses Found:**

1. **Line 156–158:** Direct `.txt` files accepted without checking parent is under `Translation\en\Text`
2. **Lines 161–172:** Cascading candidates `p / "BepInEx" / "Translation" / "en" / "Text"`, `p / "Translation" / "en" / "Text"`, `p / "en" / "Text"`, `p / "Text"` — the last two (`en/Text` and bare `Text`) accept non-canonical directories like `ja/Text` or arbitrary `Text/`
3. **Lines 177–179:** Bare `text` directory name accepted as fallback without validating parent chain

**Planned Fix:**

```
Supported Entry Points (ALL 5):
1. <GameRoot>  → <GameRoot>/src/BepInEx/Translation/en/Text  OR  <GameRoot>/BepInEx/Translation/en/Text
2. <BepInEx>   → <BepInEx>/Translation/en/Text
3. <Translation> → <Translation>/en/Text
4. <Translation\en> → <Translation\en>/Text
5. <Translation\en\Text> → accepted directly ONLY when trailing segments match Translation/en/Text (case-insensitive)

Direct .txt  → accepted ONLY when resolved parent is strictly inside a canonical Translation/en/Text subtree

Rejected: ja/Text, arbitrary Text/, standalone .txt outside, en/Other, en/RedirectedResources
```

Replace the cascade list with explicit segment matching:
- Check `p / "src" / "BepInEx" / "Translation" / "en" / "Text"` (Priconne-TL layout)
- Check `p / "BepInEx" / "Translation" / "en" / "Text"`
- Check `p / "Translation" / "en" / "Text"`
- Check `p / "en" / "Text"` ONLY when `p.name.lower() == "translation"`
- Check `p / "Text"` ONLY when parent chain ends `Translation/en` (case-insensitive)
- Accept `p` directly ONLY when its trailing 3 path segments match `translation/en/text` (case-insensitive)
- For `.txt` files: validate `_is_inside_canonical_en_text(p.parent)` before accepting

### 2B. Additive File Exclusions

Add to `_is_excluded_xuat_file()`:
```python
_EXCLUDED_RULE_TAILS = (".font.txt", ".resizer.txt")
_EXCLUDED_RULE_CONTAINS = ("postprocessors.txt", "preprocessors.txt", "substitutions.txt")
```
Preserving all legacy exclusions (`.missing.txt`, `.report.txt`, `_summary.txt`, `_warnings.txt`, `.bak_`).

### 2C. Canonical Metrics on `XuatIndex`

**Caller Audit of `len(idx)` / `bool(idx)`:**

| Caller | File | Usage | Impact of `entry_count` change |
|---|---|---|---|
| `__bool__` | `xuat_index.py:314` | `entry_count > 0` | ✅ Empty-normalized-key entries still increment `entry_count` currently |
| `__len__` | `xuat_index.py:317` | returns `entry_count` | ⚠️ See below |
| `__contains__` | `xuat_index.py:320` | delegates to `lookup_translation` | ✅ Unaffected |
| MTLEngine cache | `misora.py` (various) | `bool(idx)` / `len(idx)` for cache validity | ✅ Truthiness preserved since non-empty indices still have `entry_count > 0` |

**Current `add_entry()` behavior (line 238–250):** Increments `entry_count` unconditionally for every call. Empty normalized keys are excluded from `_norm_stripped_map` but still count in `entry_count` and appear in `entries`/`_exact_map`/`_value_map`.

**Planned Change:**
- `entry_count` will ONLY increment when `normalize_xuat_key(raw_key, strip_ngui=True) != ""` — this is `entries_read` semantics
- Expose `entries_read` as a property aliased to `entry_count`
- Add `files_scanned` as a persistent attribute: `files_scanned = len(files_indexed) + len(skipped_files)`, maintained by `build_xuat_index()` after scan completion
- **Empty-normalized-key entries still enter `entries`, `_exact_map`, `_value_map`** — only `entry_count` increment is guarded
- Exposed metrics: `files_scanned`, `entries_read` (= `entry_count`), `unique_keys = len(_norm_stripped_map)`, `duplicate_keys`, `duplicate_entries = entries_read - unique_keys`

**Risk Assessment:** The only place `len(idx)` is used for a numeric count is `__len__`. Since empty-normalized-key entries are extremely rare (whitespace-only or NGUI-tag-only keys with no base text), the practical impact is near-zero. The semantic change is correct: `entry_count` should reflect valid translation entries, not parse artifacts.

### 2D. Existing Test Pre-Check

All existing XUAT tests create `Translation/en/Text` directories properly:
- `test_p3_s22_import_xuat.py` line 83: `proj_dir / "BepInEx" / "Translation" / "en" / "Text"` ✅
- `test_v15_s07_xuat_cleanup_archive.py` lines 102–105: same pattern ✅
- `test_v15_s11_xuat_archiving_progress.py` lines 103–105: same pattern ✅

**No existing test creates a bare `Text/` directory that would break under the strict resolver.** No test updates needed for existing XUAT tests beyond S11b's new test file.

---

## 3. `Q-02` — Save Shortcut Remap & Bounded Save-Hang Fix

### 3A. `Ctrl+S` → Save Project; `Ctrl+Shift+S` → Save & Patch Bundle

**Conflict Check:** `Ctrl+Shift+S` is currently **not bound** in `_on_misora_shortcut()`. The `is_shift` branch (lines 9015–9033) handles `z`, `c`, `v`, `t`, `i`, `e` — no `s`. The menu at line 4543 shows `"Save & Patch Bundle"` with accelerator `"Ctrl+S"` — no `"Save As"` or `"Ctrl+Shift+S"` exists anywhere in the codebase. ✅ **No conflict.**

**Changes Required:**

| Surface | Current | New |
|---|---|---|
| **Shortcut Router** (`_on_misora_shortcut`, line 8976–8978) | `Ctrl+S` → `on_save()` | `Ctrl+S` → `on_save_project()` |
| **Shortcut Router** (new, `is_shift` block) | — | `Ctrl+Shift+S` → `on_save()` |
| **File Menu** (line 4541) | `"Save Project (.misora)..."` (no accelerator) | `"Save Project (.misora)..."`, accelerator=`"Ctrl+S"` |
| **File Menu** (line 4543) | `"Save & Patch Bundle"`, accelerator=`"Ctrl+S"` | `"Save & Patch Bundle"`, accelerator=`"Ctrl+Shift+S"` |
| **Tab Context Menu** (line 16106) | `"Save File (Ctrl+S)"` | `"Save & Patch Bundle (Ctrl+Shift+S)"` |
| **README.md** (line 72) | `Ctrl+S` → Save & Patch | `Ctrl+S` → Save Project; new row `Ctrl+Shift+S` → Save & Patch Bundle |

### 3B. `on_save_project()` Quick-Save Behavior

Currently `on_save_project()` (line 15847) opens a **file dialog** every time. For `Ctrl+S` to feel instant, we need a quick-save path:

- If a `.misora` project is already open/loaded → save to the same path without dialog
- If no project is loaded → prompt with file dialog (current behavior)
- Add `self._current_project_path: Optional[Path]` tracked on `open_project()` and `save_project()`

---

## 4. `Q-04` — Manual Investigation Findings

### 4.1 `▶` Icon Above >54-char Textboxes

**Finding:** The `▶` symbol is the **Active Box header indicator** in All Script mode: `"▶ [BOX #NNN]"` (line 9143 area, `_AllScriptPoolCard` active highlight). It appears in the card header when a box is the currently selected/active box in All Script view. It is NOT a separate clickable control — it is part of the header label text that changes from `"[BOX #NNN]"` to `"▶ [BOX #NNN]"`.

**Verdict:** This is the **intended Active Box marker**, not a broken control. **No fix needed, no failing test manufactured.** Document in `PROJECT_STATE.md`.

### 4.2 Multi-match Text Selection, Drag, Scrolling

**Finding:** `ImportFromXUATDialog` uses paired read-only `tk.Text` widgets with `state="disabled"`. Text selection, drag, and scrolling are natively disabled on `state="disabled"` Text widgets. The main view dialogue `txt_dialogue` has `state="normal"` and supports native selection/drag.

**Verdict:** Need to verify if the user's report refers to the 1-line metadata rows or the 3-line dialogue rows. Without a concrete reproduction, **document as CONDITIONAL (requires user reproduction steps).** No failing-first test manufactured.

### 4.3 (`1.3`) — `NOT TESTED`

Strictly labeled **`NOT TESTED`** everywhere. No bug report, no test.

---

## 5. `Q-23` — Remove Red Overflow Highlights in Dialogue Preview

### Changes in `misora.py`:

**A. Remove call at line 7594–7595:**
```python
# BEFORE:
if not getattr(self, "is_box0_active", False):
    self._apply_overflow_highlights(txt_w)

# AFTER:
# Q-23: Dialogue Preview never receives overflow highlights (wrap="none" native bleed only)
```

**B. Add defensive guard inside `_apply_overflow_highlights()` (line 13206):**
```python
def _apply_overflow_highlights(self, widget: Optional[tk.Text]) -> None:
    if not widget or not widget.winfo_exists():
        return
    # Q-23 Defensive: Dialogue Preview NEVER receives overflow highlights
    if widget is getattr(self, "txt_dialogue_preview", None):
        try:
            widget.tag_remove("line_overflow", "1.0", tk.END)
        except Exception:
            pass
        return
    # ... rest of existing logic unchanged ...
```

**C. Test Migrations:**

- `test_v15_s03_all_script_preview_paste.py::test_probe_3` line 202:
  - Change: `self.assertTrue(len(self.app.txt_dialogue_preview.tag_ranges("line_overflow")) >= 2)` → `self.assertEqual(self.app.txt_dialogue_preview.tag_ranges("line_overflow"), ())`
  - Add assertion: Editor (`Preview OFF`) still receives red overflow ranges

- `test_p3_s18_game_preview.py::test_01` — no assertion on `line_overflow` in current code (confirmed by reading lines 88–152). No migration needed.

---

## 6. Test Plan — `tests/test_v15_s11b_scanner_save_preview.py`

### Confirmed Failing-First Probes (3):

| # | Name | Tests |
|---|---|---|
| 1 | `test_probe_1_xuat_strict_en_text_roots_exclusions_and_canonical_metrics` | 5 valid entry points + direct `.txt` inside canonical tree; 5 forbidden targets rejected; 5 new XUAT exclusions + legacy preservation; root/file dedup with `files_scanned` identity; exact metric math (`entries_read == entry_count == unique_keys + duplicate_entries`); exact/value lookup parity including empty-normalized-key edge case |
| 2 | `test_probe_2_ctrl_s_saves_project_and_bundle_patch_has_dedicated_shortcut` | `Ctrl+S` routes to Save Project (not `on_save`); `Ctrl+Shift+S` routes to `on_save()`; menu labels/accelerators match; tab context menu updated |
| 3 | `test_probe_3_dialogue_preview_has_zero_red_blocks_while_editor_keeps_markers` | `txt_dialogue_preview.tag_ranges("line_overflow") == ()` with >54d text; defensive guard blocks direct call; `wrap="none"`, pink nameplate, gold border, pink `▼`, `54d × 3` intact; Dialogue Editor (`Preview OFF`) retains red markers |

### Conditional Probes (ONLY if reproduced):
| # | Name | Condition |
|---|---|---|
| 4 | `test_probe_4_confirmed_q04_12_repro` | ONLY if `Q-04.1.2` defect is actually reproduced — **SKIPPED (not reproduced)** |
| 5 | `test_probe_5_ruby_preview_rendering` | ONLY if `Q-18` does NOT trigger STOP Gate B — **SKIPPED (STOP Gate B triggered)** |

### Regression Guards (2):
| # | Name |
|---|---|
| 1 | `test_guard_1_core_xuat_index_free_of_tkinter_and_misora_imports` |
| 2 | `test_guard_2_dialogue_preview_readonly_non_save_and_box0_exemption_intact` |

---

## 7. File Change Matrix

| File | Action | Scope |
|---|---|---|
| `__init__.py` | Modify | Bump `"1.4.10"` → `"1.4.11"` |
| `core/xuat_index.py` | Modify | Strict `resolve_xuat_text_roots()`, additive exclusions, `files_scanned`/`entries_read` metrics, `entry_count` guard |
| `misora.py` | Modify | `Ctrl+S` → `on_save_project()` quick-save, `Ctrl+Shift+S` → `on_save()`, menu/accelerator/tooltip updates, Q-23 overflow removal + defensive guard, `_current_project_path` tracking |
| `README.md` | Modify | Update shortcut table: `Ctrl+S` → Save Project, add `Ctrl+Shift+S` → Save & Patch Bundle |
| `CHANGELOG.md` | Modify | Add `### S11b (v1.4.11)` section |
| `PROJECT_STATE.md` | Modify | Record S11b profiling, Q-04 findings (`1.3 = NOT TESTED`), Q-18 STOP Gate B deferral, verification baseline, Manual QA checklist |
| `tests/test_v15_s11b_scanner_save_preview.py` | **Create** | 3 failing-first probes + 2 regression guards |
| `tests/test_v15_s03_all_script_preview_paste.py` | Modify | Migrate `line_overflow` assertion on `txt_dialogue_preview` from `>= 2` → `== 0` |
| `tests/test_p3_s18_game_preview.py` | Inspect-only | No `line_overflow` assertion on `txt_dialogue_preview` exists; no change needed |

**Forbidden Files — Confirmed Untouched:**
`core/story_ast.py`, `core/bundle_io.py`, `core/script_codec.py`, `core/xuat_cleanup.py`, `core/xunity_sync.py`, `core/word_wrap.py`, `core/mtl_engine.py`, `core/undo_journal.py`, `assets/*`, `requirements.txt`, `misora_config.json`, `backups/`

---

## 8. Verification Commands (Post-Patch)

```bash
# 1. Pre-patch probe run (confirmed probes FAIL, guards PASS)
py -3.12 -m unittest tests.test_v15_s11b_scanner_save_preview -v

# 2. Post-patch compile check
py -3.12 -m compileall -q __init__.py misora.py core assets tests

# 3. Post-patch targeted suites
py -3.12 -m unittest tests.test_v15_s11b_scanner_save_preview tests.test_v15_s03_all_script_preview_paste tests.test_p3_s18_game_preview tests.test_v15_s11_xuat_archiving_progress tests.test_v15_s07_xuat_cleanup_archive tests.test_p3_s22_import_xuat -v

# 4. Full discovery
py -3.12 -m unittest discover -s tests -v

# 5. Git status
git status --short
```

---

## 9. STOP Gate Summary & Deferred Items

| Gate | Decision | Reason |
|---|---|---|
| **A** (`Q-02` Save Hang) | ✅ **CLEAR** — bounded shortcut remap within S11b scope | Bundle save bottleneck is in `core/bundle_io.py` (forbidden). `Ctrl+S` remap to lightweight `.misora` save eliminates the common-case hang. |
| **B** (`Q-18` Ruby Preview) | 🛑 **TRIGGERED** — `Q-18` deferred to own session | Proper above-text ruby display requires a custom Canvas text-layout engine; `tk.Text` has no native above-text rendering. Current inline `compiled_ruby` with `offset=5` is a design limitation, not a code bug. |

| Deferred Item | Target Session |
|---|---|
| `Q-18` Ruby Preview proper renderer | Own bounded session (custom Canvas layout) |
| `Q-22` Quick Edit single-box unification | S11c |
| `Q-06`–`Q-12` Import UX & productivity | S11d |
| `Q-03`, `Q-05`, `Q-13`–`Q-17` | S11e |
| `BIG-01`–`BIG-03` | Track B post-v1.5.0 |
| Async `save_bundle_story` | Own session (if save hang measured after remap) |
