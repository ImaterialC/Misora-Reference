---
trigger: always_on
description: Permanent Misora-Editor Phase 3 engineering guardrails, locked Phase 2.5 invariants, changelog/version contract, and Windows Python 3.12 verification rules.
---

# Misora-Editor — Always-On Antigravity Safety Rules (Phase 3)

Canonical authority: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`).

1. **Read From Disk Only:** Inspect live files in `D:\Misora-Editor` directly. Never rely on chat summaries or stale `PROJECT_STATE.md` claims. Bind by symbol/function name — shifted line numbers from earlier accepted sessions are NOT a STOP; missing or contradictory behavior IS a STOP.
2. **No Destructive Git Commands:** NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`. The Project Lead controls all Git commits manually.
3. **No Test Weakening or Fake Passes:** NEVER delete, skip, weaken, or mock the code under test to force a pass. If a Defect Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` — NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure. Missing real production fixtures stay `BLOCKED`, never `PASS`.
4. **No Unapproved Dependencies:** Do NOT add external dependencies beyond stdlib + UnityPy + Pillow.
5. **Surgical Edits Only:** `misora.py` (~12,144 lines) stays monolithic during this cycle (`DEF-10`). Edit strictly within the current session's Allowed Files.
6. **Hard Locked Phase 2.5 Invariants (NEVER REOPEN):**
   - Preserve binary `cmd_id == 35` (narration) and `cmd_id == 32` (subtitle) unchanged across every path (`DEF-02`).
   - Clearing a speaker adjacent to narration MUST keep boxes separate (never implicitly merge).
   - Multi-segment editing stays non-blocking with segment-aware Undo (`old_seg_texts`/`new_seg_texts`) and full `BoxSnapshot` paste.
   - `.misora` v1 stores references, workspace state, and stable-key locks `(box_ordinal, sha256(original_jp_text))` ONLY — NEVER drafts, NEVER `.unity3d` blobs, NEVER runtime `Record.uid`, NEVER silently transfer unmatched locks.
   - Native overflow rule: **50 digit-widths without a linebreak OR 3 or more linebreaks (4 or more lines)**, `wrap="none"` bleed, no auto-shrink, no copyrighted `AtlasAdv` sprites, Box 0 Summary unmeasured/deferred (`DEF-04`).
   - `All Script` MTL Drawer = exact 2 `tk.Text` widgets + 5 static status tags; `Import from XUAT` = separate Import-menu floating window sourced strictly from `BepInEx\Translation\en\Text` (no `conflict_manager`, no global pruning).
   - Workers NEVER call Tkinter APIs (including `after_idle`); deliver results on the Tk main thread via `queue.Queue`.
   - Enforce Translation Lock at the model/application layer, not only UI button state.
7. **Changelog & Version Contract:**
   - Every session `S01..S23` appends `### SXX` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md`.
   - Keep `__version__ = "1.4.0"` untouched during `S01..S23`; bump ONCE to `"1.4.1"` ONLY in `S24` after all automated gates pass.
8. **Protect Local Files:** NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, and NEVER pollute repo `backups/` during unit tests.
