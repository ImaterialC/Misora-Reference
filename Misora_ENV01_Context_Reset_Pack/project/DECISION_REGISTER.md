# Misora — Decision Register (Current)

| ID | Decision | Status / consequence |
|---|---|---|
| D-ENV-01 | Reduce always-loaded AI context by separating permanent rules, current state, task routing, architecture references, and history. | PROPOSED; requires Project Lead approval. |
| D-REL-01 | Cancel/pause the current v1.5.0 release effort and do not run the old S12 release gate now. | REPORTED council decision; current release remains HOLD. |
| D-REL-02 | Do not continue planned S15 work under the cancelled roadmap. | REPORTED council decision; clarify against older completed S15 historical record before editing history. |
| D-S11E-01 | S11e v1.4.15 was locally committed as `ead65077...`; no push. | Project-Lead transcript evidence. Verify local HEAD/status before new edits. |
| D-DEF-01 | Preserve the serializer's empty-argument single-space sentinel behavior. | DEFERRED; core changes require a separate decision/session. |
| D-XUAT-01 | Accept S11b2 real-tree 2.899 s latency under Option A; defer asynchronous disk I/O. | REPORTED accepted waiver; do not relabel original >2 s STOP as PASS. |
| D-S11C-A | Quick Edit binary round-trip parity is accepted with the known DEF-01 sentinel leakage documented. | APPROVED historical decision; not a claim of lossless round-trip. |
| D-SCOPE-01 | Approved plans do not automatically authorize edits, commits, pushes, or version promotion. | ACTIVE agent governance rule. |

## Authority rule

If this register conflicts with a newer explicit Project Lead instruction, update it only after recording the new decision's date, scope, and superseded ID. Archived AI recommendations are not approvals.
