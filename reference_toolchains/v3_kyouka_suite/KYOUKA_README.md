# Kyouka Asset Explorer

An open-source, all-in-one **datamining, full-text search, developer codename glossary, JP CDN bridge, and localization suite** for *Princess Connect! Re:Dive*.

Built for international fan translation teams who want a clean, zero-clutter workflow to find **any** text visible in-game, understand Cygames' internal asset names, export translation sheets, and repack translated scripts safely.

---

## Key Features

- **Global Full-Text Search (`master.db`)** — Type any Japanese or English text seen on screen to scan **every text column across every table** in `master.db` simultaneously.
- **Auto-Categorized Folder Exports** — Automatically classifies hundreds of SQLite tables into 10 intuitive folders (`01_story_metadata`, `03_homescreen_dialogue`, `04_guildhouse`, `05_units_and_profiles`, `06_skills_and_combat`, `07_monsters_and_enemies`, `08_ui_quests_and_system`, etc.).
- **Translator-Friendly Formats** — Exports **Excel-ready CSV (UTF-8 BOM)** with paired `*_translation` columns and **CAT-ready `.translation.json`** with unique composite keys (`table:pk:column`).
- **Safe Database Re-Injector** — Writes your completed JSON translations into `output/master_patched.db` without ever modifying your original `master.db`.
- **Developer Codename Glossary & ID Decoder** — Decodes Cygames' internal codenames (`hatsune`, `shiori`, `room`, `storydata`, `tdf`, `er_message`) and 6-/7-digit Unit & Story IDs.
- **Japanese Server CDN Bridge** — Downloads story & subtitle `.unity3d` bundles directly from Cygames' Akamai pool (`prd-priconne-redive.akamaized.net`) with MD5 verification and optional **BepInEx `RedirectedResources`** duplicate checks.
- **Standalone Lossless Story Codec** — Extracts and repacks `.unity3d` visual novel scripts (lossless v2.1 `.txt` with byte-exact round-trip verification) and anime cutscene subtitles (`.json`).

---

## Requirements

- **Python 3.10 – 3.14**
- **Core features (`master.db` search, export, re-inject, glossary, JP CDN downloader):** Zero external packages required (Python Standard Library only).
- **Optional (`.unity3d` story/subtitle extraction & repacking):**
  ```bash
  pip install -r requirements.txt
  ```

---

## Quick Start

1. **Place your decrypted `master.db`** (e.g., from `roboninon.win/db/download`) inside the `Kyouka-Asset-Explorer/` folder next to `Kyouka-Asset-Explorer.py`.
2. **Launch the interactive menu:**
   - **Windows:** Double-click `Kyouka-Asset-Explorer.bat`
   - **Terminal / Linux / macOS:**
     ```bash
     python Kyouka-Asset-Explorer.py
     ```
3. **Optional — Enable BepInEx duplicate checking:**
   ```bash
   python Kyouka-Asset-Explorer.py --bepinex "C:\Path\To\BepInEx"
   ```

---

## CLI Usage Examples

```bash
# Search any in-game text across the entire master.db
python Kyouka-Asset-Explorer.py search "コボルト"

# Export a specific localization category folder
python Kyouka-Asset-Explorer.py export-category 07_monsters_and_enemies

# Dump ALL text-bearing tables organized into category folders
python Kyouka-Asset-Explorer.py export-all

# Generate Story ID -> JP CDN AssetBundle mapping index
python Kyouka-Asset-Explorer.py export-story-index

# Apply completed .translation.json files to output/master_patched.db
python Kyouka-Asset-Explorer.py reinject-db

# Look up a Cygames developer codename
python Kyouka-Asset-Explorer.py glossary hatsune

# Decode a cryptic CDN asset path or ID
python Kyouka-Asset-Explorer.py decode a/storydata_storydata_1058001.unity3d

# Batch extract / repack local .unity3d story & subtitle bundles
python Kyouka-Asset-Explorer.py extract-bundles
python Kyouka-Asset-Explorer.py repack-bundles
```

---

## Repository Structure

```text
Kyouka-Asset-Explorer/
├── Kyouka-Asset-Explorer.py      # Main interactive TUI & CLI entry point
├── Kyouka-Asset-Explorer.bat     # Windows 1-click launcher
├── modules/
│   ├── db_explorer.py            # SQLite global search, category dumper, & DB patcher
│   ├── glossary.py               # Developer codename glossary & ID decoder
│   ├── cdn_bridge.py             # Official JP CDN pool downloader & manifest parser
│   ├── story_codec.py            # Lossless ADV story (.txt) & subtitle (.json) codec
│   └── bepinex_guard.py          # BepInEx RedirectedResources duplicate checker
├── docs/
│   ├── TUTORIAL_EN.md            # Full step-by-step tutorial (English)
│   ├── TUTORIAL_ID.md            # Panduan lengkap Bahasa Indonesia
│   ├── DEVELOPER_GLOSSARY.md     # Complete Cygames codename & ID cheat sheet
│   └── ARCHITECTURE.md           # Technical format & CDN architecture guide
├── manifests/                    # Place optional JP manifest CSV files here
├── input/                        # Raw .unity3d bundles (manual or JP CDN downloaded)
├── text/                         # Extracted v2 .txt story scripts & .json subtitles
├── output/                       # Repacked .unity3d bundles & master_patched.db
└── exports/                      # Exported master.db CSV & Translation JSON folders
```

---

## Documentation

- [English Complete Tutorial](docs/TUTORIAL_EN.md)
- [Panduan Lengkap Bahasa Indonesia](docs/TUTORIAL_ID.md)
- [Cygames Developer Codename Glossary](docs/DEVELOPER_GLOSSARY.md)
- [Technical Architecture & Binary Specs](docs/ARCHITECTURE.md)

---

## Legal Notice

This repository contains **only open-source localization tooling**. It does **not** distribute copyrighted game binaries, `master.db` files, or Cygames assets. Users must supply their own decrypted database and assets.

Licensed under the [MIT License](LICENSE).
