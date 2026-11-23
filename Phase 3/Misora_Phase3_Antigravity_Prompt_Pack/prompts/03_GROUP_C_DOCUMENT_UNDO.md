# MILESTONE C — DOCUMENT STATE, LOCKS, UNDO/REDO & MUTATION SAFETY

```text
/plan

Implement Milestone C only: BUG-10..BUG-20 and applicable HYG-02. Read the locked canonical ledger and retain its exact wording for each acceptance criterion.

Scope:
- BUG-10 multi-box caret paste dirty-state synchronization and Translation Lock.
- BUG-11 plain-text source buffer must be saved, never the NGUI-compiled preview widget. This is a hard dependency for Preview and Import from XUAT.
- BUG-12 all document-specific state must live with each open_documents entry and survive switching, cache hits, inactive-file saves, close and app exit. Stable lock/source identity rules must match the ledger.
- BUG-13 mutate model first; record Undo and dirty only after successful mutation; surface/log errors.
- BUG-14 batch translation cancellation must drain worker results and end one undo batch exactly once on the UI thread.
- BUG-15 non-contiguous Cut/Undo/Redo must restore exact positions and enforce locks.
- BUG-16 Clear Skeleton and Translator Assistant Apply must honor locks and preserve intentional whitespace.
- BUG-17 UID-safe Undo coalescing; preserve new_seg_texts when coalescing multi-segment edits.
- BUG-18 atomic byte write must preserve LF on Windows; use the atomic encoded-byte path.
- BUG-19 save metadata-only zero-box story documents safely in all modes.
- BUG-20 collision-resistant backup names for normal Save and Replace All.
- HYG-02 tests must use temporary backup folders and not pollute repository backups.

Guardrails:
- Never store runtime Record.uid in .misora.
- Never transfer unresolved locks silently.
- Never allow locked boxes to be modified by bulk operations.
- Do not call Tk methods from worker threads.
- Do not end batch Undo while a worker can still enqueue updates.
- Do not use open_file() merely to save an inactive document if it resets UI/document state.
- Do not auto-stash or rewrite local changes.

Verification:
Create tests for tab A→B→A state retention, dirty inactive document save, paste dirty state, lock skipping, failed mutation leaving undo unchanged, mid-batch cancellation, non-contiguous cut order, coalescing by UID, LF-only bytes on Windows (or a byte-level equivalent plus explicit Windows verification status), zero-box metadata save, backup collision case.

Deliverable:
Milestone report with exact output and independent adversarial review. Stop before Milestone D if any P0/P1 document-state or Undo defect remains failing or unverified.
```
