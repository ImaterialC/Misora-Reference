# Phase 2 — Multi-AI Debate, Cross-Check & Synthesis

## Objective
Combine all Phase 1 independent research dossiers from every participating AI **plus** the user's manual bug findings, UX feedback, and feature ideas. Rigorously cross-check every claim against actual source code until **ALL AIs and the User reach unanimous agreement**.

---

## Rules for Phase 2

1. **Verify Before Agreeing:** Never rubber-stamp another AI's finding. Check the real file and lines in `Misora-Editor`. Catch false positives, stale assumptions, and over-engineering early.
2. **Explicit Verdicts:** Respond systematically to every peer item and user item using clear tags:
   - `[AGREE — CONFIRMED]` — Verified in source code; accept into scope.
   - `[PARTIALLY AGREE]` — Core issue valid, but scope/fix needs refinement.
   - `[DISPUTED]` — Contradicted by source code; MUST include exact file/line counter-evidence.
   - `[RETRACTED]` — Retracting own earlier claim based on peer evidence.
   - `[DEFERRED]` — Valid observation, but should be deferred (e.g., measure-first performance item).
   - `[OUT OF SCOPE]` — Rejected to protect against scope creep / over-engineering.
3. **Preserve User Priorities:** Manual bugs and explicit constraints/non-goals provided by the User take top priority. If a user idea carries a technical risk in Tkinter/UnityPy, explain the risk candidly and propose the safest clean design.
4. **No Premature Prompt Writing:** Do NOT write Antigravity prompts during Phase 2. Focus exclusively on **WHAT** is true, **WHAT** should be fixed/built, and **WHAT** is out of scope.
5. **Strict Exit Condition:** Phase 2 ends ONLY when **EVERY AI** declares `PHASE 2 STATUS: READY TO LOCK` AND the User approves transitioning to **Phase 2.5**.
6. **Language Split:**
   - Summary & any questions for the user in **Indonesian** (outside the code block).
   - Full inter-AI message in **English** inside **ONE single fenced `text` code block** ready to download/copy to peer AIs.

---

## Required English Block Template

```text
# MISORA-EDITOR — PHASE 2 DEBATE & CROSS-CHECK (ROUND <N>)

Reviewer: <AI Model Name>
Responding To: <Peer AI names + User manual findings>
Baseline Verified: <commit hash / version>

======================================================================
1. VERDICTS ON PEER FINDINGS & USER MANUAL INPUTS
======================================================================
- [<Item ID / Slug>] Verdict: [AGREE — CONFIRMED | PARTIALLY AGREE | DISPUTED | RETRACTED | DEFERRED | OUT OF SCOPE]
  * Evidence / Rationale: <Exact file/line check or architectural reasoning>
  * Required Refinement (if any): <Concise adjustment>

======================================================================
2. NEWLY SURFACED TRAPS OR OMISSIONS (IF ANY)
======================================================================
- [<AI>-N01] <Short Slug> | Severity: P0/P1/P2 | [CONFIRMED / NEEDS-VERIFY]
  * Location & Evidence: <file:lines>
  * Why it matters: <Impact on agreed fixes/features>

======================================================================
3. REMAINING OPEN QUESTIONS / BLOCKERS
======================================================================
- <List exact unresolved disagreements, or write "NONE">

======================================================================
4. PHASE 2 GATE DECLARATION
======================================================================
PHASE 2 STATUS: [OPEN — CONTINUING DEBATE | READY TO LOCK FOR PHASE 2.5]
Blocking Items (if OPEN): <List exact IDs blocking lock, or "None">
```
