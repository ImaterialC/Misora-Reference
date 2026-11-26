# GPT Independent Technical Review — PlanS09 (Post-S08)
## Required Amendments Before Antigravity Execution

I have reviewed the current `PlanS09.md`, all three visual references, and the current public `Misora-Editor/main` source.

**Do not execute S09 yet.** Please revise the specification and session prompts first. Do not modify Misora-Editor source code during this planning revision.

Source references:
- Plan S09: https://github.com/ImaterialC/Misora-Reference/blob/main/PlanS09.md
- Expected All Script: https://github.com/ImaterialC/Misora-Reference/blob/main/Expectasi2.png
- Dialogue Preview comparison: https://github.com/ImaterialC/Misora-Reference/blob/main/DialogueBox-comparation.png
- Current application: https://github.com/ImaterialC/Misora-Reference/blob/main/CurrentDialogueBox.png
- Current project ledger: https://github.com/ImaterialC/Misora-Editor/blob/main/PROJECT_STATE.md

---

## 1. Correct the S08 Baseline Statement

The current public source baseline is:

- Repository: `ImaterialC/Misora-Editor`
- Current `main` HEAD: `1da8ee84d6e6d23e8886b296f65a6e5503ee358f`
- Root `__version__`: `1.4.7`
- Release state: S08 Release Gate Hold.
- `misora.py`: 20,808 lines in the inspected snapshot.

The dedicated S08 stress suite passed 8/8 tests.

However, the full discovery suite is NOT green:

| Result | Count |
|---|---:|
| Passed | 370 |
| Skipped | 35 |
| Failed | 6 |
| Errors | 2 |
| Total | 413 |

The six failures and two errors are described in `PROJECT_STATE.md`:

- Three failures and two errors in `tests/test_s8b2_memory_guards.py` are blocked by the missing proprietary `storydata_1001005.unity3d` fixture.
- One failure in `test_phase3_performance_config::test_05` is related to local `misora_config.json`.
- One failure in `test_s9c_workspace_safety::test_04` is related to a pre-existing missing `misora_config.default.json`.
- One failure in `test_v15_s01_stability_remediation::test_probe_8` is caused by a stale hardcoded `"1.4.1"` assertion after the version has advanced to `1.4.7`.

Please replace the ambiguous statement "413 tests found, 0 regressions" with:

"Dedicated S08 stress suite: 8/8 PASS. Full suite: 413 tests, 370 pass, 35 skipped, 6 failures, 2 errors. Three failures and two errors are fixture-blocked; the remaining three failures require separate test/environment hygiene corrections. No regression was detected inside the dedicated S08 stress suite."

Do not claim that the whole project test suite is clean.

Keep the v1.5.0 release hold. The production fixture blocker must remain explicitly BLOCKED unless the Project Lead resolves or formally waives the requirement under the project's release policy.

---

## 2. S09 — Native Paste Box Must Use the Actual Selection Model

This is a confirmed source-code issue.

In the current `misora.py::on_box_paste()`:

- `start_idx` is derived from `current_box_idx`.
- Replace targets are calculated as `start_idx + offset`.
- `_selected_boxes` is not used to determine the Replace target list.

Therefore, the Dialogue view's selected Box count cannot control Replace as expected.

Please define these exact rules:

### Replace mode

1. Use `_selected_boxes` as the source of targets.
2. Sort selected target indices in document order.
3. Match clipboard snapshots to selected target Boxes one-to-one.
4. Require exact equality between selected Box count and clipboard Box count.
5. If counts differ, abort before mutation and show both counts.
6. Never silently clamp, partially replace, or append extra content.
7. Handle locked targets explicitly. Do not silently skip a locked Box and shift subsequent clipboard content onto another target.
8. Box 0 metadata (`-1`) must never be treated as `doc.boxes[-1]`; define an explicit metadata policy or reject it from normal Box Replace.

### Insert mode

Define whether selection is ignored or whether insertion occurs after the last selected Box. My recommendation is to retain the active Box as the insertion anchor and explicitly state that selection is only used by Replace.

Add tests for:

- One selected Box.
- Multiple selected Boxes.
- Non-contiguous selections.
- Selection in Dialogue view.
- Selection in All Script view.
- Selected count smaller/larger than clipboard count.
- Locked selected targets.
- Box 0 selected.
- Full Undo/Redo restoration.

The entire operation must be validated before mutation and remain atomic.

---

## 3. S09 — Clarify Pin Speaker Semantics Before Changing It

The current source has two distinct controls:

- The `📌` Pin Speaker button.
- The separate `Jump to Speaker Box` dropdown/button.

The current Pin Speaker implementation preserves the speaker value across normal Box navigation. The current `Next` and `Prev` functions still move sequentially through the document.

Therefore, the new requirement that Pin Speaker makes Next/Prev jump only to the same speaker is a behavior change, not merely a repair of the original sticky-speaker behavior.

Please explicitly define the revised contract.

Suggested behavior when pinned:

1. Capture the active speaker as the pinned speaker identity.
2. `Next` searches for the next Box with the same speaker.
3. `Prev` searches for the previous Box with the same speaker.
4. Do not jump to a different speaker.
5. Define whether reaching the end wraps around or displays a "No further occurrence" message. Do not leave this implicit.
6. Show clear feedback such as `Speaker Miyako — Box 12 of 27`.
7. Define what happens if the pinned speaker is renamed while Pin is active.
8. Preserve the current Add Box behavior that uses the pinned speaker, unless that behavior is intentionally replaced by a separately specified control.

Update tooltip text so that the UI accurately communicates the new behavior.

Do not simply change `on_next_box()` and `on_prev_box()` without preserving current insertion and speaker-edit behavior.

Add tests for repeated speakers, no next/previous match, one occurrence, empty speaker, narration, speaker rename, and pin/unpin transitions.

---

## 4. S09 — Speaker Autocomplete Popup Position

The current implementation creates an overrideredirect `Toplevel` and then calculates its geometry in `_refresh_speaker_autocomplete()`.

The user reports that on the first click the popup appears at screen coordinate `(0, 0)` outside the application window.

Please fix the popup lifecycle, not merely add another geometry assignment.

Requirements:

1. Create the popup initially withdrawn/hidden.
2. Wait until the parent and Entry layout geometry is valid.
3. Calculate screen coordinates from the actual `entry_speaker` root position.
4. Clamp the popup to the usable screen/work area.
5. Handle negative coordinates and multiple monitors.
6. Show the popup only after the correct geometry has been applied.
7. Never flash the popup at `(0, 0)`.
8. Preserve the S05 FocusOut safety behavior so focusing the autocomplete list does not commit a speaker rename.
9. Test first click before typing, first click after typing, empty filter, window movement, resize, and 125%/150% DPI.

Do not regress the existing FocusOut fix.

---

## 5. S09 — Adopt the 54d Calibration as One Shared Measurement Contract

The current `_measure_dialogue_metrics()` still calculates `safe_w` using 50 digit-widths:

`rf.measure("1234567890" * 5)`

Replace the old 50d contract with a single shared 54d measurement source.

New rule:

- Exactly 54 digit-widths is within the horizontal limit.
- Horizontal overflow begins only beyond 54d.
- Three lines are within the vertical limit.
- Four or more lines are vertical overflow.

Use the same measurement helper for:

- Dialogue ruler.
- Header character/overflow indicator.
- Dialogue Editor red marker.
- Dialogue Preview.
- Auto Word Wrap.
- Any other feature that depends on dialogue width.

Do not implement different approximations in each UI component.

Update the S17 measurement tests and S06 word-wrap tests. Update every stale 50d reference in the applicable project invariants, documentation, and tests.

### Box 0 exception

Box 0 must be excluded from:

- Horizontal overflow red markers.
- Vertical overflow red markers.
- Dialogue overflow warnings.
- Auto Word Wrap.
- Any 54d × 3 dialogue-card clipping rule.

Box 0 is metadata/synopsis, not an ordinary dialogue Box. Its complete title, subtitle, and synopsis must remain visible.

The All Script interface has no red overflow marker at all under U-20; preserve that distinction.

---

## 6. S09 — Dialogue Preview Pink Arrow and Frame Clipping

Use the provided `DialogueBox-comparation.png` as the visual comparison reference.

The pink down arrow in the lower-right corner must be fully visible, sharp, and not clipped by the dialogue content widget or gold border.

Please inspect the actual stacking and clipping behavior of the Canvas, frame, and text widget.

Reserve a dedicated area for the arrow and ensure:

- The right gold border remains continuous.
- The arrow remains entirely inside its intended visual region.
- Text never draws over the arrow.
- The arrow does not get clipped by the parent widget.
- The result remains correct at DPI 100%, 125%, and 150%.

Do not treat this as merely a color or padding adjustment. Add a GUI-level regression test or a repeatable screenshot verification procedure.

---

## 7. S09 — Remove Windows Console Toggle Completely

The current source still contains:

- `Show / Hide Windows Console` Debug menu item.
- `var_console_visible`.
- Console visibility state in debug preferences.
- `_toggle_windows_console()`.
- `_toggle_console_visibility()`.
- `_toggle_console_shortcut()`.
- F12 key binding.
- Console-specific messages and tests.

The user explicitly wants this feature removed because it does not behave as intended in their Windows 11 Terminal environment.

Remove the entire console visibility feature, not only its menu entry.

Requirements:

- Remove the menu option.
- Remove F12 binding and shortcut handler.
- Remove console-specific application state.
- Remove persisted `console_visible` preference handling/writing.
- Remove console toggle tests and replace them with a guard that ensures F12 is no longer bound to this feature.
- Keep Debug logging, Log to File, log filtering, and normal diagnostics intact.
- Do not remove `ctypes` globally if it is still used by font or other Windows functionality.
- Do not overwrite the user's existing `misora_config.json`; tolerate old `console_visible` keys safely.

---

## 8. S09 — MTL Apply Button Position

Move each MTL Apply (`←`) button to the left of its engine name, matching the requested layout.

Verify all engine cards, refresh buttons, drawer resizing, and light/dark themes. Keep engine-specific Apply behavior and existing lock/stale-result safeguards unchanged.

---

## 9. S10 — Choose Virtualized Card Pool for All Script

After inspecting `Expectasi2.png`, I recommend architecture option A:

**Virtualized Read-Only Card Pool.**

A single `tk.Text` cannot provide independent fixed-height clipping and internal scrolling for each Box. A permanent widget per Box may become expensive for documents containing 150–300+ Boxes.

Use a pool of reusable card widgets:

- Only visible cards plus a small dynamic overscan buffer are instantiated.
- Widget count is based on viewport size, not total document Box count.
- Reuse the same widgets when scrolling to new Box indices.
- Do not create Pillow header images per Box.
- Preserve selection and Translation Lock behavior.
- Preserve Box UID identity while widgets are recycled.
- Ensure no stale event callbacks apply to a different Box after recycling.

Do not hardcode the pool to exactly 12–15 rows. Calculate viewport capacity and overscan dynamically.

### U-20 card design

For ordinary dialogue Boxes:

- Fixed visual height of three text lines.
- Width based on 54 digit-widths.
- No red overflow marker in All Script.
- Four or more lines must not increase card height.
- Keep excess content in the underlying model.
- Provide a clear selected/active Box highlight.
- Keep selection and lock indicators visually distinct.
- No unnecessary dashed separators.
- No voice cue data may be deleted from the AST merely because the header presentation changes.

### Important visual reference contradiction

`Expectasi2.png` appears to show a blue voice/sound indicator and the voice cue identifier `vo_adv_1007003_000` in the header.

However, U-20 says the header should have no sound icon.

Please resolve this contradiction explicitly:

- If the screenshot is authoritative, preserve the voice cue indicator and text.
- If the written specification is authoritative, remove the icon and clarify whether the voice cue text is also hidden.
- Do not discard voice cue information from the document model.
- Update the visual reference if it is no longer authoritative.

### Box 0

Box 0 must appear as a separate full metadata/synopsis block. Do not force it into the ordinary 54d × 3 dialogue card. Never clip its complete synopsis or display a red overflow warning.

### All Script Preview removal

Remove only the separate All Script Preview rendering mode. Keep Dialogue Preview as an independent feature.

The Preview control must continue to work in Dialogue mode. Do not accidentally remove or regress the clean-room Dialogue Preview renderer or its pink arrow.

### Replace S08 architecture-specific test assumptions

The current S08 stress test asserts:

- Exactly one mapped `tk.Text`.
- At most three total `tk.Text` descendants.
- Zero Treeview widgets.

These assertions describe the old Technique A implementation and must be revised when the virtualized architecture is accepted.

Replace them with new invariants:

- Widget count remains bounded as total story Box count increases.
- Active card widgets scale with viewport height, not document length.
- No per-Box permanent widget explosion.
- No memory growth proportional to every render/scroll cycle.
- Recycled widgets never display stale Box content.
- 150-, 300-, and preferably 1000-Box stress cases work.
- Scroll-to-end and scroll-back do not rebuild every card.
- Selection and lock state survive widget recycling.

Record initial render, scroll, active-card update, and 142+ Box paste performance on the same Windows/Python/Tk environment as the old 1436.37 ms benchmark.

Do not claim an O(1) total operation if AST mutation itself still requires document-wide work. The UI requirement is that Quick Edit does not trigger a full All Script UI render for every keystroke.

---

## 10. S10 — Quick Edit Must Preserve Full Document State

`Quick Edit` is a new editor path, not just a plain Text widget.

Requirements:

1. All Script remains read-only.
2. Quick Edit edits only the currently active Box.
3. Updating Quick Edit must patch only the corresponding visible All Script card.
4. Never call `_render_continuous_view()` for every keystroke.
5. Commit a pending edit before changing the active Box, closing the document, or switching documents.
6. Translation Lock must be checked at the model/application mutation layer.
7. Use stable Box UID identity, not only positional indices.
8. Undo/Redo must restore the original and updated state correctly.
9. Preserve all `BoxSnapshot` data: speaker, voice cue, kind, segment texts, raw breaks, and extra args.
10. Multi-segment Boxes must not be flattened or silently lose segment ownership.

Define how Quick Edit handles a Box with multiple segments. It must use the established lossless snapshot/segment-aware model path.

Quick Edit must not change immutable JP source keys or write into `.misora` workspace files.

---

## 11. S11 — XUAT Archiving Scan Must Be Asynchronous and Lightweight

The current source confirms that `XuatCleanupDialog.__init__()` runs candidate classification synchronously and `_populate_candidates()` creates a large number of individual Tkinter widgets.

This is a credible cause of the reported freeze.

Please implement a clear background workflow:

1. Capture an immutable document/XUAT snapshot on the main thread.
2. Run index building and candidate classification in a worker.
3. Worker threads must never access Tkinter or mutate the live StoryDocument.
4. Send progress and result messages through a thread-safe queue.
5. Poll/process the queue only from the main thread.
6. Ignore stale task results after document switch, dialog close, or a newer reload.
7. Support cooperative cancellation.
8. Do not keep obsolete worker state or candidate lists after the operation ends.

Use a lightweight virtualized list or `ttk.Treeview` for archiving candidates instead of creating a Frame, Checkbutton, and multiple Labels for each entry.

Preserve all S07 transaction rules:

- SHA-256 stale-source guard.
- Mandatory archive-first for destructive cleanup.
- Per-file atomicity.
- Exact archive and cleanup reports.
- No silent deletion.
- Existing raw encoding/BOM/newline safety.

### U-09 checkbox semantics

The pre-import checkbox `Archive the XUAT translation` defaults to checked.

Define its unchecked behavior as:

**Import only. Leave every XUAT source file untouched. Do not open cleanup, do not archive, and do not delete or rewrite any source entry.**

When checked, open the XUAT Translation Archiving workflow after a successful import.

This checkbox must never become a way to bypass mandatory archive-first when destructive cleanup is being performed.

### U-11 — Exclude global speaker dictionary entries entirely

The current `core/xuat_cleanup.py` classifies a shared speaker dictionary match as `uncertain`, `selected=False`, with reason `"Shared speaker dictionary match (unchecked by default)"`.

That still displays the actor entry in the candidate list.

The revised requirement is stronger:

- Global Actor/Speaker dictionary entries must not appear in the cleanup/archive candidate list.
- Do not merely leave them unchecked.
- If a value is ambiguous between a speaker dictionary entry and dialogue translation, handle it conservatively and exclude it from destructive cleanup.
- Keep the actor dictionary available for import/matching where appropriate.

### U-14 — Clarify Actor, Title, and Subtitle import semantics

Separate metadata candidates from ordinary dialogue Box rows.

Define explicitly:

- How unique Actor/Speaker candidates are displayed and selected.
- How duplicate Actor/Speaker matches are resolved.
- How actor translations are applied to speaker names.
- How Title and Subtitle are applied to Box 0 metadata.
- How metadata Undo/Redo is recorded.
- How skipped or locked dialogue Boxes are represented.
- Why Box 0 does not appear as an ordinary dialogue card.

The Actor/Speaker dictionary may be used for import, but must remain outside cleanup/deletion candidates.

---

## 12. S11 — Unified Progress Indicator

Unify progress display for:

- Project Search.
- Reload XUAT Index.
- XUAT Archiving Scan.

Use one status-bar progress location, but implement task identity so concurrent tasks cannot overwrite or prematurely hide each other's status.

Each task should have:

- Unique task ID or generation token.
- Start, progress, completion, failure, and cancellation events.
- Clear status text.
- Optional determinate or indeterminate progress.
- Stale message rejection.
- Safe cleanup of task state.

A worker must never call `widget.after()`, `config()`, or any Tkinter API. All UI progress updates must be processed by the main thread.

---

## 13. S12 — Release Gate Must Remain Honest

S12 must not turn known blockers into artificial green tests.

Requirements:

- Fixture-dependent production checks remain BLOCKED without the real fixture.
- The three non-fixture full-suite failures must be fixed or explicitly classified with evidence.
- Replace stale hardcoded version assertions with dynamic version-source parity.
- Isolate tests from real local configuration; never overwrite the user's config to satisfy tests.
- Preserve all user-created/untracked files.
- Report exact test discovery and execution counts.
- Do not promote to `1.5.0` merely because the dedicated stress test passes.
- Preserve the explicit Windows manual QA gate.

Treat the S08 widget-budget test changes as an intentional architecture migration with new acceptance criteria, not as test weakening.

Any new source defect discovered during a read-only S12 audit must be recorded and sent to a follow-up fix session. Do not silently patch outside the session's Allowed Files.

---

## 14. Documentation and Versioning Updates

Please ensure that:

- `PROJECT_STATE.md` records the newly confirmed manual Windows findings.
- `CHANGELOG.md` records the new S09–S11 work.
- The permanent hard invariants update the old 50d threshold to 54d.
- Box 0 metadata exemption is explicit everywhere relevant.
- The All Script architecture contract is updated from Technique A to Virtualized Card Pool after S10 approval.
- Old test assumptions are removed only when replaced by equivalent or stronger acceptance guards.
- S09 starts at `1.4.8`, S10 at `1.4.9`, S11 at `1.4.10`, and S12 only promotes to `1.5.0` after all gates are satisfied.

Do not duplicate version literals across code.

---

## 15. Deliverables Before Execution

Please return:

1. Revised `PlanS09.md` or a clearly versioned replacement.
2. Revised S09, S10, S11, and S12 implementation prompts.
3. Updated architecture decision for All Script.
4. A requirements-to-tests traceability matrix.
5. A clear list of manual verification steps.
6. Updated full-suite baseline and blocker classification.
7. Updated `PROJECT_STATE`/release-gate policy proposal.
8. A list of unresolved questions and visual-reference conflicts.

Do not modify the source code and do not ask for Proceed.

**The revised plan must be reviewed independently before Antigravity begins S09.**