# Project Mandate

## Purpose

Misora-Reference is the shared evidence and review workspace for the development of Misora Editor. It is not itself the application and it is not a mandate to recreate every tool placed in the reference library.

## Project links

- Main application: https://github.com/ImaterialC/Misora-Editor
- Reference repository: https://github.com/ImaterialC/Misora-Reference
- Preserved Priconne ADV reference tools: https://github.com/ImaterialC/Misora-Reference/tree/main/references/priconne-adv-tools

## Operating goal

Help the owner make evidence-based decisions about:
1. Existing Misora Editor bugs and regressions.
2. Missing core capabilities that block the intended workflow.
3. A future Datamine capability focused on game text and MV/movie subtitle text.
4. Safe implementation order, verification, and maintainability.

## Priority rule

**Existing Misora Editor stability and missing core features take priority over adding the Datamine plugin.**

The review must first determine which core issues block reliable use. Datamine integration planning should follow only when dependencies and required core behavior are understood and approved.

## Datamine scope

The current discussion is narrowly focused on:
- Extracting or discovering text-based game data.
- Understanding ADV/story text and related text assets.
- Discovering and handling MV/movie subtitle text and its associated metadata.
- Mapping text records to relevant identifiers, assets, manifests, or database records where supported by evidence.
- Preserving stable identifiers and round-trip data integrity where editing/repacking is part of the approved feature.

The following are not automatically in scope:
- General-purpose texture, sprite, audio, or 3D asset extraction.
- Rebuilding every function in the Priconne reference tool.
- Downloading all game assets.
- Replacing the existing application architecture without evidence.
- Assuming a data format or subtitle location without inspecting it.

## Evidence-first technical assumptions

- The repository contains a Priconne ADV reference tool. Its presence is evidence that a reference implementation exists, not proof that its approach is suitable for Misora Editor.
- A candidate data source (for example master.db, Unity TextAsset, MonoBehaviour records, manifests, or a movie container) must be inspected before it is described as the actual source.
- Do not assume that video files such as `.usm` contain subtitle text. Verify whether subtitle information is stored separately or in a specific metadata structure.
- Record format/version differences and unknown cases explicitly.

## Owner experience

The owner coordinates the AI review manually by copying prompts and responses between AI services. The owner may not be able to verify code-level claims independently. Therefore:
- Explain conclusions in clear Bahasa Indonesia.
- Make all technical claims auditable with paths, snippets, test steps, and evidence.
- Do not use unexplained jargon when a plain explanation is possible.
- Give the owner one clear next action at each gate.
