# MILESTONE D — SEARCH, REPLACE & PROJECT ROOT IDENTITY

```text
/plan

Implement Milestone D only: BUG-21..BUG-24 and HYG-05, consistent with DEP-10 and the locked ledger.

Scope:
- BUG-21 Match Case must remain meaningful when Ignore Whitespace is enabled, including Unicode normalization.
- BUG-22 structured skipped-path/error reporting; safe immutable search snapshots; never hand live AST to worker; stale-search sequence guard; raw-to-clean highlight spans must be accurate or explicitly approximate.
- BUG-23 replace stale project roots rather than appending; keep Project Search roots bounded to Text and RedirectedResources; never search plugins/config; do not inject unrelated local input/output roots. XUAT Import source remains its own strict Text path.
- BUG-24 one shared matcher and lock policy across Find, Replace Next, current/multi-file Replace All; fix cache keys and cache invalidation; do not overwrite dirty open documents from disk; do not mark disk-saved files dirty; ask before undo/redo touches closed paths; preserve per-document break_char.
- HYG-05 import typing.Any and add an annotation-resolution test.

Guardrails:
- Do not describe inaccessible files as zero matches.
- Do not let background search read a live mutable StoryDocument.
- Do not scan unrelated BepInEx/plugins or config directories.
- Do not silently reopen closed tabs during BulkFileDelta Undo/Redo.
- Do not claim current-file Replace All lock handling was broken; the ledger explicitly corrects this claim. Fix the actual remaining multi-file issues.
- Do not create the deferred Replace-All dry-run diff pane (DEF-09).

Verification:
Test Match Case × Ignore Whitespace combinations, Unicode widths, regex and literal mode, raw/clean spans, snapshot failures, os.walk errors, rapid successive searches, stale project roots, Text/RedirectedResources boundaries, same open file in multiple states, locks, dirty open docs, closed path Undo/Redo confirmation, and break_char preservation.

Deliverables:
Report all exact tests and real output, independent diff review, and any paths skipped because fixture/permission is unavailable. Stop before Milestone E if any P0/P1 in-scope search/cache integrity test fails.
```
