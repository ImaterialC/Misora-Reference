# Contributing to Kyouka Asset Explorer

Contributions from the international *Princess Connect! Re:Dive* fan translation community are welcome!

## Code & Documentation Guidelines

1. **Language:** Keep all source code, docstrings, comments, and primary CLI strings in clear **English** so contributors worldwide can read and maintain the project.
2. **Minimal Dependencies:** Core database, glossary, and CDN modules must remain **Python Standard Library only**. Optional dependencies (like `UnityPy`) should be lazily imported with helpful fallback messages.
3. **Never Commit Game Assets:** Do not commit `master.db`, `.unity3d` bundles, or copyrighted game scripts in Pull Requests.
4. **Taxonomy Updates:** When Cygames introduces new game modes or table prefixes in `master.db`, please add them to:
   - `CATEGORY_RULES` in `modules/db_explorer.py`
   - `ASSET_GLOSSARY` in `modules/glossary.py`
   - `docs/DEVELOPER_GLOSSARY.md`
