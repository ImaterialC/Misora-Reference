# Phase 1 — Independent Research & Audit

## Objective
Conduct a thorough, **strictly independent** technical audit and brainstorm on `Misora-Editor` without being biased by other AIs or leading hints from the user.

---

## Rules for Phase 1

1. **Full Independence:** Do NOT ask what other AIs found. Rely strictly on the verified codebase (`Misora-Editor`), reference tools (`tools/`), and supporting images (`images/`).
2. **Evidence-First:** Every bug or code-level claim MUST cite exact file paths, function/method names, and line numbers (or clearly tag as `[NEEDS-VERIFY]` if a line could not be directly confirmed).
3. **Balanced Coverage:** Inspect across four lenses:
   - **A. Bugs & Data Integrity / Thread Safety / Edge Cases** (Severity: P0 Critical, P1 High, P2 Medium/Low)
   - **B. Efficiency, Performance & Code Hygiene** (dead code, O(N^2) bottlenecks, resource/memory leaks — flag whether proven or needs measurement)
   - **C. Practical Feature & UX Ideas** (high-ROI improvements tailored to Priconne Re:Dive translation workflows — NO over-engineering)
   - **D. Reference Tools / Visual Assets Audit** (if any files exist in `tools/` or `images/`, audit edge cases or traps to avoid before porting/implementing)
4. **Auto-Completion:** Do NOT stall Phase 1 with minor clarifying questions. Place open/ambiguous questions at the bottom of your English block so they are resolved collectively in Phase 2. Only pause to ask the user in Indonesian if a *critical blocker* makes analysis impossible.
5. **Language Split:**
   - Brief executive summary for the user in **Indonesian** (outside the code block).
   - Full research dossier in **English** inside **ONE single fenced `text` code block** ready to copy/download and paste to other AIs.

---

## Required English Block Template

```text
# MISORA-EDITOR — PHASE 1 INDEPENDENT RESEARCH DOSSIER

Reviewer: <AI Model Name>
Date: <YYYY-MM-DD>
Inspected Baseline: <Misora-Editor commit hash / version>
Reference Files Inspected: <list tools/ and images/ inspected, or None>

======================================================================
1. BUGS & DEFECTS (EVIDENCE-BASED)
======================================================================
- [<AI>-B01] <Short Slug> | Severity: P0/P1/P2 | Status: [CONFIRMED / NEEDS-VERIFY]
  * Location: `<file_path>` -> `<Class/function>` (lines X–Y)
  * Problem: <Clear technical explanation of what fails and why>
  * Impact: <Data loss / crash / UI desync / silent corruption>
  * Proposed Fix Direction: <Minimal, safe fix direction>

======================================================================
2. EFFICIENCY, PERFORMANCE & HYGIENE OBSERVATIONS
======================================================================
- [<AI>-E01] <Short Slug> | Measure-First: Yes/No | Status: [CONFIRMED / NEEDS-VERIFY]
  * Location: `<file_path>` -> `<Class/function>` (lines X–Y)
  * Observation: <Concrete bottleneck, leak, or dead code>
  * Recommendation: <Lean optimization or cleanup>

======================================================================
3. FEATURE & UX IMPROVEMENT IDEAS (SCOPED & PRACTICAL)
======================================================================
- [<AI>-F01] <Short Feature Name>
  * User Value: <Why this improves Priconne translation workflow>
  * Proposed Scope: <Lean, Tkinter-safe scope>
  * Guardrails / Risks: <What to avoid>

======================================================================
4. REFERENCE TOOLS / VISUAL ASSETS AUDIT (IF APPLICABLE)
======================================================================
- [<AI>-R01] <Tool/Image Name> — <Edge cases, legacy bugs, or scope constraints>

======================================================================
5. OPEN QUESTIONS FOR PHASE 2 DEBATE
======================================================================
1. <Specific technical verification or design trade-off question for counterpart AIs>
2. <Specific preference question for the Project Lead>

PHASE 1 STATUS: COMPLETE
```
