#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_asset_registry.py - Unit & Integration Tests for P1 Asset Registry & Duplicate Detection
"""
import shutil
import tempfile
from pathlib import Path
from asset_registry import (
    BepInExWorkspace,
    AssetIdentity,
    RedirectIndex,
    NamingManager,
    NamingStrategy,
    PreConversionScanner,
    AssetStatus,
    MatchLevel
)


def test_workspace_resolution():
    print("[TEST 1] Workspace Resolution & Boundary Isolation...")
    # Real project path
    real_bep = Path(r"C:\[Gacha]\PriconneRe-TL\src\BepInEx")
    ws1 = BepInExWorkspace.resolve(real_bep)
    assert ws1.bepinex_root == real_bep
    assert ws1.xuat_text_dir == real_bep / "Translation" / "en" / "Text"
    assert ws1.redirected_resources_dir == real_bep / "Translation" / "en" / "RedirectedResources"
    assert ws1.redirected_exists()
    assert ws1.text_exists()

    # Resolving from Text subfolder
    text_sub = real_bep / "Translation" / "en" / "Text"
    ws2 = BepInExWorkspace.resolve(text_sub)
    assert ws2.bepinex_root == real_bep
    assert ws2.xuat_text_dir == text_sub
    assert ws2.redirected_resources_dir == real_bep / "Translation" / "en" / "RedirectedResources"

    # Resolving from RedirectedResources subfolder
    redir_sub = real_bep / "Translation" / "en" / "RedirectedResources"
    ws3 = BepInExWorkspace.resolve(redir_sub)
    assert ws3.bepinex_root == real_bep
    assert ws3.redirected_resources_dir == redir_sub
    print("  -> Passed!")


def test_asset_identity():
    print("[TEST 2] Asset Identity Creation & Normalization...")
    # Case A: folder + basename
    id1 = AssetIdentity.create(Path("storydata/0000011.unity3d"))
    assert id1.folder == "storydata"
    assert id1.basename == "0000011.unity3d"
    assert id1.category == "storydata"
    assert id1.asset_id == "0000011"
    assert id1.flattened_name == "storydata_0000011.unity3d"

    # Case B: already flattened name
    id2 = AssetIdentity.create(Path("storydata_0000011.unity3d"))
    assert id2.category == "storydata"
    assert id2.asset_id == "0000011"
    assert id2.flattened_name == "storydata_0000011.unity3d"

    # Case C: bare story ID
    id3 = AssetIdentity.create(Path("9080155.unity3d"))
    assert id3.category == "storydata"
    assert id3.asset_id == "9080155"
    assert id3.flattened_name == "storydata_9080155.unity3d"
    print("  -> Passed!")


def test_real_redirected_index():
    print("[TEST 3] Real RedirectedResources Indexing & Lookup...")
    real_redir = Path(r"C:\[Gacha]\PriconneRe-TL\src\BepInEx\Translation\en\RedirectedResources")
    idx = RedirectIndex(real_redir)
    print(f"  Indexed {idx.total_count:,} bundles from real project.")
    assert idx.total_count > 2000

    # 0000011 should match storydata_0000011.unity3d
    id_known = AssetIdentity.create(Path("0000011.unity3d"))
    lvl, match, _ = idx.find_match(id_known)
    assert match is not None
    assert match.name.lower() == "storydata_0000011.unity3d"
    assert lvl in (MatchLevel.EXACT_FLATTENED, MatchLevel.NORMALIZED_ID, MatchLevel.BASENAME_UNIQUE)

    # 9080155 is NOT in RedirectedResources
    id_new = AssetIdentity.create(Path("9080155.unity3d"))
    lvl_new, match_new, _ = idx.find_match(id_new)
    assert match_new is None
    assert lvl_new == MatchLevel.NONE
    print("  -> Passed!")


def test_scanner_and_collision_prevention():
    print("[TEST 4] Pre-Conversion Scanner, Duplicate Detection & Collision Safety...")
    real_bep = Path(r"C:\[Gacha]\PriconneRe-TL\src\BepInEx")
    ws = BepInExWorkspace.resolve(real_bep)

    # Create temporary input files with duplicates and collision candidates
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        (tmp_root / "storydata").mkdir()
        (tmp_root / "event").mkdir()

        # 1. An asset that already exists in RedirectedResources (0000011)
        f_existing = tmp_root / "0000011.unity3d"
        f_existing.write_bytes(b"dummy1")

        # 2. A new asset not in RedirectedResources (9080155)
        f_new = tmp_root / "9080155.unity3d"
        f_new.write_bytes(b"dummy2")

        # 3. Two different files with identical basename in different folders (collision test!)
        f_clash1 = tmp_root / "storydata" / "conflict_test.unity3d"
        f_clash2 = tmp_root / "event" / "conflict_test.unity3d"
        f_clash1.write_bytes(b"clash1")
        f_clash2.write_bytes(b"clash2")

        # Test A: Default scan (skip existing, flag collisions)
        scanner = PreConversionScanner(ws, strategy=NamingStrategy.AUTO_REDIRECT)
        input_files = [f_existing, f_new, f_clash1, f_clash2]
        cands = scanner.scan_candidates(input_files, input_root=tmp_root)

        by_stem = {c.identity.file_path.name + ("_" + c.identity.folder if c.identity.folder else ""): c for c in cands}

        # Verify existing asset is marked ALREADY_IMPLEMENTED and action is SKIP
        c_exist = [c for c in cands if c.identity.basename == "0000011.unity3d"][0]
        assert c_exist.status == AssetStatus.ALREADY_IMPLEMENTED
        assert c_exist.action == "SKIP"
        assert c_exist.existing_redirect is not None

        # Verify new asset is marked NEW and action is CONVERT
        c_new = [c for c in cands if c.identity.basename == "9080155.unity3d"][0]
        assert c_new.status == AssetStatus.NEW
        assert c_new.action == "CONVERT"
        assert c_new.proposed_filename == "storydata_9080155.unity3d"

        # Verify clash files: event_conflict_test vs storydata_conflict_test
        # Because folder differs, auto_redirect gives different proposed names:
        # storydata_conflict_test.unity3d vs event_conflict_test.unity3d
        c_clash1 = [c for c in cands if c.identity.folder == "storydata" and c.identity.basename == "conflict_test.unity3d"][0]
        c_clash2 = [c for c in cands if c.identity.folder == "event" and c.identity.basename == "conflict_test.unity3d"][0]
        assert c_clash1.proposed_filename != c_clash2.proposed_filename
        assert c_clash1.proposed_filename == "storydata_conflict_test.unity3d"
        assert c_clash2.proposed_filename == "event_conflict_test.unity3d"

        # Test B: If naming strategy was PRESERVE_ORIGINAL, both would try to output "conflict_test.unity3d"
        scanner_preserve = PreConversionScanner(ws, strategy=NamingStrategy.PRESERVE_ORIGINAL)
        cands_preserve = scanner_preserve.scan_candidates([f_clash1, f_clash2], input_root=tmp_root)
        for c in cands_preserve:
            assert c.status == AssetStatus.COLLISION_WARNING
            assert c.action == "SKIP"
            assert "Output collision" in c.reason

        # Test C: Explicit reprocess request for existing asset
        scanner_reproc = PreConversionScanner(ws, strategy=NamingStrategy.AUTO_REDIRECT, reprocess_keys={"0000011"})
        cands_reproc = scanner_reproc.scan_candidates([f_existing], input_root=tmp_root)
        assert cands_reproc[0].status == AssetStatus.REPROCESS_REQUESTED
        assert cands_reproc[0].action == "CONVERT"

        # Render preview report
        report = scanner.render_summary(cands)
        assert "PRE-CONVERSION REDIRECTED RESOURCES SCAN REPORT" in report
        assert "ALREADY_IMPLEMENTED" in report
        print(f"\nSample Preview Output:\n{report}")
    print("  -> Passed!")


if __name__ == "__main__":
    test_workspace_resolution()
    test_asset_identity()
    test_real_redirected_index()
    test_scanner_and_collision_prevention()
    print("\nALL P1 REGISTRY & DUPLICATE DETECTION TESTS PASSED SUCCESSFULLY!")
