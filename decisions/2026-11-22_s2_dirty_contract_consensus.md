# Decision Record: S2 Dirty Tracking Contract & Multi-Document Safety

**Date:** 2026-11-22  
**Participants:** GPT (Arbiter), Gemini (Technical Reviewer), Qwen (Source Verifier), User (Relay & Product Owner)  
**Status:** **UNANIMOUS LOCK (ALL 3 AIS + USER)**  
**Executable Prompt:** `prompts/S2_dirty_contract_final_locked.md`  
**Companion Guide:** `prompts/S2_execution_guide.md`

---

## 1. Problem Statement (Core Integrity Defects)
Detailed codebase inspection of `misora.py` identified four critical multi-document safety defects:
1. **P0 False-Clean Clobber:** Modifying Document A, then switching to or saving Document B erroneously cleared or desynchronized Document A's dirty flag.
2. **Ambiguous `on_save()` Contract:** The `on_save()` function lacked explicit boolean return semantics across all exit paths, leaving callers unable to distinguish save successes from fatal disk errors.
3. **Undo-Storm & Desynchronization:** Performing undo/redo operations triggered redundant widget-wide UI re-renders and failed to clear dirty indicators when returning to saved baseline revisions.
4. **Secondary XUAT Wipe:** If primary document persistence succeeded but secondary XUnity dictionary synchronization failed, `self._modified_boxes` was prematurely cleared, preventing subsequent save attempts from retrying XUAT sync.

---

## 2. Qwen Technical Amendments (Q1–Q6)
Qwen proposed 6 technical precisions, unanimously accepted into the prompt:
- **Q1 (Flag-Only & Single UI Sync):** `_mark_document_dirty(path)` strictly mutates in-memory booleans. The UI update helper `_dirty_state_changed()` is invoked exactly **once** at the conclusion of an operation (Rule 13 anti-UNDO-STORM).
- **Q2 (Fingerprint Checkpoints & Multi-File Evaluation):** Compute deterministic document fingerprints upon save and open. In `on_undo()`/`on_redo()`, re-evaluate dirty status across the set of affected files after the delta loop completes. Explicitly forbidden from using lazy baseline shortcuts (first observation as baseline).
- **Q3 (Uncached-Path Guards):** Provide robust fallback guards in `on_save()` and `_dirty_state_changed()` for documents loaded outside the `open_documents` cache dictionary.
- **Q4 (Comprehensive Mutation Audit):** Ensure dirty flags are set across all mutation vectors: `on_replace_next()`, active-file `on_replace_all()`, both MTL apply paths (`on_translate_current_box` and `TranslatorAssistantDialog._on_apply`), and worker-side mutations.
- **Q5(b) (Latent Branch Deferral):** Defer latent `inject_box(..., None)` speaker handling to S7/F20 to prevent scope creep.
- **Q6 (Secondary XUAT Failure Invariant):** If disk persistence succeeds but XUAT fails, the document remains clean (`dirty = False`), but `self._modified_boxes` is **RETAINED** for retry and `on_save()` returns `True`.

---

## 3. Resolution of Blockers B1 & B2 and Deltas 1–4
GPT placed a temporary hold (`NOT LOCK`) pending resolution of two architectural blockers, which were cleanly resolved:
- **Blocker B1 (`test_34` & `test_39` Baseline Contract):** Established an explicit 3-branch classification during `/plan` preflight. If `test_34` manipulates `undo_journal` directly, Antigravity must stop in `/plan` and request direction. Tests `test_34` and `test_39` must never be weakened or modified.
- **Blocker B2 (`StoryDocument` Serializer Inspection):** Read-only inspection of `core/story_ast.py` verifying the full serializer (deterministic, uid-free, non-projected records included, side-effect free).
- **Delta 1 (True No-Op KeyRelease):** `_on_dialogue_edited()` returns a boolean; `_commit_widget_edit()` syncs UI only when `True`, eliminating dock rebuilds on arrow navigation.
- **Delta 2 (Plain-Text Cache Synchronization):** Synchronize plain-text cache across Page View, Continuous View, and Undo/Redo, verified by Test 12.
- **Delta 3 (Rule 15 Disclosure):** Acknowledge that `BatchTranslateDialog.worker()` runs off the main thread; S2 keeps worker updates flag-only without pretending to fix threading (owned by S6).
- **Delta 4 (Test 11 Suite-Level Guard):** Test 11 asserts only against pre-S2 attributes; `test_34` and `test_39` run at suite-level.

---

## 4. Final Lock Verdict
- **GPT:** `GPT FINAL VERDICT: LOCK`
- **Qwen:** `VERDICT: LOCK`
- **Gemini:** `LOCK FINAL CONFIRMED`
- **User:** Approved for Antigravity planning execution.
