# Change Summary — S09–S12 Antigravity Execution Prompts (v1.0)

Responding To: `GPT2Gemini3.txt` (GPT Final Prompt Review — S09–S12 Execution Specifications)
Repository Baseline: `ImaterialC/Misora-Editor` `main` @ `1da8ee84d6e6d23e8886b296f65a6e5503ee358f` (`v1.4.7`, S08 Release Gate Hold)
Execution Boundary: Prompt package revision ONLY. Zero source files modified. Antigravity MUST run `/plan`, present a symbol-bound Allowed Files plan, and wait for explicit Project Lead `Proceed` before each session's first edit.

## All 7 Targeted Corrections Applied

1. **S09 — Corrected Test File Paths & Explicit 54d Reference-Font Contract (`prompts/S09_v1.4.8_Core_Fixes_54d.txt`):**
   - Replaced `tests/test_p3_s17_rulers_overflow.py` -> `tests/test_p3_s17_pixel_rulers.py` and `tests/test_v15_s02_fonts_ruler_chars.py` -> `tests/test_v15_s02_fonts_ruler_metrics.py` in BOTH Part 1 (Allowed Files) and Part 4 (unittest command), plus explicit `/plan` path verification on disk.
   - Specified canonical **Nunito Bold** 54-digit reference pixel width (`safe_w`) as the constant ruler/container boundary across both font presets, while measuring actual dialogue line text width in the currently active dialogue font (zero `tk.Text(width=54)` approximations).

2. **S10 — `BoxSnapshot.raw_breaks`-Safe Multi-Segment Editing & Binary Round-Trip Verification (`prompts/S10_v1.4.9_All_Script_Virtualized_Quick_Edit.txt`):**
   - Explicitly addressed `BoxSnapshot.from_box()` / `StoryDocument._records_from_snapshot()` `raw_breaks` semantics so Quick Edit updates raw segment representation consistently with edited segment texts using existing AST APIs (with a hard STOP rule if forbidden `core/story_ast.py` would be needed).
   - Required `test_probe_5` to verify edited segment content directly in `StoryDocument.records`, serialize via `to_binary()`, reload via `from_binary()`, compare all segments/metadata/`voice_cue`/command structure, and verify full Undo/Redo round-trip.

3. **S10 — View-Aware Quick Edit Sync & One Logical Segment-Edit Transaction (`prompts/S10_v1.4.9_All_Script_Virtualized_Quick_Edit.txt`):**
   - Defined distinct live-sync targets per active view: All Script (patch active visible Virtualized Card only), Dialogue Preview OFF (refresh Dialogue Editor), Dialogue Preview ON (update read-only Dialogue Preview capsule), Raw Commands active (avoid redundant Quick Edit updates except pending-edit flush).
   - Locked single logical Undo transaction per edit session (capture `old_snapshot` at session start, separate segment buffers, commit ONE old/new snapshot delta on flush/commit before nav/mode/tab/doc-switch/close/save — never per keypress).

4. **S11 — Deterministic Pre-Pass Actor/Speaker Protection (`prompts/S11_v1.4.10_Async_XUAT_Archiving_Progress.txt`):**
   - Required building deterministic protected Actor source-key and translation-value sets BEFORE Applied, Duplicate, and Right-Side Matching passes so Actor entries and actor-ambiguous entries NEVER enter `analysis.candidates` (0 rows), duplicate Actor entries across files stay protected, and Actor matching in Import stays intact — without unverified filename-only heuristics.
   - Added all 6 required test cases in `test_probe_3`.

5. **S11 — Import Document Identity Guard & Atomic Metadata Undo/Rollback (`prompts/S11_v1.4.10_Async_XUAT_Archiving_Progress.txt`):**
   - Captured document identity/generation token, path, target Box UIDs + original JP keys, and metadata identity at `ImportFromXUATDialog` construction; required full validation before Apply (abort safely if switched/replaced).
   - Required Title/Subtitle import to use existing metadata model API + `MetadataDelta`, preserve Synopsis untouched unless explicitly selected, and provide transaction-level rollback on mid-operation failure inside ONE Undo batch.

6. **S11 — Cancellable Recursive File Discovery & Reliable Terminal Queue Events (`prompts/S11_v1.4.10_Async_XUAT_Archiving_Progress.txt`):**
   - Required `core/xuat_index.py::build_xuat_index()` to honor `cancel_event` during recursive file discovery as well as parsing (avoiding premature materialization of large file lists).
   - Required unified progress controller to coalesce progress updates per task while NEVER dropping `start`/`complete`/`fail`/`cancel` terminal events, guaranteeing active-task removal and preventing stuck progress bars under queue saturation.

7. **S12 — Baseline-Relative Git Status Verification (`prompts/S12_v1.5.0_Audit_Release_Gate.txt`):**
   - Updated Part 0, Part 4, and Part 5 so final `git status --short` is compared baseline-relatively against the initial pre-session snapshot: pre-existing modifications and untracked files remain untouched and are NOT flagged as S12 violations, while only newly introduced changes must stay strictly inside S12 Allowed Files.
