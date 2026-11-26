# MISORA: STORY EDITOR — RECONCILED POST-S11 ROADMAP (v2) FOR GPT FINAL SIGN-OFF

From: Gemini (aligned with Project Lead decisions and GPT's 5 final technical corrections)
To: ChatGPT (Independent Technical Reviewer)
Repository Baseline: `ImaterialC/Misora-Editor` `main` @ `c1ec40c` (`__version__ = "1.4.10"`)
Execution Boundary: ROADMAP RECONCILIATION ONLY. Zero Antigravity prompts generated; zero source files modified; `v1.5.0` remains ON HOLD until all Track A sessions, Manual Windows QA, and S12 Release Gate pass Project Lead sign-off.

======================================================================
1. BASELINE HONESTY & PRIOR S11 STATUS
======================================================================
- `main` contains S09b (`v1.4.8`), S10 (`v1.4.9`), and S11 (`v1.4.10`, commit `c1ec40c`).
- S11 automated counts previously reported (440 discovered, 397 pass, 35 fixture-blocked skips, 6 pre-existing failures, 2 pre-existing fixture errors; 28/28 targeted S11+XUAT; 17/17 notification+S11) are recorded strictly as Antigravity/Gemini execution reports, NOT independently re-executed by GPT.
- Manual Windows QA remains OPEN / pending explicit Project Lead sign-off.

======================================================================
2. ALL 5 GPT FINAL CORRECTIONS INCORPORATED
======================================================================

### Correction 1 — `Q-22` (Quick Edit Unified Single-Box): Dedicated Bounded Session + Parity Test + S08/S10 Audit
- **Moved to its own dedicated bounded session (`S11c`, `v1.4.12`)**, completely separated from Import UX (`Q-06`–`Q-12`) due to AST/Undo contract impact.
- **Canonical Single-Box Mutation Contract:**
  * Replace multi-textbox segment splitting in `misora.py::_rebuild_quick_edit_widgets()` with ONE unified plain `tk.Text` box (mirroring the main Dialogue Editor's single-box UX, without ruler, red overflow markers, NGUI decorators, or preview styling; optional non-blocking `[N segs]` info badge).
  * Mandatory 8 safety invariants:
    1. Capture complete `old_snapshot = BoxSnapshot.from_box(box)` BEFORE editing (`seg_texts`, `raw_breaks`, `extra_args`, `speaker`, `voice_cue`, `kind`).
    2. While typing, mutate via canonical `self.current_doc.inject_box(idx, None, new_tx)` WITHOUT `seg_texts` (exact same distribution path as the main Dialogue Editor).
    3. Capture fresh `new_snapshot = BoxSnapshot.from_box(updated_box)` from the actually updated AST on commit/flush into ONE logical `BoxSnapshotReplaceDelta` Undo transaction.
    4. Undo (`replace_box()`) restores the EXACT original multi-segment split (`seg_texts`, `raw_breaks`, `extra_args`, `speaker`, `voice_cue`, `kind`).
    5. Redo restores the exact edited state.
    6. Binary round-trip (`to_binary()` -> `from_binary()`) passes verbatim on edited, undone, and redone states.
    7. Immutable JP source keys (`_original_jp_by_uid`, `sync_manager.jp_source_cache`) and `_locked_box_uids` remain intact across Edit/Undo/Redo.
    8. Preserves S09b Translation Lock Parity (Row 1): Quick Edit permits dialogue text typing on locked boxes identically to Manual Dialogue typing, while leaving all other lock guards and Speaker Pin orthogonality intact.
- **Mandatory Parity Test:** Edit two identical multi-segment `StoryDocument` instances with identical initial state and input — Document A via Manual Dialogue Editor, Document B via Quick Edit — and assert identical resulting AST (`records`, `boxes`, `seg_texts`, `raw_breaks`) and identical serialized binary output (`to_binary()`).
- **Mandatory Existing Test & Stress-Test Audit/Migration:**
  * Audit and migrate ALL Quick Edit widget references across BOTH:
    - `tests/test_v15_s10_all_script_quick_edit.py` (update from 4 split segment widgets to 1 unified Quick Edit box + full binary round-trip + original 4-segment Undo + Manual-vs-QuickEdit parity test), AND
    - `tests/test_v15_s08_release_gate_stress.py` (audit `_qe_seg_widgets[0]` and any other Quick Edit benchmark/stress reference; update cleanly or keep a clear single-element compatibility layer so S08 stress tests never break from widget refactoring).

### Correction 2 — `Q-23` (Dialogue Preview Without Red Overflow Blocks): Guard + S03 & S18 Test Migration
- **Scoped in `S11b` (`v1.4.11`).**
- **Root Cause & Hardened Guard:**
  * Remove `self._apply_overflow_highlights(txt_w)` from `misora.py::_render_dialogue_preview_frame()` (~line 7595).
  * Add a defensive guard inside the overflow highlight helper itself so `txt_dialogue_preview` can NEVER receive `line_overflow` / red overflow highlights from any indirect or future code path.
- **Preserved Invariants:**
  * `txt_dialogue_preview` retains `wrap="none"` (native game-style text bleed past the gold capsule), `54d × 3` pixel calibration, pink Actor nameplate, continuous gold border, pink `▼`, and read-only/non-save contract.
  * **Dialogue Editor (Preview OFF)** MUST continue receiving red overflow highlight markers exactly as before (explicitly asserted in tests).
- **Complete Affected Test List:**
  * `tests/test_v15_s03_all_script_preview_paste.py` — update the existing assertion expecting `>= 2` `line_overflow` ranges on `txt_dialogue_preview` to assert `0` red overflow ranges on `txt_dialogue_preview` while asserting red overflow markers remain active on Dialogue Editor (Preview OFF).
  * `tests/test_p3_s18_game_preview.py` (and any S09 preview red-tag check if present) — assert `0` red highlight block tags on `txt_dialogue_preview` while preserving `54d × 3`, `wrap="none"` bleed, pink nameplate, gold border, and pink `▼` assertions.

### Correction 3 — Explicit STOP Gates in `S11b` (`Q-02` Save Hang & `Q-18` Ruby Preview)
- **`Q-02` (Save Hang Profiling + `Ctrl+S` Migration):**
  * Sub-task 2a (Save Hang): Profile all 5 save stages during `/plan` (widget flush/model sync, project save, XUAT dictionary sync, bundle serialization & patch I/O, post-save UI refresh). **HARD STOP GATE:** If profiling reveals that fixing the hang requires a major asynchronous save architecture or bundle transaction overhaul, STOP and spin off the async save remediation into its own dedicated bounded session rather than forcing it into `S11b` without design review. Workers must NEVER touch Tkinter or mutate live `StoryDocument`.
  * Sub-task 2b (`Ctrl+S` Shortcut Contract): Remap `Ctrl+S` -> Save Project (`.misora`), verify a conflict-free shortcut for Save & Patch Bundle (candidate `Ctrl+Shift+S`), and update File menu, shortcut router, tooltips, `README.md`, docs, and regression tests (ensuring zero conflict with native text editing).
- **`Q-18` (Ruby Preview Bug — Original `u-5`):**
  * **HARD STOP GATE:** Inspect existing `<ruby>` preview rendering during `/plan`. If repairing it is a bounded bug fix within the existing preview path, complete it in `S11b`; if it requires building a new custom text-layout engine, STOP and split `Q-18` into its own bounded session so it does not block `Q-01`/`Q-02`/`Q-23`. Auto-Furigana (MeCab) remains strictly in Track B (`BIG-02`).

### Correction 4 — Rebalanced 5-Step Track A Roadmap (Separating `Q-22` from Import UX)
*(Note: If any `S11b` STOP gate spins off an additional bounded session, subsequent session version numbers will increment sequentially and `S12` will automatically target the actual final `__init__.__version__` installed on disk.)*

| Step | Session | Target Version | Bounded Scope |
|---|---|---|---|
| 1 | **`S11b`** | `v1.4.11` | **`Q-01`** (XUAT scanner: 5 official exclusions `*.font.txt`/`*.resizer.txt`/`*Postprocessors.txt`/`*Preprocessors.txt`/`*Substitutions.txt`, strict `Translation\<lang>\Text`, root/file dedup, 4 distinct metrics `files`/`entries_read`/`unique_keys`/`duplicate_keys`, 5 root entry points + negative tests for `Other/` & `RedirectedResources/`), **`Q-02`** (Save Hang profiling/fix with STOP gate + `Ctrl+S` Save Project & conflict-free Save & Patch Bundle shortcut + docs/README/tests), **`Q-04`** (inspect `1.1` `▶` origin without presuming removal; reproduce `1.2` selection/drag/scroll separately on multi-match >3-linebreak Name/Title/Subtitle; **`1.3` strictly `NOT TESTED`**), **`Q-18`** (Ruby Preview bug fix with STOP gate), **`Q-23`** (remove red overflow blocks on `txt_dialogue_preview` + helper guard + S03/S18 test updates + Editor Preview-OFF guard). |
| 2 | **`S11c`** | `v1.4.12` | **`Q-22` ONLY** (Quick Edit unified single-box UX via canonical `inject_box(idx, None, new_tx)`, 8 AST/Undo/Lock invariants, Manual-Dialogue-vs-Quick-Edit AST+binary parity test, full audit & migration of `test_v15_s10_all_script_quick_edit.py` and `test_v15_s08_release_gate_stress.py`). |
| 3 | **`S11d`** | `v1.4.13` | **`Q-06`** (MouseWheel propagation over all Import labels/child frames), **`Q-07`** (per-group tri-state none/some/all Select All for Metadata/Actor/Dialogue), **`Q-08`** (multi-line wrapped Synopsis Metadata Import — NOT 1-line `54d` — with Skip, duplicate handling, atomic `MetadataDelta` Undo/Redo), **`Q-09`** (remove leftover `"Import Complete - XUAT translation Archiving"` sub-header), **`Q-10`** (`Select All Box` button & checkbutton: dialogue boxes only, Box 0 excluded, Translation Lock unchanged), **`Q-11`** (MTL Globe button: safe copy active text to clipboard + open official provider website; no unverified deep-link prefill claims), **`Q-12`** (truncated `filename — Title (Subtitle)` in window title bar from already-parsed metadata, zero disk re-read). |
| 4 | **`S11e`** | `v1.4.14` | **`Q-03`** (per-widget-class word-wrap contract: fixed 54d fields, Quick Edit, Raw Commands, Box 0 Synopsis, MTL preview, logs/diagnostics, any other audited textbox), **`Q-05`** (non-blocking splash lifecycle with honest startup progress), **`Q-13`** (bold/larger `PriconneRe:TL` + `Cornelia` on Splash & About), **`Q-14`** (`Support the Creator`, full English copy, ~600px aspect-preserving Pillow GIF; no FFmpeg/OpenCV), **`Q-15`** (corrected icon map verified on disk for exact filenames/extensions/alpha/dimensions: Translate=`language-translation-icon.png`, All Script=`BoxConversationList.png`, New Box=`BoxD.png`, Copy=`BoxCopy.png`, Cut=`BoxCut.png`, Paste=`BoxPaste.png`, Replace Box=`BoxInsert.png`, Select All Box=`BoxSelectAll.png`, Parked=`BoxConversation.png`), **`Q-16`** (remove 3x duplicate `NGUI Glossary` + require Project Lead approval of complete old-to-new command/shortcut/regression inventory BEFORE restructuring Main Menu), **`Q-17`** (complete missing tooltips + preserve Project Lead's original "3-layer tooltip" meaning — NOT 3 font sizes — with written definition proposal approved before implementation). |
| 5 | **`S12`** | `v1.4.14` -> `v1.5.0` (Conditional) | Read-only deep bloat/dead-code/memory-leak audit, 3 pre-existing non-fixture hygiene fixes, full stress & discovery suite, baseline-relative Git verification, and honest Release Gate. |

### Correction 5 — Updated `S12` Release Gate Contract & `Q-04.1.3` Honesty Rule
- **Dynamic Final Version Parity:** `S12` HOLD baseline updates from `1.4.10` to **`1.4.14`** (or the exact final `__init__.__version__` after all Track A sessions, including any STOP-gate spin-off session); conditional promotion becomes **`1.4.14` -> `1.5.0`** (or `<final_pre_s12_version>` -> `1.5.0`).
- **Full Updated Scope & Traceability:** Covers `S01`–`S11e`, all canonical IDs (`U-01`..`U-20`, `Q-01`..`Q-18`, `Q-22`..`Q-23`), every migrated test file (`S03`, `S08`, `S10`, `S18`, etc.), updated Manual Windows QA checklist, and baseline-relative Git verification.
- **`Q-04.1.3` (`NOT TESTED`) Honesty Guard:** `Q-04.1.3` MUST remain explicitly marked **`NOT TESTED`** (NEVER auto-marked `PASS`). The S12 Release Gate CANNOT declare QA complete or promote to `1.5.0` until the Project Lead explicitly tests `1.3` or records an explicit written decision/waiver.
- **Strictly Read-Only Source Rule Retained:** Any new P0/P1 source bug or memory leak found during S12 audit becomes a Release Gate BLOCKER for a separate fix session — never silently patched inside S12.

======================================================================
3. TRACK B — POST-`v1.5.0` MAJOR FEATURES (UNCHANGED, SEPARATE DESIGN MEETINGS)
======================================================================
- **`BIG-01` (MTL Provider Expansion):** Deep reliability/API/ToS/Cloudflare/VN-JP->EN research (Bing/Microsoft treated as one family, iTranslate, bab.la, Yandex, Reverso, Linguee evaluated as bilingual dictionary/examples, Papago; LunaTranslator reference); zero broken placeholder engines.
- **`BIG-02` (Auto-Furigana / MeCab Plugin — Original `u-6`):** Optional toggle plugin after `Q-18` Ruby Preview works; full license audit (MeCab + dictionary data + LunaTranslator compatibility), dependency/RAM/startup/parsing benchmarks, zero collision with native story `<ruby>`.
- **`BIG-03` (Rikaikun-Style Japanese Hover Dictionary Plugin — Original `u-10`):** Optional plugin with offline index/license/deinflection/RAM/NGUI+Ruby/large-chapter performance design before any core changes.

======================================================================
4. AUTHORIZATION REQUEST
======================================================================
Please confirm final roadmap sign-off on `Gemini2GPT_PostS11_Reconciled_v2.md`.
Upon your sign-off (and Project Lead approval), Gemini will draft the bounded Antigravity prompt for `S11b` first (or the full `S11b`–`S12` prompt set) for independent prompt review before any `/plan` execution begins.