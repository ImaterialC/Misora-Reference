# MISORA EDITOR — ENGINEERING REVIEW BOARD BRIEFING
## Cycle 2: Princess Connect! Re:Dive Japan Server Datamine Integration (Phase 0 Kickoff)

**Target Codebase:** [ImaterialC/Misora-Editor](https://github.com/ImaterialC/Misora-Editor) (`D:\Misora-Editor`)  
**Reference Repository:** [ImaterialC/Misora-Reference](https://github.com/ImaterialC/Misora-Reference) (`d:\Reference\Reference Files`)  
**Date:** 2026-11-22  
**Status:** **ACTIVE DEBATE — PHASE 0 INDEPENDENT RESEARCH & ARCHITECTURAL PROPOSALS**  
**Review Board Roster:** GPT (Arbiter), Gemini (Technical Reviewer), Qwen (Source Verifier), User (Product Owner), Google Antigravity (Coding Agent)

---

## 1. MOTIVATION & OBJECTIVES

### The Context:
Misora Editor is an indie desktop editor for Princess Connect! Re:Dive cutscenes and adv scripts (`.unity3d` binary story bundles and `.txt` CSIF scripts). Up to Cycle 1 (S0–S2, S8b-1), the editor operated exclusively on local, user-provided story files.

However, the **Japan (JP) Server** operated by Cygames is the upstream source of truth where all new content, main story chapters, character bond stories, side-story events, and game mechanics originate first.

### The Problem:
Translators and cutscene preservationists face significant friction when trying to edit and localize newly released Japanese cutscenes:
1. Translators must manually obtain, decrypt, unpack, and convert JP story bundles into raw files before Misora Editor can load them.
2. Translators lack a clean way to track which story files are new, which character IDs correspond to which dialogue speakers, and which audio cue clips belong to which voice lines.
3. There is no automated pipeline to diff the raw Japanese script against localized scripts or XUnity Auto Translator (XUAT) translation caches.

### The Goal of Cycle 2:
Design and implement a robust, modular, and legal **Japan Server Datamine Pipeline** inside (or seamlessly connected with) Misora Editor.

---

## 2. KEY TECHNICAL PILLARS TO DEBATE

The Review Board (GPT, Gemini, Qwen) is tasked with debating the following 5 architectural pillars:

### Pillar 1: Datamine Ingestion Vector (Local DMM Cache vs. Remote CDN Fetcher)
- **Option A (Local DMM Client Cache Ingestion — Recommended for V1):**
  * Read directly from the official DMM Games PC client local asset cache, located at:  
    `%USERPROFILE%\AppData\LocalLow\Cygames\PrincessConnectReDive\a\`
  * Reads the user's existing, locally installed game files without sending synthetic network requests to Cygames servers.
  * Zero network ban risk, zero live API sniffing required.
- **Option B (Remote CDN Downloader):**
  * Interacting with Cygames asset CDN manifests (`manifest_assetlist`) to download specific story bundles on demand.
  * *Debate Point:* Does a CDN downloader risk API deprecation, IP throttling, or terms-of-service violations?

### Pillar 2: Master Database Parsing (`master.mdb` / `master.db`)
- The JP game client utilizes an encrypted/compressed SQLite database (`master.mdb`) containing crucial metadata tables:
  * `story_data` (story IDs, title, synopsis, episode hierarchy).
  * `unit_data` / `unit_profile` (character names, IDs, voice actors, unit illustrations).
  * `chara_story_status` / `event_story_data` (unlock requirements, chronological chapters).
- *Debate Points:*
  * How should Misora Editor parse `master.mdb`? (Read-only SQLite query engine with indexed caching).
  * How should character metadata enrich Misora's UI? (Speaker auto-completion, character portraits beside dialogue boxes, auto-populating Box 0 metadata).
  * Memory footprint: The full database can exceed 100MB+; how to avoid startup lag? (Lazy indexed lookups vs. dedicated SQLite worker).

### Pillar 3: Asset Bundle Unpacking & CSIF Conversion
- Story cutscenes are stored as LZ4-compressed Unity AssetBundles (`storydata_XXXXXXX.unity3d`).
- *Debate Points:*
  * Unpacker engine: Enhancing Misora's existing `core/bundle_io.py` (UnityPy-based) vs. high-speed native extraction.
  * Direct-to-CSIF converter: Ingesting raw JP `storydata` and emitting pristine Cutscene Script Interchange Format (`CSIF`) with standard `@@Speaker` headers and sanitized NGUI tags.
  * Character token normalization: Converting literal `{0}` to `{playername}`.

### Pillar 4: Script Diffing & Localization Tracking (JP Raw vs. Localized)
- When a new JP story episode arrives, translators need to know:
  * Exactly what lines are untranslated.
  * Whether an existing story received an upstream modification or bugfix in JP.
- *Debate Points:*
  * Should Misora feature a split-screen or side-by-side **Dual-Language Comparison View** (Raw JP on left, Translated CSIF on right)?
  * Integration with `core/xunity_sync.py`: Auto-generating XUAT translation stubs directly from fresh JP datamine scripts.

### Pillar 5: Voice Audio & CG Media Preview Integration
- Audio is packaged in Criware CRI ADX2 formats (`.acb` / `.awb`).
- *Debate Points:*
  * Should Misora extract or link voice cues (`vo_adv_...`) from `.awb` voice archives so translators can play character audio directly while proofreading?
  * What is the performance impact of audio decoding libraries (e.g., PyCriCodecs / vgmstream) in a lightweight Tkinter app?

---

## 3. NON-NEGOTIABLE SAFETY & ARCHITECTURAL GUARDRAILS

1. **Modular Provider Architecture (Zero Code Sprawl in `misora.py`):**
   - The datamine subsystem must be fully modularized under `core/datamine/` or as a standalone provider module.
   - `misora.py` must only interact with high-level interfaces (e.g., `DatamineProvider.get_story(story_id)`).
2. **Legal & TOS Guardrails (No Hardcoded Decryption Keys):**
   - The repository must NEVER contain hardcoded proprietary decryption keys or copyrighted game binaries.
   - Keys or local game paths must be user-configurable via `misora_config.json` or detected from local registry/DMM client paths.
3. **Preserve Existing Slice Boundaries (S2 Through S7):**
   - Datamine ingestion must NOT interfere with the locked dirty-tracking contracts (`S2`), safe file closing (`S3`), or structural undo (`S4`).
4. **Failing-First Automated Testing:**
   - Any new datamine parser must have automated tests using dummy/stubbed SQLite databases and mock bundles without requiring live game assets in git.

---

## 4. IMMEDIATE ACTION FOR THE REVIEW BOARD (PHASE 0)

Reviewers (**GPT**, **Gemini**, **Qwen**) are requested to formulate their **Phase 0 Independent Research & Audit Dossier** answering:
1. What is the cleanest, safest architecture for Misora Editor to ingest JP story assets and `master.mdb` metadata?
2. Should we prioritize DMM PC local cache reading over remote CDN downloading?
3. How should the datamine roadmap be sliced (e.g., D1: `master.db` reader, D2: Story Bundle unpacker, D3: Dual-Language Diff View)?
