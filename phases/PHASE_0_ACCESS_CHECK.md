# Phase 0 — Preflight & Complete File Access Check

## Objective
Ensure you have verified access to **all required repositories, files, tools, and supporting images** BEFORE performing any analysis, bug hunting, or brainstorming.

**STRICT RULE:** Do NOT start researching bugs, suggesting features, or debating in Phase 0. Phase 0 is strictly a visibility and integrity audit.

---

## What You Must Check

1. **Target Codebase (`https://github.com/ImaterialC/Misora-Editor`):**
   - Can you inspect the repository tree and read raw file contents?
   - Verify visibility of core areas:
     - Root docs & config: `README.md`, `AGENTS.md`, `PROJECT_STATE.md`, `requirements.txt`, `misora_config.default.json`, `misora.bat`
     - Main GUI: `misora.py` (Note: large file — confirm whether you can read it completely or if it gets truncated!)
     - Core modules: `core/*.py`
     - Assets: `assets/*.py`
     - Docs: `docs/*.md`
     - Tests: `tests/*.py`
   - Report the latest visible commit hash / version if accessible.

2. **Reference Repository (`https://github.com/ImaterialC/Misora-Reference`):**
   - Confirm you have read `PROTOCOL.md`, `ANTIGRAVITY_GUIDE.md`, and the phase files under `phases/`.
   - List all user-supplied reference files visible inside `tools/` and `images/` (or any uploaded files attached by the user in this chat).

3. **Missing, Truncated, or Corrupted Items:**
   - Explicitly flag ANY file that:
     - Returns 404 / permission error / fetch error
     - Is truncated due to size limits (especially `misora.py`)
		-If you are unable to access the complete `misora.py` file or if the integration fails, I have broken it down into 4 parts. https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Misora.py1.4.0.Part1.txt
https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Misora.py1.4.0.Part2.txt
https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Misora.py1.4.0.Part3.txt
https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Misora.py1.4.0.Part4.txt
     - Is unreadable, corrupted, or binary-inaccessible (e.g., images you cannot view)

---

## Required Response Format (Indonesian to User)

Respond in **Indonesian** with:
1. **Identitas Model:** Name/version of your AI model and whether you have live web/GitHub fetch capability or rely on uploaded attachments.
2. **Baseline Terbaca:** Commit hash / version of `Misora-Editor` and `Misora-Reference` you observed.
3. **Inventaris Akses File:** Clear checklist of accessible folders/files (`Misora-Editor`, `Misora-Reference`, `tools/`, `images/`).
4. **Daftar File Bermasalah / Tidak Terbaca / Terpotong:** Explicitly list every gap, OR clearly state: *"Tidak ada file yang rusak, hilang, atau terpotong."*
5. **Status Phase 0:**
   - `STATUS PHASE 0: READY FOR PHASE 1` (if 100% readable)
   - OR `STATUS PHASE 0: BLOCKED — BUTUH FILE TAMBAHAN` (list exact files the user needs to upload/paste).
