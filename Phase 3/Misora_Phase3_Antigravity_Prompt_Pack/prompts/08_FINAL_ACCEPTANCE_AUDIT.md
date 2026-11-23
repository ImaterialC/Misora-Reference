# FINAL PHASE 3 ACCEPTANCE AUDIT & INTEGRATION

```text
/goal Complete the final evidence-based acceptance audit for Misora-Editor Phase 3 and prepare a reviewable integration patch. Do not invent missing test or fixture evidence.

Context:
- @AGENTS.md
- @PROJECT_STATE.md
- @README.md
- @tests/
- @core/
- @misora.py
- Locked ledger: https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Phase_2.5_Canonical_Ledger_LOCKED.md

Objective:
Audit every canonical ID BUG-01..BUG-41, HYG-01..HYG-08, FEAT-01..FEAT-14, plus all DEF/NO dispositions. Confirm that all required P0/P1 and dependent feature acceptance gates have genuine evidence before declaring Phase 3 complete.

Done criteria:
1. Each canonical ID has exactly one status: PASS, FAIL, BLOCKED, DEFERRED, or NOT APPLICABLE, with an evidence pointer and reason.
2. Every PASS references the specific regression test(s), exact command, exit code, and actual output.
3. Full test suite and appropriate static/compile checks are run and report exact counts, skipped tests and failures.
4. All unresolved fixture-dependent claims remain BLOCKED/NOT VERIFIED. In particular do not claim binary IDs 35/32 or non-target bundle invariance were production-verified without real fixtures.
5. Verify no test weakening, mocked-out behavior, fabricated screenshots, silent exception swallowing, or unreviewed unrelated code changes were introduced.
6. Review `git diff --check`, full diff, repository status and changed files. Preserve ignored/untracked user data.
7. Ensure no automatic push or destructive integration. Produce a clean patch/diff and integration instructions for the Project Lead.
8. Success Auditor and an independent reviewer both sign off; disagreements are reported, not averaged away.

Stop conditions:
- Any required P0/P1 gate fails or lacks evidence.
- Any hard guardrail is violated.
- Any fixture-dependent behavior is incorrectly claimed as passed.
- The working tree includes unexplained edits or untracked data.

Deliverables:
- Final acceptance matrix.
- Test/evidence report.
- Changed-file summary and diff artifact.
- Remaining BLOCKED/DEFERRED items.
- Explicit statement of whether Phase 3 is complete, partially complete, or blocked.
Do not commit or push unless I explicitly authorize it.
```

Note: `/goal` has no iteration cap. Use this only for the bounded final audit, monitor progress, and cancel it if it starts repeating work without new evidence.
