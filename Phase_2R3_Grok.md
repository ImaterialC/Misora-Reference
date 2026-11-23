# MISORA-EDITOR — PHASE 2 DEBATE & CROSS-CHECK (ROUND 3)

Reviewer: Grok
Responding To: Gemini R3, Qwen R3, GPT R3, Project Lead answers (a) and (b)
Baseline Verified: Misora-Editor 683724edaf2afac89d2695a80e30a471a0da9195
  GitHub compare vs 1924487: ahead_by=1, only file `.gitignore`. Source line numbers below are this HEAD.

======================================================================
1. VERDICTS ON PEER FINDINGS & USER MANUAL INPUTS
======================================================================
- [Lead (a) QW-B13 IDs 35 and 32] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: `core/story_ast.py` `_CMD_MAP` stores `35: "tag"` and `32: "cmd_32"` (lines 40–56). `set_box_kind` writes narration as `cmd_id = 35` (lines 421–427). `get_metadata` reads subtitles from `cmd_id == 32` (lines 365–366). `to_binary` rewrites a blank-speaker `print` into id 35 (lines 714–719). That last rewrite is the current narration rule, not a license to renumber 35 to 9 or 32 to 61. No production `.unity3d` fixture is in this review.
  * Required Refinement: LOCKED. Do not change binary ids 35 or 32 on any path (`_CMD_MAP`, `_INV_CMD_MAP`, v2, `to_binary`, Raw Commands labels) until a real narration/subtitle fixture proves a different id. A display label may change only if it cannot flow back into a numeric id. Regression: ids 35 and 32 survive `to_binary` / `from_binary` and v2 unchanged.

- [Lead (b) QW-B01 keep narration boxes separate] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: `_rebuild_boxes` merges adjacent text records when speaker and kind match, and only a non-12 breaker splits them (`story_ast.py` lines 326–332). `inject_box` turns a blank speaker on a `print` box into `set_box_kind(..., "tag")`, which rebuilds immediately, then indexes `self.boxes[box_index]` again (lines 476–480). Two adjacent boxes with no breaker between them (different kind or speaker) collapse into one box, and the old index can raise `IndexError` or hit the merged box. `tag -> print` then assigns `box.speaker` after that rebuild without rewriting records (lines 481–484).
  * Required Refinement: LOCKED. Clearing a speaker must not merge boxes. Capture the primary `Record.uid` first. Insert the minimum valid boundary only when the post-edit projection would collapse two boxes. Rebuild only after the full write. Undo must restore both boxes. Do not merge text as a shortcut.

- [QW-B02 sparse CSIF index shift] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: `apply_to_document` writes metadata (script_codec.py lines 463–468) before the sparse range check (lines 476–485), then calls `inject_box` by the old positional index (line 498). A mid-loop kind conversion that hits QW-B01 shifts later indexes after a partial write.
  * Required Refinement: Validate every sparse target, snapshot their record uids, apply metadata and dialogue as one transaction, roll back on any failure. Kind conversion must not change the box count unless the user explicitly inserted or deleted.

- [QW-B13 name/breaker half] Verdict: [PARTIALLY AGREE]
  * Evidence / Rationale: The map is name-ambiguous: `touch` is both 10 and 12, `fade` is 0 and 15, `motion` is 4 and 18, `effect` is 20 and 59. `_INV_CMD_MAP` is last-wins (line 58). `to_binary` still rewrites `cid == 0` when `cmd_name != "fade"` and the name is in that inverse map (lines 711–712). Renaming cmd 0 inside `_CMD_MAP` can therefore change a saved command id. `DEFAULT_BREAKERS` is name-based (line 33); cmd 12 is excluded only by `cmd_id != 12` (line 331).
  * Required Refinement: This matches GPT R3, not a new dispute. Split Raw Commands labels from the inverse id map. Remove the cmd-0 rewrite before any rename. Classify new breakers by verified `cmd_id` (0, 1, 4, 36), never by a shared name. Do not treat cmd 12 `vo_` as a breaker. Do not touch ids 35 or 32.

- [QW-B14 voice-cue ownership] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: `delete_boxes` and `move_box` collect only `seg.record.uid` (lines 605–607 and 626–631). `_rebuild_boxes` attaches a cue only when `cmd_id == 12` and `args[0]` starts with `vo_` immediately before the box (lines 311–312). Move also reinserts text records without the boundary breaker (lines 637–642), so same-kind boxes can merge after a move.
  * Required Refinement: One structural-ownership contract with Grok-B04 and CLAUDE-N09. Move/delete/insert share it. Attached voice cue travels with the box. Remove only an empty projected tap-breaker (`cmd_id == 10` or other verified empty breaker), never a `vo_` cue and never an unknown command. Snapshot every removed structural record for undo.

- [QW-B15 CSIF `\@@` parity] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: `ESCAPE_PREFIX = r"\@@"` (script_codec.py line 32). Parse strips exactly one backslash only when the line starts with `\@@` (lines 270–273). Serialize adds a backslash only when the line starts with `@@` (lines 429–430). So `\@@example` round-trips to `@@example`. `\\@@example` currently survives only because parse does not strip it.
  * Required Refinement: Change serialize and parse in the same patch. Serialize adds one backslash to `^\\*@@`. Parse removes one backslash from `^\\+@@`. Round-trip `@@`, `\@@`, `\\@@`, and `\\\@@`. Do not strip every leading backslash.

- [QW-B17 Replace-All backup collision] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: Text branch uses `%Y%m%d_%H%M%S` plus flat `fpath.stem` (misora.py lines 9467–9468). Bundle branch already uses `%f` (lines 9442–9443). Same stem, or two replaces in one second, overwrites the backup.
  * Required Refinement: Microseconds plus a short hash of the full path, or a mirrored relative path, and refuse an existing backup path. See Grok-N03 for normal save.

- [QW-B22 undo coalesce by index] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: `same_box` is uid-equal OR `box_index` equal (`undo_journal.py` lines 215–218). Two non-None, unequal uids at the same index still coalesce.
  * Required Refinement: If both uids are non-None, require uid equality. Use index only when at least one uid is None. When BoxEditDelta grows `old_seg_texts` / `new_seg_texts` for Grok-B01, coalescing must copy those fields too or multi-seg undo keeps the first keystroke's segments.

- [QW-E05 removed_records] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: `delete_boxes` physically drops the records and also adds their uids to `removed_records` (lines 608–609). Nothing else writes that set. The tombstones are not needed once the records are gone.
  * Required Refinement: Hygiene only. Do not keep them for the session. Do not prune a uid that an in-flight undo still needs.

- [QW-E06 raw-search span] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: If the raw box matches and clean text does not, every hit is rewritten as `(0, len(box.clean_text), box.clean_text)` (`search_engine.py` lines 302–308).
  * Required Refinement: Map the span or mark the hit as an approximate raw match. Do not invent an exact clean-text offset.

- [QW-E07 missing Any] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: `search_engine.py` line 384 annotates `Dict[Path, Any]` but the typing import (line 15) has no `Any`. `from __future__ import annotations` (line 8) means this is not an import-time crash.
  * Required Refinement: Add the import. P2 hygiene, not a data-loss bug.

- [QW-E08 DeepL UA 1.3] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: `mtl_engine.py` lines 212 and 309 send `Misora-Story-Editor/1.3`. App version is `1.4.0` (`misora.py` lines 105–107).
  * Required Refinement: One version source. Do not import `misora.py` from `core/` (cycle). A tiny shared constant is enough.

- [QW-R03 `\b64:` never emitted] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: `unescape_arg` accepts `\b64:` (story_ast.py lines 143–144). `escape_arg` (lines 124–138) never emits it. `decode_arg` / `encode_arg` use `surrogateescape` (lines 82 and 87).
  * Required Refinement: Fold into GEM-B16. v2 may not be treated as lossless until this round-trips. This gates U-B31, not the references-only `.misora` v1.

- [Gemini R3 dedup map and Qwen §1A acceptance] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: The overlaps I already verified still match: QW-B06 is Grok-B02, QW-B11 is the Replace options gap, QW-B19 is Grok-B07, QW-B14 joins Grok-B04. I am not reopening the folded ids.
  * Required Refinement: Ledger has one entry per defect. Qwen ids stay as aliases.

- [BulkFileDelta undo on closed files] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: AGENTS.md §16 forbids undo from silently reopening a closed file. Gemini R3 §2C and Qwen's acceptance match that rule.
  * Required Refinement: A confirmation listing every affected path, including closed ones, before a multi-file undo/redo touches disk.

- [Qwen §1B second review of GEM-B01..B16, B19a–f, GEM-N01] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: I re-read this round: GEM-B03 (preview save still reads the widget, misora.py lines 8517–8529), GEM-B04 order (metadata before sparse validation, script_codec.py 463–485), GEM-B19e (empty-story indexing at 8519 and 8524; the page branch crashes inside `inject_box`, not on line 8528 itself), GEM-N01 (roots only appended/inserted at 2740, 9092, 9148, 10441; `Text` child replaces the mod root at 2738–2739). Qwen's line cites for the remaining GEM items match the mechanisms I left open in R1. I accept that second review and close my R1 hold.
  * Required Refinement: GEM-B02 stays the multi-file branch plus the `bundle_env` / `target_object` key bug. The current-file replace-all path does skip locks.

- [U-B33 All Script MTL] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: Panel lock is one read-only multi-line `tk.Text` of tagged boxes plus one shared editable scratchpad, five static status tags, lock-aware Translate All / Apply All.
  * Required Refinement: I RETRACT the Treeview alternative from Grok R1. Apply still checks Translation Lock on the model and must not `.strip()` translation text.

- [U-B34 Import from XUAT] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: Locked spec in Qwen R3 §1E matches the lead: separate from the MTL drawer, source under `BepInEx\Translation\en\Text`, one indexer, no `conflict_manager`, paired read-only 3x50 boxes, explicit pre-apply counts, one undo batch.
  * Required Refinement: Depends on GEM-B12 (stable JP keys), GEM-N01 (bounded roots), and GEM-B03 (preview save). Do not ship it before those.

- [U-B30 Raw Commands, U-B17 references-only .misora, unresolved-lock rule, pinned HEAD] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: Bottom pane name is Raw Commands. `.misora` v1 stores paths, view, and lock identity only, no story drafts and no `.unity3d` bytes. An unmatched `(box_ordinal, sha256(original_jp_text))` lock stays unresolved and is reported. It is never moved onto another box. HEAD `683724e` verified above.
  * Required Refinement: None.

- [Grok-B05 Replace Next scope] Verdict: [RETRACTED]
  * Evidence / Rationale: `on_replace_next` does advance to the next box that contains the literal (misora.py lines 9237–9243). My Phase 1 claim that replace never leaves the active box is wrong. The advance still ignores Translation Lock and Find options, and the actual replace is still a literal `str.replace` (lines 9208–9228) recorded before `inject_box`.
  * Required Refinement: One shared matcher and lock policy for Find, Replace Next, and Replace All. Record undo only after a successful inject (same rule as Grok-B02).

- [Grok-B06 Ctrl+H] Verdict: [AGREE — CONFIRMED]
  * Evidence / Rationale: Lead's Windows check stands. Not a ledger blocker. Optional hygiene: the non-editor `bind_all` still should return `"break"`.

- [Grok-B07 / QW-B19 space sentinel] Verdict: [DEFERRED]
  * Evidence / Rationale: `to_binary` still substitutes `" "` for an empty argument (story_ast.py lines 722–725). No live-client proof in this round.
  * Required Refinement: Test-only. Do not change the sentinel in the stabilization slice.

- [GEM-F05 / GEM-F06 / QW-F01] Verdict: [OUT OF SCOPE]
  * Evidence / Rationale: No story downloader and no Replace-All diff pane in this cycle.

- [Phase_2R1_Claude.md empty-file note] Verdict: [RETRACTED]
  * Evidence / Rationale: The blob I fetched in R1 was 0 bytes. The current `Phase_2R1_Claude.md` is 22852 bytes. Qwen's citations of that review stand. It is not a blocker.

======================================================================
2. NEWLY SURFACED TRAPS OR OMISSIONS (IF ANY)
======================================================================
- [Grok-N03] Normal-save backup uses the same colliding name | Severity: P2 | [CONFIRMED]
  * Location & Evidence: `misora.py` `on_save` lines 8494–8495 and 8550–8551: `%Y%m%d_%H%M%S` plus `stem`, no `%f` and no path hash.
  * Why it matters: Same defect as QW-B17, outside Replace-All. Fold into that one backup-name fix. Not a new ledger id.

======================================================================
3. REMAINING OPEN QUESTIONS / BLOCKERS
======================================================================
- NONE.
- Ledger constraints already agreed, not new questions: ids 35 and 32 stay; speaker-clear does not merge boxes; command labels stay separate from binary ids; breakers are chosen by cmd_id; CSIF escape parity, backup names, and undo uid-coalescing use the refinements in §1.

======================================================================
4. PHASE 2 GATE DECLARATION
======================================================================
PHASE 2 STATUS: READY TO LOCK FOR PHASE 2.5
Blocking Items (if OPEN): None