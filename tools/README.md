# Reference Tools & Legacy Scripts

Place external reference scripts, prototypes, or helper utilities used during multi-AI research and debate here (for example: legacy XUAT migration scripts, format converters, or diagnostic scripts).

## Guidelines for AIs Inspecting `tools/`
1. **Audit Before Porting:** Legacy or third-party scripts may contain edge-case bugs, unsafe file I/O, or incompatible assumptions. Always audit them critically in Phase 1/2 before recommending porting any logic into `Misora-Editor`.
2. **Scope Respect:** Presence of a script or module in `tools/` does NOT automatically mean all of its functionality should be ported into `Misora-Editor`. Follow the User's explicit scope boundaries.
