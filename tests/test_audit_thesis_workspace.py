from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from scripts.audit_thesis_workspace import audit_thesis_control, render_text


def repository_result(*, issues: list[dict[str, str]] | None = None) -> dict[str, object]:
    return {
        "id": "idea-control-plane",
        "name": "idea-control-plane",
        "kind": "control_plane",
        "branch": "main",
        "behind": 0,
        "ahead": 0,
        "dirty": 0,
        "issues": issues or [],
    }


def literature_result(*, exit_code: int = 0) -> dict[str, object]:
    return {
        "exit_code": exit_code,
        "packets_total": 2,
        "sources_total": 9,
        "runtime_scan": {"registered_zotero_items": 5},
        "open_actions": [
            {
                "action_id": "lit-cross-device-seadrive-verification",
                "kind": "external_verification",
                "status": "pending_external_verification",
                "gate": "second_device_access",
            }
        ],
        "issues": [],
    }


class ThesisControlAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "research-harness"
        self.root.mkdir()
        self.target = {
            "id": "idea-control-plane",
            "name": "idea-control-plane",
            "kind": "control_plane",
            "required": True,
            "path": self.root,
            "expected_branch": "main",
            "expected_origin_repo": "owner/repo",
            "checkpoint": None,
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_audit(self, repo: dict[str, object], literature: dict[str, object]):
        with (
            patch(
                "scripts.audit_thesis_workspace.audit_workspace",
                return_value={"exit_code": 0, "issues": [], "required_repositories": 1},
            ),
            patch("scripts.audit_thesis_workspace.load_targets", return_value=[self.target]),
            patch("scripts.audit_thesis_workspace.audit_repository", return_value=repo),
            patch("scripts.audit_thesis_workspace.audit_literature_control", return_value=literature),
        ):
            return audit_thesis_control(self.root, as_of=date(2026, 9, 1))

    def test_ready_workspace_preserves_pending_human_gate(self) -> None:
        result = self.run_audit(repository_result(), literature_result())
        self.assertEqual((result["exit_code"], result["readiness"]), (0, "ready"))
        self.assertEqual(len(result["pending_human_gates"]), 1)
        self.assertIn("second_device_access", render_text(result))

    def test_repository_warning_requires_attention(self) -> None:
        warning = repository_result(
            issues=[{"level": "warning", "code": "dirty_worktree", "message": "dirty"}]
        )
        result = self.run_audit(warning, literature_result())
        self.assertEqual((result["exit_code"], result["readiness"]), (2, "attention_required"))

    def test_repository_critical_blocks_workspace(self) -> None:
        critical = repository_result(
            issues=[{"level": "critical", "code": "diverged", "message": "diverged"}]
        )
        result = self.run_audit(critical, literature_result())
        self.assertEqual((result["exit_code"], result["readiness"]), (1, "blocked"))

    def test_literature_warning_is_not_hidden_by_clean_repositories(self) -> None:
        literature = literature_result(exit_code=2)
        literature["issues"] = [{"code": "read_only_scan_overdue", "message": "overdue"}]
        result = self.run_audit(repository_result(), literature)
        self.assertEqual(result["exit_code"], 2)
        self.assertIn("read_only_scan_overdue", render_text(result))


if __name__ == "__main__":
    unittest.main()
