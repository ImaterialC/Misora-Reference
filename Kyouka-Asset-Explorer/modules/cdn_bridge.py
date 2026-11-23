#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
modules/cdn_bridge.py
=====================
Official Japanese Server CDN Asset Bridge for Princess Connect! Re:Dive.

Connects to Cygames' content-addressed Akamai pool:
    https://prd-priconne-redive.akamaized.net/dl/pool/{AssetBundles|Sound|Movie}/{md5[:2]}/{md5}

Supports two manifest backends automatically:
    1. Standalone Manifest CSV files placed in `./manifests/` (or passed via `--manifest`).
    2. Optional hook into a local `NewDataMiner` package if present in the workspace.
"""

from __future__ import annotations

import csv
import hashlib
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence

JP_CDN_HOST = "https://prd-priconne-redive.akamaized.net"
JP_CDN_ASSET_POOL = f"{JP_CDN_HOST}/dl/pool/AssetBundles"
JP_CDN_SOUND_POOL = f"{JP_CDN_HOST}/dl/pool/Sound"
JP_CDN_MOVIE_POOL = f"{JP_CDN_HOST}/dl/pool/Movie"
DEFAULT_USER_AGENT = "UnityPlayer/2021.3.20f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)"


@dataclass
class CDNManifestEntry:
    """Single downloadable asset entry indexed from a JP CDN manifest."""

    name: str
    md5_hash: str
    size: int = 0
    category: str = ""
    raw_obj: object = None

    @property
    def pool_url(self) -> str:
        """Build the direct JP Cygames CDN download URL from the MD5 hash."""
        lower = self.name.lower()
        if lower.startswith("m/") or lower.endswith(".usm"):
            base = JP_CDN_MOVIE_POOL
        elif lower.startswith(("v/", "b/", "s/")) or lower.endswith((".acb", ".awb")):
            base = JP_CDN_SOUND_POOL
        else:
            base = JP_CDN_ASSET_POOL
        return f"{base}/{self.md5_hash[:2]}/{self.md5_hash}"

    @property
    def human_size(self) -> str:
        if self.size <= 0:
            return "unknown"
        if self.size < 1024:
            return f"{self.size} B"
        if self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} KB"
        return f"{self.size / (1024 * 1024):.2f} MB"


class JPCDNBridge:
    """Manifest indexer and MD5-verified downloader for the Japanese CDN server."""

    def __init__(
        self,
        project_root: Path,
        manifest_paths: Optional[Sequence[Path]] = None,
    ) -> None:
        self.project_root = Path(project_root)
        self.entries: Dict[str, CDNManifestEntry] = {}
        self.dm: Optional[object] = None
        self.backend_status = "No manifest loaded"
        self._initialize(manifest_paths or [])

    def _initialize(self, extra_manifests: Sequence[Path]) -> None:
        candidates: List[Path] = list(extra_manifests)
        for folder in (self.project_root / "manifests", self.project_root):
            if folder.is_dir():
                for pattern in ("*manifest*", "*.csv"):
                    for fp in folder.glob(pattern):
                        if fp.is_file() and fp.name.lower() != "readme.md":
                            candidates.append(fp)

        seen_paths = set()
        loaded_files = 0
        for fp in candidates:
            resolved = fp.resolve()
            if resolved in seen_paths or not resolved.is_file():
                continue
            seen_paths.add(resolved)
            loaded_files += self._load_manifest_csv(resolved)

        if self.entries:
            self.backend_status = f"Standalone JP Manifest ({len(self.entries):,} assets from {loaded_files} file(s))"
            return

        try:
            from NewDataMiner.dataminer import DataMiner  # type: ignore

            self.dm = DataMiner()
            self.dm.manifest_manager.load_manifests()
            raw_entries = self._collect_newdataminer_entries(self.dm.manifest_manager)
            for e in raw_entries:
                self.entries[e.name.lower()] = e
            if self.entries:
                self.backend_status = f"NewDataMiner Bridge ({len(self.entries):,} JP assets)"
                return
        except Exception:
            self.dm = None

        self.backend_status = (
            "No manifest loaded (place JP manifest files in ./manifests/ or pass --manifest)"
        )

    @staticmethod
    def _collect_newdataminer_entries(manifest_manager: object) -> List[CDNManifestEntry]:
        collected: List[CDNManifestEntry] = []
        pools: List[object] = []
        for attr in ("entries", "all_entries", "assets", "_entries"):
            val = getattr(manifest_manager, attr, None)
            if isinstance(val, dict):
                pools.extend(val.values())
            elif isinstance(val, list):
                pools.extend(val)

        for item in pools:
            name = getattr(item, "name", None) or getattr(item, "path", None)
            md5 = getattr(item, "hash", None) or getattr(item, "md5", None) or ""
            size = int(getattr(item, "size", 0) or 0)
            cat = str(getattr(item, "category", "") or "")
            if name and md5:
                collected.append(
                    CDNManifestEntry(
                        name=str(name),
                        md5_hash=str(md5).lower(),
                        size=size,
                        category=cat,
                        raw_obj=item,
                    )
                )
        return collected

    def _load_manifest_csv(self, path: Path) -> int:
        """Parse standard Cygames comma-separated manifest rows: name,md5,group,size,..."""
        added = 0
        try:
            with path.open("r", encoding="utf-8", errors="replace") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 2:
                        continue
                    name = row[0].strip()
                    md5 = row[1].strip()
                    if not name or not re.fullmatch(r"[0-9a-fA-F]{32}", md5):
                        continue
                    size = int(row[3]) if len(row) > 3 and row[3].strip().isdigit() else 0
                    cat = row[4].strip() if len(row) > 4 else ""
                    self.entries[name.lower()] = CDNManifestEntry(
                        name=name, md5_hash=md5.lower(), size=size, category=cat
                    )
                    added += 1
        except OSError:
            return 0
        return 1 if added > 0 else 0

    def search(self, keyword: str) -> List[CDNManifestEntry]:
        """Search loaded JP CDN manifest entries by substring, Story ID, or codename."""
        kw = keyword.lower().strip()
        if not kw:
            return []
        hits = [e for e in self.entries.values() if kw in e.name.lower()]
        hits.sort(key=lambda e: e.name)
        return hits

    def download(
        self,
        entry: CDNManifestEntry,
        dest_dir: Path,
        verify_md5: bool = True,
        timeout: int = 30,
    ) -> Path:
        """Download an asset from the JP Cygames CDN pool and verify its MD5 checksum."""
        dest_dir.mkdir(parents=True, exist_ok=True)
        target_path = dest_dir / Path(entry.name).name

        req = urllib.request.Request(entry.pool_url, headers={"User-Agent": DEFAULT_USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"JP CDN HTTP {exc.code} while fetching {entry.pool_url}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"JP CDN connection failed: {exc.reason}") from exc

        if verify_md5:
            actual_md5 = hashlib.md5(data).hexdigest().lower()
            if actual_md5 != entry.md5_hash.lower():
                raise RuntimeError(
                    f"MD5 mismatch for {entry.name}: expected {entry.md5_hash}, got {actual_md5}"
                )

        target_path.write_bytes(data)
        return target_path
