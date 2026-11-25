---
trigger: always_on
description: Permanent Misora: Story Editor engineering guardrails, locked invariants, A.b.c session versioning contract, bounded concurrency + backpressure, and Windows Python 3.12 verification rules.
---

# Misora: Story Editor — Always-On Antigravity Safety Rules (v1.5 Cycle — Rev 2)

1. **Read From Disk Only:** Inspect live files in `D:\Misora-Editor` directly. Never rely on chat summaries or stale ledger claims. Bind edits by symbol/function name — shifted line numbers are NOT a STOP; missing or contradictory behavior IS a STOP.
2. **No Destructive Git Commands & Preserve Pre-Existing Local Work:** NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`. Record initial branch, `HEAD`, and `git status --short` before editing, and preserve all pre-existing user modifications and untracked local files. The Project Lead controls all Git commits manually.
3. **No Test Weakening or Fake Passes:** NEVER delete, skip, weaken, or mock the code under test to force a pass.
   - Failing-first Defect Probes MUST fail before patching and pass afterward.
   - Regression Guards MUST pass both before and after patching.
   - If a Defect Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` — NEVER plant a fake bug.
   - Acceptance/stress tests (e.g., S08) are distinct from failing-first Defect Probes.
   - `Ran 0 tests` is ALWAYS a hard failure.
   - Missing proprietary production fixtures (`storydata_1001005.unity3d`) stay `BLOCKED`, NEVER `PASS`.
4. **No Unapproved Dependencies:** Do NOT add third-party dependencies beyond `stdlib + UnityPy + Pillow`.
5. **Surgical Edits & Strict Session Boundaries:** Keep `misora.py` monolithic unless a session explicitly authorizes a new pure-Python `core/` or `assets/` helper module. Edit strictly within the current session's Allowed Files. If a read-only audit session discovers a source defect outside its Allowed Files, STOP and report it rather than patching silently.
6. **Hard Locked Data-Integrity & Concurrency Invariants (NEVER REOPEN):**
   - Preserve binary `cmd_id == 35` (narration) and `cmd_id == 32` (subtitle) unchanged across every path (`DEF-02`).
   - Clearing a speaker adjacent to narration MUST keep boxes separate (never implicitly merge).
   - Multi-segment editing stays non-blocking with segment-aware Undo (`old_seg_texts`/`new_seg_texts`) and **full lossless `BoxSnapshot` preservation** (`speaker`, `voice_cue`, `kind`, `seg_texts`, `raw_breaks`, `extra_args`) across Insert, Replace, Undo, and Redo.
   - `.misora` v1 stores file references, view/scope state, and stable-key locks `(box_ordinal, sha256(original_jp_text))` ONLY — NEVER drafts, NEVER `.unity3d` blobs, NEVER runtime `Record.uid`, NEVER silently transfer unmatched locks.
   - Native overflow rule: **50 digit-widths without a linebreak OR 3 or more linebreaks (4 or more lines)**, `wrap="none"` visible bleed in Preview, no auto-shrink, ZERO copyrighted `AtlasAdv` sprites (locally generated clean-room Pillow frames are permitted), Box 0 Summary unmeasured (`DEF-04`).
   - `All Script` mode inside the right-side **MTL Drawer** stays exact 2 `tk.Text` widgets + 5 static status tags (`NO-03`).
   - Silent/global XUAT pruning remains FORBIDDEN; XUAT cleanup/archival MUST be opt-in, SHA-256 stale-checked, previewed, archive-first per-file transactional (`.tmp` -> reopen & verify -> `os.replace()`), with mandatory archival backup by default (explicit separate irreversible confirmation required to opt out), preserving strict XUAT format and immutable JP keys.
   - Workers NEVER call Tkinter APIs (including `after_idle`); communicate via bounded `queue.Queue` (cancellation-aware submission), per-job `threading.Event` cancellation, AND **both bounded concurrent workers AND a finite pending-work limit / producer backpressure** (a bare `ThreadPoolExecutor(max_workers=N)` without pending-Future backpressure is insufficient).
   - Enforce Translation Lock at the model/application layer, not only UI button state.
7. **Versioning & Changelog Contract (`U00` — `A.b.c`):**
   - Root `__init__.py` (`__version__`) is the **sole** version source of truth. Never hardcode duplicated version literals elsewhere; other modules must import or derive from `__init__.py`.
   - `A` = major total/product pivot; `b` = official release milestone after all planned sessions and release gates pass; `c` = incremented `+1` per completed session (`1.4.1`..`1.4.7`, then official release `1.5.0`).
   - Unfinished, blocked, or reverted sessions are documented with status `BLOCKED` / `REVERTED` WITHOUT bumping a release version. Do NOT promote to `1.5.0` while any mandatory production-fixture gate remains `BLOCKED` without explicit Project Lead risk waiver.
8. **Protect Local Files & Licensing:** NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, NEVER pollute repo `backups/` during unit tests, and NEVER commit proprietary commercial fonts (e.g., `nintendoP_Humming-E_002pr`).
