# Reference Toolchains — Cold Storage Archive Manifest

This directory preserves compressed `.zip` archives of Generation 1 legacy prototypes, obsolete batch scripts, redundant intermediate test harnesses, and historical reports.

> **Token Conservation Rule:** These files are compressed to prevent AI agents from burning tokens reading obsolete or duplicated code. Only the uncompressed golden reference modules in `v3_kyouka_suite/` and `v2_modular_tools/` should be actively inspected.

---

## 1. `v1_legacy_prototypes.zip`
- **File Size:** ~160 KB (71 files)
- **Source Origins:** `D:\priconne_backup_archive\OldDataMiner`, `V1-V2`, and `src/`
- **Contents:**
  * `OldDataMiner/`: Monolithic category scripts (`e_all.py`, `e_story.py`, `e_baner.py`, `e_comic.py`, `e_event.py`, `e_gacha.py`, `e_movie.py`, `e_unit.py`) and legacy batch runners (`DataMinerv2.bat`, `Dataminerv3.bat`).
  * `V1-V2/`: Prototype script extractor `priconne_tool(old).py` and early `priconne_tool.py`.
  * `src/`: Early open-source modular prototype (`asset_bundle.py`, `mdb.py`, `manifest.py`).
  * Batch scripts: `1_extract.bat`, `2_repack.bat`, `3_autotranslate.bat`.

---

## 2. `v2_intermediate_toolchain.zip`
- **File Size:** ~2,033 KB (48 files)
- **Source Origins:** `D:\priconne-asset-extractor-main` and `D:\Kyouka-Asset-Explorer\OLD*`
- **Contents:**
  * Duplicate subfolder `priconne-adv-tools/`.
  * Unit test suite `tests/` (`test_asset_registry.py`, `test_database_integration.py`, `test_new_dataminer.py`, etc.).
  * Historical project planning and progress logs (`DECISIONS.md`, `PROGRESS.md`, `PROJECT_PLAN.md`).
  * `kyouka_legacy/`: Early Kyouka refactor snapshots (`OLD/browse_master_db.py`, `OLD2/priconne_tool.py`).
  * `historical_chat_artifacts/grok_report.pdf`: Historical Grok audit report recovered from `Reference Files.zip`.
