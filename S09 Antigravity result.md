Ran find navigation and pin speaker methods
Analyzed misora.py:L18460-18490
Analyzed misora.py:L10035-10100
Analyzed misora.py:L6480-6550
Analyzed misora.py:L11560-11615
Ran find document switch sites
Analyzed misora.py:L8810-8860
Analyzed misora.py:L6650-6710
Created test_v15_s09_core_fixes_54d.py
Ran run pre-patch S09 probes · Exited with code 1

Running the pre-patch `tests.test_v15_s09_core_fixes_54d` suite to verify that all 7 probes fail and both regression guards pass before applying any edits.

Edited test_v15_s09_core_fixes_54d.py
Ran verify probe 3 fails pre-patch · Exited with code 1

Verifying `test_probe_3` fails pre-patch with the new withdraw-before-position and multi-monitor clamping assertions.

Analyzed misora.py:L345-375
Analyzed misora.py:L1660-1735
Analyzed misora.py:L4385-4405
Analyzed misora.py:L5115-5138
Analyzed misora.py:L8340-8360
Analyzed misora.py:L8602-8618
Analyzed misora.py:L14315-14405
Edited misora.py
Edited __init__.py
Edited misora.py
Analyzed test_p3_s17_pixel_rulers.py:L85-159
Analyzed test_v15_s02_fonts_ruler_metrics.py:L140-230
Analyzed test_v15_s06_tools_word_wrap.py:L355-417
Edited test_p3_s17_pixel_rulers.py
Edited test_v15_s02_fonts_ruler_metrics.py
Edited test_v15_s02_fonts_ruler_metrics.py
Edited test_v15_s05_speaker_console_about.py
Edited test_v15_s06_tools_word_wrap.py
Edited test_v15_s06_tools_word_wrap.py
Ran compileall and S09 affected tests · Exited with code 1
Analyzed misora.py:L13980-14005
Edited misora.py
Ran compileall and S09 affected tests · Exited with code 1
Analyzed misora.py:L14045-14065
Edited misora.py
Ran compileall and S09 affected tests · Exited with code 1

`compileall` passed; waiting for `tests.test_v15_s09_core_fixes_54d` and the 4 affected suites to finish.

Analyzed misora.py:L10025-10065
Ran find is_box0_active resets
Analyzed misora.py:L11580-11618
Ran check has_metadata in story_ast.py
Analyzed story_ast.py:L390-415
Ran check insert_box and has_metadata behavior
Edited test_v15_s09_core_fixes_54d.py
Edited test_v15_s09_core_fixes_54d.py
Edited test_v15_s09_core_fixes_54d.py
Ran run S09 test suite

Re-running `tests.test_v15_s09_core_fixes_54d` after fixing the test fixture metadata command ID and autocomplete spy setup.

Ran run S09 suites and full discovery · Exited with code 1

Running `compileall`, the 5 S09/affected test suites, and full `unittest discover -s tests -v`. This may take a few minutes; waiting for completion.

Checked task Run S09 suites and full discovery

`task-202` is actively progressing (`test_s3_document_close`); continuing to wait for full discovery completion.

Ran summarize targeted and discover results
Analyzed CHANGELOG.md:L1-20
Analyzed PROJECT_STATE.md:L1-60
Edited CHANGELOG.md
Edited PROJECT_STATE.md
Edited PROJECT_STATE.md
Ran check git status

Everything for **S09 (`v1.4.8`)** is implemented, verified, and documented within the allowed file boundaries.

---

### Changed Files
- [__init__.py](file:///D:/Misora-Editor/__init__.py) — bumped `__version__` from `"1.4.7"` to `"1.4.8"`.
- [misora.py](file:///D:/Misora-Editor/misora.py) — implemented:
  - **`U-01` Paste Box Selection Model** (`_show_box_paste_mode_dialog`, `on_box_paste`): strict `sorted(self._selected_boxes)` targeting, disabled `Replace` with inline hint when empty, atomic abort on Box 0 (`-1`) / out-of-range / count mismatch / locked targets, and Insert before index `0` when Box 0 is active.
  - **`U-02` Pin Speaker Captured Identity & Boundaries** (`_on_toggle_pin_speaker`, `_reset_speaker_pin`, `_navigate_pinned_speaker`, `on_prev_box`, `on_next_box`, `on_box_new`): captures canonical `doc.boxes[current_box_idx].speaker` into `_pinned_speaker_name`, navigates within `0..len(doc.boxes)-1` without wrap-around (`Next` from Box 0 starts at index `0`), preserves `_pinned_speaker_name` on speaker rename, prefills `on_box_new()`, and resets on unpin / `open_file()` / `close_file()` / `_close_all_documents_without_prompt()`.
  - **`U-06` Speaker Autocomplete Lifecycle & Multi-Monitor Clamping** (`_open_speaker_autocomplete`, `_get_monitor_work_area`, `_refresh_speaker_autocomplete`): creates `overrideredirect(True)` `tk.Toplevel` withdrawn, clamps to Win32 `MonitorFromPoint` + `GetMonitorInfoW` `rcWork` (supporting negative secondary-monitor coordinates), and sets `geometry()` before `deiconify()`/`lift()`.
  - **`U-07` & `U-18` Shared 54d Reference & Box 0 Exemption** (`DIALOGUE_MAX_DIGITS = 54`, `DIALOGUE_MAX_LINES = 3`, `_get_54d_reference_safe_w`): unified Nunito Bold `54d` pixel boundary across `_measure_dialogue_metrics()`, `_get_word_wrap_params()`, `_draw_single_pixel_ruler()`, `_update_char_overflow_indicator()`, `_render_dialogue_preview_frame()`, and `ImportFromXUATDialog`; Box 0 (`is_box0_active`) is immune to `_apply_overflow_highlights()`, `_apply_gutter_overflow_tag()`, red header warnings, and Auto Word Wrap.
  - **`U-19` Dialogue Preview Pink Arrow & Border Fix** (`_render_dialogue_preview_frame`): added `arrow_safe_zone = 28` and constrained embedded `txt_dialogue_preview` (`win_w`, `max_inner_h`) strictly inside the inner content safe zone (`preview_arrow` and `preview_capsule` non-overlapping).
  - **`RM-01` Complete Console Toggle Removal**: removed `Debug > Show / Hide Windows Console`, `var_console_visible`, `_console_visible`, `_toggle_windows_console()`, `_toggle_console_visibility()`, `_toggle_console_shortcut()`, `F12` bindings/routing, and `console_visible` saving while tolerating legacy `console_visible` in config on load.
  - **`U-16` MTL Apply Button Placement**: moved `btn_apply` (`←`) to the left of `lbl_engine` on all Dialogue MTL cards.
- [tests/test_v15_s09_core_fixes_54d.py](file:///D:/Misora-Editor/tests/test_v15_s09_core_fixes_54d.py) — new S09 suite (7 failing-first probes + 2 regression guards).
- [tests/test_p3_s17_pixel_rulers.py](file:///D:/Misora-Editor/tests/test_p3_s17_pixel_rulers.py), [tests/test_v15_s02_fonts_ruler_metrics.py](file:///D:/Misora-Editor/tests/test_v15_s02_fonts_ruler_metrics.py), [tests/test_v15_s05_speaker_console_about.py](file:///D:/Misora-Editor/tests/test_v15_s05_speaker_console_about.py), [tests/test_v15_s06_tools_word_wrap.py](file:///D:/Misora-Editor/tests/test_v15_s06_tools_word_wrap.py) — updated `50d` → `54d` assertions and replaced the retired console toggle probe with a negative `F12` unbound guard.
- [CHANGELOG.md](file:///D:/Misora-Editor/CHANGELOG.md) & [PROJECT_STATE.md](file:///D:/Misora-Editor/PROJECT_STATE.md) — updated with S09 (`v1.4.8`) details and exact verification baseline.

---

### Verification Output
- **Pre-patch S09 probes (`py -3.12 -m unittest tests.test_v15_s09_core_fixes_54d -v`):**
  - All 7 probes failed pre-patch (6 failures + 1 error after tightening Probe 3), and both regression guards passed (`2/2`).
- **Compile check (`py -3.12 -m compileall -q __init__.py misora.py core assets tests`):**
  - **PASS** (exit code `0`).
- **Targeted S09 + affected suites (`py -3.12 -m unittest tests.test_v15_s09_core_fixes_54d tests.test_p3_s17_pixel_rulers tests.test_v15_s02_fonts_ruler_metrics tests.test_v15_s05_speaker_console_about tests.test_v15_s06_tools_word_wrap -v`):**
  - **PASS:** `Ran 34 tests in 55.068s — OK` (`34 pass, 0 failures, 0 errors`).
- **Full discovery (`py -3.12 -m unittest discover -s tests -v`):**
  - `Ran 422 tests in 514.771s — FAILED (failures=10, errors=2, skipped=35)` (`375 pass`):
    - **3 failures + 2 errors** in `test_s8b2_memory_guards` (plus 35 skips across `test_misora_core` / `test_misora_ui_integration`): **fixture-blocked** by missing `storydata_1001005.unity3d`.
    - **3 pre-existing non-fixture hygiene failures** (deferred to S12): `test_phase3_performance_config::test_05` (local `misora_config.json`), `test_s9c_workspace_safety::test_04` (deleted `misora_config.default.json`), `test_v15_s01_stability_remediation::test_probe_8` (pinned `"1.4.1"`).
    - **4 failures in tests outside S09 Allowed Files** reflecting intentional S09 contract changes (deferred to S12): `test_p3_s18_game_preview::test_01` & `test_03` (`50d→54d` & `U-19` inner bounds), `test_v15_s03_all_script_preview_paste::test_probe_4` (`U-01` strict `_selected_boxes` Replace contract), `test_v15_s08_release_gate_stress::test_stress_5` (pinned `"1.4.7"` Release Gate Hold).
- **`git status --short`:** Only the 9 allowed files above (`M` / `??`), zero untracked/forbidden modifications.

---

### Manual Windows QA Items (Project Lead)
1. **Paste Box (`U-01`):** Test empty selection (`Replace` disabled), mismatched selection count, Box 0 (`-1`) rejection, locked box atomic abort, non-contiguous multi-box `Replace` + Undo/Redo, and `Insert` with Box 0 active (inserts before Box #1) in both Dialogue and All Script views.
2. **Pin Speaker (`U-02`):** Pin a speaker, rename the current box's speaker, and verify `Next`/`Prev` still steps to the original pinned speaker without wrapping around at chapter boundaries.
3. **Speaker Autocomplete (`U-06`):** Click Speaker entry on first launch and on a secondary monitor (negative coordinates) to verify zero `(0, 0)` flash and clean work-area alignment.
4. **54d Reference & Box 0 Exemption (`U-07`, `U-18`):** Verify `54d` ruler, `N/54d · M/3L` header, `Global — Nunito Bold` vs `Japanese` constant ruler width, and Box 0 immunity to red markers/wrap.
5. **Dialogue Preview (`U-19`):** Toggle Preview on a long/3-line box at 100%/125%/150% DPI and verify the pink `▼` and right gold border are crisp and unclipped.
6. **MTL Apply & Console Removal (`U-16`, `RM-01`):** Verify `[←]` sits left of each engine name on Dialogue MTL cards, `Debug > Show / Hide Windows Console` and `F12` are gone, and an existing `misora_config.json` containing `"console_visible": true` loads cleanly.
