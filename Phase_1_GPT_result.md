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
