# Antigravity Prompt — Apply Misora Reference Repair Pack Safely

Use Plan mode first. This is a documentation and repository-hygiene task in **Misora-Reference only**.

## Required preflight

1. Confirm the Git root is the local `Misora-Reference` repository, not `Misora-Editor`.
2. Report the current branch, HEAD SHA, and complete `git status --short` before making changes.
3. If the working tree contains unexplained changes, stop and report them. Do not overwrite the user's changes.
4. Make no commit and do not push.
5. Never run `git clean`, `git reset --hard`, or a broad checkout/restore command.

## Apply the repair pack

The user has extracted `Misora-Reference-Repair-Pack` to a temporary folder. Copy the files listed in `REPLACEMENT_MANIFEST.md` into the root of this repository, preserving the `templates/` subfolder. Replace only the five explicitly listed existing Markdown files. Add the new files as listed. Do not copy the outer package folder itself into the repository.

Do not modify:

- `tools/secretary.py`
- Any file under `extractor_prototype/`, `reference_toolchains/`, `tests/`, or `archives/`
- Any file in `Misora-Editor`
- Any database, Unity bundle, or user transcript

## Tracked Python cache check

The audited remote `main` tree contained this tracked file:

`tests/__pycache__/test_extractor_prototype.cpython-312.pyc`

Check it rather than assuming it is still tracked:

```bash
git ls-files --error-unmatch tests/__pycache__/test_extractor_prototype.cpython-312.pyc
```

If and only if that exact path is still tracked, propose removing it from the Git index while retaining the local file:

```bash
git rm --cached -- tests/__pycache__/test_extractor_prototype.cpython-312.pyc
```

If the command says it is not tracked, do nothing. Do not remove other cache files in bulk.

## Review and verification

1. Show `git status --short` and `git diff --stat`.
2. Run `git diff --check`.
3. Inspect every changed file and verify that only manifest-approved files changed, plus the optional exact `.pyc` index removal above.
4. Confirm no `master.db`, `.db`, `.sqlite`, `.unity3d`, or other game-data binary was added.
5. Confirm the documentation describes only existing `secretary.py` commands: `status`, `verify-zips`, and `ingest`.
6. Confirm the documentation preserves AI disagreement and does not grant any model final decision authority.
7. Run existing safe local checks if the environment permits; report the actual commands and outputs. Do not claim tests passed without running them. If a check is blocked, name the blocker.
8. Stop and present the diff summary and verification report for the owner. Do not commit, push, or begin implementing new secretary features.

## Completion report

Return in Bahasa Indonesia with:

- Exact branch and starting/ending SHA.
- Every file added/replaced.
- Whether the tracked `.pyc` path still existed and what was done.
- Output of `git diff --check` and any tests actually run.
- Confirmation that no application source, database, or archive/transcript was modified.
- Any unexpected issue requiring the owner's decision.
