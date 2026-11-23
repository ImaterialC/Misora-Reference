/plan Implement S22: Unified `core/xuat_index.py` & Separate Floating `Import from XUAT` Resolver (Paired Fixed `3×50` Read-Only) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING — DO NOT TRUST CHAT SUMMARIES):
@AGENTS.md @PROJECT_STATE.md @core/xunity_sync.py @core/ngui_tags.py @core/text_encoding.py @misora.py @tests/test_p3_s10_xuat_integrity.py

CANONICAL AUTHORITY: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).
SESSION SCOPE: **FEAT-14** (Track 2 · Group G7 (post-DEP-2, DEP-7)).

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source, test, or doc file during this `/plan` phase.
   - Inspect live `D:\Misora-Editor` directly from disk, produce an **Implementation Plan artifact**, and WAIT for the Project Lead to click `Proceed`.
   - Do NOT use `/grill-me`, `/teamwork`, `/browser`, `/run-workflow`, or `/automation`. Requirements are locked; this is a Windows Tkinter desktop app.
2. **Workspace, Baseline & Git Hygiene:**
   - Report actual local Git branch, `git rev-parse HEAD`, `git status --short --branch`, and `py -3.12` executable path & version.
   - `683724edaf2afac89d2695a80e30a471a0da9195` is the initial S01 reference only. `S22` starts from the accepted tree of the preceding session (either manually committed by the Project Lead or an authorized uncommitted tree). Do NOT treat expected changes from prior sessions as unexpected drift; STOP only if unrelated conflicting edits exist.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`.
   - NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER write test `.bak_*` files into repo root `backups/`.
3. **Symbol-Binding Rule (Anti-Line-Rot):**
   - Any line numbers referenced in the ledger are hints from commit `683724e`. Bind by **function/class/symbol name**.
   - Shifted line numbers from earlier accepted sessions are NOT a discrepancy. Missing or contradictory behavior IS a STOP — report it in the Implementation Plan instead of guessing.
4. **Allowed File Ownership (ONLY after `Proceed`):**
   - Allowed to create/modify:
  * `core/xuat_index.py (NEW single-pass background XUAT indexer + backslash-parity `\n` unescape)`
  * `core/__init__.py (export `xuat_index` symbols)`
  * `core/mtl_engine.py (use normalized index lookup to fix `QW-E03` O(N) scan when XUAT index provided)`
  * `misora.py (`File/Import -> Import from XUAT...` menu entry, auto-close MTL drawer on open, `ImportFromXUATDialog` floating window, unify `var_xuat_cache`/`D11`)`
  * `tests/test_p3_s22_import_xuat.py (NEW)`
  * `CHANGELOG.md (append `### S22` under `## [Unreleased]`)`
  * `PROJECT_STATE.md (measured verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/bundle_io.py`
  * `core/script_codec.py`
5. **Changelog & Version Contract:**
   - Append `### S22` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` (except `S24` which promotes `## [Unreleased]` to `## [1.4.1]` and bumps `__version__` ONCE).
   - Keep `__version__ == '1.4.0'` untouched in `S01..S23`.
6. **Invariants:** No new external dependencies; preserve `cmd_id` 35/32 unchanged; never call Tk from worker threads; never weaken/skip/mock existing tests; stop strictly after `S22`.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live files on disk and report exact current symbol locations/line ranges for:
1. Verify `DEP-2` (S06 `BUG-11`), `DEP-7` (S08 `BUG-23`, S10 `BUG-25`), S17 shared pixel-measure helper, and S20/S21 MTL drawer auto-close hook are green.
2. Bind by symbol name: `split_xuat_line` / `escape_xuat_value` in `core/xunity_sync.py`, `strip_tags` in `core/ngui_tags.py`.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FEAT-14)
==================================================
### A. **`core/xuat_index.py` (Single Shared Indexer — `CLAUDE-N07`, `QW-E03`, `RF-3`):** Build ONE background-safe in-memory XUAT dictionary indexer scanning strictly `BepInEx\Translation\en\Text` (excluding `.missing.txt`, `.report.txt`, `_SUMMARY.txt`, `_warnings.txt`), unified with `var_xuat_cache`/`D11` (eliminating `QW-E03` O(N) scan in `core/mtl_engine.py`). Implement symmetric backslash-parity-aware `unescape_xuat_value()` (literal `\n` -> real Enter newline while preserving `\\n`). Avoid ALL 6 `advscript.py` traps (`GEM-R01`: `split_xuat_line()` first unescaped `=`, no block-mode hijack, no unconditional global conflict resolution, no unordered set slice, NGUI-tag & `{playername}`/`{0}`-aware normalization, NO global XUAT pruning) AND `priconne_tool.py`'s speaker-blind completion (`GEM-R02`: track dialogue & speaker match counts separately) AND `asset_registry.py`'s 3-tuple `find_match` caller trap (`GEM-R04`). ZERO `conflict_manager` (`NO-09`).

### B. **`ImportFromXUATDialog` (`U-B34` — LOCKED Lead Ruling #9):** Entry strictly under **File/Import -> Import from XUAT...** (separate floating window, NOT inside MTL drawer; auto-closes MTL drawer on open). Layout: single outer scrollable list of **paired rows** — Left = Story boxes (`All Script` style), Right = XUAT search match. **BOTH Left and Right boxes are strictly READ-ONLY** (`state='disabled'`) with **fixed 3 lines × 50 digit-widths** (via S17's shared pixel-measure helper) and **NO visible per-box scrollbars**. Normal wheel scrolls the outer list; overflowing boxes display a subtle indicator (`▼`/`▶`) and clicking/focusing enables inner vertical wheel + horizontal `Shift+Wheel`/drag. Duplicates show `◀ 1/N ▶` + `filename:line` provenance + 3-tier conflict scope (`This Box` default / `This Story` / `Global` opt-in). Per-box `Skip` checkbox + auto-skip & gray-out for locked boxes (`🔒`). Top filter chips (`All | Duplicates | Missing | Matched`) + optional speaker translation checkbox with separate dialogue/speaker counts. Explicit **Pre-Apply confirmation prompt** listing: (1) exact box numbers/ranges to import, (2) exact boxes skipped due to **Translation Lock (`🔒`)**, (3) exact boxes skipped due to **User Skip checkbox**, and (4) missing/untranslated count. Commits as ONE atomic Undo batch (`source='xuat_import'`).

### C. **`CHANGELOG.md`:** Append `### S22` under `## [Unreleased] (Target: v1.4.1)`.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER PROCEED)
==================================================
Create/update `tests/test_p3_s22_import_xuat.py` using `unittest` conventions:
- Preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `tempfile.TemporaryDirectory` in `setUp`/`tearDown`.
- Suppress modal `messagebox` popups on automated error paths; ZERO live network/API calls.
- **Anti-False-Pass Rule:** Run `tests.test_p3_s22_import_xuat` BEFORE patching production code. Every **Defect Probe** MUST fail and every **Regression Guard** MUST pass. If any Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` with evidence — NEVER weaken the probe and NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure.

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — `core/xuat_index.py`] Indexes `BepInEx\Translation\en\Text` strictly (skips `.missing.txt`/comments), splits on first unescaped `=`, unescapes `\n` -> real Enter while preserving `\\n`, normalizes NGUI tags & `{playername}`/`{0}` consistently, and uses O(1) normalized lookup.
2. [Probe 2 — Dialog Contract] Opening `Import from XUAT` auto-closes MTL Drawer; both left & right boxes are `state='disabled'` fixed 3 lines × 50 digit-widths with zero per-box Scrollbar widgets; duplicates show `◀ 1/N ▶` + `filename:line`; locked boxes auto-skip and per-box Skip works.
3. [Probe 3 — Pre-Apply Prompt & Atomic Undo] Pre-Apply prompt enumerates exact imported box numbers, lock-skipped box numbers, user-skipped box numbers, and missing count; confirming applies in ONE Undo batch (`Ctrl+Z` reverts cleanly), preserves locked & skipped boxes, and leaves XUAT `.txt` files untouched (zero pruning).

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests.test_p3_s10_xuat_integrity`, `tests.test_p3_s06_doc_state_save`, and `tests.test_p3_s21_mtl_drawer_all_script` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- NO `conflict_manager`, NO global XUAT auto-pruning (`NO-09`), NO inline editing in `Import from XUAT`, NO Text-Only Dataminer (`DEF-05`).
- All deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s22_import_xuat.py` -> run pre-patch (`py -3.12 -m unittest tests.test_p3_s22_import_xuat -v`) and record Probes FAILING & Guards PASSING (or STOP if a Probe already passes).
   - Implement Part 2 changes cleanly and update `CHANGELOG.md`.
   - Run `/misora-verify tests.test_p3_s22_import_xuat` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s22_import_xuat -v` (`Ran 0 tests` = FAIL!)
     * `py -3.12 -m unittest discover -s tests -v` (`Ran 0 tests` = FAIL!)
   - Deliver a **Walkthrough artifact** containing exact commands, real stdout, pre-patch vs post-patch test evidence, `git status --short`, concise diff summary, any `BLOCKED` fixture items, and confirmation that `backups/` and `misora_config.json` were untouched.
