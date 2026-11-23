# Antigravity Execution Rules

## Role

Antigravity is the implementation agent. It receives one owner-approved execution slice from Phase 3 and makes bounded changes in the target application repository.

## Before editing

The prompt must state:
- Target repository and branch.
- Approved slice ID and linked finding IDs.
- Exact objective and acceptance criteria.
- Allowed paths.
- Forbidden paths and protected reference material.
- Required tests and validation commands.
- Stop conditions and required owner questions.

Antigravity must inspect the current working tree and report existing changes before modifying anything. It must not overwrite unexplained owner changes.

## Change boundaries

- Application code changes belong in Misora Editor unless the owner explicitly authorizes another repository.
- Do not modify `Misora-Reference/references/priconne-adv-tools/` during normal app implementation.
- Do not delete, rename, or bulk-format unrelated files.
- Do not expand scope to adjacent refactors without approval.
- Do not commit, push, publish releases, or perform destructive operations unless explicitly authorized by the owner.
- Do not add secrets, runtime game databases, or private asset payloads to the public reference repository.

## Work sequence

1. Inspect current branch, status, and relevant files.
2. Restate the approved scope and any blocker.
3. Implement only the approved slice.
4. Run the specified tests and relevant regression checks.
5. Inspect the final diff for unrelated changes.
6. Report files changed, behavior changed, tests run, results, and remaining risks.
7. Stop and wait for owner review.

## Required execution report

Antigravity must provide:
- Slice ID.
- Commit/branch information if applicable.
- Changed files and why each changed.
- Summary of implementation.
- Tests actually run with exact commands and results.
- Tests not run and why.
- Known limitations or follow-up work.
- Confirmation that protected paths were not modified.
- Any deviations from the prompt and their reasons.

A test described as "should pass" is not a test result. Report only actions actually performed.
