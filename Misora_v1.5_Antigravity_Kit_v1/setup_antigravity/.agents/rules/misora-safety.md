---
trigger: always_on
description: Permanent Misora: Story Editor engineering guardrails, locked invariants, A.b.c session versioning contract, and Windows Python 3.12 verification rules.
---

# Misora: Story Editor — Always-On Antigravity Safety Rules (v1.5 Cycle)

1. **Read From Disk Only:** Inspect live files in `D:\Misora-Editor` directly. Never rely on chat summaries or stale ledger claims. Bind edits by symbol/function name — shifted line numbers are NOT a STOP; missing or contradictory behavior IS a STOP.
2. **No Destructive Git Commands:** NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git restore`, `git commit`, or `git push`. The Project Lead controls all Git commits manually.
3. **No Test Weakening or Fake Passes:** NEVER delete, skip, weaken, or mock the code under test to force a pass. If a failing-first Defect Probe ALREADY passes before patching, STOP and record `ALREADY PASSING / NOT REPRODUCED` — NEVER plant a fake bug. `Ran 0 tests` is ALWAYS a failure. Missing real production `.unity3d` fixtures stay `BLOCKED`, never `PASS`.
4. **No Unapproved Dependencies:** Do NOT add third-party dependencies beyond `stdlib + UnityPy + Pillow`.
5. **Surgical Edits & Session Boundaries:** Keep `misora.py` monolithic unless a session explicitly authorizes a new pure-Python `core/` or `assets/` helper module. Edit strictly within the current session's Allowed Files.
6. **Hard Locked Data-Integrity Invariants (NEVER REOPEN):**
   - Preserve binary `cmd_id == 35` (narration) and `cmd_id == 32` (subtitle) unchanged across every path (`DEF-02`).
   - Clearing a speaker adjacent to narration MUST keep boxes separate (never implicitly merge).
   - Multi-segment editing stays non-blocking with segment-aware Undo (`old_seg_texts`/`new_seg_texts`) and full `BoxSnapshot` paste.
   - `.misora` v1 stores file references, view/scope state, and stable-key locks `(box_ordinal, sha256(original_jp_text))` ONLY — NEVER drafts, NEVER `.unity3d` blobs, NEVER runtime `Record.uid`, NEVER silently transfer unmatched locks.
   - Native overflow rule: **50 digit-widths without a linebreak OR 3 or more linebreaks (4 or more lines)**, `wrap="none"` visible bleed in Preview, no auto-shrink, ZERO copyrighted `AtlasAdv` sprites (locally generated clean-room Pillow frames are permitted), Box 0 Summary unmeasured (`DEF-04`).
   - `All Script` mode inside the right-side **MTL Drawer** stays exact 2 `tk.Text` widgets + 5 static status tags (`NO-03`).
   - Silent/global XUAT pruning remains FORBIDDEN; XUAT cleanup/archival MUST be opt-in, previewed, transactional (`.tmp` -> reopen & verify -> `os.replace()`), and preserve strict XUAT format (BOM, CRLF/LF, comments, first unescaped `=`, immutable JP keys).
   - Workers NEVER call Tkinter APIs (including `after_idle`); communicate via `queue.Queue` and use per-job `threading.Event` cancellation + bounded concurrency.
   - Enforce Translation Lock at the model/application layer, not only UI button state.
7. **Versioning & Changelog Contract (`U00` — `A.b.c`):**
   - Root `__init__.py` (`__version__`) is the single version source of truth. Never hardcode versions elsewhere.
   - `A` = major total/product pivot; `b` = official release milestone after all planned sessions pass release criteria; `c` = incremented `+1` per completed session (`1.4.1`, `1.4.2`, ..., `1.4.7`, then official release `1.5.0`).
   - Every completed session updates `CHANGELOG.md` and `PROJECT_STATE.md`. Unfinished, blocked, or reverted sessions are documented with status `BLOCKED` / `REVERTED` WITHOUT bumping a release version.
8. **Protect Local Files & Licensing:** NEVER overwrite untracked `misora_config.json`, NEVER print API keys/DPAPI blobs, NEVER pollute repo `backups/` during unit tests, and NEVER commit proprietary commercial fonts (e.g., `nintendoP_Humming-E_002pr`).
