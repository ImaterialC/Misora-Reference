# S2 Execution Guide — Step-by-Step Operator Manual

**Target Slice:** S2 (Minimum Per-Document Dirty Contract & Explicit `on_save() -> bool`)  
**Target Codebase:** `D:\Misora-Editor` (Windows, Python 3.12)  
**Execution Agent:** Google Antigravity  
**Companion Prompt:** `prompts/S2_dirty_contract_final_locked.md`

---

## Step 1: Pre-Execution Workspace Hygiene
Before running S2 in Google Antigravity, ensure all prior S0 and S1 work is cleanly committed in local Git:
```powershell
cd D:\Misora-Editor
git status --short
# S0 and S1 must be committed so S2 produces a clean, isolated git diff
```

---

## Step 2: Run Planning Mode in Google Antigravity
1. Open Google Antigravity in the workspace `D:\Misora-Editor`.
2. Copy the entire contents of [S2_dirty_contract_final_locked.md](file:///d:/Reference/Reference%20Files/prompts/S2_dirty_contract_final_locked.md).
3. Paste the prompt directly into the chat with `/plan`.
4. Ensure Antigravity enters planning mode (ZERO file edits).

---

## Step 3: Audit the Implementation Plan Artifact
When Antigravity generates its **Implementation Plan**, inspect these 7 critical verification checkpoints before approving:
1. **`test_34` Classification:** Verify which branch was detected (Branch 1: `open_file`/`on_save`, Branch 2: `misora.py` `mark_saved`, or Branch 3: direct journal manipulation). If Branch 3 is reported, Antigravity MUST stop and ask for direction.
2. **`StoryDocument` Serializer:** Verify it identified the live full-document serializer from `core/story_ast.py` (not a boxes-only digest).
3. **Plain-Text Cache Key:** Verify the cache key convention matches `misora.py` (`str` vs `Path`).
4. **No-Op KeyRelease:** Confirm `_on_dialogue_edited()` returns a boolean and UI sync is gated by `True`.
5. **Rule 15 Disclosure:** Confirm `BatchTranslateDialog.worker()` threading is acknowledged as pre-existing, with S2 keeping updates flag-only.
6. **Zero Core Edits:** Verify `core/` modules are strictly protected from modification.
7. **Scope Boundaries:** Confirm S3 (Save-All on exit), S4 (structural cut/paste), S5 (bulk delta), S6 (threading), and S7 (full journal) remain strictly out of scope.

If all 7 points align: Click **Proceed**.

---

## Step 4: Verify TDD Execution & Walkthrough Deliverables
After clicking Proceed, verify the execution outputs presented in the **Walkthrough artifact**:
- **Pre-Fix Failing-First Evidence:**
  * Probes 1–10 and 12 MUST fail on unpatched code.
  * Guard 11 MUST pass on unpatched code.
- **Post-Fix Verification Suite:**
  ```powershell
  py -3.12 -m compileall -q misora.py core assets tests
  py -3.12 -m unittest tests.test_s2_dirty_contract -v
  py -3.12 -m unittest tests.test_s1_open_file_safety -v
  py -3.12 -m unittest tests.test_phase2_required -v
  py -3.12 -m unittest discover -s tests -v
  ```
- **Git Hygiene:** Verify `git status --short` touches only `misora.py`, `tests/test_s2_dirty_contract.py`, and `PROJECT_STATE.md`.

---

## Step 5: Quick 1-Minute Manual Sanity Check in Windows GUI
Launch the editor directly from PowerShell:
```powershell
cd D:\Misora-Editor
py -3.12 misora.py
```
Perform these 3 fast manual tests:
1. **Multi-File Anti-Clobber (P0):**
   - Open Document A -> edit 1 word -> asterisk `*` appears in window title and Opened Files dock.
   - Open Document B -> edit 1 word -> press `Ctrl+S` (`*` clears on Document B).
   - Click back to Document A -> confirm `*` is immediately visible -> click inside the dialogue box and press Left/Right arrow keys -> confirm `*` does NOT disappear.
2. **No-Op Arrow Key Navigation (Anti False-Dirty):**
   - Open a clean document (no `*`).
   - Click inside the dialogue box, press Left/Right arrow keys, then click inside the Speaker box and press arrow keys -> confirm `*` does NOT appear.
3. **Plain-Text Cache Parity:**
   - Open a `.txt` file, edit 1 line -> switch to another document -> switch back -> confirm edits are preserved and `*` remains active.

---

## Step 6: Phase 4 Cross-AI Audit & S3 Transition
1. Present the Walkthrough artifact and `git diff --stat` to the AI review board for rapid verification.
2. Commit S2 locally.
3. Proceed to Slice S3 (Save-all on exit, close-file abort, raw plain-text model save `F-GPT-04`, and `write_atomic_utf8`).
