# MISORA: STORY EDITOR — POST-S11 STATUS BRIDGE & TRIAGE PROPOSAL FOR GPT REVIEW

From: Gemini (on behalf of Project Lead / Cornelia)
To: ChatGPT (Independent Technical Reviewer)
Purpose: Catch-up summary since GPT's last review (S09b/S10 prompt check) + triage of newly reported manual Windows QA bugs, UX polish items, and post-v1.5.0 major feature proposals.
Execution Boundary: PLANNING & TRIAGE ONLY. Release `v1.5.0` remains ON HOLD at `v1.4.10`. Zero Antigravity prompts generated and zero source files edited until Project Lead + GPT agree on scope split.

======================================================================
1. CATCH-UP SUMMARY (WHAT COMPLETED SINCE GPT'S LAST MESSAGE)
======================================================================
1. **S09b (`v1.4.8` — Completed & Committed):**
   - Fixed `U-02` (unpin-first actor switching; `▼` Jump menu strictly navigation-only), `U-06` (full actor list on first popup open, Windows post-autocomplete caret/focus recovery micro-fix), `U-19` (pink Actor nameplate with WCAG white contrast + continuous gold border + unclipped pink `▼`), and migrated the 4 post-S09 test failures.
   - Produced live-verified 12-row Granular Translation Lock Operation Matrix in `PROJECT_STATE.md`: **Row 1 (Manual Dialogue typing) = `ALLOWED`** (widget stays `normal`, no `is_box_locked` block on typing), while speaker rename, Paste Replace, Cut Box, MTL Apply, Auto Word Wrap, Clear Skeleton, and XUAT Import enforce their specific lock guards.
2. **S10 (`v1.4.9` — Completed & Committed, `HEAD e92839a`):**
   - Replaced Technique A single `tk.Text` with **Virtualized Read-Only Card Pool** (viewport-dynamic pool, pixel-exact Nunito Bold `54d × 3` cards, Box 0 unclipped metadata block, active highlight, non-conflicting outer vs `Shift+Wheel`/keyboard internal scrolling, All Script Preview removed while Dialogue Preview preserved, round blue speaker badge removed while inline `♪ vo_adv_...` preserved).
   - Implemented `raw_breaks`-safe segment-aware **`Quick Edit`** tab beside `"Raw Commands"` following S09b Lock Parity (Row 1) with single logical `BoxSnapshotReplaceDelta` Undo/Redo and view-aware live sync.
3. **S11 (`v1.4.10` — Completed, awaiting final manual QA sign-off before local commit):**
   - Implemented pre-pass Actor/Speaker protection (`core/xuat_cleanup.py`), cancellable iterative `os.walk()` XUAT indexing with `\\?\` prefix stripping (`core/xuat_index.py`), `ImportFromXUATDialog` 3-section `54d` layout (Metadata Title/Subtitle, Unique Actors, Dialogue; no `Include Actor`, no Box 0 dialogue row; `Archive the XUAT translation` checkbox default ON; Document Identity Guard; `MetadataDelta`; segment-preserving speaker renames; atomic rollback), async `XUAT Translation Archiving` with 80-row batched `ttk.Treeview`, and unified `_ProgressTaskManager` (O(1) coalesced progress map + non-droppable lifecycle queue) shared across Search, Reload XUAT, and Archiving Scan.
   - **Verified S11 Test Baseline (`v1.4.10`):**
     * `compileall`: PASS (exit 0).
     * Targeted S11 + XUAT suites: 28/28 PASS; notification + S11 verification: 17/17 PASS.
     * Full discovery: **440 tests across 56 modules — 397 pass, 35 fixture-blocked skips (`storydata_1001005.unity3d`), 6 pre-existing failures (3 fixture-blocked + 3 S12 hygiene), 2 pre-existing fixture errors; 0 S11 regressions.**

======================================================================
2. PROJECT LEAD'S NEW MANUAL QA FINDINGS & FEATURE REQUESTS (TRIAGED)
======================================================================
Note: To prevent ID collision with completed S09–S11 IDs (`U-01`..`U-20`), all new items are assigned canonical IDs `Q-01`..`Q-17` (pre-v1.5.0 track) and `BIG-01`..`BIG-03` (post-v1.5.0 track), with the Project Lead's original note numbers preserved in parentheses.

### TRACK A — PRE-`v1.5.0` BOUNDED FIX & POLISH SESSIONS (BEFORE `S12` RELEASE GATE)

#### Proposed Session `S11b` (`v1.4.11`) — Critical P0/P1 Bugs & Core Usability
- **`Q-01` (User `u-20`, P0 — XUAT Scanner Over-Scanning 650k Entries):**
  * Observed: XUAT search/index reports ~650,000 entries even though the actual XUAT dictionary has <300,000 entries.
  * Confirmed real PriconneRe-TL XUAT directory contract supplied by Project Lead:
    - Game root: `...\PriconneRe-TL`
    - Framework: `...\src\BepInEx`
    - XUAT root: `...\src\BepInEx\Translation`
    - **ONLY valid translation text folder:** `...\Translation\<lang>\Text` (e.g., `en\Text`).
    - **MUST EXCLUDE folders:** `...\Translation\<lang>\Other` (non-XUAT files with similar syntax but different purpose) and `...\Translation\<lang>\RedirectedResources` (raw `.unity3d` swap files).
    - **MUST EXCLUDE XUAT config/rule files inside `Text\`:** `*.font.txt`, `*.resizer.txt`, `*Postprocessors.txt`, `*Preprocessors.txt`, `*Substitutions.txt`.
  * Also audit `core/xuat_index.py` for duplicate/overlapping root traversal that could double-count entries.
- **`Q-02` (User `U-21`, P0 — Save Hang + `Ctrl+S` Shortcut Semantics):**
  * Diagnose and fix UI hang occurring on Save (inspect `on_save()` main-thread XUAT dictionary update / 650k-entry scan coupling / bundle patch I/O).
  * Remap **`Ctrl+S`** to **Save Project (`.misora`)** instead of Save & Patch Bundle; assign a dedicated non-conflicting shortcut (proposed: **`Ctrl+Shift+S`**) to **Save & Patch Bundle**.
- **`Q-03` (User `u-4b`, P1 — Global Textbox Word-Wrap Audit):**
  * Project Lead reports textboxes are unexpectedly word-wrapping across the app. Audit every `tk.Text` widget and enforce a strict contract: `wrap="none"` for all `54d`-calibrated dialogue/card/import fields; `wrap="word"` ONLY where wrapping is genuinely required (Box 0 Synopsis, MTL preview output, logs/diagnostics).
- **`Q-04` (User `1.1` & `1.2`, P1 — S10/S11 Manual Test Findings):**
  * `1.1`: Inspect and fix/remove a non-functional `▶` icon appearing above textboxes exceeding 54 characters.
  * `1.2`: Verify multi-match switching and >3-linebreak internal scrolling behavior on Metadata/Actor/Dialogue boxes.
- **`Q-05` (User `u-1`, P1 — Splash Screen Startup Lifecycle):**
  * Keep the Splash Screen visible (with startup progress feedback) until full UI construction AND deferred/previous session restoration complete, eliminating the perceived startup freeze/hang gap.

#### Proposed Session `S11c` (`v1.4.12`) — Import/Archiving UX & Editor Productivity
- **`Q-06` (User `U-22`, P1):** Propagate `<MouseWheel>` across all static info labels and child frames inside `ImportFromXUATDialog` (`Story Speaker`, `Story Metadata`, `Actor`, `No XUAT Match`, `Skip`, `XUAT Actor Match`, etc.).
- **`Q-07` (User `U-23`, P2):** Add per-group `Select All` (or toggle-all) checkbox headers above Metadata, Unique Actors, and Dialogue sections in `ImportFromXUATDialog`.
- **`Q-08` (User `U-24`, P1 — Explicit Policy Update from S11):** Add **Synopsis (`summary`)** row to `ImportFromXUATDialog`'s Metadata section (alongside Title and Subtitle) with duplicate switcher, `Skip` checkbox, `MetadataDelta` atomic Undo/Redo, and non-speaker archiving eligibility if imported.
- **`Q-09` (User `U-25`, P2):** Fix leftover sub-header string `"Import Complete - XUAT translation Archiving"` inside `XuatCleanupDialog` to `"XUAT Translation Archiving"`.
- **`Q-10` (User `u-19`, P2):** Add `Select All Box` button and checkbutton (selecting all dialogue boxes safely while excluding Box 0 `-1`).
- **`Q-11` (User `u-3`, P2):** Add a Globe (`🌐`) button on each MTL engine card that opens that engine's official website in the system browser with the active box text pre-filled via URL query template (lightweight, zero scraping).
- **`Q-12` (User `u-16`, P2):** Append safely truncated `Title (Subtitle)` to the main window title bar (`Misora: Story Editor - 1001012.unity3d* — Title (Subtitle)`), refreshed on open/tab-switch/Box 0 edit/Import. (Verified near-zero RAM/CPU overhead since `StoryDocument` is already parsed in memory; keeps `"Dialogue"` header label untouched.)

#### Proposed Session `S11d` (`v1.4.13`) — Branding, Icons, Support Dialog, Main Menu Cleanup & Tooltips
- **`Q-13` (User `u-11`, P2):** Display main project **`PriconneRe:TL`** (larger, bold) and creator **`Cornelia`** on both Splash Screen and About dialog.
- **`Q-14` (User `u-12`, `u-13`, `U-14`, P2):** Rename Support dialog to **`Support the Creator`**, translate all remaining Indonesian copy to English, and enlarge `Service.gif` display width (keeping Pillow GIF — NOT video, to avoid heavy FFmpeg/OpenCV dependencies and decoder leaks).
- **`Q-15` (User `u-2`, `u-17`, `u-18`, P2):** Refresh & DPI-resize icons from `assets/icons/`:
  * Translate -> `language-translation-icon.png`
  * All Script -> `BoxConversationList.png`
  * New Box -> `BoxInsert.png` (preferred over `BoxD.png`), Copy -> `BoxCopy.png`, Cut -> `BoxCut.png`, Paste -> `BoxPaste.png`, Select All Box -> `BoxSelectAll.png` (`BoxConversation.png` parked).
- **`Q-16` (User `u-15`, P2):** Consolidate cluttered 12-item Main Menu into ~8 clean menus (`File | Edit | View | Search | Translate | Tools | Debug | Help`) and eliminate the 3× duplicate `NGUI Glossary` entries.
- **`Q-17` (User `u-8`, `u-9`, P2):** Audit and complete missing tooltips on all buttons, toggles, and radiobuttons, and verify consistent 3-level/3-size tooltip behavior.

#### Final Pre-Release Gate — `S12` (`v1.4.13` -> Conditional `v1.5.0`)
- Unchanged from GPT-approved S12 scope: Read-only deep bloat/dead-code/memory-leak audit, 3 pre-existing non-fixture test hygiene fixes (`test_v15_s01::test_probe_8`, `test_phase3_performance_config::test_05`, `test_s9c_workspace_safety::test_04`), baseline-relative Git verification, full stress run, and honest conditional `v1.5.0` promotion.

### TRACK B — DEFERRED POST-`v1.5.0` MAJOR FEATURES (SEPARATE DESIGN MEETINGS, `v1.6.0+`)
- **`BIG-01` (User `u-4a`):** Deep research & expansion of free MTL providers (Bing/Microsoft, iTranslate, bab.la, Yandex, Reverso, Linguee, Papago; reference architecture `HIllya51/LunaTranslator/translator`) — requires live endpoint/rate-limit/Cloudflare reliability research; drop anything unreliable.
- **`BIG-02` (User `u-5` + `u-6`):** Proper `<ruby>` tag visual rendering in Dialogue Preview (`u-5`, prerequisite) followed by optional Furigana toggle plugin using MIT MeCab / `LunaTranslator/myutils/mecab.py` (`u-6`) without colliding with native story ruby tags or bloating core dependencies.
- **`BIG-03` (User `u-10`):** Optional interactive Japanese hover dictionary plugin (Rikaikun-style JMdict/deinflection) — heavy data/indexing scope requiring standalone plugin design.

======================================================================
3. QUESTIONS FOR GPT TECHNICAL REVIEW
======================================================================
1. Do you approve the **Track A (`S11b` -> `S11c` -> `S11d` -> `S12`) vs Track B (`v1.6.0+`)** split, and should any item move between Track A and Track B (specifically checking `Q-08` Synopsis import & `Q-16` Menu restructuring)?
2. For **`Q-01` (`u-20` XUAT Scanner)**, what exact path-scoping & exclusion invariants should we lock in `core/xuat_index.py` (including handling users who point XUAT root to `Translation\`, `Translation\en\`, or directly to `Translation\en\Text\`)?
3. For **`Q-02` (`U-21` `Ctrl+S` Remap & Save Hang)**, do you approve `Ctrl+S` = Save Project (`.misora`) and `Ctrl+Shift+S` = Save & Patch Bundle, and what existing shortcut/workflow tests or `AGENTS.md` invariants must be updated explicitly?
4. For **`Q-03` (`u-4b` Word-Wrap Audit)**, confirm the exact `wrap="none"` vs `wrap="word"` matrix across Misora's widgets so we do not accidentally break `Quick Edit`, `Raw Commands`, or `Box 0` Synopsis.
5. Any technical caveats before we lock `S11b`–`S11d` specifications and draft their bounded Antigravity prompts?