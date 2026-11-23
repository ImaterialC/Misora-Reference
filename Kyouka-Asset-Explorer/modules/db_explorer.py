#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
modules/db_explorer.py
======================
Core SQLite master.db explorer, full-text searcher, category folder exporter,
and safe translation re-injector for Princess Connect! Re:Dive.

Zero third-party dependencies (Python Standard Library only).
"""

from __future__ import annotations

import csv
import json
import re
import shutil
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


CATEGORY_RULES: List[Tuple[str, str, List[str]]] = [
    (
        "01_story_metadata",
        "Main Story, Event Story, Character/Guild Story titles & synopses (dialogue scripts live in CDN bundles)",
        [
            r"^story_",
            r"^event_story_",
            r"^hatsune_",
            r"^shiori_",
            r"^tower_story_",
            r"^character_love_",
            r"^still$",
            r"^movie_",
            r"^sub_story_",
            r"^nyx_story_",
            r"^sjr_story_",
        ],
    ),
    (
        "02_tutorial_and_glossary",
        "Tutorials, Glossary definitions, Help pages, and Loading Tips",
        [
            r"^tutorial_",
            r"^glossary_",
            r"^help_",
            r"^tips$",
            r"^guide_",
        ],
    ),
    (
        "03_homescreen_dialogue",
        "Home Screen / MyPage dialogues, unit voice comments, birthday & login greetings",
        [
            r"^unit_comments$",
            r"^unit_mypage_",
            r"^my_page_",
            r"^mypage_",
            r"^birthday_",
            r"^login_bonus_",
            r"^voice_",
            r"^dear_",
        ],
    ),
    (
        "04_guildhouse",
        "Guildhouse (Room) chirping, character interactions, and furniture descriptions",
        [
            r"^room_",
        ],
    ),
    (
        "05_units_and_profiles",
        "Playable character names, bios, guilds, voice actors, and album entries",
        [
            r"^unit_data$",
            r"^unit_profile$",
            r"^unit_introduction$",
            r"^unit_background$",
            r"^unit_rarity$",
            r"^unit_status_",
            r"^actual_unit_",
            r"^chara_",
            r"^guild$",
            r"^album_",
            r"^emblem_",
        ],
    ),
    (
        "06_skills_and_combat",
        "Unit skills, Union Bursts, skill action descriptions, and status ailments",
        [
            r"^skill_",
            r"^sp_skill_",
            r"^ailment_",
            r"^ub_",
            r"^rf_skill_",
        ],
    ),
    (
        "07_monsters_and_enemies",
        "Monster names, boss lore/descriptions, Clan Battle & wave enemy definitions",
        [
            r"^enemy_",
            r"^unit_enemy_",
            r"^clan_battle_",
            r"^boss_",
            r"^wave_",
            r"^tower_enemy_",
            r"^dungeon_",
        ],
    ),
    (
        "08_ui_quests_and_system",
        "System messages, UI text, missions, titles, quests, areas, arenas, shops & gacha",
        [
            r"^system_",
            r"^er_message",
            r"^message_",
            r"^mission_",
            r"^daily_mission_",
            r"^title_",
            r"^quest_",
            r"^area_",
            r"^world_",
            r"^arena_",
            r"^grand_arena_",
            r"^campaign_",
            r"^shop_",
            r"^gacha_",
            r"^banner",
            r"^config_",
            r"^menu_",
            r"^notif",
            r"^text_",
            r"^calendar_",
            r"^stamp",
            r"^clan_",
            r"^unlock_",
        ],
    ),
    (
        "09_items_and_equipment",
        "Items, equipment, unique equipment, EX equipment, and crafting materials",
        [
            r"^item_",
            r"^equipment_",
            r"^unique_equipment_",
            r"^ex_equipment_",
            r"^redeem_",
            r"^memory_piece",
        ],
    ),
]

FALLBACK_CATEGORY = (
    "99_uncategorized_text",
    "Other tables containing text columns (auto-detected from current DB schema)",
)


@dataclass
class TableSchema:
    """Metadata describing a single SQLite table in master.db."""

    name: str
    category: str
    all_columns: List[str]
    text_columns: List[str]
    pk_columns: List[str]
    row_count: int = 0


@dataclass
class SearchHit:
    """Single full-text search match across master.db."""

    table: str
    category: str
    pk_value: str
    column: str
    matched_text: str
    full_row: Dict[str, Any]


def quote_ident(identifier: str) -> str:
    """Safely double-quote a SQLite table or column name."""
    return '"' + identifier.replace('"', '""') + '"'


def classify_table(table_name: str) -> str:
    """Assign a SQLite table name to a localization category folder."""
    lowered = table_name.lower()
    for category_id, _, patterns in CATEGORY_RULES:
        for pattern in patterns:
            if re.search(pattern, lowered):
                return category_id
    return FALLBACK_CATEGORY[0]


def get_category_description(category_id: str) -> str:
    """Return the human-readable description for a category ID."""
    for cid, desc, _ in CATEGORY_RULES:
        if cid == category_id:
            return desc
    return FALLBACK_CATEGORY[1]


class PriconneDBExplorer:
    """Read-only inspector, full-text search engine, and exporter for master.db."""

    TEXT_TYPE_TOKENS = ("TEXT", "CHAR", "CLOB", "STR")

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        if not self.db_path.is_file():
            raise FileNotFoundError(f"Database file not found: {self.db_path}")

        uri = f"file:{self.db_path.resolve().as_posix()}?mode=ro"
        self.conn = sqlite3.connect(uri, uri=True)
        self.conn.row_factory = sqlite3.Row
        self.schemas: Dict[str, TableSchema] = {}
        self._load_schema()

    def close(self) -> None:
        self.conn.close()

    def _load_schema(self) -> None:
        """Inspect sqlite_master and cache schema metadata for every table."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name ASC
            """
        )
        table_names = [row[0] for row in cur.fetchall()]

        for table in table_names:
            cur.execute(f"PRAGMA table_info({quote_ident(table)})")
            cols_info = cur.fetchall()
            all_cols: List[str] = []
            text_cols: List[str] = []
            pk_pairs: List[Tuple[int, str]] = []

            for col in cols_info:
                col_name = col["name"]
                col_type = (col["type"] or "").upper()
                pk_order = col["pk"]

                all_cols.append(col_name)
                if any(tok in col_type for tok in self.TEXT_TYPE_TOKENS):
                    text_cols.append(col_name)
                if pk_order > 0:
                    pk_pairs.append((pk_order, col_name))

            pk_pairs.sort(key=lambda x: x[0])
            pk_cols = [name for _, name in pk_pairs]

            cur.execute(f"SELECT COUNT(*) FROM {quote_ident(table)}")
            row_count = int(cur.fetchone()[0])

            self.schemas[table] = TableSchema(
                name=table,
                category=classify_table(table),
                all_columns=all_cols,
                text_columns=text_cols,
                pk_columns=pk_cols,
                row_count=row_count,
            )

    def get_text_tables(self) -> List[TableSchema]:
        """Return all non-empty tables containing at least one TEXT column."""
        return [s for s in self.schemas.values() if s.text_columns and s.row_count > 0]

    def get_tables_by_category(self, include_empty: bool = False) -> Dict[str, List[TableSchema]]:
        """Group text-bearing tables into their logical category folders."""
        grouped: Dict[str, List[TableSchema]] = defaultdict(list)
        for schema in self.schemas.values():
            if not schema.text_columns:
                continue
            if not include_empty and schema.row_count == 0:
                continue
            grouped[schema.category].append(schema)
        return dict(sorted(grouped.items()))

    @staticmethod
    def _format_pk(row: sqlite3.Row, schema: TableSchema) -> str:
        if schema.pk_columns:
            return "|".join(f"{col}={row[col]}" for col in schema.pk_columns)
        return f"rowid={row['_internal_rowid']}"

    def global_search(
        self,
        keyword: str,
        case_sensitive: bool = False,
        max_hits_per_table: int = 50,
    ) -> Dict[str, List[SearchHit]]:
        """Scan EVERY text column across EVERY table in master.db for keyword."""
        if not keyword:
            return {}

        cur = self.conn.cursor()
        hits_by_table: Dict[str, List[SearchHit]] = {}
        escaped_kw = keyword.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

        for schema in self.get_text_tables():
            where_clauses = [
                f"{quote_ident(col)} LIKE ? ESCAPE '\\'" for col in schema.text_columns
            ]
            params: List[Any] = [f"%{escaped_kw}%"] * len(schema.text_columns)
            params.append(max_hits_per_table)

            select_prefix = "" if schema.pk_columns else "rowid AS _internal_rowid, "
            sql = (
                f"SELECT {select_prefix}* FROM {quote_ident(schema.name)} "
                f"WHERE {' OR '.join(where_clauses)} "
                f"LIMIT ?"
            )

            try:
                cur.execute(sql, params)
                rows = cur.fetchall()
            except sqlite3.Error:
                continue

            table_hits: List[SearchHit] = []
            for row in rows:
                pk_str = self._format_pk(row, schema)
                row_dict = {k: row[k] for k in row.keys() if k != "_internal_rowid"}
                for col in schema.text_columns:
                    val = row[col]
                    if not isinstance(val, str) or not val:
                        continue
                    matched = keyword in val if case_sensitive else keyword.lower() in val.lower()
                    if matched:
                        table_hits.append(
                            SearchHit(
                                table=schema.name,
                                category=schema.category,
                                pk_value=pk_str,
                                column=col,
                                matched_text=val,
                                full_row=row_dict,
                            )
                        )

            if table_hits:
                hits_by_table[schema.name] = table_hits

        return hits_by_table

    def search_stories(self, keyword: str, limit: int = 50) -> List[Dict[str, str]]:
        """Find Story IDs and episode titles across story metadata tables."""
        candidate_tables = (
            "story_detail",
            "event_story_detail",
            "tower_story_detail",
            "shiori_event_story_detail",
        )
        cur = self.conn.cursor()
        results: List[Dict[str, str]] = []

        for tbl in candidate_tables:
            if tbl not in self.schemas:
                continue
            cols = set(self.schemas[tbl].all_columns)
            if "story_id" not in cols or "title" not in cols:
                continue

            sub_col = "sub_title" if "sub_title" in cols else None
            where = ['CAST("story_id" AS TEXT) LIKE ?', '"title" LIKE ?']
            params: List[Any] = [f"%{keyword}%", f"%{keyword}%"]
            if sub_col:
                where.append(f'"{sub_col}" LIKE ?')
                params.append(f"%{keyword}%")
            params.append(limit)

            cur.execute(
                f'SELECT * FROM "{tbl}" WHERE {" OR ".join(where)} LIMIT ?',
                params,
            )
            for row in cur.fetchall():
                sid = str(row["story_id"])
                padded = sid.zfill(7) if sid.isdigit() else sid
                results.append(
                    {
                        "table": tbl,
                        "story_id": sid,
                        "title": str(row["title"] or ""),
                        "sub_title": str(row[sub_col] or "") if sub_col else "",
                        "bundle_hint": f"storydata_{padded}",
                        "expected_cdn_bundle": f"a/storydata_storydata_{padded}.unity3d",
                    }
                )
        return results

    def export_table(
        self,
        table_name: str,
        output_dir: Path,
        formats: Sequence[str] = ("csv", "json"),
        only_text_columns: bool = False,
    ) -> List[Path]:
        """Export a single SQLite table to Excel-safe CSV (UTF-8 BOM) and CAT-ready JSON."""
        if table_name not in self.schemas:
            raise ValueError(f"Table '{table_name}' does not exist in database.")

        schema = self.schemas[table_name]
        output_dir.mkdir(parents=True, exist_ok=True)
        created_files: List[Path] = []

        cur = self.conn.cursor()
        select_prefix = "" if schema.pk_columns else "rowid AS _internal_rowid, "
        cur.execute(f"SELECT {select_prefix}* FROM {quote_ident(table_name)}")
        rows = cur.fetchall()
        if not rows:
            return created_files

        if "csv" in formats:
            csv_path = output_dir / f"{table_name}.csv"
            export_cols = (
                list(dict.fromkeys(schema.pk_columns + schema.text_columns))
                if only_text_columns
                else list(schema.all_columns)
            )
            with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                header: List[str] = []
                for col in export_cols:
                    header.append(col)
                    if col in schema.text_columns:
                        header.append(f"{col}_translation")
                writer.writerow(header)

                for row in rows:
                    out_row: List[Any] = []
                    for col in export_cols:
                        val = row[col]
                        out_row.append("" if val is None else val)
                        if col in schema.text_columns:
                            out_row.append("")
                    writer.writerow(out_row)
            created_files.append(csv_path)

        if "json" in formats:
            json_path = output_dir / f"{table_name}.translation.json"
            entries: List[Dict[str, Any]] = []
            for row in rows:
                pk_str = self._format_pk(row, schema)
                for col in schema.text_columns:
                    val = row[col]
                    if isinstance(val, str) and val.strip():
                        entries.append(
                            {
                                "key": f"{table_name}:{pk_str}:{col}",
                                "table": table_name,
                                "pk": pk_str,
                                "column": col,
                                "source": val,
                                "translation": "",
                            }
                        )
            payload = {
                "meta": {
                    "table": table_name,
                    "category": schema.category,
                    "primary_keys": schema.pk_columns,
                    "text_columns": schema.text_columns,
                    "entry_count": len(entries),
                },
                "entries": entries,
            }
            with json_path.open("w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            created_files.append(json_path)

        return created_files

    def export_category(
        self,
        category_id: str,
        base_export_dir: Path,
        formats: Sequence[str] = ("csv", "json"),
    ) -> Tuple[Path, int]:
        """Export every text-bearing table belonging to a category folder."""
        grouped = self.get_tables_by_category(include_empty=False)
        if category_id not in grouped:
            raise ValueError(f"Category '{category_id}' not found or has no text tables.")

        cat_dir = base_export_dir / category_id
        exported_tables = 0
        for schema in grouped[category_id]:
            if self.export_table(schema.name, cat_dir, formats=formats):
                exported_tables += 1
        return cat_dir, exported_tables

    def export_all_categories(
        self,
        base_export_dir: Path,
        formats: Sequence[str] = ("csv", "json"),
    ) -> Dict[str, int]:
        """Export every text-bearing table in master.db grouped by category folder."""
        grouped = self.get_tables_by_category(include_empty=False)
        summary: Dict[str, int] = {}
        for category_id in grouped:
            _, count = self.export_category(category_id, base_export_dir, formats=formats)
            summary[category_id] = count
        return summary

    def export_story_asset_index(self, output_dir: Path) -> Optional[Path]:
        """Export Story ID -> expected JP CDN Unity AssetBundle CSV index."""
        candidate_tables = [
            "story_detail",
            "event_story_detail",
            "tower_story_detail",
            "shiori_event_story_detail",
        ]
        existing = [t for t in candidate_tables if t in self.schemas]
        if not existing:
            return None

        output_dir.mkdir(parents=True, exist_ok=True)
        out_path = output_dir / "story_cdn_asset_index.csv"
        cur = self.conn.cursor()
        records: List[Dict[str, Any]] = []

        for tbl in existing:
            schema = self.schemas[tbl]
            cols = set(schema.all_columns)
            id_col = "story_id" if "story_id" in cols else schema.pk_columns[0]
            title_col = "title" if "title" in cols else None
            sub_col = "sub_title" if "sub_title" in cols else None
            group_col = "story_group_id" if "story_group_id" in cols else None

            cur.execute(f"SELECT * FROM {quote_ident(tbl)}")
            for row in cur.fetchall():
                sid = str(row[id_col])
                padded_sid = sid.zfill(7) if sid.isdigit() else sid
                records.append(
                    {
                        "source_table": tbl,
                        "story_group_id": row[group_col] if group_col else "",
                        "story_id": sid,
                        "title": row[title_col] if title_col else "",
                        "sub_title": row[sub_col] if sub_col else "",
                        "expected_cdn_bundle": f"a/storydata_storydata_{padded_sid}.unity3d",
                    }
                )

        with out_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "source_table",
                    "story_group_id",
                    "story_id",
                    "title",
                    "sub_title",
                    "expected_cdn_bundle",
                ],
            )
            writer.writeheader()
            writer.writerows(records)

        return out_path

    def reinject_json_translations(self, translation_root: Path, patched_db_path: Path) -> Tuple[int, int]:
        """
        Apply non-empty translations from `*.translation.json` files onto a safe
        COPY of master.db (never mutating the original database).

        Returns (files_processed, rows_updated).
        """
        patched_db_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.db_path, patched_db_path)

        json_files = sorted(translation_root.rglob("*.translation.json"))
        if not json_files:
            return 0, 0

        conn = sqlite3.connect(str(patched_db_path))
        files_used = 0
        rows_updated = 0

        try:
            cur = conn.cursor()
            for jf in json_files:
                payload = json.loads(jf.read_text(encoding="utf-8"))
                entries = payload.get("entries", [])
                file_updates = 0

                for item in entries:
                    tl = item.get("translation", "")
                    if not isinstance(tl, str) or not tl.strip():
                        continue
                    table = item.get("table", "")
                    col = item.get("column", "")
                    pk_str = item.get("pk", "")
                    if table not in self.schemas or col not in self.schemas[table].all_columns:
                        continue

                    where_parts: List[str] = []
                    where_vals: List[Any] = []
                    for token in pk_str.split("|"):
                        if "=" not in token:
                            continue
                        k, v = token.split("=", 1)
                        if k == "rowid":
                            where_parts.append("rowid = ?")
                            where_vals.append(int(v))
                        else:
                            where_parts.append(f"{quote_ident(k)} = ?")
                            where_vals.append(v)

                    if not where_parts:
                        continue

                    sql = (
                        f"UPDATE {quote_ident(table)} "
                        f"SET {quote_ident(col)} = ? "
                        f"WHERE {' AND '.join(where_parts)}"
                    )
                    cur.execute(sql, [tl] + where_vals)
                    if cur.rowcount > 0:
                        rows_updated += cur.rowcount
                        file_updates += cur.rowcount

                if file_updates > 0:
                    files_used += 1

            conn.commit()
        finally:
            conn.close()

        return files_used, rows_updated
