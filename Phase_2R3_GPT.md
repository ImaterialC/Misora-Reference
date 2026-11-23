# MISORA-EDITOR — GPT PHASE 2 DEBATE RESPONSE (ROUND 3)

**Reviewer:** OpenAI GPT-6  
**Role:** Independent Technical Reviewer  
**Responding To:**
- Gemini — `Phase_2R3_gemini.md`
- Qwen — `Phase_2R3_Qwen.md`
- GPT — `Phase_2R2_GPT.md`
- Gemini — `Phase_2R2_gemini.md`
- Previous Phase 1 and Phase 2 research dossiers
- Project Lead's final answers to Qwen's two open questions

**Target Repository:** `ImaterialC/Misora-Editor`  
**Reference Repository:** `ImaterialC/Misora-Reference`

---

## 1. BASELINE REVALIDATION

### 1.1 Target repository

The current target repository HEAD is still:

`683724edaf2afac89d2695a80e30a471a0da9195`

I independently checked the GitHub branch and compared it against the Phase 1 baseline:

`1924487f28c9da3b5ede399fd69f24a23e547527`

The comparison confirms:

- `683724e` is one commit ahead of `1924487`.
- The only changed file is `.gitignore`.
- No application source files changed between those commits.

Therefore, the source-level findings from Phase 1 and Round 2 remain applicable to the pinned Round 3 target baseline.

### 1.2 Review limitations

This is an independent source-code review. It is not a Windows runtime test session.

I have not executed Misora in the Project Lead's local environment, run the full test suite, or tested the relevant changes in a production game client.

Any claim that depends on an actual production `.unity3d` fixture remains explicitly conditional.

### 1.3 Reference repository

The Round 3 Gemini and Qwen documents have been read from the current `Misora-Reference` main branch.

The consolidated review should use the target commit above as its code baseline and should identify the Reference commit used for the final decision ledger.

---

## 2. PROJECT LEAD'S TWO ROUND 3 ANSWERS — ACCEPTED AND LOCKED

Both answers resolve the final questions raised by Gemini and Qwen.

### 2.1 QW-B13 — Preserve command IDs 35 and 32

**GPT verdict: AGREE — PROJECT LEAD DECISION ACCEPTED.**

The current project must preserve:

- `cmd_id == 35` for the narration representation.
- `cmd_id == 32` for the subtitle representation.

These numeric IDs must not be automatically rewritten based on a command-name mapping, a reference-tool mapping, or an assumption about another command table.

The hard guardrail is:

**Do not change binary command ID 35 or 32 until a real production `.unity3d` fixture containing the relevant narration and subtitle records proves that a different binary representation is required.**

This applies to:
- `_CMD_MAP` corrections.
- `_INV_CMD_MAP` corrections.
- AST kind conversion.
- v2 text serialization and parsing.
- Binary serialization.
- Raw Commands display-name cleanup.

Command display names and binary identity must be treated as separate concerns.

A readable command label may be corrected without silently changing the underlying numeric command ID.

The existing `cmd_id == 0` remapping defect must also be fixed independently. A display-name cleanup must never reintroduce a command-ID rewrite.

**Implementation guardrail:** Add regression tests proving that records with IDs 35 and 32 retain those exact numeric IDs through the supported serialization paths. A production fixture is still required before making claims about the game's authoritative expected semantics.

### 2.2 QW-B01 — Clearing a speaker must not merge narration boxes

**GPT verdict: AGREE — PROJECT LEAD DECISION ACCEPTED.**

When the speaker is cleared between two narration boxes, they must remain two separate boxes.

The editor must not silently merge them merely because both boxes now have an empty speaker and the same projected kind.

The required behavior is:

- Preserve the original box distinction.
- Preserve the primary record identity where possible.
- Insert the minimum required structural boundary when a kind conversion would otherwise merge adjacent boxes.
- Rebuild the AST projection only after the mutation has been performed safely.
- Ensure the resulting boxes remain independently editable and undoable.

This is not an optional UI preference. It is a document-structure invariant.

The implementation must not solve the problem by silently merging text, discarding a box, or relying on a stale positional index after the projection changes.

**Required regression case:** Two adjacent narration boxes must remain separate after speaker clearing, save/reload, and Undo/Redo.

Both Project Lead answers are now considered settled requirements. They should be recorded in the canonical ledger and should not be asked again in later rounds.

---

## 3. RESPONSE TO GEMINI ROUND 3

**Overall verdict: AGREE — CONFIRMED.**

Gemini's Round 3 review is consistent with my Round 2 position.

I agree with the following conclusions:

1. The Project Lead's decisions on `.misora`, Raw Commands, the All Script MTL Drawer, Import from XUAT, and native overflow behavior are sufficiently settled.
2. The second-reviewer verification of `GEM-B01..B16`, `GEM-B19a..f`, and `GEM-N01` is now complete according to the submitted Qwen line-level audit.
3. Qwen's newly surfaced AST, structural ownership, CSIF, backup, and undo defects must be incorporated into the canonical ledger.
4. The existing Group A–G dependency order from GPT Round 2 and Claude's DEP-1..DEP-10 remains a good basis for implementation sequencing.
5. The two remaining Project Lead questions are now resolved by the Project Lead's explicit answers in this conversation.

I especially agree with Gemini's adoption of the following rule:

If a persisted Translation Lock identity cannot be matched confidently when reopening a `.misora` workspace, Misora must leave that lock unresolved and notify the user. It must never silently transfer the lock to a different box.

This is an important safety property for workspace restoration.

---

## 4. GPT'S INDEPENDENT VERDICTS ON QWEN'S NEW FINDINGS

I checked the relevant source paths and methods against target HEAD `683724e`.

### 4.1 QW-B01 — Kind conversion can merge adjacent boxes

**Severity: P0**  
**GPT verdict: AGREE — CONFIRMED.**

Relevant source:
- `core/story_ast.py`
- `StoryDocument.set_box_kind()`
- `StoryDocument.inject_box()`
- `StoryDocument._rebuild_boxes()`

The current implementation changes a box's kind and then rebuilds the box projection.

The projection groups adjacent text records based on their kind and speaker. Consequently, converting a spoken dialogue box into narration can cause it to merge with an adjacent narration box.

`inject_box()` subsequently accesses the box again using its original positional index. That index may now refer to a different box or no longer exist.

The opposite conversion also requires care: the speaker property and the underlying segment records must remain consistent after the projection is rebuilt.

**Required fix:**

- Capture the target's primary `Record.uid` before mutation.
- Resolve the target through record identity rather than assuming its old `box_index` remains valid.
- Preserve distinct boxes when converting kind.
- Insert a minimal, valid boundary only when needed to prevent an unintended merge.
- Rebuild the projection after the full record mutation.
- Make the operation undoable without losing the original segment structure.

The Project Lead's new ruling resolves the intended behavior: clearing a speaker must preserve separate narration boxes.

Do not implement implicit merging as a shortcut.

### 4.2 QW-B02 — Sparse CSIF indices can shift during kind conversion

**Severity: P1**  
**GPT verdict: AGREE — CONFIRMED.**

Relevant source:
- `core/script_codec.py`
- `apply_to_document()`
- `core/story_ast.py`
- `inject_box()`

Sparse CSIF uses absolute 1-based document addressing.

The implementation currently validates sparse indices before applying dialogue changes, but then applies changes sequentially through `inject_box()`.

If an earlier operation changes box kind and modifies the box projection, later positional indices may no longer identify the original targets.

This is independent of the earlier preview/undo index mismatch and metadata atomicity findings. All belong to the same safe-import transaction.

**Required fix:**

1. Validate every sparse index before mutation.
2. Capture the target primary `Record.uid` for every sparse block before mutation.
3. Resolve each target by identity during application.
4. Ensure kind conversion does not unexpectedly change the document's box count.
5. Apply metadata and dialogue changes atomically.
6. Roll back all changes if any target fails.

Do not allow an import to partially update metadata or earlier boxes before a later target fails.

The implementation should use a staged document or an equivalent transaction mechanism rather than trusting the current positional projection throughout a mutating loop.

### 4.3 QW-B13 — Command names, default breakers, and binary ID risk

**Severity: P1 for naming and projection; fixture-dependent for narration/subtitle semantics**  
**GPT verdict: AGREE WITH THE PROJECT LEAD'S HARD GUARDRAIL.**

Relevant source:
- `core/story_ast.py`
- `_CMD_MAP`
- `_INV_CMD_MAP`
- `DEFAULT_BREAKERS`
- `StoryDocument._rebuild_boxes()`
- `StoryDocument.get_metadata()`

The current command map and default breaker definitions need reconciliation.

The projection currently relies on command names for some structural behavior. The command map contains naming inconsistencies, and the existing breaker set does not represent every non-dialogue structural command identified by Qwen.

I agree that the safe work can proceed in two separate parts:

**Part A — Safe source corrections**

- Reconcile readable command names with the observed record semantics.
- Correct the default breaker classification for commands that have been verified as structural breakers.
- Preserve the current dialogue projection for `cmd_id == 6`.
- Preserve the voice-cue interpretation of `cmd_id == 12` records with `vo_` arguments.
- Ensure command-name cleanup does not modify binary identity.
- Add regression tests for the affected records.

**Part B — Fixture-gated work**

Do not change IDs 35 or 32.

The Project Lead's decision is explicit. Keep both numeric IDs unchanged until a real production `.unity3d` fixture containing narration and subtitle records establishes otherwise.

I also reiterate that `cmd_id == 0` preservation must be handled separately from command naming. The numeric command ID is the authoritative identity during binary serialization.

### 4.4 QW-B14 — Moving and deleting boxes can orphan voice cues

**Severity: P1/P2**  
**GPT verdict: AGREE — CONFIRMED.**

Relevant source:
- `core/story_ast.py`
- `StoryDocument.move_box()`
- `StoryDocument.delete_boxes()`
- `StoryDocument._rebuild_boxes()`

The current structural operations collect the segment record UIDs, but do not consistently include the associated voice-cue record.

The projection explicitly recognizes a voice cue represented by `cmd_id == 12` with an argument beginning with `vo_`.

That cue is associated with the following box and must not be left behind when the box moves.

**Required structural ownership contract:**

- A `cmd_id == 12` record with a `vo_` argument immediately preceding the first segment of a box is attached to that box.
- Moving the box moves its attached voice cue.
- Deleting the box handles its attached voice cue consistently.
- Empty projected tap-breakers may be removed only when positively identified as structural boundary records.
- Never remove voice cues as if they were tap-breakers.
- Never silently delete unknown or meaningful interstitial commands.
- Snapshot every removed or moved structural record needed for exact Undo/Redo.
- Prevent duplicate boundary breakers when moving and reinserting boxes.

This finding must be merged with `Grok-B04` and `CLAUDE-N09` into one canonical structural-ownership task.

Do not create separate patches for `move_box()`, `delete_boxes()`, and `insert_box()` that use conflicting ownership assumptions.

### 4.5 QW-B15 — CSIF backslash parity corruption

**Severity: P2**  
**GPT verdict: AGREE — CONFIRMED.**

Relevant source:
- `core/script_codec.py`
- `serialize()`
- `_parse_csif()`

The serializer escapes body lines beginning with `@@`, but does not correctly preserve an existing backslash prefix before `@@`.

The parser removes one escape prefix from the encoded header-like line. A body line already beginning with `\@@` can therefore become `@@` after a round-trip.

**Required fix:**

The serializer must add exactly one escape backslash to body lines containing zero or more leading backslashes followed by `@@`.

The parser must remove exactly one escape backslash from that encoded family.

Examples that must round-trip exactly:

- `@@example`
- `\@@example`
- `\\@@example`
- `\\\@@example`

Do not solve this by stripping all leading backslashes or normalizing the original content.

Add round-trip tests for every case above, including body lines containing ordinary backslashes that do not precede `@@`.

### 4.6 QW-B17 — Multi-file text Replace All backup collisions

**Severity: P2**  
**GPT verdict: AGREE — CONFIRMED.**

Relevant source:
- `misora.py`
- `on_replace_all()`

The text-file branch uses a second-resolution timestamp and a flat backup filename based on `fpath.stem`.

Two different files with the same stem can collide. Repeated replacements within the same second can also target the same backup path.

The bundle branch already uses microsecond precision, but the text branch does not.

**Required fix:**

Use collision-resistant backup names for all Replace-All targets.

Acceptable components include:
- Microsecond timestamp.
- Short deterministic hash of the normalized full source path.
- Mirrored relative directory structure.

The implementation must also ensure the backup path does not already exist before writing.

This is a backup-integrity task, not merely a filename-style cleanup.

### 4.7 QW-B22 — Undo coalescing can merge different boxes

**Severity: P2**  
**GPT verdict: AGREE — CONFIRMED.**

Relevant source:
- `core/undo_journal.py`
- `MasterUndoJournal.record()`

The current `same_box` condition uses:

`same box UID OR same box index`

This is unsafe when both deltas have non-null but different UIDs and happen to share the same positional index.

**Required fix:**

- If both `box_uid` values are non-None, require UID equality.
- Use `box_index` as a fallback only when at least one UID is None.
- Keep the source, file, and coalescing-time checks.

Regression test: two distinct records with different UIDs but the same box index must never coalesce into one edit operation.

### 4.8 QW-E05 — Unbounded `removed_records` growth

**GPT verdict: AGREE — CONFIRMED.**

`StoryDocument.delete_boxes()` removes records from `self.records` and also adds their UIDs to `removed_records`.

Because record UIDs are monotonic, retaining every removed UID indefinitely can accumulate unnecessary state during a long editing session.

The fix must first establish whether any undo or serialization path still depends on these tombstones.

If the records are already physically removed and the tombstones serve no remaining purpose, do not keep them indefinitely. Otherwise, implement a bounded lifecycle tied to the relevant document and undo history.

Do not prune IDs while an operation still needs them for rollback.

### 4.9 QW-E06 — Search fallback returns inaccurate match spans

**GPT verdict: AGREE — CONFIRMED.**

Relevant source:
- `core/search_engine.py`
- `ProjectSearchEngine.search_file()`

When raw text matches but cleaned text does not, the fallback currently maps each raw match to the entire clean-text span.

This can make search highlighting misleading and does not represent the actual location of the match.

Use a proper raw-to-clean span mapping or explicitly represent the result as an approximate raw-text match.

Do not fabricate exact character offsets.

### 4.10 QW-E07 — Missing `Any` import

**GPT verdict: AGREE — CONFIRMED, WITH SEVERITY PRECISION.**

`core/search_engine.py` uses `Any` in a type annotation but does not import it from `typing`.

Because the module uses postponed annotation evaluation, this should not be described as an unconditional startup crash.

However, type-hint introspection and tooling that evaluates annotations can fail.

Add the missing import and an annotation-resolution check.

This is a small hygiene fix, not a P0/P1 data-integrity defect.

### 4.11 QW-E08 — Hard-coded DeepL User-Agent version

**GPT verdict: AGREE — CONFIRMED.**

Relevant source:
- `core/mtl_engine.py`
- `MTLEngine._translate_deepl()`

The DeepL request identifies the application with a hard-coded `1.3` version although the inspected application is v1.4.0.

Use a single application-version source rather than duplicating a stale version string.

This should remain a small maintenance fix.

### 4.12 QW-R03 — Missing v2 base64 surrogate emission

**GPT verdict: AGREE — CONFIRMED.**

Relevant source:
- `core/story_ast.py`
- `decode_arg()`
- `encode_arg()`
- `escape_arg()`
- `unescape_arg()`

The decoder uses `surrogateescape`, and `unescape_arg()` accepts a `\b64:` representation. However, `escape_arg()` does not emit that representation for text containing surrogate-escaped bytes.

This is a genuine gap in the v2 losslessness contract.

**Required fix:**

When an argument contains surrogate-escaped bytes that cannot safely be represented as ordinary UTF-8 text, serialize the original bytes through the `\b64:` surrogate representation.

The result must decode back using the same `surrogateescape` semantics.

Add binary-to-v2-to-binary regression tests with invalid UTF-8 byte sequences.

This must be folded into `GEM-B16` and the v2 losslessness gate. It must be completed before any feature is allowed to depend on v2 as a lossless document representation.

---

## 5. DEDUPLICATION AND FINAL FINDING OWNERSHIP

**GPT verdict: AGREE WITH GEMINI'S DEDUPLICATION MAP AND QWEN'S ACCEPTANCE.**

The canonical ledger must contain each underlying defect only once.

The following mappings should be retained:

| Qwen finding | Canonical finding / group |
|---|---|
| QW-B01 | New P0 AST kind-conversion / projection identity defect |
| QW-B02 | GPT-B04 / GPT-B05 / GEM-B04 — sparse CSIF transaction |
| QW-B13 | GEM-B16 / GPT-B02 — command mapping, breaker projection, binary identity |
| QW-B14 | Grok-B04 / CLAUDE-N09 — structural ownership and voice-cue attachment |
| QW-B15 | New CSIF escaping defect |
| QW-B17 | New multi-file Replace-All backup collision |
| QW-B22 | New Undo journal identity/coalescing defect |
| QW-E05 | New AST tombstone lifecycle issue |
| QW-E06 | GPT-B08 / GEM-B18 — search span correctness |
| QW-E07 | Small search-engine annotation hygiene |
| QW-E08 | MTL engine version metadata hygiene |
| QW-R03 | GEM-B16 / GPT-B02 — v2 losslessness |

Other mappings from Gemini R3 §2B are accepted.

Keep the following deferred or out of scope:

- `Grok-B07` / `QW-B19`: retain the current empty-argument space sentinel until live-client evidence supports a change. Add tests, but do not blindly alter the binary format.
- `QW-E01`, `QW-E02`, `QW-E04`: measure-first performance observations.
- `QW-F01`: multi-file Replace-All dry-run diff pane is outside the agreed U-B1..U-B34 scope.
- `GEM-F05`: Text-only Story Dataminer.
- `GEM-F06`: Watermark / Hybrid Pin.

No broad architectural rewrite of `misora.py` should be introduced as part of this stabilization cycle.

---

## 6. FINAL ACCEPTANCE OF THE PROJECT LEAD'S LOCKED DESIGN REQUIREMENTS

GPT continues to accept the Project Lead's finalized decisions.

### 6.1 `.misora` workspace

`.misora` v1 stores references and workspace state only:

- Schema version.
- Relative and absolute file paths.
- Active file and box.
- View and search-scope state.
- Per-document stable-key Translation Locks.

It must not store unsaved story drafts or duplicate binary story content.

Use `(box_ordinal, sha256(original_jp_text))` as the persisted lock identity.

Use runtime `box.uid` only during the live editing session.

If a saved lock cannot be matched confidently, leave it unresolved and notify the user.

### 6.2 View naming and Raw Commands

Locked labels:

- `Dialogue`
- `All Script`
- `Dialogue Preview`
- `All Script Preview`
- `Raw Commands`

Do not use `Raw Script` as the bottom pane name.

### 6.3 Native overflow and Preview

Use the Project Lead's direct in-game test:

- Horizontal safe boundary: 50 digit-widths.
- Vertical safe boundary: three lines.
- Overflow warning at four or more lines.
- No automatic shrinking.
- `wrap="none"` or equivalent native overflow visualization.
- Pixel measurement calibrated to the actual editor font.
- Dialogue and All Script Preview share one measurement helper.
- Box 0 Summary remains deferred until its game limit is measured.

The editor-font ruler is an estimate of game behavior, not a claim that the editor font is identical to the game font.

### 6.4 Multi-segment editing

Allow normal editing.

Show a non-blocking `N segs` indicator.

Undo must preserve segment-level content through `old_seg_texts` and `new_seg_texts`.

Internal Copy/Paste must preserve the complete `BoxSnapshot`, including:

- `seg_texts`
- `voice_cue`
- `extra_args`

### 6.5 All Script MTL Drawer

Use exactly two Text widgets:

1. Read-only multi-line list with clickable per-box tagged entries.
2. Shared editable scratchpad.

Use the five agreed status indicators and theme-aware styling.

Translation Lock must be enforced at the model/application layer, not only through disabled controls.

### 6.6 Import from XUAT

Keep this as a separate Import-menu workflow.

Use the bounded source directory:

`BepInEx\Translation\en\Text`

Use one background indexer in `core/xuat_index.py`, unified with the existing cache.

The resolver must retain the agreed paired fixed `3 × 50` read-only display, duplicate navigation, provenance, Skip controls, lock skipping, filters, backslash-aware newline conversion, exact pre-apply summary, and one atomic Undo operation.

The XUAT feature depends on immutable Japanese source keys and bounded project roots.

It must not silently overwrite ambiguous translations.

---

## 7. UPDATED PHASE 2.5 DEPENDENCY ORDER

GPT continues to recommend the Group A–G structure from Round 2, with Qwen's new findings incorporated.

### Group A — Baseline and ledger integrity

- Pin target HEAD `683724e`.
- Reconcile `PROJECT_STATE.md`, README, and AGENTS.
- Correct stale resolved statuses.
- Reconcile test-count arithmetic and filenames.
- Separate verified defects, fixture-dependent questions, and deferred items.
- Establish canonical finding IDs and acceptance tests.

### Group B — Core AST, projection, and serialization integrity

- GPT-B01: reject truncated binary records.
- GPT-B02 / GEM-B16 / QW-R03: v2 and command-ID losslessness.
- QW-B13: command mapping and breaker projection, preserving IDs 35 and 32.
- QW-B01: kind conversion and stable box identity.
- QW-B14 / Grok-B04 / CLAUDE-N09: structural ownership and voice cues.
- Grok-B01 / GEM-B09: multi-segment editing and full BoxSnapshot preservation.
- GPT-B04 / GPT-B05 / GEM-B04 / QW-B02: atomic sparse CSIF application.
- QW-B15: CSIF escape-parity round-trip.
- GPT-B12: real-fixture verification of non-target bundle preservation.

### Group C — Document state and Undo integrity

- GEM-B05: per-document state and lock persistence across file switches.
- Grok-B02: mutate before recording Undo.
- Grok-B03: safe batch cancellation lifecycle.
- GEM-B08: non-contiguous Cut/Undo correctness.
- GEM-B10: enforce Translation Lock across every mutation path.
- QW-B22: UID-safe Undo coalescing.
- QW-E05: bounded removed-record/tombstone lifecycle.

### Group D — Search, Replace, and project identity

- GPT-B07: Match Case and Ignore Whitespace correctness.
- GPT-B08 / GEM-B18 / Grok-E02: snapshot isolation and skipped-path reporting.
- QW-E06: accurate raw-to-clean search spans.
- QW-E07: typing annotation import.
- GEM-N01: bounded project roots and stale-root cleanup.
- GEM-B02: multi-file Replace-All/cache integrity.
- Grok-B05 / QW-N01: shared matcher and lock policy for Find, Replace Next, and Replace All.
- QW-B17: collision-resistant Replace-All backup paths.

### Group E — XUAT integrity

- GEM-B12: immutable Japanese source keys.
- GPT-B09: conflict-aware save behavior.
- GEM-B19f: safe XUAT atomic file writes.
- One shared XUAT index architecture.
- Keep Import from XUAT separate from the MTL Drawer.

### Group F — MTL and application lifecycle

- GPT-B03 / GEM-B11: stale translation request protection.
- GPT-B06: main-thread-only Tk scheduling.
- GEM-B19a–c: UnityPy, logger, and startup lifecycle.
- GPT-B10: logger completion barrier and shutdown.
- GPT-B11: explicit credential-protection failure.
- GEM-B19d/e: splash sorting and empty-document save safety.
- QW-E08: application-version metadata for DeepL.

### Group G — Approved UI and workflow features

Implement the approved UX slices after their required integrity dependencies pass:

- U-B1..U-B21: search, toolbar, selection, drawers, and workspace.
- U-B22..U-B28: rulers and native game-style preview.
- U-B17/U-B18: references-only `.misora` session workflow.
- U-B31: editable Raw Commands only after the lossless document transaction is ready.
- U-B32/U-B33: MTL Drawer.
- U-B34: Import from XUAT.

This ordering is a dependency plan, not permission to skip acceptance tests or combine unrelated fixes into a large unreviewable patch.

---

## 8. ROUND 3 REGRESSION TEST ADDITIONS

The existing GPT Round 2 acceptance list remains valid. Add the following focused tests.

1. Converting a spoken box to narration beside another narration box must preserve two separate boxes.
2. Clearing a speaker must not merge adjacent narration boxes.
3. Kind conversion must not cause `inject_box()` to mutate the wrong box or raise an avoidable `IndexError`.
4. Sparse CSIF with multiple kind-changing targets must update the originally intended absolute 1-based targets.
5. Invalid sparse CSIF must leave metadata and all dialogue records unchanged.
6. Records with command IDs 35 and 32 must retain those IDs during supported round-trips.
7. Moving a box must move its attached `cmd_id == 12` `vo_` cue.
8. Deleting a box must not orphan the attached voice cue.
9. Structural edits must preserve unknown and meaningful interstitial commands.
10. Moving or deleting boxes must not create duplicate empty tap-breakers.
11. CSIF body lines with zero, one, or multiple backslashes before `@@` must round-trip exactly.
12. Multi-file text Replace-All backups must not collide for same-stem files or repeated operations.
13. Undo coalescing must not combine two different non-null box UIDs merely because their indices match.
14. Long editing/deletion sessions must not accumulate unnecessary unbounded record tombstones.
15. Raw-text search fallback must not fabricate whole-box match locations.
16. `typing.get_type_hints()` must be able to resolve the search-engine annotations.
17. DeepL User-Agent must use the application version source rather than a hard-coded stale release.
18. Invalid UTF-8 argument bytes must survive binary → v2 → binary round-trip through the `\b64:` surrogate representation.

All tests must include relevant Undo/Redo or failure-path coverage where applicable.

A passing unit test is not a substitute for a real production fixture when the behavior depends on the game's actual binary format.

---

## 9. ROUND 3 CONVERGENCE STATUS

### GPT's final verdicts

| Area | GPT verdict |
|---|---|
| Gemini Round 3 overall review | AGREE |
| Qwen's second-reviewer verification of GEM findings | AGREE |
| QW-B01 / QW-B02 | AGREE — CONFIRMED |
| QW-B13 | AGREE — preserve IDs 35 and 32 |
| QW-B14 | AGREE — CONFIRMED |
| QW-B15 / QW-B17 / QW-B22 | AGREE — CONFIRMED |
| QW-E05..E08 / QW-R03 | AGREE — CONFIRMED |
| Project Lead answer (a) | ACCEPTED AND LOCKED |
| Project Lead answer (b) | ACCEPTED AND LOCKED |
| QW-B19 empty argument sentinel | DEFERRED — fixture evidence required |
| GEM-F05 / GEM-F06 | DEFERRED / OUT OF SCOPE |

### Phase 2 gate

**GPT POSITION: READY TO LOCK FOR PHASE 2.5.**

The two remaining Project Lead confirmations have now been answered.

I have no remaining technical disagreement with the consolidated direction presented by Gemini and Qwen.

However, the overall panel should record Claude's and Grok's final nods before declaring the cross-AI Phase 2 ledger fully locked.

The final canonical ledger must contain:

- One deduplicated entry per underlying defect.
- Canonical ID and severity.
- Source path and method.
- Evidence and verification status.
- Project Lead decisions.
- Fixture-dependent restrictions.
- Dependencies.
- Regression tests and acceptance criteria.
- Explicit deferred and out-of-scope items.

**Phase 2 review readiness does not itself authorize code implementation.** The implementation phase must follow the Project Lead's explicit instruction and the locked ledger.

---

## 10. SOURCE-HYGIENE NOTES

Two document issues must remain visible in the Reference repository's audit trail:

1. `Phase_1_Gemini.md` was reported by Gemini R2 to contain Claude's Phase 1 dossier by mistake. It must not be treated as Gemini's independent Phase 1 research without correcting the document provenance.
2. `Phase_2R1_Claude.md` was reported by Grok R1 as an empty file. The panel should not count that document as a valid peer review unless its contents are restored or its status is explicitly recorded.

The Project Lead's clarification that local `docs/` and `storydata_1001005.unity3d` fixtures were intentionally removed from GitHub remains accepted. Do not reopen the earlier local-file access questions.

---

**END OF GPT PHASE 2 ROUND 3 RESPONSE**

**Final GPT recommendation:** Consolidate the deduplicated Phase 2.5 ledger using GPT Group A–G ordering and Claude DEP-1..DEP-10, incorporate Qwen's new confirmed defects, record both Project Lead answers as locked decisions, and obtain Claude/Grok's final confirmation before declaring full panel convergence.