#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
modules/bepinex_guard.py
========================
Lightweight BepInEx RedirectedResources Duplicate Detector.

Scans an existing BepInEx `Translation/<lang>/RedirectedResources` directory
so translators can avoid re-downloading or overwriting already-translated
Unity3D bundles.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple


@dataclass
class BepInExPaths:
    """Resolved paths inside a BepInEx translation workspace."""

    bepinex_root: Optional[Path] = None
    redirected_dir: Optional[Path] = None
    xuat_text_dir: Optional[Path] = None

    @classmethod
    def resolve(cls, hint: Optional[Path | str], lang: str = "en") -> "BepInExPaths":
        if not hint:
            return cls()
        p = Path(hint).expanduser().resolve()
        parts_lower = [part.lower() for part in p.parts]

        if "translation" in parts_lower:
            t_idx = parts_lower.index("translation")
            bep_root = Path(*p.parts[:t_idx])
            detected_lang = p.parts[t_idx + 1] if t_idx + 1 < len(p.parts) else lang
            return cls(
                bepinex_root=bep_root,
                redirected_dir=bep_root / "Translation" / detected_lang / "RedirectedResources",
                xuat_text_dir=bep_root / "Translation" / detected_lang / "Text",
            )

        return cls(
            bepinex_root=p,
            redirected_dir=p / "Translation" / lang / "RedirectedResources",
            xuat_text_dir=p / "Translation" / lang / "Text",
        )


class BepInExGuard:
    """Fast lookup index over already-implemented RedirectedResources bundles."""

    def __init__(self, bepinex_hint: Optional[Path | str] = None, lang: str = "en") -> None:
        self.paths = BepInExPaths.resolve(bepinex_hint, lang=lang)
        self.by_filename: Dict[str, Path] = {}
        self._scan()

    @property
    def is_active(self) -> bool:
        return bool(self.paths.redirected_dir and self.paths.redirected_dir.is_dir())

    def _scan(self) -> None:
        if not self.is_active or self.paths.redirected_dir is None:
            return
        for entry in os.scandir(self.paths.redirected_dir):
            if entry.is_file() and entry.name.lower().endswith((".unity3d", ".asset")):
                self.by_filename[entry.name.lower()] = Path(entry.path)

    def check(self, asset_name: str) -> Tuple[bool, str]:
        """
        Check whether an asset is already present in RedirectedResources.
        Returns (is_already_present, status_message).
        """
        if not self.is_active:
            return False, "BepInEx check inactive (set --bepinex to enable)"

        base = Path(asset_name).name.lower()
        if base in self.by_filename:
            return True, f"ALREADY IN PATCH: {self.by_filename[base].name}"

        normalized = base.replace("storydata_storydata_", "storydata_")
        if normalized in self.by_filename:
            return True, f"ALREADY IN PATCH: {self.by_filename[normalized].name}"

        for existing_name, existing_path in self.by_filename.items():
            if existing_name.endswith(f"_{base}") or base.endswith(f"_{existing_name}"):
                return True, f"ALREADY IN PATCH: {existing_path.name}"

        return False, "NEW (not yet in RedirectedResources)"
