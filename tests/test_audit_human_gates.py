from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_human_gates import audit_human_gates


class HumanGateAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "research-harness"
        self.gates_file = self.root / "registry" / "human_gates.json"
        self.queue_file = self.root / "evidence" / "literature" / "maintenance_queue.json"
        self.config_file = self.root / "config" / "repository_sync.json"
        self.chapter2 = self.root.parent / "chapter2"
        self.chapter3 = self.root.parent / "chapter3"
        for path in (self.gates_file.parent, self.queue_file.parent, self.config_file.parent):
            path.mkdir(parents=True, exist_ok=True)
        self._write_artifacts()
        self._write_config()
        self._write_queue()
        self._write_gates()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write_json(self, path: Path, value: object) -> None:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")

    def _write_artifacts(self) -> None:
        control_artifacts = [
            "evidence/literature/runtime_scan.json",
            "evidence/literature/packets/geospatial_agent_comparators_2026/intake_decision.md",
            "evidence/literature/packets/agent_evaluation_user_validity_2026/intake_decision.md",
            "evidence/literature/packets/knowledge_evidence_governance_2026/intake_decision.md",
            "evidence/literature/packets/scientific_agent_workflow_boundaries_2026/intake_decision.md",
            "evidence/literature/packets/urban_forest_remote_sensing_context_2026/intake_decision.md",
            "evidence/literature/writing_intakes/opening_report_v05_20260901/decision_matrix.json",
        ]
        for relative in control_artifacts:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n", encoding="utf-8")
        ch2 = self.chapter2 / "g4.md"
        ch2.parent.mkdir(parents=True, exist_ok=True)
        ch2.write_text("# G4\n", encoding="utf-8")
        ch3 = self.chapter3 / "route.md"
        ch3.parent.mkdir(parents=True, exist_ok=True)
        ch3.write_text("# route\n", encoding="utf-8")

    def _write_config(self) -> None:
        self._write_json(
            self.config_file,
            {
                "schema_version": 2,
                "repositories": [
                    {"id": "idea-control-plane", "path": "."},
                    {"id": "chapter-2-knowledge", "path": "../chapter2"},
                    {"id": "chapter-3-evaluation", "path": "../chapter3"},
                ],
            },
        )

    def _write_queue(self) -> None:
        actions = [
            {
                "action_id": "lit-cross-device-seadrive-verification",
                "kind": "external_verification",
                "status": "pending_external_verification",
                "gate": "second_device_access",
            },
            {
                "action_id": "lit-geospatial-agent-zotero-import",
                "kind": "zotero_write",
                "status": "pending_authorization",
                "gate": "explicit_user_authorization",
            },
            {
                "action_id": "lit-agent-evaluation-zotero-import",
                "kind": "zotero_write",
                "status": "pending_authorization",
                "gate": "explicit_user_authorization",
            },
            {
                "action_id": "lit-knowledge-governance-zotero-import",
                "kind": "zotero_write",
                "status": "pending_authorization",
                "gate": "explicit_user_authorization",
            },
            {
                "action_id": "lit-scientific-agent-workflows-zotero-import",
                "kind": "zotero_write",
                "status": "pending_authorization",
                "gate": "explicit_user_authorization",
            },
            {
                "action_id": "lit-urban-forest-background-zotero-import",
                "kind": "zotero_write",
                "status": "pending_authorization",
                "gate": "explicit_user_authorization",
            },
            {
                "action_id": "lit-opening-v05-contract-merge",
                "kind": "writing_merge",
                "status": "pending_task_specific_review",
                "gate": "fresh_context_v1_and_explicit_contract_acceptance",
            },
        ]
        self._write_json(self.queue_file, {"schema_version": "1.0", "actions": actions})

    def _gate(
        self,
        gate_id: str,
        category: str,
        status: str,
        repository_id: str,
        artifact_path: str,
        gate: str,
        source_action_id: str | None = None,
    ) -> dict[str, object]:
        value: dict[str, object] = {
            "gate_id": gate_id,
            "category": category,
            "status": status,
            "decision_owner": "researcher",
            "repository_id": repository_id,
            "artifact_path": artifact_path,
            "gate": gate,
            "blocks": ["blocked_outcome"],
            "required_evidence": ["researcher evidence"],
            "next_action": "wait for researcher",
        }
        if source_action_id:
            value["source_action_id"] = source_action_id
        return value

    def _write_gates(self) -> None:
        gates = [
            self._gate(
                "lit-cross-device-seadrive-verification",
                "maintenance_external",
                "pending_external_verification",
                "idea-control-plane",
                "evidence/literature/runtime_scan.json",
                "second_device_access",
                "lit-cross-device-seadrive-verification",
            ),
            self._gate(
                "lit-geospatial-agent-zotero-import",
                "zotero_write",
                "pending_authorization",
                "idea-control-plane",
                "evidence/literature/packets/geospatial_agent_comparators_2026/intake_decision.md",
                "explicit_user_authorization",
                "lit-geospatial-agent-zotero-import",
            ),
            self._gate(
                "lit-agent-evaluation-zotero-import",
                "zotero_write",
                "pending_authorization",
                "idea-control-plane",
                "evidence/literature/packets/agent_evaluation_user_validity_2026/intake_decision.md",
                "explicit_user_authorization",
                "lit-agent-evaluation-zotero-import",
            ),
            self._gate(
                "lit-knowledge-governance-zotero-import",
                "zotero_write",
                "pending_authorization",
                "idea-control-plane",
                "evidence/literature/packets/knowledge_evidence_governance_2026/intake_decision.md",
                "explicit_user_authorization",
                "lit-knowledge-governance-zotero-import",
            ),
            self._gate(
                "lit-scientific-agent-workflows-zotero-import",
                "zotero_write",
                "pending_authorization",
                "idea-control-plane",
                "evidence/literature/packets/scientific_agent_workflow_boundaries_2026/intake_decision.md",
                "explicit_user_authorization",
                "lit-scientific-agent-workflows-zotero-import",
            ),
            self._gate(
                "lit-urban-forest-background-zotero-import",
                "zotero_write",
                "pending_authorization",
                "idea-control-plane",
                "evidence/literature/packets/urban_forest_remote_sensing_context_2026/intake_decision.md",
                "explicit_user_authorization",
                "lit-urban-forest-background-zotero-import",
            ),
            self._gate(
                "lit-opening-v05-contract-merge",
                "writing_acceptance",
                "pending_task_specific_review",
                "idea-control-plane",
                "evidence/literature/writing_intakes/opening_report_v05_20260901/decision_matrix.json",
                "fresh_context_v1_and_explicit_contract_acceptance",
                "lit-opening-v05-contract-merge",
            ),
            self._gate(
                "ch2-g4-batch-a-researcher-review",
                "scientific_evidence",
                "pending_researcher_review",
                "chapter-2-knowledge",
                "g4.md",
                "researcher_review_batch_a_10_low_boundary_items",
            ),
            self._gate(
                "ch3-first-evaluation-route-selection",
                "scientific_route",
                "pending_researcher_decision",
                "chapter-3-evaluation",
                "route.md",
                "researcher_select_route_b_or_rss_first_round",
            ),
        ]
        self._write_json(
            self.gates_file,
            {
                "schema_version": "1.0",
                "policy": {
                    "source_of_truth": "registry/human_gates.json",
                    "decision_owner": "researcher",
                    "open_statuses": [
                        "pending_external_verification",
                        "pending_authorization",
                        "pending_task_specific_review",
                        "pending_researcher_review",
                        "pending_researcher_decision",
                    ],
                    "automatic_resolution_forbidden": True,
                    "literature_queue_binding_required": True,
                },
                "gates": gates,
            },
        )

    def audit(self) -> dict[str, object]:
        return audit_human_gates(self.root, self.gates_file, self.queue_file, self.config_file)

    def test_current_nine_gate_registry_passes(self) -> None:
        result = self.audit()
        self.assertEqual(result["exit_code"], 0)
        self.assertEqual((result["gates_total"], len(result["open_gates"])), (9, 9))
        self.assertEqual(result["category_counts"]["zotero_write"], 5)
        self.assertEqual(len(result["category_counts"]), 5)

    def test_missing_current_gate_is_reported(self) -> None:
        registry = json.loads(self.gates_file.read_text(encoding="utf-8"))
        registry["gates"] = registry["gates"][:-1]
        self._write_json(self.gates_file, registry)
        result = self.audit()
        self.assertIn("missing_current_human_gate", {issue["code"] for issue in result["issues"]})

    def test_literature_status_drift_is_reported(self) -> None:
        registry = json.loads(self.gates_file.read_text(encoding="utf-8"))
        registry["gates"][0]["status"] = "pending_authorization"
        self._write_json(self.gates_file, registry)
        result = self.audit()
        self.assertIn("human_gate_status_drift", {issue["code"] for issue in result["issues"]})

    def test_missing_owning_artifact_is_reported(self) -> None:
        (self.chapter2 / "g4.md").unlink()
        result = self.audit()
        self.assertIn("missing_human_gate_artifact", {issue["code"] for issue in result["issues"]})

    def test_completed_gate_requires_resolution_evidence(self) -> None:
        registry = json.loads(self.gates_file.read_text(encoding="utf-8"))
        registry["gates"][5]["status"] = "completed"
        self._write_json(self.gates_file, registry)
        result = self.audit()
        self.assertIn("missing_human_gate_resolution", {issue["code"] for issue in result["issues"]})


if __name__ == "__main__":
    unittest.main()
