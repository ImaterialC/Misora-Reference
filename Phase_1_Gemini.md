# MISORA-EDITOR — PHASE 1 INDEPENDENT RESEARCH DOSSIER

Reviewer: Gemini
Date: 2026-11-23
Inspected Baseline: Misora-Editor v1.4.0 (root `__init__.py` = "1.4.0", commit `8e40994`) — full production codebase read (`misora.py`, all 12 `core/*.py`, `assets/icon.py`, `assets/splash.py`, `AGENTS.md`, `PROJECT_STATE.md`, `misora_config.default.json`, `README.md`). Note: `tests/*.py`, `misora.bat`, and `docs/*.md` were not uploaded in this session; no claims are made about uninspected test internals.
Reference Files Inspected: `asset_registry.py`, `priconne_tool.py`, `advscript.py`, `advverify.py`, `NewDataMiner/{config,models,manifest_manager,database,db_updater,downloader,extractor,resource_cross_ref,dataminer,cli}.py`.

======================================================================
1. BUGS & DEFECTS (EVIDENCE-BASED)
======================================================================

- [GEM-B01] Multi-Box Triple-Enter Paste Immediately Resets Dirty Flag to False (S2 Regression) | Severity: P0 | Status: [CONFIRMED]
  * Location: `misora.py` -> `MisoraApp._on_card_paste_caret()` & `_dirty_state_changed()`
  * Problem: `_on_card_paste_caret()` mutates multiple boxes on `\n\n\n` paste, sets `self.is_dirty = True` directly WITHOUT calling `self._mark_document_dirty(self.current_file_path)`, and then calls `self._dirty_state_changed()`. Because S2 changed `_dirty_state_changed()` to mirror `self.is_dirty` strictly from `self.open_documents[p]["dirty"]`, `self.is_dirty` is immediately overwritten back to `False`!
  * Impact: Silent data loss — multi-box pasted edits appear clean, window title lacks `*`, and closing/exiting discards all pasted edits without prompting.
  * Proposed Fix Direction: Call `self._mark_document_dirty(self.current_file_path)` (and check locked boxes!) before `self._dirty_state_changed()`.

- [GEM-B02] Wrong `open_documents` Cache Keys, Memory Leak, Unsaved-Edit Clobber & Lock Bypass in Multi-File Replace-All / BulkFileDelta Undo (S9b Regressions) | Severity: P0 | Status: [CONFIRMED]
  * Location: `misora.py` -> `MisoraApp.on_replace_all()` (multi-file branch) & `MisoraApp._apply_delta()` (`BulkFileDelta` branch)
  * Problem:
    1. `_apply_delta(BulkFileDelta)` and its rollback block read/write `self.open_documents[fp]["bundle_env"]` and `["target_object"]`, whereas `open_file()` stores `"env"` and `"obj"`. `old_env` is always `None` (leaking UnityPy environments), and the active cache retains stale `env`/`obj` references!
    2. Multi-file `on_replace_all()` reads bundles/text directly from disk, silently discarding unsaved in-memory edits in open dirty documents; for inactive open bundles it never updates `open_documents[f_res]["doc"]`/`"env"`/`"obj"`; for both bundles and text it calls `_mark_document_dirty(f_res)` AFTER already saving to disk (leaving saved files falsely dirty); and `self.current_file_path in matching_files` compares a resolved path against un-resolved `rglob` paths (can miss reloading the active file).
    3. Multi-file bundle Replace-All never checks Translation Locks (`self.is_box_locked`), never deduplicates overlapping `target_roots`, and both `on_replace_next()` and `on_replace_all()` use literal `find_text in ...` / `.replace()`, ignoring `Match Case`, `Regex`, and `Ignore Whitespace` options.
  * Impact: Corrupted bundle repacks from stale `env`/`obj`, leaked RAM, overwritten unsaved edits, bypassed locks, and broken Replace UX.
  * Proposed Fix Direction: Fix cache keys to `"env"`/`"obj"` consistently; resolve & deduplicate candidate paths; guard or flush/prompt dirty open docs before disk replacement; honor Translation Lock and search options; do not falsely mark disk-saved files dirty.

- [GEM-B03] Plain-Text `on_save()` Reads Stripped Compiled Preview Widget (F-GPT-04 Still Alive) | Severity: P0 | Status: [CONFIRMED]
  * Location: `misora.py` -> `MisoraApp.on_save()` (non-bundle, `not self.current_doc` branch)
  * Problem: When `var_preview_compiled` is ON for a plain-text file, `_update_views()` populates `txt_dialogue`/`txt_continuous` via `_insert_compiled_ngui_text()` (stripping all NGUI markup). `on_save()` reads `txt_dialogue.get("1.0", "end-1c")` instead of `self._plain_text_content`, writing stripped preview text to disk and overwriting `_plain_text_content` and cache.
  * Impact: Permanent loss of all NGUI formatting tags in `.txt` files saved while Preview is enabled.
  * Proposed Fix Direction: When `self.var_preview_compiled.get()` is True, save `self._plain_text_content` directly (never read from the compiled presentation widget).

- [GEM-B04] `ScriptPastePreviewDialog` Ignores Unchecked Metadata Checkbox & Corrupts Sparse CSIF Undo/Preview | Severity: P0 | Status: [CONFIRMED]
  * Location: `misora.py` -> `MisoraApp._show_paste_preview_and_apply()`, `ScriptPastePreviewDialog._populate_tree()`, and `core/script_codec.py` -> `apply_to_document()`
  * Problem:
    1. When the user unchecks "Apply metadata (title / subtitle / summary) to Box 0" (`apply_meta = False`), `_show_paste_preview_and_apply()` skips recording `MetadataDelta` but STILL passes `result` (with non-empty `result.metadata`) to `apply_to_document()`, which unconditionally executes `doc.set_metadata(...)` — silently mutating Box 0 against user choice with NO undo entry!
    2. For sparse CSIF (`result.is_sparse == True`), `_show_paste_preview_and_apply()` records `BoxEditDelta` at sequential `start_idx + k` instead of each block's actual `blk.index - 1`, while `apply_to_document()` mutates `blk.index - 1`. Undo then overwrites completely wrong boxes! `ScriptPastePreviewDialog._populate_tree()` also previews wrong sequential target boxes (`start_idx + k`).
  * Impact: Silent un-undoable Box 0 corruption and wrong-box Undo corruption on sparse CSIF paste/import.
  * Proposed Fix Direction: Pass `apply_metadata=apply_meta` to `apply_to_document()`; map both preview rows and `BoxEditDelta` recording to `blk.index - 1` when `result.is_sparse` is True (and validate bounds before starting undo batch).

- [GEM-B05] Document Switch Wipes All Translation Locks, Modified Boxes, Caret Position & Original JP XUAT Keys (Rule 16 Broken) | Severity: P0 | Status: [CONFIRMED]
  * Location: `misora.py` -> `MisoraApp.open_file()`
  * Problem: On EVERY `open_file()` call (including cache-hit tab switches!), `open_file()` unconditionally runs `self._locked_boxes.clear()`, `self._modified_boxes.clear()`, resets `self.current_box_idx = 0`, and rebuilds `self._original_box_texts` from the CURRENT (already-edited English) `doc.boxes`. Furthermore, `close_file()` and `_on_app_exit()` call `open_file(p)` before `on_save()`, wiping `p`'s modified boxes and JP keys right before saving!
  * Impact: Switching tabs silently unlocks all locked boxes and breaks XUAT synchronization.
  * Proposed Fix Direction: Persist `locked_box_uids`, `modified_box_uids`, immutable `original_jp_by_uid`, and `current_box_idx`/`is_box0_active` inside each `open_documents[path]` entry (keyed by stable `box.uid`), and save inactive dirty entries via a dedicated `_save_document_entry()` helper without switching active UI state.

- [GEM-B06] Silent LF -> CRLF Corruption on Windows in `write_atomic_encoded()` (S8b-3 Bug) | Severity: P1 | Status: [CONFIRMED]
  * Location: `core/text_encoding.py` -> `write_atomic_encoded()`
  * Problem: After computing exact `data = encode_with_metadata(...)`, `write_atomic_encoded()` checks `if not has_bom and newline in (None, "\n"): tmp_file.write_text(content, encoding=encoding)`. On Windows, `Path.write_text()` without `newline=""` translates every `\n` into `\r\n`, silently converting LF-only files into CRLF and contradicting Rule 10 / S8b-3. `on_export_script()` in `misora.py` has the same non-atomic `write_text` CRLF issue.
  * Impact: Unintended CRLF churn on every saved LF-only `.txt` / v2 / CSIF export file on Windows.
  * Proposed Fix Direction: Always write the encoded bytes via `tmp_file.write_bytes(data)` inside `write_atomic_encoded()`, and use `write_atomic_encoded(..., newline="\n")` in `on_export_script()`.

- [GEM-B07] Continuous View NGUI Ribbon Dead (`B3`) + Page View Ribbon Title-Dirty Regression + Size Button Never Commits | Severity: P1 | Status: [CONFIRMED]
  * Location: `misora.py` -> `_insert_text_wrapper()`, `apply_ngui_wrapper()`, `on_insert_ruby()`, `on_insert_font_size()`
  * Problem:
    1. `_insert_text_wrapper()` and `on_insert_ruby()` still target the hidden `self.txt_continuous` when `var_continuous_view` is True, so Bold/Italic/Underline/Strike/Sub/Sup/Color/Gradient/`[-]`/`{playername}`/Ruby/Glossary buttons do nothing on `.unity3d`/v2 Continuous cards.
    2. `on_insert_font_size()` modifies the widget text but NEVER calls `_commit_widget_edit(target)` (contrary to `PROJECT_STATE.md` claiming `SIZE-RIBBON-NO-COMMIT` is resolved).
    3. In Page View, `_insert_text_wrapper()` calls `_on_dialogue_edited()` (which injects into `current_doc` and marks dirty), and then `apply_ngui_wrapper()` calls `_commit_widget_edit(target)` which calls `_on_dialogue_edited()` a SECOND time -> `old_tx == new_tx` -> returns `False` -> `_dirty_state_changed()` is SKIPPED! Window title `*`, dock `*`, and Undo menu remain stale after ribbon wraps.
  * Impact: Broken formatting workflow in Continuous View, lost font-size edits on navigation, and stale dirty/Undo UI in Page View.
  * Proposed Fix Direction: Resolve active card via `_get_card_text_widget(self.current_box_idx)` in `_insert_text_wrapper()` and `on_insert_ruby()`, remove the redundant `_on_dialogue_edited()` call inside `_insert_text_wrapper()` so `apply_ngui_wrapper()`'s `_commit_widget_edit()` performs the single commit + single `_dirty_state_changed()`, and call `_commit_widget_edit(target)` in `on_insert_font_size()`.

- [GEM-B08] Non-Contiguous `on_box_cut()` Scrambles Story Order on Undo/Redo & Bypasses Locks | Severity: P0 | Status: [CONFIRMED]
  * Location: `misora.py` -> `on_box_cut()`, `_apply_delta()` (`BoxStructuralDelta`)
  * Problem: `on_box_cut()` records only `box_index = targets[0]` for a non-contiguous selection (e.g., `[1, 4]`). Undo re-inserts all snapshots consecutively at indices `1, 2` instead of `1, 4`, scrambling dialogue order; Redo then deletes the wrong boxes (`1, 2`). Also ignores `self.is_box_locked()`.
  * Impact: Silent story ordering corruption on Undo/Redo and deletion of locked boxes.
  * Proposed Fix Direction: Store per-snapshot original indices in `BoxStructuralDelta` (restore in ascending original index order on Undo, delete exact indices on Redo) and skip/warn on locked boxes.

- [GEM-B09] Internal `on_box_paste()` Flattens `BoxSnapshot` (Loses Multi-Segment Structure, Voice Cues & Extra Args) | Severity: P1 | Status: [CONFIRMED]
  * Location: `misora.py` -> `on_box_paste()`
  * Problem: Internal `_box_clipboard` holds rich `BoxSnapshot` instances (`seg_texts`, `voice_cue`, `extra_args`), but `on_box_paste()` converts them to flattened `DialogueBlock` and rebuilds single-segment `BoxSnapshot` objects with `voice_cue=""` and `extra_args=None`.
  * Impact: Loss of multi-segment alignment, voice cues, and unmanaged command arguments on internal Copy/Cut/Paste Box.
  * Proposed Fix Direction: Insert deep-copied internal `BoxSnapshot` objects directly when `_box_clipboard` matches system clipboard; use `DialogueBlock` conversion only for external clipboard payloads.

- [GEM-B10] `on_clear_dialogue_skeleton()` and `TranslatorAssistantDialog._on_apply()` Bypass Translation Lock (and Strip Text) | Severity: P1 | Status: [CONFIRMED]
  * Location: `misora.py` -> `on_clear_dialogue_skeleton()`, `TranslatorAssistantDialog._on_apply()`
  * Problem: Neither handler checks `is_box_locked()`, allowing locked boxes to be wiped or overwritten. `_on_apply()` also calls `.strip()` on `txt_trans.get("1.0", tk.END)`, stripping intentional whitespace/line breaks.
  * Impact: Silent overwrite/wiping of proofread locked boxes.
  * Proposed Fix Direction: Skip locked boxes in `on_clear_dialogue_skeleton()` and report preserved count; block `_on_apply()` with toast on locked boxes and use `get("1.0", "end-1c")` without destructive `.strip()`.

- [GEM-B11] Async MTL Cross-File Stale Injection & Remaining Rule 15 Worker-Thread `after_idle` Calls | Severity: P1 | Status: [CONFIRMED]
  * Location: `misora.py` -> `on_translate_current_box()`, `TranslatorAssistantDialog._on_translate()` / `_on_fetch_all()`, `MTLSettingsDialog._on_test_connection()`
  * Problem:
    1. `on_translate_current_box()` (F8) captures only `b_idx` — NOT `file_path`, `box_uid`, or a request sequence number. Switching files or modifying box structure while a request is in flight injects the translation into the WRONG file/box!
    2. `on_translate_current_box()`, `TranslatorAssistantDialog`, and `MTLSettingsDialog` still invoke `self.after_idle(...)` directly from background threads (violating Rule 15: "Workers never call Tk methods").
  * Impact: Cross-file dialogue corruption on slow MTL responses and Tk thread-safety violation.
  * Proposed Fix Direction: Marshal all async MTL/connection-test results through a main-thread `queue.Queue` polled by the UI, validating `(file_path, box_uid, req_seq)` before applying.

- [GEM-B12] XUAT Sync Key Overwritten with English Text & Positional Key Drift (Rule 10 Broken) + Dead `xuat_entries` | Severity: P1 | Status: [CONFIRMED]
  * Location: `misora.py` -> `on_save()`; `core/xunity_sync.py` -> `XUnitySyncManager`
  * Problem: After saving, `on_save()` executes `self._original_box_texts[b_idx] = box_obj.clean_text`, replacing the Japanese key with English text so a second edit/save fails to match XUAT. `_original_box_texts` is also indexed by mutable `b_idx` rather than `box.uid` (`XUnitySyncManager.register_jp_key()`/`get_jp_key()` are unused). Meanwhile `getattr(self, "xuat_entries", None)` is never populated anywhere, leaving the `"XUAT Cache"` MTL provider permanently dead.
  * Impact: Bi-directional XUAT sync breaks on second save or after box insertion/deletion; XUAT Cache provider never works.
  * Proposed Fix Direction: Wire immutable `box.uid`-keyed Japanese source snapshots into `open_documents[path]` and `sync_manager`; never overwrite them with translated English text.

- [GEM-B13] Shortcut Router Conflicts, Blocked `Ctrl+Alt` Hotkeys, Schizophrenic `Ctrl+T` & Missing Advertised Bindings (Rule 12) | Severity: P1 | Status: [CONFIRMED]
  * Location: `misora.py` -> `_on_misora_shortcut()`, `_bind_shortcuts()`; `README.md`
  * Problem:
    1. `_on_misora_shortcut()` unconditionally returns `None` when `is_ctrl and is_alt` and omits Windows `0x20000` (`MOD2_MASK`), while `_bind_shortcuts()` has NO bindings for `Ctrl+Alt+X/C/V/A` (advertised in tooltips) — directly contradicting `PROJECT_STATE.md`'s `CTRL-ALT-HOTKEYS-BLOCKED: RESOLVED` claim.
    2. `Ctrl+T` invokes `on_copy_ai_prompt()` when focus is inside an editor (`_on_misora_shortcut()`), but invokes `on_open_translator_assistant()` from menu/root binding (`_bind_shortcuts()`).
    3. `self.bind("<Control-C>", _toggle_continuous_shortcut)` collides with `Ctrl+Shift+C` (`on_copy_script`).
    4. `Ctrl+R` (Ruby) is missing from `_on_misora_shortcut()`, and `Ctrl+N` only works when focus is inside an editor widget. `README.md` advertises non-existent `Ctrl+Shift+S`, `Ctrl+W`, `Ctrl+G`, `Ctrl+Alt+V`.
  * Impact: Broken advertised hotkeys and unexpected actions depending on widget focus.
  * Proposed Fix Direction: Reconcile one canonical shortcut table across `_on_misora_shortcut()`, `_bind_shortcuts()`, menus, tooltips, and `README.md`; explicitly whitelist app `Ctrl+Alt` shortcuts safely without breaking AltGr typing.

- [GEM-B14] `ScriptPastePreviewDialog` White-on-White Invisible Treeview on Dark Themes (`B8`) & Regressed Box 0 Select Checkbox | Severity: P1 | Status: [CONFIRMED]
  * Location: `misora.py` -> `_apply_styles()`, `ScriptPastePreviewDialog`, `_render_continuous_view()`
  * Problem:
    1. `_apply_styles()` configures `"."` with light foreground on dark themes but configures NO `Treeview` or `Treeview.Heading` style. Under `clam`, `ScriptPastePreviewDialog`'s `ttk.Treeview` renders white text on a white background (appears blank).
    2. Contrary to `PROJECT_STATE.md` (`BOX0-NO-SELECT-CHECKBOX: RESOLVED`), `_render_continuous_view()` Card #0 (`hdr_0`) has NO Select Box checkbutton when `var_select_box_mode` is enabled.
  * Impact: Paste/Import preview table appears completely empty on dark themes; Box 0 cannot be selected in Select Box mode.
  * Proposed Fix Direction: Configure `Treeview` and `Treeview.Heading` styles in `_apply_styles()` using theme `bg_editor`/`fg_on_editor`/`highlight_bg`; restore Box 0 select checkbutton in `_render_continuous_view()`.

- [GEM-B15] Continuous View Search-Jump Steals Focus to Hidden `txt_continuous` + Continuous/Box 0 No-Op KeyRelease Dock Rebuild + Frozen Page View Gutter (`B6`) | Severity: P1 | Status: [CONFIRMED]
  * Location: `misora.py` -> `_select_result_index()`, `_commit_widget_edit()`, `_on_dialogue_edited()`, `_on_card_text_edited()`
  * Problem:
    1. `_select_result_index()` calls `_focus_continuous_box(...)` and then immediately calls `self.txt_continuous.focus_set()` — moving focus into the unpacked hidden widget so the user has no visible cursor after search-jump in Continuous View!
    2. `_on_dialogue_edited()` never calls `self._update_gutter_clean()`, so Page View line numbers freeze when pressing Enter/Delete/Paste.
    3. `_commit_widget_edit()` calls `_dirty_state_changed()` unconditionally on Continuous View card `<KeyRelease>` and Box 0 `<KeyRelease>`, causing full Opened Files dock rebuilds on arrow keys (S2 only fixed Page View `txt_dialogue`).
    4. `_on_card_text_edited()` never updates the card header's `(N chars)` counter (`lbl_chars` is not even stored in `_card_widgets[i]`).
  * Impact: Invisible cursor after search jump, frozen line numbers, arrow-key UI stutter, and stale per-card char counts.
  * Proposed Fix Direction: Remove the erroneous `self.txt_continuous.focus_set()` calls for bundle Continuous View; call `_update_gutter_clean()` in `_on_dialogue_edited()`; make `_on_card_text_edited()` and `_on_box0_metadata_edited()` return `bool` to gate `_dirty_state_changed()`; store and update `lbl_chars`.

- [GEM-B16] `core/story_ast.py` v2 Round-Trip Corruption (Unescaped Category Collisions, Whitespace-Only Args, Legacy `cmd_id==0`, Duplicate `_CMD_MAP` Values & `move_box` Merging) | Severity: P1 | Status: [CONFIRMED]
  * Location: `core/story_ast.py` -> `escape_arg()`, `from_v2_text()`, `Record.render_v2()`, `to_binary()`, `_CMD_MAP`, `move_box()`
  * Problem:
    1. `escape_arg()` does not escape arguments matching `DEFAULT_CATEGORIES` (e.g., `"System"`, `"Effect"`, `"Other"`), nor whitespace-only arguments (`" "`), so `from_v2_text()` terminates the record prematurely on those lines.
    2. `Record.render_v2()` checks `if self.cmd_name in _CMD_MAP` (str in int-keyed dict -> ALWAYS `False`), always appending `#id`; external v2 files without `#id` hit duplicate `_CMD_MAP` values (`0`/`15` `"fade"`, `10`/`12` `"touch"`, `11`/`13` `"wait"`, `4`/`18` `"motion"`, `20`/`59` `"effect"`).
    3. `to_binary()` still contains the legacy `if cid == 0 and r.cmd_name != "fade"...` special case forbidden by Rule 8 (contrary to `PROJECT_STATE.md`).
    4. `move_box()` relocates `print`/`tag` records without separating breaker records, allowing moved boxes with the same speaker to silently merge into one box.
    5. `misora.py:_update_raw_view()` highlights Box 0 `cmd_id == 0` using `len(r.args) > 1 and r.args[1]`, whereas `story_ast.get_metadata()` reads `r.args[0]`.
  * Impact: v2 script corruption on edge arguments, broken external v2 interop, and accidental box merging on move.
  * Proposed Fix Direction: Escape category collisions and trailing/whitespace-only args (aligning with `priconne_tool.py`), remove `cmd_id == 0` special case in `to_binary()`, preserve breakers in `move_box()`, and align `_update_raw_view()` Box 0 highlight with `get_metadata()`.

- [GEM-B17] `core/security.py` DPAPI Fails Open to Plaintext & Silent Key Wipe on Decrypt Failure | Severity: P1 | Status: [CONFIRMED]
  * Location: `core/security.py` -> `protect_secret()`, `unprotect_secret()`
  * Problem: On encryption error, `protect_secret()` swallows the exception and returns raw `plaintext` (saving API keys unencrypted to disk). On decryption error, `unprotect_secret()` silently returns `""`, wiping the saved key on next config save with zero user warning.
  * Impact: Silent plaintext credential exposure or unexplained API key loss.
  * Proposed Fix Direction: Fail closed on encryption failure (raise explicit security error + warn user; never silently write plaintext) while preserving read compatibility for legacy plaintext configs; surface explicit warning on decryption failure without silently overwriting the stored encrypted value.

- [GEM-B18] Search Engine Silently Swallows File Errors, Misses In-Memory Plain-Text Edits, & Races on Re-Entrant `<Return>` / Rapid Restart | Severity: P1 | Status: [CONFIRMED]
  * Location: `core/search_engine.py` -> `search_file()`, `search_directory()`; `misora.py` -> `on_start_search()`, `_run_background_search()`, `_process_search_queue()`
  * Problem:
    1. `search_file()` catches `except Exception: pass` for both bundles and text files, silently under-reporting unreadable/corrupt files (violating Rule 15).
    2. `on_start_search()` snapshots only `StoryDocument` entries into `mem_docs`, ignoring unsaved edits in open plain-text files; and `search_directory()` looks up `in_memory_docs.get(fp)` using un-resolved paths that can miss resolved `open_documents` keys.
    3. Pressing `<Return>` in `search_entry` while a search is running ignores `btn_find` disabled state and spawns concurrent search threads sharing one `search_queue` with no `search_seq` generation guard.
  * Impact: Missing search matches on edited text files, silent skipped files, and mixed/corrupted search results on rapid re-search.
  * Proposed Fix Direction: Return/report per-file read errors via a skipped channel; snapshot plain-text buffers too and normalize lookup paths; add a monotonic `search_seq` generation guard and ignore re-entrant `<Return>` while searching.

- [GEM-B19] UnityPy Environment Leak on Reload/Revert + Missing `after info` Sweep & Unclosed Logger Thread on Exit + Synchronous Session Restore + Fragile Splash Filename Parse | Severity: P1/P2 | Status: [CONFIRMED]
  * Location: `misora.py` -> `open_file()`, `destroy()`, `_on_app_exit()`, `__init__()`; `assets/splash.py` -> `SPLASH_IMAGES`; `core/xunity_sync.py` -> `find_and_update()`
  * Problem:
    1. `open_file(..., reload_from_disk=True)` overwrites `self.open_documents[file_path]` without calling `dispose_unity_env()` on the previous entry's `"env"`.
    2. `destroy()` does NOT perform the `self.tk.call("after", "info")` sweep claimed in `PROJECT_STATE.md`, and `_on_app_exit()`/`destroy()` never call `self.logger.close()`, risking dropped final log lines.
    3. `MisoraApp.__init__()` loads `initial_path` and `_saved_opened_files` synchronously BEFORE `deiconify()` (contrary to `PROJECT_STATE.md` Phase 3 & Rule 22).
    4. `assets/splash.py` sorts `Splash_*.jpg` via `int(n.replace(...))` with no error guard — any non-numeric `Splash_*.jpg` crashes startup on import.
    5. `on_save()` crashes into the error handler (`IndexError`) if saving a story document with 0 dialogue boxes (e.g., metadata-only); `xunity_sync.find_and_update()` uses non-unique `.tmp` with no Windows retry and splits mixed-EOL files strictly on one `newline` string.
  * Impact: Memory leaks on reload, startup freeze on large sessions, startup crash on stray splash filename, and fragile XUAT writes.
  * Proposed Fix Direction: Dispose old `env` on reload; close logger cleanly and sweep `after` jobs on destroy; defer session restore via `after_idle` after `deiconify()`; harden splash sorting; guard 0-box saves; delegate XUAT writes to `write_atomic_encoded()`.

- [GEM-B20] `PROJECT_STATE.md` Severe Ledger Drift vs. Actual v1.4.0 Implementation | Severity: P1 (Process/Governance) | Status: [CONFIRMED]
  * Location: `PROJECT_STATE.md` vs. `misora.py`, `core/story_ast.py`
  * Problem: Multiple defects marked `RESOLVED` in `PROJECT_STATE.md` are demonstrably still broken or regressed in live v1.4.0 (`CTRL-ALT-HOTKEYS-BLOCKED`, `BOX0-NO-SELECT-CHECKBOX`, `SIZE-RIBBON-NO-COMMIT`, `CONTINUOUS-RIBBON-TARGET-STALE`, `PLAINTEXT-SAVE-ROUTING`, `CMD0-SPECIAL-CASE`, `FIND-REPLACE-UI-ASYMMETRY` still uses `pack()` not 5-col `grid`, `after() info` sweep missing, deferred session restore missing). Additionally, S8b-1..4 and S9a..c in v1.4.0 diverged completely from previously discussed UX slices (Dialogue Preview, Ribbon/Tooltips/Gutter, Lock/Pin, CSIF/B8, Open Project/Console, MTL Drawer, Import from XUAT).
  * Impact: Future AI agents trusting `PROJECT_STATE.md` will skip real P0/P1 defects or mis-target slices.
  * Proposed Fix Direction: Reconcile `PROJECT_STATE.md` strictly against verified code during the next hygiene/planning cycle.

======================================================================
2. EFFICIENCY, PERFORMANCE & HYGIENE OBSERVATIONS
======================================================================

- [GEM-E01] Search Results Full Widget Rebuild on Every Queue Batch | Measure-First: Yes | Status: [CONFIRMED]
  * Location: `misora.py` -> `_process_search_queue()`
  * Observation: `_render_search_results()` deletes and rebuilds the entire `txt_results` widget on EVERY `"batch"` tuple popped inside the `while True:` loop rather than once after draining available messages.
  * Recommendation: Set a `dirty_render = True` flag inside the `while` loop and call `_render_search_results()` once after the queue drains (simple, zero-risk win).

- [GEM-E02] Redundant Cross-View NGUI Highlighting & Sync Layout on Every Keystroke | Measure-First: Yes | Status: [CONFIRMED]
  * Location: `misora.py` -> `_on_dialogue_edited()`, `_highlight_ngui_tags()`
  * Observation: Every keystroke in Page View calls `_highlight_ngui_tags()`, which scans BOTH `txt_dialogue` AND the hidden `txt_continuous` widget, plus calls `gd_inner.update_idletasks()` via `_auto_resize_dialogue_box()`.
  * Recommendation: Only highlight the currently visible view widget; measure before adding keystroke debouncing.

- [GEM-E03] Unbounded `cstyle_*` Tag Growth in Compiled Preview | Measure-First: No | Status: [CONFIRMED]
  * Location: `misora.py` -> `_insert_compiled_ngui_text()`, `_get_or_create_compiled_style_tag()`
  * Observation: Gradient preview mints per-character `cstyle_*` Tcl tags on `txt_dialogue` and never sweeps them on box navigation (only swept on theme/font change in `_configure_editor_rich_tags()`).
  * Recommendation: Sweep `cstyle_*` tags before repopulating compiled preview widgets.

- [GEM-E04] Dead Code, Misleading UI Labels & Unused Settings | Measure-First: No | Status: [CONFIRMED]
  * Location: `misora.py` -> `_update_gutter_cont()`, `gutter_cont`, `BatchTranslateDialog._toggle_pin_top()`, `NguiColorPickerPopup._sync_ui_from_hsv()`, `AIPromptSettingsDialog`, `on_copy_ai_prompt()`
  * Observation:
    - `_update_gutter_cont()` has zero callers while `gutter_cont` can still be packed empty on plain-text Continuous View.
    - `BatchTranslateDialog._toggle_pin_top()` is dead copy-pasted code referencing non-existent `self.btn_pin`.
    - `NguiColorPickerPopup` gradient button text still displays invalid comma syntax `Insert [C0,C1]` (while inserting `[C0-C1]`), and `__init__` writes `picker_error.log` to CWD.
    - `AIPromptSettingsDialog` shows legacy `=== [BOX:0|Speaker:...] ===` checkbox text for `ai_prompt_include_speaker`, which `on_copy_ai_prompt()` never reads.
    - `on_box_new()` honors `_is_speaker_pinned`, while Page View `_update_views()` ignores it unconditionally.
  * Recommendation: Clean up dead methods/widgets and align labels with real behavior.

- [GEM-E05] Automated Tests Pollute Repo `backups/` Folder | Measure-First: No | Status: [CONFIRMED]
  * Location: `misora.py` -> `_get_backup_dir()` (evidenced by hundreds of `cancel1.bak_*`, `dirty.bak_*`, `doc.bak_*`, `doc_a.bak_*`, `cp932_dict.bak_*` files in the user's ZIP archive)
  * Observation: Tests calling `on_save()` without redirecting `app.backup_folder` to a `TemporaryDirectory` write permanent `.bak_*.txt` junk files into `D:\Misora-Editor\backups\`.
  * Recommendation: Ensure test fixtures isolate `app.backup_folder` into each test's temp directory alongside `CONFIG_PATH`.

======================================================================
3. FEATURE & UX IMPROVEMENT IDEAS (SCOPED & PRACTICAL)
======================================================================

- [GEM-F01] Priconne Fixed-Box Dialogue Preview (Page View Only, `wrap="none"`, `50x3` Pixel Ruler)
  * User Value: Lets translators verify actual in-game spatial fit (both horizontal right-spill in non-NGUI scenes and vertical >3-line / `<size>` overflow) without launching the game or shipping game assets.
  * Proposed Scope: Hybrid `tk.Canvas` + single embedded read-only `tk.Text` (`wrap="none"`), deterministic `logical_lines`, Tk `ypixels`/`xpixels` measurement, simultaneous dual-axis overflow indicators, caret/selection/`yview` restore on Preview OFF.
  * Guardrails / Risks: Pure presentation layer (zero doc/dirty/undo mutation), conditional `_sync_gd_scroll_bounds()` clamp exemption, zero per-box Canvas creation, no game assets/emulation.

- [GEM-F02] Unified Editor UX Polish (View Ribbon Grouping, Mode Naming, 1-Tier Rich Tooltips, Soft-Lock Per-Card Alignment, Hybrid Pin Navigation)
  * User Value: Fixes daily proofreading friction (clear mode names, uniform `VIEW` toggle icons, 1-tier structured tooltips with real names/shortcuts/examples, aligned per-card soft-lock with Cut=Copy + toast, hybrid Pin jumping to same speaker while preserving new-box prefill).
  * Proposed Scope: Split across small focused slices (Presentation vs. Behavior) so diffs stay reviewable.
  * Guardrails / Risks: Single 350ms timer in `ToolTip` (no multi-stage timer chains); preserve alignment when Select Box mode toggles.

- [GEM-F03] Docked MTL Drawer (3rd Side-Drawer Tab) & Retirement of Floating `TranslatorAssistantDialog`
  * User Value: Eliminates clunky modal/floating MTL popups and F8 silent overwrites; gives a full-height editable scratchpad with shared session cache, opt-in debounced Live Translation (default OFF), and auto-close/reopen when `Import from XUAT` opens.
  * Proposed Scope: Queue-marshaled worker (Rule 15), `(file, box_uid, seq)` stale guard, URL allowlist, XUAT literal `\n` rendered as real Enter via backslash-parity-aware unescape.
  * Guardrails / Risks: Exclude scratchpad from story-widget routing and ribbon dispatch; no compare-all spam.

- [GEM-F04] Native `Import from XUAT` Window (`core/xuat_index.py`)
  * User Value: Directly replaces manual CLI `xuat2raw` / `advscript` migration workflows for 300k+ line XUAT projects inside Misora with story-order context.
  * Proposed Scope: Background in-memory XUAT indexer (populating `xuat_entries`), lightweight Treeview left + candidate inspector right + status filter chips, 3-tier conflict scope (this-box default, per-story, global opt-in), separate dialogue/speaker completion meters, "Copy Missing + Context" button, symmetric `\n` unescape.
  * Guardrails / Risks: No `conflict_manager`, no global XUAT auto-pruning, no heavy dual/triple card streams.

- [GEM-F05] Text-Only JP Story Dataminer (`core/story_dataminer.py` — Rewrite of `NewDataMiner` for Stories Only)
  * User Value: Completes the end-to-end fansub pipeline inside Misora (Search JP story by ID/character/title -> check `RedirectedResources` patch status -> download tiny `.unity3d` story bundles -> open directly in Misora).
  * Proposed Scope: Strict JP story-text subset only (`prd-priconne-redive.akamaized.net` `storydata*_assetmanifest` + Robo Ninon `master.db` read-only search + `RedirectIndex` duplicate status). Strip out all Audio/Movie/Spine/Texture extractors and `.exe` dependencies (`UsmToolkit`, `vgmstream`).
  * Guardrails / Risks: Schedule strictly AFTER core integrity & `Import from XUAT`; all network/SQLite I/O on background threads via queue; add manifest fetcher, MD5/size verification, path-traversal guard, and close SQLite before Windows `os.replace()` DB update.

======================================================================
4. REFERENCE TOOLS / VISUAL ASSETS AUDIT
======================================================================

- [GEM-R01] `advscript.py` — 6 Legacy Traps (Do NOT Port Blindly Into `core/xuat_index.py`)
  * `Store.load_file()` splits flat lines with `line.split("=", 1)` instead of first unescaped `=` (breaks keys containing `\=`), and flips the entire file to block mode if ANY line starts with `=`.
  * `Store.resolve_conflict()` writes `self.resolutions[norm_k] = chosen.val` unconditionally even without `'1a'`, silently enforcing global conflict resolution on short context-dependent Japanese lines (`はい`, `うん`).
  * `Store._fuzzy()` slices `list(pool)[:4000]` on an unordered Python `set` (non-deterministic fuzzy results).
  * `prompt_xuat_cleanup()` imports `conflict_manager` and prunes lines globally after one story repacks, breaking other unmigrated stories sharing those lines.
  * `norm2()` ignores NGUI tags and `{playername}`/`{0}` equivalence.

- [GEM-R02] `priconne_tool.py` — Completion Gate & Command Table Traps
  * `run_autotranslate()` computes `is_complete` ignoring untranslated speaker names (`miss_names`).
  * `COMMANDS` table in `priconne_tool.py` uses completely different command IDs (`0=title`, `1=outline`, `8=print`, `12=touch`, `14=vo`) than Misora's `core/story_ast.py` `_CMD_MAP` (`0=fade`, `1=log`, `6=print`, `12=touch`, `35=tag`). Any v2 interop between the two tools must be verified against real production `.unity3d` binaries, not assumed identical!

- [GEM-R03] `NewDataMiner` (`manifest_manager.py`, `db_updater.py`, `downloader.py`, `resource_cross_ref.py`) — 4 Gaps to Fix in Text-Only Rewrite
  * `manifest_manager.py` only reads already-downloaded local manifests — it has NO remote manifest download logic yet.
  * `db_updater.py` uses `db_path.unlink(); temp_dest.rename(db_path)` without closing active SQLite handles (fails on Windows file locks and is non-atomic on crash).
  * `downloader.py` does not write to `.part` temp files, does not verify `entry.hash` (MD5), and does not guard `entry.path` against path traversal.
  * `resource_cross_ref.py:discover_story()` pulls all assets matching `story_id` (including voice/icons); Misora's text-only fetcher must filter strictly to `storydata_<id>.unity3d` (and optionally subtitle bundles if approved).

- [GEM-R04] `asset_registry.py` — Clean Pattern Worth Reusing (With 1 Bug Fix)
  * `BepInExWorkspace` and `RedirectIndex` cleanly scan `RedirectedResources` with bounded non-recursive `os.scandir`.
  * Note bug in `priconne_tool.py:run_integrated_workflow()`: `existing = redir_index.find_match(ident)` returns a 3-tuple `(MatchLevel, Optional[Path], List[Path])`, yet `priconne_tool.py` accesses `existing.path.name` (`AttributeError`). Do not copy that caller pattern.

======================================================================
5. OPEN QUESTIONS FOR PHASE 2 DEBATE
======================================================================

1. [To User — Manual Bug Intake] Which specific new bugs and legacy bugs did you observe manually in v1.4.0 so we can map every single one against `GEM-B01`..`GEM-B20` and catch any UI/runtime defects not visible from static reading?
2. [To Peer AIs — `tests/*.py` Audit] Since `tests/*.py` were not uploaded in this turn, can peer AIs with full GitHub access verify why the 234/234 test suite did NOT catch `GEM-B01` (`_on_card_paste_caret` dirty reset), `GEM-B02` (`bundle_env` wrong key), `GEM-B06` (Windows LF->CRLF in `write_atomic_encoded`), and `GEM-B07` (Page View ribbon title-dirty skip)?
3. [To Peer AIs — `story_ast._CMD_MAP` vs `priconne_tool.COMMANDS`] Confirm against real Priconne `.unity3d` fixture `storydata_1001005.unity3d` which command IDs are authoritative for Box 0 metadata (`title`/`subtitle`/`summary`) and dialogue (`print`/`tag`/`focus`), so `GEM-B16` fixes v2 round-trip without breaking binary compatibility.
4. [To User — Scope & Priority Order] For the new cycle starting from v1.4.0: should we execute a dedicated **v1.4.x Stabilization Pass** (`GEM-B01`..`GEM-B20` + your manual findings) FIRST before building the deferred UX & feature slices (`S8b-1..4`, `Open Project`/Console, `MTL Drawer`, `Import from XUAT`, and `Text-Only Story Dataminer`)?
5. [To User — Text-Only Dataminer Scope] When `Story Dataminer` is scheduled, should v1 fetch strictly `storydata_*.unity3d` story scripts only, or also video subtitle bundles and/or read-only `master.db` dialogue/skill text views?

PHASE 1 STATUS: COMPLETE