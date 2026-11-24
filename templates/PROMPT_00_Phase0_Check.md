# MULTI-AI ENGINEERING COUNCIL — PHASE 0 (FILE ACCESS & BASELINE CHECK)

You are participating in a structured Multi-AI engineering council for **[PROJECT_NAME]** (Next Cycle: **[CYCLE_NAME, e.g., v1.4.2]**).
We are strictly in **PHASE 0: File Access & Baseline Lock**. Do NOT propose code patches, architecture, or Antigravity prompts yet.

## 1. Authoritative Inputs to Verify
1. **Target Codebase Repo:** `[GITHUB_REPO_URL]`
   - Expected Pinned Baseline Commit SHA: `[40_CHAR_COMMIT_SHA]` (Version: `[CURRENT_VERSION]`)
2. **Meeting Reference Index / Bundle (`MANIFEST_AUTO.md` or `_BUNDLE_*.md`):**
   `[PASTE_RAW_URL_FROM_scan_meeting.bat]`
3. **Project Lead Wishlist (`USER_WISHLIST.md`):**
   `[PASTE_USER_WISHLIST_URL]`
4. **Core Governance Docs in Target Repo:** `AGENTS.md`, `PROJECT_STATE.md`, `CHANGELOG.md`, `README.md` (and key code files `[e.g., misora.py / split parts]`).

## 2. Non-Negotiable Ground Rules (All Phases 0–6)
- **Zero Fabricated Verification:** NEVER guess file contents, line numbers, or runtime behavior. If a URL is unreachable, truncated, or exceeds your line-read limit, explicitly report `UNREACHABLE` / `TRUNCATED AT LINE X` / `BLOCKED`.
- **Evidence Tags:** Every technical claim in later phases MUST carry `[CONFIRMED]` (directly read in pinned source), `[NEEDS-VERIFY]` (requires live run/fixture), or `[ASSUMPTION]`.
- **Anti-Truncation Rule:** If any single file (such as `misora.py`) is too large for your tool to read completely without truncation, say so NOW and request the pre-split parts (`misora_part01..N`) from the Project Lead.

## 3. Required Phase 0 Deliverable (Concise Proof Block Only)
1. **AI Identity & Tooling:** Model name + capabilities (live raw GitHub fetch, Python sandbox, file upload only, approximate line/KB read limit if known).
2. **Baseline Proof (Anti-Hallucination Check):**
   - Exact `HEAD` commit SHA inspected (must match `[40_CHAR_COMMIT_SHA]`).
   - Exact `__version__` string and latest heading in `CHANGELOG.md` read directly from the repo.
   - Exact byte size / top heading of `USER_WISHLIST.md` and every file read from the Reference Index.
3. **Access Gaps / Truncation Warnings:** List any unreachable URL or file that was truncated mid-read.
4. **Status Line (Mandatory):** End strictly with either:
   - `PHASE 0 STATUS: READY FOR PHASE 1`
   - `PHASE 0 STATUS: BLOCKED — MISSING ACCESS / TRUNCATED FILES` (list exact files needed)
