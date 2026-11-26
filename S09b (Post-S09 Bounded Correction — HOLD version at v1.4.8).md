/plan Implement S09b (Post-S09 Bounded Correction — HOLD version at v1.4.8): Fix U-02 Pin/Unpin Speaker Switching Flow, U-06 Full-List Speaker Autocomplete & Editing, U-19 Pink Actor Nameplate in Dialogue Preview, Granular Translation Lock Operation Matrix Audit, and 4 Post-S09 Test Contract Migrations.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @CHANGELOG.md @__init__.py @misora.py @assets/preview_frames.py @tests/test_v15_s09_core_fixes_54d.py @tests/test_p3_s18_game_preview.py @tests/test_v15_s03_all_script_preview_paste.py @tests/test_v15_s08_release_gate_stress.py

==================================================
PART 0 — EXECUTION BOUNDARY, PLANNING GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. Planning-First Gate: Inspect live files on disk first (verify every file path, every `is_box_locked` call site, and the exact causes of the 4 post-S09 test failures), capture pre-session `git rev-parse HEAD`, `git status --short`, and Python 3.12 version, then output a symbol-bound Implementation Plan artifact (including the live-verified granular Translation Lock Operation Matrix with exact `file:line` and test evidence per sub-operation) and STOP to wait for explicit Project Lead `Proceed` before editing ANY file.
2. Version Hold Rule: DO NOT bump `__init__.py` to `"1.4.9"` and DO NOT begin any S10 work (`All Script` Virtualized Card Pool / `Quick Edit`). `__init__.__version__` MUST remain `"1.4.8"`.
3. No Destructive Git Commands: NEVER run `git reset`, `git clean`, `git stash`, `git checkout`, `git restore`, `git commit`, or `git push`. Preserve all pre-existing modified/untracked files, local `misora_config.json`, and `backups/`.
4. No Test Weakening: Never skip, delete, or weaken assertions. Update the 4 affected pre-existing tests strictly to the verified S09/S09b contracts (`54d`, Preview geometry/pink nameplate, Paste selection model, dynamic version parity).
5. Honest Reporting: Separate fixture-blocked failures (`storydata_1001005.unity3d`: 3 fail + 2 error + 35 skips) from non-fixture pre-existing hygiene failures (3 fail deferred to S12) and confirm ZERO S09/S09b regressions.

==================================================
PART 1 — STRICT FILE OWNERSHIP BOUNDARIES (S09b)
==================================================
Allowed Files to Modify (ONLY after `Proceed`; verify exact paths on disk during `/plan`):
- `misora.py` (strictly scoped to U-02 Pin/unpin speaker switching, U-06 Speaker editing/autocomplete, U-19 Dialogue Preview pink nameplate call/color)
- `assets/preview_frames.py` (strictly scoped to U-19 pink Actor nameplate background & contrasting text while keeping gold nameplate border, cream/gold capsule, and pink `▼`)
- `CHANGELOG.md` (append bounded `S09b` post-S09 manual QA correction note under `v1.4.8`)
- `PROJECT_STATE.md` (update S09b results, granular Translation Lock Operation Matrix with code/test evidence, separated full-suite baseline, and updated manual Windows QA checklist)
- `tests/test_v15_s09_core_fixes_54d.py` (update U-02/U-06/U-19 probes, add explicit deterministic assertions, fix the 1 probe that errored pre-patch so all probes fail deterministically as assertion failures)
- `tests/test_p3_s18_game_preview.py` (migrate `test_01` and `test_03` to `54d` / updated Dialogue Preview geometry & pink nameplate without weakening assertions)
- `tests/test_v15_s03_all_script_preview_paste.py` (migrate `test_probe_4` to S09 `U-01` Paste selection model without weakening assertions)
- `tests/test_v15_s08_release_gate_stress.py` (fix `test_stress_5` version/source parity expectation for S09 without weakening version-unification guards)

Forbidden Files (DO NOT MODIFY in S09b):
- `__init__.py` (MUST stay `"1.4.8"`), `core/*.py`, `requirements.txt`, `misora_config.json`, `backups/`, and any S10/S11/S12 files outside the list above.

==================================================
PART 2 — EXACT TECHNICAL SPECIFICATIONS (S09b)
==================================================

### 1. `U-02` — Revised Pin Speaker & Actor Switching Workflow (`misora.py`)
Inspect live `_on_toggle_pin_speaker`, `_navigate_pinned_speaker`, `_commit_speaker_edit`, `entry_speaker`, and `_jump_to_speaker` (`▼`), then enforce this exact workflow:
1. Pinning Actor A via `📌` captures Actor A into `self._pinned_speaker_name` and enables same-speaker `Next`/`Prev` navigation (no wrap-around, keeping `"the first/last time speaking in this chapter"` boundary messages) plus `New Box` speaker prefill.
2. **Unpin-First Actor Switching Contract:**
   - Releasing `📌` clears `self._is_speaker_pinned = False` and `self._pinned_speaker_name = None`, leaving `entry_speaker` usable again.
   - If the user attempts to change the active box's speaker to Actor B (via `entry_speaker` edit or autocomplete selection) while `📌` is active: **automatically execute an explicit unpin-first release** (set `_is_speaker_pinned = False`, `_pinned_speaker_name = None`, update `📌` button visual to unpinned, emit clear status/toast such as `"Speaker Pin released — speaker changed to <Actor B>. Click 📌 to pin <Actor B>."`) and commit Actor B (subject to existing Translation Lock commit policy).
   - **Pin MUST remain OFF** after the actor change. NEVER silently preserve the old Actor A pin identity while displaying Actor B!
   - Clicking `📌` again captures Actor B as the new `_pinned_speaker_name`; subsequent `Next`/`Prev` navigate using Actor B only, and Actor A no longer influences navigation.
3. **Strict Control Distinction:**
   - `▼` (`Jump to Speaker Box` dropdown menu): **navigation-only** — jumps to an existing box of the selected speaker and MUST NEVER rename/mutate the active box's speaker.
   - `entry_speaker` + Autocomplete popup: selects/commits the speaker name for the active box.
4. **Zero Conflation with Translation Lock:** Pinning, unpinning, or switching actors MUST NEVER modify Translation Lock state, and Speaker Pin MUST NEVER be confused with Translation Lock.

### 2. `U-06` — Speaker Entry Editing & Full-List Autocomplete (`misora.py`)
Inspect why `entry_speaker` could not be edited as expected and why autocomplete showed only 1 actor, then enforce:
1. **Explicit Separation of Entry Usability vs. Commit Permission:**
   - **Entry Usability:** `entry_speaker` MUST remain usable/editable on dialogue boxes both normally and immediately after unpinning — NEVER stuck `readonly`/`disabled` due to Speaker Pin state.
   - **Commit Permission:** Making `entry_speaker` usable MUST NOT bypass or weaken any existing Translation Lock guard that specifically blocks committing a speaker rename on a locked box.
2. **All Document Actors on First Open:** Add an explicit typing-session flag (e.g., `self._speaker_ac_user_typed: bool = False`) reset to `False` whenever the popup opens on click/focus or the active box changes.
   - While `_speaker_ac_user_typed` is `False` (first open / before the user types): display **ALL unique Actor names in the current document** plus `(Narration — Clear Speaker)` — do NOT filter the initial popup list by the pre-existing `speaker_var.get()`.
   - Only apply prefix/substring filtering AFTER the user actually types/edits the query (`_speaker_ac_user_typed = True`).
   - Clearing the query (`""`) restores the complete Actor list plus `(Narration — Clear Speaker)`.
3. **Clean Commit & Lifecycle Preservation:**
   - Selecting a different Actor from the popup commits the speaker edit cleanly without a stale pinned value overwriting the new selection.
   - Preserve S09 withdrawn-first creation + multi-monitor `rcWork` clamping (zero `(0,0)` flash) + S05 FocusOut safety.

### 3. `U-19` (Part 2) — Dialogue Preview Pink Actor Nameplate (`assets/preview_frames.py`, `misora.py`)
Authoritative reference: `DialogueBox-comparation.png` (pink Actor nameplate above the gold dialogue capsule).
1. Replace ONLY the dark Actor nameplate background (`#3B2C4E`) with the intended **pink nameplate appearance** matching the reference / application pink theme (e.g., soft Priconne pink `#E8759F` / subtle pink gradient with crisp high-contrast `#FFFFFF` bold Actor text).
2. **Strictly Preserve:**
   - Gold nameplate border,
   - Cream/gold dialogue capsule frame (do NOT recolor the dialogue capsule),
   - Crisp unclipped lower-right pink `▼` arrow and continuous right gold border fixed in S09 (`U-19`),
   - Read-only & clean-room contract (`txt_dialogue_preview` stays `disabled` and excluded from save paths).

### 4. Granular Translation Lock Operation Matrix (Audit & Documentation — Mandatory S10 Prerequisite)
During `/plan`, inspect ALL existing `is_box_locked` / `_locked_boxes` call sites in `misora.py` and existing lock tests in `tests/`. Do NOT silently redefine Translation Lock as a universal read-only state!
Document the live-verified **Granular Translation Lock Operation Matrix** in BOTH the `/plan` Implementation Plan and `PROJECT_STATE.md`. **Do NOT merge sub-operations that may have distinct policies**; record actual behavior (`ALLOWED` / `BLOCKED` / `SKIPPED`) PLUS exact `file:line` symbol and test evidence for EACH row separately:
1. Manual Dialogue typing
2. Speaker rename commit (distinguished from Speaker Entry usability/focus)
3. Quick Edit (target S10 parity: MUST follow Row 1 Manual Dialogue typing lock policy unless Project Lead approves a separate universal read-only RFC)
4. Paste Box — Insert
5. Paste Box — Replace
6. MTL Apply (Dialogue card Apply & All Script Apply Selected / Apply All — note any difference)
7. XUAT Import
8. Auto Word Wrap
9. Batch — Search & Replace (current file & project replace-all)
10. Batch — Apply Script (Paste Script / CSIF)
11. Batch — Clear Skeleton & Cut Box
12. Select Box and navigation (`Next`/`Prev`, Jump-to-Speaker, Pin)

Verify in code and tests that Speaker Pin and Translation Lock are strictly orthogonal.

### 5. Resolve 4 Post-S09 Full-Suite Failures & Deterministic Failing-First Probe
Inspect and migrate each of the 4 failing tests to match the verified S09/S09b contracts without weakening assertions:
1. `tests/test_p3_s18_game_preview.py::test_01`
2. `tests/test_p3_s18_game_preview.py::test_03`
3. `tests/test_v15_s03_all_script_preview_paste.py::test_probe_4`
4. `tests/test_v15_s08_release_gate_stress.py::test_stress_5`
Also fix the 1 probe in `tests/test_v15_s09_core_fixes_54d.py` that previously raised an unhandled `ERROR` instead of a clean assertion `FAIL` before patch, so failing-first verification is 100% deterministic.

==================================================
PART 3 — REQUIRED AUTOMATED TESTS (`tests/test_v15_s09_core_fixes_54d.py`)
==================================================
Use strict test isolation (`misora.CONFIG_PATH` & `app.backup_folder` in `TemporaryDirectory`, `MisoraApp(restore_session=False, show_splash=False)`, mocked `messagebox`, `app.destroy()` in `finally:`).

Update/add deterministic probes covering ALL required scenarios:
1. **U-02 Pin/Unpin & Actor Switching Probe:**
   - Pin Actor A -> Unpin Actor A -> Change speaker to Actor B -> verify Pin stays OFF -> Re-pin Actor B -> verify `Next`/`Prev` navigate to Actor B only and old Actor A identity no longer influences navigation.
   - Attempt actor change while Pin is active -> verify explicit unpin-first release (Pin turns OFF, Actor B committed, old Actor A pin never lingers).
   - Verify `▼` Jump-to-Speaker menu is navigation-only and NEVER mutates the active box's speaker.
2. **U-06 Speaker Editing & Full-List Autocomplete Probe:**
   - First popup open with an existing speaker name in `entry_speaker` -> ALL unique document Actors + `(Narration — Clear Speaker)` are visible BEFORE typing.
   - Typing filters candidates; clearing query restores all candidates.
   - Selecting a different Actor commits the speaker edit cleanly; Entry remains editable after unpinning.
   - Verify Speaker Entry editability does NOT bypass existing Translation Lock speaker-rename rules, and Translation Lock state remains strictly independent from Pin state.
   - Retain S09 withdrawn-first `(0,0)` guard & S05 FocusOut safety.
3. **U-19 Pink Actor Nameplate Probe:**
   - Inspect rendered nameplate PIL Image pixels / configured pink color to assert pink nameplate fill (NOT `#3B2C4E`, red channel dominant over green/blue with high-contrast text), gold nameplate border intact, dialogue capsule NOT recolored pink, and S09 `▼` bounding-box non-overlap still passing.

==================================================
PART 4 — VERIFICATION COMMANDS & DEFINITION OF DONE
==================================================
Run and report exact real observed output in the Walkthrough artifact:
1. Pre-patch probe run: `py -3.12 -m unittest tests.test_v15_s09_core_fixes_54d -v` (confirm new/updated S09b probes fail cleanly as assertion FAILs, NOT unhandled ERRORs).
2. Post-patch compile check: `py -3.12 -m compileall -q __init__.py misora.py core assets tests`
3. Post-patch targeted suites:
   `py -3.12 -m unittest tests.test_v15_s09_core_fixes_54d tests.test_p3_s18_game_preview tests.test_v15_s03_all_script_preview_paste tests.test_v15_s08_release_gate_stress tests.test_p3_s17_pixel_rulers tests.test_v15_s02_fonts_ruler_metrics tests.test_v15_s05_speaker_console_about tests.test_v15_s06_tools_word_wrap -v`
4. Full discovery run: `py -3.12 -m unittest discover -s tests -v`
   - Report exact total / pass / skipped / failure / error counts, explicitly separated into:
     * **Fixture-Blocked (`storydata_1001005.unity3d`):** 3 failures + 2 errors + 35 skips
     * **Pre-Existing Non-Fixture Hygiene (S12):** 3 failures
     * **S09 / S09b Regressions:** MUST be `0`.
5. `git status --short` compared baseline-relatively against pre-session snapshot (confirm `__init__.py` untouched at `"1.4.8"` and only S09b Allowed Files modified).
6. Update `CHANGELOG.md`, `PROJECT_STATE.md` (with the 12-row Granular Translation Lock Matrix), and include the updated **Manual Windows QA Checklist**.