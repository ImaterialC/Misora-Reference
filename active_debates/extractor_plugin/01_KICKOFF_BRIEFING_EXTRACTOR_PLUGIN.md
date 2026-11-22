# Kickoff Briefing: Misora Extractor Plugin Integration

**Debate Topic:** Integrating the 3-Pillar Headless Extractor Prototype into `Misora-Editor`  
**Target Codebase:** `https://github.com/ImaterialC/Misora-Editor` (`D:\Misora-Editor`)  
**Reference Codebase:** `https://github.com/ImaterialC/Misora-Reference` (`D:\Reference\Misora-Reference`)  
**Date:** 2026-11-22  
**Status:** **PHASE 0 KICKOFF — ACTIVE DEBATE**

---

## 1. Context & Motivation

Princess Connect! Re:Dive (Priconne JP) is the primary upstream release where new story episodes, characters, and events release first. Cutscene translators and editors using **Misora Editor** currently must extract and unpack `.unity3d` asset bundles manually outside the application.

We have constructed and verified a **Headless Extractor Prototype** in `Misora-Reference/extractor_prototype/` that performs end-to-end extraction and metadata enrichment in **0.34 ms** (300x faster than the 100ms threshold):
1. **Pillar 1 (`local_scanner.py`)**: Local DMM client cache scanner (`%USERPROFILE%\AppData\LocalLow\Cygames\PrincessConnectReDive\a\`) — zero bandwidth, zero ban risk, instant discovery.
2. **Pillar 2 (`story_codec.py`)**: In-memory `BytesIO` direct-to-CSIF converter using lossless `_invert_every_third_byte` byte transformation and FlatBuffer/command table parsing.
3. **Pillar 3 (`db_metadata.py`)**: SQLite 3 metadata resolver querying Robo Ninon's deobfuscated `master.db` (auto-resolving `118201` $\rightarrow$ *Misora / ミソラ* and chapter titles).

Now, our objective is to architect the cleanest, safest integration of this engine into `Misora-Editor` as a dedicated plugin: `plugins/datamine_extractor/`.

---

## 2. Review Board Roles & Invariants

- **Arbitration & Review Board:**
  - **GPT**: Arbiter, deepest inspector, and final lock authority.
  - **Gemini**: Technical reviewer, GUI/Tkinter safety auditor, and sync briefs compiler.
  - **Qwen**: Precision code auditor, AST integrity checker, and bug reproducer.
  - **Antigravity (Google DeepMind)**: Local coding agent executing verified prompts on `D:\Misora-Editor`.
  - **User**: Product owner and relay between AI models.

- **Non-Negotiable Guardrails:**
  1. **Strict Language Discipline**: User dialogue in **Bahasa Indonesia**; all technical documentation, debate dossiers, and code prompts in **English**.
  2. **Zero Code Sprawl in `misora.py`**: The extractor plugin must live entirely in `plugins/datamine_extractor/` or `core/datamine/`. `misora.py` only binds high-level menu items or events.
  3. **Zero Intermediate Disk Files**: Stream directly from memory (`BytesIO`) into `core/story_ast.py`.
  4. **No Hardcoded Decryption Keys**: All paths and configurations must use system environment defaults or `misora_config.json`.
  5. **Failing-First Automated Testing**: Unit tests must accompany every slice.

---

## 3. Debate Slices to Deliberate (D1 to D4)

The board is invited to critique and finalize the slice boundaries for integration into `Misora-Editor`:

- **Slice D1: Core Plugin Infrastructure & Headless Ingestion**
  - Install `plugins/datamine_extractor/` with `LocalScanner` and `StoryCodec`.
  - Connect `StoryCodec.decode_scene_from_bytes()` directly with Misora's `core/story_ast.py` (`StoryAST.from_records()`).
  - Unit tests verifying in-memory roundtrip without launching Tkinter GUI.

- **Slice D2: SQLite `master.db` Metadata Enrichment**
  - Implement read-only `DatabaseMetadata` query worker.
  - Auto-enrich speaker names in `StoryBox` dialog elements.
  - Cache unit mappings in memory.

- **Slice D3: GUI Integration & Import Dialog**
  - Add "Import from Game Cache (Datamine)..." under the File menu.
  - Lightweight modal dialog browsing scanned local chapters with search filter.
  - Background threading so scanning does not block the Tkinter UI thread.

- **Slice D4: BepInEx Collision Prevention & Export**
  - Export clean `.translation.json` patch files validated against `bepinex_guard.py` rules.
