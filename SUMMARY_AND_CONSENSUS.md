# MISORA REFERENCE — MASTER SUMMARY & CONSENSUS LEDGER
## Comprehensive Executive Minutes, Architectural Overview, Bug Registry (F1–F20, B1–B10), and S0–S11 Roadmap

**Author:** Autonomous Recording Secretary Agent (Google Antigravity AI)  
**Target Codebase:** `Misora-Editor` (`D:\Misora-Editor` | [GitHub: ImaterialC/Misora-Editor](https://github.com/ImaterialC/Misora-Editor))  
**Review Reference Repository:** `Misora-Reference` (`d:\Reference\Misora Reference` | [GitHub: ImaterialC/Misora-Reference](https://github.com/ImaterialC/Misora-Reference))  
**Last Synchronized:** 2026-11-22

---

## 1. EXECUTIVE SUMMARY & PURPOSE

This document serves as the **authoritative, single-source-of-truth consensus ledger** for the engineering review board evaluating **Misora Editor**. It synthesizes all technical debates, architectural invariants, verified defects, and feature specifications agreed upon across hundreds of discussion turns between **GPT**, **Gemini**, **Qwen**, and the human **Product Owner**.

By consolidating these determinations into a structured, zero-redundancy format, any new AI instance or developer can immediately understand the project state, verified design constraints, and active engineering milestones without reading multi-megabyte chat transcripts.

---

## 2. MISORA EDITOR ARCHITECTURAL OVERVIEW

Misora Editor is an indie desktop story/script editor designed for Princess Connect! Re:Dive adv scripts (`.unity3d` text assets). It is implemented in Python 3.12 utilizing standard Tkinter for GUI controls, interacting with NGUI-tagged text formats, raw binary Unity assets, and XUnity Auto Translator (XUAT) dictionary mappings.

### Core Component Breakdown:
- **`misora.py`:** Application entrypoint, main Tkinter window lifecycle, ribbon toolbar, tab management, key/mouse event dispatching, and view presentation logic.
- **`core/story_ast.py`:** Object AST (*Abstract Syntax Tree*) model representing scripts (`StoryDocument`, `Box`, `CommandRecord`), responsible for serialization and deserialization.
- **`core/bundle_io.py`:** Unity binary asset packaging and extraction utilizing UnityPy/binary serialization.
- **`core/script_codec.py`:** Bidirectional codec translating raw script streams to and from AST nodes.
- **`core/undo_journal.py`:** Delta-based command history engine supporting undo and redo operations.
- **`core/ngui_tags.py`:** Parser, validator, and renderer for NGUI formatting tags (`[b]`, `[i]`, `[color]`, `<size>`, ruby annotations).
- **`core/mtl_engine.py`:** Machine translation assistant engine supporting asynchronous translation calls.
- **`core/search_engine.py`:** Cross-document and cross-box text search and regex evaluation engine.
- **`core/xunity_sync.py`:** Bidirectional synchronizer with XUnity Auto Translator persistent dictionary files.
- **`core/security.py`:** Filesystem sanitization, path traversal mitigation, and asset integrity validation.
- **`core/logger.py`:** Application logging and diagnostic subsystem.
- **`tests/`:** Automated regression test suite implemented under standard Python `unittest`.

---

## 3. MULTI-AI REVIEW BOARD GOVERNANCE

The engineering review operates under a strict consensus-driven multi-model protocol:

| Participant | Primary Designation | Core Responsibility |
| :--- | :--- | :--- |
| **GPT** | Final Arbiter | Deepest architectural inspector; holds final `LOCK` / `NOT LOCK` authority; authors initial engineering prompts. |
| **Gemini** | Technical Reviewer | Tkinter GUI and UX risk auditor; evaluates thread safety; compiles cross-AI synchronization briefs. |
| **Qwen (Assistant A)** | Source Verifier | Verifies assertions against disk source; reproduces edge-case bugs; contributes precision technical corrections. |
| **Product Owner (User)**| Executive Director | Defines product scope, arbitrates UX preferences, and relays messages across AI models. |
| **Google Antigravity** | Autonomous Coding Agent | Executes finalized engineering prompts locally in `D:\Misora-Editor` following strict `/plan` pre-flight and failing-first TDD. |
| *Grok* | *Dismissed* | *Removed from the review board by user after Phase 1. Historical findings remain valid where cited, but it holds no voting rights.* |

### Operational Communication Rules:
1. All direct interaction with the human **Product Owner** is conducted in **Bahasa Indonesia**.
2. All technical debates, cross-AI critiques, engineering prompts, and code documentation are conducted in **English**.
3. **No Execution Without Unanimous Lock:** No code edits are permitted until GPT, Gemini, and Qwen achieve unanimous `LOCK` and the Product Owner approves.

---

## 4. MASTER DEFECT & BUG REGISTRY

### A. Foundational Data Integrity & System Defects (F1–F20)
- **F1 (Dirty Tracking Desynchronization):** The `is_dirty` flag and `open_documents` cache desynchronize during document switching. *(Resolved in S2)*.
- **F2 (Inconsistent `on_save()` Return Value):** `on_save()` returns `None` on exits and fails to report disk exceptions as boolean values. *(Resolved in S2)*.
- **F3 (Undo-Storm & False Baseline):** Undoing edits triggers redundant widget-wide UI re-renders and fails to restore clean state at saved baselines. *(Resolved in S2)*.
- **F4 (Plain-Text Save Model Clobber):** Plain-text files opened in preview mode risk data corruption during persistence. *(Assigned to S3)*.
- **F5 (Close File Abort Missing):** Closing tabs does not abort when saving fails. *(Assigned to S3)*.
- **F6 (Structural Snapshot Integrity):** Cut/Paste/Delete Box operations corrupt internal Box ID sequences. *(Assigned to S4)*.
- **F7 (Multi-File Replace-All Safety):** Unvalidated direct disk modifications during multi-file replace. *(Assigned to S5)*.
- **F8 (Threading Race Conditions):** Worker threads in search and MTL touch Tkinter widgets outside `after()`. *(Assigned to S6)*.
- **F9 (XUAT Secondary Error Wipe):** Dictionary write failures clear `self._modified_boxes` prematurely. *(Resolved in S2)*.
- **F10–F20:** Boundary edge cases in NGUI parsing, unbounded Tcl gradient tag accumulation, UTF-8 BOM encoding validation, multibyte path safety on Windows, and speaker mutation branches.

### B. User Testing & UX Defects (B1–B10)
- **B1 (Preview Mode Guard & Aesthetic):** Preview mode (`👁`) must be strictly read-only to safeguard raw NGUI markup, styled after in-game Princess Connect! Re:Dive dialogue boxes, with a non-modal cooldown toast on edit attempts. *(Assigned to S8b-1; LOCKED & PARKED)*.
- **B2 (Ribbon Grouping):** View toggles grouped separately from NGUI format controls; formatting controls dimmed during preview. *(Assigned to S8b-2)*.
- **B3 (Continuous View NGUI Inactive):** Formatting buttons target hidden widget rather than active editor card. *(Assigned to S8)*.
- **B4 (Header Renaming):** Replace `"GAME VIEW"` with dynamic headers reflecting active view mode. *(Assigned to S8b-1)*.
- **B5 (Structured Tooltips):** Adopt 1-tier Rich Tooltips (Title, Short Description, Italic Example) instead of brittle multi-tier timers. *(Assigned to S8b-3)*.
- **B6 (Stale Line Number Rendering):** Line number margin fails to recalculate on Enter, Delete, or multiline Paste. *(Assigned to S8)*.
- **B8 (Empty Paste Preview Bug):** Clipboard script import preview dialog renders blank on certain inputs. *(Assigned to S4)*.
- **B9 (Translation Soft-Lock):** Dialogue locking mechanism blocking typing and Japanese IME while allowing text selection and `Ctrl+C`. *(Assigned to S8b-4)*.
- **B10 (Opened Files vs Open Project):** Left sidebar tab clarified with `+` signifiers to prevent confusion with opening files. *(Assigned to S9)*.
- **Speaker Pin (`📌`):** Converted to an explicit toggle locking/unlocking speaker modification across navigation. *(Assigned to S8b-2)*.

---

## 5. S-SERIES IMPLEMENTATION ROADMAP (S0–S11)

```mermaid
flowchart LR
    S0["S0: Test Harness"] --> S1["S1: Open File Safety"]
    S1 --> S2["S2: Dirty Tracking Contract"]
    S2 --> S3["S3: Multi-Doc Save/Exit"]
    S3 --> S4["S4: Structural Undo & Paste"]
    S4 --> S5["S5: Bulk Replace Delta"]
    S5 --> S6["S6: Threading Redesign"]
    S6 --> S7["S7: Full Undo Journal"]
    S7 --> S8["S8: Editor Polish"]
    S8 --> S8b["S8b: Dialogue Preview & UX"]
    S8b --> S9["S9: Sidebar Workspace"]
    S9 --> S10["S10: XUAT Hardening"]
    S10 --> S11["S11: Final Packaging"]

    style S0 fill:#2ea043,stroke:#fff,color:#fff
    style S1 fill:#2ea043,stroke:#fff,color:#fff
    style S2 fill:#1f6feb,stroke:#fff,color:#fff
    style S8b fill:#d29922,stroke:#fff,color:#fff
```

| Slice | Milestone Scope | Review Status | Primary Output Files |
| :---: | :--- | :---: | :--- |
| **S0** | Test Harness & Environment Isolation | **IMPLEMENTED** ✅ | `tests/test_misora_core.py` |
| **S1** | Open File Safety & Multi-Document Isolation | **IMPLEMENTED** ✅ | `tests/test_s1_open_file_safety.py` |
| **S2** | Minimum Per-Document Dirty Contract & `on_save() -> bool` | **UNANIMOUS LOCK** 🔒 | `prompts/S2_dirty_contract_final_locked.md` |
| **S3** | Inactive-Doc Save, Close-File Abort & Exit Save-All | QUEUED | `prompts/S3_safe_exit_and_save_all.md` |
| **S4** | Structural Snapshot, Cut/Paste Integrity & B8 Fix | QUEUED | Pending S3 |
| **S5** | Multi-File Replace-All & BulkFileDelta Checkpoints | QUEUED | Pending S4 |
| **S6** | Background Threading Redesign (Search & MTL Async) | QUEUED | Pending S5 |
| **S7** | Full MasterUndoJournal Revisions & Speaker Hardening | QUEUED | Pending S6 |
| **S8** | Editor Polish (B3 Continuous View & B6 Line Numbers) | QUEUED | Pending S7 |
| **S8b-1** | Narrowed Game-Style Dialogue Box Preview (Preview Skin) | **LOCKED & PARKED** ⏸️ | `prompts/S8b-1_narrowed_dialogue_box.md` |
| **S8b-2** | Ribbon Cleanup & Speaker Pin Toggle (`📌`) | QUEUED | Pending S8 |
| **S8b-3** | Rich 1-Tier Structured Tooltips | QUEUED | Pending S8 |
| **S8b-4** | Translation Soft-Lock UX (Caret/Copy Active) | QUEUED | Pending S8 |
| **S9** | Left Sidebar Workspace (Opened Files vs Project Nav B10) | QUEUED | Pending S8b |
| **S10** | XUnity Auto Translator Persistent Sync Hardening | QUEUED | Pending S9 |
| **S11** | Final Integration Verification, Build & Packaging | QUEUED | Pending S10 |

---

## 6. HISTORICAL DEBATE CHRONICLES (CYCLE 1 ARCHIVED)

### A. 2026-11-21: Phase 0 Independent Audits & Phase 1 Consensus
- Gemini, Grok, Qwen, and GPT produced independent technical audit dossiers.
- Cross-review rounds identified foundational AST vulnerabilities, UTF-8 inconsistencies, and Tkinter event wrapper anomalies.
- User dismissed Grok from voting after Round 4 due to inconsistent reasoning.
- Phase 1 locked unanimously, establishing the foundational bug register and slice roadmap.
- S0 and S1 implemented on `D:\Misora-Editor`, passing automated regression tests.

### B. 2026-11-22: Phase 1b UX Audit & Antigravity Migration
- User migrated execution agent from GitHub Copilot to **Google Antigravity**.
- Audit of real-user testing yielded items B1 through B10.
- User clarified word-wrapping behavior for dialogue boxes (Summary Box wraps; Story Dialogue Box does NOT wrap).
- S8b-1 prompt locked unanimously and parked to protect data-integrity priorities.

### C. 2026-11-22: S2 Dirty Contract & Multi-Document Safety Lock
- Gemini drafted revised S2 specification.
- Qwen contributed amendments Q1 through Q6.
- GPT raised blockers B1 (`test_34` saved baseline) and B2 (`StoryDocument` full serializer), which were folded into the text.
- Qwen, Gemini, and GPT issued unanimous **LOCK** on the final S2 prompt text.
- Raw transcripts and debate turn files packed into `archives/*.zip`.

---

## 7. IMMEDIATE OPERATIONAL INSTRUCTIONS (CYCLE 1 S2 EXECUTION)
1. Confirm S0 and S1 local git commits in `D:\Misora-Editor`.
2. Follow the operator checklist in `prompts/S2_execution_guide.md`.
3. Submit `prompts/S2_dirty_contract_final_locked.md` to Google Antigravity with `/plan`.
4. Review the Implementation Plan artifact, confirm baseline classification for `test_34`, and approve `Proceed`.

---

## 8. CYCLE 2: JAPAN SERVER DATAMINE INTEGRATION (ACTIVE DEBATE)

**Status:** **PHASE 0 KICKOFF — ACTIVE DEBATE**  
**Working Directory:** `active_debates/datamine_jp_server/`

### Motivation & Goals:
Princess Connect! Re:Dive JP server is the active upstream development branch where new story content releases first. Cycle 2 focuses on creating an automated pipeline for:
1. **Asset Ingestion:** Local DMM Games PC client asset cache (`%USERPROFILE%\AppData\LocalLow\Cygames\PrincessConnectReDive\a\`) vs. remote CDN downloaders.
2. **Metadata Parsing:** Querying SQLite `master.db` (Robo Ninon datamine: `story_data`, `unit_data`, `event_story_data`) for automatic speaker identification, chapter trees, and character portraits.
3. **CSIF Unpacker Pipeline:** Direct extraction of raw Japanese story bundles into clean `CSIF` documents.
4. **Dual-Language Comparison:** Side-by-side Japanese raw vs. translated text comparison in the editor.
5. **Safety Constraints:** Zero hardcoded decryption keys in source code; user-configured local paths only.

For detailed technical review questions and opening debate prompts, refer to:
- 👉 **[01_KICKOFF_BRIEFING_JP_DATAMINE.md](active_debates/datamine_jp_server/01_KICKOFF_BRIEFING_JP_DATAMINE.md)**
- 👉 **[02_OPENING_PROMPT_DEBATE_JP_DATAMINE.md](active_debates/datamine_jp_server/02_OPENING_PROMPT_DEBATE_JP_DATAMINE.md)**
