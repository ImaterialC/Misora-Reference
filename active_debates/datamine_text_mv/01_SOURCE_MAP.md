# Datamine Text + MV Subtitle — Source Map

Static source map from the 2026-11-23 GitHub review. All statements below must be rechecked against the current local checkout before implementation.

## Candidate file map

| Function | File | What the code appears to do | Main risk / next check |
|---|---|---|---|
| DB text search | `Kyouka-Asset-Explorer/modules/db_explorer.py` | Discovers text-bearing SQLite tables/columns, searches text, exports categories; uses read-only SQLite URI | Verify schema against actual `master.db`; keep reinjection out of initial plugin |
| ADV/story codec | `Kyouka-Asset-Explorer/modules/story_codec.py` | Parses story TextAsset binary records, exports `.txt`, builds records and checks byte round-trip | Verify object selection uniqueness and unknown/empty argument behavior |
| MV subtitle codec | `Kyouka-Asset-Explorer/modules/story_codec.py` | Finds MonoBehaviour `recordList`, exports JSON, updates text/timing and writes bundle | No subtitle read-back verification; no tracked subtitle tests; verify actual schema/unknown fields |
| Asset manifest search | `priconne-asset-extractor-main/NewDataMiner/manifest_manager.py` | Parses local manifests, classifies story/movie/sound/etc., supports targeted search | Verify manifest version/format and asset-to-subtitle mapping |
| Asset data model | `priconne-asset-extractor-main/NewDataMiner/models.py` | Defines `ManifestEntry`, categories and download scope | Confirm ID/path identity contract |
| DB/resource cross-reference | `priconne-asset-extractor-main/NewDataMiner/resource_cross_ref.py` | Connects DB story/unit records to manifest entries | Heuristic naming may miss edge cases; verify against fixtures |
| General asset extractor | `priconne-asset-extractor-main/NewDataMiner/extractor.py` | TextAsset extraction and `.usm` to `.mp4` conversion; also textures/audio | Does not show MonoBehaviour subtitle extraction; too broad for first plugin |
| Legacy ADV workflow | `priconne-asset-extractor-main/priconne-adv-tools/` | Older raw/work/trans sheets, XUAT conversion, validation, conflict tools | Batch launchers use relative paths; don't rename files in place |
| Legacy monolith | `Kyouka-Asset-Explorer/OLD2/priconne_tool.py` | Old all-in-one CLI/extractor/repacker workflow | Read-only historical reference; do not copy wholesale |

## Exact-identical curated copies

- Kyouka root app/docs/modules largely match `reference_toolchains/v3_kyouka_suite/` byte-for-byte.
- NewDataMiner package matches `reference_toolchains/v2_modular_tools/NewDataMiner/` byte-for-byte.
- A subset of legacy ADV/conflict scripts match V2 references exactly.

Use the SHA-256 inventory tool for the live working-tree report; Git blob identity in the audit is tied to the inspected Git commit.

## Critical separation: movie video versus subtitle data

- `movie2manifest` is parsed by NewDataMiner as movie assets, generally `.usm` files from the Movie pool.
- Kyouka's subtitle codec searches a Unity bundle for a `MonoBehaviour` with `recordList` entries containing `text`.
- The generic NewDataMiner Unity extractor shown in the source handles `Texture2D`, `Sprite`, and `TextAsset`, not this subtitle MonoBehaviour path.

Therefore, first prove the actual movie-to-subtitle bundle relationship from a sample and manifests. Do not assume the `.usm` contains the editable subtitle strings.
