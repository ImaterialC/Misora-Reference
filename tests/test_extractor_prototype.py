#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_extractor_prototype.py
==================================
Unit tests and performance benchmarks for the Misora Extractor Prototype.
Verifies all 3 pillars: Local Scanner, In-Memory Story Codec, and Database Metadata Resolver.
"""

import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path

from extractor_prototype.db_metadata import DatabaseMetadata, STATIC_UNIT_FALLBACKS
from extractor_prototype.local_scanner import LocalScanner, ScannedStoryItem
from extractor_prototype.service import MisoraExtractorService
from extractor_prototype.story_codec import DialogueBlock, StoryCodec, StoryScene


class TestStoryCodec(unittest.TestCase):
    """Verifies in-memory codec math, bytecode serialization, and CSIF generation."""

    def test_byte_inversion_roundtrip(self):
        original = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        inverted = StoryCodec.invert_every_third_byte(original)
        self.assertNotEqual(original, inverted)
        reverted = StoryCodec.invert_every_third_byte(inverted)
        self.assertEqual(original, reverted)

    def test_argument_codec_roundtrip(self):
        samples = [
            "Hello World!",
            "主さま、目を覚ましてください！",
            "ミソラ: 「ふふっ、見つかっちゃった☆」",
            "Line 1\nLine 2\tTabbed",
            "Special characters: 『』【】♪〜☆★",
        ]
        for s in samples:
            encoded = StoryCodec.encode_arg(s)
            self.assertEqual(StoryCodec.decode_arg(encoded), s)

    def test_bytecode_parsing_and_building(self):
        # Build synthetic ADV commands:
        # cmd 0 (title), cmd 8 (print)
        title_arg = StoryCodec.encode_arg("第1章 旅立ち")
        spk_arg = StoryCodec.encode_arg("コッコロ")
        txt_arg = StoryCodec.encode_arg("主さま、朝ですよ。")

        raw_records = [
            (0, [title_arg]),
            (8, [spk_arg, txt_arg]),
        ]
        payload = StoryCodec.build_raw_bytecode(raw_records)
        parsed = StoryCodec.parse_raw_bytecode(payload)

        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0][0], 0)
        self.assertEqual(parsed[1][0], 8)
        self.assertEqual(StoryCodec.decode_arg(parsed[0][1][0]), "第1章 旅立ち")
        self.assertEqual(StoryCodec.decode_arg(parsed[1][1][0]), "コッコロ")
        self.assertEqual(StoryCodec.decode_arg(parsed[1][1][1]), "主さま、朝ですよ。")

    def test_scene_decoding_and_csif(self):
        title_arg = StoryCodec.encode_arg("不思議な出会い")
        outline_arg = StoryCodec.encode_arg("ランドソルでのプロローグ")
        spk1 = StoryCodec.encode_arg("ペコリーヌ")
        txt1 = StoryCodec.encode_arg("お腹がペコペコです〜！")
        spk2 = StoryCodec.encode_arg("キャル")
        txt2 = StoryCodec.encode_arg("ちょっと、勝手に食べないでよ！")

        raw_records = [
            (0, [title_arg]),
            (1, [outline_arg]),
            (8, [spk1, txt1]),
            (8, [spk2, txt2]),
        ]
        payload = StoryCodec.build_raw_bytecode(raw_records)
        scene = StoryCodec.decode_scene_from_bytes(payload)

        self.assertEqual(scene.title, "不思議な出会い")
        self.assertEqual(scene.outline, "ランドソルでのプロローグ")
        self.assertEqual(len(scene.dialogues), 2)
        self.assertEqual(scene.dialogues[0].speaker, "ペコリーヌ")
        self.assertEqual(scene.dialogues[1].speaker, "キャル")

        csif = scene.to_csif()
        self.assertIn("# Title: 不思議な出会い", csif)
        self.assertIn("@@ペコリーヌ", csif)
        self.assertIn("お腹がペコペコです〜！", csif)
        self.assertIn("@@キャル", csif)


class TestDatabaseMetadata(unittest.TestCase):
    """Verifies SQLite queries and fallback resolution."""

    def test_unit_resolution_and_fallback(self):
        db = DatabaseMetadata()
        # Test known Misora unit ID (118201)
        meta_misora = db.get_unit(118201)
        self.assertEqual(meta_misora.unit_name, "Misora")
        self.assertEqual(meta_misora.unit_name_jp, "ミソラ")

        # Test known Pecorine unit ID (105801)
        meta_pecorine = db.get_unit(105801)
        self.assertEqual(meta_pecorine.unit_name, "Pecorine")
        self.assertEqual(meta_pecorine.unit_name_jp, "ペコリーヌ")

        # Test unknown unit fallback
        meta_unknown = db.get_unit(999999)
        self.assertEqual(meta_unknown.unit_name, "Unit_999999")

    def test_scene_enrichment(self):
        db = DatabaseMetadata()
        scene = StoryScene(title="")
        scene.dialogues.append(DialogueBlock(speaker="118201", text="こんにちは！"))
        scene.dialogues.append(DialogueBlock(speaker="105801", text="ごはんの時間です！"))

        db.enrich_scene(scene)
        self.assertIn("ミソラ", scene.dialogues[0].speaker)
        self.assertIn("ペコリーヌ", scene.dialogues[1].speaker)


class TestLocalScanner(unittest.TestCase):
    """Verifies DMM cache discovery with mock directories."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="dmm_cache_test_"))
        # Create dummy mock bundles
        (self.test_dir / "storydata_100101.unity3d").write_bytes(b"mock_bundle_1")
        (self.test_dir / "storydata_100102.unity3d").write_bytes(b"mock_bundle_2")
        (self.test_dir / "unit_icon_105801.unity3d").write_bytes(b"mock_icon")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_scan_and_filter(self):
        scanner = LocalScanner(cache_dir=self.test_dir)
        self.assertTrue(scanner.is_cache_available())

        # Filter story only
        items = scanner.scan(filter_story_only=True)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].story_id, 100101)
        self.assertEqual(items[1].story_id, 100102)

        # Include all
        all_items = scanner.scan(filter_story_only=False)
        self.assertEqual(len(all_items), 3)


class TestPerformanceBenchmark(unittest.TestCase):
    """Asserts that decoding large story payloads completes in < 100ms."""

    def test_service_end_to_end(self):
        service = MisoraExtractorService()
        raw_records = [
            (0, [StoryCodec.encode_arg("絆ストーリー 第1話")]),
            (8, [StoryCodec.encode_arg("118201"), StoryCodec.encode_arg("また会えたね、お兄ちゃん♪")]),
        ]
        payload = StoryCodec.build_raw_bytecode(raw_records)
        scene = service.extract_from_bytes(payload, enrich=True)
        csif = scene.to_csif()

        self.assertIn("# Title: 絆ストーリー 第1話", csif)
        self.assertIn("@@ミソラ", csif)
        self.assertIn("また会えたね、お兄ちゃん♪", csif)

    def test_benchmark_50_dialogue_lines(self):
        raw_records = []
        for i in range(50):
            spk = StoryCodec.encode_arg(f"Speaker_{i % 5}")
            txt = StoryCodec.encode_arg(f"This is dialogue test line number {i} for benchmarking.")
            raw_records.append((8, [spk, txt]))

        payload = StoryCodec.build_raw_bytecode(raw_records)

        start = time.perf_counter()
        scene = StoryCodec.decode_scene_from_bytes(payload)
        csif = scene.to_csif()
        elapsed_ms = (time.perf_counter() - start) * 1000

        self.assertEqual(len(scene.dialogues), 50)
        self.assertLess(elapsed_ms, 100.0, f"Decoding took {elapsed_ms:.2f}ms, exceeding 100ms limit")
        print(f"\n[BENCHMARK] Decoded 50 dialogue lines and generated CSIF in {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    unittest.main()
