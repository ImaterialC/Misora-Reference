#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_new_dataminer.py - Unit & Integration Tests for P2 Universal Japanese Game Data Miner
"""
import tempfile
from pathlib import Path

from NewDataMiner import (
    DataMiner,
    MinerConfig,
    ManifestManager,
    AssetCategory,
    AssetExtractor,
)


def test_manifest_indexing_and_fast_search():
    print("[TEST 1] Manifest Indexing & Fast Offline Search...")
    dm = DataMiner()
    total = dm.manifest_manager.load_manifests()
    print(f"  Indexed {total:,} assets across {len(dm.manifest_manager._by_manifest)} manifests.")
    assert total > 10000, f"Expected > 10,000 assets across manifests, got {total}"

    # Search 1: Quest 80-9 story script (9080155)
    story_matches = dm.search("9080155", category=AssetCategory.STORY)
    assert len(story_matches) >= 1
    found_story = story_matches[0]
    assert "9080155" in found_story.name
    assert found_story.category == AssetCategory.STORY
    print(f"  -> Story search matched: {found_story.name} ({found_story.human_size}) in {found_story.manifest_name}")

    # Search 2: Unit 1001 (Pecorine)
    unit_matches = dm.search("1001", category=AssetCategory.UNIT)
    assert len(unit_matches) >= 1
    print(f"  -> Unit search matched {len(unit_matches)} asset(s) for unit 1001")

    # Search 3: Sound BGM (bgm_AM01)
    sound_matches = dm.search("bgm_AM01", category=AssetCategory.SOUND)
    assert len(sound_matches) >= 1
    print(f"  -> Sound search matched: {sound_matches[0].name} ({sound_matches[0].human_size})")

    # Search 4: Movie arcade
    movie_matches = dm.search("arcade_1001", category=AssetCategory.MOVIE)
    assert len(movie_matches) >= 1
    print(f"  -> Movie search matched: {movie_matches[0].name} ({movie_matches[0].human_size})")
    print("  -> Passed!")


def test_download_scope_preview():
    print("\n[TEST 2] Download Scope Preview & Safety Calculation...")
    dm = DataMiner()
    story_matches = dm.search("9080155", category=AssetCategory.STORY)
    scope = dm.preview_scope(story_matches)
    assert scope.total_count == len(story_matches)
    assert scope.total_bytes > 0
    print(f"  Scope summary: {scope.summary()}")
    assert "file(s)" in scope.summary()
    assert scope.human_size.endswith(("B", "KB", "MB"))
    print("  -> Passed!")


def test_local_bundle_extraction():
    print("\n[TEST 3] Local Unity3D Bundle Extraction...")
    sample_bundle = Path("9080155.unity3d")
    assert sample_bundle.exists(), "Sample bundle 9080155.unity3d must exist"

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_out = Path(tmp_dir)
        extractor = AssetExtractor()
        extracted = extractor.extract_unity_bundle(sample_bundle, dest_dir=tmp_out)
        assert len(extracted) > 0, "Expected at least 1 extracted asset from 9080155.unity3d"
        text_file = extracted[0]
        assert text_file.exists()
        assert text_file.suffix.lower() == ".txt"
        content = text_file.read_bytes()
        assert len(content) > 0
        print(f"  Extracted: {text_file.name} ({len(content)} bytes)")
    print("  -> Passed!")


if __name__ == "__main__":
    test_manifest_indexing_and_fast_search()
    test_download_scope_preview()
    test_local_bundle_extraction()
    print("\nALL P2 NEW DATA MINER TESTS PASSED SUCCESSFULLY!")
