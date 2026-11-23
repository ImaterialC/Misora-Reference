/plan Implement S01: Docs, Ledger & AGENTS.md Topic-Safe Reconciliation + Initialize CHANGELOG.md in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @README.md

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **HYG-01** (Track 1 · Group A (DEP-10)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - Expected initial starting baseline is commit `683724edaf2afac89d2695a80e30a471a0da9195` (v1.4.0). If local HEAD differs or uncommitted changes exist, inspect and report the delta in the Implementation Plan; NEVER reset/clean/stash.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `PROJECT_STATE.md`
  * `README.md`
  * `AGENTS.md`
  * `CHANGELOG.md (CREATE with `## [Unreleased] (Target: v1.4.1)` and `### S01`)`
   - DO NOT modify:
  * `misora.py`
  * `__init__.py`
  * `core/*.py`
  * `assets/*.py`
  * `tests/*.py`
  * `misora_config.json`
5. **Changelog & Version Contract:**
   - Append `### S01` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S01`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Workspace Preflight (GPT standard): report exact branch, `git rev-parse HEAD` (expected initial S01 baseline `683724edaf2afac89d2695a80e30a471a0da9195`), `git status --short --branch`, staged/unstaged/untracked/ignored status (without printing secrets or `misora_config.json` values), active `py -3.12` path/version, and whether any local `.unity3d` fixtures exist.
2. Locate every contradicted `RESOLVED` slug in `PROJECT_STATE.md` (`CMD0-SPECIAL-CASE`, `V2-ROUNDTRIP-LOSS`, `FIND-REPLACE-UI-ASYMMETRY`, `CONTINUOUS-RIBBON-TARGET-STALE`, `SIZE-RIBBON-NO-COMMIT`, `TRANSLATION-LOCK`, `CTRL-ALT-HOTKEYS-BLOCKED`, `BOX0-NO-SELECT-CHECKBOX`, `PLAINTEXT-SAVE-ROUTING`, `GAME-BOX-PREVIEW`, `MULTI-TEXTASSET-TARGET`, `API-KEYS-PLAINTEXT`), plus §2 test-count arithmetic (`238` vs `234`) and S8b-2/S8b-3 test filenames.
3. Inspect live headings in `AGENTS.md` by topic (`NGUI single source`, `CSIF rules`, `UI safety`, `Scope discipline`, `Machine-confirmed release blockers`) and confirm exact lines before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (HYG-01)
==================================================
### A. **HYG-01 — `PROJECT_STATE.md` & `README.md`:** Reconcile against pinned starting commit `683724edaf2afac89d2695a80e30a471a0da9195`. Downgrade contradicted `RESOLVED` slugs to `REOPENED` with canonical ledger IDs (`CMD0-SPECIAL-CASE -> BUG-03`, `V2-ROUNDTRIP-LOSS -> BUG-03`, `FIND-REPLACE-UI-ASYMMETRY -> BUG-38`, `CONTINUOUS-RIBBON-TARGET-STALE -> BUG-28`, `SIZE-RIBBON-NO-COMMIT -> BUG-28`, `TRANSLATION-LOCK -> BUG-12/BUG-16`, `CTRL-ALT-HOTKEYS-BLOCKED -> BUG-29`, `BOX0-NO-SELECT-CHECKBOX -> BUG-41`, `PLAINTEXT-SAVE-ROUTING -> BUG-11`, `GAME-BOX-PREVIEW -> FEAT-09/FEAT-10`, `MULTI-TEXTASSET-TARGET -> BUG-09/DEF-03`, `API-KEYS-PLAINTEXT -> BUG-33`). Keep historical records (add dated `REOPENED` notes; do not delete history). Correct §2 test-count arithmetic from actual disk discovery and fix mismatched S8b-2/S8b-3 test filenames. Record intentional removal + `.gitignore` of local `docs/` and `storydata_1001005.unity3d`. Record Reference audit provenance (`Phase_1_Gemini.md` = Gemini's dossier; `Phase_1_Claude.md` = Claude's dossier; `Phase_2R1_Claude.md` = 22,852 B valid).

### B. **HYG-01 — `AGENTS.md` (BIND BY HEADING — DO NOT DESTROY EXISTING INVARIANTS):**
   - Under **`NGUI single source`** (currently §19): **KEEP the heading and the first three NGUI bullets (`core/ngui_tags.py`, hyphen gradients, `TagMasker`) INTACT.** Amend ONLY the fourth bullet (length-counter bullet) to specify pixel-calibrated measurement on rendered text excluding markup.
   - Under **`CSIF rules`** (currently §20): Amend only the opening phrase calling CSIF a future format (CSIF is shipped; keep all other CSIF rules intact).
   - Under **`UI safety`** (currently §21): Add the locked native overflow rule wording explicitly as **50 digit-widths without a linebreak OR 3 or more linebreaks (4 or more lines)** (editor font is a proxy/estimate of the in-game font; NEVER write ambiguous shorthand).
   - Under **`Scope discipline`** (currently §24): Remove already-shipped CSIF from the not-to-implement list and tie the MTL Drawer gate to Phase 2.5 Track 1 P0/P1 stabilization closure (`S01..S13`).
   - Under **`Machine-confirmed release blockers`** (currently §29): Mark ONLY `Ctrl+H` as verified fixed on Windows v1.4.0 (retaining `HYG-07` minor `bind_all` hygiene). Keep `ribbon Cut` and `Paste Box` blockers intact until their sessions and manual Windows tests pass.

### C. **Initialize `CHANGELOG.md` (Project Lead Contract):** Create `CHANGELOG.md` at repo root with `## [Unreleased] (Target: v1.4.1)` and append `### S01 — Docs, Ledger & AGENTS.md Reconciliation` recording `HYG-01`, modified files, and observed baseline `unittest discover` count. Keep `__version__ = '1.4.0'` unchanged until `S24`.

==================================================
PART 3 — VERIFICATION CHECKS (AFTER PROCEED)
==================================================
This is a documentation-only session (no new `.py` test module).
- **Anti-False-Pass Uniformity (`m2`):** Although S01 has no failing-first code probes, if any targeted doc check is ALREADY satisfied on disk, record `ALREADY PASSING / NOT REPRODUCED` honestly in the Walkthrough rather than fabricating edits; `Ran 0 tests` on full discovery is ALWAYS a failure.

- **Documentation Verification Checks:**
1. [Doc Check — HYG-01] Verify `AGENTS.md` retains the `NGUI single source` heading and all 3 NGUI pattern bullets intact, documents `50 digit-widths without a linebreak OR 3 or more linebreaks (4 or more lines)` under `UI safety`, removes CSIF from `Scope discipline`, and marks only `Ctrl+H` fixed in release blockers.
2. [Doc Check — CHANGELOG] Verify `CHANGELOG.md` exists with `## [Unreleased] (Target: v1.4.1)` and `### S01`.

- **Regression Guards (MUST PASS before AND after):**
1. [Guard 1] Zero `.py` files modified (`git status --short` lists ONLY `PROJECT_STATE.md`, `README.md`, `AGENTS.md`, `CHANGELOG.md`).
2. [Guard 2] `py -3.12 -m compileall -q misora.py core assets tests` exits 0 and `py -3.12 -m unittest discover -s tests -v` passes with 0 failures, 0 errors, 0 skips (record exact observed test count).

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- ZERO edits to any `.py` file (`BUG-01..BUG-41`, `FEAT-01..FEAT-14`, `HYG-02..HYG-08`). Do NOT bump `__version__` (happens once in `S24`).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Apply Part 2 documentation edits cleanly.
   - Run `/misora-verify --docs-only` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest discover -s tests -v` (confirm `Ran N tests` with `N > 0`, 0 failures, 0 errors, 0 skips)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, `git status --short`, concise diff summary, and handoff to `S02`.
