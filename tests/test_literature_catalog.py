from __future__ import annotations

from datetime import datetime, timezone
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.literature_catalog import CACHE, arxiv, build_catalog, cache_delta, exact_lookup, fingerprints, identity_matches, main, read_pages, search


def item(key="PARENT01", **fields):
    return {"key": key, "data": {"itemType": "journalArticle", "title": "Knowledge to Action", "dateAdded": "2026-09-01T00:00:00Z", **fields}}


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.lit = self.root / "evidence/literature"
        self.packet = self.lit / "packets/test"
        self.packet.mkdir(parents=True)
        self.source = {"source_id": "S1", "title": "Knowledge to Action", "locator": "https://doi.org/10.1/published", "identifiers": {"doi": "10.1/published"}, "zotero_item_key": "PARENT01", "bibtex_key": "paper_2026", "read_state": "full_text"}
        self.ledger = {"sources": [self.source], "claims": [{"claim_id": "C1", "text": "专家经验可以引导行动", "evidence_status": "needs_review"}], "links": [{"claim_id": "C1", "source_id": "S1", "relation": "context", "entailment_status": "unassessed"}]}
        self.write(self.packet / "ledger.json", self.ledger)
        self.write(self.lit / "packet_registry.json", {"packets": [{"packet_id": "test", "path": "evidence/literature/packets/test"}]})
        self.write(self.lit / "retrieval_facets.json", {"facets": [{"id": "knowledge", "terms": ["专家经验", "knowledge"], "packets": ["test"]}]})

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, data):
        path.write_text(json.dumps(data), encoding="utf-8")

    def build(self, items=None):
        return build_catalog(self.root, items or [item(DOI="10.1/published")], [], datetime(2026, 9, 4, tzinfo=timezone.utc))

    def test_preprint_and_publication_not_silently_equated(self):
        match = identity_matches(self.source, [item(DOI="10.48550/arXiv.2403.03101")])
        self.assertEqual(match[0]["match"], "title_candidate_version_review")

    def test_exact_identifier_survives_title_change(self):
        match = identity_matches(self.source, [item(title="Revised title", DOI="https://doi.org/10.1/PUBLISHED")])
        self.assertEqual(match[0]["match"], "exact_identifier")

    def test_arxiv_revision_is_work_not_exact_version(self):
        self.assertEqual(arxiv("https://arxiv.org/pdf/2512.15231v3"), "2512.15231")
        source = {"identifiers": {"arxiv": "2512.15231"}, "title": "Earlier title"}
        self.assertEqual(identity_matches(source, [item(url="https://arxiv.org/abs/2512.15231v1")])[0]["match"], "same_arxiv_work_version_unchecked")

    def test_wrong_registered_key_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
            self.build([item("OTHER001", DOI="10.1/published")])

    def test_registered_key_cannot_mask_conflicting_publication_doi(self):
        with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
            self.build([item(DOI="10.1/preprint")])

    def test_bilingual_hint_retrieves_english_library_title(self):
        catalog = self.build([item(DOI="10.1/published"), item("EXPER001", title="Experiential Learning")])
        catalog["query_expansions"] = {"经验": ["experiential"]}
        self.assertIn("EXPER001", [k for e in search(catalog, "经验") for k in e["zotero_item_keys"]])

    def test_failed_live_scan_preserves_previous_cache(self):
        cache = self.root / CACHE
        cache.parent.mkdir(parents=True)
        cache.write_bytes(b"last valid cache")
        with patch("scripts.literature_catalog.discover_zotero_helper", return_value=Path("unused")), patch("scripts.literature_catalog._helper_json", return_value={"api_running": True, "api_status": 200}), patch("scripts.literature_catalog.read_pages", side_effect=RuntimeError("incomplete pagination")), patch("sys.stdout", new_callable=io.StringIO):
            self.assertEqual(main(["--root", str(self.root), "scan", "--write"]), 1)
        self.assertEqual(cache.read_bytes(), b"last valid cache")

    def test_child_objects_are_not_papers_and_private_payload_is_excluded(self):
        catalog = self.build([item(DOI="10.1/published"), item("ATTACH01", itemType="attachment", parentItem="PARENT01", contentType="application/pdf", path="SECRET_LOCAL_PATH"), item("NOTE0001", itemType="note", parentItem="PARENT01", note="PRIVATE_NOTE_BODY")])
        self.assertEqual(catalog["summary"]["bibliographic_items"], 1)
        self.assertEqual(catalog["entries"][0]["zotero"]["pdf_attachment_count"], 1)
        self.assertNotIn("PRIVATE_NOTE_BODY", json.dumps(catalog))
        self.assertNotIn("SECRET_LOCAL_PATH", json.dumps(catalog))

    def test_question_retrieval_preserves_unresolved_claim(self):
        result = search(self.build(), "专家经验如何影响行动")
        self.assertEqual(result[0]["title"], "Knowledge to Action")
        self.assertEqual(result[0]["evidence"][0]["status"], "needs_review")
        self.assertEqual(result[0]["writing_eligibility"], "not_accepted_by_this_catalog")

    def test_unread_library_item_stays_metadata_even_with_read_tag(self):
        catalog = self.build([item(DOI="10.1/published"), item("UNREAD01", title="Unread", tags=[{"tag": "full_text"}])])
        self.assertEqual(catalog["entries"][1]["read_state"], "metadata")

    def test_cross_packet_reuse_does_not_inflate_unique_source_count(self):
        self.write(self.lit / "packet_registry.json", {"packets": [{"packet_id": "one", "path": "evidence/literature/packets/test"}, {"packet_id": "two", "path": "evidence/literature/packets/test"}]})
        cat = self.build()
        self.assertEqual(cat["summary"]["packet_source_entries"], 2)
        self.assertEqual(cat["summary"]["unique_packet_sources"], 1)
        self.assertEqual(cat["entries"][0]["zotero_item_keys"], ["PARENT01"])

    def test_fingerprints_invalidate_changed_evidence(self):
        paths = [Path("evidence/literature/packets/test/ledger.json")]
        before = fingerprints(self.root, paths)
        self.ledger["claims"][0]["evidence_status"] = "rejected"
        self.write(self.packet / "ledger.json", self.ledger)
        self.assertNotEqual(before, fingerprints(self.root, paths))

    def test_delta_distinguishes_first_scan_and_real_changes(self):
        initial = {"entries": [{"id": "a", "title": "old"}]}
        self.assertEqual(cache_delta(None, initial)["added_entry_ids"], [])
        changed = {"entries": [{"id": "a", "title": "new"}, {"id": "b"}]}
        delta = cache_delta(initial, changed)
        self.assertEqual(delta["changed_entry_ids"], ["a"])
        self.assertEqual(delta["added_entry_ids"], ["b"])

    def test_incomplete_api_read_is_not_an_empty_library(self):
        def opener(*args, **kwargs):
            response = io.BytesIO(b"[]")
            response.headers = {"Total-Results": "5"}
            return response
        with self.assertRaisesRegex(RuntimeError, "incomplete"):
            read_pages("items", opener)

    def test_unknown_facet_does_not_select_everything(self):
        self.assertEqual(search(self.build(), "", facet="unknown"), [])

    def test_exact_doi_is_not_ranked_as_the_number_ten(self):
        cat = {"entries": [{"id": "distractor", "title": "10 metre mapping"}, {"id": "target", "title": "Target", "zotero": {"doi": "10.1038/s41586-026-10644-y"}}]}
        result = exact_lookup(cat, "https://doi.org/10.1038/S41586-026-10644-Y")
        self.assertEqual(result["route"], "exact_doi")
        self.assertEqual([e["id"] for e in result["results"]], ["target"])
        self.assertEqual(exact_lookup(cat, "10.1038/does-not-exist")["results"], [])

    def test_exact_doi_preserves_multiple_records_for_review(self):
        cat = {"entries": [{"id": "one", "locator": "https://doi.org/10.1234/example"}, {"id": "two", "zotero": {"doi": "10.1234/example"}}]}
        self.assertEqual(len(exact_lookup(cat, "10.1234/example")["results"]), 2)

    def test_exact_key_and_title_do_not_merge_versions(self):
        cat = self.build()
        self.assertEqual(exact_lookup(cat, "paper_2026")["route"], "exact_key")
        self.assertEqual(exact_lookup(cat, "PARENT01")["route"], "exact_key")
        self.assertEqual(exact_lookup(cat, "Knowledge to Action")["route"], "exact_title")
        self.assertIsNone(exact_lookup(cat, "a rough question about action"))


if __name__ == "__main__":
    unittest.main()
