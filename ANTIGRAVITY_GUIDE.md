# Google Antigravity Prompt Engineering Guide (`Misora-Editor`)

This guide defines the mandatory standards for all Phase 3 prompts targeting **Google Antigravity** for `Misora-Editor`.

---

## 1. Core Principles for Antigravity Sessions

1. **Planning-First Gate (`/plan`):**
   - Always begin engineering prompts with `/plan` so Antigravity inspects the live local disk first, produces an **Implementation Plan artifact**, and WAITS for user approval (`Proceed`) before editing any file.
2. **Small, Dependency-Ordered Sessions (Slices):**
   - Never dump 20 unrelated bugs and 3 new UI features into one giant prompt.
   - Split work into focused, verifiable sessions (e.g., `Session 1: Data Integrity`, `Session 2: Thread Safety`, `Session 3: Feature X`) ordered by strict dependency.
   - Each session must leave the repository in a **green, runnable, fully tested state**.
3. **Explicit Context Pointers (`@file`):**
   - Point Antigravity to exact files on disk (`@AGENTS.md`, `@PROJECT_STATE.md`, `@misora.py`, `@core/...`, `@tests/...`) and explicitly forbid relying on chat summaries as source code.
4. **Strict File Ownership Boundaries:**
   - List **Allowed Files to Create/Modify** explicitly.
   - List **DO NOT Modify** files/modules explicitly to prevent accidental collateral damage.
   - Include a clear **Out of Scope** section so Antigravity does not bleed into the next session.

---

## 2. Mandatory Safety Guardrails (Include in Every Prompt)

Every Antigravity prompt MUST include these non-negotiable guardrails:

1. **No Destructive Git Commands:** Never run `git reset`, `git clean`, `git stash`, destructive `git checkout`, `git commit`, or `git push` (user controls Git commits).
2. **No New External Dependencies** unless explicitly approved in Phase 2.5.
3. **No Test Weakening:** Never delete, skip, weaken, or silently mock existing tests to force a green run.
4. **Honest Execution Reporting:** Never claim a command or test passed unless actually executed with real observed output.
5. **Preserve Existing User Files & Config:** Never overwrite local untracked files (e.g., `misora_config.json`) or print secrets/API keys.
6. **Respect `AGENTS.md` Invariants:** Especially main-thread Tkinter safety, undo integrity, and atomic persistence.

---

## 3. Verification & Testing Standard

Every engineering session prompt should define:

- **Failing-First TDD (where applicable):**
  - Distinguish **Defect/Behavior Probes** (must FAIL before patch, PASS after patch) from **Regression Guards** (must PASS both before and after patch; must only reference pre-existing contracts).
- **Test Isolation:** Preserve/restore global state (e.g., `misora.CONFIG_PATH`) in `setUp`/`tearDown`, suppress modal `messagebox` popups during automated error tests, and never perform live network/API calls in unit tests.
- **Standard Verification Commands (Windows / Python 3.12):**
  ```powershell
  py -3.12 -m compileall -q misora.py core assets tests
  py -3.12 -m unittest tests.<new_or_target_test_module> -v
  py -3.12 -m unittest discover -s tests -v
  ```
- **Required Walkthrough Artifact:** Must include exact commands run, real observed test results, `git status --short`, concise diff summary, and any `PROJECT_STATE.md` update (if owned by the session).

---

## 4. Session Slicing Checklist (For Phase 3 Debate)

Before approving a session split in Phase 3, AIs MUST verify:
- [ ] Does Session N depend on anything still scheduled in Session N+1? (If yes -> reorder!)
- [ ] Is the diff surface small enough that Antigravity won't lose focus or introduce regressions?
- [ ] Does every item from the Phase 2.5 Canonical Ledger appear in exactly one session (zero dropped items)?
- [ ] Are acceptance criteria and test cases concrete and unambiguous?
- [ ] Are there any known pre-existing environment quirks (e.g., untracked `misora_config.json`) documented honestly?
