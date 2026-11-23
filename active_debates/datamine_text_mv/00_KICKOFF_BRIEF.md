# MISORA DATAMINE PLUGIN — KICKOFF BRIEF

**Project:** Misora Editor  
**Reference repository:** Misora-Reference  
**Target:** a focused, read-only-first Datamine plugin for game text and MV subtitles  
**Status:** RESET / PHASE 0 — SOURCE AUDIT AND REQUIREMENTS REVIEW  
**Decision owner:** User (Product Owner)  
**Implementation agent:** Antigravity, only after an approved execution brief

## 1. Mission

Design and eventually integrate a dedicated Datamine feature into Misora Editor that discovers, searches, extracts, previews, exports, and safely repacks **textual game data** and **movie/cutscene subtitle records** from Princess Connect! Re:Dive JP assets.

The plugin must be a focused data-mining workflow, not a general-purpose asset browser. It must not grow into a full image, texture, Spine, audio, or video editor during the first milestone.

## 2. In-scope data domains

### A. Text datamine

Investigate and design support for:

1. `master.db` text-bearing SQLite tables: story titles/subtitles, units/profiles, UI/system text, glossary, skills, homescreen dialogue, guildhouse dialogue, and other text-bearing tables discovered dynamically.
2. Unity `TextAsset` content, including raw text/configuration payloads where relevant.
3. ADV story scripts stored in story Unity bundles and represented by the existing lossless `.txt` interchange format.
4. Manifest-backed discovery: query local manifests first, show exact match/path/category/size, and only download when the user explicitly requests it.

### B. MV / movie subtitle datamine

Investigate support for subtitle-bearing Unity bundles whose `MonoBehaviour` data exposes a `recordList` of timed text records.

The existing Kyouka codec suggests records containing `startTime`, `endTime`, and `text`. It exports JSON and requires the translated record count to match the original. This format and schema must be verified with real and synthetic fixtures before being treated as stable.

Movie/video files (`.usm`) and subtitle-bearing Unity bundles must be treated as separate asset types until a verified ID/path relationship proves otherwise. `movie2manifest` can help locate video resources; it does not by itself prove where subtitle records live.

## 3. Explicitly out of scope for the first release

- Texture, Sprite, icon, background, Spine, and 3D model extraction/editing.
- Audio/music extraction or conversion.
- USM-to-MP4 conversion and video playback UI, unless separately approved later.
- Downloading all manifests/assets blindly or running a full mirror of the CDN.
- Translating content automatically or rewriting XUAT dictionaries as an implicit side effect.
- Modifying the user's original `master.db`.
- Automatically deploying patched assets into BepInEx `RedirectedResources`.
- Refactoring the whole legacy toolchain before the actual plugin requirements are known.

## 4. Repository authority and source order

Read in this order:

1. `AGENTS.md` — current repository guardrails.
2. `README.md` and the active debate documents — repository purpose and current decision state.
3. `docs/LEGACY_TOOLCHAIN_AUDIT_2026-11-23.md` — static inventory and source lineage findings.
4. `reference_toolchains/v2_modular_tools/` and `reference_toolchains/v3_kyouka_suite/` — curated reference implementations.
5. `priconne-asset-extractor-main/` and `Kyouka-Asset-Explorer/` — preserved historical snapshots; inspect before reuse.
6. `Misora-Editor/AGENTS.md`, `PROJECT_STATE.md`, `core/story_ast.py`, `core/bundle_io.py`, and relevant tests — current target application contracts.

Current source code and reproducible tests outrank historical descriptions, README claims, old transcripts, and AI-generated summaries.

## 5. Candidate implementation sources (not yet approved)

| Capability | Candidate source | Current assessment |
|---|---|---|
| SQLite text search/export | `Kyouka-Asset-Explorer/modules/db_explorer.py` | Strong candidate; query path is read-only, but keep DB reinjection out of initial scope |
| ADV story codec | `Kyouka-Asset-Explorer/modules/story_codec.py` | Candidate; story path has byte-level read-back verification |
| MV subtitle codec | `Kyouka-Asset-Explorer/modules/story_codec.py` | Candidate but unverified; subtitle repack has no read-back verification in current code |
| Manifest search and asset classification | `priconne-asset-extractor-main/NewDataMiner/manifest_manager.py`, `models.py` | Candidate for offline discovery and preview |
| DB-to-manifest discovery | `priconne-asset-extractor-main/NewDataMiner/resource_cross_ref.py` | Candidate; verify ID conventions against current manifests |
| Generic TextAsset and USM extraction | `priconne-asset-extractor-main/NewDataMiner/extractor.py` | Partial reference; does not currently extract `MonoBehaviour.recordList` subtitles |
| Old integrated workflow | `Kyouka-Asset-Explorer/OLD2/priconne_tool.py` | Historical reference; do not import wholesale |
| XUAT workflow scripts | `priconne-asset-extractor-main/priconne-adv-tools/` | Historical translation pipeline; reuse only after a concrete requirement |

## 6. Architecture constraints for Misora Editor

- Keep the plugin isolated (candidate location: `plugins/datamine/` or `plugins/datamine_extractor/`; choose only after checking existing plugin architecture).
- Keep `misora.py` as a thin integration point; do not grow it into the datamine engine.
- The plugin must expose a headless service API so extraction and parsing can be tested without starting Tkinter.
- Use the existing `StoryAST`/document import contract only after reading its real constructor and invariants. Do not invent `StoryAST.from_records()` or any other method without confirming it exists.
- Tkinter widgets and application document state may only be changed on the UI thread. Workers return immutable results through the project's established queue/callback pattern.
- Database access must be read-only for the first milestone.
- Downloads are targeted and previewed. Do not silently fetch large assets.
- Repack to a separate output file. Never overwrite the original Unity bundle in place.
- Reopen and validate every repacked bundle before reporting success.
- Preserve unknown fields, command IDs, ordering, timing, record counts, encodings, and untouched bytes wherever the source format allows it.
- No new third-party dependency without a documented necessity and user approval.

## 7. Phase gates

### D0 — Source and fixture verification (current phase)

Deliver:
- Exact source tree and version/commit IDs inspected.
- Confirmed duplicate report and candidate-source map.
- At least one legally usable local fixture for text and one for MV subtitles, or a precise statement that a real fixture is unavailable.
- Schema dumps of relevant `master.db` tables and subtitle MonoBehaviour typetrees, with private paths/secrets redacted.
- Dependency/runtime report.

**No application code changes in D0.**

### D1 — Headless text discovery contract

Define typed result models for data source, category, record identity, language, text, source asset, and provenance. Add read-only SQLite search and local manifest indexing behind a headless service. Tests use temporary databases and synthetic fixtures.

### D2 — ADV/TextAsset extraction contract

Add headless extraction for Unity `TextAsset` and ADV story scripts. Verify lossless round-trip for unchanged records, including unknown command IDs and non-ASCII/control characters. Do not add GUI yet.

### D3 — MV subtitle codec hardening

Document the confirmed subtitle schema. Add tests for extraction and repack, record-count changes, malformed/missing keys, timing preservation, unknown fields, multiple candidate MonoBehaviours, and output read-back verification. Do not claim support until the output bundle reopens and matches the expected records.

### D4 — Misora UI integration

Only after D1–D3 pass: add a dedicated import/search panel or dialog, progress/cancel support, background worker, preview, and import into the existing document model. UI design should follow current Misora patterns.

### D5 — Packaging and release

Document supported sources, limitations, backup behavior, and manual Windows verification. No silent CDN-wide downloads or original-bundle overwrites.

## 8. Decisions required from the council

1. What does “text datamine” mean for the first user-facing release: database text only, ADV story scripts, Unity TextAssets, or all three?
2. Does MV subtitle editing require fixed record count, or should insertion/deletion be supported? The legacy codec only supports fixed-count replacement.
3. Is `.usm` video preview required, or is subtitle extraction/editing enough?
4. Should the plugin only export/import text into Misora's editor document, or also create modified `.unity3d` bundles in a separate output directory?
5. What is the minimum metadata needed in every exported row: source bundle, path ID, object name, table, primary key, story/movie ID, start/end time, language, and original text?
6. What should happen when `master.db` or a manifest is missing/outdated?
7. Should automatic CDN download be disabled by default? Recommendation: yes.

## 9. Definition of done for the design phase

The design is ready for implementation only when:

- Every proposed source is linked to a real file and code symbol.
- All assumptions are tagged `UNVERIFIED` until tested.
- Text and MV subtitle data paths are distinguished.
- Headless API and data identity rules are documented.
- Repack verification and non-destructive output behavior are explicit.
- Tests and stop conditions are specified.
- The Product Owner approves one bounded D1 execution brief.

**Consensus is not a substitute for evidence. Unanimity is not required; unresolved risks must be recorded and presented to the Product Owner.**
