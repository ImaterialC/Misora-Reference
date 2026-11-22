# Program Lineage, Aliases & Missing Files Audit

This document serves as the master registry mapping the evolutionary lineage of reverse-engineering and data-mining programs across three generations (**V1**, **V2**, and **V3**). It defines canonical aliases, functional domains, cryptographic hashes, and documents anomalies/missing files detected during repository curation.

---

## 1. Generation Breakdown: V1 vs V2 vs V3

| Generation | Architecture Style | Core Scope | Storage Status | AI Token Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **V1: Legacy Prototypes** | Monolithic scripts (`e_*.py`), batch wrappers (`.bat`), unversioned utilities. | Blind asset bundle dumping, full-game download without scoping, raw texture ripping. | **Archived** in `v1_legacy_prototypes.zip` | Compressed. Kept off active desk to prevent token bloat. |
| **V2: Modular ADV Tools** | Modular package (`NewDataMiner`), standalone Tkinter UIs, XUAT translation bridges. | 49-category manifest indexing, Robo Ninon HEAD updater, BepInEx duplicate detector, XUAT JSON/Raw bidirectional converters. | **Selective Active Desk** (`v2_modular_tools/` active; redundant archived in `v2_intermediate_toolchain.zip`) | Only essential, deduplicated golden modules remain uncompressed. |
| **V3: Kyouka Suite** | Modern unified GUI (`Kyouka-Asset-Explorer.py`), decoupled `modules/` architecture. | 998-table SQLite FTS5 search, CAT translation exporter, DB re-injector, Akamai CDN bridge, lossless ADV cutscene codec (`_invert_every_third_byte`). | **Primary Active Reference** (`v3_kyouka_suite/`) | Fully uncompressed, indexed, and available for AI agent inspection. |

---

## 2. Functional Domains Taxonomy

Every tool and script in this registry is classified under one or more functional domains:
- **Domain A (Story Codec & Scene Scripting)**: Unpacks, decodes, edits, and re-encodes Unity ADV cutscene scripts (`.unity3d`, FlatBuffers, XOR byte transformations).
- **Domain B (Translation & XUAT Interop)**: Manages BepInEx XUAT translation files (`.translation.json`, `.txt`), prevents asset collision, and performs bidirectional mapping.
- **Domain C (Database Mining & Metadata)**: Interrogates, searches, and extracts narrative/unit metadata from SQLite `master.db`.
- **Domain D (Media & Texture Extraction)**: Converts Unity texture atlases, sprites, audio cues (`.acb`/`.awb`), and movie files (`.usm`).
- **Domain E (CDN Downloader & Manifest Indexing)**: Downloads game assets directly from CyGames/Akamai CDN using manifest parsing and hash tables.

---

## 3. Comprehensive Master Alias Registry

| Original Path / Script Name | Canonical Alias | Gen | Domain | Size | MD5 Hash | Status / Location | Role & Architectural Function |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| `Kyouka-Asset-Explorer/Kyouka-Asset-Explorer.py` | `kyouka_gui_main` | **V3** | A,B,C,E | 41.5 KB | `a9069d27195b0c954e38e1e793e2efd9` | Active (`v3_kyouka_suite/`) | Unified PyQt/Tkinter exploration suite coordinating all modular sub-engines. |
| `Kyouka-Asset-Explorer/modules/db_explorer.py` | `kyouka_db_explorer` | **V3** | C | 19.3 KB | `7ad553094ea511c5e408ec210fecdbb8` | Active (`v3_kyouka_suite/modules/`) | Full-text search engine across all 998 tables in `master.db` with CAT & CSV export. |
| `Kyouka-Asset-Explorer/modules/cdn_bridge.py` | `kyouka_cdn_bridge` | **V3** | E | 10.7 KB | `4f31cfa7541604cf64239845dd50cb25` | Active (`v3_kyouka_suite/modules/`) | High-speed Akamai CDN downloader with scoped bundle fetching and local cache bypass. |
| `Kyouka-Asset-Explorer/modules/story_codec.py` | `kyouka_story_codec` | **V3** | A | 13.9 KB | `714c1143c0c057639f72ae0b0f79db77` | Active (`v3_kyouka_suite/modules/`) | Lossless ADV script decoder using `_invert_every_third_byte` algorithm and FlatBuffer unpacking. |
| `Kyouka-Asset-Explorer/modules/glossary.py` | `kyouka_glossary` | **V3** | C | 6.7 KB | `c2e177b96e57aa36f3223069147eb8e2` | Active (`v3_kyouka_suite/modules/`) | Internal unit codename resolver (maps internal IDs like `105801` to display names). |
| `Kyouka-Asset-Explorer/modules/bepinex_guard.py` | `kyouka_bepinex_guard` | **V3** | B | 6.3 KB | `432243d489b52a1ba763ec78e47da6b9` | Active (`v3_kyouka_suite/modules/`) | Conflict prevention engine verifying that translation keys do not collide with engine assets. |
| `priconne-asset-extractor-main/NewDataMiner/` | `v2_new_data_miner` | **V2** | C,E | 96.0 KB (tot) | *(Multiple)* | Active (`v2_modular_tools/NewDataMiner/`) | 10-module manifest indexer with Robo Ninon HEAD updater and selective bundle downloaders. |
| `priconne-asset-extractor-main/conflict_manager.py` | `v2_conflict_manager` | **V2** | B | 56.0 KB | `ee2cfddda3e1dfb9ba8ff030df1b802d` | Active (`v2_modular_tools/`) | Advanced Tkinter UI for detecting translation overrides and regex collision rules. |
| `priconne-asset-extractor-main/raw2xuat.py` | `v2_raw_to_xuat` | **V2** | B,A | 23.3 KB | `82b4f91e9ec9033e680a6c0ea4b47eb1` | Active (`v2_modular_tools/`) | Compiles decompiled ADV narrative JSON directly into BepInEx XUAT translation format. |
| `priconne-asset-extractor-main/xuat2raw.py` | `v2_xuat_to_raw` | **V2** | B,A | 14.1 KB | `674ec25078519fc6368d5a23fc26ea3d` | Active (`v2_modular_tools/`) | Decompiles BepInEx XUAT patch strings back into raw dialogue text for scene re-encoding. |
| `priconne-asset-extractor-main/advscript.py` | `v2_adv_script_engine` | **V2** | A | 30.2 KB | `821f0ce53baae23769c02506e5da59f7` | Active (`v2_modular_tools/`) | Core scene parser generating command lists and text arrays from story asset bundles. |
| `priconne-asset-extractor-main/advverify.py` | `v2_adv_verifier` | **V2** | A | 13.9 KB | `7ef7a6279f6e626e2ef30a6ba88fbb69` | Active (`v2_modular_tools/`) | Static validator checking story bytecode integrity against structural schema limits. |
| `priconne-asset-extractor-main/asset_registry.py` | `v2_asset_registry` | **V2** | B,E | 14.1 KB | `51061972f77839fa76a267b2d29486c8` | Active (`v2_modular_tools/`) | Local disk asset inventory manager cataloging cached bundles and detecting duplicates. |
| `priconne_backup_archive/OldDataMiner/` | `v1_old_data_miner` | **V1** | C,E | 60.5 KB (tot) | *(Multiple)* | Archived (`v1_legacy_prototypes.zip`) | Monolithic procedural scripts (`e_all.py`, `e_story.py`, `e_unit.py`). Superseeded by V2. |
| `priconne_backup_archive/priconne_tool(old).py` | `v1_priconne_tool` | **V1** | A,D | 22.4 KB | `04b8b5fa4ee176b6b7a2d4b52b2f6ef3` | Archived (`v1_legacy_prototypes.zip`) | Early single-file extractor utilizing basic UnityPy loops. Superseeded by `story_codec.py`. |
| `priconne_backup_archive/1_extract.bat` | `v1_batch_extract` | **V1** | A,E | 0.8 KB | `4f387588e404b967e89fe83d1c9ef001` | Archived (`v1_legacy_prototypes.zip`) | Hardcoded Windows CMD pipeline script for asset unpacking. Superseeded by Python CLI. |
| `priconne_backup_archive/2_repack.bat` | `v1_batch_repack` | **V1** | A | 0.7 KB | `cc5f08836ecda6a9e14a1e531818a7a0` | Archived (`v1_legacy_prototypes.zip`) | Hardcoded Windows CMD pipeline script for asset rebuilding. Superseeded by Python CLI. |
| `priconne_backup_archive/3_autotranslate.bat` | `v1_batch_autotranslate` | **V1** | B | 0.9 KB | `1d3c0130db99df7378d38eef6551b3d6` | Archived (`v1_legacy_prototypes.zip`) | Unbuffered Google Translate batch call script. Deprecated due to high error rate. |
| `priconne-asset-extractor-main/Chat history/` | `v2_chat_reference_docs` | **V2** | Docs | 2.0 MB | *(Multiple)* | Archived (`v2_intermediate_toolchain.zip`) | Legacy developer prompt logs, troubleshooting transcripts, and `grok_report.pdf`. |

---

## 4. Missing Files & Repository Anomalies Audit

During the forensic audit across `priconne_backup_archive`, `priconne-asset-extractor-main`, and `Kyouka-Asset-Explorer`, the following critical discrepancies and missing files were identified and cataloged:

### 1. The Disappearing `master.db` Anomaly
- **Finding**: In both `D:\priconne_backup_archive` and `D:\priconne-asset-extractor-main`, the primary SQLite database `master.db` **did not exist**. Only orphaned write-ahead logs (`master.db-shm` and `master.db-wal`) remained.
- **Resolution**: The complete, functional `master.db` (51.4 MB, MD5: `de141a91138d3b5342dd26bb7f5b14ad`) was recovered exclusively from `D:\Kyouka-Asset-Explorer\master.db`. 
- **Operational Rule**: AI agents running local tests must reference `D:\Kyouka-Asset-Explorer\master.db` or obtain a fresh sync from `https://roboninon.win/db/download`.

### 2. Empty `misora/` Directory
- **Finding**: `D:\priconne-asset-extractor-main\misora` existed as an empty directory containing 0 files.
- **Cause**: This was an uninitialized output stub intended to receive filtered Misora cutscene scripts and character assets before development pivoted to Kyouka Asset Explorer.
- **Resolution**: Kept out of the active desk; clean plugin architecture defined in `EXTRACTOR_PLUGIN_PROPOSAL.md`.

### 3. Unextracted PDF Report in Backup Zip
- **Finding**: A 2.0 MB technical report (`grok_report.pdf`) was buried inside `Reference Files.zip/Chat history/` and was missing from the extracted root directory.
- **Resolution**: Extracted and safely preserved inside `reference_toolchains/archives/v2_intermediate_toolchain.zip` under `Chat history/grok_report.pdf`.

### 4. Revision Divergence in V2 Root Files
- **Finding**: Two conflicting versions of `conflict_manager.py` (56.0 KB vs 55.8 KB) and `advscript.py` (30.2 KB vs 29.7 KB) were identified between `priconne-asset-extractor-main` and `priconne_backup_archive`.
- **Resolution**: Full AST differential analysis verified that the 56.0 KB (`ee2cfddd...`) and 30.2 KB (`821f0ce5...`) files in `priconne-asset-extractor-main` contained the latest bug fixes for Unicode regex escaping. These were promoted to `reference_toolchains/v2_modular_tools/`.
