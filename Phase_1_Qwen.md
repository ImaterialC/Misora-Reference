# MISORA-EDITOR — PHASE 1 INDEPENDENT RESEARCH DOSSIER

Reviewer: Qwen
Date: 2026-11-23
Inspected Baseline: Misora-Editor @ main 683724edaf2afac89d2695a80e30a471a0da9195 (app v1.4.0)
Reference Files Inspected:
  - Misora-Reference/tools/priconne-adv-tools/priconne_tool.py (COMMANDS table, parse_story, escape_arg)
  - Misora-Reference/tools/priconne-adv-tools/advscript.py (escape_arg / unescape_arg protections)
  - Misora-Reference/tools/priconne-adv-tools/config.json, Raw/9080155.txt, Work/9080155.txt (real extracted story)
  - Misora-Reference/images/ (AtlasAdv [48D3C5B6AD].png, 5 bandicam screenshots) — binary-verified only
  - Misora-Editor/AGENTS.md, PROJECT_STATE.md (canonical ledger cross-checked against live code)

Method note: All line numbers cite the live HEAD tarball. Items tagged [CONFIRMED] were read
directly in source; several were additionally proven by headless Python reproduction against
core.story_ast / core.script_codec (repro IDs T1b, T1c, T2, T3, T4, T5, T7, T8, T9, T10, T11, T13
referenced below). No UnityPy in sandbox, so bundle-layer claims are code-verified, not run.

======================================================================
1. BUGS & DEFECTS (EVIDENCE-BASED)
======================================================================

- [QW-B01] inject_box kind-conversion merges boxes -> IndexError / wrong-box injection
  * Severity: P0 | Status: [CONFIRMED] (repro T1b, T1c)
  * Location: core/story_ast.py -> StoryDocument.inject_box (lines 476-486), set_box_kind (409-449),
    _rebuild_boxes grouping (326-330)
  * Problem: When new_speaker clears a print box to narration (or sets a tag box to a speaker),
    inject_box calls set_box_kind(), which rebuilds the Box projection. _rebuild_boxes merges
    consecutive same-speaker/same-kind records. If the converted box sits between two boxes of the
    target kind WITH NO breaker record between them, all three merge into one Box. inject_box then
    re-reads self.boxes[box_index], which is now out of range (IndexError) or points at a different
    merged box. Repro T1b: [tag A][print B][tag C] (no breakers) + inject_box(1, speaker="") raises
    IndexError. Repro T1c: tag->print conversion leaves a STALE projection (records all become
    print/Misora but boxes are not rebuilt after the text write), so box identity/count silently
    drifts until the next rebuild.
  * Impact: Crash in the central edit/save path; or silent injection into the wrong box; or stale
    projection that desyncs undo deltas and box navigation. Reachable from GUI: clearing the speaker
    Entry, on_save (misora.py 8520/8525/8529), CSIF paste, replace-all.
  * Proposed Fix Direction: After any kind/speaker conversion, re-resolve the target box by Record
    uid (not positional index) and rebuild projection AFTER the text write; or insert a breaker to
    prevent unintended merging; reject/merge explicitly rather than indexing blindly.

- [QW-B02] CSIF sparse/replace apply shifts indices after kind conversion -> partial apply + crash
  * Severity: P1 | Status: [CONFIRMED] (repro T9)
  * Location: core/script_codec.py -> apply_to_document sparse branch (488-499), replace branch (518-543)
  * Problem: Sparse indices are validated against the ORIGINAL box count, then each block calls
    inject_box. If an earlier block converts a box kind and merges boxes (see QW-B01), later indices
    point at wrong boxes or out of range. Repro T9: "@@#2|_" + "@@#4|Kyou" on a 4-box doc raises
    IndexError AFTER block #2 was already applied -> document left partially mutated.
  * Impact: Partial paste/replace with no rollback; silent misapplication to wrong boxes; dirty state
    with half-applied CSIF. Violates AGENTS Rule 20 (never silently remap positionally).
  * Proposed Fix Direction: Apply sparse blocks by stable box uid captured before mutation; or
    apply in descending index order; or snapshot+transactional rollback on any failure.

- [QW-B03] v2 round-trip drops whitespace-only args and creates phantom records
  * Severity: P1 | Status: [CONFIRMED] (repro T2)
  * Location: core/story_ast.py -> escape_arg (124-138), from_v2_text arg loop (768-776, blank-break 771)
  * Problem: escape_arg does not escape spaces. A whitespace-only arg (e.g. " ", which to_binary
    itself emits for empty args) renders as a line " "; from_v2_text treats any blank-stripped line
    as a record terminator, dropping the arg and misparsing the category line as a new header.
    Repro T2: print#6 ["Misora"," "] -> reparsed as print ["Misora"] + phantom record ("Other",0,[]).
  * Impact: Silent data corruption on v2 export/import round-trip. Directly contradicts ledger
    V2-ROUNDTRIP-LOSS = RESOLVED. AGENTS Rule 8 requires preserving whitespace-only args.
  * Proposed Fix Direction: Port advscript.py escape_arg protections (trailing-space \s/\S escaping
    and category-collision prefixing) — see QW-R01.

- [QW-B04] v2 round-trip misparses an arg whose text equals a category name
  * Severity: P1 | Status: [CONFIRMED] (repro T3)
  * Location: core/story_ast.py -> from_v2_text (773), escape_arg (124-138)
  * Problem: The parser treats any line exactly matching DEFAULT_CATEGORIES ("Sound","Effect",
    "Camera","Face","Animation","Volume","Other","System","Movie","Motion","Background",
    "Foreground","Screen") as the category terminator. A legitimate dialogue arg equal to one of
    these words is consumed as the category, dropping it and spawning a phantom record from the
    real category line. Repro T3: print ["Misora","Sound"] -> print ["Misora"] + ("Other",0,[]).
  * Impact: Silent corruption for common English words that collide with category names.
  * Proposed Fix Direction: Escape category-colliding args with a leading backslash on emit and
    unescape on parse (advscript.py 104/111 already does this).

- [QW-B05] Plain-name v2 import resolves duplicate command names to the WRONG numeric ID
  * Severity: P1 | Status: [CONFIRMED] (repro T4)
  * Location: core/story_ast.py -> _INV_CMD_MAP (58), from_v2_text header parse (755-764)
  * Problem: _CMD_MAP has duplicate names (10/12="touch", 11/13="wait", 0/15="fade", 4/18="motion",
    20/59="effect"). _INV_CMD_MAP = {v:k} keeps the LAST id. A plain header "touch" (no #id) parses
    to cmd_id 12 (the voice-cue id) instead of 10 (the breaker). Repro T4 confirms touch->12,
    wait->13, fade->15, motion->18, effect->59.
  * Impact: External/legacy v2 files (or hand-edited headers) import with altered command semantics
    (breaker becomes voice-cue-style; _rebuild_boxes treats cmd 12 as non-breaker). App-generated v2
    is safe only because render_v2 always emits #id (see QW-B18 dead branch).
  * Proposed Fix Direction: Make plain-name resolution unambiguous (first-id wins, or require #id,
    or maintain a canonical name->id table distinct from the display map).

- [QW-B06] Silent "except Exception: pass" around inject_box desyncs undo journal vs model
  * Severity: P1 | Status: [CONFIRMED]
  * Location: misora.py -> _on_dialogue_edited (8312-8316), _flush_continuous_card_edits (6900-6903)
  * Problem: Both paths record a BoxEditDelta and mark dirty BEFORE calling inject_box, then wrap
    inject_box in try/except: pass. If inject_box raises (e.g. QW-B01 IndexError), the model is NOT
    updated but the undo stack and dirty flag already reflect a change. The widget shows new text,
    the model holds old text, and undo believes a mutation occurred.
  * Impact: Undo/model desync; "dead" edits that appear saved but are not; subsequent save re-raises.
    Violates AGENTS Rule 28 (visible failures, no silently dead operations).
  * Proposed Fix Direction: Commit to model FIRST, then record delta/dirty only on success; surface
    failures via status bar / report_callback_exception instead of pass.

- [QW-B07] MTL worker callbacks invoke Tk after_idle FROM the worker thread
  * Severity: P1 | Status: [CONFIRMED] (thread-affinity violation; crash manifestation intermittent)
  * Location: core/mtl_engine.py -> translate_async worker (345-351); misora.py ->
    on_translate_current_box on_success/on_error (10546, 10553), TranslatorAssistantDialog._on_translate
    (11761, 11767)
  * Problem: translate_async runs on_success(result)/on_error(err) inside the background thread.
    Those callbacks call self.after_idle(...), i.e. a Tk call on a non-main thread. The search path
    correctly uses queue.Queue + main-thread poll (_process_search_queue), but MTL does not.
  * Impact: Violates Tkinter thread affinity and AGENTS Rule 15 (worker completion posted via a
    main-thread queue). Risk of Tcl interpreter corruption / intermittent crash under load.
  * Proposed Fix Direction: Route MTL results through a main-thread queue polled by after(), identical
    to the search architecture; never call Tk from the worker.

- [QW-B08] Bulk-delta cache uses wrong keys ("bundle_env"/"target_object" vs "env"/"obj")
  * Severity: P1 | Status: [CONFIRMED]
  * Location: misora.py -> _apply_delta BulkFileDelta branch (9668-9673, 9718-9723) vs open_file cache
    construction (6538-6546) and cache-hit read (6513-6515); close_file reads .get("env") (9894)
  * Problem: The canonical open_documents cache stores "env" and "obj". The bulk undo/redo path
    reads old_env via .get("bundle_env") (always None -> the real stale env is never disposed) and
    writes entry["bundle_env"]/["target_object"] (keys the rest of the app never reads). entry["env"]
    and entry["obj"] remain stale after a bulk undo/redo on an open bundle.
  * Impact: UnityPy Environment memory leak + stale current_unity_env/current_text_obj on next switch;
    later save may verify against a disposed/stale object. Inconsistent key naming is the root cause.
  * Proposed Fix Direction: Use the canonical "env"/"obj" keys everywhere; dispose the actual old env;
    add a single cache-accessor helper to prevent key drift.

- [QW-B09] XUAT sync JP source key is positional and falls back to English text
  * Severity: P1 | Status: [CONFIRMED]
  * Location: misora.py -> on_save (8576 orig_key fallback, 8586 update), _original_box_texts build
    (6630-6634); core/xunity_sync.py -> jp_source_cache / register_jp_key / get_jp_key (78-87) UNUSED
    by on_save
  * Problem: _original_box_texts is Dict[int,str] keyed by box INDEX, rebuilt only on open_file.
    Structural edits (insert/delete/move) shift indices but the dict is not rekeyed, so b_idx maps to
    the wrong box's JP snapshot. When a key is missing, the fallback is box_obj.clean_text (the
    CURRENT, possibly English text) used as the "Japanese key". The uid-keyed immutable cache in
    XUnitySyncManager exists but on_save never calls it.
  * Impact: Wrong dictionary entry updated, or no match, or English used as JP key -> silent
    cross-contamination of translations. Violates AGENTS Rule 10 (immutable JP keys per Box uid).
  * Proposed Fix Direction: Key JP snapshots by box uid (use sync_manager.register_jp_key/get_jp_key);
    never fall back to current text as the JP key.

- [QW-B10] Search silently skips unreadable/corrupt files (no skip reporting)
  * Severity: P1 | Status: [CONFIRMED]
  * Location: core/search_engine.py -> search_file bundle except (346-347), text except (372-373);
    search_directory loop (412-419)
  * Problem: Any exception (corrupt bundle, missing UnityPy, permission, decode error) is swallowed
    and the file returns []. The directory walker does not track or report skipped files.
  * Impact: Search under-reports results with zero indication; user trusts an incomplete result set.
    Violates AGENTS Rule 15 (report skipped/inaccessible paths).
  * Proposed Fix Direction: Return/accumulate a skipped-paths list with reasons; surface a
    "N files skipped" banner + detail dialog.

- [QW-B11] Replace All ignores Find options (regex / case / whitespace-insensitive)
  * Severity: P1 | Status: [CONFIRMED]
  * Location: misora.py -> on_replace_all (9284/9290 current-file, 9388/9437 multi-file)
  * Problem: Replace All uses literal "find_text in box.clean_text" and str.replace(), regardless of
    the search panel's match_case / use_regex / ignore_whitespace settings. Find may show hits
    (regex/case-insensitive/whitespace-collapsed) that Replace All then cannot match, or replaces
    different text than what was found.
  * Impact: Find/Replace inconsistency; "not found" despite visible hits; wrong replacements.
  * Proposed Fix Direction: Share the compiled matcher from ProjectSearchEngine._compile_matcher for
    replacement span discovery; honor the same options; operate on raw text spans, not normalized
    clean_text, to preserve break style.

- [QW-B12] from_binary silently accepts truncated/corrupt bytes (no validation)
  * Severity: P1 | Status: [CONFIRMED] (repro T7)
  * Location: core/story_ast.py -> StoryDocument.from_binary (675-697)
  * Problem: On truncated arg length or trailing bytes the parser breaks out of loops and still
    appends partial records, then continues reading garbage as new command IDs. No exception.
    Repro T7: cutting the last 3/10 bytes or to 5 bytes yields fewer/garbage records silently.
  * Impact: Opening a corrupt bundle shows a partial/garbled story; saving re-serializes garbage ->
    silent corruption. The reference priconne_tool.parse_story (125-145) RAISES ToolError on exactly
    these conditions; the port dropped that validation.
  * Proposed Fix Direction: Raise on trailing/truncated bytes (port parse_story guards); refuse to
    save a document whose parse was incomplete.

- [QW-B13] Command table misnaming + breaker gaps + narration/subtitle ID risk
  * Severity: P1 (misnaming/breakers) / P0-candidate (narration/subtitle) |
    Status: [CONFIRMED] for misnaming/breakers; [NEEDS-VERIFY] for narration/subtitle IDs
  * Location: core/story_ast.py -> _CMD_MAP (40-57), DEFAULT_BREAKERS (33), has_metadata/get_metadata/
    set_metadata (346-407); vs Misora-Reference/tools/priconne-adv-tools/priconne_tool.py COMMANDS
    (59-69) and real data Raw/9080155.txt
  * Problem: The authoritative reference table is 0=title,1=outline,2=chara,3=visible,4=type,5=face,
    6=focus,7=background,8=print,9=tag,10=goto,11=bgm,12=touch,13=choice,14=vo,15=wait,...,35=transition,
    ...,61=title_telop. Misora's _CMD_MAP names 0="fade",1="log",2="bg",4="motion",9="voice",35="tag",
    etc. The behaviorally-critical IDs happen to work (6 dialogue renamed "print"; 10 breaker renamed
    "touch"; 12 voice-cue via vo_ prefix), BUT:
      (a) Raw AST view shows wrong command names (confusing/unsafe for manual edits).
      (b) DEFAULT_BREAKERS=("touch","page","next_page") misses real breakers title(0)/outline(1)/
          type(4)/situation(36) ("page"/"next_page" do not exist in the real table). Boxes can merge
          across mid-script title/outline/situation boundaries.
      (c) Narration: Misora writes narration as cmd 35 ("tag" in Misora) but reference[35]="transition"
          and reference[9]="tag". If real narration is id 9, Misora both (i) swallows it on parse
          (names 9="voice" -> treated as a voice cue, never displayed) and (ii) writes a transition
          command when the user creates narration.
      (d) Subtitle: Misora uses cmd 32; reference[32]="black_in", reference[61]="title_telop". Editing
          "subtitle" could overwrite a black_in screen-effect command.
  * Impact: (a,b) confirmed UX/structural risk; (c,d) potential P0 story corruption IF the reference
    table is correct for production bundles. The sample story has no narration/subtitle records, so
    (c,d) cannot be finalized without a real fixture.
  * Proposed Fix Direction: Reconcile _CMD_MAP with the verified reference table; add title/outline/
    type/situation to breakers; VERIFY narration/subtitle IDs against a real narration-bearing bundle
    before any change (see Open Question 1). Do not relabel blindly.

- [QW-B14] move_box / delete_boxes orphan voice cues and leave double breakers
  * Severity: P2 | Status: [CONFIRMED] mechanism (repro T10, T13); game impact [NEEDS-VERIFY]
  * Location: core/story_ast.py -> move_box (614-644), delete_boxes (589-612)
  * Problem: Only the box's print/tag segment records are moved/deleted; the associated voice record
    and surrounding breaker records stay in place. Repro T10: move(0->1) leaves vo_1001 orphaned at
    the top and the moved Misora box loses its voice. Repro T13: delete_boxes([1]) leaves two
    consecutive touch records.
  * Impact: Voice/dialogue desync and extra empty tap-pages in-game after structural edits.
  * Proposed Fix Direction: Move/delete the owning voice cue and normalize adjacent breakers as part
    of the structural API; define explicit semantics for voice attachment.

- [QW-B15] CSIF body line beginning with "\@@" is corrupted on round-trip
  * Severity: P2 | Status: [CONFIRMED] (repro T8)
  * Location: core/script_codec.py -> serialize body escape (424-432), _parse_csif unescape (271-273)
  * Problem: serialize only escapes body lines starting with "@@". A line literally starting "\@@"
    is emitted unchanged; the parser then strips the leading "\" -> text becomes "@@...".
    Repro T8: "line1\n\@@looks like header" -> "line1\n@@looks like header".
  * Impact: Silent text alteration for dialogue containing literal "\@@" at line start.
  * Proposed Fix Direction: Also escape body lines starting with "\@@" (double the backslash) on emit.

- [QW-B16] XUAT find_and_update overwrites ALL conflicting matches without a gate
  * Severity: P2 | Status: [CONFIRMED]
  * Location: core/xunity_sync.py -> find_and_update (186-198); preview_matches conflict flag (128)
  * Problem: preview_matches flags is_conflict when matched lines have differing translations, but
    find_and_update never checks it and overwrites every matching line across every file. on_save
    (misora.py 8577) calls find_and_update directly with no preview/conflict gate.
  * Impact: Context-specific translations for homonym keys get unified/lost silently.
  * Proposed Fix Direction: Gate updates on conflict preview (AGENTS Rule 10); let the user resolve
    duplicates before writing.

- [QW-B17] Multi-file text Replace All backup filenames can collide
  * Severity: P2 | Status: [CONFIRMED]
  * Location: misora.py -> on_replace_all text backup (9467-9468) vs bundle backup (9442)
  * Problem: Text backups use second-resolution timestamp + stem only in a FLAT backup dir; bundles
    use microseconds. Two same-stem text files in different folders replaced in the same second
    produce the same backup name -> the second overwrites the first backup.
  * Impact: Lost pre-replace backup -> weakened rollback safety.
  * Proposed Fix Direction: Use microseconds + a path hash (or mirror relative dirs) for backup names.

- [QW-B18] to_binary cmd_id==0 special-case still present (ledger says removed)
  * Severity: P2 | Status: [CONFIRMED]
  * Location: core/story_ast.py -> to_binary (710-712)
  * Problem: "if cid == 0 and r.cmd_name != 'fade' and r.cmd_name in _INV_CMD_MAP: cid = _INV_CMD_MAP[...]"
    remains. PROJECT_STATE ledger CMD0-SPECIAL-CASE = RESOLVED ("Removed cmd_id==0 special case")
    contradicts live code. Also render_v2 (187) has a dead branch: "self.cmd_name in _CMD_MAP" is
    always False (keys are ints), so headers ALWAYS carry #id (repro T5).
  * Impact: Name-edit of a cmd-0 record can silently change its binary ID; ledger/code drift erodes
    trust in the canonical state.
  * Proposed Fix Direction: Remove the special-case per AGENTS Rule 8; fix the render_v2 membership
    test (use _INV_CMD_MAP / cmd_id) or delete the dead branch; reconcile the ledger.

- [QW-B19] Empty binary arg becomes a single space (semantic change)
  * Severity: P2 | Status: [CONFIRMED] (repro T11)
  * Location: core/story_ast.py -> to_binary (725)
  * Problem: Empty args are encoded as " " to preserve arity (binary length-0 terminates the record).
    Repro T11: print ["Misora",""] -> reparsed ["Misora"," "]. Arity is preserved but a space is
    injected into game text.
  * Impact: Minor text alteration for cleared fields; ledger EMPTY-ARG-ARITY wording ("retains empty
    string arguments") is misleading.
  * Proposed Fix Direction: Document the trade-off explicitly; consider whether cleared dialogue
    should instead convert to narration or be rejected upstream.

- [QW-B20] Bulk-replaced non-current open bundle keeps stale cache -> later save clobbers bulk edit
  * Severity: P2 | Status: [CONFIRMED] mechanism
  * Location: misora.py -> on_replace_all bundle cache sync (9455-9457) + open_file cache-hit (6508-6520)
  * Problem: For an open bundle that is NOT the current file, bulk replace records a checkpoint and
    marks dirty but does not refresh entry["doc"]/["env"]/["obj"]. Switching to it uses the stale
    cache (no disk reload), showing pre-replace text; saving then overwrites the bulk-replaced disk
    version. Only the CURRENT file is reloaded (9502-9503).
  * Impact: Lost bulk edits on other open documents.
  * Proposed Fix Direction: Refresh or invalidate cache entries for all affected open documents;
    reload from disk on switch when a bulk op touched them.

- [QW-B21] Async MTL result applied to positional index after the async gap
  * Severity: P2 | Status: [CONFIRMED]
  * Location: misora.py -> on_translate_current_box update_ui (10524-10539)
  * Problem: The callback captures b_idx and only checks b_idx < len(boxes). If boxes were inserted/
    deleted while translation was in flight, b_idx points at a different box; inject_box writes the
    translation into the wrong box. box_uid is recorded in the delta but not used to re-resolve.
  * Impact: Translation lands in the wrong dialogue box.
  * Proposed Fix Direction: Re-resolve target by box uid at apply time; abort if identity changed.

- [QW-B22] Undo coalescing positional OR fallback can merge two different boxes
  * Severity: P2 | Status: [CONFIRMED]
  * Location: core/undo_journal.py -> record coalescing same_box (215-218)
  * Problem: same_box = (uid match) OR (box_index match). After a structural edit, a new box can
    occupy the same positional index as a previous different box; the positional fallback then
    coalesces their edits into one undo operation.
  * Impact: Undo loses one box's edit history.
  * Proposed Fix Direction: Prefer uid identity; only fall back to index when BOTH uids are None.

======================================================================
2. EFFICIENCY, PERFORMANCE & HYGIENE OBSERVATIONS
======================================================================

- [QW-E01] Multi-file Replace All runs synchronously on the UI thread | Measure-First: Yes | [CONFIRMED]
  * Location: misora.py -> on_replace_all (9428-9492)
  * Observation: Per-file bundle load + inject + save + backup copy all execute on the UI thread with
    no progress dialog and no cancel. Large projects freeze the GUI.
  * Recommendation: Move bulk replace to a worker with a main-thread progress/cancel queue (mirror
    search architecture); keep disk writes transactional.

- [QW-E02] Search loads + disposes every bundle fully, no caching | Measure-First: Yes | [CONFIRMED]
  * Location: core/search_engine.py -> search_file (269-270), search_directory (412-419)
  * Observation: Each .unity3d is fully loaded via UnityPy then disposed for every search. Hundreds
    of bundles = heavy repeated work. (Disposal itself is correct; doc is pure-Python.)
  * Recommendation: Measure first; consider an LRU keyed by path/mtime/size (ledger SEARCH-CACHE)
    only if profiling shows a real bottleneck.

- [QW-E03] XUAT cache normalized lookup is O(N) per translation | Measure-First: Yes | [CONFIRMED]
  * Location: core/mtl_engine.py -> translate (126-129)
  * Observation: On exact-match miss, the whole cache is scanned with a regex per key. Batch
    translate of many boxes against a large dictionary is O(boxes x dict_size).
  * Recommendation: Precompute a normalized-key index once per cache load.

- [QW-E04] TagMasker.unmask recompiles + scans per tag | Measure-First: Yes | [CONFIRMED]
  * Location: core/ngui_tags.py -> unmask (158-160)
  * Observation: One regex compile + full-text sub per masked token. Minor for typical box sizes.
  * Recommendation: Single combined pass if profiling warrants; otherwise leave.

- [QW-E05] removed_records set grows unbounded | Measure-First: No | [CONFIRMED]
  * Location: core/story_ast.py -> delete_boxes (609)
  * Observation: Records are filtered out of self.records but their uids accumulate in
    removed_records forever (also to_binary/from_binary membership checks scan it).
  * Recommendation: Prune uids no longer present; minor memory hygiene.

- [QW-E06] Search raw-text fallback fabricates a whole-box highlight span | Measure-First: No | [CONFIRMED]
  * Location: core/search_engine.py -> search_file (302-308)
  * Observation: When only box.text (raw) matches, the result span is (0, len(clean_text)) -> the
    entire box is highlighted instead of the actual hit.
  * Recommendation: Map raw spans back to clean_text spans, or label the result as a raw-only match.

- [QW-E07] Missing "Any" import in search_engine.py | Measure-First: No | [CONFIRMED]
  * Location: core/search_engine.py -> search_directory signature (384)
  * Observation: "Any" is used in a type hint but never imported; masked by "from __future__ import
    annotations". Would fail under typing.get_type_hints / runtime evaluation.
  * Recommendation: Import Any from typing.

- [QW-E08] Version drift: DeepL User-Agent hardcoded "1.3" | Measure-First: No | [CONFIRMED]
  * Location: core/mtl_engine.py -> _translate_deepl (212), _test_deepl_usage (309)
  * Observation: App is v1.4.0 (misora.py _get_app_version returns "1.4.0"); UA says 1.3. AGENTS
    Rule 21 wants a single version source (__init__.__version__).
  * Recommendation: Derive UA from the single version source.

- [QW-E09] logger.flush() race vs in-flight write | Measure-First: No | [CONFIRMED]
  * Location: core/logger.py -> flush (97-101)
  * Observation: flush polls queue.empty(); an entry already get()-ed but still being written makes
    empty() True before the write completes -> flush can return early.
  * Recommendation: Use task_done()/join() on the file queue for a true barrier.

- [QW-E10] write_atomic_encoded fast path bypasses newline normalization | Measure-First: No | [CONFIRMED]
  * Location: core/text_encoding.py -> write_atomic_encoded (189-190)
  * Observation: When not has_bom and newline in (None,"\n"), it writes raw content via write_text,
    skipping the normalization that encode_with_metadata (185) computed. Mixed endings can survive.
  * Recommendation: Always write the normalized "data" bytes for consistency.

- [QW-E11] Documentation drift: AGENTS Rule 29 vs PROJECT_STATE | Measure-First: No | [CONFIRMED]
  * Location: AGENTS.md Rule 29 (lists Ctrl+H / ribbon Cut / Paste Box as release blockers) vs
    PROJECT_STATE.md (all RESOLVED); live misora.py _on_misora_shortcut (6166-6168) returns "break"
    for Ctrl+H.
  * Observation: Ctrl+H is verified fixed in code; AGENTS Rule 29 is stale. Ledger also marks
    V2-ROUNDTRIP-LOSS / CMD0-SPECIAL-CASE RESOLVED while code still exhibits them (QW-B03/B04/B18).
  * Recommendation: Reconcile AGENTS/PROJECT_STATE with verified code state each phase.

======================================================================
3. FEATURE & UX IMPROVEMENT IDEAS (SCOPED & PRACTICAL)
======================================================================

- [QW-F01] Bulk Replace preview pane (per-file diff before write)
  * User Value: Priconne translators edit many bundles; a dry-run diff prevents accidental mass
    corruption and builds trust in Replace All.
  * Proposed Scope: Reuse the search matcher to collect spans; show a read-only Treeview of
    file/box/old->new; Apply writes via the existing transactional BulkFileDelta path.
  * Guardrails / Risks: No new subsystem; must honor Find options (ties to QW-B11); keep UI-thread
    safe via the search worker pattern.

- [QW-F02] XUAT conflict-resolution gate before sync
  * User Value: Homonym JP keys appear in multiple dictionaries; previewing conflicts avoids
    clobbering context-specific translations.
  * Proposed Scope: Wire the existing preview_matches() into on_save; show conflicts in a dialog;
    let the user pick/skip. Use uid-keyed JP snapshots (QW-B09).
  * Guardrails / Risks: Do not block short JP keys (ledger REJECTED); no forced minimum key length.

- [QW-F03] Search "skipped files" report
  * User Value: Translators need to know when results are incomplete (corrupt/locked bundles).
  * Proposed Scope: Accumulate skipped paths + reasons in search_directory; show a banner + detail
    list. Pure reporting, no engine rewrite.
  * Guardrails / Risks: Keep worker thread-free of Tk; post via queue.

- [QW-F04] Identity-stable undo/apply (uid-based)
  * User Value: Structural edits + async MTL currently risk wrong-box writes; uid resolution makes
    undo/translation land correctly.
  * Proposed Scope: Resolve BoxEditDelta/MTL targets by box uid at apply time (QW-B01/B21/B22);
    fall back to index only when uid absent.
  * Guardrails / Risks: Respect AGENTS Rule 4 (Seg.record direct reference; no stale rec_index).

- [QW-F05] Real-fixture round-trip test harness (command table verification)
  * User Value: Guarantees binary/v2/CSIF losslessness against ACTUAL game data, not self-consistent
    synthetic fixtures; settles the narration/subtitle ID question (QW-B13).
  * Proposed Scope: Add a small set of real .unity3d fixtures (with narration + subtitle) and
    byte-exact round-trip tests; port priconne_tool.parse_story validation.
  * Guardrails / Risks: Fixtures must be legally shareable; no hardcoded decryption keys; do not
    weaken existing tests (AGENTS Rule 2).

- [QW-F06] Batch translate progress + cancel + rate-limit awareness
  * User Value: Batch MTL over many boxes needs visible progress, cancel, and engine rate-limit
    handling to avoid bans/timeouts.
  * Proposed Scope: Extend BatchTranslateDialog's existing queue/poll loop with a progress bar,
    cancel flag, and per-engine delay (config.rate_limit_delay already exists).
  * Guardrails / Risks: Keep workers Tk-free (QW-B07); no new threads beyond the existing pattern.

======================================================================
4. REFERENCE TOOLS / VISUAL ASSETS AUDIT (IF APPLICABLE)
======================================================================

- [QW-R01] advscript.py escape_arg/unescape_arg — the proven fix for QW-B03/B04
  * tools/priconne-adv-tools/advscript.py (99-104, 107-119): escape_arg escapes trailing spaces as
    \s/\S and prefixes a backslash when the escaped arg equals a category name; unescape_arg reverses
    both. Misora's story_ast.escape_arg dropped BOTH protections -> direct cause of QW-B03/B04.
    Port this pattern (adapted to Misora's larger DEFAULT_CATEGORIES set).

- [QW-R02] priconne_tool.py COMMANDS + parse_story — authoritative ID table & validation
  * tools/priconne-adv-tools/priconne_tool.py COMMANDS (59-69) is the verified ID->name table;
    parse_story (125-145) RAISES on trailing/truncated bytes. Use it to reconcile _CMD_MAP (QW-B13)
    and to restore from_binary validation (QW-B12). Real data Raw/9080155.txt confirms title(0),
    outline(1), type(4), focus(6)=dialogue(speaker,text), touch(12)=vo_ cue, goto(10)=page breaker.

- [QW-R03] priconne_tool.py escape_arg \b64 surrogate fallback — v2 export gap
  * priconne_tool.py escape_arg (156-158) emits "\b64:<base64>" when an arg contains surrogateescape
    chars (non-UTF8 binary). Misora story_ast.unescape_arg ACCEPTS "\b64:" (143-144) but escape_arg
    never EMITS it. A v2 export of an arg with surrogates would write raw surrogates that fail strict
    UTF-8 encoding on save. [NEEDS-VERIFY] with a non-UTF8 fixture; port the \b64 emission.

- [QW-R04] images/ — visual references only; pixel rendering unavailable in this environment
  * images/AtlasAdv [48D3C5B6AD].png (2048x2048) and 5 bandicam screenshots are binary-verified
    (PIL decode OK) but cannot be visually rendered here. Per images/README.md, treat strictly as
    scoped visual references; do NOT extrapolate into game replicas or unrequested UI. If Phase 2
    needs pixel-level UI analysis, the Project Lead should describe the relevant screenshot regions.

- [QW-R05] tools/priconne-adv-tools/misora/ — LEGACY nested copy, not the target
  * Contains an older misora.py (352,158 bytes) and older core/. This is a reference snapshot, NOT
    the audited codebase (target misora.py is 543,343 bytes). Do not port from or cite this copy as
    current behavior.

- [QW-R06] config.json break_char="\r", filler=" " — break-style convention
  * The reference tool config uses break_char="\r" and filler=" ". Misora auto-detects break_char
    from record args. When porting escape/round-trip logic, preserve the detected break style and do
    not hardcode "\n" (ties to QW-B11 replacement on clean_text losing break style).

======================================================================
5. OPEN QUESTIONS FOR PHASE 2 DEBATE
======================================================================

1. (Verification, high priority) What are the REAL production command IDs for narration and subtitle?
   Reference priconne_tool.COMMANDS says 9="tag", 35="transition", 32="black_in", 61="title_telop",
   while Misora uses 35 for narration and 32 for subtitle. Please provide a real .unity3d fixture
   containing narration + a chapter subtitle so we can confirm/refute QW-B13(c,d) before Phase 2.5.
   Also confirm whether any production story uses id 8 ("print") for dialogue (Misora names 8="se").

2. (Design) Is the multi-segment Box model INTENDED to span multiple in-game pages (a same-speaker
   run across touch(12) voice cues), or should each in-game tap-page be its own Box? This determines
   the correct fix for inject_box text redistribution (QW-B01) and voice/pacing preservation
   (QW-B14). Current code merges same-speaker runs and redistributes all text into the first
   non-empty segment.

3. (Design) Should XUAT sync (a) gate on conflict preview and (b) key immutable JP snapshots by box
   uid via XUnitySyncManager.jp_source_cache rather than the positional _original_box_texts?
   (QW-B09/B16). Confirm the desired conflict-resolution UX.

4. (Project Lead preference) When the user clears a speaker on a dialogue box sandwiched between two
   narration boxes, should the result MERGE into one narration box, or stay a separate narration
   box? This chooses the QW-B01 fix direction (merge-by-design vs breaker-preserving).

5. (Verification) Is the non-Windows DPAPI plaintext fallback acceptable (core/security.py 35-36
   returns plaintext off win32; unprotect_secret returns "" on failure at 99)? Should non-Windows
   refuse to store keys, or use an OS keyring? And should a failed decrypt warn rather than silently
   yield an empty key?

6. (Design) BulkFileDelta undo writes to closed files' disk paths (misora.py 9661/9698) even though
   close_file prunes per-file journals (9896). Is cross-file bulk undo on closed files intended, or
   should it skip/notify for closed paths? (AGENTS Rule 16 vs bulk transaction semantics.)

PHASE 1 STATUS: COMPLETE