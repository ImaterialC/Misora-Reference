# MISORA-EDITOR — PHASE 2 DEBATE, CLEANED USER SPECIFICATION & CROSS-CHECK (ROUND 1)

Reviewer: Gemini
Responding To: Claude Phase 1 Dossier, OpenAI GPT-6 Phase 1 Dossier, and Project Lead Clarified Manual Findings (U-B1..U-B34)
Baseline Verified: Misora-Editor v1.4.0 (commit `1924487f28c9da3b5ede399fd69f24a23e547527` / local v1.4.0 production files: `misora.py`, all 12 `core/*.py`, `assets/icon.py`, `assets/splash.py`, `AGENTS.md`, `PROJECT_STATE.md`, `misora_config.default.json`)

======================================================================
1. CLEANED & CLARIFIED PROJECT LEAD SPECIFICATION (U-B1 .. U-B34)
======================================================================
Note: Rewritten for technical clarity with Project Lead confirmation so peer AIs do not need to re-ask resolved questions. Items marked [OPEN FOR AI COMPARISON] explicitly invite alternative design proposals from Claude and GPT before locking.

### A. Search & Replace Bar Layout
- [U-B1] Align Find and Replace text entry boxes to identical horizontal start/end coordinates.
- [U-B2] Align the 4 action buttons (`Find in Files`, `Cancel`, `Replace`, `Replace All`) in a symmetrical grid with uniform widths/heights.
- [U-B21] When Search Scope is set to `Current File(s)`, hide the directory path textbox (and its browse button) rather than leaving a disabled/readonly field visible (preserve stored folder paths in memory/config).

### B. Toolbar, Ribbon, Icons & Mode Naming
- [U-B3 & U-B5 — CONFIRMED DUPLICATE, MERGED] The `{playername}` / `{0}` button must become an icon-only button (`player.png`, NO `{0}` label text), with a clear tooltip explaining its function (`{playername}` / `{0}`), and [U-B13] moved OUT of the NGUI formatting ribbon group (e.g., to the speaker/text-actions area).
- [U-B4] Remove the standalone `[-]` button from the NGUI ribbon (redundant with Color/Gradient wrappers which already emit `[-]`; keep `[-]` in the NGUI Glossary / menu).
- [U-B6, U-B7, U-B8, U-B30]
  * Rename toggle `Continuous View` -> `All Script` (displays all dialogue boxes sequentially top-to-bottom).
  * Group the 3 view toggles (`Select Box`, `All Script`, `Preview`) into ONE unified `VIEW` ribbon group, adding matching icons for `Select Box` and `All Script` (plus Unicode fallback + tooltips per `AGENTS.md` §21).
  * Replace confusing `GAME VIEW (Clean Dialogue)` / `GAME VIEW (Continuous Stream)` headers with:
    - Preview OFF: `Dialogue` / `All Script`
    - Preview ON: `Dialogue Preview` / `All Script Preview`
  * [OPEN FOR AI COMPARISON — Bottom Pane Name] Do NOT keep `"Raw Script"` for the bottom AST pane because `"Script"` collides confusingly with `"All Script"`. Project Lead suggests `"Raw File"` or `"Raw"` and invites better naming suggestions (Gemini proposes `"Raw Data"` or `"Raw Commands"`).
- [U-B14] Add `View > Toggle NGUI Ribbon` to hide/show the NGUI formatting buttons. Root UX problem: on small/snapped windows (<=1280px), right-packed toolbar controls vanish/crop off-screen; toolbar layout must prevent control disappearance and allow collapsing NGUI controls when not needed.

### C. Selection & Translation Lock UX
- [U-B11 & U-B29] `Select Box` mode must work in BOTH `All Script` AND single-box `Dialogue` view. In `Dialogue` view, display an inline header checkbox (e.g., `[ ] Select Box #N (X selected)`) so the translator can navigate across boxes and check specific boxes for multi-box Copy/Cut. (Also restore the missing Box 0 select checkbox in `All Script` view.)
- [U-B12] Place the Translation Lock icon immediately to the right of the `Select Box` checkbox in card headers (with reserved slot width so headers never shift horizontally when `Select Box` mode is toggled).

### D. Left Dock, Empty State, Multi-Open & `.misora` Workspace Sessions
- [U-B15] Convert the left `Search Results` / `Opened Files` dock into a clean collapsible/openable drawer.
- [U-B16] Default empty state (first launch or when 0 files are open): display a large centered `"Open Files"` button with a clear hint underneath (drag & drop `.unity3d` story files here, or open a saved `.misora` workspace project).
- [U-B19] Double-clicking the `Opened Files` tab triggers `Open Files`.
- [U-B20] `Open Files` dialog must allow selecting multiple files at once (`askopenfilenames`) with a single batched UI refresh.
- [U-B17 & U-B18 — OPEN FOR AI COMPARISON] Project Session Save (`.misora` file):
  * Project Lead Goal: Save an in-progress translation session (typically ~8 episode files per chapter/event, ~20-50 boxes each; even 100 boxes is ~21 KB) as a `.misora` file and resume later — ideally preserving ALL unsaved edits without yet overwriting target `.unity3d` files on disk.
  * Confirmed Constraint: Project Lead agrees NOT to embed raw binary `.unity3d` blobs inside `.misora`.
  * Gemini's Proposal (for comparison with Claude & GPT): `.misora` as an atomic JSON workspace file storing file list, active file/box, view/scope state, per-doc `box.uid` locks, AND — for dirty documents — their lossless v2 text draft (`to_v2_text()`) / plain-text draft + immutable original JP keys + SHA-256 hash of the original disk file. On open, load real `.unity3d` bundles from disk, check disk hashes, apply drafts into memory (`dirty=True`), and if another session is currently open (or disk files diverged), show [U-B18] an Overwrite Warning + Project Difference Mapping dialog (Current vs. Incoming files, dirty/conflict indicators, Save / Overwrite / Cancel).
  * Peer AIs: Please critique Gemini's draft-snapshot-plus-hash approach or propose a cleaner alternative!

### E. Rulers, Overflow Detection & Game-Style Preview (Native Overflow Semantics)
- [U-B22 — DECIDED] REMOVE the inaccurate character counter completely (`lbl_char_count` in Page View and `(N chars)` in All Script card headers). Rely on calibrated rulers and pixel-accurate overflow highlighting instead.
- [U-B23, U-B24, U-B25, U-B26]
  * Fix the misleading horizontal ruler: previously `Consolas 9pt` ruler vs `Segoe UI 11pt` editor made 50 digits appear at column "60" (`images/bandicam 2026-11-23 12-02-06-049.jpg`). Calibrate ruler ticks directly from the active editor font's pixel metrics (`50` digit-widths = `editor_font.measure("1234567890" * 5)`), NOT character count and NOT column 60 of a mismatched font.
  * Horizontal ruler red zone: starts past the calibrated `50` digit-width safe bound.
  * Vertical line-number gutter red zone: starts at line `4` and onward (and fix frozen Page View gutter updates on Enter/Delete/Paste).
  * Inline horizontal overflow highlight: highlight text exceeding the `50` digit-width pixel boundary natively via pixel measurement so narrow Latin glyphs and wide Japanese CJK glyphs (~2x width) are measured accurately.
- [U-B27 & U-B28] Game-Style Preview (`Dialogue Preview` & `All Script Preview`):
  * Critical Domain Context from Project Lead: While Priconne Re:TL currently uses a safety plugin that auto-resizes text beyond 50 chars or 4+ lines, the NATIVE game engine does NOT auto-shrink — text visually bleeds/overflows straight past the dialogue box texture border!
  * Required Preview Behavior: Draw the game-style dialogue box as a visual background frame (calibrated to `50` digit-widths x `3` lines safe area, with a small visual margin to the outer border, matching `images/bandicam 2026-11-22 02-28-14-200.jpg` for Page Preview and `images/bandicam 2026-11-22 02-28-27-995.jpg` for All Script Preview). Use `wrap="none"` so over-wide or >3-line text visibly spills/bleeds past the safe box boundary, letting the translator judge whether slight margin bleed is acceptable.
  * Implementation Guardrail: Code-drawn Tkinter primitives (cream/gold frame, pink `▼`, zero copyrighted `AtlasAdv` sprites bundled into the MIT repo). Start v1 with Dialogue (`50x3`) and All Script (`50x3`); Box 0 Summary profile follows once measured.

### F. Editable Raw Pane (Whole-File v2)
- [U-B31] Allow editing the bottom Raw pane across the **entire file** (needed so translators can edit sensitive non-dialogue records such as voice-file cues).
  * Required Safety Flow: Must use lossless v2 text representation (only after v2 codec round-trip bugs are fixed per `AGENTS.md` §8). Before committing changes to the workspace, show a confirmation warning prompt (`Yes/No`). On `Yes`, parse and validate the edited text (including binary serializability check); if valid, apply atomically as one undoable operation and refresh all views; if parsing/validation fails (e.g., corrupted command or invalid structure), abort and revert cleanly with a clear error message. (Until this feature is implemented, set `txt_raw` read-only so accidental edits are not silently discarded.)

### G. Right-Side MTL Drawer & `Import from XUAT`
- [U-B9, U-B32, U-B33 — OPEN FOR AI COMPARISON on All-Script Layout]
  * Project Lead approves amending `AGENTS.md` §24 once P0/P1 stabilization passes.
  * Move MTL into a 3rd tab in the right-side drawer (retiring the floating `TranslatorAssistantDialog`).
  * **Dialogue (1-box) mode (`U-B32`):** Stack enabled MTL engines vertically from top to bottom. Each engine card has an editable translation box, a per-card `↻` Refresh button, and a `→` Apply button (respecting Translation Lock), plus a top `Refresh All` control (respecting enabled-engine opt-in + session cache + paid-API confirmation to avoid quota burn).
  * **All Script mode (`U-B33`):** Switch the MTL drawer to display translations across ALL boxes for ONE engine selected at the top.
    - Gemini's Proposal (for comparison with Claude & GPT): To avoid doubling Tkinter RAM (~320 MB+) and UI lag from 142 simultaneous `tk.Text` editors inside the right drawer, render a lightweight `ttk.Treeview` list (`Box # | Translation | Status`, synced to active box) + ONE shared editable scratchpad + `Refresh` / `Apply Box` / `Apply All (Skip Locked)` bar at the bottom.
    - Peer AIs: Please critique or propose an even cleaner Tkinter-safe layout for `U-B33`!
- [U-B34] Native `Import from XUAT` floating resolution window (All-Script-like scan workflow):
  * Single-pass background XUAT indexer (`core/xuat_index.py`), handling duplicate translations across project files (3-tier conflict scope: This Box default / This Story / Global opt-in) and missing/untranslated lines, separate dialogue/speaker completion meters, symmetric backslash-parity-aware `\n` unescape (so XUAT literal `\n` renders as real Enter line breaks in Misora), NO `conflict_manager`, NO global XUAT auto-pruning. Auto-close MTL Drawer when `Import from XUAT` opens.

### H. Confirmed Sequencing & Priority Agreement
- Project Lead explicitly APPROVED:
  1. **Stabilization First:** Fix confirmed v1.4.0 P0/P1 data-integrity, threading, and regression defects FIRST before implementing new UX/feature slices.
  2. **AGENTS.md §24:** Approved relaxing the MTL Drawer non-goal strictly AFTER the P0/P1 integrity gates pass.
  3. **Preview v1 Scope:** Dialogue (`50x3`) and All Script (`50x3`) first; Box 0 Summary profile deferred until measured.

======================================================================
2. GEMINI CROSS-CHECK VERDICTS ON PEER FINDINGS (CLAUDE & GPT)
======================================================================

### A. Verdicts on Claude's Findings
- [C-B01, C-B02] Find/Replace & 4-button misalignment: [AGREE — CONFIRMED] (unified 5-column `grid`).
- [C-B03..C-B05, C-B10] Player icon-only + out of NGUI + remove ribbon `[-]`: [AGREE — CONFIRMED] (U-B3 confirmed duplicate of U-B5).
- [C-B06] View toggle grouping & icons: [PARTIALLY AGREE] — Factual correction: `assets/icon.py:get_icon()` returns `None` when an icon file is missing (it does NOT fall back to `_create_fallback_icon()`); ensure Unicode fallback + tooltips per `AGENTS.md` §21.
- [C-B07] Blank `ScriptPastePreviewDialog` Treeview on dark themes: [AGREE — CONFIRMED] (`_apply_styles()` lacks `Treeview`/`Treeview.Heading` styling).
- [C-B08, C-N04] Select Box hidden in Page view + misleading toast: [AGREE — CONFIRMED] (also restore missing Box 0 checkbox in Continuous view).
- [C-B09] Lock icon placement next to Select Box checkbox: [AGREE — CONFIRMED].
- [C-B11, C-X01] Controls clipped at <=1280px / snapped windows + `View > Toggle NGUI Ribbon`: [AGREE — CONFIRMED].
- [C-B12] Hide directory textbox on `Current File(s)` scope: [AGREE — CONFIRMED].
- [C-B13..C-B15, C-X02] Char counter removal (`U-B22`) + font-mismatch ruler bug (`U-B26`) + pixel-calibrated red zones (`U-B23..B25`): [PARTIALLY AGREE] — Do not rely on `Text(width=50)` for proportional line width; measure rendered line width natively via Tk `xpixels` / editor-font pixel ruler against `editor_font.measure("1234567890" * 5)`.
- [C-N01] Translation locks wiped on file switch: [AGREE — CONFIRMED] (matches `GEM-B05`, P0/P1).
- [C-N02, C-F07] Raw View editable safety (`U-B31`): [AGREE — CONFIRMED] — Make read-only immediately in stabilization; build whole-file v2 editing after `GEM-B16`/`GPT-B02` with `DocumentRecordsDelta` undo.
- [C-N03] Missing ribbon tooltips: [AGREE — CONFIRMED].
- [C-F01] Left dock collapsible drawer (`U-B15`): [PARTIALLY AGREE] — Prefer pane-based collapsible drawer over `place()` overlay for Windows focus/z-order stability.
- [C-F02..C-F04] Empty state, double-click tab open, multi-select `askopenfilenames`: [AGREE — CONFIRMED] (batch render once at end).
- [C-F05, C-F06, C-F08, C-F09] `.misora`, Preview, MTL Drawer, `Import from XUAT`: [PARTIALLY AGREE] — See Section 1 D/E/G above for refined guardrails & open AI comparisons.
- [C-E01..C-E04] Measure-first perf & missing `docs/` hygiene: [AGREE — CONFIRMED].

### B. Verdicts on GPT's Findings
- [GPT-B01] Truncated binary ADV records silently accepted (`core/story_ast.py:from_binary`): [AGREE — CONFIRMED] — Must raise `BundleIOError`/`ValueError` instead of `break`ing silently.
- [GPT-B02] Legacy `cmd_id == 0` remapping still present in `to_binary()`: [AGREE — CONFIRMED] (matches `GEM-B16`).
- [GPT-B03, GPT-B06] Single-box F8 MTL cross-file corruption & worker-thread `after_idle`: [AGREE — CONFIRMED] (matches `GEM-B11`; extend queue fix to `TranslatorAssistantDialog` & `MTLSettingsDialog._on_test_connection()`).
- [GPT-B04, GPT-B05] Sparse CSIF index mismatch & pre-validation metadata commit: [AGREE — CONFIRMED] (matches `GEM-B04`; also fix unchecked metadata checkbox bug).
- [GPT-B07] `Match Case` ignored when `Ignore Whitespace` is enabled: [AGREE — CONFIRMED] (`core/search_engine.py:_compile_matcher()` & `_norm_search_with_spans()` unconditionally call `.casefold()`).
- [GPT-B08, GPT-F01] Search errors silently swallowed as 0 results: [AGREE — CONFIRMED] (matches `GEM-B18`; add `os.walk` `onerror` + per-file error channel + plain-text in-memory snapshot + `search_seq` guard).
- [GPT-B09, GPT-F02] XUAT conflict preview not wired into `on_save()`: [PARTIALLY AGREE] — First fix `GEM-B12` (stop overwriting JP keys with English text and key by `box.uid`); prompt only when `preview_matches()` detects `is_conflict=True`.
- [GPT-B10] `MisoraLogger.flush()` races with in-flight disk write (`core/logger.py`): [AGREE — CONFIRMED] (class name is `MisoraLogger`, not `AppLogger`; use completion barrier / `join` + call `logger.close()` on exit).
- [GPT-B11] `protect_secret()` silently falls back to plaintext: [AGREE — CONFIRMED] (matches `GEM-B17`; also warn instead of silent wipe in `unprotect_secret()`).
- [GPT-B12, GPT-F03] Bundle save verification does not compare non-target asset bytes: [PARTIALLY AGREE] — Verify on real fixtures (`storydata_1001005.unity3d` / `9080155.unity3d`) whether non-target raw bytes are invariant under `packer="original"` before enforcing hash equality.
- [GPT-E01..E04, GPT-R01..R04] Hygiene & reference tools audit: [AGREE — CONFIRMED].

======================================================================
3. GEMINI'S CONFIRMED v1.4.0 BUGS & SCOPED IDEAS FOR PEER VERIFICATION
======================================================================
Please cross-check these [CONFIRMED] defects (not yet covered in Claude/GPT Phase 1 reports) directly against `1924487`:

### A. Confirmed Data-Integrity & Regression Bugs
- [GEM-B01] P0 — Multi-box `\n\n\n` paste resets dirty flag to `False` (`misora.py:_on_card_paste_caret()` sets `self.is_dirty = True` without `_mark_document_dirty()`, then `_dirty_state_changed()` overwrites `self.is_dirty` back to `False` from `open_documents[p]["dirty"]`). Also ignores locked boxes.
- [GEM-B02] P0 — Multi-file `on_replace_all()` & `_apply_delta(BulkFileDelta)` wrong cache keys (`"bundle_env"`/`"target_object"` vs `"env"`/`"obj"`), leaking envs and keeping stale bundle handles; overwrites unsaved in-memory edits from disk; marks disk-saved files falsely dirty; ignores Translation Lock & search options (`Match Case`/`Regex`/`Ignore Whitespace`).
- [GEM-B03] P0 — Plain-text `on_save()` reads compiled stripped preview widget (`txt_dialogue`/`txt_continuous`) instead of `self._plain_text_content`, permanently destroying NGUI tags in `.txt` files saved while Preview is ON.
- [GEM-B04 (Part 1)] P0 — Unchecking "Apply metadata to Box 0" in `ScriptPastePreviewDialog` still silently mutates Box 0 without undo because `apply_to_document()` unconditionally applies `result.metadata`.
- [GEM-B05] P0 — `open_file()` wipes `_locked_boxes`, `_modified_boxes`, `current_box_idx`, and overwrites `_original_box_texts` on every tab switch (and right before saving inactive dirty files during `close_file()`/`_on_app_exit()`, which call `open_file(p)` instead of a non-switching `_save_document_entry()`).
- [GEM-B06] P1 — Silent Windows LF -> CRLF corruption in `core/text_encoding.py:write_atomic_encoded()` (`tmp_file.write_text(content)` used instead of `write_bytes(data)` when `not has_bom and newline in (None, "\n")`), plus non-atomic `write_text` in `on_export_script()`.
- [GEM-B07] P1 — Continuous View NGUI Ribbon completely dead (`_insert_text_wrapper()` & `on_insert_ruby()` target hidden `txt_continuous`); `on_insert_font_size()` never commits; AND Page View ribbon wraps skip `_dirty_state_changed()` because `_insert_text_wrapper()` calls `_on_dialogue_edited()` before `apply_ngui_wrapper()` calls `_commit_widget_edit()`, making the second call return `False` (stale `*` title/dock/Undo menu).
- [GEM-B08] P0 — Non-contiguous `on_box_cut()` records only `targets[0]`, scrambling box order on Undo/Redo, and ignores Translation Lock.
- [GEM-B09] P1 — Internal `on_box_paste()` flattens `BoxSnapshot` through `DialogueBlock`, losing `seg_texts`, `voice_cue`, and `extra_args`.
- [GEM-B10] P1 — `on_clear_dialogue_skeleton()` and `TranslatorAssistantDialog._on_apply()` bypass Translation Lock (`_on_apply()` also destructively `.strip()`s intentional whitespace/line breaks).
- [GEM-B12] P1 — `on_save()` overwrites `_original_box_texts[b_idx]` with English text after save (breaking second-save XUAT sync) and indexes by mutable `b_idx` instead of `box.uid` (`XUnitySyncManager.register_jp_key()` unused; `xuat_entries` never populated).
- [GEM-B13] P1 — Shortcut conflicts (`Ctrl+Alt` blocked & missing root bindings despite tooltips; `Ctrl+T` triggers different commands inside vs outside editors; `<Control-C>` collides with `Ctrl+Shift+C`; `Ctrl+R` missing from bindtag router; `README.md` lists non-existent shortcuts).
- [GEM-B15] P1 — Continuous View search-jump steals focus into hidden `txt_continuous`; Page View gutter frozen on Enter/Delete/Paste (`_on_dialogue_edited()` never calls `_update_gutter_clean()`); Continuous & Box 0 no-op `<KeyRelease>` still trigger unconditional `_dirty_state_changed()` dock rebuilds.
- [GEM-B16] P1 — `core/story_ast.py` v2 round-trip gaps: `escape_arg()` does not escape category-name collisions (`System`/`Effect`/etc.) or whitespace-only args; `Record.render_v2()` checks `str in int-keyed _CMD_MAP`; duplicate `_CMD_MAP` names; `move_box()` drops separating breakers (merging same-speaker boxes); `_update_raw_view()` Box 0 highlight checks `r.args[1]` instead of `r.args[0]`.
- [GEM-B19] P1/P2 — UnityPy `env` leak on `open_file(reload_from_disk=True)`; `destroy()` lacks `after info` sweep & never calls `logger.close()`; synchronous session restore in `__init__()` before `deiconify()`; `assets/splash.py` crashes on non-numeric `Splash_*.jpg`; `on_save()` `IndexError` on 0-box metadata-only story; `xunity_sync.py` non-atomic temp filename without Windows retry.
- [GEM-B20 & GEM-E05] Hygiene — Severe `PROJECT_STATE.md` / `README.md` drift vs actual v1.4.0 code; automated tests pollute repo `backups/` folder because `app.backup_folder` is not isolated in test `setUp`.

### B. Gemini's Scoped Efficiency & Feature Proposals (For Peer Debate)
- [GEM-E01..E04] Coalesce `_process_search_queue()` redraws to once per poll cycle; skip hidden-view highlighting on keystrokes; sweep `cstyle_*` tags on Preview populate; clean dead code (`_update_gutter_cont()`, `BatchTranslateDialog._toggle_pin_top()`, comma gradient label in `NguiColorPickerPopup`, unused `ai_prompt_include_speaker` label).
- [GEM-F05 — Deferred / Later-Slice Proposal] **Text-Only JP Story Dataminer (`core/story_dataminer.py`):** Rewrite `NewDataMiner` strictly for JP story text bundles (`prd-priconne-redive.akamaized.net` `storydata*_assetmanifest` + Robo Ninon `master.db` read-only search + `asset_registry.RedirectIndex` patch-status check), stripping all Audio/Movie/Texture/Spine extractors and `.exe` tools, while fixing all 4 legacy traps (`manifest_manager` remote fetch, Windows SQLite close + `os.replace`, `.part` + MD5/size validation + path-traversal guard, story-only filter). Proposed strictly as a later slice AFTER `Import from XUAT` (`U-B34`).
- [GEM-F06 — Polish Reminder] Shared-constant watermark (`Project Priconne Re:TL` / `Cornelia` on Splash scrim + About) and hybrid `Pin 📌` navigation (jump Next/Prev to same speaker + toast + keep `on_box_new` prefill + Page View parity).

======================================================================
4. REMAINING OPEN QUESTIONS / BLOCKERS FOR PHASE 2 CONVERGENCE
======================================================================
1. [Peer Verification] Claude & GPT: Please verify Gemini's newly surfaced P0/P1 defects (`GEM-B01..B20`) against `1924487`.
2. [Design Comparison — `.misora` (`U-B17`/`U-B18`)] Compare Gemini's **JSON Draft Snapshot (v2 text + plain text) + Disk SHA-256 Hash** proposal vs. Claude/GPT's proposals for saving full unsaved edits cleanly without embedding binary `.unity3d` blobs.
3. [Design Comparison — `All Script` MTL Drawer (`U-B33`)] Compare Gemini's **Treeview list + single bottom editable scratchpad** vs. Claude/GPT's proposals for keeping `U-B33` fast and Tkinter-safe on 142+ box stories.
4. [Naming Consensus — Bottom Pane (`U-B30`)] Pick the clearest name to replace `"Raw Script"` (avoiding collision with `"All Script"`): `"Raw Data"`, `"Raw Commands"`, `"Raw File"`, or `"Raw"`.
5. [Technical Check — `story_ast._CMD_MAP` vs `priconne_tool.COMMANDS` & `GPT-B12`] Verify authoritative command IDs and non-target asset byte stability on real fixtures (`storydata_1001005.unity3d` / `9080155.unity3d`).
6. [Scope Placement] Confirm whether `GEM-F05` (Text-Only JP Story Dataminer) belongs in this cycle's later slice or deferred to the next cycle after `U-B1..U-B34`.

======================================================================
5. PHASE 2 GATE DECLARATION
======================================================================
PHASE 2 STATUS: OPEN — CONTINUING DEBATE
Blocking Items (if OPEN): Peer verification of `GEM-B01..B20`, design convergence on `.misora` (`U-B17`/`U-B18`), `All Script` MTL Drawer (`U-B33`), bottom Raw pane naming (`U-B30`), and final cycle scope boundary (`GEM-F05`).