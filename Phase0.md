# Phase 0 — Repository Access and File Integrity Gate

**Purpose:** establish what the AI can actually access and inspect before any technical analysis begins.

This phase is mandatory for every participating AI, including ChatGPT, Gemini, Claude, Qwen, DeepSeek, Kimi, Grok, Meta AI, or any replacement model. Do not assume their browsing, GitHub, archive, image, or upload capabilities are identical.

## Required reading

Read:
- `README.md`
- `AGENTS.md`
- `docs/PROJECT_MANDATE.md`
- `docs/WORKFLOW_RULES.md`
- `docs/RESEARCH_AND_EVIDENCE.md`
- `docs/REPOSITORY_LAYOUT.md`
- `templates/PHASE0_ACCESS_REPORT.md`

## Repository targets

- Reference repository: https://github.com/ImaterialC/Misora-Reference
- Main application repository: https://github.com/ImaterialC/Misora-Editor

Inspect the actual current default branch and record the commit SHA. Do not rely only on old conversation context or a past repository snapshot.

## Tasks

### 1. Verify repository access

Determine whether you can:
- Open the repository page.
- Browse the complete current repository tree, including nested folders.
- Open and read text/source files.
- Access file contents rather than only filenames and metadata.
- Open and visually inspect images.
- Retrieve and inspect binary archives, if any are present.
- Inspect the main application repository, if accessible.

Report the actual access method and limitations. Do not claim a GitHub integration exists unless it is genuinely available in this conversation.

### 2. Inventory the current repository

Record the current branch and commit SHA. Enumerate all tracked files recursively where possible.

For each file, distinguish:
- File listed but not opened.
- Text/source file opened and read.
- Binary file listed but not decoded.
- Image visually opened and legible.
- Archive retrieved and extracted.
- File partially inspected due to output, token, or platform limits.

Do not infer file readability from a filename, extension, GitHub listing, or file size. If the repository is too large for a complete in-chat listing, say so and provide directory-level counts plus the exact inventory method and omissions. Do not silently omit files.

### 3. Inspect reference tools without analyzing their design yet

Pay special attention to `references/priconne-adv-tools/`. Verify which files are accessible and which folders are present. Do not execute tools or change their files during Phase 0.

If an archive such as `Misora-Reference.rar` is present, verify whether you can retrieve the actual bytes, extract it, and inspect the extracted files. Seeing an archive filename is not evidence that its contents were read.

### 4. Inspect supporting assets

For every image or diagram, distinguish whether it was actually opened and visually examined from whether only its name or metadata was visible. State if it is unreadable, cropped, too small, or otherwise unclear.

### 5. Use these status labels

- `READABLE` — opened and inspected successfully.
- `PARTIALLY_READABLE` — only part of the content inspected.
- `PRESENT_NOT_INSPECTED` — file exists, contents not inspected.
- `UNREADABLE` — attempted to open, but content could not be read.
- `ACCESS_RESTRICTED` — access blocked by permissions or platform.
- `MISSING` — expected file is not present in the current inspected tree.
- `NOT_EXTRACTED` — archive exists but its contents were not extracted.
- `CORRUPT` — actual evidence indicates file damage or invalid format.

Do not call a file corrupt merely because the platform cannot decode its format. That is an access limitation, not proof of damage.

## Required deliverable

Use `templates/PHASE0_ACCESS_REPORT.md` and return:

1. Repository access and exact commit information.
2. Recursive inventory or a clearly qualified inventory summary.
3. List of files actually opened and inspected.
4. Archive status and extraction status, if applicable.
5. Image visibility and legibility status.
6. Every file not inspected, partially inspected, inaccessible, or missing.
7. Exact owner action required to close the access gap.
8. Counts that are supported by the inspection; do not invent counts.

## Stop condition

**STOP after the report. Do not perform Phase 1 research, bug hunting, feature analysis, or implementation planning.**

Wait for the owner to review the report and explicitly confirm that the Phase 0 access gate is satisfied. If an important source file is unavailable, name it and request the specific file/folder or alternate format required.
