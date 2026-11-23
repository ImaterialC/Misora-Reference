ini adalah dari claude
```
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
```

this is gpt
```
# MISORA-EDITOR — PHASE 1 INDEPENDENT RESEARCH DOSSIER

Reviewer: OpenAI GPT-6
Date: 2026-11-23

Inspected Baseline:
- Misora-Editor: 1.4.0
- Commit: 1924487f28c9da3b5ede399fd69f24a23e547527
- Reference: Misora-Reference
- Commit: 931bbd061950c5939d95186986aaed69cdd464f4
- Branch: main

Reference Files Inspected:
- PROTOCOL.md
- ANTIGRAVITY_GUIDE.md
- All six files under phases/
- AGENTS.md
- PROJECT_STATE.md
- README.md
- All 12 core Python modules
- All 3 assets Python modules
- All 24 target repository test files
- All 136 files under Misora-Reference/tools/ were inventoried and retrieved during Phase 0.
- Targeted Phase 1 inspection included NewDataMiner, asset_registry.py, advscript.py, advverify.py, xuat2raw.py, raw2xuat.py, and the bundled legacy Misora copy.
- Five image files under images/ were visually inspected.
- AtlasAdv [48D3C5B6AD].png was intentionally excluded from visual inspection with explicit Project Lead permission.
- Three bundled Misora splash images were also visually inspected.

Verification Limitations:
- GitHub source and repository trees were accessible.
- Main application source was retrieved completely.
- No local Windows execution environment was available.
- No unit tests or compileall commands were executed independently.
- The 234/234 test result is recorded in PROJECT_STATE.md, not independently reproduced by this reviewer.

======================================================================
1. BUGS & DEFECTS (EVIDENCE-BASED)
======================================================================

- [GPT-B01] Truncated Binary ADV Records Are Silently Accepted
  | Severity: P1
  | Status: [CONFIRMED]

  Location:
  core/story_ast.py -> StoryDocument.from_binary()
  Lines 669-697

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/core/story_ast.py#L669-L697

  Problem:
  The binary parser uses `break` when encountering incomplete record
  headers, incomplete argument length fields, or argument payloads
  extending beyond the available input.

  It does not raise a parsing exception.

  After breaking out of the inner argument loop, the parser can still
  append a Record containing incomplete or missing arguments.

  The outer parsing loop can then interpret leftover bytes as another
  command.

  Impact:
- A corrupted or truncated Unity3D story payload may appear to load.
- The editor can present an incomplete StoryDocument without an
    explicit corruption warning.
- Saving the reconstructed document may discard original trailing
    binary data or serialize fabricated command boundaries.
- Potential irreversible story data loss.

  Proposed Fix Direction:
  Validate every record header, argument length field, argument payload,
  and terminating zero-length argument marker.

  Reject incomplete records with a descriptive BundleIOError instead
  of returning a partially parsed StoryDocument.

  Add malformed-input tests covering:
- One-byte trailing command ID.
- Incomplete 4-byte argument length.
- Argument length exceeding available bytes.
- Truncated final record after several valid records.


- [GPT-B02] Legacy Command ID Zero Remapping Still Exists
  | Severity: P1
  | Status: [CONFIRMED]

  Location:
  core/story_ast.py -> StoryDocument.to_binary()
  Lines 699-712

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/core/story_ast.py#L699-L712

  Problem:
  The current implementation still contains:

      if cid == 0 and r.cmd_name != "fade" and r.cmd_name in _INV_CMD_MAP:
          cid = _INV_CMD_MAP[r.cmd_name]

  This means a Record with numeric command ID 0 and a non-fade
  recognized command name can be silently serialized using another
  numeric command ID.

  For example, the inverse command map associates "title" with 30.
  A Record(cmd_id=0, cmd_name="title") would therefore be serialized
  with command ID 30.

  This contradicts the explicit AGENTS.md Rule 8 requirement that
  numeric command IDs be preserved.

  It also contradicts PROJECT_STATE.md, which marks CMD0-SPECIAL-CASE
  as RESOLVED and claims the special case was removed.

  Existing test coverage is insufficient:
- test_03_binary_roundtrip uses command ID 0 with cmd_name="fade".
- test_16_v2_roundtrip_lossless does not exercise command ID 0 with
    another recognized command name.

  Impact:
- Command identity may change during serialization.
- Binary round-trip fidelity can be violated.
- Unusual imported or constructed command records may be rewritten
    into different commands.

  Proposed Fix Direction:
  Remove the legacy remapping branch and preserve the original
  numeric command ID except for explicitly documented structural
  conversions such as the narration representation.

  Add a regression test for command ID zero with a non-fade name.


- [GPT-B03] Asynchronous Translation Can Modify the Wrong Document
  | Severity: P1
  | Status: [CONFIRMED]

  Location:
  misora.py -> MisoraApp.on_translate_current_box()
  Lines 10501-10561

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/misora.py#L10501-L10561

  Problem:
  The translation request captures:
- The active box index.
- The original text.
- The engine name.

  However, the completion callback does not capture or validate:
- The original document identity.
- The original file path.
- The original Box UID.

  When the asynchronous result arrives, update_ui() accesses:

      self.current_doc
      self.current_doc.boxes[b_idx]
      self.current_file_path

  These values refer to whichever document is currently active when
  the callback executes, not necessarily the document from which the
  translation was requested.

  Reproduction path:
1. Open story A.
2. Start translation on Box 3.
3. Allow the network request to remain pending.
4. Switch to story B.
5. Receive the translation response.

  The callback may write story A's translated text into Box 3 of
  story B if that index exists.

  Impact:
- Cross-document data corruption.
- Incorrect undo history.
- Wrong file marked dirty.
- Translation silently applied to unrelated dialogue.

  Proposed Fix Direction:
  Capture immutable request identity:
- Original file path/document identity.
- Original Box UID.
- Original box index.
- Original source text.

  Before applying the result, verify that the same document and box
  remain active and unchanged.

  Discard stale results instead of applying them to another document.


- [GPT-B04] Sparse CSIF Import Uses Inconsistent Target Indices
  | Severity: P1
  | Status: [CONFIRMED]

  Location:
  misora.py -> MisoraApp._show_paste_preview_and_apply()
  Lines 10602-10756

  core/script_codec.py -> apply_to_document()
  Lines 442-505

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/misora.py#L10602-L10756

  https://github.com/ImaterialC/Misora-Editor/blob/main/core/script_codec.py#L442-L505

  Problem:
  The UI integration treats imported blocks as contiguous relative
  to the current box index.

  It calculates:

      b_idx = start_idx + k

  It also records undo deltas against those contiguous indices.

  However, apply_to_document() handles sparse CSIF blocks differently:

      box_idx = b.index - 1

  Sparse indices are absolute 1-based document addresses.

  Consequently, when a sparse CSIF payload is imported while the
  active box index is not zero:

- Preview may show different target boxes from those actually edited.
- Undo deltas may reference different boxes from the boxes modified.
- _modified_boxes may track the wrong box indices.
- Undo/redo can restore unrelated content.

  Reproduction example:
  A document contains 10 boxes.

  The active box is Box 6.

  Incoming sparse CSIF contains:
      @@#1|Kokkoro
      Translation A
      @@#3|Pecorine
      Translation B

  The codec applies to Box 1 and Box 3.

  The UI integration builds undo entries and preview targets based on
  Box 6 and Box 7.

  Impact:
- Incorrect target preview.
- Incorrect undo history.
- Potential corruption of unrelated dialogue during undo/redo.

  Proposed Fix Direction:
  Choose and enforce a single sparse-addressing contract.

  Since AGENTS.md specifies 1-based document addressing, the UI must:
- Preview the actual absolute target indices.
- Validate all sparse indices before recording any undo delta.
- Record deltas against b.index - 1.
- Update _modified_boxes using actual target indices.

  Preserve contiguous cursor-relative behavior only for non-sparse
  imports.


- [GPT-B05] Sparse Import Can Partially Commit Metadata Before Validation
  | Severity: P1
  | Status: [CONFIRMED]

  Location:
  core/script_codec.py -> apply_to_document()
  Lines 442-485

  misora.py -> MisoraApp._show_paste_preview_and_apply()
  Lines 10694-10756

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/core/script_codec.py#L442-L485

  https://github.com/ImaterialC/Misora-Editor/blob/main/misora.py#L10694-L10756

  Problem:
  apply_to_document() applies metadata before validating sparse indices.

  The function executes:

      doc.set_metadata(...)

  before checking whether all sparse indices are within the document
  bounds.

  In the UI path, _show_paste_preview_and_apply() also applies and
  records metadata before calling apply_to_document().

  If an imported CSIF document contains metadata and an invalid sparse
  index, apply_to_document() raises an exception after metadata has
  already been modified.

  The surrounding UI handler ends the undo batch in finally but does
  not roll back the committed metadata mutation.

  Impact:
- Partial script import.
- Metadata may change while dialogue application fails.
- Dirty-state notification and view refresh are bypassed when the
    exception propagates.
- Document and undo state can become inconsistent.

  Proposed Fix Direction:
  Validate all sparse indices and all other rejection conditions before
  mutating metadata or dialogue.

  Make script application a true atomic operation:
  either all requested metadata/dialogue changes commit, or none do.


- [GPT-B06] Single-Box Translation Calls Tkinter From a Worker Thread
  | Severity: P1
  | Status: [CONFIRMED]

  Location:
  core/mtl_engine.py -> translate_async()
  Lines 337-355

  misora.py -> MisoraApp.on_translate_current_box()
  Lines 10522-10560

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/core/mtl_engine.py#L337-L355

  https://github.com/ImaterialC/Misora-Editor/blob/main/misora.py#L10522-L10560

  Problem:
  translate_async() executes on_success() and on_error() directly
  inside its background worker.

  The current single-box UI callbacks then invoke:

      self.after_idle(update_ui)
      self.after_idle(show_err)

  These are Tkinter calls originating from the worker thread.

  This violates AGENTS.md Rule 15:
  Workers must never call Tk methods.

  The BatchTranslateDialog already uses a queue-based completion
  architecture, but the single-box translation path still uses
  callback-based cross-thread interaction.

  Impact:
- Potential TclError or cross-thread execution failures.
- Unpredictable behavior during shutdown or widget destruction.
- UI thread-safety contract is inconsistent across translation
    workflows.

  Proposed Fix Direction:
  Use the same main-thread queue/polling pattern used by the batch
  translation workflow.

  Worker threads should return plain data only. All UI updates must
  occur from a main-thread queue consumer.


- [GPT-B07] Case-Sensitive Search Is Ignored During Whitespace-Insensitive Search
  | Severity: P2
  | Status: [CONFIRMED]

  Location:
  core/search_engine.py -> ProjectSearchEngine._compile_matcher()
  Lines 174-220

  core/story_ast.py -> norm_search()
  Lines 112-121

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/core/search_engine.py#L174-L220

  https://github.com/ImaterialC/Misora-Editor/blob/main/core/story_ast.py#L112-L121

  Problem:
  The whitespace-insensitive matcher uses norm_search().

  norm_search() always applies casefold().

  The whitespace matcher never checks options.match_case.

  Consequently, when:
- Match Case = enabled
- Ignore Whitespace = enabled
- Regex = disabled

  Search remains case-insensitive.

  The GUI does pass the Match Case setting into SearchOptions:

  misora.py -> on_start_search(), lines 8613-8625.

  Impact:
- Search results can include incorrect case variants.
- Search UI options do not accurately describe actual matching
    behavior.

  Proposed Fix Direction:
  Preserve case when match_case=True while applying whitespace and
  Unicode normalization.

  Add tests for combinations of:
- Match Case on/off.
- Ignore Whitespace on/off.
- Full-width and half-width Unicode input.


- [GPT-B08] Search Errors Are Silently Converted Into Zero Results
  | Severity: P2
  | Status: [CONFIRMED]

  Location:
  core/search_engine.py -> ProjectSearchEngine.search_file()
  Lines 250-375

  core/search_engine.py -> ProjectSearchEngine.search_directory()
  Lines 377-421

  misora.py -> MisoraApp._run_background_search()
  Lines 8714-8750

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/core/search_engine.py#L250-L421

  https://github.com/ImaterialC/Misora-Editor/blob/main/misora.py#L8714-L8750

  Problem:
  search_file() catches exceptions from bundle parsing and strict text
  decoding using broad except blocks, then returns an empty result list.

  search_directory() uses os.walk() without an onerror handler.

  As a consequence, inaccessible directories or unreadable files can
  disappear from results without a corresponding skipped-path record.

  _run_background_search() only records paths when search_file() or
  search_directory() raises an exception.

  Because the underlying search engine swallows many errors, the UI
  may report zero matches without accurately reporting what it failed
  to inspect.

  This violates AGENTS.md Rule 15:
  Report skipped/inaccessible paths instead of silently under-reporting
  results.

  Impact:
- False confidence in search completeness.
- Important translation files may be silently omitted.
- Users cannot distinguish zero matches from inaccessible files.

  Proposed Fix Direction:
  Return structured per-file errors or propagate errors to the
  background worker.

  Add an onerror handler for directory traversal.

  Present inaccessible/skipped paths in the search result summary.


- [GPT-B09] XUAT Conflict Preview Is Not Part of the Normal Save Path
  | Severity: P2
  | Status: [NEEDS-VERIFY]

  Location:
  core/xunity_sync.py -> XUnitySyncManager.preview_matches()
  and find_and_update()

  misora.py -> MisoraApp.on_save()
  Lines 8568-8595

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/core/xunity_sync.py#L90-L220

  https://github.com/ImaterialC/Misora-Editor/blob/main/misora.py#L8568-L8595

  Problem:
  preview_matches() identifies duplicate or conflicting existing
  translations.

  However, the ordinary save workflow calls find_and_update()
  directly without invoking preview_matches().

  find_and_update() updates every entry whose normalized Japanese
  key matches the requested key.

  If multiple dictionary entries share a normalized Japanese key but
  have different existing English translations, the ordinary save
  path can overwrite all of them without presenting the conflict
  preview.

  Whether this is intended global synchronization behavior or an
  unintended bypass of the conflict-review contract requires
  Project Lead confirmation.

  Proposed Fix Direction:
  Confirm the expected behavior for duplicated XUAT entries.

  If conflicts require human review, insert preview/confirmation
  before the actual write operation.


- [GPT-B10] Logger Flush Does Not Wait For An In-Flight Disk Write
  | Severity: P2
  | Status: [CONFIRMED]

  Location:
  core/logger.py -> AppLogger.flush()
  Lines 97-112

  core/logger.py -> AppLogger.clear_log_file()
  Lines 245-260

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/core/logger.py#L97-L112

  https://github.com/ImaterialC/Misora-Editor/blob/main/core/logger.py#L245-L260

  Problem:
  flush() waits only while Queue.empty() returns False.

  The writer thread removes an entry from the queue before writing it
  to disk.

  Therefore, Queue.empty() may become True while the writer is still
  processing an entry.

  clear_log_file() calls flush() and then truncates the log file.

  An entry already removed from the queue may consequently be written
  after the file has been cleared.

  Impact:
- Log clearing can leave stale entries behind.
- flush() does not reliably satisfy its documented completion
    guarantee.

  Proposed Fix Direction:
  Use Queue.join()/task_done() or an explicit writer completion
  barrier with a bounded timeout.


- [GPT-B11] Credential Encryption Silently Falls Back To Plaintext
  | Severity: P2
  | Status: [NEEDS-VERIFY]

  Location:
  core/security.py -> protect_secret()
  Lines 28-62

  core/mtl_engine.py -> MTLConfig.to_dict()
  Lines 50-74

  misora.py -> MisoraApp._save_user_prefs()
  Lines 1715-1729

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/core/security.py#L28-L62

  https://github.com/ImaterialC/Misora-Editor/blob/main/core/mtl_engine.py#L50-L74

  https://github.com/ImaterialC/Misora-Editor/blob/main/misora.py#L1715-L1729

  Problem:
  protect_secret() returns plaintext when:
- The application is not running on Windows.
- DPAPI is unavailable.
- CryptProtectData fails.

  _save_user_prefs() explicitly calls MTLConfig.to_dict(secure=True)
  and persists the returned values to misora_config.json.

  Therefore, DPAPI failure silently degrades to plaintext storage.

  This is conditional, but the fallback behavior is directly visible
  in source code.

  Impact:
  API credentials may be stored in ordinary configuration files
  without an explicit warning when credential encryption fails.

  Proposed Fix Direction:
  On supported Windows deployments, fail closed or explicitly warn
  the user before persisting credentials in plaintext.

  Never silently claim credentials are protected when DPAPI failed.


- [GPT-B12] Bundle Save Verification Does Not Compare Non-Target Assets
  | Severity: P1
  | Status: [NEEDS-VERIFY]

  Location:
  core/bundle_io.py -> save_bundle_story()
  Lines 145-268, especially 194-220

  Evidence:
  https://github.com/ImaterialC/Misora-Editor/blob/main/core/bundle_io.py#L145-L220

  Problem:
  AGENTS.md Rule 9 specifies verification of:
- Exact target TextAsset.
- Object count.
- Non-target bytes.
- Source fingerprint.

  The implementation verifies the target TextAsset bytes and object
  count but does not compare the other TextAsset/object bytes against
  their original values.

  Impact:
  If the repacker unexpectedly changes a non-target asset while
  preserving object count and target story bytes, the current
  verification gate may not detect it.

  Actual unintended non-target modification has not been demonstrated.

  Proposed Fix Direction:
  Implement non-target asset identity/content verification according
  to AGENTS.md Rule 9, or explicitly revise that invariant with
  evidence that packer="original" guarantees the required behavior.


======================================================================
2. EFFICIENCY, PERFORMANCE & CODE HYGIENE OBSERVATIONS
======================================================================

- [GPT-E01] Main GUI Module Has A Very Large Maintenance Surface
  | Measure-First: Yes
  | Status: [CONFIRMED]

  Location:
  misora.py

  Observation:
  The main GUI module currently contains approximately 12,144 lines
  and 543 KB of source code.

  Several application workflows remain coordinated directly in this
  single module.

  This is primarily a maintainability and review-surface concern,
  not proof of a runtime performance bottleneck.

  Recommendation:
  Avoid a broad architectural rewrite.

  Any future extraction of responsibilities should be incremental,
  dependency-aware, and justified by a concrete change or maintenance
  problem.


- [GPT-E02] Project State And Current Repository Tree Disagree About docs/
  | Measure-First: No
  | Status: [CONFIRMED]

  Location:
  PROJECT_STATE.md -> GitHub Documentation Audit
  Lines 793-799

  README.md and current main repository tree.

  Observation:
  PROJECT_STATE.md claims that these files exist:

- docs/ANTIGRAVITY_PROMPTS.md
- docs/SCRIPT_FORMAT.md

  However, the currently inspected Misora-Editor main tree contains
  no docs/ directory.

  The documentation audit therefore appears stale or inconsistent
  with the current repository snapshot.

  Recommendation:
  Reconcile the documentation audit and actual repository tree.

  Do not assume those documentation files exist until they are
  restored or the ledger is corrected.


- [GPT-E03] Project State Has Contradictory Multi-TextAsset Status

  Location:
  PROJECT_STATE.md
  Lines 523 and 789-795

  Observation:
  The bug ledger marks MULTI-TEXTASSET-TARGET as RESOLVED.

  However, the remaining open questions still ask whether multiple
  story TextAssets exist in production Unity3D bundles.

  This leaves an unresolved distinction between:
- Selecting and locking an already selected target by path_id.
- Correctly identifying which story TextAsset should initially
    be selected when several candidates exist.

  Recommendation:
  Preserve this as an explicit verification question until actual
  production bundles establish the intended selection behavior.


- [GPT-E04] Recorded Test Baseline Is Not Independently Reproduced

  Location:
  PROJECT_STATE.md
  Lines 43-73 and 403

  Observation:
  PROJECT_STATE.md records 234/234 tests passing.

  This reviewer accessed the test sources but did not execute the
  suite in a local Windows/Python 3.12 environment.

  Recommendation:
  Keep the recorded 234/234 result as repository-reported evidence,
  not as an independently executed result from this reviewer.

  The next execution session should preserve actual command output,
  environment information, and test counts.


======================================================================
3. FEATURE & UX IMPROVEMENT IDEAS
======================================================================

- [GPT-F01] Visible Search Coverage And Error Summary

  User Value:
  Users searching large Priconne translation workspaces need to
  distinguish between:
- No matching translation.
- File could not be decoded.
- Bundle could not be parsed.
- Directory could not be accessed.
- Search was cancelled.

  Proposed Scope:
  Extend the existing search result summary to expose skipped paths
  and per-file errors.

  Guardrails:
  Reuse the existing search engine, queue, and result dock.
  Do not introduce another search framework.


- [GPT-F02] XUAT Conflict Review Before Dictionary Synchronization

  User Value:
  Translation projects may contain repeated normalized Japanese keys
  with different existing English translations.

  Proposed Scope:
  Reuse XUnitySyncManager.preview_matches() to show:
- Matching file and line.
- Existing translation.
- Proposed translation.
- Duplicate/conflict status.

  Allow the user to confirm the synchronization policy.

  Guardrails:
  Preserve existing Japanese source keys.
  Preserve BOM, newline style, key whitespace, and backups.
  Do not introduce a separate dictionary database.


- [GPT-F03] Explicit Story TextAsset Selection When Ambiguous

  User Value:
  Prevent the editor from silently choosing an unintended story
  payload when a Unity3D bundle contains multiple plausible
  TextAssets.

  Proposed Scope:
  Only introduce a selection step if production bundles demonstrate
  genuine ambiguity.

  The selection should display asset name and path_id.

  Guardrails:
  Keep the existing path_id-based save identity.
  Avoid mandatory extra dialogs for ordinary single-story bundles.


======================================================================
4. REFERENCE TOOLS / VISUAL ASSETS AUDIT
======================================================================

- [GPT-R01] NewDataMiner Download Integrity
  | Severity: P2 | Status: [CONFIRMED]

  Location:
  tools/priconne-adv-tools/NewDataMiner/downloader.py
  -> AssetDownloader.download_entry()
  Lines 25-61

  Observation:
  Existing files are considered reusable when their size matches
  the manifest size.

  The file hash is not checked.

  Newly downloaded content is written directly to the final path,
  and the received byte count is not validated against the expected
  manifest size before success is returned.

  A same-size corrupted local file can therefore be accepted as
  complete.

  An incomplete but normally terminated HTTP response can also
  leave an undersized final file without a successful integrity
  rejection.

  Recommendation:
  Before porting or reusing this downloader, establish integrity
  verification using expected size and manifest hash, preferably
  with temporary-file staging before promotion.


- [GPT-R02] NewDataMiner Database Activation Is Not Fully Atomic
  | Severity: P1 | Status: [CONFIRMED]

  Location:
  tools/priconne-adv-tools/NewDataMiner/db_updater.py
  -> DatabaseUpdater.download_and_apply_update()
  Lines 298-368, particularly 344-354

  Observation:
  After backup creation, the existing master.db is explicitly
  deleted before the staging file is renamed.

  If the subsequent rename fails, the active database path remains
  absent even though a backup exists.

  This contradicts the method's atomic-activation description.

  Recommendation:
  Preserve the original file until the replacement operation
  succeeds.

  Use an atomic replacement strategy and test failure between
  staging validation and activation.


- [GPT-R03] Bundled Misora Copy Is Not The Target Source Of Truth

  Location:
  tools/priconne-adv-tools/misora/

  Observation:
  The tools repository contains a standalone older Misora application
  copy, including its own:
- misora.py
- core/
- assets/
- tests/

  Its main GUI file differs from the current target repository
  misora.py in both file size and blob identity.

  Recommendation:
  Use the root ImaterialC/Misora-Editor repository as the authoritative
  source.

  Treat the bundled copy strictly as historical/reference material.
  Never merge its code into the target without independent review.


- [GPT-R04] Visual References Establish Existing UI Context

  Location:
  Misora-Reference/images/

  Observation:
  Five visually accessible screenshots show:
- Original game ADV interface and text display.
- Game Summary and Skip confirmation.
- Full Story Script Display.
- Misora Game Display / Page View.
- Misora Continuous Stream View with Raw Script View.

  The screenshots are consistent with the application's existing
  translation/editor workflow.

  Recommendation:
  Use these screenshots as contextual references for specific,
  user-requested UI discussions.

  Do not extrapolate them into an unrequested game replica,
  emulator, asset pipeline, or wholesale redesign.

  AtlasAdv [48D3C5B6AD].png was intentionally not inspected
  visually at the Project Lead's request.


======================================================================
5. OPEN QUESTIONS FOR PHASE 2 DEBATE
======================================================================

1. Command ID Preservation:
   The current to_binary() still contains the command ID zero
   remapping branch, while PROJECT_STATE.md marks the issue resolved.

   Is there any intentionally supported exception to AGENTS.md
   Rule 8, or should numeric command IDs always remain authoritative?

2. Sparse CSIF Semantics:
   Are sparse @@#N addresses always absolute 1-based document
   addresses, including when importing at a non-zero active box?

   The current codec, UI preview, and undo integration do not
   consistently implement the same addressing model.

3. Production Bundle Identification:
   Can the Project Lead supply or identify production bundles
   containing multiple plausible story TextAssets?

   What rule determines the intended story TextAsset when more than
   one candidate is present?

4. Binary Parser Strictness:
   Should malformed or truncated ADV binary files always be rejected
   during load rather than opened as partially reconstructed scripts?

5. MTL Request Lifecycle:
   Should a translation result be discarded when its originating
   document or box has changed while the request is pending?

6. XUAT Synchronization:
   Should duplicate dictionary keys with different existing
   translations always require preview/confirmation before an
   automatic synchronization?

7. Windows Release Verification:
   Have the Rule 29 manual Windows checks been completed against
   the exact current main commit?
   In particular:
- Copy Box round-trip.
- Paste Box in both views.
- Ctrl+H keyboard behavior.

8. Credential Failure Policy:
   If Windows DPAPI fails, should the application refuse to persist
   API keys in plaintext, or should a clearly disclosed fallback
   require explicit user consent?

9. Repository Documentation:
   Are docs/ANTIGRAVITY_PROMPTS.md and docs/SCRIPT_FORMAT.md
   intentionally absent from the current main repository, or should
   PROJECT_STATE.md's documentation audit be reconciled?


======================================================================
PHASE 1 STATUS: COMPLETE
======================================================================
```

dan ini adalah temuan saya
``
bug yang sekarang saya temukan antara lain:
B1. text box find dan replace tidak sejajar.
B2. 4 button find in files, cancel, replace, replace all tidak sejajar.
B4. tombol [-] pada ribon group ngui dihapus karena tidak berguna dan redundant dengan fungsi tombol warna yang sudah sepaket dengan [-]
B5 tombol icon player{0} diganti menjadi cuma icon player .
B6 toggle continous view diganti menjadi toggle all script (melihat seluruh box dialog berurutan dari atas kebawah)
B7. toggle untuk select box, all script (continous view) belum memiliki icon
B8 memindahkan tombol preview bareng dengan tombol continous view dan select box dan menjadikan nya 1 grup
B9. permintaan untuk membuat tombol mtl menjadi drawer tidak dilakukan.
B10. float windows paste import script preview tidak terlihat apa apa.
B11. select box cuma muncul saat continous view aktif.
B12. icon gembok berada di sebelah kanan check box select box
B13. tombol player keluar dari group ngui
B14. tambahkan di main menu view>toggle ribbon ngui> tombol2 ngui di hilangkan,
temuan ini terjadi karena dalam tampilan kecil saat snap, banyak tombol dan fungsi di sebelah kiri hilang/tertutup, sedangkan untuk view lemabr kerja text dan box sudah berlebih
B15. rubah windows search result dan opened files menjadi drawer yang bisa di buka
B16. default untuk pertama kali dibuka atau saat opened files kosong adalah tombol besar ditengah "open files" dan di bawah ada deskripsi, drag and drop unity3d story data  disini atau save lembar kerja .misora.
B17. save project, kemampuan untuk menyimpan sesi pekerjaan dan dilanjutkan nanti dalam bentuk file .misora
B18 saat membuka save project padahal ada project lain akan ada prompt untuk menyimpan project lama, atau ditimpa, berikan warning jika ditimpa maka pekerjaan lama akan hilang, buat windows untuk memetakan perbedaan project yang akan ditimpa.

File .misora hanya menyimpan daftar referensi file yang terbuka, file & box aktif, mode tampilan, status gembok per box.uid, dan pengaturan scope—bukan isi biner editan yang belum disimpan (editan tetap disimpan ke file .unity3d/.txt asli lewat prompt Save / Discard / Cancel standar agar tidak tercipta dua versi file yang saling bentrok). Jendela diff (B18) cukup berupa tabel ringkas: file yang ada di sesi lama vs sesi baru + penanda file mana yang masih dirty.

B19 tab opened files jika dipencet 2 kali fungsinya sama dengan open file
B20 tombol open files tidak bisa memilih lebih dari 1 file.
B21. ketika select current files text box directori dihapus
B22. perhitungan characters tidak tepat, perhatikan juga bahwa karakter latin dan jepang beda ukuran, usulan saya adalah dihapus, karena sudah ada vertical rules dan horisontal rules,
B23 berikan warna merah pada rules horisontal 60 dan seterusnya
B24 berikan warna merah pada line 4 dan seterusnya pada vertikal
B25 highlight ketika ada  horisontal 60 ditembus. perhatikan bahwa ukuran font jepang dan latin berbeda.
B26 angka pada rules menyesatkan B23 dan B26 menyebut angka 60 yang sejatinya adalah 50 jika berdasarkan  jumlah karakter. mungkin ini diakibatkan bedanya font pada box kerja dan rules perhatikan refrensi gambat ini
https://github.com/ImaterialC/Misora-Reference/blob/main/references/assets/bandicam%202026-11-23%2012-02-06-049.jpg
https://github.com/ImaterialC/Misora-Reference/blob/main/references/assets/bandicam%202026-11-23%2012-02-21-785.jpg

B27 toggle preview membuat tampilan box identik dengan game mengacu pada gambar di bawah dan juga asset game dibawah ini
https://github.com/ImaterialC/Misora-Reference/blob/main/references/assets/bandicam%202026-11-22%2002-28-14-200.jpg
https://github.com/ImaterialC/Misora-Reference/blob/main/references/assets/AtlasAdv%20[48D3C5B6AD].png
B28 toggle preview pada continous mode membuat tampilan box identik dengan game mengacu pada gambar di bawah
https://github.com/ImaterialC/Misora-Reference/blob/main/references/assets/bandicam%202026-11-22%2002-28-27-995.jpg
pakai gambar primitif kode Tkinter (tanpa memasukkan file gambar AtlasAdv Cygames ke repo MIT), serta apakah batas kapasitas hanya untuk Dialogue (50×3) dulu atau sekalian Box 0 Summary (berapa digit × baris pada screenshot Summary)?

B29 toggle select box juga berfungsi pada tampilan Game view (clean dialogue)
di header atas (jadi kamu bisa lompat-lompat box lalu centang mana yang mau di-copy/cut)
B30 ubah nama yang membingungkan Game view (XXX) Nama ini dibuat sebagai lawan dari raw view di window bawah.
B31 kemampuan untuk bisa meng edit raw view, tapi saat meng edit akan ada warning box sebelum di commit di tampilan ketika menekan yes, akan di parser sebagai edited files dan tampilan refresh sesuai yang di edit di raw, tapi jika parser gagal misalnya karena yang di edit bukan string text maka akan revert atau batal.


B32 windows mtl di rombak total, windows mtl di pindah di drawer kanan, disana berbagai macam pilihan mtl disusun dari atas kebawah dari berbagai MTL yang ada.
box dari translate bisa di edit, tombol refresh dengan icon refresh di tiap box agar bisa di translate ulang, tombol apply dengan icon panah ke kanan untuk menerapkan terjemahan. terdapat refresh semuanya
Di drawer kanan, pengguna mencentang mesin mana saja yang ingin ditampilkan berurutan dari atas ke bawah (mencegah token user hangus)Tiap kartu mesin bisa diedit, punya tombol ↻ (Refresh) & → (Apply, hormati gembok). Tombol Refresh All hanya menyegarkan mesin yang dicentang + minta konfirmasi jika ada mesin berbayar + memakai cache sesi.

B33 untuk tampilan alls script tampilan mtl drawer berubah bukan menampilkan berbagai mtl tiap box melainkan menampilkan terjemahan tiap box pada mtl yang di pilih di atas.
B34 kemampuan untuk import from xuat. problematikanya adalah ada beberapa terjemahan ganda, dan ada yang belum diterjemahkan, oleh karena itu akan muncul floating windows untuk memilah milah terjemahan apa saja yang akan di terapkan, tampilannya mirip dengan all script view.

Disklaimer, semua penamaan dan konsep visual masih tentatif dan boleh diusulkan ulang, kalian bebas membantah usulan saya dan merevisi ulang atas usulan saya.
```