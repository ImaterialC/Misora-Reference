---
trigger: always_on
description: Enforces Misora-Editor Phase 3 ledger scope, data-integrity invariants, safe Git behavior, and evidence-based verification.
---

# Misora Editor — Phase 3 Guardrails

The canonical authority is the locked ledger:
https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Phase_2.5_Canonical_Ledger_LOCKED.md
Expected blob SHA: `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`.

The project is in Phase 3 implementation. Phase 2.5 is locked and must not be reopened.

## Hard invariants
- Preserve numeric binary command IDs 35 and 32 unchanged until a real production `.unity3d` fixture proves otherwise.
- Clearing a speaker never merges adjacent narration boxes.
- Preserve multi-segment structure, voice cues, extra arguments and exact Undo/Redo snapshots.
- `.misora` v1 stores references/state/stable locks only, never drafts or binary blobs. Never serialize runtime Record.uid. Never silently remap unresolved locks.
- Translation Lock must be enforced in model/application code for every mutation path.
- Workers never call Tk APIs. Async results are delivered on the Tk main thread and revalidated by document/box/source identity.
- Sparse CSIF is absolute 1-based and transactional. Validation precedes mutation; failure leaves the document unchanged.
- Never turn inaccessible search files into “zero matches”; report skipped paths.
- Never silently replace immutable Japanese XUAT source keys with English translations.
- Raw Commands stays read-only until its lossless/transaction gates are proven.
- Preview uses the locked 50 digit-width / 4+ line bleed model, without auto-shrinking. Box 0 Summary remains unmeasured.
- Never remove unknown/meaningful interstitial records as if they were empty breakers.

## Execution rules
- Work only on canonical BUG/HYG/FEAT IDs from the locked ledger.
- Follow its dependencies and P0/P1 stabilization gates.
- Keep each milestone small and reviewable. Add a failing regression test before root-cause fixes where feasible.
- Record exact test commands, output, exit codes, skips and fixture limitations.
- Never weaken tests or invent verification evidence.
- Do not run destructive Git commands, delete ignored files, or commit/push without explicit approval.
- Ask before adding dependencies or changing binary/data formats.
- No broad `misora.py` rewrite, no second Unity writer, no legacy dataminer port, no AtlasAdv assets, no global XUAT pruning, no conflict_manager.

If the ledger, code, fixture, or test evidence conflict, stop the affected item and produce a discrepancy report. Do not silently choose a convenient interpretation.
