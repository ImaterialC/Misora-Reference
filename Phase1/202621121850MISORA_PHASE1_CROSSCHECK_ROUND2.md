# MISORA EDITOR — PHASE 1 INDEPENDENT CROSS-CHECK (ROUND 2)

**Review status:** Independent technical review; proposed for Phase 1 debate, not final consensus  
**Date:** 2026-11-21  
**Target project:** `ImaterialC/Misora-Editor`  
**No code changes made. No Copilot implementation prompt produced.**

---

## 0. Scope, source of truth, and evidence quality

### 0.1 Authoritative code baseline

The user has designated the uploaded local archive as authoritative when it differs from GitHub `main`.

- Reviewed archive: `Misora-Editor.zip`
- Local `misora.py`: **510,461 bytes**
- Local `misora.py` SHA-256: `2188eab968e031d4d5469f117f3cfb8403dc27622b5b6009d38b3880dd97babe`
- ZIP SHA-256: `9a313a71066c93c817edeca636d5fb19dfe9012ce789fec1f3d2f0eeadc3e930`
- GitHub `main` is still an older version: fetched `misora.py` blob SHA `ba6ae25c3f7088392d968ed1d5915fe08bd87ed8`; its reported file size is about 499 KB, not the 510,461-byte local file.

**Important:** Findings in this report refer to the uploaded local ZIP unless explicitly labelled as findings in the separate `Reference-Files/priconne-adv-tools` code. Do not use the older GitHub `main` file to reject or validate local-only behavior. Before any Copilot edit, verify that Copilot's active workspace is the same local tree as this archive. A Cloud Agent operating on the stale `main` branch would edit the wrong baseline.

### 0.2 Debate material inspected

The public `Reference-Files` repository was accessible. The main readable materials were:

- `202621121617gemini1.txt` — Gemini's preliminary hypotheses.
- `202621121618grook1.txt` — Grok's Phase 0 memo.
- `202621121653Qwen1.txt` — an echo of the earlier Assistant A research brief, not an independent Qwen review.
- `202621121658GPT1.txt` — the earlier independent audit report.
- `202621121735gemini2.txt` — Gemini's cross-check, MTL Drawer and XUAT discussion.
- `202621121751Qwen2.txt` — Qwen's first substantive independent cross-check, legacy-tool audit and MTL design critique.
- `202621121801gemini3.txt` — Gemini's user-clarification and Left Sidebar review.
- `202621121815Qwen3.txt` — Qwen's follow-up delta, native DnD correction, workspace and console findings.
- `202621121819gemini4.txt` — byte-identical duplicate of `gemini3` in the repository tree; not a second independent review.
- `202621121825grook2.txt` — empty (0 bytes); contains no review.
- `PromptAgent/github_copilot_ai_prompting_reference.md` and `PromptAgent/google_antigravity_ai_prompting_reference.md` — prompting playbooks, used only as guidance for later prompt structure, not as evidence about Misora defects.

The user explicitly stated that `Chat history` is redundant. It is excluded from this review.

### 0.3 Verification performed

- Python compile check: `python -m compileall -q misora.py core assets tests` — **PASS**.
- `python -m unittest tests.test_script_codec -v` — **14 passed**.
- The full 100-test suite was **not** independently completed: this Linux environment has no Tk display and UnityPy is not installed. The 100/100 result in `PROJECT_STATE.md` remains a previously recorded Windows result, not a result reproduced here.
- Direct runtime reproductions were performed for search normalization, UndoJournal file-dirty behavior, XUAT source-key drift, and Misora v2 serialization of a reserved category-name argument.
- Static source review was performed against the uploaded local files. Windows-only Tk/Win32 behaviors still require real Windows verification.

---

## 1. Executive assessment

The debate found real integrity, threading, state-management and interop issues. The highest-risk problems are not cosmetic and should be addressed before building the MTL Drawer or Import from XUAT UI.

The most important accepted findings are:

1. Failed file opening can leave the application pointing at a new path while retaining the previous document and bundle objects.
2. Closing a dirty file can close it even after its Save operation fails.
3. Exit can prompt about all dirty documents but only save the active document.
4. Compiled Preview can cause a plain-text file to be saved from rendered widget content rather than the raw model text.
5. Multi-file Replace All can discard unsaved active edits, leave other cached documents stale, bypass Translation Lock on bundle paths, and cannot undo bundle replacements.
6. Internal Copy Box → Paste Box flattens segment structure and drops voice cue / extra argument metadata.
7. XUAT sync replaces the original JP lookup key with English after saving; the existing UID-keyed JP registry is not wired into the GUI.
8. Batch translation and asynchronous MTL callbacks cross the Tkinter thread boundary unsafely.
9. Search workers read live mutable documents, and search failures can be silently swallowed.
10. Misora's local v2 serializer/parser has a reserved-category argument round-trip bug and does not fully share the external ADV tool's v2 escape contract.

These should take precedence over new UI features.

---

## 2. Consolidated findings — confirmed in the local Misora ZIP

Severity labels here are relative engineering priorities, not a claim that every defect has already caused user data loss in production.

### DATA-INTEGRITY / SAVE SAFETY

#### F1 — `OPEN-FAILURE-STATE-CORRUPTION` — NEW — P0/P1

**Evidence:** `misora.py:6066-6108`, `6110-6177`, `on_save()` at `7855-7924`.

`open_file()` assigns `self.current_file_path = file_path` and resets some state before attempting to load the new asset. If `load_bundle_story()` or `StoryDocument.from_v2_text()` fails, the exception handler shows an error but does not roll back or clear the previous `current_doc`, `current_unity_env`, `current_text_obj`, or `is_bundle_file` state.

This leaves an inconsistent active-document tuple: the path can refer to the failed new file while the in-memory document and Unity objects still refer to the previously open file. `on_save()` uses the active path together with the active document/environment fields. Depending on the previous document type, a later save can write old content to the new path or create a wrongly named copy of the old bundle. The mismatch is definite; the exact write path depends on the previous active-file type.

**Minimal direction:** Stage the new document, environment, TextAsset, mode and metadata in local variables. Commit them to `self.*` only after a successful load. On failure, preserve the complete previous active state. Avoid a global open/load framework.

**Regression tests:** Open valid A; attempt to open an existing but invalid/corrupt B; assert A remains the active path and document; invoke Save and verify B is untouched. Test bundle→bundle, v2→v2 and text→bundle failure transitions.

#### F2 — `CLOSE-FILE-IGNORES-SAVE-FAILURE` — CONFIRMED — P0/P1

**Evidence:** `misora.py:9027-9046`; `on_save()` catches errors at `7952-7954` and returns without a success value.

When a dirty file is closed and the user selects Save, `close_file()` calls `on_save()` and then unconditionally deletes the `open_documents` entry and prunes its undo history. It does not verify that the save succeeded or that the document is clean. A disk error, bundle verification failure or other save exception can therefore be followed by closing the only in-memory copy of the edits.

**Minimal direction:** Make the save path report success explicitly, or check a reliable per-document saved/dirty state after it returns. Abort close if Save failed. Do not infer success merely because `on_save()` returned.

**Regression tests:** Mock a failed text write and failed bundle verification; choose Save in the close flow; assert the document remains open, dirty and undoable.

#### F3 — `EXIT-SAVES-ONLY-ACTIVE-DOCUMENT` — CONFIRMED — P0/P1

**Evidence:** `misora.py:1349-1363`.

`_on_app_exit()` prompts if either the active document or any cached `open_documents` entry is dirty. If the user selects Yes, it calls `self.on_save()` once. `on_save()` saves only the active document, and exit checks only `self.is_dirty`. Other dirty cached documents can be discarded when the application destroys itself.

**Minimal direction:** Save every dirty open document, or present an explicit per-file Save/Discard/Cancel decision. Abort exit if any requested save fails. Keep the implementation aligned with the existing `open_documents` cache; do not introduce a new session manager.

**Regression tests:** Open two files, modify both, make one inactive, trigger exit and choose Save. Verify both files are saved. Then force one save failure and verify the application remains open with the failed document intact.

#### F4 — `PLAINTEXT-SAVE-COMPILED-PREVIEW-CORRUPTION` — CONFIRMED — P1

**Evidence:** compiled rendering in `misora.py:6179-6207`; plain-text Save reads the widget at `7863-7874`.

For plain-text files, Compiled Preview inserts rendered NGUI content into the editor widget and disables it. The plain-text Save branch then reads the widget contents and writes those rendered contents to disk. This can permanently remove or transform the original markup rather than saving `_plain_text_content`.

**Minimal direction:** Save from the authoritative raw plain-text model, not a compiled/read-only presentation widget. If the content is not editable in compiled mode, do not silently persist the preview representation.

**Regression tests:** Open a text file containing NGUI tags; enable Compiled Preview; save; assert the file bytes/text still contain the original raw markup. Repeat in Page and Continuous views.

#### F5 — `BULK-REPLACE-ALL-CLOBBERS-OPEN-DOCUMENT-STATE` — CONFIRMED — P0/P1

**Evidence:** `misora.py:8609-8802`, especially `8722-8737`, `8762-8798`.

Several issues converge in multi-file Replace All:

- Bundle prefiltering scans raw `.unity3d` / `.asset` bytes using `raw.count(find_text.encode(...))`, while replacement later searches decoded `StoryDocument` dialogue. Binary byte counts are not a reliable count or filter for decoded dialogue matches.
- Bundle replacements are saved but not added to `per_file_deltas`; only plain-text replacements are journaled. Undo therefore cannot restore the bundle side of a mixed operation.
- Plain-text scanning uses `errors="ignore"`, and the replacement read uses `errors="replace"`; invalid source bytes can be silently skipped or rewritten as U+FFFD.
- Forward and undo text writes use direct `Path.write_text()` rather than atomic replacement.
- The bundle branch does not consult the Translation Lock before replacing matching boxes.
- If the active file is affected, the function calls `open_file(..., reload_from_disk=True)`, which can discard unsaved in-memory edits.
- Other already-open matching documents are not all refreshed or reconciled after their on-disk bundle/text content changes. A later save of a stale cached document can overwrite the bulk replacement.
- Candidate paths can be discovered more than once when configured roots overlap; the dictionary de-duplicates paths for replacement but `total_matches` can count the same source more than once. This is a lower-severity count/reporting issue.

**Minimal direction:** Treat this as a data-integrity task, not a search UI redesign. Use the structured bundle loader for bundle candidates; strict decoding and an explicit skip/report path for unsupported text encodings; atomic writes for text files and undo; journal bundle changes using a bounded backup/snapshot strategy; protect or explicitly reconcile dirty and locked open documents; and update/invalidate every affected in-memory cache. Preserve the existing `UndoJournal` model.

**Important scope note:** This cluster is too broad for one vague “fix Replace All” prompt. It should be split into small, ordered steps with tests and a clear shared transaction boundary. Do not implement a new general-purpose transaction framework unless current APIs prove insufficient.

**Regression tests:**
- Bundle matches that exist in decoded TextAsset content.
- Bundle with binary bytes that happen to contain the query but no decoded dialogue match.
- Mixed bundle + text replacement followed by Undo and Redo.
- Invalid UTF-8 text file must be skipped/reported, never rewritten lossily.
- UTF-8 BOM, CRLF and LF preservation.
- Active dirty document is not discarded.
- Another open cached document is not left stale.
- Locked matching boxes remain unchanged.
- Simulate write failure; original file remains intact.
- Overlapping roots do not double-count matches.

#### F6 — `BOX-PASTE-FLATTENS-INTERNAL-SNAPSHOTS` — CONFIRMED — P1

**Evidence:** `misora.py:6827-6888`; `BoxSnapshot.from_box()` and fields in `core/story_ast.py:207-230`.

The internal `_box_clipboard` already contains `BoxSnapshot` objects with segment breakdown, voice cue and extra args. However, `on_box_paste()` converts those snapshots into flattened `DialogueBlock(text=snap.clean_text)` objects, then rebuilds snapshots with `seg_texts=[b.text]`, empty `voice_cue`, and no preserved per-segment `extra_args` / raw-break information.

This loses data during an internal copy/paste operation even though the internal clipboard format has enough information to preserve it. External CSIF is a separate case: its current per-box interchange representation is not inherently segment-lossless, so that limitation should be documented rather than disguised as a lossless round trip.

**Minimal direction:** For a valid internal `_box_clipboard`, insert the original snapshots (or faithful copies) directly. Keep the flattening adapter only for external clipboard/CSIF input.

**Regression tests:** Copy and paste a box with multiple segments, voice cue and extra arguments; assert the resulting snapshot and binary output preserve those fields. Keep a separate test documenting external CSIF behavior.

#### F7 — `XUAT-JP-KEY-DRIFT` — CONFIRMED — P1

**Evidence:** `misora.py:7926-7950`; existing registry helpers `core/xunity_sync.py:79-86`.

On Save, `orig_key` is read from `_original_box_texts`, used as the Japanese key, and then `_original_box_texts[b_idx]` is overwritten with `box_obj.clean_text`. After the first successful translation, that text is English. A later save can therefore search the XUAT dictionary using the English text rather than the original Japanese key. The existing `XUnitySyncManager.register_jp_key(box_uid, jp_text)` / `get_jp_key(box_uid)` helpers are present but not called by the GUI.

This is compounded by document switching: the cache-hit branch rebuilds `_original_box_texts` from the currently cached document's current `clean_text`, which may already be translated English.

**Minimal direction:** Register the immutable JP source once per stable `box.uid` when a document is loaded; always use the UID registry for sync; do not overwrite the source key after translation. Ensure UID-key data survives cached-document switches and structural edits. Avoid relying on list indices as identity.

**Regression tests:** Save the same translated box twice; the same original Japanese key must be used both times. Repeat after switching documents and after moving/inserting a box.

#### F8 — `V2-RESERVED-CATEGORY-ARG-ROUNDTRIP` — NEW — P1/P2

**Evidence:** local `core/story_ast.py:124-171`, `185-197`, `735-787`; external `priconne-adv-tools/advscript.py:94-120`.

Misora's v2 parser treats an unescaped line exactly equal to `System`, `Motion` or `Effect` as the record category (`story_ast.py:773-775`). But local `escape_arg()` does not escape those exact argument values (`124-138`). A direct runtime test with a `print` record containing `args=['Hero', 'System']` shows that `to_v2_text()` writes `System` as a bare line and `from_v2_text()` parses it as the category, dropping the argument. This is a **Misora self-round-trip bug**, not merely an external-tool mismatch.

There is also a cross-tool escape-contract mismatch. The external ADV v2 helper uses `\N`, `\L`, `\P`, `\s`, `\S`, and a leading backslash for the reserved category values. Misora's local decoder does not decode those forms; it instead uses `\x85`, `\u2028`, `\u2029` and lacks the external trailing-space/category escapes. Both claim `#!priconne-story v2`, so cross-tool import/export may silently alter text.

**Minimal direction:** Define and document one canonical v2 escaping contract shared by both tools, or explicitly version the incompatible dialects. Add migration-compatible parsing for the external forms. Do not silently change already-exported v2 files without regression fixtures.

**Regression tests:** Round-trip an argument exactly equal to each reserved category; trailing ASCII and ideographic spaces; NEL/U+0085; U+2028/U+2029; backslashes; escaped equals; and representative Japanese text through both toolchains.

### THREAD-SAFETY / ASYNC LIFECYCLE

#### F10 — `BATCH-TRANSLATE-MUTATES-TK-AND-DOCUMENT-FROM-WORKER` — CONFIRMED — P1

**Evidence:** `misora.py:11089-11145`.

The translation worker accesses the live `StoryDocument` and `Box` objects, mutates the document, records UndoJournal deltas, modifies `_modified_boxes` and `is_dirty`, and calls `self.after_idle()` for progress and completion. `end_batch()` is not protected by `finally`. It uses list indexes without validating stable box identity when the results are applied.

This violates the documented Rule 13/15 model: worker threads should perform external translation work only; document, journal and Tk operations belong to the main thread.

**Minimal direction:** Capture a detached list of translation inputs on the UI thread, including file/document identity and each `box.uid`; translate in the worker; post results into a thread-safe queue; apply only on the main thread after verifying that the target document/box still exists. Use `with undo_journal.batch(...)` for the application step. Do not add a generic job scheduler.

**Regression tests:** Cancel mid-run; fail one request; switch documents; structurally edit while translation runs; close the dialog; verify late results cannot edit a different box; verify one Undo restores the full completed batch.

#### F11 — `MTL-CALLBACK-TK-FROM-WORKER` — CONFIRMED — P1/P2

**Evidence:** `core/mtl_engine.py:337-354`; UI callbacks at `misora.py:9650-9670`, `10847-10860`, `10905-10923`.

`translate_async()` invokes `on_success` / `on_error` inside its worker. Several UI callbacks then call `after_idle()` from that worker thread. This is not a safe Tkinter thread-marshalling mechanism.

**Minimal direction:** Reuse the existing main-thread polling queue used by search. The worker should only enqueue plain result data. The main-thread poll should decide whether the target window/document/request is still current before touching widgets.

**Correction to Gemini's timeout proposal:** `MTLConfig.timeout_sec` already exists and defaults to **12 seconds** (`core/mtl_engine.py:50`); outbound calls pass `timeout=cfg.timeout_sec` (e.g. lines 182, 215, 242, 254, 291, 312). Do not ask Copilot to invent another timeout setting. The remaining work is to verify timeout/error classification and reliably re-enable Refresh / discard stale results.

#### F12 — `SEARCH-WORKER-READS-LIVE-DOCUMENTS` — CONFIRMED — P1

**Evidence:** `misora.py` search-start and worker setup around `7960-8085`; `core/search_engine.py:260-339`.

The search worker receives `entry['doc']` references from `open_documents` and traverses mutable boxes/metadata while the UI can edit the same document. This violates Rule 15 and can produce inconsistent results or races.

**Minimal direction:** Capture a compact immutable search snapshot on the UI thread (UID, speaker, clean text, metadata, path and any required offsets) and pass that snapshot to the worker. Do not deep-copy the whole application object or add broad locks around Tk.

**Regression tests:** Search while editing dialogue, speaker and Box 0 metadata; results must reflect one consistent snapshot.

### SEARCH / NORMALIZATION / DIAGNOSTICS

#### F13 — `SEARCH-SWALLOWS-FILE-ERRORS` — CONFIRMED — P2

**Evidence:** `core/search_engine.py:250-366` and `394+`.

Bundle and text file scan branches contain broad exception handling that silently passes. `os.walk()` is used without an error callback. Corrupt/unreadable files or inaccessible directories can disappear from the result without being reported as skipped. This contradicts Rule 15's requirement to report inaccessible/skipped paths.

**Minimal direction:** Add a small structured error/skipped-path collection to the search result. Distinguish “no matches” from “could not scan”. Do not make normal no-match files warnings.

#### F14 — `HALFWIDTH-KANA-DIAKRITIC-SPAN-NORMALIZATION` — CONFIRMED — P2

**Evidence:** `core/search_engine.py:27-30`, `65-92`.

Qwen2's retraction is incorrect. `_TOKEN_RE` groups a base character with combining marks U+0300–U+036F and U+3099/U+309A, but it does not group the half-width voiced/semi-voiced marks U+FF9E/U+FF9F with the preceding half-width kana. NFKC is therefore applied token-by-token without composing the pair.

Direct runtime reproductions against the uploaded ZIP:

- `ｶﾞ` vs `ガ` → span-normalized strings differ (`ガ` vs `ガ`).
- `ﾊﾟ` vs `パ` → differ (`パ` vs `パ`).
- `ｳﾞ` vs `ヴ` → differ (`ヴ` vs `ヴ`).
- `ｶﾟ` vs `カ゚` → equal in the tested implementation; do not overstate the bug as affecting every half-width mark.

Whole-string `story_ast.norm_search()` returns the expected composed forms for the first three pairs. The inconsistency is in the span-preserving search normalizer used to retain original offsets/highlights.

**Minimal direction:** Extend token grouping / span mapping for U+FF9E and U+FF9F while preserving correct original character spans. Do not replace the span-aware matcher with whole-string normalization if that would break highlight offsets.

#### F15 — `SEARCH-CANDIDATE-ROOT-DOUBLE-COUNT` — CONDITIONAL — P2/P3

**Evidence:** `misora.py:8688-8737`.

Candidate paths are appended independently for each configured root. If roots overlap, the same file can be appended more than once. `matching_files` de-duplicates by path, but `total_matches` increments before the dictionary replacement and can overstate the confirmation dialog's match count.

**Minimal direction:** De-duplicate canonical paths before prefiltering. Keep this low priority and do not let it distract from replacement correctness.

### STATE / UNDO / SHORTCUTS

#### F16 — `DIRTY-STATE-IS-GLOBAL-NOT-PER-FILE` — CONFIRMED — P1

**Evidence:** `core/undo_journal.py:95-96`, `213-221`; UI use around `misora.py:6684-6690`.

`mark_saved(file_path)` and `is_clean(file_path)` accept a path but ignore it. A single `_revision` and `_saved_revision` are shared by all open files. A direct runtime reproduction confirms that editing A then calling `mark_saved(B)` can make A appear clean.

**Minimal direction:** Introduce per-file revision/saved-revision state keyed by canonical file identity, or a minimal per-document dirty state consistent with the existing journal. Reconcile the counters when `prune_file()` removes history. Do not just remove the path argument; that would hide the design mismatch.

#### F17 — `DOC-SWITCH-STATE-BLEED` — CONFIRMED — P1/P2

**Evidence:** cache-hit branch `misora.py:6082-6098`; fresh-load initialization `6101-6108`; `open_documents` entries created around `6123-6131`, `6148-6156`, `6165-6173`.

The active `_locked_boxes`, `_modified_boxes`, `_original_box_texts`, `current_box_idx` and some view state are application-level fields rather than state saved per cached document. On cache hit, the code resets `current_box_idx` to 0 and rebuilds `_original_box_texts` from current content, but it does not restore the document's own lock/modified/JP-baseline state. Switching between cached documents can therefore leak index-based locks or modified indices, lose the selected box and corrupt the JP source baseline.

**Minimal direction:** Store only the necessary per-document fields in the corresponding `open_documents` entry and restore them on switch. Use stable `box.uid` for lock/source identity where possible. Keep the cache entry shape small.

#### F18 — `UNDO-SOURCE-TAGS-MISSING-AT-GUI-CALLS` — PARTIALLY CONFIRMED — P2

**Evidence:** `core/undo_journal.py:138-158`; `BoxEditDelta.source` defaults to `keyboard`; `misora.py` has only a small number of explicit `source=` call sites (e.g. `paste_caret` around 6954/6976).

The journal itself already checks same box, same source and same file before coalescing. The defect is that many GUI-originated actions (ribbon, speaker edits, MTL, replace paths) leave the default `source="keyboard"`, so unrelated action types can still merge within the coalescing window.

**Minimal direction:** Add accurate `source=` labels at the point each edit is recorded. Do not redesign `MasterUndoJournal` to solve missing caller metadata.

#### F19 — `UNDO-COALESCE-UID-FALLBACK` — CONDITIONAL — P2

**Evidence:** `core/undo_journal.py:146-154`.

`same_box` is true when UIDs match **or** indexes match. If both deltas have non-null but different UIDs, matching indexes still permit coalescing. This weakens stable identity. A normal user-facing reproduction has not yet been demonstrated, so do not classify it as a confirmed defect or rewrite the logic blindly.

**Minimal direction:** If both UIDs exist, compare UIDs only; fall back to index only when one or both UIDs are unavailable. Add a focused test that constructs two different UIDs at the same index and determines whether coalescing is possible in an actual reload/rebind workflow.

#### F20 — `SPEAKER-EDIT-BYPASSES-CENTRAL-COMMIT` — CONFIRMED — P2

**Evidence:** binding at `misora.py:3526`; `_on_speaker_edited()` at `7455-7475+`.

The speaker entry has a separate KeyRelease path. It marks the document dirty before checking whether the value changed, reads the untrimmed StringVar, and records edits outside the same central commit path used elsewhere. This can mark dirty on non-edit keys and lacks the same stable UID/source handling used by the central route.

**Minimal direction:** Unify speaker commit semantics with the central edit path or a small shared helper. Preserve current widget behavior; only record an actual value change; attach box UID and source; update the dirty/list state consistently.

#### F21 — `CTRL-ALT-HOTKEYS-BLOCKED` — CONFIRMED IN LOCAL ZIP — P2

**Evidence:** `misora.py:5741-5768`; UI advertises Ctrl+Alt shortcuts at the tooltip call sites identified in Qwen2.

The shortcut dispatcher detects Ctrl+Alt and immediately returns `None` to protect AltGr. The intended whitelist branch for application Ctrl+Alt shortcuts is absent in the local 510,461-byte source. This contradicts the old ledger's RESOLVED claim.

**Minimal direction:** Implement only the advertised Ctrl+Alt combinations while preserving AltGr text input. Verify physical Windows keyboard layouts; do not simply permit all Ctrl+Alt chords.

#### F22 — `CTRL-T-ROUTER-CONFLICT` — CONFIRMED — P2

**Evidence:** `misora.py:5808-5810` and root binding around `6043`.

The first-position `MisoraShortcuts` bindtag routes Ctrl+T to `on_copy_ai_prompt()`, while the root binding/menu assigns Ctrl+T to Translator Assistant. In editor widgets the first handler can consume the event, causing inconsistent behavior.

**Minimal direction:** Choose one documented Ctrl+T action and make the router, root binding and menu agree. Preserve Ctrl+Shift+T if it is the intended AI prompt shortcut.

#### F23 — `AFTER-JOB-TEARDOWN-INCOMPLETE` — CONFIRMED GAP / CONDITIONAL RUNTIME IMPACT — P2

**Evidence:** `misora.py:1365-1384`; timer creation/use at `1031`, `1876-1906`, `4215-4220`, plus `_search_poll_job` at `1251`.

`destroy()` cancels the search polling job but does not cancel all tracked long-lived jobs such as the continuous-resize, toast and eyedropper timers. The existing owner-specific cancellation methods are not all called by application teardown. This is a lifecycle gap; whether it causes a user-visible Tcl error depends on timing and which callback runs during destruction.

**Minimal direction:** Cancel tracked jobs through their owning components during shutdown, with guarded widget-existence checks. Do not blindly sweep every Tcl `after` job unless the source proves that anonymous callbacks cannot be cancelled by their owners.

#### F24 — `STARTUP-RESTORE-NOT-DEFERRED-AS-DOCUMENTED` — CONFIRMED DOCUMENTATION/IMPLEMENTATION DRIFT — P2

**Evidence:** `misora.py:1268-1298`.

Session files are opened inline in `__init__` while the splash is active; they are not deferred with `after_idle()` until after the main window is displayed as the ledger claims. The splash does update progress, so “startup freezes completely” is not proven. The actual issue is that restoration work blocks completion of initialization and may extend perceived startup time for large sessions.

**Minimal direction:** Measure startup phases before changing the lifecycle. If needed, defer only the restore portion until the first main-window paint. Preserve the single Tk root and existing splash; no second launcher process or splash redesign.

#### F25 — `VERSION-PICKER-HARDCODED` — CONFIRMED — P3

**Evidence:** `misora.py:488` hardcodes `(v1.3.3)` in the color picker title despite the version being available from the application package.

**Minimal direction:** Use the existing dynamic version helper. Cosmetic only.

#### F26 — `GRADIENT-LABEL-USES-COMMA` — CONFIRMED — P3

**Evidence:** `misora.py:904-908` displays `[c0,c1]`; gradient insertion uses the hyphen form.

**Minimal direction:** Change the display string to match the syntax actually inserted. Cosmetic only.

#### F27 — `EYEDROPPER-CHANGES-DPI-AWARENESS-AT-RUNTIME` — DESIGN-INVARIANT VIOLATION / CONDITIONAL — P2/P3

**Evidence:** `misora.py:952-959`, specifically `SetProcessDpiAwareness(1)` inside the eyedropper activation path; AGENTS Rule 23 prohibits runtime process DPI-awareness changes.

The call is made after Tk and windows already exist. The practical effect is not established without a Windows DPI/multi-monitor reproduction; a call can fail depending on the process's existing awareness and the exception is swallowed.

**Minimal direction:** Do not claim that the entire UI definitely rescales. Verify on Windows with mixed-DPI monitors. Prefer setting process awareness at startup/manifest and removing the runtime call if redundant.

---

## 3. Cross-AI disagreements and corrected verdicts

| Topic | Debate claim | Independent verdict |
|---|---|---|
| `STALE-CARD-REGISTRY` | Some earlier ledger text still suggests an open bug. | **RETRACTED / RESOLVED.** `_render_continuous_view()` clears `_card_widgets` before the plain-text early return (`misora.py:7049`). Do not re-prompt. |
| Undo cross-source merge | Described as a journal coalescing defect. | **Partially confirmed at caller level.** Journal already compares source/file/box. Missing `source=` metadata at many GUI call sites is the remaining issue. |
| `mark_saved(file_path)` TypeError | Old ledger mentioned TypeError from path arguments. | **RETRACTED.** The methods accept optional `file_path`; the real defect is that the argument is ignored and revision state is global (F16). |
| Empty binary argument converted to one space | Previously listed as a bug. | **RETRACTED / INTENTIONAL.** Binary length zero terminates the argument list; the one-space placeholder preserves arity (`story_ast.py:721-727`). |
| Record UID serialized in v2 | Previously claimed. | **NOT CONFIRMED.** Runtime record UIDs are not part of the serialized v2 record data. |
| TLS verification disabled | Old ledger once listed it. | **RESOLVED.** `mtl_engine.py` uses a default SSL context; do not reintroduce an “ignore SSL” option. |
| Half-width dakuten/handakuten bug | Qwen2 retracts it; Gemini2 agrees it exists. | **CONFIRMED.** Direct local repros for `ｶﾞ`, `ﾊﾟ`, `ｳﾞ` prove the span-normalizer mismatch. Qwen2's reasoning overlooked U+FF9E/U+FF9F. |
| Empty-state DnD overlay | Gemini3 warns about `tkinterdnd2` per-widget binding. | **RETRACTED AS STATED.** Local code uses native Win32 `WM_DROPFILES` on the outer HWND (`misora.py:1951+`), not `tkinterdnd2`. An overlay does not inherently need a separate widget drop target. The separate multi-folder `dirs[0]` issue remains confirmed. |
| MTL network timeout | Gemini asks for explicit timeout handling. | **Partially already implemented.** `timeout_sec=12.0` is present and used in HTTP requests. Improve user-facing timeout classification/retry state rather than adding a duplicate timeout mechanism. |
| `conflict_manager` in future XUAT import | External ADV helper imports it for pruning. Reports differ on whether this was explicitly excluded by the user. | **Do not port this dependency by default.** Misora already has its own `XUnitySyncManager`; the import feature should reuse Misora code and avoid coupling to the separate tool's conflict-manager internals. |

---

## 4. `priconne-adv-tools` — verified legacy hazards, NOT Misora source defects

These findings concern the separate helper scripts in `Reference-Files/priconne-adv-tools`. They are important because a future `Import from XUAT` feature may be tempted to reuse their parsing, conflict and cleanup logic. They are **not** bugs in `Misora-Editor` itself.

### L1 — Escaped equals parsing bug

`advscript.py:77` supports `\=` in `unesc()`, but `advscript.py:507` uses `line.split("=", 1)`. A key containing an escaped equals can be split at the wrong delimiter.

**Port rule:** Reuse Misora's existing `core/xunity_sync.split_xuat_line()` / first-unescaped-equals behavior. Do not copy the naïve split.

### L2 — Whole-file block-mode hijack

`advscript.py:480` uses `block = any(l.startswith("=") for l in lines)`. One stray line beginning with `=` can switch the entire dictionary file into block parsing.

**Port rule:** Use strict format sniffing or per-entry parsing; do not let one malformed line reclassify every entry.

### L3 — Conflict selection is always remembered globally

`advscript.py:602+` prompts that an `a` suffix means remember, but `advscript.py:641` assigns `self.resolutions[norm_k] = chosen.val` after every selection.

**Port rule:** Provide three scopes: Use Once (default), Apply to identical JP within this story, Remember Globally (explicit opt-in). Warn on short/common context-dependent phrases such as `はい`, `うん`, `えっ？`, `……`.

### L4 — Fuzzy candidate truncation is nondeterministic

`advscript.py:654-659` builds a set and evaluates `list(pool)[:4000]`. Set iteration order is not a stable relevance ranking; with more than 4,000 candidates, a best candidate may be omitted differently across runs.

**Port rule:** Apply deterministic ranking before a cap. Do not silently truncate an unordered set.

### L5 — Completion status ignores missing speaker names

`xuat2raw.py:175-180` populates `miss_names` but `is_complete` is based on `missing_real` and `real_boxes_count` only.

**Port rule:** Report dialogue completion and speaker-name completion separately. Do not silently show 100% overall completion when speaker names remain untranslated. Do not impose a strict repack block for every unknown speaker until the project defines which speaker names must be translated; allow a clear override where appropriate.

### L6 — Automatic XUAT pruning can remove a key still needed by another story

`advscript.py:758+` prompts to prune dictionary entries used in the story just repacked. The cleanup does not verify whether another untranslated story still relies on the same JP key. It also imports `conflict_manager` as its file-editing mechanism.

**Port rule:** v1 of Misora Import from XUAT should be read-only / report-only regarding dictionary cleanup. Do not prune shared keys after a single story repack. A later pruning feature requires a reference index of all remaining stories, backups and review.

### L7 — Normalization ignores placeholders and NGUI tags

`advscript.py:122` uses NFKC/dash/whitespace normalization but does not align with `{playername}` / `{0}` placeholders or Misora's NGUI tag handling.

**Port rule:** Keep exact raw-text match as the highest confidence. Use `TagMasker` and existing placeholder rules for secondary matching. Label tag-stripped / placeholder-normalized / fuzzy candidates as review-required; never silently discard markup during injection.

---

## 5. MTL Drawer — accepted design direction and necessary trims

The current local UI contains a floating `TranslatorAssistantDialog`; the side drawer has `Customize` and `NGUI Glossary` tabs, not a `Reference` tab. The debate's latest decision is to add MTL as another drawer tab and keep `NGUI Glossary` as-is (do not rename it).

### Accepted requirements

1. **Single visible MTL surface:** Retire the floating Translator Assistant in favor of the drawer's MTL tab. Existing MTL toolbar button, menu command and F8 should open that tab. F8 must not silently overwrite the current box.
2. **Readable source + editable result:** Show the immutable original JP source for the active UID in a compact read-only area; use a full-height editable result scratchpad. If no XUAT/cache result exists, leave it empty with an explanatory placeholder rather than copying JP into the result field.
3. **Explicit apply:** Apply uses central commit semantics, includes `box_uid` and `source="mtl"`, respects Translation Lock, skips unchanged values, and preserves trailing line breaks (do not `.strip()` the result). Provide Copy and optionally Apply & Next.
4. **Quota-safe live translation:** Live checkbox defaults OFF on every launch. One selected provider in v1. Trigger only when active box UID changes, not as the user types English. Debounce navigation; skip empty/Box 0/punctuation-only items; consult XUAT/session cache before network calls.
5. **Stale-response safety:** Each request must identify the document, box UID and request sequence. A late response may populate a cache, but must not overwrite another box's visible scratchpad or user edits.
6. **Refresh semantics:** Refresh explicitly bypasses the session cache and supersedes prior request sequences. Existing 12-second timeout should be used; differentiate timeout, 429 and auth failures in status text. Never leave Refresh disabled permanently.
7. **Local scratchpad editing:** Ctrl+Z/Ctrl+Y must undo the scratchpad's own typing, not the main document's UndoJournal. Clipboard shortcuts should remain native. Avoid `bind_all`.
8. **Import window mutual exclusion:** When Import from XUAT opens, close the MTL drawer and cancel/deactivate its pending live request. The latest debate records the user's preference to restore the drawer's previous visibility/tab when the Import window closes. Reopen only if it was open before Import; do not unexpectedly pop it open otherwise.
9. **Teardown:** Cancel the live debounce and invalidate request sequences on drawer close, Import open and application destroy. Reuse the existing main-thread queue poll rather than creating a second Tk polling loop.

### Design trims / objections

- A bounded in-memory cache is reasonable as quota protection for the new feature. A cap such as 2,000 entries is a design parameter, not an evidence-based performance threshold. Keep it session-only in v1; do not add disk persistence or a translation-memory subsystem.
- Do not add a token-bucket scheduler in v1. Existing debounce, configured `rate_limit_delay` and 429 handling are enough to start.
- Do not add speaker-context fields to providers unless `MTLEngine` already supports them. Displaying a speaker hint can be useful without changing provider APIs.
- `Fetch All` is explicitly user-triggered, so do not describe it as silent API use. However, it launches five engines and can make a paid request if configured; a single-provider v1 drawer is safer and simpler.
- `xuat_entries` is read via `getattr` in several places but is not assigned/populated anywhere in the current Misora code. The XUAT Cache engine/badge is therefore inert until the future index feature exists.
- `safe_clipboard_get()` retries five times with 50 ms sleeps (`misora.py:1304-1314`), so it can block an event handler for up to roughly 250 ms. In the scratchpad, Ctrl+V should bypass the application's CSIF clipboard sniffing and use the normal local widget paste path.
- Do not implement the drawer before the JP UID registry and main-thread MTL queue are reliable; otherwise the new UI will sit on unstable identity/thread behavior.

---

## 6. Import from XUAT — recommended product shape

### Accepted approach

- Build a one-pass index of candidate dictionary entries with file and line provenance. Indexing may run in a worker, but the worker should receive immutable file inputs and return plain data.
- Reuse `core/xunity_sync.py` parsing and `core/ngui_tags.py` / search normalization where appropriate. Do not import the external `conflict_manager` module.
- Use a lightweight left Treeview/list for all boxes: Box number, speaker, JP preview, current EN preview, status. The right inspector shows the selected JP, candidate translations, source file/line, match confidence and an editable override.
- Provide filters such as All, Conflicts, Missing, Normalized/Fuzzy, Exact. Avoid rendering several full rich-text candidate streams; that creates needless Tk widget churn and memory use.
- Make confidence visible: Exact, normalized, fuzzy, conflict, missing, locked. Exact unique matches can be selected as the default suggestion, but applying them should remain a deliberate action unless the user approves a clearly specified auto-apply rule.
- Keep conflict memory at three scopes: Use Once (default), This Story, Global (explicit opt-in).
- Report dialogue completion and speaker-name completion separately.
- Do not auto-prune XUAT dictionary entries after repacking one story.

### Objections / open design details

1. **Do not hard-block every story with unresolved speaker names by default.** Some names may intentionally remain Japanese or be special/system labels. Show a separate completion metric and a clear override; define speaker eligibility before turning it into a strict repack gate.
2. A sidecar index cache is not needed in the first version unless indexing is proven slow. Start with one in-memory scan and measure.
3. Do not make a generic candidate-ranking service. A small deterministic exact/normalized/fuzzy ranking pipeline is adequate.
4. Do not silently auto-apply fuzzy or normalized matches. Human review is essential for context-dependent Japanese dialogue.

---

## 7. Left Sidebar / Open Project — cross-check and efficiency recommendation

### Confirmed current state

- `_left_dock_tab` defaults to `"search"` (`misora.py:1118`).
- Current tabs are `Search Results` and `Opened Files` (`3233-3261`).
- `on_open_file()` uses `filedialog.askopenfilename()` and opens one file (`8375-8390`).
- DnD uses native Win32 `WM_DROPFILES` on the outer window (`1951+`), not `tkinterdnd2`.
- `_handle_dropped_paths()` can process multiple files, but when multiple directories are dropped, only `dirs[0]` is passed to `_process_opened_folder()` (`2220-2288`).

### Recommended minimal user workflow

- Rename `Opened Files` to `Open Project` and default to that tab on launch.
- Show an empty state with `Open Files...`, `Open Folder...` and drag/drop guidance when there are no opened files; restore it when the last file closes.
- Use `askopenfilenames()` for multi-select.
- Route Open Files, Open Folder and DnD through one path-normalization/validation helper so they share duplicate handling and status reporting.
- Fix the dropped-multiple-folders case with a single summary message or an explicitly supported multi-folder workflow.

### Lazy loading warning

Gemini's “register paths first, load only the active document” idea could reduce repeated parsing and O(N) UI redraw on multi-select, but the current code assumes `open_documents[path]` often contains a loaded `doc`. Search scope, Replace All, close/dirty handling and file counts all read these entries. A `doc=None, loaded=False` placeholder would require auditing every consumer.

**Recommendation:** Do not add unloaded placeholder entries in the first UI pass. First implement multi-select with one final active render/list refresh (or defer rendering during the batch) while preserving the existing loaded-entry contract. Consider lazy loading only after measuring real open-time/RAM and mapping every `open_documents` consumer.

### DnD correction

The `tkinterdnd2` overlay warning in Gemini3 is not applicable to this code. Because the native drop handler is attached to the top-level outer HWND, an Empty State frame does not need its own separate DnD registration. Test drop onto the empty area on Windows, but do not add unused widget-specific DnD plumbing.

---

## 8. Additional efficiency and maintenance observations

These are lower priority than correctness and should be measured before optimization.

1. **Continuous View redraw cost:** `_render_continuous_view()` rebuilds many widgets when state changes. Avoid rebuilding it N times during multi-select or bulk operations. A single deferred refresh may be a small win; full virtualization is a separate measured project.
2. **Clipboard retry latency:** `safe_clipboard_get()` can block about 250 ms. Do not call it for scratchpad typing/focus events or where ordinary native paste can be used.
3. **Session restore startup cost:** Measure import, Tk creation, first splash paint, UI build and restore separately. The splash is already a `Toplevel` under one root; do not redesign into a second process.
4. **Icon cache:** Cache growth is a low-priority observation. Bound it only if profiling shows real accumulation; avoid speculative cache infrastructure.
5. **Project structure and packaging:** The uploaded ZIP includes `__pycache__` / `.pyc` files for multiple Python versions. They are not source defects, but should generally be excluded from release/source archives. Check `.gitignore` and packaging rules before making a cleanup change.
6. **README assets:** The README references local banner, mascot and section icon paths that are missing from the uploaded `assets/` directory. The `assets/` directory contains the Python asset loader/splash modules but not those referenced images. Either restore intended images or remove/bypass those references; do not generate replacement images as part of a code-integrity patch.
7. **Debug Console ambiguity:** `var_console_visible` / `_console_visible` are persisted, `txt_console` is only mentioned in an `hasattr` theme guard, and F12 currently displays a toast saying logs stream to the persistent Windows console. This is a product-intent question, not automatically a bug. If the user expects an in-app console, it is absent; if the intended console is the external Windows console, remove or reconcile dead in-app state and misleading controls. Ask the user before implementing a dockable console.
8. **Startup restore:** Progress is updated while restoring during splash; do not claim a total freeze. Measure whether it is actually a problem before moving lifecycle code.

---

## 9. Priority and suggested engineering slices

The following sequence is a recommendation for debate, not an implementation plan approved by the user.

### PRE-FLIGHT — baseline integrity

- Treat the uploaded 510,461-byte ZIP as the reference tree.
- Verify that the local Copilot workspace is byte-equivalent to that tree (at least key source hashes and clean working-tree/diff review).
- Do not use the current stale GitHub `main` as the Copilot codebase unless it is first synchronized.
- Reconcile `PROJECT_STATE.md` conflict markers and update its test breakdown only after source-based verification.

### SLICE A — prevent direct data loss

1. `OPEN-FAILURE-STATE-CORRUPTION` (F1).
2. Save success handling for Close and Exit (F2/F3), coordinated with per-file dirty tracking (F16).
3. Plain-text compiled preview Save source (F4).
4. Internal BoxSnapshot paste fidelity (F6).

Each should have a focused regression test and minimal file scope.

### SLICE B — Replace All integrity

1. Strict text decode + structured bundle matching.
2. Protect dirty/open/locked docs and refresh affected caches.
3. Record bundle and text deltas for Undo/Redo.
4. Atomic writes for forward and reverse operations.
5. Correct match counts and error/skipped reporting.

Do not combine a UI preview redesign with the data-integrity repair. A preview can be considered only after the replacement model is reliable.

### SLICE C — identity, state and XUAT correctness

1. UID-keyed JP baseline registry (F7).
2. Per-document lock/modified/selection state (F17).
3. Per-file revision/dirty tracking (F16).
4. Source tags at GUI Undo call sites (F18).
5. Verify conditional UID fallback behavior (F19).

### SLICE D — background-thread correctness

1. Search snapshots (F12).
2. Batch translation worker/result queue (F10).
3. MTL async callback marshaling (F11).
4. Exception-safe Undo batch lifecycle for all long operations.

Use the existing queue/poll pattern; no new scheduler or task framework.

### SLICE E — format/search correctness and lightweight UX

1. Misora v2 reserved-category and external escape compatibility (F8).
2. Search silent-error reporting and half-width kana spans (F13/F14).
3. Ctrl+Alt whitelist, Ctrl+T consistency, timer teardown (F21/F22/F23).
4. Open Project default, multi-select, empty state and dropped-folder handling (Section 7).
5. Geometry clamp and startup measurement only if Windows evidence justifies them.

### SLICE F — new MTL and Import features

Only after the identity and thread foundations are complete:

1. MTL Drawer with the minimum accepted safety behavior.
2. Import from XUAT using the existing parser/sync/tag primitives and the lightweight Treeview/inspector UI.
3. Add bounded session cache only as needed for the live translation quota guard.

Do not split the 11k-line `misora.py` merely because it is large. Use focused helpers only when a change has a real ownership boundary and measurable benefit.

---

## 10. Prompting playbook observations for later Phase 2

The two PromptAgent files advocate a seven-block prompt structure: execution surface/mode, exact goal, context pointers, file scope/ownership, guardrails, verification loop, and deliverable/handoff. That is a useful structure for later Copilot prompts.

For this project and the user's limited Copilot quota:

- Prefer one bounded engineering slice per prompt, not an all-in-one “fix every bug and build both features” task.
- Include exact files and functions, expected behavior and a minimal reproducer/test.
- State out-of-scope items explicitly (no module split, no new dependencies, no unrelated UI redesign).
- Require a regression test that fails before the fix, and require real command output.
- Do not tell the agent to skip, weaken or silently mock failing tests.
- Use the local workspace baseline, not stale `main`.
- Keep recurring project invariants in the existing `AGENTS.md`; do not copy dozens of repeated rules into every prompt. A small `.github/copilot-instructions.md` may be useful only if it adds concise Copilot-specific commands and does not duplicate/conflict with `AGENTS.md`.
- Do not pin a model name or use a Copilot CLI / Antigravity command unless the user's actual installed surface exposes it. The reference playbooks are templates, not proof that every named command/model is available in the user's account.

No Phase 2 prompt is created in this report.

---

## 11. Questions for the next Phase 1 debate round

Please have the other AIs challenge these specific points with source evidence or reproductions. Do not implement code.

1. **F1 open failure:** Can any `open_file()` failure path leave a mismatched active path/document/environment? Is the proposed “stage then commit” fix the smallest safe correction?
2. **F2/F3 save lifecycle:** What is the minimum API change to make `on_save()` report success and ensure Close/Exit never discard a failed save? How should inactive dirty files be saved without changing active UI state unpredictably?
3. **F5 Replace All:** Is a single prompt too broad? Propose the smallest safe split for structured bundle search, dirty/cache handling, lock behavior, Undo and atomic writes.
4. **F6 internal box clipboard:** Can direct BoxSnapshot insertion preserve all fields without breaking legacy external CSIF paste?
5. **F7 immutable JP:** Confirm UID registration lifetime across load, structural changes, save, reload and cached-document switching.
6. **F8 v2 interop:** Confirm the `System` argument round-trip failure and compare every escape sequence with the external ADV v2 helper. Should the v2 contract be unified or explicitly versioned?
7. **F10/F11/F12 threads:** Can the existing `_process_search_queue` be reused for all three paths without adding a new poller? What minimal stale-result identity is required?
8. **F14 normalization:** Reproduce `ｶﾞ`/`ガ`, `ﾊﾟ`/`パ`, `ｳﾞ`/`ヴ` and verify highlight offsets after a fix.
9. **F16 dirty state:** Is per-file revision sufficient, or would per-document journals be safer? Avoid a rewrite unless a concrete Undo scenario requires it.
10. **F17 document state:** Which fields must be stored per document now, and which can remain global? Avoid bloating each cache entry.
11. **F19 UID fallback:** Is there a practical path where different non-null UIDs at the same index can be coalesced? Provide a test or downgrade the finding.
12. **Sidebar lazy load:** Is lazy registration necessary for the requested multi-select workflow, or can one batched registration/render preserve current invariants with less complexity?
13. **Console intent:** Is F12 meant to open an in-app panel or simply announce the Windows console? Do not implement a console without user clarification.
14. **MTL scope:** Are live debounce, cache, epoch/request-sequence, local scratchpad undo and XUAT mutual exclusion sufficient? Identify any item that can be safely deferred.
15. **Import confidence policy:** Should exact unique matches be preselected only, or can they be automatically applied? Normalized/fuzzy candidates should remain manual unless explicitly approved.
16. **Speaker completion:** Which Japanese speaker names are expected to be translated? Recommend separate meters and explicit override before strict repack gating.

### Required response format from counterpart AIs

For each item, reply with:

- `AGREE`, `DISAGREE`, `PARTIALLY AGREE`, or `NEEDS EVIDENCE`.
- Exact file and line range from the authoritative local ZIP (or a direct minimal reproduction).
- User-visible impact and realistic severity.
- Smallest recommended fix.
- Regression test.
- Any remaining uncertainty.

Do not create a Copilot execution prompt. Do not modify files. Do not propose a broad rewrite. The goal is an evidence-backed Phase 1 consensus for user approval.

---

## Appendix A — Key source references

Local Misora paths/line ranges:

- Open file state: `misora.py:6066-6177`
- Close/exit save handling: `misora.py:1349-1363`, `9027-9046`
- Compiled/plain-text Save: `misora.py:6179-6207`, `7855-7880`
- Replace All: `misora.py:8609-8802`
- Copy Box/Paste Box: `misora.py:6827-6895`; snapshots `core/story_ast.py:207-230`
- XUAT immutable key registry: `core/xunity_sync.py:74-86`; GUI save sync `misora.py:7926-7950`
- Search tokenizer/spans: `core/search_engine.py:27-30`, `65-92`; scan exceptions `250-366`, `394+`
- UndoJournal revisions/coalescing: `core/undo_journal.py:95-96`, `138-158`, `213-221`
- Threaded translation: `core/mtl_engine.py:337-354`, `misora.py:11089-11145`
- Shortcut router: `misora.py:5741-5810`
- DnD: `misora.py:1951+`, `2220-2288`
- Sidebar: `misora.py:1118`, `3233-3261`, `8375-8390`, `8950-8968`

Reference repository files:

- [Grok memo](https://github.com/ImaterialC/Reference-Files/blob/main/202621121618grook1.txt)
- [Gemini cross-check and MTL proposal](https://github.com/ImaterialC/Reference-Files/blob/main/202621121735gemini2.txt)
- [Qwen cross-check and legacy ADV audit](https://github.com/ImaterialC/Reference-Files/blob/main/202621121751Qwen2.txt)
- [Gemini workspace / MTL clarifications](https://github.com/ImaterialC/Reference-Files/blob/main/202621121801gemini3.txt)
- [Qwen native DnD / sidebar / console delta](https://github.com/ImaterialC/Reference-Files/blob/main/202621121815Qwen3.txt)
- [Copilot prompting reference](https://github.com/ImaterialC/Reference-Files/blob/main/PromptAgent/github_copilot_ai_prompting_reference.md)
- [Antigravity prompting reference](https://github.com/ImaterialC/Reference-Files/blob/main/PromptAgent/google_antigravity_ai_prompting_reference.md)

**End of Phase 1 Round 2 independent review.**
