# Misora-Editor Phase 3 — Operator Guide for Google Antigravity (v3 Final Candidate)

This is the **single unified Phase 3 kit** compiled by Gemini (sole compiler) after incorporating all Round 1, Round 2, and Round 3 critiques from **Qwen**, **Grok**, and **GPT** (all three serving as dedicated correctors/auditors).

---

## 1. Safe `.agents/` Setup (MERGE — NEVER BLIND OVERWRITE!)

Before touching `.agents/`, inspect whether `D:\Misora-Editor\.agents\` already exists:
- **If it already exists:** inspect existing files inside `.agents/rules/`, `.agents/skills/`, `.agents/hooks.json`, and `.agents/mcp_config.json` FIRST. Merge carefully — **NEVER overwrite** existing user rules, skills, hooks, or MCP settings!
- **Recommended optional files to install from `setup_antigravity/.agents/`:**
  1. `.agents/rules/misora-safety.md` (`trigger: always_on`, flat directory, <24 KB)
  2. `.agents/skills/misora-verify/SKILL.md` (invoked as `/misora-verify tests.test_p3_sXX_<name>`)
- **Why NO `guard_git.py` hook is shipped in v2/v3:**
  All three peer reviewers (Qwen, Grok, GPT) correctly identified that Antigravity's published `PreToolUse` payload uses `toolCall.args.CommandLine` and plugin `hooks.json` uses a nested `hooks[]` array, and that an unverified fail-open hook gives dangerous false confidence. **We intentionally removed `guard_git.py` and `hooks.json` from v2/v3.** (Any older GitHub URL pointing to `hooks.json` is stale and should be ignored.)
  - If you later want a mechanical git hook on your exact local Antigravity build, run `/antigravity-guide` and `/agy-customizations` inside Antigravity FIRST, author the hook against the live verified schema, and prove it denies a real test `git commit` attempt before trusting it.
- *(CLI users: run `/skills reload` after installing `SKILL.md`.)*

---

## 2. How to Run Each Session (`S01` -> `S24`)

1. **Fresh chat per session** (`/clear` or New Chat).
2. **Select the recommended model** from the table in `Phase_3_Master_Plan_v3.md` §2.
   - **Quota-saving rule:** For `S14`, `S15`, `S23`, run `/plan` on **Claude Sonnet 4.6**, review the line-anchored Implementation Plan artifact, and optionally switch to **Gemini 3.8 Flash** before clicking `Proceed`.
   - **Never** let Flash plan `FEAT-04` or edit high-risk binary/AST/undo/threading/DPAPI/XUAT code (`S03`, `S04`, `S06`, `S07`, `S09`, `S11`, `S12`, `S19`, `S22`).
   - **GPT-OSS 120B** is strictly for **read-only adversarial diff critique** (e.g., `@test-auditor` inside optional post-milestone read-only `/swarm`).
3. **Open `prompts/SXX_*.md` and paste the ENTIRE file (`Ctrl+A`, `Ctrl+C`, `Ctrl+V`)** — every file begins at **Line 1 Column 1 with `/plan`** (zero wrapper comments above it).
4. **Review the Implementation Plan Artifact** before clicking `Proceed`:
   - Confirm symbol locations (shifted line numbers after S01 are normal; missing behavior is a STOP).
   - Confirm Allowed/Forbidden files and `CHANGELOG.md` entry plan.
5. **Click `Proceed`.** (Only if needed: paste the matching `/goal` snippet from `AFTER_PROCEED_OPTIONAL_SNIPPETS.md`, or `/boost` on a stuck high-risk probe in `S03`/`S04`/`S09`/`S11`/`S22`.)
6. **Review Walkthrough + `CHANGELOG.md`**, then **commit manually in Git yourself** (or consciously carry forward an authorized tree) before moving to `S(N+1)`.

---

## 3. Changelog & `v1.4.0` -> `v1.4.1` Version Contract

- Every session `S01..S23` appends a concise `### SXX` entry under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md` so you can always see at a glance what was fixed, which files changed, which test module passed, and what remains `BLOCKED`.
- `__version__` in root `__init__.py` **stays `"1.4.0"` throughout `S01..S23`** (avoiding 23 fake patch bumps and DeepL User-Agent churn via `HYG-06`).
- In **`S24` (Final Acceptance Audit & Release Gate)**, Antigravity always appends `### S24` under `## [Unreleased]` and fixes the hardcoded `"1.4.0"` assertion in `test_01_version_unification` to derive from root `__init__.__version__`. It promotes `## [Unreleased]` to `## [1.4.1] - <YYYY-MM-DD>` and bumps `__version__ = "1.4.1"` ONCE **ONLY** when: (a) all automated gates pass, (b) ZERO unwaived `BLOCKED` P0/P1 items remain (such as `BUG-09` real `.unity3d` fixture verification), AND (c) mandatory manual Windows release blockers (`AGENTS.md` §29: Ribbon Cut, Paste Box both views + visual/smoke checks) are confirmed PASS by you (or explicitly risk-waived in writing)!
