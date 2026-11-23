---
trigger: always_on
description: Permanent engineering safety guardrails, locked Phase 2.5 decisions, and Windows Python 3.12 verification rules for Misora-Editor.
---

# Misora-Editor — Always-On Antigravity Safety Rules

1. **Read From Disk Only:** Inspect live files in `D:\Misora-Editor` directly. Never assume chat summaries or stale `PROJECT_STATE.md` entries reflect live code.
2. **No Destructive Git Commands:** NEVER run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push`. The Project Lead controls all Git commits.
3. **No Test Weakening:** NEVER delete, skip, weaken, or silently mock failing assertions. Always run real verification via `py -3.12`.
4. **No Unapproved Dependencies:** Do NOT install or add external packages beyond the existing stdlib + UnityPy + Pillow environment.
5. **Surgical Edits on `misora.py`:** `misora.py` (~12,144 lines) stays monolithic during this cycle (`DEF-10`). Make minimal, surgical edits strictly within the current session's Allowed Files.
6. **Hard Locked Domain Guardrails (Phase 2.5):**
   - NEVER alter binary `cmd_id == 35` (narration) or `cmd_id == 32` (subtitle) on any path (`DEF-02`).
   - Clearing a speaker on a box adjacent to narration MUST keep boxes separate (never implicitly merge).
   - Never serialize runtime `Record.uid` into `.misora` or binary/v2 outputs.
   - Never store unsaved drafts or `.unity3d` blobs inside `.misora` v1 (`NO-01`).
   - Never bundle copyrighted `AtlasAdv` sprites or build a game emulator (`NO-02`).
   - Never call Tkinter methods (including `after_idle`) from background worker threads (`AGENTS.md` §15).
   - Never overwrite local untracked `misora_config.json` or pollute repo `backups/` during tests.
7. **Honest Reporting:** Never claim a command or test passed unless executed with actual observed stdout/exit code.
