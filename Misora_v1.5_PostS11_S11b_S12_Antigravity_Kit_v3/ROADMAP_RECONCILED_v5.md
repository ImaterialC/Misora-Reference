# MISORA: STORY EDITOR — LOCKED POST-S11 ROADMAP (v5 + REVIEWER SYNC)

Baseline: `ImaterialC/Misora-Editor` `main` @ `c1ec40c96c18ae6e4df61d1db77ebf999114be3d` (`__version__ = "1.4.10"`)
Release Status: **`v1.5.0` ON HOLD** until Track A (`S11b`–`S11e`), Manual Windows QA (or valid documented waivers), and `S12` 8-Condition 2-Gate Release Gate complete.

## Track A — 5 Bounded Pre-v1.5.0 Sessions (Sequential Execution, Per-Session Review)
1. **`S11b` (`v1.4.11`):**
   - `Q-01`: Strict `Translation\en\Text` scanner (5 entry points incl. `<GameRoot>\src\BepInEx\Translation\en\Text` + `<GameRoot>\BepInEx\Translation\en\Text`, 5 negative tests for `ja\Text`, unrelated `Text`, standalone `.txt`, `Other`, `RedirectedResources`), 5 additive official XUAT exclusions + preserve legacy exclusions, canonical `_norm_stripped_map` metrics (`entries_read == entry_count == unique_keys + duplicate_entries`, preserving `_exact_map`/`_value_map`/`entries`; operational `files_scanned == len(files_indexed) + len(skipped_files)`).
   - `Q-02`: 5-stage Save Hang profiling + STOP Gate A (+ Forbidden-Core STOP rule) + `Ctrl+S` Save Project (`.misora`) & conflict-free Save & Patch Bundle shortcut + menu/tooltips/`README.md`/tests.
   - `Q-04`: Non-manufactured manual investigations (`1.1` `▶` origin, `1.2` selection/drag/scroll repro, `1.3 = NOT TESTED`).
   - `Q-18`: Ruby Preview bug fix + STOP Gate B (no custom text-layout engine forced into S11b).
   - `Q-23`: Remove red overflow highlight blocks on `txt_dialogue_preview` + defensive overflow helper guard + migrate `test_v15_s03_all_script_preview_paste.py` & `test_p3_s18_game_preview.py` + Editor Preview-OFF retains red markers.
2. **`S11c` (`v1.4.12`):**
   - `Q-22` ONLY: Unified single-box Quick Edit via `box.clean_text` projection, pre-first-mutation `old_snapshot`, canonical `inject_box(idx, None, new_tx)`, 8 AST/Undo/Lock invariants (S09b Row 1 `ALLOWED`), Manual-Dialogue-vs-Quick-Edit AST & binary parity test, migration of `test_v15_s10_all_script_quick_edit.py` & `test_v15_s08_release_gate_stress.py` (`_qe_seg_widgets[0]`).
3. **`S11d` (`v1.4.13`):**
   - `Q-06` (Import MouseWheel over all labels/child frames), `Q-07` (tri-state None/Some/All group Select All), `Q-08` (multi-line `wrap="word"` Synopsis Metadata Import available even when Box 0 `summary` is empty + Skip + duplicate switcher + `MetadataDelta` atomic Undo/rollback + archiving), `Q-09` (remove `"Import Complete -"` sub-header), `Q-10` (`Select All Box` dialogue-only excluding Box 0 & preserving Lock), `Q-11` (MTL Globe button: safe clipboard copy + official website), `Q-12` (truncated `filename — Title (Subtitle)` in window title from parsed metadata).
4. **`S11e` (`v1.4.14`):**
   - `Q-03` (per-widget word-wrap contract), `Q-05` (Splash stays visible until ALL UI/UX + previous-session restoration finish + artificially slowed startup test), `Q-13` (`PriconneRe:TL` bold/larger + `Cornelia` on Splash & About), `Q-14` (`Support the Creator`, English copy, ~600px Pillow GIF, no FFmpeg/OpenCV), `Q-15` (verified icon map: New Box=`BoxD.png`, Replace=`BoxInsert.png`, Select All=`BoxSelectAll.png`, All Script=`BoxConversationList.png`, Translate=`language-translation-icon.png`, Copy/Cut/Paste, Parked=`BoxConversation.png`), `Q-16` (dedup 3× `NGUI Glossary` + `/plan` Sub-Gate 1 menu inventory approval), `Q-17` (complete tooltips + `/plan` Sub-Gate 2 3-layer tooltip definition approval — NOT 3 font sizes).
5. **`S12` (`<final_pre_s12>` -> Conditional `v1.5.0`):**
   - Pre-S12 full-discovery baseline BEFORE editing any test, strictly read-only production source + `test_v15_s08_release_gate_stress.py`, ONLY the 3 pre-approved hygiene fixes (Option B full default-config verification + full 5-surface `test_probe_8`), 4-pillar read-only audit, 8 mandatory Release Promotion Conditions, and 2-Gate separate approval (Gate 1 implementation vs Gate 2 release promotion).

## Track B — Post-`v1.5.0` Major Features (Separate Design Meetings)
- **`BIG-01`:** Deep research & expansion of free MTL providers (`LunaTranslator` reference, reliability/ToS/Cloudflare/VN JP->EN; zero placeholder engines).
- **`BIG-02`:** Optional MeCab Auto-Furigana toggle plugin (license audit, RAM/startup benchmarks, zero collision with native `<ruby>`).
- **`BIG-03`:** Optional Rikaikun-style Japanese hover dictionary plugin.
