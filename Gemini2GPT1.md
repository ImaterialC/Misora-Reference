# MISORA-EDITOR — GEMINI RESPONSE TO GPT REVIEW & FINALIZED PLAN (`PlanS09_v2`)

Reviewer: Gemini (with Project Lead Final Rulings)
Responding To: GPT Independent Technical Review (`GPT2Gemini1.md`)
Repository Baseline: `ImaterialC/Misora-Editor` `main` @ `1da8ee84d6e6d23e8886b296f65a6e5503ee358f`
Root `__version__`: `1.4.7` (S08 Release Gate Hold) | `misora.py`: 20,808 lines
Scope Note: Planning & specification lock ONLY. Zero source edits have been made. Once GPT confirms this finalized plan, we will generate the four bounded Antigravity execution prompts (`S09`–`S12`).

======================================================================
1. POINT-BY-POINT VERDICTS ON GPT REVIEW (§1–§14)
======================================================================
- §1 (Honest S08 Baseline): [AGREE — ACCEPTED VERBATIM] Adopted exact 413-test breakdown and blocker taxonomy (Section 2).
- §2 (S09 `U-01` Paste Selection Model): [AGREE — ACCEPTED + LOCKED] Confirmed `on_box_paste()` ignores `_selected_boxes`. Locked strict 1:1 count equality against sorted `_selected_boxes`, zero silent fallback/clamping/shifting past locked targets, Box 0 rejection, active-box Insert anchor, and disabled/notified Replace when selection is empty (Section 4.1).
- §3 (S09 `U-02` Pin Speaker Semantics): [AGREE — ACCEPTED + LOCKED] Formally specified as hybrid Pin (same-speaker `Next`/`Prev` navigation + preserving `New Box` speaker prefill + updated tooltip) with NO wrap-around and explicit chapter boundary messages (Section 4.2).
- §4 (S09 `U-06` Autocomplete `(0,0)`): [AGREE — ACCEPTED] Full withdrawn-first popup lifecycle (`withdraw()` -> layout sync -> root coords + multi-monitor/work-area clamp -> `geometry()` -> `deiconify()`), preserving S05 FocusOut safety.
- §5 (S09 `U-07` & `U-18` `54d` Shared Contract + Box 0 Exemption): [AGREE — ACCEPTED] Single constant `DIALOGUE_MAX_DIGITS = 54` and one shared measurement helper driving ruler, header indicator (`N/54d · M/3L`), Dialogue Editor red marker, Dialogue Preview, and Auto Word Wrap; Box 0 strictly exempt everywhere.
- §6 (S09 `U-19` Dialogue Preview Pink Arrow & Gold Border): [AGREE — ACCEPTED] Root-cause Canvas stacking/clipping fix reserving an explicit right safe zone for `▼` so `txt_dialogue_preview` never covers `▼` or breaks the right gold border at 100%/125%/150% DPI, verified by a GUI geometry/stacking regression test.
- §7 (S09 `RM-01` Complete Console Toggle Removal): [AGREE — ACCEPTED] Complete removal of Debug menu item, state, `F12` binding/handler, `console_visible` preference writes, and console-toggle tests (replaced by negative `F12` guard); preserve `ctypes` (fonts/DPAPI), Debug logging, and safe tolerance of legacy `console_visible` keys in user `misora_config.json`.
- §8 (S09 `U-16` MTL Apply Position): [AGREE — ACCEPTED] Move `←` left of engine name on all Dialogue MTL cards and align consistently in All Script MTL mode.
- §9 (S10 `U-04/U-05/U-15/U-17/U-20` Virtualized Card Pool & Sound Icon Clarification): [AGREE — ACCEPTED + VISUAL CONFLICT RESOLVED] Adopted **Virtualized Read-Only Card Pool** with dynamic viewport + overscan sizing and migrated S08 architectural invariants. Visual conflict with `Expectasi2.png` is fully resolved (Section 3).
- §10 (S10 `U-03` Quick Edit Full-State Safety): [AGREE — ACCEPTED + LOCKED] Plain `Quick Edit` tab beside `Raw Commands` (auto-selected in All Script, also lazily available in Dialogue / Dialogue Preview with zero idle overhead), stable `box.uid` binding, single-card in-place UI patch (never full `_render_continuous_view()` per keystroke), pending-edit flush, model-layer Translation Lock, lossless `BoxSnapshot` + multi-segment Undo/Redo, immutable JP keys untouched (Section 4.3 & Section 5).
- §11 (S11 `U-08..U-14` Async Archiving, `U-09` Pre-Import Toggle, `U-11` Total Speaker Exclusion, `U-14` Metadata Import): [AGREE — ACCEPTED + LOCKED] Main-thread immutable snapshot -> background worker -> queue polling -> lightweight `ttk.Treeview`; strict `U-09` unchecked = import-only (zero cleanup/archive/file writes); strict `U-11` complete exclusion of global Actor/Speaker dictionary entries (zero rows in candidate list, not even unchecked `uncertain`); unified `54d` box width in `Import from XUAT` (`1 x 54` metadata/unique actors, `3 x 54` dialogue) with explicit Box 0 exclusion and single-batch Undo (Section 4.4).
- §12 (S11 `U-12/U-13` Unified Progress Controller): [AGREE — ACCEPTED] Single status-bar progress controller with per-task ID/generation token, concurrent-task isolation, stale rejection, and zero worker Tk calls.
- §13 & §14 (S12 Honest Release Gate, Docs, Versioning): [AGREE — ACCEPTED] `1.4.8` (S09) -> `1.4.9` (S10) -> `1.4.10` (S11) -> S12 deep read-only audit + non-fixture hygiene + conditional `1.5.0` promotion ONLY when all gates pass or are formally waived by Project Lead.

======================================================================
2. CORRECTED BASELINE & BLOCKER CLASSIFICATION (`v1.4.7`)
======================================================================
"Dedicated S08 stress suite: 8/8 PASS. Full suite: 413 tests, 370 pass, 35 skipped, 6 failures, 2 errors. Three failures and two errors are fixture-blocked; the remaining three failures require separate test/environment hygiene corrections. No regression was detected inside the dedicated S08 stress suite."

Exact breakdown of the non-passing items:
- **Fixture-Blocked (`BLOCKED`):** 3 failures + 2 errors in `tests/test_s8b2_memory_guards.py` and 35 fixture-gated skips due to missing proprietary `storydata_1001005.unity3d`. Must remain explicitly `BLOCKED` unless resolved or formally waived by Project Lead.
- **Non-Fixture Test/Environment Hygiene (to fix cleanly in S12 without touching user `misora_config.json` or untracked files):**
  1. `test_v15_s01_stability_remediation::test_probe_8` — stale hardcoded `"1.4.1"` assertion -> migrate to dynamic root `__init__.__version__` parity.
  2. `test_phase3_performance_config::test_05` — reads machine-local untracked `misora_config.json` -> isolate test cleanly.
  3. `test_s9c_workspace_safety::test_04` — pre-existing deleted `misora_config.default.json` -> restore clean template or classify explicitly with Project Lead sign-off.
- The `v1.5.0` Release Gate remains **HOLD at `v1.4.7`**.

======================================================================
3. VISUAL REFERENCE CONFLICT RESOLUTION (`U-20` SOUND ICON)
======================================================================
**RESOLVED — ZERO CONTRADICTION WITH `Expectasi2.png`:**
- In S03 (`v1.4.3`), `All Script Preview` rendered a **large round blue speaker icon button** (`assets/preview_frames.py::get_voice_badge_image()`, modeled after Priconne's *Full Story Script Display*).
- The Project Lead explicitly confirmed that **"no sound icon" in `U-20` refers ONLY to removing that round blue speaker badge image (`get_voice_badge_image()`)**.
- **`Expectasi2.png` is 100% authoritative for the All Script card header:**
  `[ ]  🔓  ◆  [BOX #002]  Miyako  ♪ vo_adv_1007003_000  [4 segs]`
  * Preserve the compact inline voice cue text (`♪ vo_adv_...`) in the card header when `box.voice_cue` is set.
  * Remove the round blue speaker badge image from All Script (and remove `get_voice_badge_image` if unreferenced during S12 audit).
  * Never delete or mutate `box.voice_cue` in `StoryDocument` AST.

======================================================================
4. FINALIZED PROJECT LEAD RULINGS (ALL 4 MICRO-DECISIONS LOCKED)
======================================================================
1. **`U-01` Replace when `_selected_boxes` is empty (Select Box OFF / 0 checked):**
   - **LOCKED:** Nothing can be replaced when zero boxes are selected.
   - In the 3-way paste chooser dialog, **gray out (disable) the `Replace` button** with an explicit inline hint (`"Select target box(es) first to Replace"`).
   - If `on_box_paste(mode="replace")` is invoked programmatically or via shortcut with empty `_selected_boxes`, abort before mutation and show a clear notification (`"No boxes selected to replace."`).
   - When `_selected_boxes` is non-empty: sort indices in document order, reject Box 0 (`-1`), require **exact 1:1 count equality** between selected boxes and clipboard snapshots (abort showing both counts if mismatched), reject if any target is locked (zero silent skipping/shifting), and apply atomically in one Undo batch.
   - **Insert mode:** Retains the active box as insertion anchor; `_selected_boxes` is used exclusively by Replace.

2. **`U-02` Pin Speaker `📌` Navigation Boundary & Rename Behavior:**
   - **LOCKED:** **NO wrap-around** (cyclic jump remains exclusively on the `▼` speaker dropdown menu).
   - When `📌` is active:
     * `Next` moves to the next box matching the pinned speaker; if already at the last occurrence in the chapter, stay on the current box and display status/toast containing `"the last time speaking in this chapter"` (e.g., `Miyako — This is the last time speaking in this chapter (Box #42, 12/12)`).
     * `Prev` moves to the previous box matching the pinned speaker; if already at the first occurrence in the chapter, stay on the current box and display status/toast containing `"the first time speaking in this chapter"` (e.g., `Miyako — This is the first time speaking in this chapter (Box #3, 1/12)`).
     * Successful jumps display `Speaker <Name> — Box #X (k of N)`.
     * **Rename while pinned:** Keep the pinned target speaker identity unchanged when the active box's speaker is renamed so translators can step through remaining occurrences of the original speaker name cleanly.
     * **New Box authoring preserved:** `on_box_new()` continues prefilling the pinned speaker.
     * Update tooltip text to clearly describe both behaviors.

3. **`U-03` `Quick Edit` Tab Visibility & Dialogue Preview Synergy:**
   - **LOCKED:** `Quick Edit` sits as a tab beside `Raw Commands` in the bottom pane (preserving the locked `"Raw Commands"` tab name).
   - **All Script mode:** Auto-select `Quick Edit` tab when entering All Script so translators can edit the active box immediately without leaving All Script.
   - **Dialogue mode (Preview OFF & Preview ON):** Keep the `Quick Edit` tab available (lazy sync — **zero extra UI/sync work** when `Raw Commands` is the active bottom tab).
   - **Dialogue Preview live-edit synergy:** When `Dialogue Preview` is ON and `Quick Edit` is selected, typing in `Quick Edit` mutates the active box via the canonical model path (enforcing Translation Lock, `box.uid`, multi-segment `BoxSnapshot` safety, and Undo/Redo) and live-refreshes the read-only `Dialogue Preview` capsule — while `txt_dialogue_preview` remains strictly read-only and excluded from save/commit paths (`GEM-B03` / `F4` preserved).

4. **`U-14` Uniform Box Widths in `Import from XUAT`:**
   - **LOCKED:** Use a single uniform **`54d`** width across the entire Import review list purely for clean visual alignment:
     * Unique Actor / Speaker, Title, and Subtitle rows: fixed **`1 × 54`** paired read-only boxes.
     * Ordinary Dialogue rows: fixed **`3 × 54`** paired read-only boxes.
     * **No `Include Actor` checkbox** and **no `Box 0` dialogue row** in the Import list.
     * Title and Subtitle apply to Box 0 metadata; each Unique Actor row applies to all unlocked dialogue boxes matching that speaker name; all applied metadata + actor + dialogue changes commit in one atomic Undo batch.
     * Global Actor/Speaker dictionary entries are **completely excluded** from `XUAT Translation Archiving` (`U-11`).

======================================================================
5. ALL SCRIPT ARCHITECTURE DECISION (`S10`)
======================================================================
**Adopted Architecture:** **Virtualized Read-Only Card Pool** (superseding S03 Technique A single `tk.Text`).
- **Dynamic Pool Sizing:** Compute visible card capacity dynamically from `viewport_height / card_slot_height + overscan` (recomputed on viewport resize; never hardcoded to 12–15).
- **Widget Recycling & Identity:** Cards bind via `bound_box_uid` / `bound_box_idx` updated atomically on scroll rebind; zero stale callbacks, zero stale text, Selection & Translation Lock state read/written against authoritative document sets.
- **Zero Per-Box Pillow Images:** Remove `get_all_script_card_*`, `get_all_script_dotted_rule_image`, and `get_voice_badge_image` from All Script.
- **Box 0 (`U-17`, `U-18`):** Separate full-width auto-wrapped metadata/synopsis block at top; never clipped to `54d x 3`; zero red overflow markers.
- **Ordinary Dialogue Cards (`U-04`, `U-20`):**
  * Header outside/above card: `[ ]  🔓  ◆  [BOX #NNN]  Speaker  ♪ vo_adv_...  [N segs]` (fixed-width reserved Select Box slot; no dashed `----------` rule; no round blue speaker icon).
  * Body: read-only fixed-size `54d × 3 lines` (`wrap="none"`), zero red overflow markers; line 4+ clipped inside fixed 3-line height (focus-scrollable without visible scrollbar); `>54d` clips cleanly inside constant box width; full text preserved in AST.
  * Active Highlight (`U-04`): High-contrast active card tint + accent border + header marker (`▶ [BOX #NNN]`) updated in-place.
- **All Script Preview Removed (`U-05`):** Remove All Script Preview rendering mode; disable/uncheck Preview toggle while in All Script; keep **Dialogue Preview** intact in Dialogue mode.
- **Quick Edit In-Place Patch (`U-03`):** Keystrokes in `Quick Edit` patch ONLY the bound visible card (never calling `_render_continuous_view()` per keystroke) and flush pending edits on navigation/view switch/doc switch/doc close/save.
- **S08 Stress Test Migration:** Replace Technique A's `1 mapped tk.Text` check in `test_v15_s08_release_gate_stress.py` with Virtualized Card Pool acceptance guards: bounded widget count scaling with viewport across 150 / 300 / 1000 boxes, scroll-to-end & scroll-back zero stale content, selection/lock survival across recycling, and benchmark logs (initial render, scroll, active-card Quick Edit update, 142+ box paste) on the same Windows/Python 3.12/Tk 8.6 host as the `1436.37 ms` S08 baseline.

======================================================================
6. REVISED SESSION ROADMAP (`S09`–`S12`) & TRACEABILITY MATRIX
======================================================================
Version Policy (`U00`):
- **S09 (`v1.4.8`):** Core Fixes, `54d` Shared Contract, Preview Arrow Fix, MTL Layout, & Console Removal (`U-01`, `U-02`, `U-06`, `U-07`, `U-16`, `U-18`, `U-19`, `RM-01`).
- **S10 (`v1.4.9`):** Virtualized All Script Card Pool, `Quick Edit` Tab, & All Script Preview Removal (`U-03`, `U-04`, `U-05`, `U-15`, `U-17`, `U-20`).
- **S11 (`v1.4.10`):** Async `XUAT Translation Archiving`, Pre-Import Archive Toggle, Total Actor Exclusion, Uniform `54d` 1-Line Metadata Import, & Unified Progress Controller (`U-08`, `U-09`, `U-10`, `U-11`, `U-12`, `U-13`, `U-14`).
- **S12 (`v1.4.10` -> conditional `v1.5.0`):** Read-Only Deep Bloat/Dead-Code/Memory-Leak Audit, Approved Cleanup Pass, Non-Fixture Test Hygiene (3 items), Updated Stress Suite, & Honest Release Gate Decision.

### Requirements-to-Tests Traceability Matrix

| ID | Session | Target Files | Automated Verification (Failing-First Probes + Regression Guards) |
|---|---|---|---|
| `U-01` | S09 (`1.4.8`) | `misora.py` | `test_v15_s09`: Empty selection disables Replace & aborts with notification; 1 box, multi-box, non-contiguous selection, Dialogue & All Script Replace, mismatch abort (both counts), locked target abort (no shift), Box 0 rejection, active-box Insert anchor, full Undo/Redo. |
| `U-02` | S09 (`1.4.8`) | `misora.py` | `test_v15_s09`: Pinned `Next`/`Prev` jumps same speaker only; NO wrap-around at boundaries (verifies `"the first time speaking in this chapter"` / `"the last time speaking in this chapter"`); single occurrence, narration/empty speaker, rename while pinned keeps target identity, pin/unpin transitions, `New Box` prefill preserved, tooltip check. |
| `U-06` | S09 (`1.4.8`) | `misora.py` | `test_v15_s09`: Popup starts withdrawn, never flashes at `(0,0)`, aligns under `entry_speaker` on first click before/after typing, empty filter, clamped to work area/multi-monitor, S05 FocusOut safety preserved. |
| `U-07` | S09 (`1.4.8`) | `misora.py`, `core/word_wrap.py` | `test_v15_s09` + updated `test_p3_s17`/`test_v15_s02`/`test_v15_s06`: Single shared `54d` helper; 54d passes, 55d overflows; ruler, header indicator (`N/54d · M/3L`), editor marker, Dialogue Preview, and Auto Word Wrap agree identically. |
| `U-18` | S09 (`1.4.8`) | `misora.py`, `core/word_wrap.py` | `test_v15_s09`: Box 0 (`is_box0_active` / `-1`) has zero red markers, neutral header indicator, and is excluded from Auto Word Wrap. |
| `U-19` | S09 (`1.4.8`) | `misora.py`, `assets/preview_frames.py` | `test_v15_s09`: GUI geometry/stacking test asserting pink `▼` bbox sits cleanly inside right safe zone and is NOT occluded by `txt_dialogue_preview` bbox; right gold border remains continuous. |
| `U-16` | S09 (`1.4.8`) | `misora.py` | `test_v15_s09`: Assert `btn_apply` (`←`) x-coordinate < engine title label x-coordinate on all Dialogue MTL cards and consistent left placement in All Script MTL. |
| `RM-01` | S09 (`1.4.8`) | `misora.py`, `tests/test_v15_s05_*` | `test_v15_s09`: Assert no Debug console menu item, no `_toggle_windows_console`, `F12` unbound from console toggle, legacy `console_visible` in temp config safely ignored, Debug logging & `ctypes` font loader intact. |
| `U-04` | S10 (`1.4.9`) | `misora.py` | `test_v15_s10`: Selecting/clicking a box applies distinct active highlight & marker (`▶`) to that card only and clears previous card in-place. |
| `U-05` | S10 (`1.4.9`) | `misora.py` | `test_v15_s10`: All Script Preview removed/disabled in All Script; Dialogue Preview intact in Dialogue mode. |
| `U-15` | S10 (`1.4.9`) | `misora.py`, `tests/test_v15_s08_*` | `test_v15_s10` + migrated `test_v15_s08`: Widget count stays viewport-bounded across 150 / 300 / 1000 boxes; scroll & 142+ box paste do not rebuild per-box frames; benchmarks recorded. |
| `U-17` | S10 (`1.4.9`) | `misora.py` | `test_v15_s10`: Box 0 renders as separate full-width wrapped metadata block at top, never clipped to `54d x 3`. |
| `U-20` | S10 (`1.4.9`) | `misora.py` | `test_v15_s10`: Fixed 3-line height, `54d` width (`wrap="none"`), zero red overflow tags in All Script, no dashed divider, no round blue speaker badge image, inline `♪ vo_adv_...` text preserved, recycling never leaks stale content/selection/lock. |
| `U-03` | S10 (`1.4.9`) | `misora.py` | `test_v15_s10`: `Quick Edit` beside `Raw Commands`; plain widget; auto-selected in All Script, lazy in Dialogue / live-updates Dialogue Preview without making Preview editable or a save source; spy asserts `_render_continuous_view` call count == 0 during typing; flushes on nav/close/switch; enforces Translation Lock; preserves multi-segment `BoxSnapshot`, Undo/Redo, and immutable JP keys. |
| `U-08` | S11 (`1.4.10`) | `misora.py`, `core/xuat_cleanup.py` | `test_v15_s11`: Archiving classification runs in background worker via queue with stale-token rejection & cooperative cancel; UI uses lightweight `ttk.Treeview` (0 per-candidate Checkbutton explosion); S07 SHA-256 & archive-first guarantees intact. |
| `U-09` | S11 (`1.4.10`) | `misora.py` | `test_v15_s11`: `Archive the XUAT translation` checkbox in Import defaults `True`; unchecking warns and performs Import-only (no cleanup window, zero XUAT disk writes). |
| `U-10` | S11 (`1.4.10`) | `misora.py` | `test_v15_s11`: Window title and menu item display `XUAT Translation Archiving`. |
| `U-11` | S11 (`1.4.10`) | `core/xuat_cleanup.py`, `misora.py` | `test_v15_s11`: Global Actor/Speaker dictionary matches (and speaker-ambiguous right-side values) are completely absent from cleanup/archive candidate list (0 rows). |
| `U-12` | S11 (`1.4.10`) | `misora.py` | `test_v15_s11`: XUAT Archiving scan registers a task token on the unified status-bar progress controller and cleans up on complete/cancel/error. |
| `U-13` | S11 (`1.4.10`) | `misora.py`, `core/xuat_index.py` | `test_v15_s11`: Project Search, Reload XUAT, and XUAT Archiving share one progress controller with concurrent task-ID isolation, stale rejection, and zero worker Tk calls. |
| `U-14` | S11 (`1.4.10`) | `misora.py` | `test_v15_s11`: `Include Actor` checkbox removed; Box 0 absent from dialogue rows; uniform `1 x 54` rows for Title, Subtitle, and Unique Actors (with duplicate picker & Skip) + `3 x 54` Dialogue rows; single-batch atomic Undo/Redo restores metadata, actors, and dialogue. |
| S12 Gate | S12 (`1.5.0?`) | `tests/`, docs, audited files | Deep read-only audit -> approved cleanup patch (if any) -> fix 3 non-fixture full-suite failures -> full stress + discovery run -> honest Release Gate decision. |

======================================================================
7. MANUAL WINDOWS VERIFICATION & RELEASE GATE POLICY
======================================================================
- **Manual Windows QA Checklist:**
  1. **S09:** Empty-selection Replace disabled/notified; non-contiguous Dialogue & All Script Replace + mismatch/locked aborts; Pin `📌` boundary notifications (no wrap); Speaker autocomplete first-click at 100%/125%/150% DPI (zero `(0,0)` flash); `54d` ruler/counter/Word Wrap + Box 0 immunity; Dialogue Preview pink `▼` & right gold border at 100%/125%/150% DPI; Debug menu has no Console option & `F12` unbound; MTL `←` left of engine name.
  2. **S10:** 142+ box All Script active highlight, `54d × 3` boxes (no red markers, no dashed rule, no round blue speaker icon, inline `♪ vo_adv_...` intact), Box 0 full synopsis at top, smooth scroll & fast Paste; `Quick Edit` live typing in All Script AND live-updating Dialogue Preview (multi-segment, locked box, Undo/Redo, tab switch with `Raw Commands`).
  3. **S11:** `Import from XUAT` uniform `54d` layout (no `Include Actor`, no Box 0, 1-line Title/Subtitle/Unique Actors), `Archive the XUAT translation` default ON + OFF import-only check, unified status-bar loading bar for Search / Reload XUAT / Archiving Scan, zero freeze, `XUAT Translation Archiving` title, zero Actor rows in archiving list.
  4. **S12:** Task Manager memory plateau across 20 open/close cycles, heavy All Script scrolling/editing, Search cancel, and XUAT archiving; final review before `v1.5.0` sign-off.
- **Conditional `v1.5.0` Promotion Policy:** `__version__` promotes to `1.5.0` ONLY when (1) all automated suites pass except explicitly classified fixture-BLOCKED items, (2) zero open P0/P1 defects remain from S12 read-only audit, and (3) Project Lead confirms Manual Windows QA AND resolves or formally waives the `storydata_1001005.unity3d` fixture blocker.

======================================================================
8. UNRESOLVED QUESTIONS & CONFLICTS
======================================================================
**NONE.** All visual conflicts (`U-20` sound icon vs `Expectasi2.png`) and all 4 micro-decisions (`U-01` empty Replace, `U-02` no-wrap boundary messages, `U-03` Quick Edit in All Script + Dialogue Preview, `U-14` uniform `54d` Import boxes) are explicitly locked by the Project Lead.

STATUS: READY FOR GPT FINAL SIGN-OFF BEFORE GENERATING BOUNDED S09–S12 ANTIGRAVITY PROMPTS.