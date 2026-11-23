# Misora-Reference — Multi-AI Research & Antigravity Orchestration Hub

This repository serves as the **shared protocol, reference hub, and onboarding bridge** for multiple web-based AI models (ChatGPT, Claude, Gemini, Qwen, Grok, etc.) collaborating to audit, improve, and plan engineering tasks for **[Misora-Editor](https://github.com/ImaterialC/Misora-Editor)**.

All finalized engineering specifications produced through this multi-AI workflow are executed locally by **Google Antigravity**.

---

## Target Project Overview

- **Target Repository:** `https://github.com/ImaterialC/Misora-Editor`
- **Reference Repository:** `https://github.com/ImaterialC/Misora-Reference`
- **Application:** Misora Editor — a zero-pipeline Tkinter desktop revision editor, multi-scope search engine, and CSIF/XUAT interchange suite for *Princess Connect! Re:Dive* Unity3D story assets (`.unity3d`) and XUAT translation dictionaries (`.txt`).
- **Tech Stack:** Python 3.11+ (3.12 recommended), Tkinter, `UnityPy>=1.20.0`, `Pillow>=10.0.0`, `unittest` test suite (`tests/`).
- **Primary Source of Truth:** Actual live source files on `Misora-Editor` (`main` branch or exact commit hash specified by the user). `PROJECT_STATE.md` is a helpful ledger but may drift; always verify claims directly against source code.

---

## Multi-AI Meeting Workflow (Phase 0 -> Phase 4)

| Phase | Name | Purpose | Exit Gate |
| :--- | :--- | :--- | :--- |
| **Phase 0** | [Access & Integrity Check](phases/PHASE_0_ACCESS_CHECK.md) | Confirm every AI can read all required source files, tools, and images before analyzing. | All AIs report full access (or missing files are supplied). |
| **Phase 1** | [Independent Research](phases/PHASE_1_INDEPENDENT_RESEARCH.md) | Each AI audits `Misora-Editor` independently without influence from other AIs or the user. | All AIs submit their English dossier block; no crucial user blocker. |
| **Phase 2** | [Multi-AI Debate & Synthesis](phases/PHASE_2_DEBATE_SYNTHESIS.md) | Combine all Phase 1 reports + user manual findings. Cross-check code, expose hallucinations, and debate fixes/features. | **UNANIMOUS** agreement from all AIs + User approval. |
| **Phase 2.5** | [Canonical Ledger Lock](phases/PHASE_2_5_LEDGER_LOCK.md) | Fast synchronization gate: all AIs output an identical, uniform master list of agreed bugs & features. Zero omissions, zero hallucinations. | **ALL AIs** confirm `LOCKED & IDENTICAL`. |
| **Phase 3** | [Antigravity Prompt Engineering](phases/PHASE_3_PROMPT_ENGINEERING.md) | Debate execution order, test strategy, and Antigravity session slicing; produce identical Antigravity prompts. | **ALL AIs** confirm `APPROVED & IDENTICAL` prompt(s). |
| **Phase 4** | [Antigravity Execution & Q&A](phases/PHASE_4_ANTIGRAVITY_QA.md) | User runs prompts in Antigravity. AIs strictly review Antigravity plans/walkthroughs and troubleshoot feedback (**NO new debate**). | Session completed & verified by tests. |

---

## Repository Map

```text
Misora-Reference/
├── README.md                          # You are here
├── PROTOCOL.md                        # Master rules: language, evidence, anti-hallucination, consensus
├── ANTIGRAVITY_GUIDE.md               # Antigravity prompt standards (/plan gate, TDD, guardrails)
├── phases/
│   ├── PHASE_0_ACCESS_CHECK.md        # Phase 0 rules & output format
│   ├── PHASE_1_INDEPENDENT_RESEARCH.md# Phase 1 rules & output format
│   ├── PHASE_2_DEBATE_SYNTHESIS.md    # Phase 2 rules & output format
│   ├── PHASE_2_5_LEDGER_LOCK.md       # Phase 2.5 fast sync lock rules
│   ├── PHASE_3_PROMPT_ENGINEERING.md  # Phase 3 prompt & session-slicing debate rules
│   └── PHASE_4_ANTIGRAVITY_QA.md      # Phase 4 execution feedback & Q&A rules
├── templates/
│   ├── MANUAL_FINDINGS_TEMPLATE.md    # User template for manual bugs & feature ideas
│   ├── CANONICAL_LEDGER_TEMPLATE.md   # Standardized Phase 2.5 unified ledger
│   └── ANTIGRAVITY_PROMPT_TEMPLATE.md # Standardized Phase 3 Antigravity prompt structure
├── prompts/
│   └── COPY_PASTE_PROMPTS.md          # Universal copy-paste prompts for web AIs (Phase 0 -> 4)
├── sessions/                          # Optional archive of completed debate rounds & ledgers
├── tools/                             # User-supplied reference tools & legacy scripts
└── images/                            # User-supplied UI screenshots & visual references
```

---

## Quick Start for Any Joining AI

Read these files first in exact order:
1. `PROTOCOL.md` (mandatory global rules)
2. The active phase specification under `phases/PHASE_*.md`
3. `ANTIGRAVITY_GUIDE.md` (mandatory before Phase 3)
4. Target codebase at `https://github.com/ImaterialC/Misora-Editor` (especially `AGENTS.md`, `PROJECT_STATE.md`, `misora.py`, `core/`, `assets/`, and `tests/`)
5. Any user-supplied reference files in `tools/` and `images/` (strictly respecting scope boundaries)
