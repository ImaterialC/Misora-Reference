<!-- ======================================================================
RECOMMENDED ANTIGRAVITY SETUP FOR S16
- Surface        : Antigravity App / IDE / CLI (`agy`)
- Command        : /plan (review Plan Artifact) -> Proceed
- Model & Effort : Claude Sonnet 4.6
- Cheap-Model OK : NO — Recommended Claude Sonnet 4.6 (multi-mode drawer state, queue delivery & model-level locks)
- Ledger Coverage: FEAT-12, FEAT-13 (Group G6 (post-DEP-6))
- Tip            : Paste everything BELOW the horizontal rule directly into Antigravity.
                   Review the Implementation Plan artifact (add inline comments if needed)
                   before clicking Proceed! Use `/compact` if session context grows noisy.
====================================================================== -->

---

/plan Implement S16: Docked Right-Side MTL Drawer (`Dialogue` Multi-Engine Stack & `All Script` 2-Widget Text + 5 Status Tags) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/mtl_engine.py @misora.py @tests/test_p3_s08_xuat_mtl_threading.py

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. **Planning-First Gate (STRICT):**
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`) directly from disk, produce a clear **Implementation Plan artifact**, and WAIT for my approval (`Proceed`) before editing any file.
   - After `Proceed`, execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. **Workspace & Git Hygiene:**
   - Report actual local Git branch, `HEAD` commit hash, `git status --short`, and active `py -3.12` interpreter path/version.
   - If unexpected uncommitted modifications conflict with `S16`, STOP and report them in the Implementation Plan.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`.
3. **Allowed File Ownership (after `Proceed`):**
   - Allowed to create/modify:
  * `misora.py (3rd right-drawer tab 'MTL' alongside Customize | NGUI Glossary; retire floating TranslatorAssistantDialog entry point; Dialogue enabled-engine vertical stack; All Script 2-widget tk.Text list + bottom scratchpad + 5 static status tags; session cache; paid-API confirm)`
  * `tests/test_p3_s16_mtl_drawer.py`
  * `PROJECT_STATE.md (verification update only)`
   - DO NOT modify:
  * `core/story_ast.py`
  * `core/xunity_sync.py`
  * `core/script_codec.py`
4. **No new external dependencies.** Follow all `@AGENTS.md` invariants and locked Phase 2.5 decisions (preserve binary `cmd_id` 35/32 unchanged; never call Tk from worker threads; isolate `misora.CONFIG_PATH` and `app.backup_folder` in tests).
5. **Never remove, skip, weaken, or silently mock existing tests.** Zero live network/API calls in unit tests.
6. **Stop strictly after `S16`.** Do NOT implement items belonging to later sessions.

==================================================
PART 1 — PREFLIGHT VERIFICATION (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live source files on disk and report exact current function names and line ranges for:
1. Verify S08 (`BUG-14`, `BUG-27`) and S01 (`AGENTS.md` §24 update) are green (`DEP-6`).
2. Inspect `_build_side_drawer()`, `_switch_side_drawer_tab()`, `on_open_translator_assistant()`, and `TranslatorAssistantDialog` in `misora.py`.
- Surface ANY discrepancy between these assumptions and live disk code in the Implementation Plan before editing.

==================================================
PART 2 — REQUIRED IMPLEMENTATION (FEAT-12, FEAT-13)
==================================================
Covers Phase 2.5 Canonical Ledger IDs: **FEAT-12, FEAT-13**

### A. **FEAT-12 (`U-B9`, `U-B32`):** Add **`MTL`** as the 3rd tab in the right-side drawer (`Customize` | `NGUI Glossary` | `MTL`), routing `Translator -> Translator Assistant...` and the `MTL` toolbar button to open/toggle this drawer (retiring the floating `TranslatorAssistantDialog` popup). In **`Dialogue` (1-box) mode**: stack cards vertically ONLY for user-enabled engines (default: `XUAT Cache` + `Google`; opt-in toggles for `DeepL` / `Local / Sugoi` / `LLM / OpenAI`). Each engine card has an editable scratchpad (isolated from story-widget routing + local Ctrl+Z), per-card `↻` Refresh (bypasses session cache), and per-card `→` Apply (enforces Translation Lock at model/application layer, commits via central path `source='mtl'`, NO `.strip()`). Top `Refresh All` refreshes enabled engines only, uses bounded session cache, and confirms before batch-calling paid APIs. ALL worker calls use main-thread `queue.Queue` + stale `(file_path, doc_id, box_uid, seq)` guard (`BUG-27`).

### B. **FEAT-13 (`U-B33` — LOCKED Lead Ruling #8, `NO-03`):** In **`All Script` mode**, switch the MTL right drawer to ONE engine selector at top + **EXACTLY 2 Text widgets**: (1) ONE read-only multi-line `tk.Text` list of clickable per-box tagged blocks (rendering full 2–3 line translations without `Treeview` truncation) + (2) ONE shared bottom editable `tk.Text` scratchpad synced to the clicked box. Configure 5 shared static theme-aware status tags: `✓` Ready, `⏳` Translating, `⚠` Error/Timeout, `🔒` Locked (grayed via theme `fg_muted`), `-` Untranslated/Empty/Punct-only (grayed via theme `fg_muted`). Provide Refresh Selected, Apply Selected, Translate All, and Apply All (reusing lock-skipping queue/batch pipeline; target box by stable `box.uid`; model-level lock check).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create/update `tests/test_p3_s16_mtl_drawer.py` using `unittest` conventions (preserve/restore `misora.CONFIG_PATH` AND redirect `app.backup_folder` to a `TemporaryDirectory` in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, zero live network calls).

- **Defect / Behavior Probes (MUST FAIL before patch, PASS after patch):**
1. [Probe 1 — FEAT-12] Opening MTL opens right-side drawer 3rd tab (no floating Toplevel); Dialogue mode stacks only enabled engines; per-card Apply honors model-level Translation Lock and preserves whitespace; paid engine Refresh All triggers confirmation.
2. [Probe 2 — FEAT-13] Switching to `All Script` mode renders EXACTLY 2 `tk.Text` widgets inside MTL drawer (read-only multi-line list + bottom scratchpad; ZERO per-box Text editors and ZERO `Treeview`); 5 static status tags exist (`✓`, `⏳`, `⚠`, `🔒`, `-`) with locked/empty using `fg_muted`; Apply All skips locked boxes.
3. [Probe 3] Switching files while an MTL drawer request is in flight discards the stale result cleanly.

- **Regression Guards (MUST PASS both before AND after patch — pre-patch contracts only):**
1. [Guard 1] `tests/test_p3_s08_xuat_mtl_threading.py` and `tests/test_s8a_dialog_grab_safety.py` pass.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN THIS SESSION)
==================================================
- Do NOT merge `Import from XUAT` into the MTL drawer (`NO-09`). Do NOT use `ttk.Treeview` or 142 separate `tk.Text` widgets (`NO-03`).
- All explicitly deferred items (`DEF-01..DEF-10`) and rejected non-goals (`NO-01..NO-12`) from the locked Phase 2.5 Canonical Ledger.

==================================================
PART 4 — VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. **Now (`/plan` — ZERO file edits):** Deliver the Implementation Plan artifact and WAIT for `Proceed`.
2. **After `Proceed`:**
   - Write `tests/test_p3_s16_mtl_drawer.py` -> run pre-fix (`py -3.12 -m unittest tests.test_p3_s16_mtl_drawer -v`) and record Probes FAILING & Guards PASSING.
   - Implement Part 2 changes cleanly.
   - Run `/misora-verify` (or exact Windows commands):
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_p3_s16_mtl_drawer -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** containing exact commands run, real observed test output, `git status --short`, concise diff summary, and confirmation that `backups/` and `misora_config.json` were untouched.
