from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from scripts.audit_workspace_navigation import audit_workspace, main as audit_main
from scripts.bootstrap_workspace import (
    apply_navigation_plan,
    build_navigation_plan,
    main as bootstrap_main,
)


class WorkspaceNavigationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "phd-thesis"
        self.harness = self.root / "research-harness"
        self.config = self.harness / "config" / "repository_sync.json"
        self.config.parent.mkdir(parents=True)
        self._write_config()
        self._write_required_entries()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write_config(self) -> None:
        payload = {
            "schema_version": 2,
            "workspace": {
                "layout": "sibling-v1",
                "navigation": {
                    "control_plane_dir": "research-harness",
                    "root_entry_files": ["README.md", "AGENTS.md", "phd-thesis.code-workspace"],
                    "deprecated_markers": ["thesis-harness", "phd-research"],
                    "recovery_marker": ".recovery-only.json",
                },
            },
            "repositories": [
                {
                    "id": "idea-control-plane",
                    "name": "research-harness",
                    "kind": "control_plane",
                    "required": True,
                    "path": ".",
                    "origin_repo": "owner/research-harness",
                    "expected_branch": "main",
                    "entry_docs": ["REPO_MAP.md", "AGENTS.md", "process/current_execution_plan_20260802.md"],
                },
                {
                    "id": "chapter-1-ursa",
                    "name": "URSA",
                    "kind": "chapter",
                    "required": True,
                    "path": "../URSA",
                    "origin_repo": "owner/URSA",
                    "expected_branch": "main",
                    "entry_docs": ["AGENTS.md"],
                },
                {
                    "id": "chapter-2-knowledge",
                    "name": "chapter2-urban-forest-knowledge",
                    "kind": "chapter",
                    "required": True,
                    "path": "../chapter2-urban-forest-knowledge",
                    "origin_repo": "owner/chapter2",
                    "expected_branch": "main",
                    "entry_docs": ["AGENTS.md"],
                },
                {
                    "id": "chapter-3-evaluation",
                    "name": "urbfo-agent-demo",
                    "kind": "chapter",
                    "required": True,
                    "path": "../urbfo-agent-demo",
                    "origin_repo": "owner/chapter3",
                    "expected_branch": "main",
                    "entry_docs": ["AGENTS.md"],
                },
            ],
            "satellites": [],
        }
        self.config.write_text(json.dumps(payload), encoding="utf-8")

    def _write_required_entries(self) -> None:
        plan = self.harness / "process" / "current_execution_plan_20260802.md"
        plan.parent.mkdir(parents=True)
        plan.write_text("# Current execution plan\n", encoding="utf-8")
        (self.harness / "AGENTS.md").write_text(
            "Read `process/current_execution_plan_20260802.md`.\n",
            encoding="utf-8",
        )
        (self.harness / "REPO_MAP.md").write_text(
            "Use `research-harness/`, `URSA/`, `chapter2-urban-forest-knowledge/`, "
            "and `urbfo-agent-demo/`.\n",
            encoding="utf-8",
        )
        for directory in ("URSA", "chapter2-urban-forest-knowledge", "urbfo-agent-demo"):
            repo = self.root / directory
            repo.mkdir(parents=True)
            (repo / "AGENTS.md").write_text("# Active entry\n", encoding="utf-8")

    def _generate_root_entries(self) -> None:
        plan = build_navigation_plan(self.config, self.root)
        apply_navigation_plan(plan)

    def test_clean_sibling_workspace_passes(self) -> None:
        self._generate_root_entries()
        result = audit_workspace(self.config, self.root)
        self.assertEqual(result["exit_code"], 0)
        self.assertEqual(result["issues"], [])
        workspace = json.loads((self.root / "phd-thesis.code-workspace").read_text(encoding="utf-8"))
        paths = {item["path"] for item in workspace["folders"]}
        self.assertIn("research-harness", paths)

    def test_missing_root_and_required_entry_are_navigation_drift(self) -> None:
        self._generate_root_entries()
        (self.root / "AGENTS.md").unlink()
        (self.root / "URSA" / "AGENTS.md").unlink()
        result = audit_workspace(self.config, self.root)
        codes = {issue["code"] for issue in result["issues"]}
        self.assertEqual(result["exit_code"], 2)
        self.assertIn("missing_root_entry", codes)
        self.assertIn("missing_entry_doc", codes)

    def test_root_markdown_must_point_to_repo_map_not_only_control_directory(self) -> None:
        self._generate_root_entries()
        (self.root / "README.md").write_text(
            "Open the research-harness control directory.\n",
            encoding="utf-8",
        )
        result = audit_workspace(self.config, self.root)
        codes = {issue["code"] for issue in result["issues"]}
        self.assertEqual(result["exit_code"], 2)
        self.assertIn("root_entry_missing_control_plane_pointer", codes)

    def test_repo_map_must_register_every_required_checkout(self) -> None:
        self._generate_root_entries()
        (self.harness / "REPO_MAP.md").write_text(
            "Use `research-harness/`, `URSA/`, and `urbfo-agent-demo/`.\n",
            encoding="utf-8",
        )
        result = audit_workspace(self.config, self.root)
        issues = [item for item in result["issues"] if item["code"] == "missing_repo_map_registration"]
        self.assertEqual(result["exit_code"], 2)
        self.assertEqual(len(issues), 1)
        self.assertIn("chapter2-urban-forest-knowledge/", issues[0]["message"])

    def test_deprecated_route_and_missing_current_plan_are_reported(self) -> None:
        self._generate_root_entries()
        entry = self.root / "chapter2-urban-forest-knowledge" / "AGENTS.md"
        entry.write_text(
            "Use D:/Projects/phd-research/thesis-harness as the source.\n"
            "Resume at `thesis/current_execution_plan.md`.\n",
            encoding="utf-8",
        )
        result = audit_workspace(self.config, self.root)
        codes = [issue["code"] for issue in result["issues"]]
        self.assertEqual(result["exit_code"], 2)
        self.assertIn("deprecated_workspace_route", codes)
        self.assertIn("missing_current_execution_plan", codes)

    def test_explicit_recovery_notice_is_not_a_stale_active_route(self) -> None:
        self._generate_root_entries()
        entry = self.root / "URSA" / "AGENTS.md"
        entry.write_text(
            "D:/Projects/phd-research is recovery-only; do not write there.\n",
            encoding="utf-8",
        )
        result = audit_workspace(self.config, self.root)
        self.assertEqual(result["exit_code"], 0)

    def test_optional_recovery_marker_is_read_only_and_validated(self) -> None:
        self._generate_root_entries()
        recovery = Path(self.temp.name) / "phd-research"
        recovery.mkdir()
        missing = audit_workspace(self.config, self.root, recovery_roots=[recovery])
        self.assertEqual(missing["exit_code"], 2)
        self.assertIn("missing_recovery_marker", {item["code"] for item in missing["issues"]})

        marker = recovery / ".recovery-only.json"
        marker.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "recovery-only",
                    "writable": False,
                    "canonical_workspace": str(self.root),
                }
            ),
            encoding="utf-8",
        )
        before = marker.read_bytes()
        valid = audit_workspace(self.config, self.root, recovery_roots=[recovery])
        self.assertEqual(valid["exit_code"], 0)
        self.assertEqual(marker.read_bytes(), before)

        marker.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "recovery_only",
                    "writes_allowed": False,
                    "canonical_root": str(self.root),
                }
            ),
            encoding="utf-8",
        )
        compatible = audit_workspace(self.config, self.root, recovery_roots=[recovery])
        self.assertEqual(compatible["exit_code"], 0)

    def test_cli_exit_codes_are_zero_two_and_one(self) -> None:
        self._generate_root_entries()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(audit_main(["--config", str(self.config), "--workspace-root", str(self.root)]), 0)

        (self.root / "README.md").unlink()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(audit_main(["--config", str(self.config), "--workspace-root", str(self.root)]), 2)

        self.config.write_text("{bad json", encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(audit_main(["--config", str(self.config), "--workspace-root", str(self.root)]), 1)

    def test_bootstrap_is_dry_run_by_default_and_idempotent_on_apply(self) -> None:
        for name in ("README.md", "AGENTS.md", "phd-thesis.code-workspace"):
            path = self.root / name
            if path.exists():
                path.unlink()

        with redirect_stdout(io.StringIO()):
            code = bootstrap_main(["--workspace-root", str(self.root), "--config", str(self.config), "--skip-existing"])
        self.assertEqual(code, 0)
        self.assertFalse((self.root / "README.md").exists())

        args = [
            "--workspace-root",
            str(self.root),
            "--config",
            str(self.config),
            "--apply",
            "--skip-existing",
        ]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(bootstrap_main(args), 0)
        first = {
            name: (self.root / name).read_bytes()
            for name in ("README.md", "AGENTS.md", "phd-thesis.code-workspace")
        }
        with redirect_stdout(io.StringIO()):
            self.assertEqual(bootstrap_main(args), 0)
        second = {name: (self.root / name).read_bytes() for name in first}
        self.assertEqual(second, first)


if __name__ == "__main__":
    unittest.main()
