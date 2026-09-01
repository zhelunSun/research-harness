from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.audit_literature_control import audit_literature_control


class LiteratureControlAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "research-harness"
        self.literature = self.root / "evidence" / "literature"
        self.packet = self.literature / "packets" / "sample"
        self.packet.mkdir(parents=True)
        self.registry = self.literature / "packet_registry.json"
        self.queue = self.literature / "maintenance_queue.json"
        self.routes = self.literature / "consumer_routes.json"
        self.intakes = self.literature / "writing_intakes.json"
        self.runtime = self.literature / "runtime_scan.json"
        self.acquisition = self.literature / "acquisition_queue.json"
        self.human_gates = self.root / "registry" / "human_gates.json"
        self.repo_config = self.root / "config" / "repository_sync.json"
        self.consumer = self.root.parent / "chapter" / "consumer.md"
        self.consumer.parent.mkdir(parents=True)
        self.consumer.write_text("# consumer\n", encoding="utf-8")
        self.target_document = self.root / "thesis" / "opening.md"
        self.target_contract = self.root / "thesis" / "opening.contract.json"
        self.target_document.parent.mkdir(parents=True)
        self.target_document.write_text("# opening\n\nEvidence gap. [REF-MISSING]\n", encoding="utf-8")
        self._write_json(self.target_contract, {"schema_version": "1.0"})
        self.intake_dir = self.literature / "writing_intakes" / "sample"
        self.intake_dir.mkdir(parents=True)
        self._write_intake_artifacts()
        self._write_packet()
        self._write_registry()
        self._write_queue()
        self._write_routes()
        self._write_intakes()
        self._write_runtime()
        self._write_acquisition()
        self._write_human_gates()
        self._write_repo_config()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write_json(self, path: Path, value: object) -> None:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")

    def _write_packet(self) -> None:
        (self.packet / "README.md").write_text("# sample\n", encoding="utf-8")
        (self.packet / "evidence_cards.md").write_text("# cards\n", encoding="utf-8")
        (self.packet / "references.bib").write_text(
            "@article{sample_2026, title={Sample}, year={2026}}\n",
            encoding="utf-8",
        )
        ledger = {
            "ledger_id": "sample-packet",
            "sources": [
                {
                    "source_id": "S-1",
                    "title": "Sample",
                    "bibtex_key": "sample_2026",
                    "zotero_item_key": "ABC12345",
                }
            ],
            "claims": [{"claim_id": "C-1", "evidence_status": "verified"}],
            "links": [{"claim_id": "C-1", "source_id": "S-1", "entailment_status": "verified"}],
        }
        self._write_json(self.packet / "ledger.json", ledger)
        self._write_json(
            self.packet / "audit.json",
            {
                "ledger_id": "sample-packet",
                "ok": True,
                "summary": {"sources": 1, "claims": 1, "links": 1, "errors": 0, "warnings": 0},
                "findings": [],
            },
        )
        self._write_json(
            self.packet / "writing_bridge.json",
            {"source_ledger_id": "sample-packet", "claims": []},
        )

    def _write_registry(self) -> None:
        self._write_json(
            self.registry,
            {
                "schema_version": "1.0",
                "source_of_truth": {
                    "bibliography": "local Zotero Desktop",
                    "linked_attachments": "SeaDrive",
                    "evidence_packets": "research-harness/evidence/literature/packets",
                },
                "packets": [
                    {
                        "packet_id": "sample-packet",
                        "path": "evidence/literature/packets/sample",
                        "status": "audited",
                        "source_count": 1,
                        "zotero_item_keys": ["ABC12345"],
                        "writing_eligibility": "not_merged_into_any_writing_contract",
                        "last_audited": "2026-09-01",
                    }
                ],
            },
        )

    def _write_queue(self, *, last_completed: str = "2026-09-01") -> None:
        self._write_json(
            self.queue,
            {
                "schema_version": "1.0",
                "policy": {
                    "zotero_write_gate": "explicit_user_authorization",
                    "writing_merge_gate": "task_specific_contract_review",
                    "linked_attachment_transport": "SeaDrive",
                    "read_only_scan_interval_days": 7,
                },
                "read_only_scan": {
                    "last_completed": last_completed,
                    "runtime_snapshot": "evidence/literature/runtime_scan.json",
                    "checks": [
                        "zotero_status",
                        "selected_target",
                        "doi_or_exact_title_dedup",
                        "linked_pdf_resolution",
                        "packet_audit",
                    ],
                },
                "actions": [
                    {
                        "action_id": "write-sample",
                        "kind": "zotero_write",
                        "packet_id": "sample-packet",
                        "status": "pending_authorization",
                        "gate": "explicit_user_authorization",
                    }
                ],
            },
        )

    def _write_runtime(self) -> None:
        self._write_json(
            self.runtime,
            {
                "schema_version": "1.0",
                "observed_at": "2026-09-01T12:00:00+08:00",
                "scope": "current_local_device",
                "zotero": {
                    "version": "9.0.5",
                    "local_api_enabled_pref": True,
                    "api_running": True,
                    "api_status": 200,
                    "connector_running": True,
                },
                "selected_target": {
                    "library_id": 1,
                    "library_name": "Library",
                    "collection_id": 19,
                    "collection_name": "AI_for_Science",
                    "editable": True,
                },
                "items": [
                    {
                        "parent_item_key": "ABC12345",
                        "attachment_item_key": "ATT12345",
                        "linked_file_exists": True,
                        "transport": "SeaDrive",
                    }
                ],
                "summary": {
                    "registered_zotero_items": 1,
                    "linked_files_resolved": 1,
                    "seadrive_linked_files_resolved": 1,
                    "all_registered_items_ready": True,
                },
                "path_disclosure": "omitted",
                "cross_device_equivalence_verified": False,
                "limitations": ["current device only"],
            },
        )

    def _write_routes(self) -> None:
        self._write_json(
            self.routes,
            {
                "schema_version": "1.0",
                "policy": {"accepted_route_gate": "task_specific_contract_review"},
                "routes": [
                    {
                        "route_id": "sample-route",
                        "packet_id": "sample-packet",
                        "repository_id": "chapter",
                        "artifact_path": "consumer.md",
                        "claim_ids": ["C-1"],
                        "status": "candidate",
                    }
                ],
            },
        )

    def _write_intake_artifacts(self) -> None:
        self._write_json(
            self.intake_dir / "decision_matrix.json",
            {
                "schema_version": "1.0",
                "intake_id": "sample-writing-intake",
                "decisions": [
                    {
                        "decision_id": "D-1",
                        "decision_scope": "content_ref_missing_gap",
                        "outcome": "partial_split_required",
                        "marker_retained": True,
                        "source_claims": [{"packet_id": "sample-packet", "claim_id": "C-1"}],
                    }
                ],
            },
        )
        self._write_json(
            self.intake_dir / "candidate_contract_fragment.json",
            {"schema_version": "1.0", "status": "not_merged"},
        )

    def _write_intakes(self) -> None:
        self._write_json(
            self.intakes,
            {
                "schema_version": "1.0",
                "policy": {"merge_gate": "task_specific_contract_review"},
                "intakes": [
                    {
                        "intake_id": "sample-writing-intake",
                        "target_repository_id": "idea-control-plane",
                        "target_document": "thesis/opening.md",
                        "target_contract": "thesis/opening.contract.json",
                        "source_packets": ["sample-packet"],
                        "status": "reviewed_candidate",
                        "reviewed_at": "2026-09-01",
                        "decision_artifact": "evidence/literature/writing_intakes/sample/decision_matrix.json",
                        "contract_fragment": "evidence/literature/writing_intakes/sample/candidate_contract_fragment.json",
                        "observed_ref_missing_occurrences": 1,
                        "content_markers_removable_now": 0,
                        "writing_contract_merged": False,
                    }
                ],
            },
        )

    def _write_repo_config(self) -> None:
        self.repo_config.parent.mkdir(parents=True)
        self._write_json(
            self.repo_config,
            {
                "schema_version": 2,
                "repositories": [
                    {"id": "idea-control-plane", "path": "."},
                    {"id": "chapter", "path": "../chapter"},
                ],
            },
        )

    def _write_acquisition(self) -> None:
        self._write_json(
            self.acquisition,
            {
                "schema_version": "1.0",
                "policy": {
                    "active_work_item_limit": 1,
                    "minimum_sources_per_packet": 3,
                    "maximum_sources_per_packet": 5,
                    "metadata_is_not_evidence": True,
                    "full_text_required_for_verified_entailment": True,
                    "zotero_write_gate": "explicit_user_authorization",
                    "writing_merge_gate": "task_specific_contract_review",
                    "candidate_discovery_does_not_remove_ref_missing": True,
                },
                "active_work_item_id": "AQ-D1",
                "work_items": [
                    {
                        "work_item_id": "AQ-D1",
                        "priority": "P0",
                        "status": "ready_for_search",
                        "target_intake_id": "sample-writing-intake",
                        "target_decision_ids": ["D-1"],
                        "target_sections": ["opening background"],
                        "research_question": "What primary evidence is needed for D-1?",
                        "search_queries": ["sample primary research"],
                        "source_target_count": 3,
                        "source_requirements": ["primary sources"],
                        "exclusions": ["metadata-only records"],
                        "candidate_sources": [],
                        "next_action": "Search and screen three primary sources.",
                        "stop_conditions": ["three sources survive full-text screening"],
                    }
                ],
            },
        )

    def _write_human_gates(self) -> None:
        self.human_gates.parent.mkdir(parents=True)
        self._write_json(
            self.human_gates,
            {"schema_version": "1.0", "gates": []},
        )

    def audit(self, *, as_of: date = date(2026, 9, 1)) -> dict[str, object]:
        return audit_literature_control(
            self.root,
            self.registry,
            self.queue,
            self.routes,
            self.repo_config,
            self.intakes,
            self.runtime,
            self.acquisition,
            self.human_gates,
            as_of=as_of,
        )

    def test_valid_control_plane_passes_with_open_gate(self) -> None:
        result = self.audit()
        self.assertEqual(result["exit_code"], 0)
        self.assertEqual((result["packets_total"], result["sources_total"]), (1, 1))
        self.assertEqual(len(result["open_actions"]), 1)
        self.assertEqual((result["routes_total"], len(result["route_actions"])), (1, 1))
        self.assertEqual(result["writing_intakes_total"], 1)
        self.assertEqual(result["runtime_scan"]["seadrive_linked_files_resolved"], 1)
        self.assertEqual(result["acquisition_queue"]["active_work_item_id"], "AQ-D1")
        self.assertEqual(result["acquisition_queue"]["work_items_total"], 1)

    def test_missing_packet_file_is_reported(self) -> None:
        (self.packet / "evidence_cards.md").unlink()
        result = self.audit()
        self.assertEqual(result["exit_code"], 2)
        self.assertIn("missing_packet_file", {item["code"] for item in result["issues"]})

    def test_zotero_identity_mismatch_is_reported(self) -> None:
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        registry["packets"][0]["zotero_item_keys"] = ["DIFFERENT"]
        self._write_json(self.registry, registry)
        result = self.audit()
        self.assertIn("zotero_key_mismatch", {item["code"] for item in result["issues"]})

    def test_bibtex_file_field_and_pdf_are_forbidden(self) -> None:
        (self.packet / "references.bib").write_text(
            "@article{sample_2026, title={Sample}, file={C:/private/sample.pdf}}\n",
            encoding="utf-8",
        )
        (self.packet / "sample.pdf").write_bytes(b"%PDF-test")
        result = self.audit()
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("bibtex_file_field", codes)
        self.assertIn("committed_pdf_binary", codes)
        self.assertIn("workstation_path_in_packet", codes)

    def test_weekly_scan_overdue_is_reported(self) -> None:
        self._write_queue(last_completed="2026-08-20")
        result = self.audit(as_of=date(2026, 9, 1))
        self.assertIn("read_only_scan_overdue", {item["code"] for item in result["issues"]})

    def test_authorized_write_requires_authorization_evidence(self) -> None:
        queue = json.loads(self.queue.read_text(encoding="utf-8"))
        queue["actions"][0]["status"] = "authorized"
        self._write_json(self.queue, queue)
        result = self.audit()
        self.assertIn(
            "missing_zotero_authorization_evidence",
            {item["code"] for item in result["issues"]},
        )

    def test_missing_consumer_and_unknown_claim_are_reported(self) -> None:
        routes = json.loads(self.routes.read_text(encoding="utf-8"))
        routes["routes"][0]["artifact_path"] = "missing.md"
        routes["routes"][0]["claim_ids"] = ["C-UNKNOWN"]
        self._write_json(self.routes, routes)
        result = self.audit()
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("missing_route_artifact", codes)
        self.assertIn("unknown_route_claim", codes)

    def test_reconciled_route_requires_reconciliation_artifact(self) -> None:
        routes = json.loads(self.routes.read_text(encoding="utf-8"))
        routes["routes"][0]["status"] = "reconciled_candidate"
        routes["routes"][0]["reconciled_at"] = "2026-09-01"
        self._write_json(self.routes, routes)
        result = self.audit()
        self.assertIn(
            "missing_route_reconciliation_artifact",
            {item["code"] for item in result["issues"]},
        )

    def test_completed_reconciliation_action_requires_evidence(self) -> None:
        queue = json.loads(self.queue.read_text(encoding="utf-8"))
        queue["actions"][0]["kind"] = "route_reconciliation"
        queue["actions"][0]["status"] = "completed"
        self._write_json(self.queue, queue)
        result = self.audit()
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("missing_reconciliation_completion_date", codes)
        self.assertIn("missing_reconciliation_completion_evidence", codes)

    def test_writing_intake_marker_drift_is_reported(self) -> None:
        intakes = json.loads(self.intakes.read_text(encoding="utf-8"))
        intakes["intakes"][0]["observed_ref_missing_occurrences"] = 2
        self._write_json(self.intakes, intakes)
        result = self.audit()
        self.assertIn("intake_marker_count_drift", {item["code"] for item in result["issues"]})

    def test_needs_review_claim_cannot_be_candidate_support(self) -> None:
        ledger_path = self.packet / "ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["claims"][0]["evidence_status"] = "needs_review"
        self._write_json(ledger_path, ledger)
        decision_path = self.intake_dir / "decision_matrix.json"
        decision = json.loads(decision_path.read_text(encoding="utf-8"))
        decision["decisions"][0]["outcome"] = "candidate_support"
        self._write_json(decision_path, decision)
        result = self.audit()
        self.assertIn("unverified_candidate_support", {item["code"] for item in result["issues"]})

    def test_missing_seadrive_file_is_reported(self) -> None:
        runtime = json.loads(self.runtime.read_text(encoding="utf-8"))
        runtime["items"][0]["linked_file_exists"] = False
        runtime["items"][0]["transport"] = "missing"
        runtime["summary"]["linked_files_resolved"] = 0
        runtime["summary"]["seadrive_linked_files_resolved"] = 0
        runtime["summary"]["all_registered_items_ready"] = False
        self._write_json(self.runtime, runtime)
        result = self.audit()
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("unresolved_runtime_attachment", codes)
        self.assertIn("runtime_transport_drift", codes)

    def test_runtime_snapshot_date_must_match_queue(self) -> None:
        runtime = json.loads(self.runtime.read_text(encoding="utf-8"))
        runtime["observed_at"] = "2026-08-31T12:00:00+08:00"
        self._write_json(self.runtime, runtime)
        result = self.audit()
        self.assertIn("runtime_scan_date_drift", {item["code"] for item in result["issues"]})

    def test_unrouted_content_gap_is_reported(self) -> None:
        acquisition = json.loads(self.acquisition.read_text(encoding="utf-8"))
        acquisition["work_items"] = []
        acquisition["active_work_item_id"] = "AQ-MISSING"
        self._write_json(self.acquisition, acquisition)
        result = self.audit()
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("unrouted_content_gap", codes)
        self.assertIn("missing_active_acquisition_item", codes)

    def test_unknown_acquisition_decision_is_reported(self) -> None:
        acquisition = json.loads(self.acquisition.read_text(encoding="utf-8"))
        acquisition["work_items"][0]["target_decision_ids"] = ["D-UNKNOWN"]
        self._write_json(self.acquisition, acquisition)
        result = self.audit()
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("unknown_acquisition_decision", codes)
        self.assertIn("unrouted_content_gap", codes)

    def test_blocked_acquisition_item_requires_registered_gate(self) -> None:
        acquisition = json.loads(self.acquisition.read_text(encoding="utf-8"))
        item = acquisition["work_items"][0]
        item["status"] = "blocked_on_gate"
        item["blocking_gate_id"] = "missing-gate"
        acquisition["active_work_item_id"] = "AQ-D1"
        self._write_json(self.acquisition, acquisition)
        result = self.audit()
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("missing_acquisition_gate", codes)
        self.assertIn("inactive_acquisition_pointer", codes)


if __name__ == "__main__":
    unittest.main()
