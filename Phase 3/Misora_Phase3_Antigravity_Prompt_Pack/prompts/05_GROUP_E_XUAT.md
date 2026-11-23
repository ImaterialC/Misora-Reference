# MILESTONE E — XUAT KEY INTEGRITY & ATOMIC SYNCHRONIZATION

```text
/plan

Implement Milestone E only: BUG-25..BUG-26 and the XUAT data-layer prerequisites for FEAT-14. Do NOT build the Import from XUAT UI yet.

Read the locked canonical ledger, especially BUG-25, BUG-26, FEAT-14, DEP-7, RF-3 and NO-09.

Scope:
- Immutable Japanese source snapshots keyed by stable live box identity (box.uid in memory).
- Register/read JP source through the existing XUnitySyncManager API rather than positional mutable indices.
- Never overwrite the original Japanese key with saved English text.
- Conflict preview is shown only when a genuine conflicting duplicate is detected.
- Replace unsafe XUAT temp naming/replacement with the shared atomic encoded write path, preserving encoding, BOM and newline behavior.
- Prepare one unified XUAT indexing architecture compatible with var_xuat_cache/D11; avoid multiple independent indexes.

Guardrails:
- Do not build FEAT-14 resolver UI in this milestone.
- Do not import/port conflict_manager.
- Do not globally prune XUAT entries.
- Do not silently overwrite genuinely conflicting translations.
- Keep source scope strict: BepInEx\Translation\en\Text for the future importer.
- Do not modify the XUAT dictionary if preview/validation fails.

Verification:
Test that second save continues to match the original Japanese key; inserting/deleting/moving boxes cannot shift JP key ownership; genuine conflicts prompt and non-conflicts do not; atomic update preserves BOM/CRLF/encoding; failed writes leave original bytes intact.

Deliverables:
BUG-25/26 test evidence, data-layer API/design note for FEAT-14, updated traceability matrix and independent review. Stop before UI work until BUG-25 is PASS.
```
