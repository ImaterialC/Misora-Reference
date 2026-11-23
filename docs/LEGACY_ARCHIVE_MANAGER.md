# Legacy Archive Manager

A standard-library-only helper for cataloguing, identifying exact duplicates, creating checksummed ZIP snapshots, verifying archives, and renaming ZIP archive filenames safely.

## Why it does not rename old source files in place

The legacy folders contain `.bat` launchers, relative paths, and Python imports. Renaming source files can break launchers or imports even when the source code itself is unchanged. Therefore:

- Original source paths are preserved inside ZIP files.
- ZIP files receive normalized, descriptive names.
- A catalogue can provide friendly labels/aliases without changing original filenames.
- The only rename command changes `.zip` archive filenames, and it is dry-run unless `--apply` is supplied.
- No command deletes or moves the original source directories.

## Commands (run from the Misora-Reference repository root)

### 1. Inventory the legacy folders

```bash
python tools/legacy_archive_manager.py inventory
```

Outputs:
- `reports/legacy_tool_inventory.json`
- `reports/legacy_tool_inventory.csv`

Each file row includes relative path, extension, classification, byte size, and SHA-256.

### 2. Find exact duplicate files

```bash
python tools/legacy_archive_manager.py duplicates
```

This detects exact content matches only. Similar code with different bytes is not marked as an exact duplicate.

### 3. Preview archive creation (safe default)

```bash
python tools/legacy_archive_manager.py pack
```

This only prints the planned ZIP names and file counts.

### 4. Create two separate ZIP snapshots

```bash
python tools/legacy_archive_manager.py pack --write
```

Expected output names (date suffix is generated automatically):

- `archives/legacy/priconne-asset-extractor-main__snapshot_YYYYMMDD.zip`
- `archives/legacy/kyouka-asset-explorer__snapshot_YYYYMMDD.zip`

Each ZIP preserves the original root directory and file paths and includes `_ARCHIVE_MANIFEST.json` with SHA-256 hashes.

### 5. Create one combined archive instead

```bash
python tools/legacy_archive_manager.py pack --single --archive-name misora-legacy-toolchains --write
```

Choose either separate ZIPs or a combined ZIP. Separate ZIPs are easier to update independently; combined ZIP is convenient for one-time transfer. Avoid keeping multiple redundant snapshots without recording why.

### 6. Verify a snapshot

```bash
python tools/legacy_archive_manager.py verify archives/legacy/priconne-asset-extractor-main__snapshot_YYYYMMDD.zip
```

The verifier checks ZIP CRC and every member's SHA-256 against the embedded manifest.

### 7. Rename an archive (not its source files)

Create a JSON mapping, for example:

```json
{
  "archives/legacy/old-name.zip": "archives/legacy/priconne-asset-extractor-main__legacy.zip"
}
```

Preview:

```bash
python tools/legacy_archive_manager.py rename-archive --root . --mapping rename-map.json
```

Apply only after confirming the preview:

```bash
python tools/legacy_archive_manager.py rename-archive --root . --mapping rename-map.json --apply
```

The command refuses to overwrite an existing destination and refuses to move files across folders.

## Recommended sequence

1. Run `inventory`.
2. Run `duplicates`.
3. Run `pack` without `--write` and inspect the plan.
4. Run `pack --write`.
5. Run `verify` on every created ZIP.
6. Only then update the repository's archive catalogue and mark legacy directories as archived/reference-only.
7. Do not delete original folders in the same task.

The utility does not download remote assets, update `master.db`, edit source code, or touch `Misora-Editor`.
