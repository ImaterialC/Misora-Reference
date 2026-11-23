<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S07
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> /boost (after Proceed)
- Model & Effort : Claude Opus 4.6 (HIGH risk: search threading, project root security, multi-file bundle Replace-All & BulkFileDelta undo)
- Cheap-Model OK : NO — Use Claude Opus 4.6 (or Claude Sonnet 4.6 minimum)
- Ledger Coverage: BUG-21, BUG-22, BUG-23, BUG-24, HYG-05 (Group D (DEP-7 part 1))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S07: Search Options/Errors/Snapshots/Spans, Bounded Project Roots & Multi-File Replace-All/Undo Integrity in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/search_engine.py @core/story_ast.py @misora.py @tests/test_s5_bulk_replace_safety.py @tests/test_s6_threading_decoupling.py @tests/test_s9a_search_unicode.py @tests/test_s9b_replace_all_bundle_safety.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S07`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `core/story_ast.py (ONLY norm_search match_case parameter)`
  * `core/search_engine.py (import Any, match_case in _norm_search_with_spans/_compile_matcher, skipped/error reporting + os.walk onerror, raw-text fallback span fix)`
  * `misora.py (_detect_environment, _on_folder_path_var_trace, on_browse_project_folder, on_open_paths_dialog, on_start_search, _run_background_search, _process_search_queue, on_replace_next, on_replace_all, _apply_delta BulkFileDelta)`
  * `tests/test_p3_s07_search_replace.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/xunity_sync.py`
  * `core/mtl_engine.py`
  * `core/script_codec.py`
  * `core/bundle_io.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S07`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Inspect `core/search_engine.py` (imports line 15, `_norm_search_with_spans` line 89, `_compile_matcher` 174-220, `search_file` 250-375, `search_directory` 377-421).
2. Inspect `misora.py`: `_detect_environment` (2725-2765), `on_start_search` (8613-8697), `_run_background_search` (8714-8750), `on_replace_next` (9195-9243), `on_replace_all` (9279-9505), `_apply_delta(BulkFileDelta)` (9661-9735).
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (BUG-21, BUG-22, BUG-23, BUG-24, HYG-05)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **BUG-21, BUG-22, BUG-23, BUG-24, HYG-05**

### A. **HYG-05 (`core/search_engine.py`):** Import `Any` from `typing` so `typing.get_type_hints()` succeeds cleanly.

### B. **BUG-21 (`core/story_ast.py` + `core/search_engine.py`):** Add `match_case: bool = False` to BOTH `story_ast.norm_search()` and `ProjectSearchEngine._norm_search_with_spans()` (preserving 100% S9a equivalence), applying `.casefold()` ONLY when `not match_case`. Wire `options.match_case` into whitespace-insensitive matching in `_compile_matcher()`.

### C. **BUG-22 (`core/search_engine.py` + `misora.py`):** (1) Stop swallowing bundle/text decode errors silently; add `os.walk(..., onerror=...)` and return/accumulate structured `(path, reason)` skipped errors surfaced in the search result UI (clearly distinguishing 0 matches / matches / partial skipped / cancelled). (2) In `on_start_search()`, on snapshot failure NEVER fall back to live `orig_doc` (`Grok-E02`) — skip and report it; also snapshot open plain-text buffers and normalize `mem_docs` keys via `Path.resolve()`. (3) Add monotonic `self._search_seq` generation guard and ignore re-entrant `<Return>` while searching. (4) In `search_file()` raw-text fallback (lines 302-308), do NOT fabricate `(0, len(box.clean_text))` — either map raw spans accurately or mark approximate raw-only match (`QW-E06`).

### D. **BUG-23 (`misora.py` — `GEM-N01`):** Replace (NEVER append indefinitely) project roots whenever `project_folder` changes; stop auto-injecting unrelated local `input`/`output`. Add a clean bounded root resolver: Project Search resolves strictly to `(Text, RedirectedResources)` (never scanning `BepInEx/plugins/` or `config/`), while XUAT text roots resolve strictly to `BepInEx\Translation\en\Text`.

### E. **BUG-24 (`misora.py`):** (1) Fix `_apply_delta(BulkFileDelta)` and its rollback block to use canonical `open_documents` keys `'env'` and `'obj'` (NOT `'bundle_env'`/`'target_object'`) and dispose old `env` properly. (2) Refresh/invalidate ALL affected open document caches (not only `current_file_path`); refuse/prompt before overwriting open dirty documents from disk; do NOT mark disk-saved files dirty; resolve & deduplicate candidate paths. (3) Share ONE compiled matcher (honoring `Match Case`, `Regex`, `Ignore Whitespace`, preserving `break_char` per `QW-R06`) and Translation Lock policy across Find, `on_replace_next()` (skip locked boxes in advance loop!), and `on_replace_all()` (enforce locks in multi-file too). (4) Multi-file `BulkFileDelta` Undo/Redo must NEVER silently reopen closed tabs (`AGENTS.md` §16) — show an explicit confirmation listing all affected paths (including currently closed disk files) before touching disk.

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s07_search_replace.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — HYG-05 & BUG-21] `typing.get_type_hints(ProjectSearchEngine.search_directory)` succeeds; Match Case ON + Ignore Whitespace ON matches `'Hero'` and rejects `'hero'` with exact span equivalence.
2. [Probe 2 — BUG-22] Corrupt/unreadable file appears in `skipped` list (never silently 0); failed AST snapshot skips file instead of passing live `orig_doc`; stale `search_seq` messages are discarded; raw-text fallback does not fabricate full-box clean spans.
3. [Probe 3 — BUG-23] Switching `project_folder` from ProjA to ProjB removes ProjA completely from search roots; selecting a `BepInEx` root scans only `Text` and `RedirectedResources` (ignores `plugins/`).
4. [Probe 4 — BUG-24] Multi-file Replace-All + Undo updates inactive open bundle cache using `'env'`/`'obj'`, disposes old env (`weakref`), respects Regex/Case/Locks, skips locked boxes in `on_replace_next()` advance loop, and prompts before modifying closed files on Undo.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_s5_bulk_replace_safety.py`, `test_s6_threading_decoupling.py`, `test_s9a_search_unicode.py`, `test_s9b_replace_all_bundle_safety.py` all pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT build Replace-All dry-run diff pane (`DEF-09`) or background bulk-replace worker (`DEF-07`) or XUAT importer (`S17`).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s07_search_replace.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s07_search_replace -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s07_search_replace -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
