# Google Antigravity — Practical Execution & Command Playbook (Misora-Editor)

This guide explains how to operate **Google Antigravity** cleanly across Sessions `S01..S17` using your **Google AI Pro / Go** models (`Claude Opus 4.6`, `Claude Sonnet 4.6`, `Gemini 3.8 Flash`, `GPT-OSS 120B`).

---

## Step 0 — One-Time Setup (5 Minutes, Saves Massive Tokens)

Copy the `setup_antigravity/.agents/` folder into `D:\Misora-Editor\.agents\` so you have:
- `D:\Misora-Editor\.agents\rules\misora-safety.md` (`trigger: always_on`, loaded automatically every turn)
- `D:\Misora-Editor\.agents\skills\misora-verify\SKILL.md` (invocable via `/misora-verify`)
- `D:\Misora-Editor\.agents\hooks.json` + `D:\Misora-Editor\.agents\hooks\guard_git.py` (hard-blocks destructive git commands on `run_command`)

*(Optional: add `.agents/` to `.gitignore` or `.git/info/exclude` if you do not want to commit local Antigravity config to GitHub.)*
If using Antigravity CLI (`agy`), run `/skills reload` once so `/misora-verify` is registered.

---

## Step 1 — Standard Per-Session Workflow (Safe & Reproducible)

For EVERY session (`S01` -> `S17`, strictly in order):
1. **Start a FRESH Antigravity conversation** (CLI: `/clear` or `/new`; App: New Chat) so prior session noise never bleeds into the next slice.
2. **Pick the Recommended Model** from the session's top header comment (or `Phase_3_Master_Plan_and_Qwen_Audit.md` §1B).
3. **Open `prompts/SXX_*.md`** and paste everything **BELOW the `---` line** (so `/plan` is strictly the FIRST token!).
4. **Review the Implementation Plan Artifact:**
   - Verify Preflight line numbers match disk.
   - Verify Allowed/Forbidden files are respected.
   - Leave inline comments on the Plan Artifact if anything looks off (no need to rewrite the whole prompt).
   - Optionally paste the Plan Artifact to Gemini/Qwen in Phase 4 for a 10-second `SAFE TO PROCEED` sanity check.
5. **Click `Proceed`** (or send the follow-up `/boost`, `/goal`, or `/swarm` command below for special sessions).
6. **Verify via `/misora-verify`** and inspect the Walkthrough Artifact (`compileall`, targeted test, full `unittest discover`, `git status --short`, zero `backups/` pollution).
7. **Commit manually yourself in Git** (e.g., `git add ... && git commit -m "S02: strict binary parse & lossless v2"`) before starting `S(N+1)`.

---

## Step 2 — Native Antigravity Command Playbook (When to Use Each)

### A. `/plan` (Mandatory Start on ALL 17 Sessions)
Already built into every file under `prompts/S01..S17`. Forces disk inspection + Implementation Plan artifact before any edit.

### B. `/boost` (Pro Plan — High-Risk Sessions `S02`, `S03`, `S07`, optional `S17`)
After you approve the `/plan` artifact on high-stakes sessions (`S02` AST codec, `S03` AST mutations, `S07` multi-file Replace-All), you can either click `Proceed` on **Claude Opus 4.6** OR invoke `/boost` to trigger 3-phase `Implement -> Challenge/Break -> Orchestrator Spot-Check`:
```text
/boost Execute the approved Implementation Plan for S02 strictly within Allowed Files. Challenge every edge case (truncated binary headers/payloads, cmd_id 0 non-fade, whitespace/category/\b64: v2 round-trip, hard guardrail keeping cmd_id 35/32 unchanged) and verify with /misora-verify.
```

### C. `/goal` (Autonomous Sweep — Ideal for `S01` Test Backup Isolation)
After approving `S01`'s `/plan`, if you want Antigravity to sweep all 23 `tests/*.py` files autonomously until zero backup files leak:
```text
/goal Complete the approved S01 plan: reconcile docs (HYG-01) and isolate app.backup_folder across all tests/*.py (HYG-02).
Done means ALL of the following are verified with real command output:
1. `py -3.12 -m compileall -q misora.py core assets tests` exits 0.
2. `py -3.12 -m unittest tests.test_p3_s01_hygiene_backup_isolation -v` exits 0.
3. `py -3.12 -m unittest discover -s tests -v` exits 0 with 0 failures, 0 errors, 0 skips.
4. Repo `backups/` gained ZERO new files during the test run, and `misora.py`/`core/`/`assets/` have ZERO edits (`git status --short`).
```

### D. `/swarm` (Parallel Isolated Modules + Cross-Model `@verifier` — Ideal for `S09`)
`S09` touches 4 cleanly separated modules. After approving `S09`'s `/plan`, you can run `/swarm` with cheap workers (`Gemini 3.8 Flash`) and a stronger cross-model `@verifier` (`Claude Sonnet 4.6`):
```text
/swarm Execute the approved S09 Implementation Plan with strict exclusive file ownership:
- @sec-worker (Gemini 3.8 Flash): owns @core/security.py and @core/mtl_engine.py (BUG-33 DPAPI fail-closed + decrypt warning).
- @log-worker (Gemini 3.8 Flash): owns @core/logger.py (BUG-32 MisoraLogger.flush completion barrier).
- @splash-worker (Gemini 3.8 Flash): owns @assets/splash.py (BUG-36 safe Splash_*.jpg sorting).
- @app-worker (Claude Sonnet 4.6): owns @misora.py (BUG-32 teardown, BUG-33 warning, BUG-34 reload env dispose, BUG-35 deferred startup).
- @verifier (Claude Sonnet 4.6): owns @tests/test_p3_s09_lifecycle_security.py; audit all worker diffs, verify no file-ownership violations, and run /misora-verify.
```
*(WARNING: NEVER use `/swarm` when two workers both need to edit `misora.py` simultaneously!)*

### E. Context Hygiene & Recovery Commands (Use Mid-Session Anytime)
- **Session getting long or hitting an error loop?** Always place `/compact` at the **very start** of your message:
  ```text
  /compact Preserve the approved SXX Implementation Plan, exact failing test tracebacks, and already-verified edits. Next, fix the remaining failing probe and run /misora-verify.
  ```
- **Need a quick explanation without polluting context?**
  ```text
  /btw Explain why inject_box() failed on Probe 2 without editing any files.
  ```
- **Antigravity repeated the same mistake twice (e.g. forgot `master=self` on a Tk variable)?**
  ```text
  /learn Always pass explicit master= to every tk.BooleanVar/StringVar/IntVar in Misora-Editor dialogs and widgets.
  ```
- **Bad turn / broke a file?** Use `/rewind` (CLI) or **Revert** (App) instead of asking the agent to run `git reset`.

---

## Step 3 — Quota-Saving "Plan-Smart / Execute-Cheap" Trick

If you want to conserve **Claude Opus 4.6 / Sonnet 4.6** quota:
1. Run `/plan` on **Claude Sonnet 4.6** (takes only 1 turn to inspect code and produce an exact, line-anchored Implementation Plan).
2. Review the Plan Artifact yourself.
3. For `S01`, `S09`, `S10`, `S11`, `S12`, switch the model picker to **Gemini 3.8 Flash** before clicking `Proceed`! Because the Plan Artifact already spells out exact functions, lines, and failing-first probes, Flash executes cleanly at a fraction of the quota.
4. Keep **Claude Opus 4.6** for `S02`, `S03`, `S07`, and **Claude Sonnet 4.6** for `S04`, `S05`, `S06`, `S08`, `S13..S17`.
