#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kyouka-Asset-Explorer.py
========================
All-in-One Localization Explorer, Developer Glossary, JP CDN Bridge, and
Story Asset Extractor for Princess Connect! Re:Dive.

Designed for international fan translation teams:
    1. Global Full-Text Search across EVERY text column in `master.db`.
    2. Automatic grouping of SQLite tables into translator-friendly category folders.
    3. Excel-safe CSV (UTF-8 BOM) & CAT-ready `.translation.json` export.
    4. Safe `master.db` translation re-injector (writes a patched copy, never mutates original).
    5. Built-in Cygames Developer Codename Glossary & Story/Unit ID Decoder.
    6. Official JP CDN Bridge (`prd-priconne-redive.akamaized.net`) with MD5 verification
       and optional BepInEx `RedirectedResources` duplicate protection.
    7. Standalone lossless `.unity3d` story script (v2 `.txt`) & cutscene subtitle (`.json`)
       extractor and repacker.

Interactive Mode:
    python Kyouka-Asset-Explorer.py --db master.db

CLI Quick Commands:
    python Kyouka-Asset-Explorer.py --db master.db search "コボルト"
    python Kyouka-Asset-Explorer.py --db master.db export-category 07_monsters_and_enemies
    python Kyouka-Asset-Explorer.py --db master.db export-all
    python Kyouka-Asset-Explorer.py --db master.db export-story-index
    python Kyouka-Asset-Explorer.py --db master.db reinject-db
    python Kyouka-Asset-Explorer.py glossary hatsune
    python Kyouka-Asset-Explorer.py decode a/storydata_storydata_1058001.unity3d
    python Kyouka-Asset-Explorer.py extract-bundles
    python Kyouka-Asset-Explorer.py repack-bundles
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules import __version__
from modules.bepinex_guard import BepInExGuard
from modules.cdn_bridge import CDNManifestEntry, JPCDNBridge
from modules.db_explorer import PriconneDBExplorer, get_category_description
from modules.glossary import explain_asset_name, search_glossary
from modules.story_codec import StoryCodecError, extract_bundle, repack_bundle


def truncate_line(text: str, max_len: int = 75) -> str:
    clean = text.replace("\r", " ").replace("\n", "\\n")
    return clean if len(clean) <= max_len else clean[: max_len - 3] + "..."


def print_glossary_table(keyword: str = "") -> None:
    terms = search_glossary(keyword)
    print("\n" + "=" * 96)
    print("             KYOUKA ASSET EXPLORER - DEVELOPER CODENAME GLOSSARY")
    print("=" * 96)
    print(f"{'Code':<18} {'Scope':<12} {'Meaning & Translator Notes'}")
    print("-" * 96)
    if not terms:
        print(f"  No glossary entries matched {keyword!r}.")
    for t in terms:
        print(f"{t.code:<18} {t.scope:<12} {t.meaning}")
        print(f"{'':<31} -> {t.notes}")
    print("=" * 96)


def interactive_global_search(explorer: PriconneDBExplorer, export_root: Path) -> None:
    keyword = input("\nEnter exact text seen in-game (JP or EN): ").strip()
    if not keyword:
        return

    print(f"\n[Scanning all text tables in {explorer.db_path.name} for {keyword!r}...]")
    hits_by_table = explorer.global_search(keyword)

    if not hits_by_table:
        print("  No matches found in master.db.")
        print("  Hint: Main/Event Story scripts live in JP CDN AssetBundles (Option 7),")
        print("        and static Unity button labels live in UI prefabs.")
        return

    matched_tables = list(hits_by_table.keys())
    print("\n" + "=" * 98)
    print(f"{'#':<4} {'Table Name':<32} {'Category Folder':<26} {'Hits':<6} {'Sample Match'}")
    print("-" * 98)
    for idx, tbl in enumerate(matched_tables, start=1):
        hits = hits_by_table[tbl]
        sample = f"[{hits[0].column}] {truncate_line(hits[0].matched_text, 40)}"
        print(f"{idx:<4} {tbl:<32} {hits[0].category:<26} {len(hits):<6} {sample}")
    print("=" * 98)

    while True:
        print("\nNext Action:")
        print("  [v <num>]  Inspect detailed matches for table #<num> (e.g. 'v 1')")
        print("  [e <num>]  Export ONLY table #<num> (CSV + Translation JSON)")
        print("  [f <num>]  Export ENTIRE Category Folder related to table #<num>")
        print("  [0]        Back to main menu")

        cmd = input("Action: ").strip()
        if not cmd or cmd == "0":
            break

        parts = cmd.split()
        if len(parts) != 2 or not parts[1].isdigit():
            print("[!] Invalid format. Examples: 'v 1', 'e 1', 'f 1'.")
            continue

        action, num = parts[0].lower(), int(parts[1])
        if not (1 <= num <= len(matched_tables)):
            print(f"[!] Number must be between 1 and {len(matched_tables)}.")
            continue

        selected_table = matched_tables[num - 1]
        selected_hits = hits_by_table[selected_table]
        selected_cat = selected_hits[0].category

        if action == "v":
            print(f"\n--- Matches in '{selected_table}' (Folder: {selected_cat}) ---")
            for h in selected_hits[:30]:
                print(f"  [{h.pk_value}] ({h.column}): {truncate_line(h.matched_text, 100)}")
            if len(selected_hits) > 30:
                print(f"  ... ({len(selected_hits) - 30} more matches)")
        elif action == "e":
            out_dir = export_root / selected_cat
            files = explorer.export_table(selected_table, out_dir)
            print(f"\n[Exported Table] '{selected_table}' -> {out_dir}")
            for fp in files:
                print(f"  + {fp.name}")
        elif action == "f":
            cat_dir, count = explorer.export_category(selected_cat, export_root)
            print(f"\n[Exported Category Folder] '{selected_cat}' ({count} tables) -> {cat_dir}")
        else:
            print("[!] Unknown command. Use 'v', 'e', 'f', or '0'.")


def interactive_cdn_flow(
    explorer: Optional[PriconneDBExplorer],
    bridge: JPCDNBridge,
    guard: BepInExGuard,
    input_dir: Path,
    text_dir: Path,
) -> None:
    print("\n--- JP CDN Asset Bridge ---")
    print(f"  Manifest Status : {bridge.backend_status}")
    print(f"  BepInEx Guard   : {'ACTIVE (' + str(len(guard.by_filename)) + ' bundles)' if guard.is_active else 'Inactive'}")
    print("  1. Search Story in master.db -> Fetch from JP CDN -> Auto-Extract")
    print("  2. Search JP CDN Manifest Directly -> Download -> Auto-Extract")
    print("  0. Back")
    sub = input("Choose [0-2]: ").strip()

    entries_to_fetch: List[CDNManifestEntry] = []

    if sub == "1":
        if explorer is None:
            print("[!] master.db is not loaded.")
            return
        kw = input("Enter Story ID or title keyword (JP/EN): ").strip()
        if not kw:
            return
        stories = explorer.search_stories(kw)
        if not stories:
            print("  No matching stories found in master.db.")
            return

        print(f"\nFound {len(stories)} story record(s):")
        for idx, s in enumerate(stories[:20], start=1):
            sub_t = f" - {s['sub_title']}" if s["sub_title"] else ""
            print(f"  {idx:<3} [{s['story_id']}] {s['title']}{sub_t}  ({s['expected_cdn_bundle']})")

        sel = input("Select story # to download from JP CDN (0 to cancel): ").strip()
        if not sel.isdigit() or not (1 <= int(sel) <= min(len(stories), 20)):
            return
        chosen = stories[int(sel) - 1]
        entries_to_fetch = bridge.search(chosen["bundle_hint"])
        if not entries_to_fetch:
            print(f"  [!] '{chosen['bundle_hint']}' not found in loaded JP CDN manifest.")
            return

    elif sub == "2":
        kw = input("Enter manifest keyword (e.g. storydata_1058, subtitle, hatsune): ").strip()
        if not kw:
            return
        matches = bridge.search(kw)
        if not matches:
            print("  No matching assets found in loaded JP CDN manifest.")
            return

        print(f"\nFound {len(matches)} asset(s) (showing up to 25):")
        for idx, e in enumerate(matches[:25], start=1):
            print(f"  {idx:<3} {e.name:<56} ({e.human_size})")

        sel = input("Enter #, 'all' (first 25), or '0' to cancel: ").strip().lower()
        if sel == "all":
            entries_to_fetch = matches[:25]
        elif sel.isdigit() and 1 <= int(sel) <= min(len(matches), 25):
            entries_to_fetch = [matches[int(sel) - 1]]
        else:
            return
    else:
        return

    for entry in entries_to_fetch:
        print(f"\n>>> Asset: {entry.name} ({entry.human_size})")
        for note in explain_asset_name(entry.name)[:2]:
            print(f"    Glossary : {note}")
        already_present, guard_msg = guard.check(entry.name)
        print(f"    BepInEx  : {guard_msg}")
        if already_present:
            ans = input("    Already exists in RedirectedResources. Download anyway? [y/N]: ").strip().lower()
            if ans != "y":
                print("    Skipped.")
                continue

        try:
            print(f"    Fetching : {entry.pool_url}")
            bundle_path = bridge.download(entry, input_dir)
            print(f"    [OK] Saved -> {bundle_path}")
            if bundle_path.suffix.lower() == ".unity3d":
                try:
                    kind, out_txt = extract_bundle(bundle_path, text_dir)
                    print(f"    [OK] Auto-extracted ({kind}) -> {out_txt}")
                except StoryCodecError as exc:
                    print(f"    [Info] Auto-extract skipped: {exc}")
        except Exception as exc:
            print(f"    [ERR] {exc}")


def run_batch_extract(input_dir: Path, text_dir: Path) -> None:
    input_dir.mkdir(parents=True, exist_ok=True)
    bundles = sorted(input_dir.rglob("*.unity3d"))
    if not bundles:
        print(f"\n[!] No .unity3d files found in: {input_dir}")
        print("    Drop story or subtitle .unity3d bundles into input/ and try again.")
        return

    ok = skipped = 0
    print(f"\n[Extracting {len(bundles)} bundle(s) from {input_dir} -> {text_dir}]")
    for bp in bundles:
        try:
            kind, out_path = extract_bundle(bp, text_dir)
            print(f"  [OK]   {bp.name} ({kind}) -> {out_path.name}")
            ok += 1
        except StoryCodecError as exc:
            print(f"  [SKIP] {bp.name}: {exc}")
            skipped += 1
    print(f"\nDone: {ok} extracted, {skipped} skipped.")


def run_batch_repack(input_dir: Path, text_dir: Path, output_dir: Path) -> None:
    bundles = sorted(input_dir.rglob("*.unity3d"))
    if not bundles:
        print(f"\n[!] No original .unity3d bundles found in: {input_dir}")
        return

    ok = skipped = 0
    print(f"\n[Repacking bundles from {input_dir} + {text_dir} -> {output_dir}]")
    for bp in bundles:
        tl_txt = text_dir / f"{bp.stem}.txt"
        tl_json = text_dir / f"{bp.stem}.json"
        tl_file = tl_txt if tl_txt.is_file() else (tl_json if tl_json.is_file() else None)
        if tl_file is None:
            print(f"  [SKIP] {bp.name}: no matching .txt or .json in text/")
            skipped += 1
            continue

        out_bundle = output_dir / bp.name
        try:
            status = repack_bundle(bp, tl_file, out_bundle)
            print(f"  [OK]   {bp.name} <- {tl_file.name} [{status}]")
            ok += 1
        except StoryCodecError as exc:
            print(f"  [ERR]  {bp.name}: {exc}")
            skipped += 1
    print(f"\nDone: {ok} repacked into {output_dir}, {skipped} skipped/failed.")


def run_interactive_menu(
    explorer: Optional[PriconneDBExplorer],
    bridge: JPCDNBridge,
    guard: BepInExGuard,
    export_root: Path,
    input_dir: Path,
    text_dir: Path,
    output_dir: Path,
) -> None:
    while True:
        if explorer is not None:
            grouped = explorer.get_tables_by_category()
            total_tables = sum(len(v) for v in grouped.values())
            db_status = f"{explorer.db_path.name} ({total_tables} text tables)"
        else:
            grouped = {}
            total_tables = 0
            db_status = "NOT FOUND (place master.db in this folder)"

        print("\n" + "=" * 84)
        print(f"        KYOUKA ASSET EXPLORER v{__version__} - PRICONNE RE:DIVE TRANSLATION SUITE")
        print("=" * 84)
        print(f"  Database      : {db_status}")
        print(f"  JP CDN Bridge : {bridge.backend_status}")
        print(f"  BepInEx Guard : {'ACTIVE' if guard.is_active else 'Inactive (pass --bepinex)'}")
        print("=" * 84)
        print("  [master.db Localization]")
        print("    1. Global Full-Text Search   (Find ANY in-game text -> Export table or folder)")
        print("    2. Export Category Folder    (Units, Skills, Guildhouse, Monsters, UI, etc.)")
        print("    3. Export ALL master.db Text (Dump entire text corpus organized by folders)")
        print("    4. Export Story CDN Index    (Generate Story ID -> .unity3d mapping CSV)")
        print("    5. Re-Inject Translations    (Build patched master_patched.db from JSON)")
        print("  [Glossary, JP CDN & Story Bundles]")
        print("    6. Developer Codename Glossary & Asset/ID Decoder")
        print("    7. JP CDN Asset Bridge       (Download Story/Subtitle bundles & auto-extract)")
        print("    8. Extract Local .unity3d    (input/*.unity3d -> text/*.txt or *.json)")
        print("    9. Repack  Local .unity3d    (input + text -> verified output/*.unity3d)")
        print("    0. Exit")
        print("-" * 84)

        try:
            choice = input("Choose an option [0-9]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if choice == "0":
            print("Goodbye!")
            break

        elif choice in ("1", "2", "3", "4", "5") and explorer is None:
            print("\n[!] master.db was not found.")
            print("    Download the latest decrypted master.db and place it next to Kyouka-Asset-Explorer.py.")
            continue

        elif choice == "1" and explorer is not None:
            interactive_global_search(explorer, export_root)

        elif choice == "2" and explorer is not None:
            categories = list(grouped.keys())
            print("\nAvailable Localization Category Folders:")
            print("-" * 84)
            for idx, cid in enumerate(categories, start=1):
                desc = get_category_description(cid)
                print(f"  {idx:<3} {cid:<28} ({len(grouped[cid]):>3} tables) - {desc}")
            print("-" * 84)
            sel = input("Enter category # to export (0 to cancel): ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(categories):
                cid = categories[int(sel) - 1]
                cat_dir, count = explorer.export_category(cid, export_root)
                print(f"\n[Done] Exported {count} tables into: {cat_dir}")

        elif choice == "3" and explorer is not None:
            confirm = input(f"\nExport ALL {total_tables} text tables to '{export_root}'? [y/N]: ").strip().lower()
            if confirm == "y":
                summary = explorer.export_all_categories(export_root)
                for cid, count in summary.items():
                    print(f"  + {cid:<28} : {count} tables")
                print(f"\n[Done] All exports saved in: {export_root}")

        elif choice == "4" and explorer is not None:
            out_csv = explorer.export_story_asset_index(export_root / "01_story_metadata")
            if out_csv:
                print(f"\n[Done] Story CDN Asset Index saved to: {out_csv}")
            else:
                print("\n[!] No story_detail tables found in this database.")

        elif choice == "5" and explorer is not None:
            patched = output_dir / "master_patched.db"
            print(f"\n[Scanning '{export_root}' for *.translation.json files...]")
            files_used, rows_updated = explorer.reinject_json_translations(export_root, patched)
            print(f"[Done] Applied {rows_updated:,} translated cell(s) from {files_used} file(s).")
            print(f"       Patched database written to: {patched}")

        elif choice == "6":
            print("\n  a. Browse / Search Developer Codename Glossary")
            print("  b. Decode an Asset Path, Table Name, or Story/Unit ID")
            sub = input("Choose [a/b]: ").strip().lower()
            if sub == "a":
                kw = input("Filter keyword (Enter for all): ").strip()
                print_glossary_table(kw)
            elif sub == "b":
                target = input("Enter filename, table name, or ID (e.g. a/storydata_storydata_1058001.unity3d): ").strip()
                if target:
                    print(f"\n[Decoded Notes for {target!r}]")
                    for line in explain_asset_name(target):
                        print(f"  - {line}")

        elif choice == "7":
            interactive_cdn_flow(explorer, bridge, guard, input_dir, text_dir)

        elif choice == "8":
            run_batch_extract(input_dir, text_dir)

        elif choice == "9":
            run_batch_repack(input_dir, text_dir, output_dir)

        else:
            print("[!] Invalid choice. Please enter 0-9.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Kyouka-Asset-Explorer",
        description="Unified Priconne Re:Dive localization explorer, glossary, JP CDN bridge, and story extractor.",
    )
    parser.add_argument("--db", type=Path, default=ROOT / "master.db", help="Path to decrypted SQLite master.db")
    parser.add_argument("--out", type=Path, default=ROOT / "exports", help="Root folder for exported CSV/JSON files")
    parser.add_argument("--input", type=Path, default=ROOT / "input", help="Folder for raw .unity3d bundles")
    parser.add_argument("--text", type=Path, default=ROOT / "text", help="Folder for extracted story .txt / subtitle .json")
    parser.add_argument("--output", type=Path, default=ROOT / "output", help="Folder for repacked bundles & patched DB")
    parser.add_argument("--bepinex", type=Path, default=None, help="Optional BepInEx root directory for duplicate checking")
    parser.add_argument("--manifest", type=Path, nargs="*", default=[], help="Optional JP CDN manifest CSV files")

    sub = parser.add_subparsers(dest="command")

    p_s = sub.add_parser("search", help="Global full-text search across master.db")
    p_s.add_argument("keyword", type=str)

    p_c = sub.add_parser("export-category", help="Export all text tables in one category folder")
    p_c.add_argument("category", type=str)

    sub.add_parser("export-all", help="Export all text tables in master.db grouped by folder")
    sub.add_parser("export-story-index", help="Export Story ID -> CDN bundle CSV index")
    sub.add_parser("reinject-db", help="Build output/master_patched.db from translated JSON files")

    p_g = sub.add_parser("glossary", help="Browse or filter the Cygames developer codename glossary")
    p_g.add_argument("keyword", nargs="?", default="")

    p_d = sub.add_parser("decode", help="Decode an asset path, table name, or Story/Unit ID")
    p_d.add_argument("target", type=str)

    sub.add_parser("extract-bundles", help="Extract all .unity3d bundles in input/ to text/")
    sub.add_parser("repack-bundles", help="Repack all translated scripts in text/ to output/")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "glossary":
        print_glossary_table(args.keyword)
        return

    if args.command == "decode":
        for line in explain_asset_name(args.target):
            print(line)
        return

    if args.command == "extract-bundles":
        run_batch_extract(args.input.resolve(), args.text.resolve())
        return

    if args.command == "repack-bundles":
        run_batch_repack(args.input.resolve(), args.text.resolve(), args.output.resolve())
        return

    explorer: Optional[PriconneDBExplorer] = None
    if args.db.is_file():
        explorer = PriconneDBExplorer(args.db)

    try:
        if args.command in ("search", "export-category", "export-all", "export-story-index", "reinject-db"):
            if explorer is None:
                print(f"[Error] master.db not found at: {args.db}")
                sys.exit(1)

            if args.command == "search":
                hits = explorer.global_search(args.keyword)
                for tbl, items in hits.items():
                    print(f"[{items[0].category}] {tbl} ({len(items)} hits)")
                    for h in items[:5]:
                        print(f"    {h.pk_value} | {h.column}: {truncate_line(h.matched_text)}")

            elif args.command == "export-category":
                cat_dir, count = explorer.export_category(args.category, args.out)
                print(f"Exported {count} table(s) -> {cat_dir}")

            elif args.command == "export-all":
                summary = explorer.export_all_categories(args.out)
                for cid, count in summary.items():
                    print(f"{cid}: {count} tables")

            elif args.command == "export-story-index":
                out_csv = explorer.export_story_asset_index(args.out / "01_story_metadata")
                print(f"Saved story index -> {out_csv}" if out_csv else "No story tables found.")

            elif args.command == "reinject-db":
                patched = args.output / "master_patched.db"
                files_used, rows_updated = explorer.reinject_json_translations(args.out, patched)
                print(f"Updated {rows_updated:,} cell(s) from {files_used} file(s) -> {patched}")
            return

        bridge = JPCDNBridge(ROOT, manifest_paths=args.manifest)
        guard = BepInExGuard(args.bepinex)
        run_interactive_menu(
            explorer=explorer,
            bridge=bridge,
            guard=guard,
            export_root=args.out.resolve(),
            input_dir=args.input.resolve(),
            text_dir=args.text.resolve(),
            output_dir=args.output.resolve(),
        )
    finally:
        if explorer is not None:
            explorer.close()


if __name__ == "__main__":
    main()
