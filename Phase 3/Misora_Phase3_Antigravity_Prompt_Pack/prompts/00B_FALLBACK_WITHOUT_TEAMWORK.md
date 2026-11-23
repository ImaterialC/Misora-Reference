# FALLBACK — WHEN `/teamwork` IS NOT AVAILABLE

Use this route if `/teamwork` is absent from the command menu or your account/session cannot launch it. It keeps work in the currently opened `D:\Misora-Editor` workspace.

## Step 1 — Plan the whole cycle, read-only

```text
/plan

We are in Misora-Editor PROJECT PHASE 3 implementation. Phase 2.5 is locked. Read the locked canonical ledger at:
https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Phase_2.5_Canonical_Ledger_LOCKED.md
Expected ledger blob SHA: e51291724d485eebbe18142f68ecdc4fdf4a7c1b.

Inspect the current workspace, git status, local HEAD, tests, fixtures, AGENTS.md, PROJECT_STATE.md and README.md. Do not edit source files yet. Do not reset/clean/checkout, stash or delete user data. Produce a reviewable plan for Groups A-G in the ledger's exact dependency order, with one milestone per group and testable acceptance criteria. The target repository baseline recorded in the ledger is 683724edaf2afac89d2695a80e30a471a0da9195; if local HEAD differs, report the delta and preserve all local changes rather than forcing a reset. Do not ask to reconfirm any locked Project Lead decision.

The plan must preserve all hard guardrails: binary command IDs 35 and 32 unchanged; clearing a speaker never merges adjacent narration boxes; multi-segment edit/Undo retains segment splits; .misora v1 is references/state/stable locks only; no drafts/binaries; no worker-thread Tk calls; sparse CSIF is transactional; Translation Lock is enforced in model logic; no broad rewrite, no second Unity writer, no legacy dataminer, no copyrighted AtlasAdv assets; no commits/pushes.

Do not proceed with edits until I approve the Implementation Plan artifact.
```

## Step 2 — Execute one group at a time

After reviewing and approving the Implementation Plan, start a separate session/turn with the matching milestone prompt:
- `01_GROUP_A_BASELINE_HYGIENE.md`
- `02_GROUP_B_AST_CODEC.md`
- `03_GROUP_C_DOCUMENT_UNDO.md`
- `04_GROUP_D_SEARCH_REPLACE.md`
- `05_GROUP_E_XUAT.md`
- `06_GROUP_F_MTL_LIFECYCLE.md`
- `07_GROUP_G_UI_FEATURES.md`

Do not paste all seven milestone prompts at once. After a milestone, review the diff and tests, then issue `/compact` with a checkpoint before starting the next group.

## Step 3 — Use swarm only for cleanly separable work

For a read-only independent audit, or for tasks split by exclusive file ownership, use:

```text
/swarm

Audit the just-completed Misora milestone against the locked canonical ledger. Keep this swarm READ-ONLY: do not edit files. Assign one worker to inspect the changed core modules, one to inspect the GUI integration, one to inspect the added regression tests, and an independent verifier using a different available model to challenge the findings. Return canonical IDs, exact file/function references, test gaps and a PASS/FAIL/BLOCKED verdict. Do not reopen locked decisions or infer runtime/game behavior from source alone.
```

Do not parallelize workers that edit the same file. `misora.py`, `core/story_ast.py`, `core/script_codec.py`, and `core/undo_journal.py` are high-collision files; prefer sequential fixes or strict exclusive ownership.

## Step 4 — Deep bugs

Use `/boost` only for one coupled problem at a time (BUG-02, BUG-07, BUG-14, BUG-27, BUG-33 are good examples). It is a hard-bug workflow, not a substitute for the milestone plan.

## Step 5 — Finish with the final audit

Use `08_FINAL_ACCEPTANCE_AUDIT.md` only after all milestone reports are present. Do not claim completion while a required P0/P1 gate is failing or lacks evidence.

