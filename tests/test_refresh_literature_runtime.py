from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.refresh_literature_runtime import build_runtime_scan, write_runtime_scan, _registered_zotero_keys


class LiteratureRuntimeRefreshTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "research-harness"
        self.literature = self.root / "evidence" / "literature"
        self.literature.mkdir(parents=True)
        self.registry = self.literature / "packet_registry.json"
        self.queue = self.literature / "maintenance_queue.json"
        self.snapshot = self.literature / "runtime_scan.json"
        self.registry.write_text(
            json.dumps(
                {
                    "packets": [
                        {"packet_id": "sample", "zotero_item_keys": ["PARENT01"]}
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.queue.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "updated_at": "2026-08-20T00:00:00+08:00",
                    "read_only_scan": {"last_completed": "2026-08-20", "checks": []},
                    "actions": [],
                }
            ),
            encoding="utf-8",
        )
        self.linked = self.root / "cache" / "SeaDrive" / "library" / "paper.pdf"
        self.linked.parent.mkdir(parents=True)
        self.linked.write_bytes(b"%PDF-test")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def json_runner(self, helper: Path, *args: str):
        if args == ("status", "--json"):
            return {
                "zotero_version": "9.0.5",
                "local_api_enabled_pref": True,
                "api_running": True,
                "api_status": 200,
                "connector_running": True,
            }
        if args == ("selected-target", "--json"):
            return {
                "libraryID": 1,
                "libraryName": "Library",
                "id": 19,
                "name": "AI_for_Science",
                "editable": True,
            }
        if args == ("children", "PARENT01", "--json"):
            return [{"key": "ATTACH01", "itemType": "attachment", "title": "PDF"}]
        raise AssertionError(args)

    def text_runner(self, helper: Path, *args: str) -> str:
        self.assertEqual(args, ("file-url", "ATTACH01"))
        return self.linked.resolve().as_uri()

    def test_build_snapshot_is_path_redacted_and_seadrive_ready(self) -> None:
        snapshot = build_runtime_scan(
            Path("fake-helper.py"),
            self.registry,
            observed_at=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
            json_runner=self.json_runner,
            text_runner=self.text_runner,
        )
        self.assertTrue(snapshot["summary"]["all_registered_items_ready"])
        self.assertEqual(snapshot["items"][0]["transport"], "SeaDrive")
        serialized = json.dumps(snapshot)
        self.assertNotIn(str(self.linked), serialized)
        self.assertFalse(snapshot["cross_device_equivalence_verified"])

    def test_write_advances_snapshot_and_queue_together(self) -> None:
        snapshot = build_runtime_scan(
            Path("fake-helper.py"),
            self.registry,
            observed_at=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
            json_runner=self.json_runner,
            text_runner=self.text_runner,
        )
        write_runtime_scan(snapshot, self.snapshot, self.queue)
        queue = json.loads(self.queue.read_text(encoding="utf-8"))
        self.assertEqual(queue["read_only_scan"]["last_completed"], "2026-09-01")
        self.assertEqual(
            queue["read_only_scan"]["runtime_snapshot"],
            "evidence/literature/runtime_scan.json",
        )
        written = json.loads(self.snapshot.read_text(encoding="utf-8"))
        self.assertTrue(written["summary"]["all_registered_items_ready"])

    def test_incomplete_snapshot_does_not_advance_freshness(self) -> None:
        snapshot = build_runtime_scan(
            Path("fake-helper.py"),
            self.registry,
            observed_at=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
            json_runner=self.json_runner,
            text_runner=self.text_runner,
        )
        snapshot["summary"]["all_registered_items_ready"] = False
        with self.assertRaisesRegex(RuntimeError, "incomplete"):
            write_runtime_scan(snapshot, self.snapshot, self.queue)
        queue = json.loads(self.queue.read_text(encoding="utf-8"))
        self.assertEqual(queue["read_only_scan"]["last_completed"], "2026-08-20")

    def test_source_reuse_across_packets_is_not_duplicate_parent(self) -> None:
        self.assertEqual(_registered_zotero_keys({"packets": [
            {"zotero_item_keys": ["PARENT01"]},
            {"zotero_item_keys": ["PARENT01", "PARENT02"]},
        ]}), ["PARENT01", "PARENT02"])

    def test_unhealthy_api_cannot_advance_runtime(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "unhealthy"):
            build_runtime_scan(Path("fake"), self.registry, json_runner=lambda *a: {"api_running": False})


if __name__ == "__main__":
    unittest.main()
