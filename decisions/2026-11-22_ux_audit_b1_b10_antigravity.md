# Decision Record: UX Audit (B1–B10) & Google Antigravity Migration

**Date:** 2026-11-22  
**Participants:** GPT (Arbiter), Gemini (Technical Reviewer), Qwen (Source Verifier), User (Product Owner)  
**Status:** **LOCKED & ADOPTED**

---

## 1. Migration to Google Antigravity
- **Context:** The execution platform for implementing code changes on `D:\Misora-Editor` (Windows, Python 3.12) has transitioned from GitHub Copilot to **Google Antigravity**.
- **Engineering Discipline Preserved:**
  - Strict file ownership per slice.
  - TDD failing-first regression tests (Probes must fail before fix, Guards must pass before and after).
  - Verification with real Windows terminal command outputs.
  - Zero tolerance for hallucinated APIs, mock bloat, or out-of-scope expansion.
- **Antigravity Specific Conventions:**
  - Engineering prompts open with `/plan` to enforce a zero-edit planning inspection phase.
  - Context pointers leverage `@file` mentions (e.g., `@misora.py`, `@AGENTS.md`).
  - Strict Proceed gate: no files modified until user explicitly approves the Implementation Plan.

---

## 2. UX Audit Findings & Architectural Allocations (B1–B10)

From hands-on user testing, 10 UI/UX defects and design improvements were audited and assigned to the S-series roadmap:

| ID | Issue & User-Approved Solution | Roadmap Assignment |
| :--- | :--- | :---: |
| **B1** | **Preview Mode Read-Only & In-Game Aesthetic:** Toggling Preview (`👁`) must be strictly read-only to safeguard raw NGUI markup. Any edit attempt triggers a cooldown toast. Background styled like in-game dialogue box. | **S8b-1** (LOCKED & PARKED) |
| **B2** | **Ribbon Grouping:** Unify View toggles (Preview `👁`, Single/Continuous View, Select Box) into a clean, monochrome group separate from NGUI format buttons. Dim formatting buttons when Preview is ON. | **S8b-2** |
| **B3** | **Continuous View NGUI Inactive:** Duplicate of `F-GPT-13`/`NEW-2`. Tag wrapper incorrectly points to hidden widget instead of active card editor. | **S8** |
| **B4** | **Header Renaming:** Replace misleading `"GAME VIEW"` label with dynamic header reflecting active view mode (*Dialogue Editor*, *Dialogue Preview*, or *Story Editor*). | **S8b-1** |
| **B5** | **Structured Tooltips:** Adopt 1-tier Rich Tooltip (Title, Short Description, Italic Example) instead of complex, brittle 2-tier timers. | **S8b-3** |
| **B6** | **Stale Line Numbers:** Line number margin fails to recalculate on Enter, Delete, or multiline Paste. | **S8** |
| **B8** | **Empty Script Paste Preview Bug:** Clipboard import dialog renders blank on specific formatted paste inputs. | **S4** |
| **B9** | **Translation Soft-Lock:** Lock dialog box content against typing, Delete, BackSpace, and Japanese IME while keeping text selectable and copyable (`Ctrl+C`). Remap `Cut` -> `Copy`. | **S8b-4** |
| **B10** | **Opened Files vs Open Project:** Left sidebar tab often confused with an Open File action. Resolved by adding `+` signifier and clear navigation tab semantics. | **S9** |
| **Pin** | **Speaker Pin Toggle (`📌`):** Convert pin button into a clear toggle locking/unlocking speaker modification across navigation. | **S8b-2** |

---

## 3. Scope Boundary Rule
To protect data integrity, all presentation/UX items (B1, B2, B4, B5, B9, Pin) are strictly isolated into **S8 / S8b** and cannot be executed until data-integrity slices S2 through S7 are fully verified.
