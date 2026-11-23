/plan Implement Session S01: Documentation & Ledger Reconciliation (HYG-01) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @README.md

==================================================
PART 0 - EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. Planning-First Gate (STRICT): Do NOT modify any file during /plan. Inspect the live local
   workspace from disk, produce an Implementation Plan artifact, and WAIT for my approval
   (Proceed) before editing. After Proceed, execute and produce a Walkthrough artifact with
   real verification outputs.
2. Workspace & Git Hygiene: Report actual local Git branch, HEAD commit hash, git status --short,
   and the active Python 3.12 interpreter path/version. Expected pinned baseline is commit
   683724edaf2afac89d2695a80e30a471a0da9195 (v1.4.0). If HEAD differs or unexpected uncommitted
   changes conflict with this session, STOP and report in the Plan. NEVER run git reset, git clean,
   git stash, destructive git checkout, git commit, or git push.
3. Allowed File Ownership (after approval): PROJECT_STATE.md, README.md, AGENTS.md ONLY.
   DO NOT modify any .py file, tests/, core/, assets/, misora.bat, or any config file.
4. No new external dependencies. No code changes in this session (documentation only).
5. Never remove, skip, weaken, or mock existing tests. Never print secrets/API keys. Never
   overwrite local untracked files such as misora_config.json.
6. Stop strictly after S01. Do NOT implement any BUG-* or FEAT-* code fix here.

==================================================
PART 1 - PREFLIGHT VERIFICATION (INCLUDE IN PLAN)
==================================================
1. Report HEAD hash and git status --short.
2. In PROJECT_STATE.md, locate every occurrence of these slugs currently marked RESOLVED and
   report their exact line numbers: CMD0-SPECIAL-CASE, V2-ROUNDTRIP-LOSS, FIND-REPLACE-UI-ASYMMETRY,
   CONTINUOUS-RIBBON-TARGET-STALE, SIZE-RIBBON-NO-COMMIT, TRANSLATION-LOCK, CTRL-ALT-HOTKEYS-BLOCKED,
   BOX0-NO-SELECT-CHECKBOX, PLAINTEXT-SAVE-ROUTING, GAME-BOX-PREVIEW, MULTI-TEXTASSET-TARGET,
   API-KEYS-PLAINTEXT. Also locate the test-count claim (238 vs 234) and any S8b-2/S8b-3 test
   filename mismatch. Report what you find; if a slug is absent, say so (do not invent it).

==================================================
PART 2 - REQUIRED IMPLEMENTATION (HYG-01)
==================================================
Covers Phase 2.5 Canonical Ledger ID: HYG-01. Documentation only.
A. Downgrade each contradicted RESOLVED slug listed in Part 1 to REOPENED, appending the canonical
   ledger ID that reopens it (use this mapping): CMD0-SPECIAL-CASE->BUG-03; V2-ROUNDTRIP-LOSS->BUG-03;
   FIND-REPLACE-UI-ASYMMETRY->BUG-38; CONTINUOUS-RIBBON-TARGET-STALE->BUG-28; SIZE-RIBBON-NO-COMMIT->BUG-28;
   TRANSLATION-LOCK->BUG-12/BUG-16; CTRL-ALT-HOTKEYS-BLOCKED->BUG-29; BOX0-NO-SELECT-CHECKBOX->BUG-41;
   PLAINTEXT-SAVE-ROUTING->BUG-11; GAME-BOX-PREVIEW->FEAT-09/FEAT-10; MULTI-TEXTASSET-TARGET->BUG-09/DEF-03;
   API-KEYS-PLAINTEXT->BUG-33. Keep the historical text; add a dated REOPENED note, do not delete history.
B. Correct the test-count arithmetic note (state the verified per-suite total honestly; if you cannot
   verify the exact number from disk, mark it UNVERIFIED rather than guessing) and fix mismatched
   S8b-2/S8b-3 test filenames to the real files under tests/.
C. Record that local docs/ and storydata_1001005.unity3d were intentionally removed from GitHub and
   are now covered by .gitignore (per Project Lead). Do not claim they exist in the repo.
D. Update AGENTS.md: section 19 -> calibrated pixel overflow (50 digit-widths, 4+ lines, wrap=none,
   editor font is an estimate of game font); section 24 -> remove CSIF from the not-to-implement list
   (it shipped) and tie the MTL Drawer gate to Phase 2.5 P0/P1 closure; section 29 -> mark Ctrl+H
   verified fixed on Windows v1.4.0 (keep only bind_all break hygiene, HYG-07).
E. Clarify MULTI-TEXTASSET-TARGET status vs the open multi-TextAsset question (DEF-03).
F. Record Reference provenance: Phase_1_Gemini.md holds Gemini's dossier; Phase_1_Claude.md holds
   Claude's dossier. Active panel: Qwen (sole evaluator) + Gemini (Notulen); GPT/Claude/Grok parked.

==================================================
PART 3 - TESTS
==================================================
No new tests (documentation-only session). Regression Guard: the existing suite must remain green.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT)
==================================================
- Any code fix (BUG-01..BUG-41), any feature (FEAT-01..FEAT-14), any other hygiene item.
- Do not reopen settled Phase 2.5 decisions; do not add new requirements.

==================================================
PART 4 - VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. Now (/plan, ZERO edits): deliver Implementation Plan artifact and WAIT for Proceed.
2. After Proceed:
   - py -3.12 -m compileall -q misora.py core assets tests
   - py -3.12 -m unittest discover -s tests -v
   - Deliver Walkthrough with exact commands, real outputs, git status --short, and a concise
     summary of every documentation line changed. Handoff: ready for S02.