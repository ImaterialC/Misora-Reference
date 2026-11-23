# Repository Layout and Reference Handling

## Top-level layout

- `README.md` — repository entry point.
- `AGENTS.md` — instructions for AI agents.
- `PROMPTS.md` — short copy-paste prompts for each phase.
- `Phase0.md` to `Phase4.md` — canonical phase instructions; Phase 2.5 is the required sub-gate.
- `docs/` — project mandate, workflow, scope, evidence, status, and execution rules.
- `templates/` — report and audit templates.
- `references/` — source tools, assets, and supporting technical references.
- `sessions/` — optional dated outputs and decision records for a specific review session.

## Protected reference material

### Priconne ADV tools

Path: `references/priconne-adv-tools/`

Treat this directory as a read-only reference by default. Do not rename, reorganize, reformat, delete, or "clean up" files inside it as part of a Misora Editor task. Preserve original files and folder structure. If an experiment requires changes, create a separate copy outside the protected source directory and clearly mark it as an experiment.

The presence of this tool does not mean every capability, dependency, or workflow must be adopted by Misora Editor.

### Assets and screenshots

Path: `references/assets/`

Preserve original screenshots and diagrams. Do not rename or recompress them unless the owner approves. If an image cannot be opened in an AI surface, report that limitation instead of describing its contents from its filename.

### Future archives and extracted source

- Keep original archives immutable.
- Verify an archive before extracting it.
- Extract into a dated staging folder, preserving the original directory structure.
- Record file counts, sizes, SHA-256 hashes, extraction errors, and source provenance.
- Do not merge duplicate-looking folders until hashes and provenance have been compared.
- Do not delete the archive after extraction unless the owner explicitly approves.

## Public repository safety

Do not commit:
- Secrets, tokens, passwords, credentials, or private keys.
- Live runtime databases or database sidecar files.
- User-private translation dictionaries or unreleased personal work.
- Decrypted game bundles, complete live game asset payloads, or other large copyrighted payloads unless the owner has confirmed that public distribution is appropriate.
- Personal data or local machine paths that expose sensitive information.

Use `.gitignore` and a separate private/local workspace for runtime data.
