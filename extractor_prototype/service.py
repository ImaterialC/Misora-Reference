#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extractor_prototype.service
============================
Unified Orchestrator for the Misora Extractor Plugin.
Binds Pillar 1 (Local Scanner), Pillar 2 (Story Codec), and Pillar 3 (Database Metadata)
into a clean, headless API ready for integration into Misora Editor.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .db_metadata import DatabaseMetadata
from .local_scanner import LocalScanner, ScannedStoryItem
from .story_codec import DialogueBlock, StoryCodec, StoryScene


class MisoraExtractorService:
    """Headless API service providing 1-click discovery, decoding, and metadata enrichment."""

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        db_path: Optional[Path] = None,
    ):
        self.scanner = LocalScanner(cache_dir=cache_dir)
        self.metadata = DatabaseMetadata(db_path=db_path)
        self.codec = StoryCodec()

    def scan_catalog(self, max_items: Optional[int] = 50) -> List[Dict[str, Any]]:
        """
        Scan local DMM client cache and enrich every discovered story bundle with master.db titles.
        Returns a JSON-serializable catalog list.
        """
        scanned_items = self.scanner.scan(filter_story_only=True, max_items=max_items)
        catalog: List[Dict[str, Any]] = []

        for item in scanned_items:
            title = ""
            if item.story_id:
                meta = self.metadata.get_story_title(item.story_id)
                title = meta.title

            catalog.append(
                {
                    "filename": item.filename,
                    "path": str(item.path),
                    "story_id": item.story_id,
                    "title": title or "Unknown Story",
                    "file_size": item.file_size,
                    "formatted_size": item.formatted_size,
                }
            )

        return catalog

    def extract_from_bytes(
        self,
        raw_bytes: bytes,
        story_id: Optional[int] = None,
        enrich: bool = True,
    ) -> StoryScene:
        """Decode raw binary story payload in memory and optionally enrich speaker names."""
        scene = self.codec.decode_scene_from_bytes(raw_bytes)
        if enrich:
            self.metadata.enrich_scene(scene, story_id=story_id)
        return scene

    def extract_from_bundle(
        self,
        bundle_source: Union[Path, bytes, io.BytesIO],
        story_id: Optional[int] = None,
        enrich: bool = True,
    ) -> StoryScene:
        """Unpack a .unity3d story bundle in memory and enrich speaker names."""
        scene = self.codec.decode_from_bundle(bundle_source)
        if enrich:
            self.metadata.enrich_scene(scene, story_id=story_id)
        return scene

    def convert_bundle_to_csif(
        self,
        bundle_source: Union[Path, bytes, io.BytesIO],
        story_id: Optional[int] = None,
    ) -> str:
        """1-step pipeline: Asset bundle in -> CSIF text string out (in-memory)."""
        scene = self.extract_from_bundle(bundle_source, story_id=story_id, enrich=True)
        return scene.to_csif()
