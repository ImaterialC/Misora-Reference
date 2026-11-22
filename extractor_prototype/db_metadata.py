#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extractor_prototype.db_metadata
================================
Pillar 3: SQLite metadata resolver querying master.db (Robo Ninon datamine).
Enriches extracted story scenes with canonical speaker names, chapter titles,
and character portraits without loading full tables into RAM.
"""

from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


# Known static fallbacks when master.db is offline or unavailable
STATIC_UNIT_FALLBACKS: Dict[int, Tuple[str, str]] = {
    118201: ("Misora", "ミソラ"),
    105801: ("Pecorine", "ペコリーヌ"),
    105901: ("Kokkoro", "コッコロ"),
    100101: ("Hiyori", "ヒヨリ"),
    100201: ("Yui", "ユイ"),
    100301: ("Rei", "レイ"),
    105701: ("Karyl", "キャル"),
}


@dataclass
class UnitMetadata:
    unit_id: int
    unit_name: str
    unit_name_jp: str = ""
    kana_name: str = ""
    voice_actor: str = ""


@dataclass
class StoryMetadata:
    story_id: int
    title: str
    sub_title: str = ""
    category: str = "main"


class DatabaseMetadata:
    """Read-only SQLite query engine for Princess Connect! Re:Dive master.db."""

    SEARCH_PATHS = [
        Path(r"D:\Kyouka-Asset-Explorer\master.db"),
        Path(r"D:\Reference\Misora-Reference\master.db"),
        Path(r".\master.db"),
    ]

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path: Optional[Path] = None
        self._conn: Optional[sqlite3.Connection] = None
        self._unit_cache: Dict[int, UnitMetadata] = {}
        self._story_cache: Dict[int, StoryMetadata] = {}

        if db_path is not None and Path(db_path).is_file():
            self.db_path = Path(db_path)
        else:
            for p in self.SEARCH_PATHS:
                if p.is_file():
                    self.db_path = p
                    break

        if self.db_path:
            self._connect()

    def _connect(self) -> None:
        """Open a read-only URI connection to master.db."""
        if not self.db_path or not self.db_path.is_file():
            return
        try:
            uri = f"file:{self.db_path.as_posix()}?mode=ro"
            self._conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        except Exception:
            self._conn = None

    def is_available(self) -> bool:
        """Check if connection to master.db is active."""
        return self._conn is not None

    def get_unit(self, unit_id: int) -> UnitMetadata:
        """Resolve unit_id (e.g. 105801) to canonical character name."""
        if unit_id in self._unit_cache:
            return self._unit_cache[unit_id]

        if not self._conn:
            fb = STATIC_UNIT_FALLBACKS.get(unit_id, (f"Unit_{unit_id}", f"Unit_{unit_id}"))
            meta = UnitMetadata(unit_id=unit_id, unit_name=fb[0], unit_name_jp=fb[1])
            self._unit_cache[unit_id] = meta
            return meta

        try:
            cursor = self._conn.cursor()
            cursor.execute(
                "SELECT unit_name, unit_name_jp, kana FROM unit_data WHERE unit_id = ?",
                (unit_id,),
            )
            row = cursor.fetchone()
            if row:
                jp_name = row["unit_name_jp"] or row["unit_name"]
                meta = UnitMetadata(
                    unit_id=unit_id,
                    unit_name=row["unit_name"],
                    unit_name_jp=jp_name,
                    kana_name=row["kana"] or "",
                )
            else:
                fb = STATIC_UNIT_FALLBACKS.get(unit_id, (f"Unit_{unit_id}", f"Unit_{unit_id}"))
                meta = UnitMetadata(
                    unit_id=unit_id,
                    unit_name=fb[0],
                    unit_name_jp=fb[1],
                )
        except sqlite3.Error:
            fb = STATIC_UNIT_FALLBACKS.get(unit_id, (f"Unit_{unit_id}", f"Unit_{unit_id}"))
            meta = UnitMetadata(
                unit_id=unit_id,
                unit_name=fb[0],
                unit_name_jp=fb[1],
            )

        self._unit_cache[unit_id] = meta
        return meta

    def get_story_title(self, story_id: int) -> StoryMetadata:
        """Resolve story_id to official chapter and episode title."""
        if story_id in self._story_cache:
            return self._story_cache[story_id]

        if not self._conn:
            meta = StoryMetadata(story_id=story_id, title=f"Story {story_id}")
            self._story_cache[story_id] = meta
            return meta

        try:
            cursor = self._conn.cursor()
            # Try story_data
            cursor.execute(
                "SELECT title, sub_title FROM story_data WHERE story_id = ?",
                (story_id,),
            )
            row = cursor.fetchone()
            if row:
                meta = StoryMetadata(
                    story_id=story_id,
                    title=row["title"] or f"Story {story_id}",
                    sub_title=row["sub_title"] or "",
                )
            else:
                meta = StoryMetadata(story_id=story_id, title=f"Story {story_id}")
        except sqlite3.Error:
            meta = StoryMetadata(story_id=story_id, title=f"Story {story_id}")

        self._story_cache[story_id] = meta
        return meta

    def enrich_scene(self, scene: Any, story_id: Optional[int] = None) -> None:
        """
        Enrich a StoryScene object in-place:
        - Populate scene.title if missing
        - Resolve speaker tags that are numeric IDs (e.g. '105801' -> 'ミソラ')
        """
        if story_id and (not scene.title or scene.title == "Untitled"):
            meta = self.get_story_title(story_id)
            scene.title = meta.title

        for d in scene.dialogues:
            if d.speaker.isdigit():
                uid = int(d.speaker)
                d.character_id = uid
                u = self.get_unit(uid)
                d.speaker = u.unit_name_jp or u.unit_name
            elif d.speaker.startswith("chara_") and d.speaker[6:].isdigit():
                uid = int(d.speaker[6:])
                d.character_id = uid
                u = self.get_unit(uid)
                d.speaker = u.unit_name_jp or u.unit_name
