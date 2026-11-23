# MISORA-EDITOR — PHASE 2 DEBATE & CROSS-CHECK (ROUND 2 — GEMINI)

Reviewer: Gemini
Responding To: Claude Phase 2 R1 (`Phase_2R1_Claude.md`), Grok Phase 1 (`Phase_1_Grook_result.md`) & Phase 2 R1 (`Phase_2R1_Grook.md`), GPT Phase 1, and Project Lead Final Decisions
Baseline Verified: Misora-Editor v1.4.0 production snapshot (`misora.py`, all 12 `core/*.py`, `assets/icon.py`, `assets/splash.py`, `AGENTS.md`, `PROJECT_STATE.md`, `misora_config.default.json`). Note: `misora.py` was ingested without printed line numbers, so Gemini cites exact file paths, method names, and verbatim code snippets (never fabricating line numbers per PROTOCOL §3.3). Peer line citations against `1924487f28c9da3b5ede399fd69f24a23e547527` are cross-referenced where verified.

======================================================================
1. CONFIRMED PROJECT LEAD RULINGS & RECORD SETTLEMENTS
======================================================================
The Project Lead has explicitly settled the following items (resolving Claude's REC-04, Q1, Q2, Q4, Q5 and Grok's open blockers):

1. [U-B30 — Bottom Pane Name -> LOCKED: `"Raw Commands"`]
   * Project Lead explicitly approved **`Raw Commands`** (unanimous across Project Lead, Claude, Grok, and Gemini).
   * Top pane headers remain locked: `Dialogue` / `All Script` (Preview OFF) and `Dialogue Preview` / `All Script Preview` (Preview ON).

2. [U-B17 — `.misora` v1 Scope -> LOCKED: References + State + Stable-Key Locks ONLY]
   * Project Lead agreed with Claude's warning against conflicting draft versions and unproven v2 losslessness -> **Gemini RETRACTS draft-snapshot embedding for `.misora` v1**.
   * `.misora` v1 stores strictly: schema version, file path list (relative + absolute fallback), active file/box, view/scope state, and per-document locks using a **stable non-runtime key** (`CLAUDE-N02`, never runtime `Record.uid`). Unsaved edits stay with the normal Save/Discard/Cancel workflow (`U-B18` prompts + compact old-vs-new file table with dirty indicators). Closes `Grok-N02` and Claude Q1.

3. [U-B33 — `All Script` MTL Drawer Layout -> LOCKED BY PROJECT LEAD]
   * Project Lead approved Claude's refinement: **one read-only multi-line `tk.Text` list with clickable per-box tagged blocks + one shared bottom editable `tk.Text` scratchpad** (2 Text widgets total; avoids single-line `Treeview` truncation and avoids per-box widget bloat).
   * Confirmed status badges using ~6 shared static Tk tags (near-zero memory overhead, theme-aware):
     - `✓` Ready (translation fetched/cached)
     - `⏳` Translating (in progress)
     - `⚠` Error / Timeout (retryable)
     - `🔒` Locked (grayed-out via theme `fg_muted`; skipped by Translate All / Apply All; Apply disabled on locked box)
     - `-` Untranslated / Empty / Punct-only (grayed-out via theme `fg_muted`)

4. [U-B34 — `Import from XUAT` Floating Window -> LOCKED SPEC BY PROJECT LEAD]
   * **Entry Point & Separation:** Strictly under the **Import** menu (NOT inside MTL Drawer). Opens as a dedicated floating review/pick window. Auto-closes MTL Drawer when opened.
   * **Source Scope:** Searches project XUAT dictionaries strictly under `BepInEx\Translation\en\Text` (using a single background in-memory indexer `core/xuat_index.py`, unified with `D11` / `var_xuat_cache`; NO `conflict_manager`, NO global XUAT auto-pruning).
   * **Layout & Read-Only Contract:**
     - Single outer scrollable list of **paired rows**: Left = Story boxes (`All Script` style), Right = XUAT search results.
     - **BOTH Left and Right boxes are strictly READ-ONLY** (no inline editing inside this dialog; translators polish text in the main editor after applying).
     - **Fixed `3 lines x 50 digit-widths` box size** on BOTH left and right with **NO visible per-box scrollbars** (saves space, guarantees 100% left-right row alignment, and reveals 3x50 fit immediately).
     - **Overflow inspection (anti-scroll-trap):** Normal mousewheel scrolls the outer paired list; overflowing boxes display a subtle indicator (`▼`/`▶`), and clicking/focusing a box lets mousewheel (vertical) / `Shift+Wheel` or drag (horizontal) scroll inside that box without visible scrollbars.
   * **Duplicates, Skips & Locks:**
     - Duplicate matches show `◀ 1/N ▶` controls plus source provenance (`filename:line`).
     - Per-box `Skip` checkbox to ignore individual boxes.
     - Boxes locked in the main editor (`🔒`) are automatically grayed-out and skipped.
   * **Top Filter Bar & Options:**
     - Quick filter chips: `All` | `Duplicates (N)` | `Missing (N)` | `Matched (N)`.
     - Optional checkbox: apply matched speaker name translations from XUAT (with separate dialogue/speaker match counts).
     - Symmetric backslash-parity-aware `\n` unescape so XUAT literal `\n` displays and applies as real in-game Enter line breaks.
   * **Explicit Pre-Apply Confirmation Prompt (NEW PROJECT LEAD REQUIREMENT):**
     - Clicking Apply/Import MUST display a clear confirmation dialog explicitly listing:
       1. Exact box numbers/ranges that WILL be imported/applied.
       2. Exact box numbers skipped due to **Translation Lock (`🔒`)**.
       3. Exact box numbers skipped due to **User Skip checkbox** (and missing/untranslated count).
     - Commits as a single atomic Undo batch (`Ctrl+Z`).

5. [CLAUDE-N03 — Native In-Game Overflow Semantics -> LOCKED]
   * Project Lead confirmed from live in-game test WITHOUT the Re:TL auto-resize plugin: text **bleeds past the dialogue frame when exceeding 50+ chars without a linebreak OR 3+ linebreaks (4+ lines)**.
   * Confirms `wrap="none"` + logical-line pixel width (`50` digit-widths) + vertical `>=4` lines (3+ linebreaks) for `U-B23..U-B28`.

6. [Grok-B06 — Windows `Ctrl+H` Check -> CONFIRMED WORKING]
   * Project Lead verified on Windows v1.4.0 that `Ctrl+H` works properly and does NOT delete a character. Not a P0 blocker; keep only a minor hygiene fix ensuring `bind_all("<Control-h>")` returns `"break"` for non-editor widgets.

7. [Grok-B01 — Multi-Segment Box Policy -> DELEGATED TO AI PANEL]
   * Project Lead delegated the multi-segment edit policy to the AI panel. Gemini's concrete consensus proposal (for Claude/GPT/Grok confirmation):
     - Allow normal editing in Page / All Script view (do NOT block typing, as English phrasing rarely splits 1:1 across JP segments).
     - Display a non-blocking `"N segs"` indicator badge (`Grok-F02` badge only).
     - Snapshot `old_seg_texts` / `new_seg_texts` in `BoxEditDelta` so Undo restores the original multi-segment split losslessly.
     - Preserve full `BoxSnapshot` (`seg_texts`, `voice_cue`, `extra_args`) in internal `on_box_paste()` (`GEM-B09`).

8. [CLAUDE-N04 — Local `docs/` & `storydata_1001005.unity3d`]
   * Project Lead confirmed both were local test files, now deleted with `.gitignore` updated -> reconcile `PROJECT_STATE.md` §2/§9 and `README.md` as hygiene (`DEP-10`).

9. [Scope Exclusions Confirmed by Project Lead]
   * **`GEM-F05` (Text-Only Dataminer)** and **`GEM-F06` (Watermark / Hybrid Pin)** are **DEFERRED / OUT OF THIS CYCLE** (not on the Phase 2.5 ledger).

10. [Record & Source Settlements (Answering Claude REC-01, Q6, Q7)]
    * `Phase_1_Gemini.md` in `Misora-Reference` accidentally holds Claude's Phase 1 dossier; Section 3 below supplies exact file/method/code anchors for every remaining unverified `GEM-*` item and splits `GEM-B19` into atomic IDs `GEM-B19a`..`GEM-B19f`.
    * **Gemini RETRACTS** the unmeasured `~320 MB+` extrapolation for `U-B33` (was a 2x estimate from `THEME-RAW-PERF`; measure-first per PROTOCOL §4).
    * Logger class name (`GPT-B10`): verified in `core/logger.py` as `class MisoraLogger:` (`AppLogger` does not exist).
    * `assets/icon.py:get_icon()` (`C-B06`): verified to return `None` when the PNG is missing (`_create_fallback_icon()` is used only by `apply_window_icon()`); `AGENTS.md` §21 Unicode fallback + tooltips remain required.
    * `GEM-B02` precision (accepting Grok's correction): current-file `on_replace_all()` DOES skip locked boxes; the confirmed defects live in the **multi-file** branch and `_apply_delta(BulkFileDelta)`.

======================================================================
2. VERDICTS ON GROK PHASE 1/2, CLAUDE PHASE 2 R1 & NEWLY SURFACED TRAP
======================================================================

--- A. Newly Surfaced Project-Search / XUAT Root Defect ---

- [GEM-N01] `xuat_search_roots` Leaks Stale Project Paths & Mis-Scopes `BepInEx` Search | Severity: P1 | [CONFIRMED]
  * Location & Evidence: `misora.py:_detect_environment()`, `on_browse_project_folder()`, `_on_folder_path_var_trace()`, `on_open_paths_dialog()`, `on_start_search()`.
  * Problem:
    1. Changing `project_folder` appends to `self.xuat_search_roots` via `insert(0, root)` without ever removing previously configured project folders, and `on_start_search()` always appends local `input`/`output` folders — causing Project search and XUAT sync to leak across stale/unrelated directories.
    2. Pointing `project_folder` to `...\Translation\en` collapses the search root to `Translation\en\Text` only (missing `RedirectedResources`), while pointing to `...\BepInEx` scans all of `BepInEx` including `plugins/` and `config/`.
  * Why it matters: Both Project Search and `U-B34` (`Import from XUAT` scanning `BepInEx\Translation\en\Text`) rely on clean, bounded project-root resolution. Fix by resolving `project_folder` cleanly into bounded `(text_dir, redirected_dir)` without accumulating stale roots.

--- B. Verdicts on Grok's Findings ---

- [Grok-B01] Multi-Segment `inject_box()` Collapses Sibling Segments | Verdict: [PARTIALLY AGREE]
  * Verified in `core/story_ast.py:inject_box()` and `misora.py:_on_dialogue_edited()`. Adopt delegated AI-panel policy in Section 1 #7 (non-blocking edit + `"N segs"` badge + `old_seg_texts`/`new_seg_texts` in `BoxEditDelta` + `GEM-B09` snapshot preservation).

- [Grok-B02] Undo Recorded & Dirty Marked Before Swallowed `inject_box()` Failure | Verdict: [AGREE — CONFIRMED]
  * Verified across `_on_dialogue_edited()`, `_on_card_text_edited()`, and `_flush_continuous_card_edits()`. Mutate model first, record undo/dirty only on success, surface exceptions (`AGENTS.md` §28).

- [Grok-B03] `BatchTranslateDialog._on_close()` Races Undo Batch With Worker | Verdict: [AGREE — CONFIRMED]
  * Verified in `BatchTranslateDialog._on_close()` and `_poll_worker_queue()`. Track `_batch_open: bool`; cancel sets `_cancelled = True` only and calls `end_batch()` strictly ONCE on completion/safe teardown.

- [Grok-B04 + GEM-B16 `move_box` = CLAUDE-N09] Unified Boundary Breaker Ownership | Verdict: [AGREE — CONFIRMED]
  * Verified in `core/story_ast.py:delete_boxes()` and `move_box()`. Touch ONLY empty projected tap-breakers (`cmd_id == 10` / `page` / `next_page` with empty args; NEVER `cmd_id == 12` voice cues or unknown commands), snapshot removed breakers in `BoxStructuralDelta`, with binary round-trip tests.

- [Grok-B05] `on_replace_next()` Only Checks Active Box | Verdict: [PARTIALLY DISPUTED]
  * Counter-evidence in `misora.py:on_replace_next()`: it DOES loop `for i in range(1, total):` to jump to the next box containing `find_text`. However, two real bugs remain: (1) advance loop does NOT skip locked boxes, and (2) ignores `Match Case`/`Regex`/`Ignore Whitespace`. Fix both.

- [Grok-B06] Duplicate `Ctrl+H` Binding Without `"break"` on `bind_all` | Verdict: [PARTIALLY AGREE]
  * Project Lead confirmed `Ctrl+H` works on Windows v1.4.0. Keep low-priority hygiene fix returning `"break"` on `bind_all("<Control-h>")` for non-editor widgets.

- [Grok-B07] `to_binary()` Space Sentinel `" "` for Empty Args | Verdict: [DEFERRED]
  * Agree with Claude & Grok: do NOT change without live client evidence (`AGENTS.md` §7); add fixture round-trip test only.

- [Grok-E02] `on_start_search()` Snapshot Fallback Shares Live `orig_doc` | Verdict: [AGREE — CONFIRMED]
  * Verified in `misora.py:on_start_search()` (`except Exception: mem_docs[fp] = orig_doc`). Fold into `GPT-B08` / `GEM-B18`: skip & report failed snapshot paths; never hand live AST to worker.

- [Grok-E01, Grok-E03, Grok-F01, Grok-F03] | Verdict: [DEFERRED / OUT OF SCOPE]
  * `Grok-E01` measure-first; `Grok-E03` no monolithic rewrite during stabilization; `Grok-F01` superseded by fixing `on_replace_all()`; `Grok-F03` deferred.

--- C. Verdicts on Claude's Traps & Dependencies ---

- [CLAUDE-N01, N04, N05, N06] Ledger Drift, Missing `docs/`, Test-Count Arithmetic (`238` vs `234` + filename mismatch) & Stale `AGENTS.md` §24 | Verdict: [AGREE — CONFIRMED]
  * Reconcile `PROJECT_STATE.md`, `README.md`, and `AGENTS.md` §24 (tying MTL Drawer gate to Phase 2.5 P0/P1 closure) as `DEP-10`.

- [CLAUDE-N02] Stable Non-Runtime Lock Identity | Verdict: [AGREE — CONFIRMED]
  * Use `box.uid` in-memory during live sessions; persist locks in `.misora` via stable composite key `(box_ordinal, sha256(original_jp_text))`, never serializing runtime `Record.uid` (`AGENTS.md` §4). Remap locks/JP keys cleanly after whole-file Raw edits (`U-B31`).

- [CLAUDE-N07 & CLAUDE-N08] XUAT Index Unification & Dirty Checkpoint Inheriting v2 Lossiness | Verdict: [AGREE — CONFIRMED]
  * Unify `core/xuat_index.py` with `var_xuat_cache` / `xuat_entries` (`D11`) while keeping `Import from XUAT` UI strictly separate from MTL Drawer; fixing `GEM-B16`/`GPT-B02` makes S2 `to_v2_text()` dirty checkpoints lossless.

- [Claude Dependency Graph `DEP-1`..`DEP-10`] | Verdict: [AGREE — CONFIRMED]
  * Note: `DEP-1` (`Treeview` styling) still gates `B10` (`ScriptPastePreviewDialog`); `U-B33` uses `tk.Text` and `U-B34` uses paired fixed `3x50` read-only boxes.

======================================================================
3. CODE ANCHORS FOR REMAINING UNVERIFIED `GEM-*` ITEMS (FOR PEER VERIFICATION)
======================================================================
Exact file paths, method names, and verbatim code anchors so GPT, Grok, and Claude (using `Misora.py1.4.0.Part1..4.txt` and `core/*.py`) can complete second-reviewer verification:

1. [GEM-B04 (Part 1) + GPT-B05] `misora.py:_show_paste_preview_and_apply()` & `core/script_codec.py:apply_to_document()`:
   * `_show_paste_preview_and_apply()` gates undo recording on `if apply_meta and not result.metadata.is_empty():`, then unconditionally calls `apply_to_document(self.current_doc, result, ...)` which executes `if not result.metadata.is_empty(): doc.set_metadata(...)` BEFORE sparse validation and WITHOUT an `apply_metadata` parameter.
2. [GEM-B07] `misora.py:_insert_text_wrapper()`, `apply_ngui_wrapper()`, `on_insert_ruby()`, `on_insert_font_size()`:
   * `_insert_text_wrapper()` and `on_insert_ruby()` both contain `if self.var_continuous_view.get(): target = self.txt_continuous` (hidden widget for story bundles); `on_insert_font_size()` inserts `<size=...>` without ever calling `_commit_widget_edit(target)`; and in Page View `_insert_text_wrapper()` calls `self._on_dialogue_edited()`, then `apply_ngui_wrapper()` calls `self._commit_widget_edit(target)` -> calls `_on_dialogue_edited()` a 2nd time -> `old_tx == new_tx` -> returns `False` -> skips `self._dirty_state_changed()` (title `*` and Undo menu remain stale).
3. [GEM-B10] `misora.py:on_clear_dialogue_skeleton()` & `TranslatorAssistantDialog._on_apply()`:
   * `on_clear_dialogue_skeleton()` iterates `for i, box in enumerate(self.current_doc.boxes):` with zero `is_box_locked(i)` check; `TranslatorAssistantDialog._on_apply()` has zero `is_box_locked(b_idx)` check and runs `new_text = self.txt_trans.get("1.0", tk.END).strip()`.
4. [GEM-B11 + GPT-B03/B06] `misora.py:on_translate_current_box()`, `TranslatorAssistantDialog._on_translate()` / `_on_fetch_all()`, `MTLSettingsDialog._on_test_connection()`:
   * All 4 spawn worker threads invoking `self.after_idle(...)` from the worker (violating Rule 15); `on_translate_current_box()` captures only `b_idx` (no `file_path`, `box_uid`, or request seq).
5. [GEM-B12] `misora.py:on_save()` & `core/xunity_sync.py:XUnitySyncManager`:
   * `on_save()` executes `orig_key = self._original_box_texts.get(b_idx, box_obj.clean_text)` followed by `self._original_box_texts[b_idx] = box_obj.clean_text` (overwrites JP key with English!). `register_jp_key()`/`get_jp_key()` and `self.xuat_entries` are unused/unpopulated anywhere in `misora.py`.
6. [GEM-B13] `misora.py:_on_misora_shortcut()` & `_bind_shortcuts()`:
   * `_on_misora_shortcut()` has `if is_ctrl and is_alt: return None` (no `0x20000` mask, no `Ctrl+Alt+X/C/V/A` whitelist), routes `Ctrl+T` to `self.on_copy_ai_prompt()` while `_bind_shortcuts()` routes `<Control-t>` to `self.on_open_translator_assistant()`, and binds `<Control-C>` to `_toggle_continuous_shortcut` (colliding with `Ctrl+Shift+C`).
7. [GEM-B15] `misora.py:_select_result_index()`, `_on_dialogue_edited()`, `_commit_widget_edit()`, `_on_card_text_edited()`:
   * `_select_result_index()` calls `self._focus_continuous_box(...)` and then immediately calls `self.txt_continuous.focus_set()`; `_on_dialogue_edited()` never calls `self._update_gutter_clean()`; `_commit_widget_edit()` calls `self._dirty_state_changed()` unconditionally on Continuous card and Box 0 `<KeyRelease>`.
8. [GEM-B16 + GPT-B02] `core/story_ast.py:escape_arg()`, `Record.render_v2()`, `from_v2_text()`, `to_binary()`, `misora.py:_update_raw_view()`:
   * `escape_arg()` fails to escape `DEFAULT_CATEGORIES` and whitespace-only args (`from_v2_text()` checks `if not l.strip(): break` and `if l in DEFAULT_CATEGORIES:`); `Record.render_v2()` checks `if self.cmd_name in _CMD_MAP` (str in int-keyed dict -> always `False`); `to_binary()` retains `if cid == 0 and r.cmd_name != "fade" and r.cmd_name in _INV_CMD_MAP:`; `_update_raw_view()` highlights `r.cmd_id == 0 and len(r.args) > 1 and r.args[1]` while `get_metadata()` reads `r.args[0]`.
9. [GEM-B19 Split Into Atomic IDs (per Claude)]:
   * `GEM-B19a`: `misora.py:open_file()` (`reload_from_disk=True`) overwrites `self.open_documents[file_path]` without calling `dispose_unity_env()` on prior `entry["env"]`.
   * `GEM-B19b`: `misora.py:destroy()` & `_on_app_exit()` never call `self.logger.close()` and lack `self.tk.call("after", "info")` teardown sweep.
   * `GEM-B19c`: `misora.py:MisoraApp.__init__()` loads `initial_path` and `_saved_opened_files` synchronously BEFORE `self.deiconify()` (Rule 22 / contradicts `PROJECT_STATE` Phase 3).
   * `GEM-B19d`: `assets/splash.py:SPLASH_IMAGES` sorts via unguarded `int(n.replace("Splash_", "").replace(".jpg", ""))` (crashes startup on non-numeric `Splash_*.jpg`).
   * `GEM-B19e`: `misora.py:on_save()` indexes `self.current_doc.boxes[self.current_box_idx]` without guarding empty `self.current_doc.boxes` (0-box metadata-only story raises `IndexError`).
   * `GEM-B19f`: `core/xunity_sync.py:find_and_update()` uses non-unique `f"{tf.name}.{os.getpid()}.tmp"` without Windows retry (should delegate to `write_atomic_encoded()`).

======================================================================
4. REMAINING OPEN QUESTIONS / BLOCKERS
======================================================================
1. [GPT, Grok, Claude] Second-reviewer line verification of Section 3 `GEM-*` anchors + `GEM-N01` (using `Misora.py1.4.0.Part1..4.txt` and `core/*.py`) + GPT's Phase 2 verdicts.
2. [GPT, Grok, Claude] Confirm consensus on:
   - Delegated `Grok-B01` multi-segment policy (non-blocking edit + `"N segs"` badge + `old_seg_texts`/`new_seg_texts` in `BoxEditDelta` + `GEM-B09` snapshot preservation).
   - Project Lead-locked `U-B33` (`tk.Text` multi-line list + bottom scratchpad + 5 static-tag badges with grayed-out `🔒`/`-`).
   - Project Lead-locked `U-B34` (`Import from XUAT` floating window: paired fixed `3x50` read-only boxes, no per-box scrollbars, focus-gated inner scroll, `◀ 1/N ▶` + `file:line`, per-box Skip + Lock auto-skip, filter bar, explicit Pre-Apply summary confirmation listing exact imported / locked-skipped / user-skipped boxes).
3. [All] Pin the exact `HEAD` commit hash of `Misora-Editor` before entering Phase 2.5.

======================================================================
5. PHASE 2 GATE DECLARATION
======================================================================
PHASE 2 STATUS: OPEN — CONTINUING DEBATE
Blocking Items (if OPEN): GPT Phase 2 reply + second-reviewer verification of Section 3 `GEM-*` anchors & `GEM-N01`; peer consensus on `Grok-B01` policy & finalized `U-B34` spec; pinned `HEAD` commit hash.