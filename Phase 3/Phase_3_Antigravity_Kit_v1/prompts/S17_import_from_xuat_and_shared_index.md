<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S17
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> /boost (or Sonnet 4.6 Proceed)
- Model & Effort : Claude Sonnet 4.6 (or Opus 4.6 for Plan/Verify — flagship translator workflow feature)
- Cheap-Model OK : NO — Recommended Claude Sonnet 4.6 / Opus 4.6
- Ledger Coverage: FEAT-14 (Group G7 (Final Cycle Deliverable — post-DEP-2, DEP-7))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S17: Shared `core/xuat_index.py` & Native `Import from XUAT` Floating Resolver (`3x50` Read-Only Paired View) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/xunity_sync.py @core/ngui_tags.py @core/text_encoding.py @misora.py @tests/test_p3_s08_xuat_mtl_threading.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S17`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/xuat_index.py (NEW single-pass background XUAT indexer + backslash-parity \n unescape)`
  * `core/__init__.py (export xuat_index symbols)`
  * `core/mtl_engine.py (use normalized index lookup to fix QW-E03 O(N) scan when XUAT index is provided)`
  * `misora.py (Import -> Import from XUAT... menu entry, auto-close MTL drawer on open, ImportFromXUATDialog floating window, wire unified XUAT cache into var_xuat_cache / D11)`
  * `tests/test_p3_s17_import_xuat.py`
  * `PROJECT_STATE.md (final cycle verification update)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/bundle_io.py`
  * `core/script_codec.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S17`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Verify S05 (`BUG-11`, `BUG-12`), S07 (`BUG-23`), S08 (`BUG-25`), and S16 (`FEAT-12`/`FEAT-13` MTL drawer auto-close hook) are green.
2. Inspect `core/xunity_sync.py:split_xuat_line()` and `escape_xuat_value()`, and `core/ngui_tags.py:strip_tags()` so `core/xuat_index.py` reuses canonical parsers without duplicating logic.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FEAT-14)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **FEAT-14**

### A. **`core/xuat_index.py` (Single Shared Indexer — `CLAUDE-N07`, `QW-E03`, `RF-3`):** Build ONE background-safe in-memory XUAT dictionary indexer scanning strictly `BepInEx\Translation\en\Text` (excluding `.missing.txt`, `.report.txt`, `_SUMMARY.txt`, `_warnings.txt`), unified with `var_xuat_cache`/`D11` (eliminating `QW-E03` O(N) scan in `core/mtl_engine.py`). Implement symmetric backslash-parity-aware `unescape_xuat_value()` (literal `\n` -> real Enter newline while preserving `\\n`). Explicitly avoid ALL 6 `advscript.py` traps (`GEM-R01`: use `split_xuat_line()` first unescaped `=`, no block-mode hijack, no unconditional global conflict resolution, no unordered set slice, NGUI-tag & `{playername}`/`{0}`-aware normalization, NO global XUAT pruning) AND `priconne_tool.py`'s speaker-blind completion (`GEM-R02`: track dialogue & speaker match counts separately) AND `asset_registry.py`'s 3-tuple `find_match` trap (`GEM-R04`). ZERO `conflict_manager` (`NO-09`).

### B. **`ImportFromXUATDialog` (`U-B34` — LOCKED Lead Ruling #9):** Entry strictly under **File/Import -> Import from XUAT...** (separate floating window, NOT inside MTL drawer; auto-closes MTL drawer if open). Layout: single outer scrollable list of **paired rows** — Left = Story boxes (`All Script` style), Right = XUAT search match. **BOTH Left and Right boxes are strictly READ-ONLY** (`state='disabled'`) with **fixed `3 lines × 50 digit-widths` dimensions** (via S14's shared pixel-measure helper) and **NO visible per-box scrollbars**. Normal wheel scrolls the outer list; overflowing boxes display a subtle indicator (`▼`/`▶`) and clicking/focusing a box enables inner vertical wheel + horizontal `Shift+Wheel`/drag. Duplicates show `◀ 1/N ▶` + `filename:line` provenance + 3-tier conflict scope (`This Box` default / `This Story` / `Global` opt-in). Per-box `Skip` checkbox + automatic gray-out & skip for editor-locked boxes (`🔒`). Top filter chips (`All | Duplicates | Missing | Matched`) + optional speaker translation checkbox with separate dialogue/speaker counts. Clicking Apply displays an **explicit Pre-Apply confirmation prompt** listing: (1) exact box numbers/ranges that WILL be imported, (2) exact box numbers skipped due to **Translation Lock (`🔒`)**, (3) exact box numbers skipped due to **User Skip checkbox**, and (4) missing/untranslated count. Commits as ONE atomic Undo batch (`source='xuat_import'`).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s17_import_xuat.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — `core/xuat_index.py`] Indexes `BepInEx\Translation\en\Text` strictly (skips `.missing.txt`/comments), splits on first unescaped `=`, unescapes `\n` -> real Enter while preserving `\\n`, normalizes NGUI tags & `{playername}`/`{0}` consistently, and eliminates O(N) lookup.
2. [Probe 2 — Dialog Contract] Opening `Import from XUAT` auto-closes MTL Drawer; both left & right boxes are `state='disabled'` fixed `3x50` with zero per-box Scrollbar widgets; duplicates expose `◀ 1/N ▶` + `filename:line`; locked boxes are auto-skipped and per-box Skip works.
3. [Probe 3 — Pre-Apply Confirmation & Atomic Undo] Pre-Apply prompt explicitly enumerates exact imported box numbers, lock-skipped box numbers, user-skipped box numbers, and missing count; confirming applies in ONE Undo batch (`Ctrl+Z` reverts all imported boxes cleanly) while preserving locked & skipped boxes and leaving XUAT `.txt` files on disk untouched (zero pruning).

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] Full `py -3.12 -m unittest discover -s tests -v` passes 100% green across the entire repository!

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- NO `conflict_manager`, NO global XUAT auto-pruning (`NO-09`), NO inline editing inside `Import from XUAT`, NO Text-Only Dataminer (`DEF-05`).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s17_import_xuat.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s17_import_xuat -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s17_import_xuat -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
