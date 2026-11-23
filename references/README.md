# Reference Library

This directory stores owner-provided source tools, screenshots, diagrams, and supporting technical material used by Misora Editor reviews.

## Protected reference tools

- `priconne-adv-tools/` contains the preserved Priconne ADV and related tool reference.
- Treat original files in this directory as read-only. Do not rename, reformat, move, delete, or execute them as part of routine review.
- If experiments are needed, work on a separate copy and label it clearly.
- Do not assume that every capability of the reference tool belongs in Misora Editor.

## Assets

- `assets/` contains owner-provided screenshots, diagrams, and images.
- Preserve original names and bytes.
- AI reviewers must report whether each image was actually opened and visually inspected. A filename is not evidence of image contents.

## Archives and extracted sources

- Any archive may be stored in this folder or elsewhere in the repository; Phase 0 must inspect the actual current tree rather than assume a fixed path.
- Keep original archives immutable.
- Verify archive integrity where possible before extraction.
- Extract into a dated staging folder and preserve the archive's original directory structure.
- Record file counts, sizes, SHA-256 hashes, extraction errors, provenance, and duplicate relationships.
- Do not delete the original archive or consolidate duplicate-looking tools without explicit owner approval.

## Public repository safety

Do not add runtime databases, live game bundles, decrypted asset payloads, private translation dictionaries, secrets, credentials, or personal data to this public repository.

Create or update a source catalog only after the corresponding tools have actually been inspected. Each catalog entry should record original path, program name, purpose, entry points, dependencies, data formats, tests, version/history clues, license, SHA-256, duplicate relationships, evidence inspected, and whether the tool is a candidate for reuse.
