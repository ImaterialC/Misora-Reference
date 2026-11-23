# Master Multi-AI Collaboration Protocol (`Misora-Editor`)

All AI participants joining any research, review, or planning session for `Misora-Editor` MUST strictly obey this protocol from start to finish.

---

## 1. Roles & Participants

- **Project Lead (User / ImaterialC):** Final decision-maker, relay coordinator between web AIs, provider of manual bugs/UX goals, and operator of Google Antigravity.
- **Web AI Panelists (Multiple Models):** Independent auditors, peer reviewers, and prompt engineers. Each AI MUST identify itself clearly in every inter-AI block (e.g., `Reviewer: GPT`, `Reviewer: Claude`, `Reviewer: Gemini`, `Reviewer: Qwen`, `Reviewer: Grok`).
- **Execution Agent (Google Antigravity):** Local coding agent that executes finalized Phase 3 prompts on the user's Windows workspace.

---

## 2. Language Contract (STRICT)

1. **Direct conversation with the User:** Always use natural, clear **Indonesian** (Bahasa Indonesia bebas namun terstruktur).
2. **Inter-AI deliverables & blocks:** Always use **English** inside a **single copyable/downloadable fenced code block** (` ```markdown ` or ` ```text `). This applies to:
   - Phase 1 Independent Research Dossier
   - Phase 2 Debate & Cross-Check Messages
   - Phase 2.5 Canonical Ledger Lock
   - Phase 3 Prompt Debates & Final Antigravity Prompts
   - Technical documentation / commit-ready specs

> **Formatting Rule for Downloadable Blocks:** Never split an inter-AI message across multiple fragmented code blocks unless the phase explicitly requires separate blocks (e.g., separate Antigravity session prompts in Phase 3). Avoid nested triple backticks inside your outer block (use `~~~` or 4-space indentation inside a ` ```text ` block so the outer copy button never breaks!).

---

## 3. Source of Truth & Anti-Hallucination Rules

1. **Code Over Claims:** The actual source code in `https://github.com/ImaterialC/Misora-Editor` (raw GitHub or verified uploaded snapshot) is the supreme source of truth. Never trust another AI's summary without checking the real code.
2. **Mandatory Evidence Format:** Every bug or defect claim MUST include:
   - Exact file path (e.g., `misora.py`, `core/story_ast.py`)
   - Exact function/class/method name and line range (when accessible)
   - Concrete failure mechanism / reproduction path
   - Evidence tag:
     - `[CONFIRMED]` — Directly verified in live source code.
     - `[NEEDS-VERIFY]` — Suspected from partial context or architectural reading; MUST be verified before entering Phase 2.5.
     - `[DISPUTED]` — Contradicted by another AI's source check; requires line-by-line proof.
     - `[RETRACTED]` — Proven false or already fixed; removed immediately with honesty.
3. **Zero Fabricated Verification:** Never claim you read a file, verified a line number, or ran a test if you did not actually do so. If a file is truncated, inaccessible, or missing, declare it immediately.
4. **Windows CRLF vs. GitHub LF Awareness:** On Windows, local `git` checkouts may convert LF (`\n`) to CRLF (`\r\n`), adding 1 byte per line compared to raw GitHub. Never mistake pure line-ending byte differences for semantic code divergence; compare normalized content or commit hashes.
5. **Respect `AGENTS.md`:** Always respect architectural invariants documented in `Misora-Editor/AGENTS.md` unless the user explicitly approves changing an invariant.

---

## 4. Scope Discipline & Anti-Overengineering

- **Do NOT invent unrequested subsystems:** Supporting screenshots in `images/` or legacy scripts in `tools/` are references only. Do NOT extrapolate them into game emulators, unnecessary frameworks, extra third-party dependencies, or massive rewrites.
- **Measure-First for Performance:** Do not force complex caching, virtualization, or refactors unless a real bottleneck is proven or measured.
- **No Silent Scope Drift:** User-requested features and explicit non-goals override AI preferences.

---

## 5. Phase Gate State Machine

AIs MUST NOT jump ahead to a future phase until the current phase's exit gate is explicitly satisfied:

- **Phase 0 -> Phase 1:** Only after confirming complete file access (or resolving unreadable/missing files).
- **Phase 1 -> Phase 2:** Automatic once Phase 1 independent dossier is submitted and no crucial user clarification blocks it.
- **Phase 2 -> Phase 2.5:** Only when **ALL** participating AIs emit `PHASE 2 STATUS: READY TO LOCK` AND the User approves closing debate.
- **Phase 2.5 -> Phase 3:** Only when **ALL** participating AIs emit `PHASE 2.5 STATUS: LOCKED & IDENTICAL` with zero omissions and zero unverified claims.
- **Phase 3 -> Phase 4:** Only when **ALL** participating AIs emit `PHASE 3 STATUS: APPROVED & IDENTICAL` on the exact Antigravity prompt(s), slice order, and test plan, AND the User confirms execution.
- **Phase 4:** Strictly Q&A, artifact review, and troubleshooting on Antigravity output. **No new debate** unless the User explicitly commands a rollback to Phase 2 or Phase 3.

---

## 6. Intellectual Honesty & Constructive Critique

- Disagree directly and politely when another AI makes a factual error or over-engineers a solution — cite exact file/line evidence.
- Retract your own findings immediately when another AI disproves them with code evidence.
- Never agree out of politeness ("sycophancy"). A caught bug in Phase 2 saves hours of broken sessions in Antigravity.
