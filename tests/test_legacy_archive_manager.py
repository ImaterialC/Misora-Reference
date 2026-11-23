import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.legacy_archive_manager import duplicate_groups, make_inventory, make_zip_for_source


class LegacyArchiveManagerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "legacy_a").mkdir()
        (self.root / "legacy_b").mkdir()
        (self.root / "legacy_a" / "same.py").write_text("print('same')\n", encoding="utf-8")
        (self.root / "legacy_b" / "same_copy.py").write_text("print('same')\n", encoding="utf-8")
        (self.root / "legacy_a" / "readme.md").write_text("hello\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_inventory_hashes_and_classifies(self):
        rows = make_inventory(self.root, ["legacy_a", "legacy_b"])
        self.assertEqual(len(rows), 3)
        by_name = {row["filename"]: row for row in rows}
        self.assertEqual(by_name["same.py"]["kind"], "python_source")
        self.assertEqual(by_name["readme.md"]["kind"], "documentation_or_text")
        self.assertEqual(len(by_name["same.py"]["sha256"]), 64)

    def test_duplicate_groups_only_exact_content(self):
        groups = duplicate_groups(make_inventory(self.root, ["legacy_a", "legacy_b"]))
        self.assertEqual(len(groups), 1)
        self.assertEqual(set(groups[0]["paths"]), {"legacy_a/same.py", "legacy_b/same_copy.py"})

    def test_zip_pack_preserves_paths_and_hashes(self):
        out = self.root / "archives" / "legacy_a.zip"
        result = make_zip_for_source(self.root, "legacy_a", out, dry_run=False)
        self.assertTrue(result["written"])
        with zipfile.ZipFile(out) as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn("legacy_a/same.py", archive.namelist())
            manifest = json.loads(archive.read("legacy_a/_ARCHIVE_MANIFEST.json"))
            self.assertEqual(manifest["files"][0]["path"], "legacy_a/readme.md")

    def test_zip_dry_run_does_not_write(self):
        out = self.root / "archives" / "legacy_a.zip"
        result = make_zip_for_source(self.root, "legacy_a", out, dry_run=True)
        self.assertFalse(result["written"])
        self.assertFalse(out.exists())

    def test_archive_no_overwrite(self):
        out = self.root / "archives" / "legacy_a.zip"
        out.parent.mkdir()
        out.write_bytes(b"existing")
        with self.assertRaises(FileExistsError):
            make_zip_for_source(self.root, "legacy_a", out, dry_run=False)
        self.assertEqual(out.read_bytes(), b"existing")


if __name__ == "__main__":
    unittest.main()
