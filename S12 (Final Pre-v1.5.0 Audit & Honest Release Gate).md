/plan Execute S12 (Final Pre-v1.5.0 Audit & Honest Release Gate): Deep Read-Only Bloat, Dead-Code, and Memory-Leak Audit of `misora.py`/`core/`/`assets/`, Non-Fixture Test Hygiene Fixes, Updated Invariant Documentation, Full Stress Verification, and Conditional `v1.5.0` Release Gate Evaluation.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @CHANGELOG.md @README.md @__init__.py @misora.py @core/ @assets/ @tests/

==================================================
PART 0 — EXECUTION MODE, HARD-STOP AUDIT RULE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. Planning-First Gate: Perform the full **READ-ONLY** audit during `/plan` (using read-only file inspection and read-only `py -3.12 -c "..."` AST/grep commands — writing ZERO temporary files to disk), present the complete Audit Findings + S12 Plan artifact, and STOP to wait for explicit user `Proceed`.
2. **HARD-STOP SOURCE RULE:** `misora.py`, `core/*.py`, and `assets/*` are **STRICTLY READ-ONLY** in S12.
   - If the audit discovers ANY new P0/P1 source bug or memory leak in `misora.py`, `core/*.py`, or `assets/*`, **DO NOT silently patch it in S12** — record it with exact `file:line` proof as a Release Gate BLOCKER for a dedicated follow-up fix session, and HOLD version at `"1.4.10"`.
   - Any confirmed 0-caller dead code (e.g., retired `get_voice_badge_image`, `get_all_script_card_*`, old Technique A remnants) MUST be cataloged with AST/grep proof for a separate Project-Lead-approved cleanup pass (do NOT delete production source code silently inside S12).
3. **Config & Environment Safety:** NEVER read, overwrite, restore, or modify the user's local `misora_config.json`, `backups/`, or untracked files. Never fall back to user config to make tests pass.
4. **Honest Release Gate (`BLOCKED != PASS`):** Never fake, skip, or weaken fixture-gated tests (`storydata_1001005.unity3d`), and never waive manual Windows QA on behalf of the Project Lead.
5. No Destructive Git Commands & No New Third-Party Dependencies.

==================================================
PART 1 — STRICT FILE OWNERSHIP BOUNDARIES
==================================================
Allowed Files to Modify (ONLY after `Proceed`):
- `AGENTS.md` (update permanent invariants: `50d` -> `54d`, Box 0 exemption, Virtualized Card Pool contract, RM-01 console removal)
- `PROJECT_STATE.md` (record S12 audit report, full-suite results, 100% traceability audit, blocker taxonomy, and final Manual Windows QA checklist)
- `CHANGELOG.md` (add S12 audit/gate entry; promote `[Unreleased]` -> `[1.5.0]` ONLY if ALL release-gate criteria pass AND Project Lead explicitly confirms promotion)
- `README.md` (sync version badge & test/feature overview)
- `tests/test_v15_s01_stability_remediation.py` (fix `test_probe_8` hardcoded `"1.4.1"` -> dynamic root `__init__.__version__` parity)
- `tests/test_phase3_performance_config.py` (isolate `test_05` strictly from local `misora_config.json` via temporary test-owned fixture; NEVER touch user config)
- `tests/test_s9c_workspace_safety.py` (fix `test_04` cleanly per repo `misora_config.default.json` contract — verify in `/plan` whether a tracked template is required or a test-owned clean fixture/absence-policy guard applies; NEVER fall back to user's `misora_config.json`)
- `tests/test_v15_s08_release_gate_stress.py` (add S09–S11 stress/leak assertions if needed: e.g., virtualized card pool recycling memory plateau + async XUAT archiving + unified progress teardown)
- `__init__.py` — **CONDITIONAL ONLY:** bump `"1.4.10"` -> `"1.5.0"` **IF AND ONLY IF** every gate criterion in Part 4 is met AND the Project Lead explicitly authorizes promotion in `Proceed`.

Strictly READ-ONLY Audit Files (DO NOT MODIFY in S12):
- `misora.py`, `core/*.py`, `assets/*`, `requirements.txt`, `misora_config.json`, `backups/`.

==================================================
PART 2 — REQUIRED READ-ONLY DEEP AUDIT PILLARS (REPORT IN `/plan` & `PROJECT_STATE.md`)
==================================================
Every finding MUST cite exact `file:line`, symbol name, concrete mechanism, and AST/grep proof (`[CONFIRMED]` or `[NEEDS-VERIFY]`):

1. **Pillar A — Structural Bloat Map:** Exact line counts & byte sizes of `misora.py`, all `core/*.py`, and `assets/*.py`; Top 15 classes & Top 20 largest methods in `misora.py`; concrete low-risk decomposition roadmap for post-v1.5.0 maintenance (advisory only).
2. **Pillar B — Dead Code & Legacy Leftovers (AST/Grep Proven):**
   - Zero-caller functions/methods/classes/imports/constants across `misora.py`, `core/`, `assets/` (specifically auditing post-S09/S10/S11 remnants: `get_voice_badge_image`, `get_all_script_card_*`, `get_all_script_dotted_rule_image`, old Technique A `_all_script_block_ranges` / `_card_widgets` leftovers, `TranslatorAssistantDialog`, unused `assets/icons/*`, dead `self.*` attributes).
   - Report production caller count, `tests/` reference count, and safety rating (`SAFE-DELETE`, `DELETE-AFTER-TEST-UPDATE`, `KEEP`).
3. **Pillar C — Memory, Tk Resource & Concurrency Leak Audit:**
   - All caches/dicts/lists across open/switch/reload/close/`destroy()` (including Virtualized Card Pool, Quick Edit segment editors, unified progress tasks, XUAT archiving worker queues, `preview_frames` cache, `icon.py` cache, `undo_journal`, `sync_manager`).
   - Untracked `after()` timers, `PhotoImage` / PIL handles, `Toplevel` grabs/variables without `master=self`, `trace_add`/`bind_all` accumulation, dynamic `tk.Text` tag leaks, worker threads/executors, UnityPy envs, Win32 GDI font handles.
4. **Pillar D — Runtime Bugs & State Desync Audit (Post S09–S11):**
   - Cross-view sync (`Dialogue`, `Dialogue Preview`, `All Script`, `Quick Edit`, `Raw Commands`, `Left Drawer`, `MTL Drawer`, `Select Box`, `Translation Lock`, `Box 0`), silent `except Exception: pass` traps, Undo/Redo & dirty-flag consistency, and file/data safety across `core/*.py`.

==================================================
PART 3 — NON-FIXTURE TEST HYGIENE & STRESS VERIFICATION
==================================================
1. Resolve the 3 pre-existing non-fixture full-suite failures cleanly (without modifying user's local `misora_config.json` or weakening assertions):
   - `tests/test_v15_s01_stability_remediation.py::test_probe_8`: dynamic parity against root `__init__.__version__`.
   - `tests/test_phase3_performance_config.py::test_05`: isolated temp config fixture; zero fallback to machine-local `misora_config.json`.
   - `tests/test_s9c_workspace_safety.py::test_04`: verify repo contract for `misora_config.default.json` during `/plan` and test cleanly via repository-owned template OR test-owned temp fixture / explicit absence policy — NEVER reading user's `misora_config.json`.
2. Re-run the full S08–S11 stress and acceptance suites and record exact `tracemalloc` deltas, 150/300/1000-box Virtualized Card Pool timings, and 100% traceability audit across all canonical IDs (`S01`–`S11`, `U-01`–`U-20`, `RM-01`).

==================================================
PART 4 — HONEST RELEASE GATE DECISION MATRIX (`v1.4.10` HOLD vs `v1.5.0` PROMOTE)
==================================================
Promote `__init__.__version__` to `"1.5.0"` and retitle `CHANGELOG.md` ONLY IF ALL 4 conditions hold:
1. All non-fixture automated tests pass (`0` unexpected failures/errors); fixture-dependent items (`storydata_1001005.unity3d`) are either resolved with the real fixture OR explicitly waived in writing by the Project Lead.
2. Zero open P0/P1 source defects or confirmed memory leaks from the S12 Read-Only Audit.
3. Project Lead explicitly confirms completion of the Manual Windows QA Checklist (S01–S11) in `Proceed`.
4. No unauthorized files modified (`git status --short` strictly matches S12 Allowed Files).

If ANY condition is unmet (missing fixture without waiver, pending Manual Windows QA, or open audit P0/P1 finding):
- Keep `__init__.__version__ = "1.4.10"` (honest **Release Gate Hold**).
- Keep `CHANGELOG.md` under `## [Unreleased] (Target: v1.5.0)`.
- List every remaining blocker explicitly in `PROJECT_STATE.md` and the Walkthrough.

==================================================
PART 5 — VERIFICATION COMMANDS & DEFINITION OF DONE
==================================================
Run and report exact real observed output in the Walkthrough artifact:
1. `py -3.12 -m compileall -q __init__.py misora.py core assets tests`
2. `py -3.12 -m unittest tests.test_v15_s08_release_gate_stress tests.test_v15_s09_core_fixes_54d tests.test_v15_s10_all_script_quick_edit tests.test_v15_s11_xuat_archiving_progress -v`
3. `py -3.12 -m unittest discover -s tests -v` (report exact total, pass, skip, failure, error breakdown with explicit fixture-BLOCKED vs non-fixture classification).
4. `git status --short` compared against pre-session snapshot.