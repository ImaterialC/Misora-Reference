# MISORA-EDITOR — PHASE 1 INDEPENDENT RESEARCH DOSSIER

Reviewer: Claude (configured id claude-sonnet-5-5; serving model may differ)
Date: 2026-11-23
Inspected Baseline: Misora-Editor main @ 1924487f28c9da3b5ede399fd69f24a23e547527 (2026-11-23 14:16 +0700, "up");
                    Misora-Reference main @ 931bbd061950c5939d95186986aaed69cdd464f4
Reference Files Inspected: images/ (6 files, all viewable), tools/priconne-adv-tools/ (listing + output/9080155.unity3d used as a test fixture),
                    phases/*, PROTOCOL.md, ANTIGRAVITY_GUIDE.md
Method: full read of the relevant misora.py regions (12,143 lines, file complete, AST-parses), core/*.py, AGENTS.md, PROJECT_STATE.md;
        PLUS a headless runtime probe (Xvfb, Python 3.12, Tk 8.6, UnityPy 1.25.4, Linux fallback fonts: Segoe UI/Consolas NOT installed).
        Runtime pixel values are therefore indicative only; mechanisms are font-independent unless stated.
Evidence tags per PROTOCOL: [CONFIRMED] = verified in source and/or observed in the headless run; [NEEDS-VERIFY] = must be re-checked on Windows.
Line numbers refer to commit 1924487.

Legend for the user's items (U-Bxx): "BUG" = defect claim, "FEAT" = feature/UX request, "MIXED" = both.

======================================================================
0. PRELIMINARY NOTES
======================================================================
- [N-01] The user's image links use `references/assets/...`; in Misora-Reference@931bbd0 the files live under `images/`
  (e.g. images/bandicam 2026-11-23 12-02-06-049.jpg). The links 404. Peer AIs must use the `images/` paths or an attached zip.
- [N-02] AGENTS.md §24 lists "MTL drawer" among things not to implement before Phase 1–2 integrity gates; PROJECT_STATE §7 repeats
  "Non-goals: MTL drawer (Phase 5)". Per PROTOCOL §3.5, changing an invariant needs explicit user approval. U-B9/B32/B33 request it;
  we should ask the user to confirm that AGENTS §24 may be amended.
- [N-03] Screenshots are the user's calibration instrument: the strings "1234567890"x5 per line show the in-game dialogue box holds
  3 lines x 50 digits (images/…02-28-14-200.jpg). The Misora screenshot (…12-02-06-049.jpg) shows "Chars: 150 (Max: 50) ⚠ Overflow" for exactly that
  game-fitting text.

======================================================================
1. BUGS & DEFECTS (EVIDENCE-BASED) — VERDICTS ON USER ITEMS B1–B14, B21–B26, B10
======================================================================
- [C-B01] U-B1 Find/Replace text boxes not aligned | BUG | Severity: P2 | Status: [CONFIRMED]
  - Location: misora.py -> MisoraApp._build_search_bar (3371–3531): row1 (3382) and row_replace (3424) are independent pack rows.
    Labels use width=7 (3386, 3426) but "Replace:" is 8 chars in bold Segoe UI, so the label overgrows and shifts the entry.
- Observed (1280x720 headless): search_entry x=84 w=830; replace_entry x=77 w=845 (left edge off by 7 px, width by 15 px).
- Fix direction: one shared grid (label | entry | btn | btn | close) with identical column minsize/weights for both rows.

- [C-B02] U-B2 Four buttons (Find in Files, Cancel, Replace, Replace All) not aligned | BUG | P2 | [CONFIRMED]
  - Location: 3412 (btn_find width=14, style Pink.TButton), 3415 (btn_cancel width=12), 3452 (btn_replace width=14), 3455 (btn_replace_all width=12),
    3419 (btn_close_search, image + width=3) vs spacer_close (3458, fixed 28 px).
- Observed: btn_find x=926 w=156 h=30; btn_replace x=934 w=150 h=28; btn_cancel x=1090 w=134; btn_replace_all x=1092 w=134.
    Width is text/image dependent (ttk width = chars), heights differ because of different styles.
- Fix direction: same grid as C-B01; fixed uniform pixel widths/heights (or sticky="ew" in equal-weight uniform column group).

- [C-B03] U-B3 "button player disingkat" | UNCLEAR (overlaps U-B5) | [NEEDS-VERIFY]
  - Interpreted as "shorten the player button label". If it means a different control the user must say which (see Open Questions).

- [C-B04] U-B4 Remove ribbon "[-]" button | FEAT | [CONFIRMED premise]
  - Location: misora.py 4105–4123 (btn_dash -> apply_ngui_wrapper("[-]","")); no tooltip on it.
  - Premise holds: _apply_active_ribbon_color (5001–5003) and _apply_active_ribbon_gradient (5005–5008) already emit "[RRGGBB]…[-]" / "[c0-c1]…[-]".
  - Caveat: the standalone button also allowed ending a colour at an arbitrary caret without wrapping. Keep as glossary/menu action
    (NGUI_GLOSSARY_ITEMS already insert_close "[-]", 303–329); removal from the ribbon is low risk. PROJECT_STATE Phase 4 already claimed
    "Remove redundant ribbon buttons" — this one survived.

- [C-B05] U-B5 Player button -> icon only | FEAT | [CONFIRMED premise]
  - Location: 4125–4146 (text=" {0}" + image player 14x14, compound=left). Icon-only controls MUST have tooltips (AGENTS §21); this one has none today.

- [C-B06] U-B6/B7/B8/B30 Toggle naming, missing icons, grouping, "Game View (XXX)" naming | MIXED | [CONFIRMED]
  - Location: cb_cont "Continuous View" (3804–3812, in gd_header), cb_sel_box "Select Box" (3814–3822, gd_header), cb_compiled "Preview" (4244–4263, inside actions_bar),
    title strings at 3773, 5996, 6024 ("GAME VIEW (Clean Dialogue)", "GAME VIEW (Continuous Stream)").
- Icons: assets/icons/ has no select_box / all_script / lock / refresh / apply icons (37 files listed); get_icon falls back to a generic placeholder (assets/icon.py:39 _create_fallback_icon). => U-B7 CONFIRMED.
- The three toggles live in two different containers (gd_header vs actions_bar) => U-B8 CONFIRMED.
- Renaming impact: tests contain "Continuous View" only in docstrings; no test asserts the title strings (grep tests/). Keep variable names (var_continuous_view etc.) to avoid test churn.
- Naming note for debate: the title "GAME VIEW" is also misleading because neither view is rendered like the game; U-B30 stands.

- [C-B07] U-B10 Paste/Import Script preview window shows nothing | BUG | Severity: P1 | Status: [CONFIRMED for dark themes]
  - Location: misora.py -> ScriptPastePreviewDialog (10986–11205) uses ttk.Treeview (11110); _apply_styles (2768+) sets style.configure(".", background=bg_dark, foreground=fg_on_dark) (2805)
    under theme "clam" and NEVER configures "Treeview" / "Treeview.Heading" (grep: the only "Treeview" token is 11110).
- Observed: preset "Midnight Violet": Treeview foreground #ffffff on background #ffffff (rows exist: 3 rows, bbox valid, dialog mapped) => white-on-white, table looks empty.
    Default light preset: foreground #221833 on #ffffff => visible. Two other presets are dark ("#14141a", "#161224" bg_dark) and very likely behave the same [NEEDS-VERIFY].
- Impact: user cannot review a destructive paste/import before "Apply Changes".
- Fix direction: configure Treeview/Treeview.Heading (background, fieldbackground, foreground, selected map) from the theme inside _apply_styles; regression test per preset using contrast check.

- [C-B08] U-B11/B29 Select Box only appears in Continuous view / should work in Game (page) view | BUG+FEAT | Severity: P2 | [CONFIRMED]
  - Location: _on_toggle_select_box_mode (7109–7116) re-renders only if continuous is on; the checkbox widgets exist only in _render_continuous_view (7775–7791).
    The toast "Select Box mode enabled" is shown regardless (7116) => misleading state with no visible effect in page view (observed in headless run).
- _selected_boxes (1267) feeds on_box_copy/on_box_cut (7393, 7420); page view has no multi-selection UI. Semantics must be defined (see Open Questions).

- [C-B09] U-B12 Lock icon should be next to the Select Box checkbox | UX | [CONFIRMED premise]
  - Location: card header (7775–7812): checkbox packed first (left), then badge, speaker, voice cue, THEN lbl_lock (7812–7813). Lock is empty text unless locked.
    Page view lock is a separate emoji-text tk.Button (3889–3903) in the speaker row.

- [C-B10] U-B13 Player button out of the NGUI group | FEAT | [CONFIRMED premise]: btn_player is packed inside `ribbon` (4125–4146). Candidate home: speaker row (3825–3912), which already holds speaker-related controls.

- [C-B11] U-B14 + rationale: buttons vanish on small/snapped windows | BUG | Severity: P1 | Status: [CONFIRMED]
  - Location: _build_main_panels: ONE pack row `speaker_ribbon_row` (3825) holds speaker entry, dropdown, pin, voice cue, lock, char counter (pack side=left),
    then `ribbon` (3923, side=right) and `actions_bar` (4008, side=right). Tk pack gives space in packing order, so later-packed widgets are cropped first.
    Same pattern in gd_header (3767–3822): cb_sel_box is packed last and is squeezed first.
- Observed at 1280x720 (not even a snap): empty state: actions_bar shows 2 of ~9 buttons, Preview missing;
    with search bar + file open: ribbon cut off after "[-]" (player, B/I/U/S/Sub/Sup/Size, Undo/Redo gone), actions_bar absent entirely,
    "Continuous Vie" label clipped, Select Box checkbox width ~0 px.
- Structural limits: h_paned minsize left=160/right=420 (3558, 3748), left dock default 340, plus optional right side drawer => the editor pane cannot fit these toolbars at ≤1280 px.
- View menu (3063–3094) has no ribbon/toolbar toggle; user proposes View > Toggle NGUI ribbon.
- Fix direction: grid/multi-row or collapsible toolbar groups; View-menu toggles per group; do not rely on pack order.

- [C-B12] U-B21 "Current File(s)" scope should hide the directory textbox | FEAT | [CONFIRMED premise]
  - Location: _sync_scope_widgets (9098–9127): scope "current" fills the entry with the parent dir (or "(Current Open Files)") and sets readonly; browse is disabled but both stay visible.
  - Guardrail: folder_path_var has a write trace (3509, _on_folder_path_var_trace 9076) and FocusOut saves prefs — hiding must not clear selected_search_folder.

- [C-B13] U-B22 Character count is inaccurate (Latin vs Japanese width) / suggest removing | BUG | Severity: P1 | Status: [CONFIRMED]
  - Location: _update_rendered_char_count (8449–8466) -> core/ngui_tags.py measure_line_lengths (99–109): len(strip_tags(line)) per PHYSICAL line (str.splitlines).
    Hard-coded threshold 45 (8457; tooltip text 3911; PROJECT_STATE line 416, 581). Label "Chars: {total} (Max: {max_line})": total excludes newlines, "Max" = longest physical line.
- Defects: (a) counts characters, not width: a full-width Japanese glyph = 1, a digit = 1, although widths differ ~2x;
    (b) threshold 45 contradicts the user's calibration (50 digit-widths per line, N-03);
    (c) ignores wrapping (editor wrap="word" 4342) — a long logical line is 1 line for the counter;
    (d) strip_tags -> NGUI_TAG_RE (ngui_tags.py:29–43) removes {playername} and {\d+} entirely, so a placeholder that renders as a player name counts 0.
- Ledger drift: PROJECT_STATE D13 says "Game Box Preview measures rendered text width" and GAME-BOX-PREVIEW is RESOLVED; the code measures characters, not width.
- User suggests deleting the counter because rulers exist. Debate point: a corrected pixel-based indicator is cheaper than losing the per-box summary in the continuous card header
    (header shows "(N chars)", 7800–7807, same flaw).

- [C-B14] U-B23/B24/B25 Red zones & overflow highlight | FEAT | [CONFIRMED absent]
  - Location: ruler_clean (4300–4315) and ruler_cont (4524–4539) are disabled tk.Text with ONE inserted static string, no tags; no tag in txt_dialogue marks overflow; no visual-line-count (>3 lines) check anywhere.

- [C-B15] U-B26 / U-B22 Ruler numbers mislead ("60" is really ~50) | BUG | Severity: P1 | Status: [CONFIRMED mechanism; ratio NEEDS-VERIFY on Windows]
  - Location: ruler string literal "     ....5...10 … 80" (4312; 6-space variant 4536) in Consolas max(8, d_sz-2)=9pt (4303, 4527);
    editor txt_dialogue uses Segoe UI 11pt (DEFAULT_PREFS 264–265; 4345), padx=10 (4351), gutter 3 chars of Consolas 11pt (4322–4324).
    Ruler columns are monospace cells of a DIFFERENT font and size, with a hard-coded left offset that ignores padx, gutter width, DPI and font changes.
- Measured from the user's screenshot (…12-02-06-049.jpg, approximate): 50 digits span ~400 px (~8.0 px/digit); ruler pitch ~6.8 px/col => 50 digits ≈ col 59–60. Matches the user's observation.
- Continuous view makes it worse: ruler_cont (4524) sits above a canvas of per-card Text widgets (cards have their own gutters and padx), so no common origin exists.
- Fix direction (for debate, not a prompt): derive all measures from ONE font object: digit_px = tkfont.measure("0") of the editor font; draw the ruler on a Canvas
    with ticks at text_left + k*digit_px; redraw on <Configure>/font/size change. Tk Text `width=N` is measured in "0" widths of the widget font [NEEDS-VERIFY], so a
    game-capacity guide at N=50 digit-widths is exact by construction. Overflow = measured pixel width of wrapped display lines > 50*digit_px; vertical limit = display lines > 3.
    Japanese glyphs then get their true width automatically via font.measure. Windows probe to settle the ratio:
    `python -c "import tkinter as tk,tkinter.font as f; r=tk.Tk(); print(f.Font(family='Segoe UI',size=11).measure('0'), f.Font(family='Consolas',size=9).measure('0'))"`

======================================================================
2. NEW DEFECTS NOT IN THE USER LIST
======================================================================
- [C-N01] Translation locks are dropped when switching files | Severity: P1 | Status: [CONFIRMED statically; runtime NEEDS-VERIFY]
  - Location: misora.py `_locked_boxes` is a single Set[int] of box indices (1268); open_file clears it on every document switch (6629) and nothing restores it
    (all references: 1268, 6629, 6781, 7812, 8431, 8441–8445, 10696). Also not in prefs/session (1706).
- Impact: boxes the user locked to protect proofread text become unprotected after A->B->A navigation or restart; batch MTL / paste / replace (design invariant D8) can overwrite them silently.
- Fix direction: per-document lock set stored in open_documents[path], restored on switch; included in the future .misora (U-B17).

- [C-N02] Raw View accepts typing but silently discards it | Severity: P2 | Status: [CONFIRMED]
  - Location: txt_raw (4689–4703) is a normal editable tk.Text with no bindings or state toggle; _update_raw_view (6816–6846) deletes and rewrites the whole content on every refresh.
  - Same root as U-B31: an edit affordance without a commit path.

- [C-N03] Tooltips missing on ribbon controls | Severity: P2 | Status: [CONFIRMED]
  - AGENTS §21 requires tooltips for icon-only controls. Currently without tooltip: Ruby (4085), "[-]" (4105), player (4125), B/I/U/S/Sub/Sup (4156–4178), Preview (4245), Continuous/Select Box.
    U-B5 (icon-only player) and the new toggle icons make this mandatory.

- [C-N04] Misleading success toast for a no-op toggle (see C-B08 line 7116). Merge into C-B08 scope.

======================================================================
3. FEATURE / ARCHITECTURE ITEMS — U-B9, B15–B20, B27, B28, B31–B34 (FEASIBILITY, RISKS, CODE ANCHORS)
======================================================================
- [C-F01] U-B15 Left dock -> openable drawer | FEAT
  - Anchor: left dock is a PanedWindow pane (3557–3558); a collapse already exists (_toggle_dock_collapse 9791: sash to 36 px; pin button 3586). Right side drawer already exists as a pane (_build_side_drawer 5221–5271, tabs Customize/Glossary).
  - Consequence: pane drawers still consume editor width when open; overlay drawers (place()) avoid that but need focus/Esc/click-away handling. Interacts with U-B14 (small windows).

- [C-F02] U-B16 Empty state with big "Open files" button + drop hint | FEAT
  - Anchor: today the empty app shows blank panels plus a status-bar text only (headless screenshot). _refresh_opened_files_list (9816) renders nothing for 0 docs.
    DnD exists (_init_drag_and_drop 2257, _handle_dropped_paths 2533) and can be reused. Safe, low risk.

- [C-F03] U-B19 Double-click on the "Opened Files" tab = Open | FEAT | [CONFIRMED absent]: btn_tab_files (3575–3584) has only command=_switch_dock_tab. Add <Double-Button-1> -> on_open_file.

- [C-F04] U-B20 Open dialog cannot multi-select | BUG | [CONFIRMED]: on_open_file uses filedialog.askopenfilename (9036). askopenfilenames is the fix.
  - Risk/Measure-First: open_file (6495–6669) flushes, rebuilds views and saves prefs per file; N files => N full _update_views passes. Open all then activate once.

- [C-F05] U-B17/B18 .misora project file + overwrite-diff window | FEAT
  - Anchors: session restore exists but stores paths only (prefs saved_opened_files / saved_active_file, 1706–1707; restore loop 1376–1390); no ".misora" code exists. Unsaved edits are not persisted anywhere.
  - Design questions: what is stored (file list, active file+box, view mode, scope settings, locks [see C-N01], search query, dock state) vs NOT stored (document bytes/dirty edits);
    atomic write (AGENTS §9/§23 style), relative vs absolute paths, schema version, missing-file policy.
- U-B18 overwrite warning: open-project while another project is dirty => Save/Discard/Cancel (AGENTS §16 pattern). The "difference mapping window" should be bounded to a simple
    list diff (added/removed/dirty files, active file) to avoid over-engineering.

- [C-F06] U-B27/B28 Preview toggle renders game-like boxes (page + continuous) | FEAT | RISK: scope + assets
  - Anchor: current "Preview" (_on_toggle_preview_compiled 5035–5045, _insert_compiled_ngui_text 5083+) is a read-only compiled-NGUI-tag view inside the same Text widget.
  - Reference audit: images/AtlasAdv [48D3C5B6AD].png (2048x2048, top half transparent) is a game UI sprite atlas (white speech-bubble frames, 5 coloured name plates, END marker, menu icons).
    It carries NO sprite rectangles; those live in the NGUI atlas asset [NEEDS-VERIFY; manifest atlasngui2_assetmanifest exists in tools/].
- Constraints: PROTOCOL §4 and images/README: screenshots/assets are references, not a mandate for an emulator. Bundling Cygames art in an MIT repo is a legal/scope question (README already notes Cygames trademarks).
- Direction for debate: draw a lightweight frame with Tk primitives (rounded rect, border, name plate, N-digit width from U-B26 calibration) rather than shipping/slicing game art; continuous variant = per-card frames
    matching images/…02-28-27-995.jpg ("Full Story Script Display": name plate + 3 lines).
- Capacity differs per game surface: main box 3x50 digits; Summary dialog (…02-28-20-144.jpg) is ~5 lines and visibly different width; log view ~3 lines. One global constant (45 or 50) cannot be right;
    a small per-surface profile (Dialogue / Summary / Log) fits Box 0 metadata too. Exact digits-per-line for Summary/Log are [NEEDS-VERIFY] (user can count with the test strings).

- [C-F07] U-B31 Editable Raw View with confirm/parse/revert | FEAT | RISK: integrity
  - Anchors: display format `[idx] name 'a'  'b'` (6835) is NOT losslessly parseable (args containing "'" or double spaces, empty args).
    A lossless codec already exists: Record.render_v2 (story_ast.py:185) / StoryDocument.from_v2_text (735–780) / escape_arg+unescape_arg (124–141).
- Gaps: from_v2_text builds NEW Record objects with new uids (AGENTS §4 identity rules); undo_journal has no "records replaced" delta (classes: BoxEditDelta, BoxStructuralDelta, PlainTextDelta, BulkFileDelta, MetadataDelta);
    AGENTS §8 says do not claim v2 lossless until round-trip tests pass.
- Direction: edit buffer in v2 syntax, parse into a candidate doc, validate (known/numeric cmd ids, arity, to_binary round-trip, box count), show Yes/No diff, commit as ONE undoable operation; any parse error => revert with message.
    Open: scope = active box's records only or whole document?

- [C-F08] U-B9/B32/B33 MTL as right drawer; per-engine stacked results; per-box refresh/apply; All-Script mode shows one engine across boxes | FEAT
  - Anchors: today MTL = floating TranslatorAssistantDialog (11558), plus MTLSettingsDialog (11211), BatchTranslateDialog (11881); engines in core/mtl_engine.py (355 lines); existing right drawer is a PanedWindow pane.
  - Risks: (1) AGENTS §24/§15: workers must not touch Tk — results via main-thread queue; (2) cost/quota: "refresh all" x engines x boxes = N*M API calls (DeepL character quota) -> needs confirm + cache + per-engine concurrency cap;
    (3) TagMasker must wrap every call (core/ngui_tags.py:116+); (4) editable result boxes must commit via the shared _commit_widget_edit/undo path (AGENTS §11); (5) Translation Lock (D8) must be honoured by Apply.
- Prerequisite: AGENTS §24 amendment (N-02).

- [C-F09] U-B34 Import from XUAT with duplicate/untranslated resolution window | FEAT
  - Anchors: XUnitySyncManager.preview_matches(japanese_key, roots) (core/xunity_sync.py:89–140) rglobs and re-reads EVERY *.txt per single key; conflict flag is_conflict (30, 137) marks 2nd+ distinct values only.
    Format rules D14/AGENTS §10 (one key=value per line, escaped \n, immutable JP keys per Box uid, preview duplicates).
- Direction: build ONE index norm_key -> [(file, line, value)] per import run; dialog modelled on ScriptPastePreviewDialog/all-script view with a per-box choice among candidates;
    untranslated = missing key or value == key [NEEDS-VERIFY convention]. Reuse the dark-theme Treeview fix from C-B07 or use Text/Canvas rows.

======================================================================
4. EFFICIENCY, PERFORMANCE & HYGIENE OBSERVATIONS
======================================================================
- [C-E01] Select Box toggle re-renders the entire continuous stream (7109–7114 -> _render_continuous_view 7657+; one Frame+gutter Text+Text+labels per box) | Measure-First: Yes | [NEEDS-VERIFY]
  - 142-box files exist in the user's workflow (README); measure card build time before any virtualization (PROTOCOL §4).
- [C-E02] open_file per file inside a multi-open loop (see C-F04) | Measure-First: Yes | [NEEDS-VERIFY].
- [C-E03] preview_matches is O(files x keys) when used for bulk import (see C-F09) | Measure-First: No (design the index up-front).
- [C-E04] Hygiene: README Project Structure lists docs/ (ANTIGRAVITY_PROMPTS.md, SCRIPT_FORMAT.md) and test names that do not exist in HEAD (test_s8b2_memory_leak_guards, test_s8b3_keyboard_shortcuts);
  PROJECT_STATE §9 claims docs/ is tracked, but `git ls-files` at 1924487 has no docs/. Either push docs/ or correct both documents.

======================================================================
5. FEATURE & UX IDEAS (SCOPED)
======================================================================
- [C-X01] Toolbar re-layout (answers U-B3/B5/B13/B14 together): Row A = speaker group (speaker, dropdown, pin, lock, player-icon, voice cue); Row B = NGUI group (Color, Grad, picker, Ruby, B/I/U/S/Sub/Sup, Size, Undo/Redo);
  Row C/compact = view group (All Script, Select Box, Preview) + text/box actions. Each row wraps or collapses via View > Toggle <group>. Uses grid, not pack order.
- [C-X02] Single "measure" module for width: one helper returns digit_px, text_left offset and display-line counts; ruler, overflow tag, card header counts and preview frame all consume it (prevents the current 4-way divergence).
- [C-X03] Rename proposal for U-B30: titles "Dialogue" (page) / "All Script" (stream); keep "Raw Script" as the technical pane. All names remain open for user debate.

======================================================================
6. REFERENCE TOOLS / VISUAL ASSETS AUDIT
======================================================================
- [C-R01] images/bandicam 2026-11-22 02-28-14-200.jpg — in-game dialogue box: 3 lines x 50 digits fit; menu panel buttons (Log, Skip, Script, Auto, Bookmark, Fast-forward, Hidden, Speed). Source of the 50-digit calibration.
- [C-R02] …02-28-20-144.jpg — Summary dialog (title + ~5 digit lines + "Skip this story?"): relevant to Box 0 summary editing; line width appears different from the dialogue box.
- [C-R03] …02-28-27-995.jpg — "Full Story Script Display": name plate + 3 lines per entry; the target look for U-B28.
- [C-R04] …2026-11-23 12-02-06-049.jpg / 12-02-21-785.jpg — Misora Page and Continuous views showing the ruler mismatch and the false "Overflow" at 50 digits.
- [C-R05] images/AtlasAdv [48D3C5B6AD].png — 2048x2048 NGUI atlas; see C-F06 (no sprite rects, art-licensing risk, do not turn into an emulator).
- [C-R06] tools/priconne-adv-tools/misora/ is an OLD copy of Misora (misora.py, core/ without ngui_tags/script_codec/security/text_encoding). Treat as stale; never port from it.
  tools/…/output/9080155.unity3d (7,300 bytes, 22 boxes) opens correctly in the current build and is a handy test fixture. Manifests/NewDataMiner are out of scope for B1–B34.

======================================================================
7. OPEN QUESTIONS FOR PHASE 2 DEBATE
======================================================================
 For the Project Lead:
1. Which theme was active when U-B10 happened (light vs a dark preset)? On Windows, is the Treeview empty in every dark preset?
2. U-B3 vs U-B5: is U-B3 the same player button, or a different control?
3. U-B25/26: should the capacity be 50 digit-widths x 3 lines for Dialogue only, or also per-surface profiles (Summary, Log)? Can you count digits per line for the Summary dialog and Log view?
4. U-B22: remove the counter entirely (your proposal) or replace it with a pixel-accurate overflow indicator? The per-card "(N chars)" label shares the same flaw.
5. U-B27/28: may the preview be drawn with Tk primitives (no bundled game art), or do you require the real atlas sprites (needs atlas metadata + licensing decision)?
6. U-B29: in page view what does "Select Box" mean — a range selector / checklist of all boxes, or a checkbox per currently shown box?
7. U-B31: Raw edit scope = active box records or the whole document? Is a diff in the confirm dialog required?
8. U-B17/18: should .misora ever contain unsaved edits, or only references + view state?
9. U-B9/B32: do you approve amending AGENTS §24 (MTL drawer) and PROJECT_STATE non-goals?
 For peer AIs:
10. Verify C-B15's ratio on Windows (probe in C-B15) and confirm Tk Text `width` uses the "0" glyph width.
11. Verify C-N01 at runtime (lock box -> open another file -> return).
12. Propose the safest undo representation for a whole-record-list replacement (U-B31) given AGENTS §4/§13.
13. Is an overlay drawer (place()) or a pane drawer preferable for U-B15 given the h_paned minsize constraints?

PHASE 1 STATUS: COMPLETE

