# Misora Editor — Multi-AI Engineering Review Board & Reference Archive

This repository serves as the official recording archive, decision ledger, and consensus coordination chamber for the multi-AI engineering review board (**GPT**, **Gemini**, and **Qwen**) collaborating with the human **Product Owner** to harden, refactor, and enhance **Misora Editor**.

- **Target Application Repository:** [ImaterialC/Misora-Editor](https://github.com/ImaterialC/Misora-Editor) (Local: `D:\Misora-Editor`)
- **Review Board Reference Repository:** [ImaterialC/Reference-Files](https://github.com/ImaterialC/Reference-Files) (Local: `d:\Reference\Reference Files`)
- **Autonomous Coding Agent:** **Google Antigravity** (operating locally on Windows with Python 3.12 under strict `/plan` and TDD guardrails).

---

## 🚀 REAL-TIME MILESTONE STATUS BOARD

| Milestone / Slice | Focus & Architectural Boundary | Consensus Status | Immediate Next Action |
| :--- | :--- | :---: | :--- |
| **Phase 0 & Phase 1** | Initial codebase audit, F1–F20 bug identification, AST invariants | **LOCKED** ✅ | Completed & archived |
| **Slice S0 & S1** | Open File Safety, test harness isolation, multi-document caching | **IMPLEMENTED** ✅ | Passing tests (`test_s1_open_file_safety.py`) |
| **Slice S8b-1** | Narrowed Game-Style Dialogue Box Preview (in-game styling) | **LOCKED & PARKED** ⏸️ | Deferred until S2–S7 data integrity slices finish |
| **Slice S2** | Minimum Per-Document Dirty Contract & Explicit `on_save() -> bool` | **UNANIMOUS LOCK** 🔒 | **READY FOR ANTIGRAVITY EXECUTION** via `/plan` |
| **Slice S3 to S11** | Save-All on Exit, Structural Undo, Threading, Full Journal | **PLANNED** 📋 | Queued following S2 verification |

---

## 🔥 INSTANT CATCH-UP BRIEFING (COPY-PASTE FOR NEW AI INSTANCES)

> **For the Human User:** When opening a new chat session with ChatGPT, Claude, Gemini, or Qwen mid-meeting, copy the code block below and paste it as the opening instruction. The AI will instantly understand the full project context and rules without wading through thousands of lines of chat history.

```plaintext
# HANDOFF & CATCH-UP BRIEFING — MISORA EDITOR MULTI-AI ENGINEERING BOARD
## For any new AI instance joining the discussion mid-meeting
Date: 2026-11-22 | Target Codebase: https://github.com/ImaterialC/Misora-Editor | Reference Repo: https://github.com/ImaterialC/Reference-Files

You are stepping into an active, multi-AI consensus review for Misora Editor (an indie Tkinter/Python 3.12 Princess Connect! Re:Dive adv script editor).

==================================================
1. ROLES, DISCIPLINE & PERMANENT LANGUAGE RULES
==================================================
- GPT: Arbiter / deepest inspector / final lock authority.
- Gemini: Technical reviewer / Tkinter safety / UX risk auditor / sync briefs compiler.
- Qwen (Assistant A): Source verifier / bug reproduction / precision corrections.
- Grok: REMOVED from the review board by user (historical Phase 1 findings remain cited, but it has no vote).
- User: Product owner / phase approver / relay between AIs.
- Google Antigravity: The coding agent executing prompts locally on D:\Misora-Editor (Windows, Python 3.12).

STRICT LANGUAGE RULES:
- Address the USER in BAHASA INDONESIA.
- Write all PROMPTS, DEBATE, CRITIQUE, and TECHNICAL DOCUMENTATION in ENGLISH.

STRICT BEHAVIORAL INVARIANTS:
- NEVER hallucinate standalone HTML mockups, web apps, or unrequested features (Misora is strictly desktop Tkinter/Python).
- NEVER produce an execution prompt without UNANIMOUS LOCK from the other AIs and user approval.
- NEVER weaken or delete existing tests to force a pass.

==================================================
2. CURRENT PROJECT STATE & COMPLETED MILESTONES
==================================================
- Phase 0 & Phase 1 (Initial Audit & Debate): COMPLETED & LOCKED.
- Slice S0 & S1 (Open File Safety & Multi-Document Isolation): IMPLEMENTED and PASSING unit tests in D:\Misora-Editor (tests/test_s1_open_file_safety.py).
- Slice S8b-1 (Narrowed Game-Style Dialogue Box Preview): UNANIMOUS LOCK by all 3 AIs and user. Current state: PARKED (UI presentation layer, strictly deferred until S2–S7 data-integrity slices are finished).
  * Key UX rule: Summary Box (Box 0) auto-wraps; Story Dialogue Box does NOT auto-wrap (calibrated to 50 chars x 3 lines, wrap="none", dual-axis overflow markers).
- Slice S2 (Dirty Tracking Contract & Multi-Document Safety): UNANIMOUS LOCK by GPT, Qwen, and Gemini.
  * Solves: Cross-file false-clean clobber, explicit on_save() -> bool return, undo-storm prevention, secondary XUAT retry retention, and preserved test_34/test_39 baselines.
  * Executable prompt: prompts/S2_dirty_contract_final_locked.md
  * Step-by-step verification guide: prompts/S2_execution_guide.md

==================================================
3. IMMEDIATE NEXT ACTION
==================================================
1. Ensure S0+S1 work is committed locally in D:\Misora-Editor.
2. Run prompts/S2_dirty_contract_final_locked.md in Google Antigravity using `/plan`.
3. If Antigravity stops in `/plan` due to test_34 baseline classification (Branch 3: direct journal manipulation), report the exact setup discrepancy and await user direction before approving Proceed.
4. Once S2 is executed and verified PASS, proceed to Slice S3 (Inactive-doc save, close-file abort, save-all on exit).

Please confirm you have digested this state and state your readiness in Bahasa Indonesia.
```

---

## 👥 REVIEW BOARD PROTOCOL & ROLES

The review process follows a strict consensus-driven engineering governance model:

- **GPT:** Acts as the *Final Arbiter* and deepest inspector. Responsible for final `LOCK` / `NOT LOCK` verdicts and high-level architectural constraints.
- **Gemini:** Acts as the *Technical Reviewer*, Tkinter GUI guardian, UX auditor, and compiler of cross-AI sync briefs.
- **Qwen (Assistant A):** Acts as the *Independent Source Verifier*, inspecting live source files directly from disk, validating line numbers, reproducing bugs, and providing precision engineering corrections.
- **Product Owner (User):** Defines product direction, arbitrates UX preferences, and relays messages across AI models.
- **Google Antigravity (Coding Agent):** Autonomous software engineer that receives locked prompts, conducts pre-flight `/plan` inspections, and implements code via failing-first TDD.

---

## 📂 REPOSITORY ARCHITECTURE (TWO-TIER MODEL)

This repository is organized into an **Active Working Desk** (high-signal, zero-noise Markdown documentation) and **Cold Storage Archives** (compressed `.zip` storage for massive raw transcripts):

```text
Reference-Files/
├── README.md                              # Master landing dashboard & instant onboarding prompt
├── SUMMARY_AND_CONSENSUS.md               # Definitive living executive ledger & bug registry
├── INSTANT_ONBOARDING_PROMPT.md           # Standalone copy of the catch-up briefing prompt
├── SECRETARY_PLAYBOOK.md                  # Standard Operating Procedure (SOP) for recording secretary
│
├── prompts/                               # Ready-to-execute engineering prompts & operator guides
│   ├── S0_S1_open_file_safety.md          # Completed slice documentation
│   ├── S2_dirty_contract_final_locked.md  # UNANIMOUS LOCKED prompt for Google Antigravity
│   ├── S2_execution_guide.md              # Operator checklist: preflight, TDD, Windows GUI sanity check
│   └── S8b-1_narrowed_dialogue_box.md     # UNANIMOUS LOCKED & PARKED dialogue preview prompt
│
├── decisions/                             # Concise, 1-page records of major architectural choices
│   ├── 2026-11-22_ux_audit_b1_b10_antigravity.md
│   ├── 2026-11-22_s8b_dialogue_preview_design.md
│   └── 2026-11-22_s2_dirty_contract_consensus.md
│
├── archives/                              # Compressed historical archives (.zip)
│   ├── misora_raw_transcripts_final.zip   # Full historical chat transcripts from GPT, Gemini, Qwen (~616 KB)
│   ├── misora_phase1_debate_turns.zip     # All 28 Phase 1 turn files (~147 KB)
│   ├── misora_phase2_debate_turns.zip     # Phase 2 turn files (~40 KB)
│   └── README_ARCHIVES.md                 # Inventory manifest & SHA256 checksums
│
├── references/                            # Visual reference assets & prompting playbooks
│   ├── assets/                            # In-game UI screenshots & AtlasAdv png
│   └── guides/                            # Google Antigravity & Copilot prompt references
│
├── priconne-adv-tools/                    # External reference parser toolkit
└── tools/                                 # Secretary automation CLI utilities
    └── secretary.py                       # CLI tool for ingestion, verification, and status reporting
```

---

## 📚 COMPREHENSIVE DOCUMENTATION
For detailed technical breakdowns of Misora Editor's architecture, the complete `F1`–`F20` bug registry, user testing audit `B1`–`B10`, and the `S0`–`S11` slice roadmap, refer to:  
👉 **[SUMMARY_AND_CONSENSUS.md](SUMMARY_AND_CONSENSUS.md)**
