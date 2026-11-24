PHASE 0 — ACCESS & INTEGRITY CHECK (NO AUDIT / NO FIXES YET)

Targets:
- Repo: `[REPO_URL]` | Expected HEAD: `[40_CHAR_SHA]` (`[VERSION]`)
- Refs/Index: `[URLS_FROM_scan_meeting.bat]`

Rules:
- Never guess unread files. Report `UNREACHABLE` or `TRUNCATED (last line seen)` honestly.
- If `misora.py` truncates or fails, fall back to `misora_part01..N` in Refs.

Output (concise):
1. Model + tool capability (raw fetch / upload-only / max URLs per turn).
2. Proof: `__version__`, `AGENTS.md` last rule #, `USER_WISHLIST.md` item count, and final 2 lines of the largest code file read.
3. Gaps/truncations (or `NONE`).
4. Status: `PHASE 0: READY` | `PHASE 0: PARTIAL` | `PHASE 0: BLOCKED`
