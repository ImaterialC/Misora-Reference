# Reference Toolchains Directory

Welcome to the **Reference Toolchains Hub** in the **Misora Reference** repository. 

This directory contains curated reverse-engineering engines, decoders, data-mining scripts, and architectural blueprints for Princess Connect! Re:Dive (Priconne JP). It is specifically structured to maximize **AI agent token efficiency** while maintaining complete access to historical code and future plugin designs.

---

## 1. Directory Structure & Quick Navigation

```
reference_toolchains/
├── README.md                           # This master documentation hub
├── PROGRAM_LINEAGE_AND_ALIASES.md      # Master alias table, V1/V2/V3 lineage, missing files audit
├── EXTRACTOR_PLUGIN_PROPOSAL.md        # Architectural proposal for Misora Extractor Plugin
├── community_heritage/
│   └── HERITAGE_AND_SOURCES.md         # Documentation on Robo Ninon master.db, Expugn, and MightyZanark
├── v3_kyouka_suite/                    # 🟢 ACTIVE GOLDEN REFERENCE (V3 Unified Suite)
│   ├── Kyouka-Asset-Explorer.py        # Complete desktop exploration GUI
│   ├── Kyouka-Asset-Explorer.bat       # Windows launcher
│   ├── KYOUKA_README.md                # Suite documentation
│   ├── modules/                        # Decoupled core engines
│   │   ├── db_explorer.py              # 998-table SQLite FTS5 search & CAT export
│   │   ├── cdn_bridge.py               # Akamai CDN downloader
│   │   ├── story_codec.py              # Lossless ADV script decoder/encoder
│   │   ├── glossary.py                 # Unit codename resolver
│   │   └── bepinex_guard.py            # BepInEx translation collision detector
│   └── docs/                           # Architecture, codec notes, and database specs
├── v2_modular_tools/                   # 🟢 ACTIVE GOLDEN REFERENCE (V2 Modular Tools)
│   ├── NewDataMiner/                   # 10-module manifest indexer & downloader
│   │   ├── cli.py, config.py, database.py, dataminer.py, db_updater.py,
│   │   ├── downloader.py, extractor.py, manifest_manager.py, models.py, resource_cross_ref.py
│   │   └── README.md
│   ├── conflict_manager.py             # Advanced Tkinter UI for translation conflict detection (56 KB)
│   ├── raw2xuat.py                     # Decompiled ADV JSON to XUAT converter (23.3 KB)
│   ├── xuat2raw.py                     # XUAT patch to raw dialogue decompiler (14.1 KB)
│   ├── advscript.py                    # ADV scene parser & command generator (30.2 KB)
│   ├── advverify.py                    # Static bytecode validator (13.9 KB)
│   └── asset_registry.py               # Local disk asset inventory manager (14.1 KB)
└── archives/                           # 🧊 COLD STORAGE (Token-Protected Zip Archives)
    ├── README_ARCHIVES.md              # Detailed inventory of archived files and checksums
    ├── v1_legacy_prototypes.zip        # Archived V1 legacy tools (e_all.py, old batch files, etc.)
    └── v2_intermediate_toolchain.zip   # Archived V2 intermediate files and legacy PDF chat logs
```

---

## 2. Core Policies for AI Agents & Contributors

### Token Conservation Policy
> [!IMPORTANT]
> **Do NOT decompress files in `archives/` unless explicitly instructed by the user.**
> All redundant, deprecated, and intermediate iterations of data miners and batch files have been safely compressed into `.zip` archives. This prevents AI agents from needlessly scanning thousands of lines of duplicate legacy code and exhausting context tokens.
> 
> The active desk (`v3_kyouka_suite/` and `v2_modular_tools/`) contains the **deduplicated, verified golden copies** of all functional code.

### Database Reference Clarification
> [!NOTE]
> Princess Connect! Re:Dive uses **`master.db` (SQLite 3)**, sourced and maintained automatically via [Robo Ninon](https://roboninon.win/db/download). There is **no `master.mdb`**. See [HERITAGE_AND_SOURCES.md](file:///d:/Reference/Misora-Reference/reference_toolchains/community_heritage/HERITAGE_AND_SOURCES.md) for full schema and heritage details.

---

## 3. High-Priority Documents for Misora Extractor Development

1. **[EXTRACTOR_PLUGIN_PROPOSAL.md](file:///d:/Reference/Misora-Reference/reference_toolchains/EXTRACTOR_PLUGIN_PROPOSAL.md)**:
   Read this first when implementing the extractor plugin inside Misora Editor. It details the **Local Cache First (Tier 1)** scanner, in-memory **Direct-to-CSIF** stream decoding, and **Robo Ninon** metadata enrichment.
2. **[PROGRAM_LINEAGE_AND_ALIASES.md](file:///d:/Reference/Misora-Reference/reference_toolchains/PROGRAM_LINEAGE_AND_ALIASES.md)**:
   Consult this table to trace any script, function, or file name mentioned in legacy documentation or developer chats to its canonical modern counterpart.
3. **[modules/story_codec.py](file:///d:/Reference/Misora-Reference/reference_toolchains/v3_kyouka_suite/modules/story_codec.py)**:
   The reference implementation for the `_invert_every_third_byte` byte transformation and Unity FlatBuffer story deserialization.
