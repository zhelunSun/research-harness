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
        "acquisition_queue": {
            "active_work_item_id": "AQ-OI-D6-EVALUATION",
            "work_items_total": 5,
            "ready_items": ["AQ-OI-D6-EVALUATION"],
        },
        "open_actions": [],
        "issues": [],
    }


def human_gate_result(*, exit_code: int = 0) -> dict[str, object]:
    gates = [
        ("lit-cross-device-seadrive-verification", "maintenance_external", "pending_external_verification"),
        ("lit-geospatial-agent-zotero-import", "zotero_write", "pending_authorization"),
        ("lit-agent-evaluation-zotero-import", "zotero_write", "pending_authorization"),
        ("lit-opening-v05-contract-merge", "writing_acceptance", "pending_task_specific_review"),
        ("ch2-g4-batch-a-researcher-review", "scientific_evidence", "pending_researcher_review"),
        ("ch3-first-evaluation-route-selection", "scientific_route", "pending_researcher_decision"),
    ]
    return {
        "exit_code": exit_code,
        "gates_total": 6,
        "category_counts": {category: sum(1 for _, item_category, _ in gates if item_category == category) for _, category, _ in gates},
        "open_gates": [
            {
                "gate_id": gate_id,
                "category": category,
                "status": status,
                "gate": "test_gate",
                "repository_id": "idea-control-plane",
                "next_action": "wait for researcher",
            }
            for gate_id, category, status in gates
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

    def run_audit(
        self,
        repo: dict[str, object],
        literature: dict[str, object],
        human_gates: dict[str, object] | None = None,
    ):
        with (
            patch(
                "scripts.audit_thesis_workspace.audit_workspace",
                return_value={"exit_code": 0, "issues": [], "required_repositories": 1},
            ),
            patch("scripts.audit_thesis_workspace.load_targets", return_value=[self.target]),
            patch("scripts.audit_thesis_workspace.audit_repository", return_value=repo),
            patch("scripts.audit_thesis_workspace.audit_literature_control", return_value=literature),
            patch(
                "scripts.audit_thesis_workspace.audit_human_gates",
                return_value=human_gates or human_gate_result(),
            ),
        ):
            return audit_thesis_control(self.root, as_of=date(2026, 9, 1))

    def test_ready_workspace_preserves_pending_human_gate(self) -> None:
        result = self.run_audit(repository_result(), literature_result())
        self.assertEqual((result["exit_code"], result["readiness"]), (0, "ready"))
        self.assertEqual(len(result["pending_human_gates"]), 6)
        rendered = render_text(result)
        self.assertIn("acquisition_active=AQ-OI-D6-EVALUATION", rendered)
        self.assertIn("ch2-g4-batch-a-researcher-review", rendered)
        self.assertIn("ch3-first-evaluation-route-selection", rendered)

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

    def test_human_gate_warning_is_not_hidden(self) -> None:
        human_gates = human_gate_result(exit_code=2)
        human_gates["issues"] = [{"code": "missing_current_human_gate", "message": "missing"}]
        result = self.run_audit(repository_result(), literature_result(), human_gates)
        self.assertEqual(result["exit_code"], 2)
        self.assertIn("missing_current_human_gate", render_text(result))


if __name__ == "__main__":
    unittest.main()
