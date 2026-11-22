#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extractor_prototype.local_scanner
==================================
Pillar 1: Fast local DMM client cache scanner.
Scans %USERPROFILE%/AppData/LocalLow/Cygames/PrincessConnectReDive/a/
to identify downloaded Princess Connect! Re:Dive JP story bundles with zero network overhead.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class ScannedStoryItem:
    """Represents a discovered story asset bundle in local cache."""
    path: Path
    filename: str
    file_size: int
    story_id: Optional[int] = None
    is_story_data: bool = False

    @property
    def formatted_size(self) -> str:
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        return f"{self.file_size / (1024 * 1024):.2f} MB"


class LocalScanner:
    """Scans and indexes game asset bundles from the official DMM Games PC client."""

    DEFAULT_SUBPATH = ("AppData", "LocalLow", "Cygames", "PrincessConnectReDive", "a")
    STORY_FILE_PATTERN = re.compile(r"storydata_?(\d+)", re.IGNORECASE)

    def __init__(self, cache_dir: Optional[Path] = None):
        if cache_dir is not None:
            self.cache_dir = Path(cache_dir)
        else:
            user_profile = os.environ.get("USERPROFILE") or os.environ.get("HOME") or ""
            if user_profile:
                self.cache_dir = Path(user_profile).joinpath(*self.DEFAULT_SUBPATH)
            else:
                self.cache_dir = Path(".")

    def is_cache_available(self) -> bool:
        """Check if the DMM local cache directory exists and is accessible."""
        return self.cache_dir.is_dir()

    def parse_story_id(self, name: str) -> Optional[int]:
        """Extract story ID from filenames like storydata_100101.unity3d or story_100101."""
        match = self.STORY_FILE_PATTERN.search(name)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None

    def scan(self, filter_story_only: bool = True, max_items: Optional[int] = None) -> List[ScannedStoryItem]:
        """
        Scan cache directory for asset bundles.
        Returns a list of ScannedStoryItem records sorted by filename.
        """
        if not self.is_cache_available():
            return []

        results: List[ScannedStoryItem] = []
        try:
            for root, _, files in os.walk(self.cache_dir):
                for f in files:
                    lower = f.lower()
                    is_story = "story" in lower
                    if filter_story_only and not is_story:
                        continue

                    full_path = Path(root) / f
                    try:
                        sz = full_path.stat().st_size
                    except OSError:
                        sz = 0

                    story_id = self.parse_story_id(f)
                    results.append(
                        ScannedStoryItem(
                            path=full_path,
                            filename=f,
                            file_size=sz,
                            story_id=story_id,
                            is_story_data=is_story,
                        )
                    )
                    if max_items and len(results) >= max_items:
                        return results
        except (PermissionError, OSError):
            return results

        results.sort(key=lambda item: item.filename)
        return results
