# T-01 (BUG-UI-EMPTY-STATE-01) — Implementation Plan (Rev 2)

**Evidence:** `CONFIRMED` (upgraded from `REPORTED + NEEDS-REPRO` via source audit + real `MisoraApp` reproduction)  
**Lifecycle:** `ACTIVE` (remains `ACTIVE` until Windows manual QA `M-1..M-12` passes)  
**Prepared:** 2026-11-28 (Rev 2 incorporating Gemini + GPT-6 review rulings)  
**Scope:** Minimal root-cause fix to `_update_empty_state_visibility()` in `misora.py` (8 lines) + strict TDD suite `tests/test_t01_empty_state_overlay.py`

---

## 1. Preflight Verification Transcript

```text
D:/Misora-Editor                                        # git rev-parse --show-toplevel
main                                                    # git branch --show-current
648cb52b0fccda5e46e26eecf90e3f1dbd719a75                # git rev-parse HEAD
(empty)                                                 # git status --short --untracked-files=all
CHECK PASS: docs/architecture/MISORA_SYMBOL_INDEX.md    # py -3.12 -B tools/generate_symbol_index.py --check
countTestCases: 475                                     # unittest discovery (tests/)
```

- Working tree is **100% clean** on branch `main` at ENV-01 HEAD `648cb52b0fccda5e46e26eecf90e3f1dbd719a75`.
- Product version: `1.4.15` (root `__init__.py`; unchanged, no version promotion authorized; `v1.5.0` remains `CANCELLED / NOT RELEASED`).
- `MISORA_SYMBOL_INDEX.md` records `Indexed Source Revision: ead65077a2a6cf3a664543cfb50f855268a29e2a` (the last commit touching indexed `.py` files) and `misora.py` SHA-256 `60c8ac82bf15d20faab81e28e277947112cd321a79895a36dfa94f9f613c8a82`; `--check` exits `0`.

---

## 2. Exact Source Audit & Real `MisoraApp` Reproduction

### 2.1 Source audit (`misora.py`)

- `MisoraApp.__init__` (`misora.py:2026-2425`):
  - Line `2036`: calls `super().withdraw()` **unconditionally** (for both `show_splash=True` and `show_splash=False`) so the main window stays hidden during UI construction.
  - Line `2306`: calls `self._build_main_panels()`.
  - Line `2314`: calls `self._update_empty_state_visibility()` **while `self` is still withdrawn**.
  - Lines `2358-2364`: if `show_splash=False` (`splash_owns_reveal == False`), line `2362` calls `self.deiconify()`. If `show_splash=True`, `self` stays withdrawn until `_deferred_restore()` finishes and line `2423` calls `self.deiconify()`.
  - Lines `2367-2425`: `_deferred_restore()` is scheduled via `self.after_idle(_deferred_restore)` and restores `self._saved_opened_files` via `self.open_file(fp)` before closing splash and calling `self.deiconify()`.
- `_build_main_panels()` (`misora.py:5239-6500`):
  - Line `6123`: creates `self.empty_state_frame = self._tag_role(tk.Frame(top_view, bg=t["bg_panel"]), "panel")` (not packed at creation).
  - Lines `6161-6162`: creates `self.gd_scroll_wrap = self._tag_role(tk.Frame(top_view, bg=t["bg_panel"]), "panel")` and **immediately packs it** (`self.gd_scroll_wrap.pack(fill="both", expand=True, padx=4, pady=(0, 4))`).
  - Lines `6204-6254`: inside `text_container` (inside `gd_inner` inside `gd_canvas` inside `gd_scroll_wrap`), packs `self.clean_editor_row` (`fill="both", expand=True`), `self.clean_scroll_x` (`side="bottom", fill="x"`, Q-03), `self.gutter_clean` (`side="left", fill="y"`), and `self.txt_dialogue` (`side="left", fill="both", expand=True`).
  - Line `6447`: creates `self.continuous_wrap = self._tag_role(tk.Frame(top_view, bg=t["bg_panel"]), "panel")` (not packed at creation).
- `_update_empty_state_visibility()` (`misora.py:9763-9786`):
  - Uses `winfo_ismapped()` 8 times (lines `9767, 9769, 9771, 9774, 9778, 9780, 9783, 9785`) to decide whether to call `.pack_forget()` or `.pack(...)` on `gd_scroll_wrap`, `continuous_wrap`, and `empty_state_frame`.
- `_on_toggle_continuous_view()` (`misora.py:8961-8987`): uses unconditional `.pack_forget()` / `.pack(...)`, then calls `self._update_views()` (which calls `_update_empty_state_visibility()` at line `9790`).

### 2.2 Exact mechanism of T-01

In Tk, `widget.winfo_ismapped()` returns `0` (`False`) for **all descendants** whenever the ancestor `Tk` window is withdrawn, even if the child widget is actively `pack`-managed (`winfo_manager() == "pack"`).

1. During `MisoraApp.__init__` (line `2314`, while `super().withdraw()` at line `2036` is active):
   - `self.gd_scroll_wrap` was packed at line `6162`, so `gd_scroll_wrap.winfo_manager() == "pack"`, **but `gd_scroll_wrap.winfo_ismapped() == 0`**.
   - `_update_empty_state_visibility()` runs with `has_docs == False`:
     - Line `9767`: `if self.gd_scroll_wrap.winfo_ismapped():` evaluates `False` -> **`gd_scroll_wrap.pack_forget()` is SKIPPED**.
     - Line `9771`: `if not self.empty_state_frame.winfo_ismapped():` evaluates `True` -> **`empty_state_frame.pack(fill="both", expand=True, ...)` is EXECUTED**.
   - **Result:** Both `gd_scroll_wrap` and `empty_state_frame` are simultaneously packed inside `top_view` in order `['gd_scroll_wrap', 'empty_state_frame']`.
2. On fresh 0-doc startup (`show_splash=False`), line `2362` calls `self.deiconify()`, immediately displaying **both** `gd_scroll_wrap` and `empty_state_frame` stacked vertically.
3. On startup with splash and saved session files (`show_splash=True, restore_session=True`):
   - `self` remains withdrawn throughout `_deferred_restore()` (`misora.py:2367-2425`) until line `2423`.
   - `open_file()` calls `_update_views()` -> `_update_empty_state_visibility()` with `has_docs == True` while `empty_state_frame.winfo_ismapped() == 0`.
   - Line `9774`: `if self.empty_state_frame.winfo_ismapped():` evaluates `False` -> **`empty_state_frame.pack_forget()` is SKIPPED**.
   - Line `2423`: `self.deiconify()` reveals **both** `gd_scroll_wrap` (`906x371+4+74`) above and `empty_state_frame` (`906x108+4+449`, purple Open Files button + hint) directly below it, stealing vertical space from `gd_scroll_wrap` and obscuring the lower border / `clean_scroll_x` (`877x17+0+640` inside `clean_editor_row`).

### 2.3 Verbatim real `MisoraApp` 7-state reproduction output (read-only)

Executed via `py -3.12 -B` against genuine `MisoraApp` instances with `CONFIG_PATH` and `messagebox` patched to a temporary directory (`D:\Misora-Editor` untouched):

```text
[State 1: 0 docs (fresh startup, show_splash=False)] state=normal | top_view.pack_slaves(views)=['gd_scroll_wrap', 'empty_state_frame']
  empty_state_frame       : mgr='pack' mapped=1 geom=906x108+4+449
  gd_scroll_wrap          : mgr='pack' mapped=1 geom=906x371+4+74
  continuous_wrap         : mgr=''     mapped=0 geom=1x1+0+0
  clean_editor_row        : mgr='pack' mapped=1 geom=877x657+0+0
  txt_dialogue            : mgr='pack' mapped=1 geom=844x640+33+0
  clean_scroll_x          : mgr='pack' mapped=1 geom=877x17+0+640

[State 2: 1 doc open (Box 1 Dialogue)] state=normal | top_view.pack_slaves(views)=['gd_scroll_wrap']
  empty_state_frame       : mgr=''     mapped=0 geom=906x108+4+449
  gd_scroll_wrap          : mgr='pack' mapped=1 geom=906x483+4+74
  clean_editor_row        : mgr='pack' mapped=1 geom=877x657+0+0
  txt_dialogue            : mgr='pack' mapped=1 geom=844x640+33+0
  clean_scroll_x          : mgr='pack' mapped=1 geom=877x17+0+640

[State 3: 2 docs open] state=normal | top_view.pack_slaves(views)=['gd_scroll_wrap']
  empty_state_frame       : mgr=''     mapped=0 geom=906x108+4+449
  gd_scroll_wrap          : mgr='pack' mapped=1 geom=906x483+4+74

[State 4 (splash_flag=False) AFTER update() [_deferred_restore done]] state=normal | top_view.pack_slaves(views)=['gd_scroll_wrap']
  empty_state_frame       : mgr=''     mapped=0 geom=906x108+4+449
  gd_scroll_wrap          : mgr='pack' mapped=1 geom=906x483+4+74
  clean_editor_row        : mgr='pack' mapped=1 geom=877x657+0+0
  clean_scroll_x          : mgr='pack' mapped=1 geom=877x17+0+640

[State 4 (splash_flag=True) AFTER update() [_deferred_restore done]] state=normal | top_view.pack_slaves(views)=['gd_scroll_wrap', 'empty_state_frame']
  empty_state_frame       : mgr='pack' mapped=1 geom=906x108+4+449
  gd_scroll_wrap          : mgr='pack' mapped=1 geom=906x371+4+74
  continuous_wrap         : mgr=''     mapped=0 geom=1x1+0+0
  clean_editor_row        : mgr='pack' mapped=1 geom=877x657+0+0
  txt_dialogue            : mgr='pack' mapped=1 geom=844x640+33+0
  clean_scroll_x          : mgr='pack' mapped=1 geom=877x17+0+640

[State 5: close 1 of 2 docs] state=normal | top_view.pack_slaves(views)=['gd_scroll_wrap']
  empty_state_frame       : mgr=''     mapped=0 geom=906x108+4+449
  gd_scroll_wrap          : mgr='pack' mapped=1 geom=906x483+4+74

[State 6: close last doc (0 docs)] state=normal | top_view.pack_slaves(views)=['empty_state_frame']
  empty_state_frame       : mgr='pack' mapped=1 geom=906x483+4+74
  gd_scroll_wrap          : mgr=''     mapped=0 geom=906x483+4+74

[State 7a: All Script ON]      top_view.pack_slaves(views)=['continuous_wrap']     | empty_state_frame mgr='' mapped=0
[State 7b: Back to Dialogue]   top_view.pack_slaves(views)=['gd_scroll_wrap']      | empty_state_frame mgr='' mapped=0 | clean_scroll_x mgr='pack' mapped=1
[State 7c: Box 0 Metadata]     top_view.pack_slaves(views)=['gd_scroll_wrap']      | clean_editor_row mgr='' mapped=0 | panel_box0_metadata mgr='pack' mapped=1
[State 7d: Box 1 Dialogue]     top_view.pack_slaves(views)=['gd_scroll_wrap']      | clean_editor_row mgr='pack' mapped=1 | clean_scroll_x mgr='pack' mapped=1
[State 7e: Dialogue Preview ON] top_view.pack_slaves(views)=['gd_scroll_wrap']     | clean_editor_row mgr='' mapped=0 | dialogue_preview_canvas mgr='pack' mapped=1
[State 7f: Dialogue Preview OFF] top_view.pack_slaves(views)=['gd_scroll_wrap']    | clean_editor_row mgr='pack' mapped=1 | clean_scroll_x mgr='pack' mapped=1
[State 7g: Line Numbers OFF]   top_view.pack_slaves(views)=['gd_scroll_wrap']      | gutter_clean mgr='' mapped=0 | clean_scroll_x mgr='pack' mapped=1
[State 7h: Line Numbers ON]    top_view.pack_slaves(views)=['gd_scroll_wrap']      | gutter_clean mgr='pack' mapped=1 | clean_scroll_x mgr='pack' mapped=1
```

**Conclusion:** T-01 is **CONFIRMED** on `v1.4.15` in both State 1 (`show_splash=False`, fresh 0-doc startup dual-packs `gd_scroll_wrap` + `empty_state_frame`) and State 4 (`show_splash=True`, `_deferred_restore()` with 2 saved files leaves `empty_state_frame` packed and mapped at `906x108+4+449` below `gd_scroll_wrap` `906x371+4+74`).

---

## 3. Smallest Root-Cause Fix Design & `pack`-Only Invariant

### 3.1 `pack`-only geometry manager invariant verification

Read-only search of `misora.py` for `empty_state_frame`, `gd_scroll_wrap`, and `continuous_wrap` returned all 24 references (`6123, 6124, 6161, 6162, 6164, 6169, 6447, 6451, 6462, 8961, 8962, 8984, 8985, 9767-9786`). **None** of these three containers are ever managed by `grid` or `place` anywhere in `misora.py` (only `empty_center` is placed *inside* `empty_state_frame`).

Using explicit `winfo_manager() == "pack"` and `winfo_manager() != "pack"` checks directly verifies `pack` ownership without relying on `winfo_ismapped()`, which is `0` whenever the `Tk` root is withdrawn.

### 3.2 Exact patch in `misora.py` (`_update_empty_state_visibility`, lines 9763–9786)

```diff
--- a/misora.py
+++ b/misora.py
@@ -9764,24 +9764,24 @@
         """Show centered empty-state frame when 0 documents are open; pack only active view when >=1."""
         has_docs = bool(self.open_documents) or bool(self.current_doc) or bool(self.current_file_path)
         if not has_docs:
-            if hasattr(self, "gd_scroll_wrap") and self.gd_scroll_wrap.winfo_ismapped():
+            if hasattr(self, "gd_scroll_wrap") and self.gd_scroll_wrap.winfo_manager() == "pack":
                 self.gd_scroll_wrap.pack_forget()
-            if hasattr(self, "continuous_wrap") and self.continuous_wrap.winfo_ismapped():
+            if hasattr(self, "continuous_wrap") and self.continuous_wrap.winfo_manager() == "pack":
                 self.continuous_wrap.pack_forget()
-            if hasattr(self, "empty_state_frame") and not self.empty_state_frame.winfo_ismapped():
+            if hasattr(self, "empty_state_frame") and self.empty_state_frame.winfo_manager() != "pack":
                 self.empty_state_frame.pack(fill="both", expand=True, padx=4, pady=(0, 4))
         else:
-            if hasattr(self, "empty_state_frame") and self.empty_state_frame.winfo_ismapped():
+            if hasattr(self, "empty_state_frame") and self.empty_state_frame.winfo_manager() == "pack":
                 self.empty_state_frame.pack_forget()
             is_cont = bool(getattr(self, "var_continuous_view", None) and self.var_continuous_view.get())
             if is_cont:
-                if hasattr(self, "gd_scroll_wrap") and self.gd_scroll_wrap.winfo_ismapped():
+                if hasattr(self, "gd_scroll_wrap") and self.gd_scroll_wrap.winfo_manager() == "pack":
                     self.gd_scroll_wrap.pack_forget()
-                if hasattr(self, "continuous_wrap") and not self.continuous_wrap.winfo_ismapped():
+                if hasattr(self, "continuous_wrap") and self.continuous_wrap.winfo_manager() != "pack":
                     self.continuous_wrap.pack(fill="both", expand=True, padx=8, pady=(0, 6))
             else:
-                if hasattr(self, "continuous_wrap") and self.continuous_wrap.winfo_ismapped():
+                if hasattr(self, "continuous_wrap") and self.continuous_wrap.winfo_manager() == "pack":
                     self.continuous_wrap.pack_forget()
-                if hasattr(self, "gd_scroll_wrap") and not self.gd_scroll_wrap.winfo_ismapped():
+                if hasattr(self, "gd_scroll_wrap") and self.gd_scroll_wrap.winfo_manager() != "pack":
                     self.gd_scroll_wrap.pack(fill="both", expand=True, padx=4, pady=(0, 4))
```

### 3.3 Preserved contracts (untouched)

- **S11e Q-03:** `clean_scroll_x` stays packed `side="bottom", fill="x"` inside `clean_editor_row`.
- **S11e Q-05:** `_deferred_restore()`, `MisoraSplashScreen`, and `super().withdraw()` / `self.deiconify()` lifecycle stay untouched.
- **Box 0 / Preview mutual exclusion:** `panel_box0_metadata`, `dialogue_preview_canvas`, and `clean_editor_row` packing in `_update_views()` (`misora.py:9858-9914`) stays untouched.
- **S15 empty-state contract:** `empty_state_frame`, `btn_empty_open`, and `lbl_empty_dnd_hint` construction (`misora.py:6122-6158`) stays untouched.
- **Line-span invariance:** `misora.py` retains the exact same line count (`23912`) and exact same AST declaration line numbers.

---

## 4. Strict File Ownership Matrix & Authorization Boundary

### 4.1 Authorization boundary

- **Under ENV-01 (current pre-Proceed state):** `D:\Misora-Editor` is **100% READ-ONLY**. No source, test, or doc changes are authorized during `/plan`.
- **After Project Lead issues an explicit T-01 Execution Charter (`Proceed`):** Modifying `misora.py` and creating `tests/test_t01_empty_state_overlay.py` are authorized **strictly and solely** under that dedicated T-01 execution charter (never implied as an exception under ENV-01). All existing tests and all other source, config, asset, tool, and archive files remain **READ-ONLY / FORBIDDEN**.

### 4.2 Allowed files (only after T-01 Charter + `Proceed`)

| File | Action | Scope / Constraint |
|---|---|---|
| `misora.py` | **MODIFY** | Only the 8 `winfo_ismapped()` conditions in `_update_empty_state_visibility()` (`9767–9785`). |
| `tests/test_t01_empty_state_overlay.py` | **CREATE (NEW)** | Exactly **11** `test_*` methods (**4** failing-first Defect Probes + **7** Regression Guards) using stdlib `unittest`. |
| `docs/project/OPEN_ISSUES.md` | **MODIFY** | Update T-01: Evidence `CONFIRMED`; automated fix & TDD verification `PASS`; Windows manual QA `M-1..M-12` `MANUAL-PENDING`; full closure deferred until manual QA passes; keep Lifecycle `ACTIVE`. Do **NOT** claim `CONFIRMED + FIXED` / closed before manual QA. |
| `PROJECT_STATE.md` | **MODIFY** | Record T-01 automated test count (`475 + 11 = 486`) and note `MANUAL-PENDING` QA; keep file size ≤ 15 KiB (15,360 bytes). |
| `docs/architecture/MISORA_SYMBOL_INDEX.md` | **DEFERRED TO POST-COMMIT** | **Do NOT run `--write` while `misora.py` has uncommitted edits.** `tools/generate_symbol_index.py:48-69` (`check_clean_indexed_sources`) intentionally rejects uncommitted `.py` changes, and even identical line spans change `misora.py`'s SHA-256 fingerprint. Project Lead / maintainer regenerates and `--check`s after committing T-01. |

### 4.3 Strictly FORBIDDEN / READ-ONLY

`__init__.py`, `core/**`, `assets/**`, all existing `tests/*.py` files, `AGENTS.md`, `docs/archive/**`, `tools/generate_symbol_index.py`, `misora.bat`, `requirements.txt`, `misora_config.json`, `backups/**`, `README.md`.

---

## 5. Strict TDD & `unittest` Verification Plan

All test runs use Python 3.12 stdlib `unittest` (**no `pytest`**). Discovery (`countTestCases()`) and execution are reported separately.

### 5.1 Pre-patch baseline & failing-first verification

1. **Compile check:**
   `py -3.12 -B -m compileall -q misora.py __init__.py` -> exit `0`
2. **Pre-addition discovery baseline:**
   `py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"` -> `countTestCases: 475`
3. **Create `tests/test_t01_empty_state_overlay.py`** (`11` `test_*` methods = `4` Probes + `7` Guards).
4. **Post-addition discovery math check:**
   `py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"` -> **`countTestCases: 486`** (`475 + 11 = 486`; any other count is a STOP condition).
5. **Pre-patch Defect Probes (MUST FAIL — 4 failures):**
   `py -3.12 -B -m unittest tests.test_t01_empty_state_overlay.TestT01DefectProbes -v` -> all 4 probes **FAIL** (and `Ran 4 tests`).
6. **Pre-patch Regression Guards (MUST PASS — 7 passes):**
   `py -3.12 -B -m unittest tests.test_t01_empty_state_overlay.TestT01RegressionGuards -v` -> all 7 guards **PASS** (`Ran 7 tests ... OK`).

### 5.2 Apply patch

Apply the 8-line substitution in `_update_empty_state_visibility()` (`misora.py:9767-9785`).

### 5.3 Post-patch verification & sequencing

1. **Compile check (including root `__init__.py`):**
   `py -3.12 -B -m compileall -q misora.py __init__.py` -> exit `0`
2. **Full T-01 suite (MUST PASS all 11):**
   `py -3.12 -B -m unittest tests.test_t01_empty_state_overlay -v` -> `Ran 11 tests ... OK` (4 probes PASS + 7 guards PASS)
3. **Targeted UI regression suites (exact verified module names on disk):**
   `py -3.12 -B -m unittest tests.test_p3_s15_selection_drawer_open tests.test_v15_s11e_polish_splash_menu_tooltips tests.test_p3_s04_ast_mutations tests.test_v15_s04_layout_drawer_controls tests.test_t01_empty_state_overlay -v`
4. **Post-patch discovery check (exact arithmetic):**
   `py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"` -> **`countTestCases: 486`** (`475 + 11 = 486`).
5. **Line-count & symbol-span invariance check (while uncommitted):**
   Verify `misora.py` line count remains `23912` and `_update_empty_state_visibility` remains at lines `9763–9786`; verify `git diff -- misora.py` touches only 8 lines.
   *(Do **NOT** run `generate_symbol_index.py` on dirty `misora.py`; Project Lead regenerates `docs/architecture/MISORA_SYMBOL_INDEX.md` and runs `--check` after committing T-01.)*
6. **Version-source parity & diff/status check:**
   Verify `__init__.__version__ == "1.4.15"`, `PROJECT_STATE.md` byte size `<= 15360`, and `git status --short --untracked-files=all` contains only the authorized T-01 files.

### 5.4 Exact 7-State Coverage & Probe/Guard Matrix (`tests/test_t01_empty_state_overlay.py`, 11 methods)

All 4 Defect Probes instantiate genuine `MisoraApp` instances (patching `CONFIG_PATH` and `messagebox` to a temp dir so `D:\Misora-Editor` config/backups are untouched).

#### Defect Probes (`TestT01DefectProbes` — 4 tests: FAIL pre-patch, PASS post-patch)

| Method | Matrix State | Scenario & Assertions | Pre-patch | Post-patch |
|---|---|---|---:|---:|
| `test_probe_1_state1_fresh_startup_zero_docs_exclusive` | **State 1** | Fresh `MisoraApp(restore_session=False, show_splash=False)` -> `update()`: asserts `empty_state_frame.winfo_manager() == "pack"`, `empty_state_frame.winfo_ismapped() == 1`, `gd_scroll_wrap.winfo_manager() == ""`, `continuous_wrap.winfo_manager() == ""`. | **FAIL** (`gd_scroll_wrap` still packed) | **PASS** |
| `test_probe_2_state4_deferred_restore_with_splash_hides_empty_state` | **State 4 (`show_splash=True`)** | `MisoraApp(restore_session=True, show_splash=True)` with **2 saved files** -> `update()` completes `_deferred_restore()` & `deiconify()`: asserts `empty_state_frame.winfo_manager() == ""`, `empty_state_frame.winfo_ismapped() == 0`, `gd_scroll_wrap.winfo_manager() == "pack"`, `clean_editor_row.winfo_manager() == "pack"`, `clean_scroll_x.winfo_manager() == "pack"`. | **FAIL** (`empty_state_frame` stays packed below `gd_scroll_wrap`) | **PASS** |
| `test_probe_3_withdrawn_open_file_and_deiconify_exclusivity` | **State 2 / 3 (withdrawn)** | `MisoraApp(restore_session=False, show_splash=False)` -> `withdraw()` -> `open_file(f1)` + `open_file(f2)` while withdrawn -> `deiconify()` + `update()`: asserts `empty_state_frame.winfo_manager() == ""`, `empty_state_frame.winfo_ismapped() == 0`, `gd_scroll_wrap.winfo_manager() == "pack"`. | **FAIL** (`empty_state_frame` never unpacked) | **PASS** |
| `test_probe_4_q05_splash_lifecycle_withdrawn_transitions` | **State 4 (Q-05)** | `MisoraApp(restore_session=True, show_splash=True)` with 2 saved files -> asserts `state() == "withdrawn"` and splash alive before `update()`, splash closes and `state() == "normal"` after `update()`, and at no point are `empty_state_frame` and `gd_scroll_wrap` simultaneously pack-managed; `clean_scroll_x.winfo_ismapped() == 1`. | **FAIL** (dual-packed during/after splash restore) | **PASS** |

#### Regression Guards (`TestT01RegressionGuards` — 7 tests: PASS pre-patch, PASS post-patch)

| Method | Matrix State | Scenario & Assertions | Pre-patch | Post-patch |
|---|---|---|---:|---:|
| `test_guard_1_state2_open_one_doc_box1_dialogue` | **State 2** | Mapped `MisoraApp`, open 1 Box-1 doc -> `empty_state_frame.winfo_manager() == ""`, `gd_scroll_wrap.winfo_manager() == "pack"`, `clean_editor_row`/`txt_dialogue`/`clean_scroll_x` all packed & mapped (`winfo_height() > 1`). | **PASS** | **PASS** |
| `test_guard_2_state3_two_docs_open_hides_empty_state` | **State 3** | Mapped `MisoraApp`, open 2 docs -> `len(open_documents) == 2`, `empty_state_frame.winfo_manager() == ""`, `empty_state_frame.winfo_ismapped() == 0`, `gd_scroll_wrap.winfo_manager() == "pack"`. | **PASS** | **PASS** |
| `test_guard_3_state4_deferred_restore_no_splash_two_files` | **State 4 (`show_splash=False`)** | `MisoraApp(restore_session=True, show_splash=False)` with 2 saved session files -> `update()`: asserts 2 open docs restored, `empty_state_frame.winfo_manager() == ""`, `gd_scroll_wrap.winfo_manager() == "pack"`, `clean_scroll_x.winfo_ismapped() == 1`. | **PASS** | **PASS** |
| `test_guard_4_state5_close_one_of_two_docs_stays_hidden` | **State 5** | With 2 docs open, `close_file(f2)` -> `len(open_documents) == 1`, `empty_state_frame.winfo_manager() == ""`, `gd_scroll_wrap.winfo_manager() == "pack"`, `clean_scroll_x.winfo_ismapped() == 1`. | **PASS** | **PASS** |
| `test_guard_5_state6_close_last_doc_restores_empty_state` | **State 6** | Close last doc (`close_file(f1)`) -> `empty_state_frame.winfo_manager() == "pack"`, `empty_state_frame.winfo_ismapped() == 1`, `gd_scroll_wrap.winfo_manager() == ""`, `continuous_wrap.winfo_manager() == ""`. | **PASS** | **PASS** |
| `test_guard_6_state7_view_toggles_and_mutual_exclusion` | **State 7** | With 1 doc open, exercise Dialogue <-> All Script, Box 0 <-> Box 1, Dialogue Preview ON/OFF, Line Numbers ON/OFF -> mutual exclusion holds at every step, `empty_state_frame.winfo_manager() == ""` throughout, `clean_scroll_x` restored & mapped in Box 1 Dialogue. | **PASS** | **PASS** |
| `test_guard_7_q03_pack_only_and_s15_empty_state_widgets` | **Invariants** | Asserts `clean_scroll_x.master is clean_editor_row`, `clean_scroll_x.winfo_manager() == "pack"`, `btn_empty_open`/`lbl_empty_dnd_hint` children of `empty_state_frame`, and `empty_state_frame`/`gd_scroll_wrap`/`continuous_wrap` never use `grid` or `place`. | **PASS** | **PASS** |

---

## 6. Rollback & Manual Windows QA Checklist

### 6.1 Rollback

1. Restore the 8 `winfo_ismapped()` conditions in `_update_empty_state_visibility()` (`misora.py:9767-9785`).
2. Delete `tests/test_t01_empty_state_overlay.py`.
3. Revert `docs/project/OPEN_ISSUES.md` and `PROJECT_STATE.md`.
4. Confirm `git status --short --untracked-files=all` is clean (or back to pre-session state).

### 6.2 Manual Windows QA Checklist (`MANUAL-PENDING` — required before closing T-01)

| # | Case | Steps | Expected | Status |
|---|---|---|---|---|
| M-1 | Fresh start, 0 docs | Launch Misora with no saved session | Purple "Open Files" button centered; `txt_dialogue` NOT visible | `MANUAL-PENDING` |
| M-2 | Open 1 bundle | Open any `.unity3d` file (Box 1 Dialogue) | Empty-state gone; dialogue editor + `clean_scroll_x` unobstructed | `MANUAL-PENDING` |
| M-3 | Open 2 bundles | Open a second `.unity3d` file | Empty-state gone; switch between both files cleanly | `MANUAL-PENDING` |
| M-4 | Session restore (splash ON) | Close with 2 open bundles; relaunch with splash enabled | Splash closes -> 2 files restored -> NO purple overlay below editor | `MANUAL-PENDING` |
| M-5 | Session restore (splash OFF) | Same as M-4 with splash disabled | 2 files restored -> NO purple overlay | `MANUAL-PENDING` |
| M-6 | Close 1 of 2 docs | Close one of the 2 open bundles | Remaining file visible; no empty-state overlay | `MANUAL-PENDING` |
| M-7 | Close last doc | Close remaining bundle | Purple "Open Files" empty-state reappears cleanly | `MANUAL-PENDING` |
| M-8 | Dialogue <-> All Script | Toggle Continuous/All Script ON & OFF | Mutual exclusion holds; no leftover overlay; `clean_scroll_x` intact | `MANUAL-PENDING` |
| M-9 | Box 0 <-> Box 1 | Navigate Box 0 <-> Box 1 | Metadata panel vs `clean_editor_row` switches cleanly; no overlay | `MANUAL-PENDING` |
| M-10 | Dialogue Preview ON/OFF | Toggle Compiled Preview ON & OFF | Preview vs `clean_editor_row` + `clean_scroll_x` switches cleanly | `MANUAL-PENDING` |
| M-11 | Line Numbers ON/OFF | Toggle Show Line Numbers ON & OFF | Gutter toggles without pack error or overlay bleed | `MANUAL-PENDING` |
| M-12 | Windows DPI (125%) | Verify at 125% scaling on Windows | No clipped `clean_scroll_x` or stray overlay | `MANUAL-PENDING` |

Record exact version (`1.4.15`), OS/DPI, steps, expected vs actual, and operator confirmation in `docs/project/OPEN_ISSUES.md` before changing T-01 Lifecycle from `ACTIVE` to closed/resolved.

---

**STOP — WAITING FOR INDEPENDENT REVIEW**
