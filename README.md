# Misora Reference: Priconne JP Datamine & Extractor Plugin Project

Welcome to the **Misora Reference** hub. This repository houses curated reverse-engineering engines, decoders, SQLite data-mining tools, and architectural blueprints for **Princess Connect! Re:Dive (Priconne JP)**. It serves as the authoritative reference desk and prototype incubator for **[Misora Editor](https://github.com/ImaterialC/Misora-Editor)**.

---

## 🚀 Active Project: Misora Extractor Plugin (Cycle 2)

**Status:** **PHASE 0 KICKOFF — ACTIVE DEBATE**  
**Active Briefing:** [active_debates/extractor_plugin/01_KICKOFF_BRIEFING_EXTRACTOR_PLUGIN.md](file:///d:/Reference/Misora-Reference/active_debates/extractor_plugin/01_KICKOFF_BRIEFING_EXTRACTOR_PLUGIN.md)  
**Historical Archives:** Previous editor core debates (S0–S2 dirty contracts, UX previews) are permanently preserved in git branch `archive/cycle-1-editor-core`.

### Verified Headless Prototype (`extractor_prototype/`)
A high-speed, zero-intermediate-file 3-pillar extraction engine located in `extractor_prototype/`:
- **Pillar 1 (`local_scanner.py`)**: Local DMM client cache scanner (`%USERPROFILE%\AppData\LocalLow\Cygames\PrincessConnectReDive\a\`) for instant bundle discovery with zero network overhead.
- **Pillar 2 (`story_codec.py`)**: Lossless in-memory `_invert_every_third_byte` ADV decoder converting encrypted bytecode directly into Cutscene Script Interchange Format (CSIF). Benchmark: **0.34 ms** for 50 dialogue lines.
- **Pillar 3 (`db_metadata.py`)**: Read-only SQLite 3 query engine resolving character names (e.g. `118201` $\rightarrow$ *Misora / ミソラ*) and chapter titles from Robo Ninon's deobfuscated `master.db`.
- **Automated Verification**: Run `python -m unittest tests/test_extractor_prototype.py` (9 tests, 100% pass).

---

## 📚 Repository Map & Navigation

```
Misora-Reference/
├── README.md                           # Master project documentation
├── INSTANT_ONBOARDING_PROMPT.md        # Instant briefing for new AI instances (GPT, Gemini, Qwen)
├── extractor_prototype/                # 🚀 Headless Extractor Prototype (3 Pillars)
│   ├── local_scanner.py                # Pillar 1: DMM local cache scanner
│   ├── story_codec.py                  # Pillar 2: In-memory streaming ADV codec (Direct-to-CSIF)
│   ├── db_metadata.py                  # Pillar 3: SQLite master.db speaker & chapter resolver
│   ├── service.py                      # Unified public API service
│   └── __init__.py
├── tests/
│   └── test_extractor_prototype.py     # 9 unit tests & benchmark (< 1ms target)
├── reference_toolchains/               # 🛠️ Curated Reference Reverse-Engineering Suites
│   ├── README.md                       # Master reference hub
│   ├── PROGRAM_LINEAGE_AND_ALIASES.md  # V1/V2/V3 lineage, aliases, and missing files audit
│   ├── EXTRACTOR_PLUGIN_PROPOSAL.md    # Detailed architectural design for Misora Editor
│   ├── community_heritage/
│   │   └── HERITAGE_AND_SOURCES.md     # Robo Ninon master.db, Expugn, and MightyZanark roots
│   ├── v3_kyouka_suite/                # 🟢 ACTIVE GOLDEN REFERENCE (V3 Unified GUI & Engines)
│   ├── v2_modular_tools/               # 🟢 ACTIVE GOLDEN REFERENCE (V2 NewDataMiner & ADV scripts)
│   └── archives/                       # 🧊 Token-protected zip archives for legacy/redundant code
├── active_debates/
│   └── extractor_plugin/               # Active discussion dossiers and review records
└── tools/
    └── secretary.py                    # Secretary Assistant CLI (status, verify-zips)
```

---

## ⚡ Instant AI Onboarding Prompt

> **For the Human User:** Copy and paste the block below into ChatGPT, Claude, Gemini, or Qwen to onboard them instantly onto the Extractor Plugin task:

```plaintext
# HANDOFF & CATCH-UP BRIEFING — MISORA MULTI-AI ENGINEERING BOARD
Date: 2026-11-22 | Target: https://github.com/ImaterialC/Misora-Editor | Reference: https://github.com/ImaterialC/Misora-Reference

You are stepping into the multi-AI review board for Princess Connect! Re:Dive (Priconne JP) reverse engineering and story tooling.

ROLES & DISCIPLINE:
- GPT: Arbiter & lock authority.
- Gemini: Technical reviewer, Tkinter/threading safety auditor.
- Qwen: Precision code & AST integrity checker.
- Antigravity: Coding agent executing local prompts on D:\Misora-Editor.
- User: Product owner.
- Language Rules: Address USER in BAHASA INDONESIA; technical discussion/prompts in ENGLISH.

CURRENT ACTIVE DEBATE: MISORA EXTRACTOR PLUGIN INTEGRATION
We have built and verified a Headless Extractor Prototype in `Misora-Reference/extractor_prototype/`:
- Pillar 1 (LocalScanner): Scans DMM client cache (%USERPROFILE%\AppData\LocalLow\Cygames\PrincessConnectReDive\a\).
- Pillar 2 (StoryCodec): Memory stream decoder using _invert_every_third_byte (0.34 ms benchmark).
- Pillar 3 (DatabaseMetadata): SQLite reader for Robo Ninon's master.db (auto-resolves 118201 -> Misora / ミソラ).

TASK: Deliver your Phase 0 Independent Review & Proposals on integrating this engine into Misora-Editor under plugins/datamine_extractor/:
1. Module placement & public API contract.
2. In-memory bridge directly to core/story_ast.py without intermediate disk files.
3. Threading safety to keep Tkinter GUI responsive during cache scanning.
4. Proposed slice sequence (D1 to D4).

Please confirm you have digested this state and state your readiness in Bahasa Indonesia.
```

---

## 🛠️ CLI Operations (`tools/secretary.py`)

- **Check Active Desk Status**:
  ```bash
  python tools/secretary.py status
  ```
- **Verify Cold Storage Zip Archives**:
  ```bash
  python tools/secretary.py verify-zips
  ```
- **Run Prototype Test Suite**:
  ```bash
  python -m unittest tests/test_extractor_prototype.py
  ```
