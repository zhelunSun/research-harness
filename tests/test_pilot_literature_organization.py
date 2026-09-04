import copy
import unittest

from scripts.pilot_literature_organization import archived_view_check, fuse, measure, metadata_view, run


def entry(key, bib=None):
    return {"id": key, "title": key, "bibtex_key": bib, "evidence": [], "packets": []}


class OrganizationPilotTests(unittest.TestCase):
    def test_metadata_ablation_does_not_mutate_evidence(self):
        original = {"facets": [{"id": "f"}], "entries": [{**entry("A"), "evidence": [{"claim": "unresolved"}], "packets": ["p"]}], "query_expansions": {"经验": ["experience"]}}
        before = copy.deepcopy(original)
        view = metadata_view(original)
        self.assertEqual(original, before)
        self.assertEqual(view["entries"][0]["evidence"], [])
        self.assertEqual(view["facets"], [])
        self.assertEqual(view["query_expansions"], original["query_expansions"])

    def test_fusion_uses_both_paths_without_duplicate_ids(self):
        a, b, c = entry("A"), entry("B"), entry("C")
        result = fuse([a, b], [c, b])
        self.assertEqual(result[0]["id"], "B")
        self.assertEqual(len({e["id"] for e in result}), len(result))

    def test_empty_path_preserves_other_path(self):
        self.assertEqual(fuse([], [entry("A")]), [entry("A")])

    def test_related_preprint_does_not_count_as_published_edition(self):
        preprint = {**entry("preprint"), "related_items": [{"bibtex_key": "published"}]}
        self.assertEqual(measure([preprint], ["published"])["coverage_at_5"], 0)

    def test_non_anchor_is_unjudged_not_precision_error(self):
        measured = measure([entry("A", "one"), entry("B", "unknown")], ["one", "two"])
        self.assertEqual(measured["coverage_at_5"], 0.5)
        self.assertNotIn("precision", measured)

    def test_archive_keeps_catalog_and_view_members(self):
        catalog = {"entries": [entry("A"), entry("B")]}
        before = copy.deepcopy(catalog)
        result = archived_view_check(catalog, ["A"])
        self.assertEqual(catalog, before)
        self.assertTrue(result["catalog_unchanged"])
        self.assertEqual(result["records_retained"], 2)

    def test_unknown_anchor_fails_before_evaluation(self):
        catalog = {"entries": [entry("A", "one")], "facets": []}
        with self.assertRaisesRegex(ValueError, "unknown anchor"):
            run(catalog, {"cases": [{"id": "x", "anchors": ["missing"]}]})


if __name__ == "__main__":
    unittest.main()
