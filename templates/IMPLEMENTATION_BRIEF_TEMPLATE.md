# Approved Implementation Brief — <TASK>

**Status:** OWNER-APPROVED / DRAFT  
**Owner approval date:** YYYY-MM-DD  
**Target repository:** <owner/repo>  
**Workspace path:** <local path>  
**Branch / starting SHA:** <branch> / <sha>

## 1. Problem and evidence

<Describe the confirmed problem and cite source paths/lines or test output.>

## 2. Goal

<Exactly what should be true after implementation.>

## 3. Allowed files

- `path/to/file.py`

## 4. Forbidden files and out-of-scope behavior

- Do not modify files outside the allowed list without stopping and asking the owner.
- Do not remove, skip, weaken, or silently mock tests.
- Do not add dependencies unless explicitly approved.
- Do not commit or push unless explicitly requested.

## 5. Required implementation behavior

1. 

## 6. Acceptance criteria

- [ ] 

## 7. Verification commands

```powershell
# Confirm workspace and source-control state first
pwd
git rev-parse --show-toplevel
git status --short
git branch --show-current
git rev-parse HEAD

# Add exact project commands here after verifying the environment
```

Record actual command output, test count, failures, errors, skips, interpreter, and environment. If a test cannot run, report the blocker. Never claim success without output.

## 8. Data preservation and rollback

- Preserve user files and uncommitted changes.
- Do not run destructive reset/clean commands.
- Use a reversible change and explain rollback.

## 9. Required delivery report

- Files changed and reason for each.
- Concise diff summary.
- Exact verification commands and observed results.
- Remaining risks, skipped tests, and unverified items.
- Stop after this task. Do not start the next slice.
