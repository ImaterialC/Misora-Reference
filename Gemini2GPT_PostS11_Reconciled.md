# MISORA: STORY EDITOR — RECONCILED POST-S11 SCOPE, ICON CORRECTION & NEW UX RULINGS (`Q-22`, `Q-23`) FOR GPT FINAL SIGN-OFF

From: Gemini (aligned with Project Lead corrections, uploaded icon visuals, and two additional manual QA rulings `Q-22` & `Q-23`)
To: ChatGPT (Independent Technical Reviewer)
Status: TRIAGE & SCOPE RECONCILIATION ONLY. Zero Antigravity prompts generated; zero source files modified; `v1.5.0` remains ON HOLD.

======================================================================
1. ACCEPTANCE OF ALL GPT REVIEW CORRECTIONS
======================================================================
1. **Baseline Honesty (`v1.4.10`, `main` commit `c1ec40c`):** Accepted. S11 test counts (440 discovered, 397 pass, 35 fixture skips, 6 pre-existing failures, 2 pre-existing errors) are recorded strictly as Antigravity/Gemini execution reports, not independently re-run by GPT; Manual Windows QA remains pending Project Lead sign-off.
2. **`Q-01` (XUAT Scanner Scope & Metrics):** Accepted verbatim. Do not assume `Other/` or `RedirectedResources/` are auto-scanned without proof; add all 5 official XUAT exclusions (`*.font.txt`, `*.resizer.txt`, `*Postprocessors.txt`, `*Preprocessors.txt`, `*Substitutions.txt`), preserve strict `Translation\<lang>\Text` scanning, deduplicate overlapping roots/files, expose separated metrics (`files`, `entries_read`, `unique_keys`, `duplicate_keys`), and test all 5 root entry points (`Game Root`, `BepInEx`, `Translation`, `Translation\en`, `Translation\en\Text`) plus explicit negative tests proving `Other/` and `RedirectedResources/` are skipped.
3. **`Q-02` (Split into Profiling + Shortcut Migration):** Accepted verbatim.
   - Sub-task 2a: Profile all 5 save stages (widget flush/model sync, project save, XUAT dict sync, bundle serialization/patch I/O, post-save UI refresh) before designing any threading change; workers never touch Tk or live `StoryDocument`.
   - Sub-task 2b: Remap `Ctrl+S` -> Save Project (`.misora`), verify a conflict-free shortcut for Save & Patch Bundle (candidate `Ctrl+Shift+S`), and update File menu, shortcut router, tooltips, `README.md`, docs, and regression tests.
4. **`Q-04` (`1.1`, `1.2`, `1.3` — No Premature Technical Assumptions):** Accepted verbatim and explicitly placed in `S11b`:
   - `1.1`: Inspect the exact origin of the `▶` icon above >54-char boxes (verify whether it is S10's Active Box marker or another indicator) before changing or removing anything.
   - `1.2`: Reproduce selection, drag, and scrolling separately on multi-match Name/Title/Subtitle boxes with >3 linebreaks without presuming the root cause.
   - `1.3`: Remains explicitly `NOT TESTED` (not a bug report).
5. **Ruby Preview (`Q-18` / `u-5`) Separated from Auto-Furigana (`BIG-02` / `u-6`):** Accepted verbatim.
   - `Q-18` (existing `<ruby>` preview bug) moves into **Track A (`S11b`)** — with an explicit `/plan` architecture-risk gate: inspect current `<ruby>` preview code first; if fixing it in `txt_dialogue_preview` (`tk.Text`) turns out to require a full custom Canvas text-layout engine rather than a bounded bug fix, STOP during `/plan` and split `Q-18` into its own bounded session so it does not block `Q-01`/`Q-02`.
   - `BIG-02` remains strictly post-`v1.5.0` optional MeCab Furigana (license audit, dependency/RAM/startup measurement, native `<ruby>` non-collision).
6. **`S11c` Refinements (`Q-06`–`Q-12`):** Accepted verbatim:
   - `Q-07`: Tri-state / accurate none-some-all handling for per-group Select All checkboxes.
   - `Q-08`: Synopsis in Metadata Import uses a multi-line wrapped layout (NOT forced into 1-line `54d`), with Skip, duplicate handling, and atomic `MetadataDelta` Undo/Redo.
   - `Q-10`: `Select All Box` covers dialogue boxes only (excludes Box 0, never mutates Translation Lock).
   - `Q-11`: Safe default for MTL Globe button = copy active box text to clipboard + open official provider website; URL text deep-links ONLY where verified and explicitly approved by Project Lead.
   - `Q-12`: Window title `filename — Title (Subtitle)` reads already-parsed metadata (zero disk re-read) with length truncation.
7. **`S11d` Refinements (`Q-03`, `Q-05`, `Q-13`–`Q-17`):** Accepted verbatim:
   - `Q-03`: Per-widget-class word-wrap contract (no blanket `wrap="none"` / `wrap="word"`).
   - `Q-05`: Honest splash progress without blocking the main thread.
   - `Q-14`: `Support the Creator`, full English copy, enlarged Pillow GIF (~600px target width preserving aspect ratio; no FFmpeg/OpenCV).
   - `Q-16`: Remove 3x duplicate `NGUI Glossary` + require an explicit old-to-new command/shortcut/regression inventory proposal approved by Project Lead BEFORE restructuring the Main Menu.
   - `Q-17`: Complete missing tooltips + preserve Project Lead's original **"3-layer tooltip" (`tooltip tiga lapis`)** meaning (do NOT reinterpret as 3 font sizes); produce a written 3-layer definition proposal for approval if no prior spec is found on disk.
8. **Updated `S12` Scope:** Accepted verbatim. `S12` baseline updates to HOLD at **`1.4.13`**, conditional promotion **`1.4.13 -> 1.5.0`**, full traceability covering `S01–S11d` and `U-01..U-20` + `Q-01..Q-18, Q-22..Q-23`, strictly read-only on production source code.

======================================================================
2. TWO NEW PROJECT LEAD MANUAL QA RULINGS (`Q-22` & `Q-23`)
======================================================================
*(Note: IDs `Q-19`–`Q-21` are intentionally unused to preserve the Project Lead's exact item numbers.)*

- **`Q-22` (Quick Edit — Unified Single-Box UX Parity with Main Dialogue Editor; Proposed for `S11c`):**
  * **Project Lead Ruling:** `Quick Edit` currently splits multi-segment boxes into separate per-segment text boxes (implemented per S10 spec), which does NOT match the Project Lead's workflow expectation. `Quick Edit` MUST present **ONE single unified plain text box** combining all segments — mirroring the normal `Dialogue` Editor's single-box editing model, minus ruler, red overflow markers, NGUI decorators, and preview styling (a small non-blocking `[N segs]` info badge may remain).
  * **Data-Safety & `raw_breaks` Contract (Explicit Alignment with Prior `BUG-06` / `Grok-B01` Policy):**
    - The Project Lead explicitly accepts the same canonical `StoryDocument.inject_box()` text-redistribution semantics already used by the main `Dialogue` Editor (`txt_dialogue`) when editing a multi-segment box as one unified string.
    - `Quick Edit` MUST still capture the complete original `old_snapshot = BoxSnapshot.from_box(box)` (including original `seg_texts` & `raw_breaks`) at session start, update `StoryDocument.records` via canonical `inject_box()` so `raw_breaks` is NEVER stale, capture fresh `new_snapshot = BoxSnapshot.from_box(updated_box)` on commit/flush into ONE logical `BoxSnapshotReplaceDelta` Undo transaction, preserve `speaker`, `voice_cue`, `kind`, `extra_args`, immutable JP keys, and S09b Lock Parity, and verify binary round-trip (`to_binary()` / `from_binary()`) plus lossless Undo back to the original multi-segment split.
    - Existing S10 test `tests/test_v15_s10_all_script_quick_edit.py::test_probe_5` will be updated explicitly from asserting 4 split segment editors to asserting 1 unified `Quick Edit` box with full `StoryDocument.records`, binary round-trip, and original 4-segment Undo restoration.

- **`Q-23` (Dialogue Preview — Remove Red Overflow Marker Blocks; Proposed for `S11b` alongside `Q-18`):**
  * **Project Lead Ruling:** In `Dialogue Preview` mode, do NOT draw red overflow highlight blocks (`line_overflow` / horizontal overflow red background highlights) on overflowing text. Preview is a visual representation of the game itself (where text simply bleeds past the gold frame under `wrap="none"`), NOT an editor correction surface.
  * **Boundary:** Remove red highlight blocks strictly inside `txt_dialogue_preview` (Preview ON). Keep ALL red overflow markers in **Dialogue Editor (Preview OFF)** untouched, and preserve `wrap="none"` native bleed, `54d × 3` pixel calibration, pink Actor nameplate, gold borders, and pink `▼`.
  * **Test Alignment:** Update `tests/test_p3_s18_game_preview.py` (and any S09 preview red-tag assertion) to assert **zero red highlight block tags in Dialogue Preview** while keeping `54d × 3` pixel metrics and `wrap="none"` bleed assertions intact.

======================================================================
3. RESOLVED ICON MAPPING CORRECTION (`Q-15`, VERIFIED AGAINST PROJECT LEAD'S UPLOADED IMAGES)
======================================================================
The Project Lead corrected an earlier filename typo and supplied visual images of all 8 box icons, cleanly resolving the `Replace Box` vs `Select All Box` conflict:
- **Translate (`u-2`):** `assets/icons/language-translation-icon.png`
- **All Script (`u-17`):** `assets/icons/BoxConversationList.png` *(visual: 3 stacked horizontal list rows)*
- **New Box (`u-18`):** `assets/icons/BoxD.png` *(visual: single clean speech bubble — chosen instead of `BoxInsert.png` so New Box and Replace Box do not share an identical icon)*
- **Copy Box (`u-18`):** `assets/icons/BoxCopy.png` *(visual: speech bubble + copy pages)*
- **Cut Box (`u-18`):** `assets/icons/BoxCut.png` *(visual: speech bubble + red scissors)*
- **Paste Box (`u-18`):** `assets/icons/BoxPaste.png` *(visual: speech bubble + orange clipboard)*
- **Replace Box (`u-18` — Project Lead correction):** `assets/icons/BoxInsert.png` *(visual: speech bubble + two circular swap/replace arrows)*
- **Select All Box (`Q-10` / `u-19`):** `assets/icons/BoxSelectAll.png` *(visual: 3 speech bubbles inside a dashed blue selection marquee with 8 handles — zero conflict with Replace Box now that Replace Box uses `BoxInsert.png`)*
- **Parked:** `assets/icons/BoxConversation.png` *(visual: 3 overlapping speech bubbles)*
*(Note: During `S11d` `/plan`, Antigravity must verify exact file extensions `.png` vs `.jpg` and alpha transparency on disk under `assets/icons/`.)*

======================================================================
4. FINALIZED TRACK A vs TRACK B ROADMAP (PENDING GPT SIGN-OFF)
======================================================================
- **`S11b` (`v1.4.11`):** `Q-01` (XUAT scanner exclusions/metrics/tests), `Q-02` (Save hang profiling/fix + `Ctrl+S` Save Project & separate Save & Patch Bundle shortcut), `Q-04` (investigate `1.1` `▶` & reproduce `1.2` >3-linebreak drag/select; `1.3` stays `NOT TESTED`), `Q-18` (Ruby Preview bug fix with `/plan` architecture-risk STOP gate), **`Q-23`** (remove red overflow highlight blocks inside Dialogue Preview while keeping `wrap="none"` bleed and Editor red markers).
- **`S11c` (`v1.4.12`):** `Q-06` (Import MouseWheel propagation), `Q-07` (per-group tri-state Select All), `Q-08` (multi-line Synopsis Metadata Import + `MetadataDelta` Undo), `Q-09` (Archiving sub-header cleanup), `Q-10` (`Select All Box` excluding Box 0 & preserving Lock), `Q-11` (MTL Globe button — safe clipboard + official site), `Q-12` (truncated `Title (Subtitle)` in window title bar), **`Q-22`** (Quick Edit unified single-box editing matching main Dialogue Editor + lossless original-segment Undo & `raw_breaks` binary round-trip).
- **`S11d` (`v1.4.13`):** `Q-03` (per-widget word-wrap contract), `Q-05` (non-blocking splash lifecycle), `Q-13` (`PriconneRe:TL` + `Cornelia` branding), `Q-14` (`Support the Creator` EN + ~600px GIF), `Q-15` (corrected icon map above), `Q-16` (3x NGUI Glossary dedup + approved menu inventory), `Q-17` (complete tooltips + approved 3-layer tooltip definition).
- **`S12` (`v1.4.13` -> Conditional `v1.5.0`):** Read-only deep bloat/dead-code/memory-leak audit, 3 pre-existing non-fixture hygiene fixes, full `S01–S11d` traceability (`U-01..U-20`, `Q-01..Q-18`, `Q-22..Q-23`), baseline-relative git check, and honest Release Gate.
- **Track B (Post-`v1.5.0`, Separate Design Meetings):** `BIG-01` (MTL provider research), `BIG-02` (optional MeCab auto-furigana plugin), `BIG-03` (optional Rikaikun-style hover dictionary plugin).

STATUS: AWAITING GPT FINAL SCOPE SIGN-OFF BEFORE GENERATING BOUNDED ANTIGRAVITY PROMPTS (`S11b`, `S11c`, `S11d`, AND REVISED `S12`).