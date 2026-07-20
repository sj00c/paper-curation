"""Regression tests for scalable Zotero slug allocation."""

import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import config_loader  # noqa: E402

with (
    patch.object(config_loader, "get_zotero_api_key", return_value="test-key"),
    patch.object(config_loader, "get_zotero_user_id", return_value="123"),
    patch.object(config_loader, "get_zotero_dir", return_value="/tmp/paper-curation-slug-test"),
    patch.object(config_loader, "get_collections", return_value={}),
):
    import run_update_force as update  # noqa: E402
SlugAllocator = getattr(update, "_SlugAllocator")
map_items_to_slugs = getattr(update, "_map_items_to_slugs")


class SlugAllocatorTests(unittest.TestCase):
    @staticmethod
    def _legacy_allocate(item, existing_slugs):
        title = item.get("title", "Unknown")
        norm_title = re.sub(r"[^a-z0-9]", "", title.lower())
        if len(norm_title) >= 10:
            for slug in existing_slugs:
                parts = slug.split("_", 1)
                if len(parts) < 2:
                    continue
                slug_text = re.sub(r"[^a-z0-9]", "", parts[1].lower())
                if len(slug_text) < 10:
                    continue
                match_len = min(40, len(norm_title), len(slug_text))
                if norm_title[:match_len] == slug_text[:match_len]:
                    return slug
        safe = "".join(
            char if char.isalnum() or char in " -_" else ""
            for char in title
        )[:60].strip().replace(" ", "_")
        maximum = max(
            (int(match.group(1)) for slug in existing_slugs if (match := re.match(r"(\d+)_", slug))),
            default=0,
        )
        return f"{maximum + 1:03d}_{safe}"

    def test_allocator_preserves_legacy_first_match_and_numbering(self):
        initial = [
            "007_Robot_Learning_from_Human_Videos_A_Survey",
            "012_A_hierarchical_framework_for_measuring_scientific_impact",
        ]
        items = [
            {"title": "Robot Learning from Human Videos: A Survey"},
            {"title": "A Hierarchical Framework for Humanoid Locomotion with Supernumerary Limbs"},
            {"title": "Novel Methods for Reliable Scientific Discovery"},
            {"title": "Novel Methods for Reliable Scientific Discovery"},
        ]
        legacy_slugs = list(initial)
        expected = []
        for item in items:
            slug = self._legacy_allocate(item, legacy_slugs)
            expected.append(slug)
            if slug not in legacy_slugs:
                legacy_slugs.append(slug)

        allocator = SlugAllocator(initial)
        actual = [allocator.allocate(item) for item in items]

        self.assertEqual(actual, expected)
        self.assertNotEqual(actual[1], initial[1])
        self.assertEqual(actual[2], actual[3])

    def test_allocator_handles_full_collection_scale(self):
        allocator = SlugAllocator([])
        slugs = [
            allocator.allocate({"title": f"T{i:08d} Unique Scientific Paper"})
            for i in range(15_304)
        ]

        self.assertEqual(len(set(slugs)), 15_304)
        self.assertTrue(slugs[-1].startswith("15304_"))

    def test_duplicate_titles_collapse_to_richer_metadata_record(self):
        title = "A sufficiently long duplicate scientific paper title for matching"
        items = [
            {"key": "BASIC", "title": title},
            {
                "key": "RICH",
                "title": title,
                "DOI": "10.1000/example",
                "abstractNote": "Detailed abstract",
            },
        ]

        item_slug_map = {}
        pairs, duplicate_count, skipped_untitled = map_items_to_slugs(
            items, [], item_slug_map
        )

        self.assertEqual(duplicate_count, 1)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][0]["key"], "RICH")
        self.assertEqual(skipped_untitled, 0)
        self.assertEqual(
            item_slug_map["BASIC"],
            item_slug_map["RICH"],
        )

    def test_markup_is_removed_and_untitled_records_are_skipped(self):
        items = [
            {
                "key": "MARKUP",
                "title": "&lt;b&gt;Artificial Intelligence &amp; Science&lt;/b&gt;",
            },
            {"key": "EMPTY", "title": "  "},
        ]

        pairs, duplicate_count, skipped_untitled = map_items_to_slugs(items, [])

        self.assertEqual(duplicate_count, 0)
        self.assertEqual(skipped_untitled, 1)
        self.assertEqual(len(pairs), 1)
        item, slug = pairs[0]
        self.assertEqual(item["title"], "Artificial Intelligence & Science")
        self.assertNotIn("ltbgt", slug)
    def test_terminal_failure_keys_survive_numeric_slug_changes(self):
        checkpoint = {
            "completed": [],
            "failed": [
                {
                    "slug": "123_Metadata_only_scientific_paper",
                    "reason": "no_pdf:no_match",
                },
                {
                    "slug": "456_Metadata_only_scientific_paper",
                    "reason": "no_pdf:no_match",
                },
            ],
        }
        pairs = [
            (
                {"key": "STABLE-KEY", "title": "Metadata only scientific paper"},
                "999_Metadata_only_scientific_paper",
            ),
        ]

        matched, removed = update._backfill_terminal_failure_keys(
            checkpoint, pairs
        )

        self.assertEqual(matched, 2)
        self.assertEqual(removed, 1)
        self.assertEqual(checkpoint["failed"][0]["key"], "STABLE-KEY")
    def test_checkpoint_mapping_stabilizes_short_title_slug(self):
        mapping = {"SHORT": "007_AI_Safety"}
        first, _, _ = map_items_to_slugs(
            [{"key": "SHORT", "title": "AI Safety"}],
            ["999_Unrelated_existing_paper"],
            mapping,
        )
        second, _, _ = map_items_to_slugs(
            [{"key": "SHORT", "title": "AI Safety"}],
            ["1500_Another_unrelated_paper"],
            mapping,
        )

        self.assertEqual(first[0][1], "007_AI_Safety")
        self.assertEqual(second[0][1], "007_AI_Safety")


if __name__ == "__main__":
    unittest.main()
