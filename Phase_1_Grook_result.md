# MISORA-EDITOR — PHASE 1 INDEPENDENT RESEARCH DOSSIER

Reviewer: Grok
Date: 2026-11-23
Inspected Baseline: Misora-Editor 1924487f28c9da3b5ede399fd69f24a23e547527 (misora.py 12143 lines; root version string 1.4.0)
Reference Files Inspected: Misora-Reference tools/README.md, tools/priconne-adv-tools (listing + bat/docs names), images/README.md and image filenames (AtlasAdv PNG, Bandicam JPGs). Pixel-level image review was not required for the code defects below.

======================================================================
1. BUGS & DEFECTS (EVIDENCE-BASED)
======================================================================
- [Grok-B01] Multi-segment inject collapses text | Severity: P1 | Status: [CONFIRMED]
  * Location: `core/story_ast.py` -> `StoryDocument.inject_box` (lines 511–525)
  * Problem: If `seg_texts` is omitted and the box has more than one segment, the full edited string is written only into the first non-empty segment (`target_idx`). Every other segment is set to `fill` (default `""`) plus a shared trailing break on the last segment. `MisoraApp._on_dialogue_edited` calls `inject_box(idx, None, new_tx)` with no `seg_texts` (`misora.py` lines 8312–8314). Page-view typing therefore destroys per-segment argument layout (voice-split / multi-record boxes).
  * Impact: Silent binary arity/content corruption on the next bundle save. Undo stores only the flattened clean text, so redo cannot restore the original segment split.
  * Proposed Fix Direction: When `len(segs) > 1` and `seg_texts` is None, either refuse the edit with a status error or distribute text using an explicit, tested policy (and record per-seg undo). Do not blank sibling segments.

- [Grok-B02] Undo recorded before a swallowed inject failure | Severity: P1 | Status: [CONFIRMED]
  * Location: `misora.py` -> `MisoraApp._on_dialogue_edited` (lines 8298–8316)
  * Problem: `undo_journal.record(BoxEditDelta...)` and `_mark_document_dirty` run before `inject_box`. The inject is wrapped in `except Exception: pass`. A failed inject (index error, unowned record, kind conversion) still leaves an undo entry and a dirty flag while the AST is unchanged, or only partially updated if failure happens mid-mutation inside `set_box_kind`.
  * Impact: Undo/redo desync and a dirty document whose bytes do not match the journal.
  * Proposed Fix Direction: Apply the model change first; record undo only after success. Surface the exception via the status bar (AGENTS.md Rule 28). Do not swallow.

- [Grok-B03] Batch-translate cancel races the undo batch | Severity: P1 | Status: [CONFIRMED]
  * Location: `misora.py` -> `BatchTranslateDialog._on_close` (lines 11958–11969) and `_poll_worker_queue` (lines 12056–12118)
  * Problem: Close sets `_cancelled`, sets `_is_running = False`, and calls `undo_journal.end_batch()` immediately, then destroys the dialog. The worker thread can still queue `("progress", ...)` items. The poller returns immediately once `winfo_exists()` is false, so queued translations are dropped, while any already applied `inject_box` calls remain. A second `end_batch()` in the poller is also possible if close and poll overlap. `begin_batch` was taken on the UI thread at line 12030.
  * Impact: Partial MTL apply, unbalanced undo batch, or a journal that no longer matches the document. Dialog destroy does not join the worker.
  * Proposed Fix Direction: On cancel, only set `_cancelled` and keep polling until the worker emits `("done", ...)`, then `end_batch()` once. Do not destroy the dialog or end the batch from `_on_close` while `_is_running` is true.

- [Grok-B04] Box delete drops text records but leaves the advance breaker | Severity: P1 | Status: [CONFIRMED]
  * Location: `core/story_ast.py` -> `StoryDocument.delete_boxes` (lines 601–610); breaker projection in `_rebuild_boxes` (lines 331–333); insert adds another breaker in `insert_box` (lines 570–583)
  * Problem: Deletion removes only `Seg.record` UIDs (print/tag). The following `touch`/`page`/`next_page` record (cmd 10/12 style breaker) stays in `self.records`. Cut-then-paste (`on_box_cut` / `on_box_paste`) therefore stacks extra advance commands between boxes.
  * Impact: In-game extra tap-to-advance or blank page beats after structural edits. Not a UI-only issue; `to_binary` serializes every remaining record.
  * Proposed Fix Direction: When deleting a box, also remove the single breaker that `_rebuild_boxes` treats as the box boundary, and include those records in the structural undo snapshot. Add a round-trip test: delete middle box, `to_binary`/`from_binary`, assert breaker count.

- [Grok-B05] In-file Replace only mutates the active box | Severity: P2 | Status: [CONFIRMED]
  * Location: `misora.py` -> `MisoraApp.on_replace_next` (lines 9195–9214)
  * Problem: Even with the search bar open, replace checks `self.current_doc.boxes[self.current_box_idx]` only and performs one `str.replace(..., 1)`. It does not walk other boxes or open documents.
  * Impact: Translators believe Ctrl+H replace covers the script. Occurrences in other boxes stay Japanese. No data loss by itself.
  * Proposed Fix Direction: After a miss in the current box, advance to the next unlocked box that contains the query, or label the button "Replace in this box" until a real script-wide replace exists (with one undo batch and lock skipping, matching batch-translate).

- [Grok-B06] Ctrl+H vs BackSpace double-fire | Severity: P2 | Status: [NEEDS-VERIFY]
  * Location: `misora.py` -> `MisoraApp._bind_shortcuts` line 6407 (`bind_all("<Control-h>", ...)`) and `_on_misora_shortcut` lines 6166–6168
  * Problem: Tk maps Ctrl+H to ASCII BackSpace. The historical AGENTS.md Rule 29 blocker says Ctrl+H mutates the dialogue buffer. Current code installs `MisoraShortcuts` first on the dialogue widget, continuous cards, and Box 0 summary (lines 6397, 7747, 7885) and returns `"break"` for Ctrl+H before the class binding. That should stop the deletion on those widgets. `bind_all` still does not return `"break"`, so any focused Text/Entry WITHOUT the bindtag can both open Replace and delete a character.
  * Impact: If the Windows repro still hits `txt_dialogue`, this dossier's reading is wrong and the item is P0. If not, residual risk is only non-editor widgets.
  * Proposed Fix Direction: Do not bind Ctrl+H twice. One router should return `"break"`. Project lead should retest on Windows in Page view and Continuous view before calling Rule 29 closed.

- [Grok-B07] Empty binary arguments are stored as a single space | Severity: P2 | Status: [NEEDS-VERIFY]
  * Location: `core/story_ast.py` -> `StoryDocument.to_binary` (lines 722–726)
  * Problem: A length of 0 terminates the ADV argument list, so the serializer substitutes `" "` for every empty argument. That preserves arity, but it also changes semantically empty text into a visible space and can touch non-text args that were empty strings in the AST.
  * Impact: Possible one-space dialogue or speaker drift after save/load. Needs a fixture round-trip, not a blind removal (removing it reintroduces arity truncation).
  * Proposed Fix Direction: Keep the terminator rule. Only substitute a space for text arguments that must stay present; add a test that a truly empty narration round-trips to the chosen sentinel and does not gain extra args.

======================================================================
2. EFFICIENCY, PERFORMANCE & HYGIENE OBSERVATIONS
======================================================================
- [Grok-E01] Per-keystroke highlight + inject on the UI thread | Measure-First: Yes | Status: [CONFIRMED]
  * Location: `misora.py` -> `_on_dialogue_edited` (lines 8310–8319)
  * Observation: Every real keystroke calls `inject_box`, `_update_raw_view`, NGUI highlight, search highlight, and dialogue widget resize. Cost scales with box size and raw-view record count. Not proven to drop frames.
  * Recommendation: Do not virtualize or cache yet. If typing stalls on long event stories, coalesce highlight/raw refresh with `after_idle` and keep the AST update synchronous.

- [Grok-E02] Search snapshot fallback shares the live document | Measure-First: No | Status: [CONFIRMED]
  * Location: `misora.py` -> `on_start_search` (lines 8683–8691)
  * Observation: The happy path copies records into a new `StoryDocument` (good, Rule 15). On any copy exception it stores `orig_doc` in `mem_docs` and the worker reads that live object.
  * Recommendation: On snapshot failure, skip that path and report it. Never hand the live AST to `_run_background_search`.

- [Grok-E03] Monolithic GUI module | Measure-First: No | Status: [CONFIRMED]
  * Location: `misora.py` (12143 lines)
  * Observation: App, dialogs, MTL UI, search, and batch translate live in one module. This is hygiene, not a measured hotspot.
  * Recommendation: Do not split the file in the same session as a data-integrity fix. Future slices may move `BatchTranslateDialog` / settings dialogs only after tests import them cleanly.

======================================================================
3. FEATURE & UX IMPROVEMENT IDEAS (SCOPED & PRACTICAL)
======================================================================
- [Grok-F01] Honest script-wide replace
  * User Value: Priconne name fixes (`{0}`, character nicknames, NGUI color typos) are repetitive across dozens of boxes.
  * Proposed Scope: One command: scan unlocked boxes in the open story, preview count, apply with a single undo batch, skip locked boxes the way batch translate already does (lines 11987–11990).
  * Guardrails / Risks: Do not regex-replace inside tag interiors unless the user opts in. Do not touch XUAT keys.

- [Grok-F02] Multi-segment box badge
  * User Value: Editors currently cannot see that a box is more than one binary segment, which is exactly when B01 fires.
  * Proposed Scope: If `len(box.segs) > 1`, show a small status label "N segments" and block plain typing until an explicit "edit as one string" confirm exists.
  * Guardrails / Risks: No new editor widget framework. Page view only.

- [Grok-F03] Speaker-consistency report
  * User Value: Catch `コッコロ` vs `ココロ` and empty print speakers before bundle save.
  * Proposed Scope: A dock list grouping `StoryDocument.actors()` with counts. Clicking jumps to the first box. No auto-rewrite.
  * Guardrails / Risks: Read-only. Do not invent a terminology database.

======================================================================
4. REFERENCE TOOLS / VISUAL ASSETS AUDIT (IF APPLICABLE)
======================================================================
- [Grok-R01] `tools/priconne-adv-tools` — Legacy extract/repack/datamine bats plus NewDataMiner/Raw/Trans trees. Treat as reference only. Do not port the bat pipeline, second Unity packer, or dataminer into Misora. Misora already has `core/bundle_io.save_bundle_story` (`packer="original"`, tmp verify, `os.replace`). A second writer would fork the byte format.
- [Grok-R02] `images/*` — UI and game screenshots (AtlasAdv PNG, Bandicam JPGs). Scope is visual reference for layout bugs the lead names. Do not derive an emulator, asset extractor, or reskin from them. No image file was required to confirm B01–B05.

======================================================================
5. OPEN QUESTIONS FOR PHASE 2 DEBATE
======================================================================
1. Can the project lead still reproduce Ctrl+H deleting a character in Page view and Continuous view on Windows with commit 1924487? If no, Rule 29 should be marked fixed rather than re-opened.
2. For multi-segment boxes, is the intended edit model "keep segment boundaries" or "flatten on purpose"? B01's fix depends on that answer.
3. Should `delete_boxes` remove the following tap-breaker, or do some stories store meaningful commands between print and the next touch that must be preserved?
4. Is a space sentinel for empty ADV args accepted by the live client, or have saves with blank narration been seen in game as a visible space?

PHASE 1 STATUS: COMPLETE