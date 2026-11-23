#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safe inventory, duplicate detection, ZIP packing, and archive renaming.

This tool is intentionally non-destructive by default:
- inventory/duplicates only read source files;
- pack only writes ZIPs when --write is supplied;
- rename-archive only renames ZIP files when --apply is supplied;
- original source files are never renamed, moved, or deleted by this tool.

The old tool folders contain launchers and relative imports. Renaming source files
in place can silently break those programs, so this tool gives archive bundles
canonical names while preserving every original relative path inside each ZIP.
Python 3.10+; standard library only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", ".tox", "node_modules", ".mypy_cache", ".pytest_cache"}
DEFAULT_SOURCES = ("priconne-asset-extractor-main", "Kyouka-Asset-Explorer")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".py", ".pyw"}:
        return "python_source"
    if suffix in {".bat", ".cmd", ".ps1", ".sh"}:
        return "launcher_or_script"
    if suffix in {".md", ".txt", ".rst"}:
        return "documentation_or_text"
    if suffix in {".json", ".toml", ".ini", ".yaml", ".yml"}:
        return "configuration_or_metadata"
    if suffix in {".zip", ".7z", ".rar"}:
        return "archive"
    if not suffix and ("manifest" in path.name.lower() or path.name.lower().endswith("assetmanifest")):
        return "manifest_or_index"
    if "manifest" in path.name.lower():
        return "manifest_or_index"
    return "other_data_or_asset"


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def iter_source_files(root: Path, sources: Iterable[str], include_archives: bool = False) -> list[Path]:
    root = root.resolve()
    found: list[Path] = []
    for source in sources:
        source_path = (root / source).resolve()
        if not is_within(source_path, root):
            raise ValueError(f"Source escapes repository root: {source}")
        if not source_path.exists():
            raise FileNotFoundError(f"Source path not found: {source_path}")
        candidates = [source_path] if source_path.is_file() else source_path.rglob("*")
        for candidate in candidates:
            # Do not follow symbolic links: a linked file could point outside the repo.
            if candidate.is_symlink() or not candidate.is_file():
                continue
            resolved_candidate = candidate.resolve()
            if not is_within(resolved_candidate, root):
                continue
            candidate = resolved_candidate
            rel_parts = candidate.relative_to(root).parts
            if any(part in SKIP_DIRS for part in rel_parts):
                continue
            if not include_archives and "archives" in {p.lower() for p in rel_parts[:-1]}:
                continue
            found.append(candidate)
    # Resolve overlapping source arguments without double counting.
    return sorted(set(p.resolve() for p in found), key=lambda p: p.as_posix().lower())


def make_inventory(root: Path, sources: Iterable[str], include_archives: bool = False) -> list[dict[str, Any]]:
    root = root.resolve()
    rows: list[dict[str, Any]] = []
    for path in iter_source_files(root, sources, include_archives=include_archives):
        stat = path.stat()
        rel = path.relative_to(root).as_posix()
        rows.append({
            "path": rel,
            "filename": path.name,
            "extension": path.suffix.lower(),
            "kind": classify(path),
            "size_bytes": stat.st_size,
            "sha256": sha256_file(path),
        })
    return rows


def duplicate_groups(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_hash[row["sha256"]].append(row)
    groups = []
    for digest, items in sorted(by_hash.items()):
        if len(items) > 1:
            groups.append({"sha256": digest, "size_bytes": items[0]["size_bytes"], "paths": [x["path"] for x in items]})
    return groups


def write_inventory(rows: list[dict[str, Any]], json_path: Path, csv_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "file_count": len(rows),
        "total_size_bytes": sum(row["size_bytes"] for row in rows),
        "files": rows,
        "exact_duplicate_groups": duplicate_groups(rows),
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["path", "filename", "extension", "kind", "size_bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)


def slug(value: str) -> str:
    value = value.strip().lower().replace("\\", "-").replace("/", "-")
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-._")
    return value or "legacy-source"


def make_zip_for_source(root: Path, source: str, output_path: Path, dry_run: bool) -> dict[str, Any]:
    root = root.resolve()
    source_path = (root / source).resolve()
    if not is_within(source_path, root) or not source_path.is_dir():
        raise ValueError(f"Expected a source directory inside root: {source}")
    files = iter_source_files(root, [source])
    # Keep only files under this source (iter_source_files is already scoped).
    entries = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        entries.append({"path": rel, "size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
    total = sum(x["size_bytes"] for x in entries)
    result = {
        "source": source,
        "output": str(output_path),
        "file_count": len(entries),
        "source_size_bytes": total,
        "written": False,
    }
    if dry_run:
        return result

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        raise FileExistsError(f"Archive already exists; refusing to overwrite: {output_path}")
    temp_path = output_path.with_name(output_path.name + ".tmp")
    manifest = {
        "archive_format": 1,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_root": source,
        "preserve_original_relative_paths": True,
        "files": entries,
    }
    try:
        with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for path in files:
                archive.write(path, arcname=path.relative_to(root).as_posix())
            archive.writestr(f"{source}/_ARCHIVE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        with zipfile.ZipFile(temp_path, "r") as archive:
            bad = archive.testzip()
            if bad is not None:
                raise zipfile.BadZipFile(f"Corrupt member after writing: {bad}")
            # Verify every archived source file's bytes against its inventory hash.
            for item in entries:
                payload = archive.read(item["path"])
                if hashlib.sha256(payload).hexdigest() != item["sha256"]:
                    raise IOError(f"Hash verification failed for archived member: {item['path']}")
        os.replace(temp_path, output_path)
        result["written"] = True
        result["archive_size_bytes"] = output_path.stat().st_size
        result["verified"] = True
        return result
    finally:
        if temp_path.exists():
            temp_path.unlink()


def cmd_inventory(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    sources = args.source or list(DEFAULT_SOURCES)
    rows = make_inventory(root, sources, include_archives=args.include_archives)
    json_path, csv_path = Path(args.json_out), Path(args.csv_out)
    write_inventory(rows, json_path, csv_path)
    dupes = duplicate_groups(rows)
    print(f"Inventory complete: {len(rows)} files, {sum(r['size_bytes'] for r in rows):,} bytes")
    print(f"Exact duplicate groups: {len(dupes)}")
    print(f"JSON: {json_path}\nCSV : {csv_path}")
    return 0


def cmd_duplicates(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    sources = args.source or list(DEFAULT_SOURCES)
    rows = make_inventory(root, sources, include_archives=args.include_archives)
    groups = duplicate_groups(rows)
    if not groups:
        print("No exact duplicate groups found.")
        return 0
    for index, group in enumerate(groups, 1):
        print(f"\n[{index}] SHA256 {group['sha256']} ({group['size_bytes']:,} bytes)")
        for path in group["paths"]:
            print(f"  - {path}")
    print(f"\n{len(groups)} exact duplicate group(s). Similar-but-different files are not classified as duplicates.")
    return 0


def cmd_pack(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    sources = args.source or list(DEFAULT_SOURCES)
    stamp = args.date or datetime.now().strftime("%Y%m%d")
    out_dir = Path(args.output_dir)
    results = []
    if args.single:
        # Single ZIP preserving both source roots.
        all_files = iter_source_files(root, sources)
        entries = [{"path": p.relative_to(root).as_posix(), "size_bytes": p.stat().st_size, "sha256": sha256_file(p)} for p in all_files]
        output = out_dir / f"{slug(args.archive_name or 'misora-legacy-toolchains')}__snapshot_{stamp}.zip"
        preview = {"sources": sources, "output": str(output), "file_count": len(entries), "source_size_bytes": sum(x['size_bytes'] for x in entries), "written": False}
        if args.write:
            output.parent.mkdir(parents=True, exist_ok=True)
            if output.exists():
                raise FileExistsError(f"Archive already exists; refusing to overwrite: {output}")
            tmp = output.with_name(output.name + ".tmp")
            try:
                manifest = {"archive_format": 1, "created_at_utc": datetime.now(timezone.utc).isoformat(), "sources": sources, "files": entries}
                with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
                    for p in all_files:
                        archive.write(p, arcname=p.relative_to(root).as_posix())
                    archive.writestr("_ARCHIVE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
                with zipfile.ZipFile(tmp, "r") as archive:
                    bad = archive.testzip()
                    if bad is not None:
                        raise zipfile.BadZipFile(f"Corrupt member: {bad}")
                    for item in entries:
                        if hashlib.sha256(archive.read(item["path"])).hexdigest() != item["sha256"]:
                            raise IOError(f"Hash verification failed: {item['path']}")
                os.replace(tmp, output)
                preview.update({"written": True, "archive_size_bytes": output.stat().st_size, "verified": True})
            finally:
                if tmp.exists():
                    tmp.unlink()
        results.append(preview)
    else:
        for source in sources:
            output = out_dir / f"{slug(source)}__snapshot_{stamp}.zip"
            results.append(make_zip_for_source(root, source, output, dry_run=not args.write))
    for item in results:
        print(f"\nSource: {', '.join(item.get('sources', [item.get('source', '?')]))}")
        print(f"Output: {item['output']}")
        print(f"Files : {item['file_count']:,}; source bytes: {item['source_size_bytes']:,}")
        print("Status: " + ("CREATED + VERIFIED" if item["written"] else "DRY RUN — no archive written"))
    if not args.write:
        print("\nNo files were changed. Add --write to create the ZIP archive(s).")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    archive_path = Path(args.archive).resolve()
    with zipfile.ZipFile(archive_path, "r") as archive:
        bad = archive.testzip()
        if bad:
            print(f"FAIL: corrupt member {bad}")
            return 1
        names = archive.namelist()
        manifest_name = next((n for n in names if n.endswith("_ARCHIVE_MANIFEST.json") or n == "_ARCHIVE_MANIFEST.json"), None)
        if not manifest_name:
            print("ZIP CRC check passed, but archive manifest is missing; content hashes were not re-verified.")
            return 2
        manifest = json.loads(archive.read(manifest_name).decode("utf-8"))
        entries = manifest.get("files", [])
        for item in entries:
            if hashlib.sha256(archive.read(item["path"])).hexdigest() != item["sha256"]:
                print(f"FAIL: hash mismatch: {item['path']}")
                return 1
    print(f"PASS: {archive_path.name} — {len(entries)} source files, ZIP CRC and SHA256 verified.")
    return 0


def cmd_rename_archive(args: argparse.Namespace) -> int:
    mapping_path = Path(args.mapping)
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    if not isinstance(mapping, dict) or not mapping:
        raise ValueError("Rename mapping must be a non-empty JSON object: {old.zip: new.zip}")
    root = Path(args.root).resolve()
    operations = []
    for old_rel, new_rel in mapping.items():
        old = (root / old_rel).resolve()
        new = (root / new_rel).resolve()
        if not is_within(old, root) or not is_within(new, root):
            raise ValueError("Rename paths must remain inside --root.")
        if old.suffix.lower() != ".zip" or new.suffix.lower() != ".zip":
            raise ValueError("Only .zip archive filenames may be renamed by this command.")
        if not old.is_file():
            raise FileNotFoundError(old)
        if new.exists() and old != new:
            raise FileExistsError(f"Destination already exists: {new}")
        if old.parent != new.parent:
            raise ValueError("Rename-archive only renames within the same folder; it does not move archives.")
        operations.append((old, new))
    for old, new in operations:
        print(f"{old.relative_to(root)}  ->  {new.relative_to(root)}")
    if not args.apply:
        print("DRY RUN — no archive renamed. Add --apply to execute the mapping.")
        return 0
    for old, new in operations:
        if old != new and new.exists():
            raise FileExistsError(f"Destination appeared during operation: {new}")
        old.rename(new)
    print(f"Renamed {len(operations)} archive(s). Source folders were not modified.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe legacy source inventory and ZIP archive utility")
    sub = parser.add_subparsers(dest="command", required=True)

    inv = sub.add_parser("inventory", help="Hash and classify files in source folders")
    inv.add_argument("--root", default=".")
    inv.add_argument("--source", action="append", help="Folder/file relative to root; repeatable")
    inv.add_argument("--json-out", default="reports/legacy_tool_inventory.json")
    inv.add_argument("--csv-out", default="reports/legacy_tool_inventory.csv")
    inv.add_argument("--include-archives", action="store_true")
    inv.set_defaults(func=cmd_inventory)

    dup = sub.add_parser("duplicates", help="List exact SHA256 duplicate groups")
    dup.add_argument("--root", default=".")
    dup.add_argument("--source", action="append", help="Folder/file relative to root; repeatable")
    dup.add_argument("--include-archives", action="store_true")
    dup.set_defaults(func=cmd_duplicates)

    pack = sub.add_parser("pack", help="Create ZIP snapshots, dry-run unless --write is supplied")
    pack.add_argument("--root", default=".")
    pack.add_argument("--source", action="append", help="Folder relative to root; repeatable")
    pack.add_argument("--output-dir", default="archives/legacy")
    pack.add_argument("--date", help="Date suffix YYYYMMDD; defaults to current local date")
    pack.add_argument("--single", action="store_true", help="Combine all selected sources into one ZIP")
    pack.add_argument("--archive-name", help="Base name for --single archive")
    pack.add_argument("--write", action="store_true", help="Actually write ZIP archive(s); otherwise dry-run")
    pack.set_defaults(func=cmd_pack)

    verify = sub.add_parser("verify", help="Verify ZIP CRC and per-file SHA256 manifest")
    verify.add_argument("archive")
    verify.set_defaults(func=cmd_verify)

    rename = sub.add_parser("rename-archive", help="Safely rename ZIP files from an explicit JSON mapping")
    rename.add_argument("--root", default=".")
    rename.add_argument("--mapping", required=True, help="JSON object mapping old.zip to new.zip")
    rename.add_argument("--apply", action="store_true", help="Apply rename; without it command is dry-run")
    rename.set_defaults(func=cmd_rename_archive)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (OSError, ValueError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
