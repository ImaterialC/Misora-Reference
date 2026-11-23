# MISORA-EDITOR — PHASE 2 DEBATE & CROSS-CHECK (ROUND 1 — CLAUDE)

Reviewer: Claude
Responding To: Gemini R1 (Phase_1R1_gemini.md); GPT Phase 1; Grok Phase 1; Claude Phase 1 (filed as Phase_1_Gemini.md); Project Lead manual findings B1..B34 (Phase_1_User_found.md)
Baseline Verified: NOT PINNED. HEAD hash unreadable to me (commits page blocked by robots). Peers cite 1924487f28c9da3b5ede399fd69f24a23e547527; I did not confirm it. PROJECT_STATE says "last updated 2026-11-22" yet records 2026-11-23 sessions, so the repo is moving. Re-pin before Phase 2.5.

======================================================================
0. VERIFICATION SCOPE (PROTOCOL §3.3 DECLARATION)
======================================================================
READ IN FULL: PROTOCOL.md; phases/PHASE_2_DEBATE_SYNTHESIS.md; ANTIGRAVITY_GUIDE.md; all four Phase 1 files; Phase_1R1_gemini.md; Misora-Editor root page (README + file tree); AGENTS.md (161 lines); PROJECT_STATE.md (798 lines).
NOT READ (robots-blocked tree pages, un-fetchable raw URLs, rate limit): misora.py, core/*.py, assets/*.py, tests/*, Misora-Reference tools/ and images/ (known to me only via peer reports).
CONSEQUENCE: I issue NO code-level [AGREE — CONFIRMED] this round. Code claims are [NEEDS-VERIFY]. Facts I read myself in AGENTS/PROJECT_STATE/README/file tree are tagged [CONFIRMED-DOC].
LEGEND (my additions, plausibility markers only):
- DOC-OK: the claim's mechanism, or the invariant it says is broken, is stated in AGENTS/PROJECT_STATE/README. NOT a code check.
- LEDGER-CONFLICT: claim contradicts a PROJECT_STATE entry marked RESOLVED. Treat that RESOLVED as unverified until lines settle it.
- NO VERDICT YET: waiting for file:lines from a peer with source access.

======================================================================
1. VERDICTS ON PEER FINDINGS & USER MANUAL INPUTS
======================================================================

--- 1A. RECORD / PROCESS ITEMS ---
- [REC-01] Verdict: [CONFIRMED-DOC] Phase_1_Gemini.md is Claude's dossier (header "Reviewer: Claude", C-xx IDs). Gemini's own Phase 1 dossier is absent from the record; GEM items exist only as summarized in Gemini R1 section 3, without line ranges.
  * Required: Project Lead supplies/renames the file; Gemini adds file:line ranges to every GEM-B item (PROTOCOL §3.2).
- [REC-02] Gemini R1 answers Claude and GPT only. Grok-B01..B07, E01..E03, F01..F03 have had no cross-check. Verdicts for them are in 1F.
- [REC-03] Most R1 verdicts are bare "AGREE — CONFIRMED" without the file/line evidence the Phase 2 template requires. I count them as one-source evidence until a second AI checks the same lines.
- [REC-04] Gemini R1 attributes to the Project Lead points absent from Phase_1_User_found.md: (a) .misora preserves ALL unsaved edits as drafts; (b) Project Lead suggests "Raw File"/"Raw" for the bottom pane; (c) U-B34 details (3-tier conflict scope, no conflict_manager, no global auto-pruning, core/xuat_index.py); (d) native engine does not auto-shrink and text bleeds past the box. They may come from chat clarifications I cannot see. Until confirmed: (a)(b)(c) are proposals; (d) is a domain claim to reconcile with PROJECT_STATE §8.1 (see CLAUDE-N03).

--- 1B. PROJECT LEAD ITEMS (B3 is absent from the file; Gemini merged it into B5) ---
- [B1, B2] Verdict: [AGREE — CONFIRMED] by Project Lead manual test; Claude Phase 1 runtime probe measured entry offset 7 px / width 15 px and unequal button sizes.
  * LEDGER-CONFLICT: FIND-REPLACE-UI-ASYMMETRY is RESOLVED in the "P0 (new)" table and again under Phase 3 and Phase 5 deliverables (function named _build_search_panel; Claude measured _build_search_bar).
  * Required Refinement: acceptance must be geometric (equal winfo_rootx/winfo_width for both entries; equal width/height for the four buttons). Three earlier "resolved" claims had no geometric assertion.
- [B4] [AGREE]. Keep "[-]" in the NGUI glossary (Phase 4 "remove redundant ribbon buttons" missed this one). User loses "end colour at arbitrary caret without wrapping" from the ribbon; acceptable per Project Lead.
- [B5, B13 (+B3)] [AGREE]. Icon-only player button, moved out of the NGUI group. AGENTS §21: tooltip AND text fallback required. S8b-4's tooltip/fallback audit list does not include btn_dash/btn_player/ruby/B-I-U-S-Sub-Sup (consistent with C-N03).
- [B6, B7, B8, B30] [AGREE] on one VIEW group (Select Box, All Script, Preview) and header names Dialogue / All Script / Dialogue Preview / All Script Preview.
  * Bottom pane: [PARTIALLY AGREE] with Gemini that "Raw Script" collides with "All Script". I RETRACT Claude C-X03. Proposal: "Raw Commands" (content is ADV command records). Project Lead's call.
  * Required: rename sweep covers README shortcut table (Ctrl+Alt+C "Continuous View"), View menu, tooltips, AGENTS wording; keep internal identifiers (var_continuous_view) to avoid test churn.
- [B9] [AGREE in principle], gated: see B32/B33 and DEP-6.
- [B10] [AGREE — CONFIRMED] mechanism by Claude runtime probe (Treeview white-on-white on "Midnight Violet"); violates AGENTS §21. Project Lead theme/Windows repro still unconfirmed.
  * Required: style Treeview/Treeview.Heading from theme in _apply_styles; per-preset contrast test.
- [B11, B29] [AGREE]. Header checkbox in Dialogue view per B29; fix the misleading "Select Box mode enabled" toast.
  * LEDGER-CONFLICT: BOX0-NO-SELECT-CHECKBOX is RESOLVED, yet Gemini says the Box 0 checkbox is missing in All Script. NEEDS-VERIFY.
- [B12] [AGREE]. Reserve a fixed slot for the lock icon so headers do not shift when Select Box toggles.
- [B14] [AGREE]. Mechanism DOC-OK: S8b-4 sets h_paned minsize left>=160, right>=420, side_drawer>=260, so the editor pane can legitimately be ~420 px while ribbons need far more. Fix via grid/wrap or collapsible groups plus View > Toggle NGUI Ribbon.
  * Required: acceptance by measured visibility at fixed widths, not visual review.
- [B15] [PARTIALLY AGREE]. Prefer extending the existing pane collapse (S8b-4: _toggle_dock_collapse, _dock_collapsed, minsize swap) over a new place() overlay. Agrees with Gemini; refines Claude C-F01.
- [B16] [AGREE]. Reuse existing DnD handlers.
- [B17, B18] [PARTIALLY AGREE].
  * v1 per Project Lead's written text: references + state only (open-file list, active file/box, view mode, scope settings, locks). Unsaved edits stay with the normal Save/Discard/Cancel flow. B18 = prompt on dirty docs + compact old-vs-new file table with dirty markers.
  * Gemini's draft-snapshot + SHA-256 proposal: [DISPUTED] against the Project Lead's own B17 text, pending the Project Lead's answer. Also: it recreates the "two conflicting versions" the Project Lead wants to avoid; it depends on v2 being lossless (AGENTS §8, not yet proven); it needs stable box identity (CLAUDE-N02).
  * Required for v1: schema version; atomic write; relative + absolute paths; missing-file policy; locks keyed by a stable key, NOT runtime Record.uid; restore through the staged/deferred open path (AGENTS §22, B20 batching).
- [B19] [AGREE]. [B20] [AGREE]: askopenfilenames; open all, activate once; keep S1 staged-commit semantics; measure before optimizing.
- [B21] [AGREE]. Hide, do not clear, selected_search_folder.
- [B22] [AGREE] (Project Lead direction). Overflow signals (B23–B25) must ship in the same release as the counter removal. Update AGENTS §19, D13, README ("> 45 chars"), ledger GAME-BOX-PREVIEW. Remove the UI use only; keep core measure_line_lengths if tested.
- [B23–B26] [PARTIALLY AGREE]. Calibrate from the active editor font (digit width via font.measure); red zone from 50 digit-widths (not 60); gutter red from line 4; fix frozen Page View gutter (GEM-B15).
  * Open: overflow per LOGICAL line (bleed model) vs per DISPLAY line (wrap model) depends on CLAUDE-N03. I partially retract C-B15's "wrapped display lines" wording pending that answer.
  * Digit-width in the editor font is a proxy for the game font; label the indicator an estimate.
- [B27, B28] [AGREE] with constraints: Tk primitives only (Project Lead decision, no AtlasAdv in the MIT repo); v1 = Dialogue and All Script at 50x3; Box 0 Summary deferred until digits-per-line are counted. Preview stays display-only and never a save source (DEP-2). Wrap behaviour per CLAUDE-N03.
- [B31] [PARTIALLY AGREE].
  * Now: txt_raw read-only (consensus: C-N02, Gemini).
  * Later: whole-file edit through v2 text after DEP-5.
  * Undo (answers my own Phase 1 question): one whole-document replace delta holding before/after snapshots (documents are small; Project Lead cites ~7–21 KB). Do not rely on v2 round-trip for undo.
  * Validation: structural only (numeric command ids, length-field integrity, to_binary round-trip). I RETRACT my earlier "arity" validation: PROJECT_STATE §8.4 lists some command arities as unknown.
  * After replace, runtime uids change: locks/JP keys must be remapped (CLAUDE-N02).
- [B32] [AGREE] gated by DEP-6. Requirements: queue-based main-thread delivery; stale-result discard; TagMasker on every call; Apply honors lock and goes through the central commit path; Refresh All = enabled engines only + paid-engine confirm + session cache.
- [B33] [PARTIALLY AGREE] with Gemini's lightweight-list direction. Two cautions:
  * ttk.Treeview rows are single-line; translations are multi-line. Alternative to compare: ONE read-only tk.Text with per-box tags + one shared edit area.
  * Gemini's "~320 MB+" is an extrapolation (2x the ledger's THEME-RAW-PERF "142 boxes = 160 MB"), not a measurement. Measure-first (PROTOCOL §4).
  * "Refresh/Apply All" must reuse the BatchTranslateDialog pipeline (queue, lock skip, single undo batch) after Grok-B03 is settled.
- [B34] [AGREE] with constraints: one indexer per import run; unify with D11 ("TM = XUAT cache index") and the existing var_xuat_cache setting seen in S8a (NEEDS-VERIFY), do not add a third index; JP keys immutable per box (AGENTS §10); no global auto-pruning; symmetric \n unescape; depends on GEM-B12, B10 Treeview fix, and the duplicate policy (GPT-B09).

--- 1C. GPT ITEMS ---
- [GPT-B01] NO VERDICT YET (plausibility high; Gemini concurs). Refinement: be strict only for truncation/length-field structure; validate against real fixtures so legitimate trailing bytes are not rejected; no command-specific arity checks (PROJECT_STATE §8.4).
- [GPT-B02] [NEEDS-VERIFY] LEDGER-CONFLICT: CMD0-SPECIAL-CASE RESOLVED and Phase 1 checkbox ticked; AGENTS §8 mandates removal; GPT and Gemini both say the branch still exists. Two AIs vs ledger; line check decides. Regression test: cmd_id 0 with a non-fade name.
- [GPT-B03, GPT-B06 (+GEM-B11)] [NEEDS-VERIFY] DOC-OK (AGENTS §13, §15). One slice: capture document identity + box uid + source-text hash; discard stale results; queue instead of worker-thread after_idle. S6 only decoupled BatchTranslateDialog (PROJECT_STATE S6), which explains why the single-box path may remain. Severity note: cross-thread Tk behaviour depends on Tcl build; the contract violation stands regardless.
- [GPT-B04] [NEEDS-VERIFY] DOC-OK (D2, D3, AGENTS §20, §26). Answers GPT Q2: sparse @@#N is absolute 1-based. Validate before any mutation or undo record.
- [GPT-B05 + GEM-B04 part 1] [PARTIALLY AGREE] as ONE atomicity item: (a) checkbox "apply to Box 0" ignored (Gemini); (b) metadata applied before validation (GPT). Same function; fix together.
- [GPT-B07] [NEEDS-VERIFY]. Refinement: PROJECT_STATE S9a records 100% equivalence between normalize_with_spans and story_ast.norm_search; a match_case fix must change both paths or the span/equivalence contract breaks.
- [GPT-B08 + GEM-B18 + Grok-E02] [NEEDS-VERIFY] DOC-OK (AGENTS §15). One slice. Ledger SEARCH-RACE covers the happy-path snapshot only. GPT-F01 (coverage summary) folds in here.
- [GPT-B09] [PARTIALLY AGREE]. AGENTS §10 already requires previewing duplicate/conflicting keys, which answers GPT Q6. Prompt only on real conflict; depends on GEM-B12.
- [GPT-B10] [NEEDS-VERIFY]. Class name disputed (AppLogger vs MisoraLogger); settle before any prompt names it.
- [GPT-B11] [PARTIALLY AGREE] P2. AGENTS §17: keys must not live in ordinary config. Fail closed + warn. Ledger API-KEYS-PLAINTEXT RESOLVED glosses the fallback.
- [GPT-B12] [PARTIALLY AGREE] with Gemini. AGENTS §9 explicitly lists non-target bytes: implement it or amend §9 with evidence. Compare per-object raw data, not whole-file bytes. Test on fixtures first.
- [GPT-E01] [AGREE] no rewrite. [GPT-E02] [AGREE — CONFIRMED-DOC]: live tree has no docs/; PROJECT_STATE §9 says it exists; README now lists it. [GPT-E03] [AGREE — CONFIRMED-DOC]: MULTI-TEXTASSET-TARGET RESOLVED vs §8 item 4 open. [GPT-E04] [AGREE].
- [GPT-F01] fold into GPT-B08. [GPT-F02] fold into GPT-B09/B34. [GPT-F03] [DEFERRED] until a real multi-TextAsset bundle is shown.
- [GPT-R01..R04] [AGREE] as reference audit (not verified by me). R01/R02 matter only if a dataminer is ported: [OUT OF SCOPE] with GEM-F05.

--- 1D. GEMINI ITEMS (GEM-B01..B20, E01..E05, F05, F06) ---
- [GEM-B01] [NEEDS-VERIFY] DOC-OK (S2: _dirty_state_changed mirrors open_documents[path]["dirty"], so code that sets only self.is_dirty loses it).
- [GEM-B02] [NEEDS-VERIFY] LEDGER-CONFLICT (TRANSLATION-LOCK/D8 promise multi-file replace protection). Structural reason: locks are one positional set for the active document (C-N01), so non-active files cannot be protected. Depends on DEP-4.
- [GEM-B03] [NEEDS-VERIFY] potentially P0 (destroys NGUI tags in .txt when saved with Preview ON). Gates B27/B28.
- [GEM-B05 + C-N01] [AGREE] as one item: two independent AIs; AGENTS §16 requires per-document restore of view state, modified boxes and JP snapshots. Second half (close/exit saving inactive files through open_file(p)) NEEDS-VERIFY.
- [GEM-B06] [NEEDS-VERIFY]. Mechanism is standard Python: text-mode write_text on Windows turns LF into CRLF. Branch reachability unchecked. LEDGER-CONFLICT for on_export_script (Phase 4 says atomic write).
- [GEM-B07] [NEEDS-VERIFY] LEDGER-CONFLICT (CONTINUOUS-RIBBON-TARGET-STALE, SIZE-RIBBON-NO-COMMIT). Plausible: S4 migrated only on_text_cut/copy/paste to _get_card_text_widget (AGENTS §3: txt_continuous is the hidden fallback).
- [GEM-B08, B09, B10] [NEEDS-VERIFY] DOC-OK (AGENTS §5 requires BoxSnapshot to keep seg_texts; D8 for locks).
- [GEM-B12] [NEEDS-VERIFY] DOC-OK (AGENTS §10: never overwrite JP keys with English).
- [GEM-B13] [PARTIALLY AGREE] LEDGER-CONFLICT: README advertises Ctrl+Alt+C / Ctrl+Alt+V while AGENTS §12 says avoid Ctrl+Alt; ledger says unblocked. Needs Windows manual test.
- [GEM-B15] [NEEDS-VERIFY].
- [GEM-B16] [PARTIALLY AGREE]. AGENTS §8: v2 not lossless until round-trip tests pass; ledger V2-ROUNDTRIP-LOSS RESOLVED. move_box breaker loss merges with Grok-B04 (CLAUDE-N09).
- [GEM-B19] [NEEDS-VERIFY]. Bundles six unrelated defects. Split into separate IDs before any lock (ANTIGRAVITY_GUIDE checklist: each ledger item in exactly one session). Sync session restore is LEDGER-CONFLICT (Phase 3 says deferred).
- [GEM-B20/E05] [AGREE]. [GEM-E01..E04] [DEFERRED] measure-first; dead-code removal as a separate hygiene item.
- [GEM-F05] [OUT OF SCOPE] this cycle (unrequested subsystem; Grok-R01 and PROTOCOL §4 agree). [GEM-F06] [OUT OF SCOPE] unless the Project Lead asks.

--- 1E. CLAUDE PHASE 1 ITEMS (own positions) ---
- [C-B06] [DISPUTED] by Gemini (get_icon returns None vs fallback placeholder). Unresolved without assets/icon.py lines. S8b-4 added Unicode fallback text to icon-only buttons, which is only needed if icons can be unavailable (mildly favors Gemini; not proof). Design is unaffected (AGENTS §21).
- [C-B13/B15] adjusted per B22 and B23–B26. [C-F07] arity part [RETRACTED]. [C-X03] [RETRACTED]. [C-F01] refined (extend existing collapse). Others stand.

--- 1F. GROK ITEMS ---
- [Grok-B01] [NEEDS-VERIFY] possible P0 (silent per-segment corruption on Page View typing). DOC-OK (AGENTS §5, §7). Needs (1) how many real boxes have >1 segment, (2) Project Lead's edit model. Default: preserve boundaries; otherwise refuse visibly (AGENTS §28), never blank siblings.
- [Grok-B02] [NEEDS-VERIFY] DOC-OK (AGENTS §13 "model first", §28 visible failures).
- [Grok-B03] [PARTIALLY AGREE]. Partial apply on cancel is acceptable if one undo step covers it. The real risk is a double end_batch or ending the batch while the worker still runs. PROJECT_STATE S6/S8a describe exactly this close-time design. Verify with a batch-open flag.
- [Grok-B04 + GEM-B16 move_box] [PARTIALLY AGREE] merged into one "boundary breaker ownership" contract across insert/delete/move/cut-paste. AGENTS §6: preserve unknown commands, so remove only the projected breaker. Round-trip tests. Ledger BOX-STRUCTURAL-OPS/PAGE-BREAK-NOT-SPLIT conflict.
- [Grok-B05] [PARTIALLY AGREE]: label/behaviour mismatch. Minimal fix: "Replace" advances to next match (skipping locked) or is relabeled. [Grok-F01] [OUT OF SCOPE] as duplicate of Replace All scope "Current File(s)" (verify).
- [Grok-B06] [NEEDS-VERIFY]; ledger SHORTCUT-BINDTAG-ORDER RESOLVED (test_31). Windows manual retest (AGENTS §29).
- [Grok-B07] [DEFERRED], test-only: AGENTS §7 documents the empty-arg constraint. No change without in-game evidence; add a fixture round-trip test.
- [Grok-E01] [DEFERRED] measure-first. [Grok-E02] folded into GPT-B08. [Grok-E03] [AGREE].
- [Grok-F02] [PARTIALLY AGREE]: badge yes; blocking typing only per the Grok-B01 decision. [Grok-F03] [OUT OF SCOPE]. [Grok-R01/R02] [AGREE] do not port.

======================================================================
2. NEWLY SURFACED TRAPS OR OMISSIONS
======================================================================
- [CLAUDE-N01] Ledger trust | Severity: P1 | [CONFIRMED-DOC]
  * Location & Evidence: PROJECT_STATE.md section 4 vs peer/user evidence. RESOLVED entries contradicted: CMD0-SPECIAL-CASE, FIND-REPLACE-UI-ASYMMETRY, CONTINUOUS-RIBBON-TARGET-STALE, SIZE-RIBBON-NO-COMMIT, TRANSLATION-LOCK, CTRL-ALT-HOTKEYS-BLOCKED, BOX0-NO-SELECT-CHECKBOX, V2-ROUNDTRIP-LOSS, GAME-BOX-PREVIEW (D13 says "width", row says "45 characters"), MULTI-TEXTASSET-TARGET (§8 item 4 open).
  * Why it matters: AGENTS §1 makes Antigravity read this ledger first; stale RESOLVED statuses will make it skip real work.
- [CLAUDE-N02] Lock/identity model | Severity: P1 | [NEEDS-VERIFY]
  * Location & Evidence: AGENTS §4 (Record.uid runtime-only, never serialized); C-N01 (_locked_boxes positional Set[int]); AGENTS §13 (stable identity, not positional).
  * Why it matters: B17's "lock per box.uid" cannot survive a reload; positional locks drift on insert/delete/move; Replace All cannot see locks of non-open files. Needs a stable key (e.g. ordinal + hash of original JP text) and per-document storage.
- [CLAUDE-N03] Game wrap semantics | Severity: P1 | [CONFIRMED-DOC]
  * Location & Evidence: PROJECT_STATE §8.1 (NGUI dialogue boxes can auto-wrap; non-NGUI scenes bleed) vs Gemini R1 section 1E (wrap="none", bleed).
  * Why it matters: decides whether overflow = logical-line width or display-line count, and what Preview must draw. Pending the Project Lead's in-game test.
- [CLAUDE-N04] Source-of-truth divergence | Severity: P2 | [CONFIRMED-DOC]
  * Live root tree lacks docs/ and storydata_1001005.unity3d; PROJECT_STATE §2 and §9 say both exist. AIs cannot run fixture tests from GitHub.
- [CLAUDE-N05] Ledger arithmetic/names | Severity: P2 | [CONFIRMED-DOC]
  * §2 per-suite counts sum to 238, not 234 (the slice-by-slice chain does sum to 234); S8b-2/S8b-3 test filenames differ between §2/README and their slice sections.
- [CLAUDE-N06] AGENTS §24 stale | Severity: P2 | [CONFIRMED-DOC]
  * Lists CSIF as not-to-implement though CSIF shipped; "Phase 1–2 gates" collides with meeting phases; the ledger already ticks Phase 1–2 complete, so the gate must be tied to the Phase 2.5 P0/P1 closure.
- [CLAUDE-N07] XUAT index overlap | Severity: P2 | [NEEDS-VERIFY]
  * var_xuat_cache (S8a), D11, SEARCH-CACHE design: B34's indexer must unify with these.
- [CLAUDE-N08] Dirty fingerprint inherits v2 lossiness | Severity: P2 | [NEEDS-VERIFY]
  * PROJECT_STATE S2: saved-state checkpoints are SHA-256 of doc.to_v2_text(). If render_v2 is lossy (GEM-B16), undo-to-clean could misreport clean.
- [CLAUDE-N09] Breaker ownership | Severity: P1 | [NEEDS-VERIFY]
  * Grok-B04 + GEM-B16 move_box + insert_box all touch the same boundary record; needs one contract, not three patches.

DEPENDENCY CONSTRAINTS (ordering input for Phase 2.5; not prompts):
- DEP-1 B10 Treeview theme fix before any Treeview UI (B10 dialog, B33 list, B34 resolver).
- DEP-2 GEM-B03 before B27/B28.
- DEP-3 GEM-B07 and tooltips (C-N03) before or with the toolbar re-layout (B3/B4/B5/B13/B14).
- DEP-4 Per-document stable-key lock store (C-N01 + CLAUDE-N02) before GEM-B02/B08/B10 lock fixes, B12 UI, B17/B18.
- DEP-5 GPT-B01, GPT-B02, GEM-B16, Grok-B01, Grok-B04 before B31 and before any .misora draft feature.
- DEP-6 GPT-B03, GPT-B06, Grok-B03 before B32/B33; AGENTS §24 amended before B9/B32/B33.
- DEP-7 GEM-B12 before GPT-B09 policy and B34.
- DEP-8 One shared measure helper before B23–B28.
- DEP-9 B20 batching and deferred restore before B17.
- DEP-10 Docs-only ledger reconciliation first.

======================================================================
3. REMAINING OPEN QUESTIONS / BLOCKERS
======================================================================
1. [Project Lead] .misora v1: references-only (B17 text) or drafts (Gemini R1)? Confirm which of REC-04 (a)-(d) are the Project Lead's own decisions.
2. [Project Lead] In-game test: 80-digit single line, NGUI scene and non-NGUI scene, with and without Re:TL plugin: wrap / bleed / shrink (CLAUDE-N03).
3. [Project Lead] Windows manual checks on current main: Ctrl+H both views; ribbon Cut then navigate; Paste Box both views; Copy Box -> Notepad++ -> Paste Box; Ctrl+Alt+C/V.
4. [Project Lead] Multi-segment boxes: how common, and keep boundaries or flatten (Grok-B01)?
5. [Project Lead] Do docs/ and storydata_1001005.unity3d exist locally? If so, why untracked?
6. [Gemini] Supply Phase 1 original and file:line ranges for GEM-B01..B20; answer Grok; justify the ~320 MB figure; confirm origin of REC-04 items.
7. [GPT, Grok] Verify with file:lines: GEM-B01, B02, B03, B05, B07, B08, B12; Grok-B01..B04; C-N01; CMD0 branch; get_icon None-vs-fallback; logger class name.
8. [All] Pin the baseline hash before Phase 2.5.

======================================================================
4. PHASE 2 GATE DECLARATION
======================================================================
PHASE 2 STATUS: OPEN — CONTINUING DEBATE
Blocking Items (if OPEN): Q1 (.misora scope), Q2 (wrap semantics), peer line-level verification of every [NEEDS-VERIFY] item, REC-01/REC-04 resolution, B33 layout choice, baseline pin.