"""Mutation tests ensure the proposal audit does not turn gaps into success."""

import json
import unittest
from pathlib import Path

from audit_packet import PACKET, audit


class ProposalAuditTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads((PACKET / "specification.json").read_text(encoding="utf-8"))

    def result(self):
        return audit(self.spec, Path("unused-chapter-root"), verify_assets=False)

    def test_candidate_pass_is_not_benchmark_readiness(self):
        result = self.result()
        self.assertTrue(result["ok"])
        self.assertEqual(result["scientific_validity"], "not-assessed")
        self.assertEqual(result["benchmark_release"], "not-ready")
        self.assertTrue(result["known_missing_asset_paths"])

    def test_cycle_is_rejected(self):
        self.spec["tasks"][0]["depends_on"] = ["S"]
        self.assertFalse(self.result()["ok"])

    def test_missing_product_is_rejected(self):
        self.spec["tasks"][1]["consumes"].append("invented_output")
        self.assertFalse(self.result()["ok"])

    def test_unlinked_producer_is_rejected(self):
        self.spec["tasks"][1]["depends_on"] = []
        self.assertFalse(self.result()["ok"])

    def test_gold_promotion_is_rejected(self):
        self.spec["approvals"]["scientific_gold_accepted"] = True
        self.assertFalse(self.result()["ok"])

    def test_answer_leakage_is_rejected(self):
        self.spec["solver_visible_inputs"].append("reference_results")
        self.assertFalse(self.result()["ok"])

    def test_scope_approval_is_not_assumed(self):
        self.spec["scope"]["approval_status"] = "accepted"
        self.assertFalse(self.result()["ok"])

    def test_path_escape_is_rejected(self):
        self.spec["assets"][0]["path"] = "../outside.json"
        self.assertFalse(self.result()["ok"])

    def test_missing_asset_reference_is_rejected(self):
        self.spec["tasks"][0]["asset_refs"].append("A999")
        self.assertFalse(self.result()["ok"])


if __name__ == "__main__":
    unittest.main()
