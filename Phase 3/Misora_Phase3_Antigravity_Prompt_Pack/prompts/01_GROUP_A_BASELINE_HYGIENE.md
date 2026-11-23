# MILESTONE A — BASELINE & REPOSITORY HYGIENE

```text
/plan

Execute ONLY Milestone A from the locked Misora Phase 3 ledger: HYG-01, plus baseline traceability needed by all later milestones. This is implementation planning for Milestone A, not a reopening of Phase 2.5.

Read the locked ledger first:
https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Phase_2.5_Canonical_Ledger_LOCKED.md

Scope:
- Verify target repository identity, local HEAD, git status, branch, and source differences from pinned target SHA 683724edaf2afac89d2695a80e30a471a0da9195.
- Audit AGENTS.md, PROJECT_STATE.md, README.md, test inventory, counts, and filename references.
- Reconcile only documentation claims that demonstrably contradict the locked ledger or current source.
- Preserve the recorded local-fixture/.gitignore history accurately.
- Establish a canonical Phase 3 execution matrix for BUG-01..BUG-41, HYG-01..HYG-08, FEAT-01..FEAT-14, DEF-01..DEF-10, and NO-01..NO-12.
- Record actual test discovery and a baseline test run; do not infer the 234/238 count from old documents.

Guardrails:
- No application source edits in this milestone.
- Do not overwrite AGENTS.md wholesale. Make minimal, reviewable changes.
- Do not claim local docs or .unity3d fixtures exist unless verified.
- Do not change ledger decisions or IDs 35/32 policy.
- Do not run destructive Git commands or commit/push.

Verification:
- Show git status before and after.
- Show test discovery command, discovered count, baseline test output, and any environmental blockers.
- Verify every canonical ledger ID maps to exactly one canonical status row, without duplicating underlying defects.

Deliverables:
- Baseline & Workspace Safety Report.
- HYG-01 documentation diff.
- Canonical execution matrix and test inventory.
- Stop and request review before Milestone B.
```
