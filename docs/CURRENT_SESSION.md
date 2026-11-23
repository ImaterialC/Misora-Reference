# Current Review Session

**Session name:** Misora Editor Core Readiness → Text Datamine and MV Subtitle

**Status:** Ready for Phase 0 access checks. No technical findings are yet approved by the council in this session.

## Repositories

- Main application: https://github.com/ImaterialC/Misora-Editor
- Reference material and review rules: https://github.com/ImaterialC/Misora-Reference

## Primary objective

Establish a reliable, evidence-based implementation roadmap for Misora Editor. First audit existing bugs and missing core features that must be resolved. Only then plan the focused Datamine capability.

## Priority order

1. Verify all participating AI surfaces can access the same required source material (Phase 0).
2. Independently inspect current Misora Editor behavior and code (Phase 1).
3. Combine AI findings and the owner's manual findings with evidence (Phase 2).
4. Prove the canonical bug/feature inventory is exhaustive (Phase 2.5).
5. Plan fixes for critical Misora Editor blockers and missing core capabilities.
6. Plan Datamine text and MV/movie subtitle support only after required foundations are stable.
7. Execute bounded tasks in Antigravity after owner approval (Phase 4).

## Datamine candidate scope

Investigate only:
- Game text records and text assets.
- ADV/story text and the current data flow around it.
- MV/movie subtitle text and the actual data structure that stores it.
- Identifiers, manifests, or database relationships needed to locate and associate those text records.
- Safe editing/export/repack behavior only if it is part of the agreed requirement and can be validated.

Do not assume any candidate format or location without evidence. In particular, establish whether subtitle content is stored in Unity objects, separate metadata, text files, video-related data, or another structure. Do not assume that a `.usm` video/audio container contains the subtitle text.

## Non-goals unless separately approved

- General-purpose image, texture, sprite, 3D, audio, or music asset extraction.
- Rebuilding the entire Priconne reference tool in Misora Editor.
- Downloading all game assets.
- Modifying the preserved reference-tool source during normal Misora Editor implementation.
- Starting Datamine implementation before core blockers and dependencies are addressed.

## Owner inputs

The owner will supply Phase 1 reports and private observations to the participating AIs at Phase 2. Keep those private observations out of Phase 1 inputs.

## Session update rule

When the owner changes the current objective, update this file and record the previous scope in a dated session archive. Do not silently reuse this scope for an unrelated feature debate.
