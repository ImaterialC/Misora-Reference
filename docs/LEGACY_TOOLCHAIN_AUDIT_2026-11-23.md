# Legacy Toolchain Audit — 2026-11-23

**Repository:** `ImaterialC/Misora-Reference`  
**Audited paths:** `priconne-asset-extractor-main/` and `Kyouka-Asset-Explorer/`  
**Purpose:** identify lineage, exact duplicates, reusable text/subtitle functions, and safe archival boundaries before starting the Misora Datamine plugin.

## 1. Executive finding

These two directories are not two unrelated products. They are snapshots in the development lineage of the same broader Priconne tool ecosystem:

- `priconne-asset-extractor-main/` contains the NewDataMiner toolchain, a separate ADV/XUAT text workflow, manifest indexes, database/update logic, and movie/audio extraction helpers.
- `Kyouka-Asset-Explorer/` contains a GUI/TUI-style all-in-one explorer, a reusable SQLite text-search module, a CDN bridge, an ADV story codec, a movie-subtitle codec path, and older monolithic tools under `OLD/` and `OLD2/`.
- `reference_toolchains/v2_modular_tools/` and `reference_toolchains/v3_kyouka_suite/` already preserve large portions of those implementations.

**Recommendation:** do not delete either source directory yet. First preserve a checksummed ZIP snapshot, then mark exact copies as `duplicate-reference` and differing implementations as `historical-variant` or `candidate-source`.

## 2. Repository snapshot counts

At the time of the audit, GitHub's `main` tree contained:

| Path | Tracked files |
|---|---:|
| `priconne-asset-extractor-main/` | 96 |
| `Kyouka-Asset-Explorer/` | 35 |
| Combined | 131 |

These are Git-tracked file counts, not local working-tree counts. The audit did not clone or execute every legacy tool.

## 3. Exact duplicate findings

Git blob identity means the file content is exactly the same in the inspected commit. A matching filename alone does not prove duplication.

### 3.1 Duplicates already inside the two audited folders

Six exact-duplicate groups were found among the two directories (14 file entries including the repeated members):

| Exact duplicate content | Locations |
|---|---|
| `advverify.py` | `Kyouka-Asset-Explorer/OLD2/advverify.py`; `priconne-asset-extractor-main/priconne-adv-tools/advverify.py` |
| `priconne_adv.bat` | `Kyouka-Asset-Explorer/OLD2/priconne_adv.bat`; `priconne-asset-extractor-main/priconne-adv-tools/priconne_adv.bat` |
| Empty `.gitkeep` | `Kyouka-Asset-Explorer/exports/`, `input/`, `output/`, `text/` |
| `conflict_manager.bat` | `priconne-asset-extractor-main/conflict_manager.bat`; `priconne-asset-extractor-main/priconne-adv-tools/conflict_manager.bat` |
| `raw2xuat.py` | `priconne-asset-extractor-main/raw2xuat.py`; `priconne-asset-extractor-main/priconne-adv-tools/raw2xuat.py` |
| `xuat2raw.py` | `priconne-asset-extractor-main/xuat2raw.py`; `priconne-asset-extractor-main/priconne-adv-tools/xuat2raw.py` |

These are safe duplicate candidates for a future archival manifest, but keep at least one canonical copy and record the historical path aliases. Do not remove them in this reset task.

### 3.2 Exact copies already preserved elsewhere in Misora-Reference

The inspected tree also showed identical Git blobs across the legacy folders and the curated `reference_toolchains/` folders:

- `Kyouka-Asset-Explorer/Kyouka-Asset-Explorer.py`, its `.bat` launcher, README, architecture docs, glossary/tutorial docs, and the six `modules/` files match the corresponding Kyouka V3 files already in `reference_toolchains/v3_kyouka_suite/`.
- All 11 files in `priconne-asset-extractor-main/NewDataMiner/` match the corresponding `reference_toolchains/v2_modular_tools/NewDataMiner/` files.
- `priconne-asset-extractor-main/conflict_manager.py` matches the V2 `conflict_manager.py`.
- `Kyouka-Asset-Explorer/OLD2/advscript.py`, `advverify.py`, and `asset_registry.py` match the corresponding V2 references.
- `priconne-asset-extractor-main/priconne-adv-tools/advverify.py`, `raw2xuat.py`, and `xuat2raw.py` also have V2 copies.

**Meaning:** V2/V3 already preserve the canonical identical copies. However, the old directories remain useful for chronology, old launchers, folder layouts, and variants that do not match the curated copies.

## 4. Important non-identical variants — retain for comparison

Do not group the following as exact duplicates:

- `priconne-asset-extractor-main/priconne-adv-tools/advscript.py` differs from the V2 `advscript.py` and from the Kyouka `OLD2/advscript.py`.
- `priconne-asset-extractor-main/priconne-adv-tools/conflict_manager.py` differs from the V2/root `conflict_manager.py`.
- `Kyouka-Asset-Explorer/OLD2/priconne_tool.py` is a large monolithic legacy workflow and is not represented by the same SHA as a current modular file in the curated tree.
- `Kyouka-Asset-Explorer/OLD/browse_master_db.py` is a separate legacy database browser.
- The many `manifest/*` files and `movie2manifest`/`soundmanifest` indexes are data catalogues, not source-code duplicates. Keep provenance/version metadata when archiving them.

These are potential sources for recovering behavior, but they must be read and tested before any part is copied into Misora Editor.

## 5. What is reusable for the requested Datamine scope

### A. Master database text discovery

Primary reference: `Kyouka-Asset-Explorer/modules/db_explorer.py` and the matching V3 copy.

Observed capabilities in the source:
- SQLite opened with URI `mode=ro` for querying.
- Dynamic discovery of tables and text columns.
- Search across text-bearing columns.
- Category-oriented export of text data.
- A separate reinjection feature writes to a new patched database; that mutation capability should be **out of scope** for the first Misora plugin milestone.

### B. ADV / story text from Unity bundles

Primary reference: `Kyouka-Asset-Explorer/modules/story_codec.py` and its V3 copy.

Observed capabilities:
- Locates a `TextAsset` whose name contains `story`.
- Decodes command records into a structured, translator-friendly `.txt` format.
- Uses the Priconne argument transform documented in code (Base64 plus bit inversion on every third byte).
- Rebuilds story bytes and compares the reconstructed payload for verification.

The separate `priconne-adv-tools/advscript.py`, `xuat2raw.py`, and `raw2xuat.py` are useful for understanding the older XUAT/translation-sheet workflow, but they should not automatically be copied into the new plugin.

### C. Movie (MV) subtitle records

Primary reference: `Kyouka-Asset-Explorer/modules/story_codec.py`.

Observed implementation:
- Scans Unity `MonoBehaviour` objects and looks for a `recordList` whose first element is a dictionary containing `text`.
- Exports records to JSON with `id`, `startTime`, `endTime`, and `text`.
- Imports translated JSON and requires the same number of subtitle records as the original.
- Writes the updated typetree back into a `.unity3d` bundle.

**Critical verification gap:** the subtitle repack branch currently writes the bundle but does not reopen the generated bundle and compare the serialized subtitle records. The story branch has a re-read verification path; the subtitle branch does not. The old Kyouka repository has no dedicated subtitle round-trip test suite in the tracked tree. Treat this as an unverified feature until tested against a real, legally usable fixture and a mock fixture.

**Important distinction:** `NewDataMiner/extractor.py` extracts Unity `TextAsset` files and can convert `.usm` movie files into `.mp4` using UsmToolkit. It does not, in the inspected implementation, traverse Unity `MonoBehaviour.recordList` to export subtitle JSON. The subtitle feature documented in Kyouka belongs to the subtitle-bearing Unity bundle, not automatically to the `.usm` video file itself.

### D. Manifest and targeted discovery

Primary reference: `priconne-asset-extractor-main/NewDataMiner/manifest_manager.py`, `models.py`, and `resource_cross_ref.py`.

Observed capabilities:
- Parses local asset manifests.
- Categorizes story, movie, sound, unit, and other assets.
- Searches locally loaded manifests without downloading first.
- Provides a `movie2manifest` path/category for movie assets and a separate story asset category.

The `movie2manifest` catalogue should be used to investigate movie/video discovery, while the subtitle-bearing `.unity3d` bundle mapping must be verified independently. Do not assume the movie and subtitle records share a filename or numeric ID without evidence.

## 6. Proposed keep / reference / park classification

| Component | Proposed status | Reason |
|---|---|---|
| Kyouka `modules/db_explorer.py` | `candidate-source` | Closest existing text-datamine implementation |
| Kyouka `modules/story_codec.py` story path | `candidate-source` | Existing story extraction/repack path and byte checks |
| Kyouka `modules/story_codec.py` subtitle path | `candidate-source-unverified` | Relevant MV subtitle logic, but repack lacks read-back verification/tests |
| NewDataMiner manifest manager and cross-reference | `candidate-source` | Useful offline discovery and targeted search |
| NewDataMiner `extractor.py` | `reference-only` for first scope | Broad media extraction; does not currently extract subtitle MonoBehaviour records |
| Old `priconne_tool.py` monolith | `historical-reference` | Preserve until feature parity and dependency review are complete |
| OLD/OLD2 wrappers and scripts | `historical-reference` | May encode path assumptions and workflow details |
| Exact copies in V2/V3 | `duplicate-reference` | Canonical byte-identical content already exists elsewhere |
| Manifests | `reference-data` | Large catalogues; retain provenance and versions |

## 7. Safe archival policy

1. Create a checksummed ZIP snapshot of each legacy directory before any physical cleanup.
2. Preserve the original relative folder structure inside each ZIP.
3. Add a file manifest containing relative path, size, and SHA-256.
4. Do not rename original `.py`, `.bat`, or data files in place. Legacy launchers often rely on current working directory and relative filenames.
5. Use human-readable canonical names for the ZIPs and a catalogue for display names/aliases.
6. Verify each ZIP CRC and every member's SHA-256 before considering the snapshot complete.
7. Only after snapshot verification, mark duplicate copies in the catalogue. Do not delete source folders during this task.

## 8. Questions that require local evidence before plugin design is locked

- Which currently available JP bundle contains the real MV subtitle `MonoBehaviour.recordList`?
- Can a single `.unity3d` bundle contain more than one candidate subtitle `MonoBehaviour`? Current code picks one candidate without reporting ambiguity.
- Does each record have fields other than `startTime`, `endTime`, and `text` that must remain intact?
- Is the record count stable for translated output, and should edits ever be allowed to add/remove subtitle records?
- How are `movie2manifest` entries linked to the subtitle bundle's manifest entry? Same ID, relation table, or another naming convention?
- Does the subtitle JSON export preserve the exact encoding/line-ending policy required by translators?
- What is the expected behavior when `master.db` is missing, outdated, or has a schema different from the reference database?

## 9. Audit limits

This is a static GitHub-tree/source review, not a runtime certification. I did not download or execute the legacy programs, did not access your local working tree, did not verify current Cygames server endpoints, and did not test against a live game bundle. Any `PASS` claims in historical `PROGRESS.md` remain historical claims until rerun in a controlled environment.
