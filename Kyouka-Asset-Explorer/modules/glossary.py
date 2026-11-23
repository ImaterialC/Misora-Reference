#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
modules/glossary.py
===================
Developer Codename Glossary and Identifier Decoder for Princess Connect! Re:Dive.

Translates internal Cygames asset prefixes, SQLite table codenames, and
numeric Story/Unit IDs into clear, human-readable explanations for fan translators.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GlossaryTerm:
    """Single entry in the Cygames developer codename glossary."""

    code: str
    meaning: str
    scope: str
    notes: str


ASSET_GLOSSARY: List[GlossaryTerm] = [
    # CDN Top-Level Prefixes
    GlossaryTerm(
        "a/",
        "Unity AssetBundle (.unity3d)",
        "CDN Path",
        "Contains story scripts, UI prefabs, movie subtitles, textures, and Spine rigs. Primary target for translation.",
    ),
    GlossaryTerm(
        "m/",
        "Criware Video (.usm)",
        "CDN Path",
        "Anime cutscenes, openings, and Union Burst movies. Subtitle text lives in a/ bundles instead.",
    ),
    GlossaryTerm(
        "v/",
        "Character Voice Audio (.acb/.awb)",
        "CDN Path",
        "Voiced story dialogue and character battle/menu lines. Useful as tone/context reference.",
    ),
    GlossaryTerm(
        "b/",
        "Background Music (.acb/.awb)",
        "CDN Path",
        "In-game BGM tracks (no translatable text).",
    ),
    GlossaryTerm(
        "s/",
        "Sound Effects (.acb/.awb)",
        "CDN Path",
        "UI clicks, combat impacts, and ambient SE (no translatable text).",
    ),
    # Developer Feature / Table Codenames
    GlossaryTerm(
        "hatsune",
        "Story Events (Monthly Limited Events)",
        "DB & CDN",
        "Named after JP's very first story event ('Hatsune's Present', 2018). Used for ALL monthly story events.",
    ),
    GlossaryTerm(
        "shiori",
        "Side Stories (Permanent Event Archive)",
        "DB & CDN",
        "Wordplay on Japanese 'shiori' (bookmark) and character Shiori. Stores permanently archived events.",
    ),
    GlossaryTerm(
        "storydata",
        "ADV Visual Novel Dialogue Script",
        "CDN Bundle",
        "Encrypted binary dialogue script inside a/storydata_storydata_<id>.unity3d (not stored in master.db).",
    ),
    GlossaryTerm(
        "adv",
        "Adventure / Visual Novel Story Mode",
        "DB & CDN",
        "Prefix for story backgrounds (bg_adv), voices (vo_adv), and scene scripts.",
    ),
    GlossaryTerm(
        "room",
        "Guildhouse (Furniture & Chirping)",
        "DB & CDN",
        "Covers room_unit_comments, room_chat_scenario, room_chat_info, and room_item descriptions.",
    ),
    GlossaryTerm(
        "mypage",
        "Home Screen (MyPage)",
        "DB & CDN",
        "Home screen character dialogue, dynamic backgrounds, and promotional banners.",
    ),
    GlossaryTerm(
        "still",
        "Story / Bond CG Illustrations",
        "DB & CDN",
        "Full-screen event or bond artwork displayed during visual novel scenes.",
    ),
    GlossaryTerm(
        "telop",
        "On-Screen Title Card / Overlay",
        "ADV Script",
        "Floating episode/chapter title text rendered over scenes (ADV command: title_telop).",
    ),
    GlossaryTerm(
        "emblem",
        "Player Titles / Profile Badges",
        "DB & CDN",
        "Unlockable titles earned from events, Clan Battle rankings, and milestones.",
    ),
    GlossaryTerm(
        "dear",
        "Trust / Affection Sub-Events",
        "DB & CDN",
        "Special character trust episodes commonly used in collaborations and special events.",
    ),
    GlossaryTerm(
        "tower",
        "Luna Tower",
        "DB & CDN",
        "Luna Tower floor data and crossover stories between characters (tower_story_*).",
    ),
    GlossaryTerm(
        "clan_battle",
        "Clan Battle (Guild Raid)",
        "DB & CDN",
        "Monthly guild boss parameters, boss lore, phase rules, and reward text.",
    ),
    GlossaryTerm(
        "tdf",
        "Dimension Fault",
        "DB & CDN",
        "Multi-phase endgame exploration mode.",
    ),
    GlossaryTerm(
        "abyss",
        "Abyssal / Deep Zone Quests",
        "DB & CDN",
        "High-difficulty elemental quests.",
    ),
    GlossaryTerm(
        "talent",
        "Elemental Attribute System",
        "DB & CDN",
        "Fire, Water, Wind, Light, Dark attributes and Princess Knight progression.",
    ),
    GlossaryTerm(
        "er_message",
        "System Error & Network Pop-ups",
        "master.db",
        "Connection error prompts, maintenance notices, and input validation dialogs.",
    ),
    GlossaryTerm(
        "unit_enemy",
        "Monster Lore & Bestiary Descriptions",
        "master.db",
        "Flavor text and encyclopedia descriptions for monsters and bosses.",
    ),
    GlossaryTerm(
        "enemy_parameter",
        "Enemy Wave Stats & Display Names",
        "master.db",
        "Contains the raw monster display names shown during combat waves.",
    ),
    GlossaryTerm(
        "glossary",
        "In-Game Lore Dictionary",
        "master.db",
        "Worldbuilding terms and definitions stored in glossary_detail.",
    ),
    GlossaryTerm(
        "spine",
        "Spine2D Chibi Animation Rig",
        "CDN Bundle",
        "2D skeletal models used in battle and Guildhouse (contains no translatable text).",
    ),
    GlossaryTerm(
        "prefab",
        "Unity UI Prefab Layout",
        "CDN Bundle",
        "Static UI buttons, headers, and config labels not loaded from master.db.",
    ),
    GlossaryTerm(
        "movie_subtitle",
        "Cutscene Subtitle Track",
        "CDN Bundle",
        "Unity MonoBehaviour containing timed recordList entries (exported as JSON).",
    ),
]


def decode_story_id(story_id: str) -> str:
    """Interpret a 7-digit Priconne Story ID into its narrative category."""
    sid = story_id.strip()
    if not sid.isdigit():
        return "Non-standard / Custom Story ID"
    if sid.startswith("0000"):
        return "Prologue / Opening Tutorial Story"
    if sid.startswith("1") and len(sid) == 7:
        chara_base = sid[:4]
        ep = int(sid[4:])
        return f"Character Bond Story (Chara {chara_base}, Episode {ep})"
    if sid.startswith("2"):
        return "Main Story Episode"
    if sid.startswith("3"):
        return "Guild Story Episode"
    if sid.startswith("4"):
        return "Extra / Birthday / Special Story"
    if sid.startswith("5"):
        return "Story Event or Side Story Episode (hatsune / shiori)"
    return "Special / Miscellaneous Story ID"


def decode_unit_id(unit_id: str) -> str:
    """Interpret a 6-digit Priconne Unit ID into playable, enemy, or NPC category."""
    uid = unit_id.strip()
    if not uid.isdigit() or len(uid) != 6:
        return "Non-standard Unit ID"
    prefix = uid[0]
    if prefix == "1":
        return f"Playable Character (Base ID {uid[:4]}, Rarity/Variant Suffix {uid[4:]})"
    if prefix == "3":
        return f"Monster / Enemy Unit (ID {uid})"
    if prefix == "5":
        return f"Story-Only NPC / Support Character (ID {uid})"
    return f"Special Unit Type (ID {uid})"


def search_glossary(keyword: str = "") -> List[GlossaryTerm]:
    """Filter glossary terms by case-insensitive substring across all fields."""
    kw = keyword.lower().strip()
    if not kw:
        return list(ASSET_GLOSSARY)
    return [
        term
        for term in ASSET_GLOSSARY
        if kw in f"{term.code} {term.meaning} {term.scope} {term.notes}".lower()
    ]


def explain_asset_name(target: str) -> List[str]:
    """
    Analyze a cryptic Cygames asset path, SQLite table name, or numeric ID
    and return human-readable explanations.
    """
    clean = target.strip()
    lower = clean.lower()
    notes: List[str] = []

    if clean.isdigit():
        if len(clean) == 7:
            notes.append(f"[Story ID {clean}] {decode_story_id(clean)}")
        elif len(clean) == 6:
            notes.append(f"[Unit ID {clean}] {decode_unit_id(clean)}")

    for term in ASSET_GLOSSARY:
        code = term.code.lower()
        if code.endswith("/"):
            if lower.startswith(code):
                notes.append(f"[{term.code}] {term.meaning} -- {term.notes}")
        elif re.search(rf"(^|[^a-z0-9]){re.escape(code)}([^a-z0-9]|$)", lower) or (
            len(code) >= 4 and code in lower
        ):
            notes.append(f"[{term.code}] {term.meaning} -- {term.notes}")

    m_story = re.search(r"storydata[_-](\d{7})", lower)
    if m_story:
        notes.append(f"[Embedded Story ID {m_story.group(1)}] {decode_story_id(m_story.group(1))}")

    m_unit = re.search(r"(?:unit|chara)[_-](\d{6})", lower)
    if m_unit:
        notes.append(f"[Embedded Unit ID {m_unit.group(1)}] {decode_unit_id(m_unit.group(1))}")

    if not notes:
        notes.append("No known developer codename matched. Inspect the SQLite table or bundle contents directly.")
    return notes
