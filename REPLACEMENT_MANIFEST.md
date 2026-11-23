# Replacement manifest

Copy the contents of this package into the root of `ImaterialC/Misora-Reference`.

## Replace existing files

- `README.md`
- `INSTANT_ONBOARDING_PROMPT.md`
- `SECRETARY_PLAYBOOK.md`
- `plan_multi_ai_workflow_and_db_strategy.md`
- `plan_multi_ai_roster_and_workflow_strategy.md`

## Add new files

- `.gitignore`
- `AGENTS.md`
- `README_PAKET_PERBAIKAN_ID.md`
- `INSTALL_REPAIR_PACK_PROMPT.md`
- `templates/DEBATE_BRIEF_TEMPLATE.md`
- `templates/AI_REVIEW_TEMPLATE.md`
- `templates/DECISION_RECORD_TEMPLATE.md`
- `templates/IMPLEMENTATION_BRIEF_TEMPLATE.md`

## Not included / not modified

- `tools/secretary.py` is intentionally unchanged; documentation describes its actual commands.
- No `master.db`, Unity bundle, or other proprietary game asset is included.
- No source file in `Misora-Editor` is included.
- Existing debate transcripts and archives are not deleted or rewritten.
- The tracked `.pyc` cleanup is not performed by this package. The optional exact-path check and safe index-removal instruction are in `INSTALL_REPAIR_PACK_PROMPT.md`.
