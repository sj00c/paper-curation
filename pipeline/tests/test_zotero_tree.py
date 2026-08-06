"""Zotero 컬렉션 트리를 분류 공급원으로 읽는 계약.

배경. 사용자는 Zotero 안에서 이미 논문을 분류해 둔다. 실제 라이브러리는 최상위
컬렉션(= 토픽) 아래에 사람이 만든 하위 컬렉션(= 카테고리)이 달린 트리다:

    AI for Science  15,388편
      ├ 01 General Methods & Platforms   3,984
      ├ 02 Biology & Medicine            2,920
      └ 99 Unclassified                  2,286

파이프라인은 최상위에서 논문만 긁고 이 구조를 버린 뒤 HDBSCAN 으로 카테고리를
새로 만들었다. 사람이 정리한 분류와 겹치지도 않는 별개 체계가 나온다.

실측: 리뷰 완료 3,273편 중 2,828편(86.4%)이 DOI 로 사람 분류에 그대로 붙었다
(제목 매칭 26편, 미매칭 6편, 99 Unclassified 439편).

여기서 고정하는 계약:
  - 하위 컬렉션이 카테고리가 되고, 이름순(01, 02 … 관례)을 지킨다.
  - 논문의 소속은 Zotero items 응답의 collections 필드에서 온다 (추가 API 0회).
  - 여러 컬렉션에 든 논문은 all_categories 에 전부 싣고 임의로 고르지 않는다.
  - "99 Unclassified" 만 있는 논문은 배정하지 않고 호출자에게 남긴다.
  - 출력은 classify_papers 가 쓰는 _new_classification.json 과 같은 형식이다.
"""

import os
import sys
import unittest

PIPELINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPELINE not in sys.path:
    sys.path.insert(0, PIPELINE)

from lib.zotero_tree import (  # noqa: E402
    _norm_doi, _norm_title, build_assignments, child_categories,
    find_root_key, is_unclassified, to_classification,
)

# 실제 라이브러리 모양을 축소한 것
COLLECTIONS = {
    "ROOT1": {"name": "AI for Science", "parent": None},
    "C01": {"name": "01 General Methods & Platforms", "parent": "ROOT1"},
    "C02": {"name": "02 Biology & Medicine", "parent": "ROOT1"},
    "C99": {"name": "99 Unclassified", "parent": "ROOT1"},
    "ROOT2": {"name": "Physical AI", "parent": None},
    "P01": {"name": "01 Perception & World Models", "parent": "ROOT2"},
}


class TreeShapeTests(unittest.TestCase):
    def test_children_are_the_categories(self):
        self.assertEqual(
            list(child_categories(COLLECTIONS, "ROOT1").values()),
            ["01 General Methods & Platforms", "02 Biology & Medicine", "99 Unclassified"],
        )

    def test_children_of_another_root_do_not_leak(self):
        self.assertEqual(list(child_categories(COLLECTIONS, "ROOT2").values()),
                         ["01 Perception & World Models"])

    def test_roots_are_found_by_name_or_key(self):
        self.assertEqual(find_root_key(COLLECTIONS, "AI for Science"), "ROOT1")
        self.assertEqual(find_root_key(COLLECTIONS, "ROOT1"), "ROOT1")
        self.assertEqual(find_root_key(COLLECTIONS, "nope"), "")


class NormalizationTests(unittest.TestCase):
    def test_doi_forms_collapse(self):
        for raw in ("10.1/AbC", "https://doi.org/10.1/abc",
                    "http://dx.doi.org/10.1/ABC", "doi:10.1/abc", " 10.1/abc "):
            with self.subTest(raw=raw):
                self.assertEqual(_norm_doi(raw), "10.1/abc")

    def test_title_ignores_case_punctuation_and_spacing(self):
        self.assertEqual(_norm_title("Deep  Learning: A Review!"),
                         _norm_title("deep learning a review"))

    def test_empty_inputs_are_empty(self):
        self.assertEqual(_norm_doi(""), "")
        self.assertEqual(_norm_title(None), "")


class AssignmentTests(unittest.TestCase):
    def setUp(self):
        self.cats = child_categories(COLLECTIONS, "ROOT1")

    def test_doi_match_wins(self):
        papers = [{"slug": "001_A", "doi": "10.1/a", "title": "irrelevant"}]
        items = [{"DOI": "https://doi.org/10.1/A", "title": "different",
                  "collections": ["C02", "ROOT1"]}]
        asg, stats = build_assignments(papers, items, self.cats)
        self.assertEqual(stats["matched_doi"], 1)
        self.assertEqual(asg[0]["primary_category"], "02 Biology & Medicine")

    def test_title_match_is_the_fallback(self):
        papers = [{"slug": "001_A", "doi": "", "title": "Deep Learning: A Review"}]
        items = [{"DOI": "", "title": "deep learning a review",
                  "collections": ["C01"]}]
        asg, stats = build_assignments(papers, items, self.cats)
        self.assertEqual(stats["matched_title"], 1)
        self.assertEqual(asg[0]["primary_category"], "01 General Methods & Platforms")

    def test_multiple_collections_are_all_kept(self):
        """사람이 두 곳에 넣었으면 둘 다 싣는다 — 임의로 하나를 고르지 않는다."""
        papers = [{"slug": "001_A", "doi": "10.1/a", "title": "t"}]
        items = [{"DOI": "10.1/a", "title": "t", "collections": ["C02", "C01"]}]
        asg, _ = build_assignments(papers, items, self.cats)
        self.assertEqual(asg[0]["all_categories"],
                         ["01 General Methods & Platforms", "02 Biology & Medicine"])
        self.assertEqual(asg[0]["primary_category"], "01 General Methods & Platforms")

    def test_unclassified_only_is_left_unassigned(self):
        """99 Unclassified 만 있으면 배정하지 않는다 (HDBSCAN 제안을 붙일 자리)."""
        papers = [{"slug": "001_A", "doi": "10.1/a", "title": "t"}]
        items = [{"DOI": "10.1/a", "title": "t", "collections": ["C99"]}]
        asg, stats = build_assignments(papers, items, self.cats)
        self.assertEqual(asg, [])
        self.assertEqual(stats["unclassified"], 1)

    def test_unclassified_can_be_included_on_request(self):
        """include 모드면 미분류도 하나의 카테고리로 쓴다."""
        papers = [{"slug": "001_A", "doi": "10.1/a", "title": "t"}]
        items = [{"DOI": "10.1/a", "title": "t", "collections": ["C99"]}]
        asg, stats = build_assignments(papers, items, self.cats,
                                       unclassified="include")
        self.assertEqual(len(asg), 1)
        self.assertEqual(asg[0]["primary_category"], "99 Unclassified")
        self.assertEqual(stats["unclassified"], 1)

    def test_include_mode_still_prefers_real_categories(self):
        """include 여도 사람이 분류해 둔 칸이 있으면 미분류는 가려진다."""
        papers = [{"slug": "001_A", "doi": "10.1/a", "title": "t"}]
        items = [{"DOI": "10.1/a", "title": "t", "collections": ["C99", "C02"]}]
        asg, _ = build_assignments(papers, items, self.cats, unclassified="include")
        self.assertEqual(asg[0]["all_categories"], ["02 Biology & Medicine"])

    def test_unknown_mode_is_rejected(self):
        """오타를 조용히 기본값으로 삼키면 안 된다."""
        with self.assertRaises(ValueError):
            build_assignments([], [], self.cats, unclassified="hdbscan")

    def test_unclassified_is_recognised_across_naming_conventions(self):
        """루트마다 이름이 다르다 — 실측: '99 Unclassified' vs 'Unclassified'."""
        for name in ("99 Unclassified", "Unclassified", "unclassified",
                     "90 Unclassified", "미분류"):
            with self.subTest(name=name):
                self.assertTrue(is_unclassified(name))
        for name in ("01 General Methods & Platforms", "Neuroscience", ""):
            with self.subTest(name=name):
                self.assertFalse(is_unclassified(name))

    def test_unclassified_does_not_hide_a_real_category(self):
        papers = [{"slug": "001_A", "doi": "10.1/a", "title": "t"}]
        items = [{"DOI": "10.1/a", "title": "t", "collections": ["C99", "C02"]}]
        asg, _ = build_assignments(papers, items, self.cats)
        self.assertEqual(asg[0]["all_categories"], ["02 Biology & Medicine"])

    def test_paper_absent_from_zotero_is_counted_not_guessed(self):
        papers = [{"slug": "001_A", "doi": "10.1/missing", "title": "nowhere"}]
        asg, stats = build_assignments(papers, [], self.cats)
        self.assertEqual(asg, [])
        self.assertEqual(stats["unmatched"], 1)

    def test_root_only_membership_is_not_a_category(self):
        """최상위에만 든 논문은 카테고리가 없다 — ROOT 는 카테고리가 아니다."""
        papers = [{"slug": "001_A", "doi": "10.1/a", "title": "t"}]
        items = [{"DOI": "10.1/a", "title": "t", "collections": ["ROOT1"]}]
        asg, stats = build_assignments(papers, items, self.cats)
        self.assertEqual(asg, [])
        self.assertEqual(stats["unmatched"], 1)

    def test_other_topics_collections_are_ignored(self):
        papers = [{"slug": "001_A", "doi": "10.1/a", "title": "t"}]
        items = [{"DOI": "10.1/a", "title": "t", "collections": ["P01"]}]
        asg, _ = build_assignments(papers, items, self.cats)
        self.assertEqual(asg, [])


class OutputContractTests(unittest.TestCase):
    """classify_papers 가 쓰는 형식과 같아야 하류가 그대로 돈다."""

    def test_shape_matches_new_classification_json(self):
        asg = [{"slug": "001_A", "primary_category": "B", "all_categories": ["B"],
                "sub_category": ""},
               {"slug": "002_B", "primary_category": "A", "all_categories": ["A"],
                "sub_category": ""}]
        out = to_classification(asg)
        self.assertEqual(sorted(out.keys()), ["assignments", "categories"])
        self.assertEqual(out["categories"], [{"name": "A"}, {"name": "B"}])
        self.assertEqual(len(out["assignments"]), 2)

    def test_assignment_keys_match_the_classifier(self):
        papers = [{"slug": "001_A", "doi": "10.1/a", "title": "t"}]
        items = [{"DOI": "10.1/a", "title": "t", "collections": ["C01"]}]
        asg, _ = build_assignments(papers, items, child_categories(COLLECTIONS, "ROOT1"))
        self.assertEqual(sorted(asg[0].keys()),
                         ["all_categories", "primary_category", "slug", "sub_category"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
