# MILESTONE F — MTL THREADING, APP LIFECYCLE, SECURITY & STABILIZATION

```text
/plan

Implement Milestone F only: BUG-27..BUG-37, HYG-06 and HYG-07, in exact dependency order from the locked ledger.

Scope:
- BUG-27 all asynchronous MTL paths use a main-thread-polled queue; capture file/document/box identity, source hash and request sequence; discard stale results safely.
- BUG-28 fix Continuous ribbon target, font size commit, and Page dirty/title/Undo synchronization.
- BUG-29 reconcile shortcut routing across bindtags, root, menus, tooltips and README, preserving AltGr behavior.
- BUG-30 search focus, page gutter refresh and no-op KeyRelease dirty-state redraw behavior.
- BUG-31 theme-aware Treeview and headings.
- BUG-32 logger flush completion barrier, logger.close(), and safe Tk after-job teardown.
- BUG-33 DPAPI fail-closed and explicit decrypt warning without silently wiping stored encrypted values.
- BUG-34 UnityPy old environment disposal on reload.
- BUG-35 defer startup session restore until after main window maps.
- BUG-36 robust Splash filename ordering.
- BUG-37 Raw Commands read-only until FEAT-11 gates.
- HYG-06 single version source for DeepL User-Agent without circular imports.
- HYG-07 bind_all Ctrl+H returns break; Ctrl+H remains CLOSED as a user-reproduced blocker, so treat only as minor hygiene.

Guardrails:
- Worker threads must never call Tk methods, including after(), after_idle(), or widget methods.
- Results must be revalidated by immutable identity immediately before apply.
- Do not apply stale translations to a different file or box.
- Do not weaken DPAPI security or silently fall back to plaintext writes.
- Keep credentials, settings and local files out of logs/artifacts.
- Do not turn the former Ctrl+H finding into a P0 regression without a new reproducible case.
- Do not allow Raw Commands edits until the full AST/v2/transaction gate passes.

Verification:
Test file switches during active MTL, box changes during request, stale source hash, worker completion after dialog close, cancel/error/timeout, batch undo balance, all UI updates on main thread, toolbar target in both views, keyboard binding dispatch, gutter refresh, logger in-flight flush/teardown, DPAPI failure/decrypt failure, UnityPy disposal, startup map-before-restore, unusual Splash filenames, Raw Commands disabled.

Deliverables:
Exact tests and output, per-bug evidence, independent Critic/Challenger review, and a P0/P1 stabilization sign-off report. Do NOT start FEAT-12/13 MTL Drawer until the applicable BUG-14/BUG-27 and HYG-01 gates are PASS. Do NOT start FEAT-10 Preview or FEAT-14 Import from XUAT unless BUG-11 is PASS.
```
