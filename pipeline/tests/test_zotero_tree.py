"""Zotero 컬렉션 트리를 분류 공급원으로 읽는 계약.

배경. 사용자는 Zotero 안에서 이미 논문을 분류해 둔다. 실제 라이브러리는 최상위
컬렉션(= 토픽) 아래에 사람이 만든 하위 컬렉션(= 카테고리)이 달린 트리다:

    My Research
      ├ 01 Methods
      ├ 02 Applications
      └ 99 Unclassified

파이프라인은 최상위에서 논문만 긁고 이 구조를 버린 뒤 HDBSCAN 으로 카테고리를
새로 만들었다. 사람이 정리한 분류와 겹치지도 않는 별개 체계가 나온다.

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


class LocalDbTests(unittest.TestCase):
    """로컬 zotero.sqlite 경로.

    같은 데이터를 Web API 로 받으면 자식 컬렉션마다 100건씩 페이징해야 해서
    ai4s(15,399건) 기준 수 분이 걸린다. sqlite 는 복사 + 쿼리 한 번으로 0.1초고,
    네트워크도 API 키도 필요 없다. 실측: 전체 분류가 2.3초, 결과는 Web API 와
    완전히 동일(3,267/3,273 배정).

    Zotero 가 실행 중이면 원본 DB 가 잠기므로 복사본을 읽는다 —
    lib/citedby/local_library.py 와 같은 방식이다.
    """

    def _make_db(self, path):
        import sqlite3

        con = sqlite3.connect(path)
        con.executescript("""
            CREATE TABLE collections (collectionID INTEGER PRIMARY KEY,
                collectionName TEXT, parentCollectionID INTEGER, key TEXT);
            CREATE TABLE collectionItems (collectionID INTEGER, itemID INTEGER);
            CREATE TABLE itemData (itemID INTEGER, fieldID INTEGER, valueID INTEGER);
            CREATE TABLE itemDataValues (valueID INTEGER PRIMARY KEY, value TEXT);
            CREATE TABLE fields (fieldID INTEGER PRIMARY KEY, fieldName TEXT);
            CREATE TABLE deletedItems (itemID INTEGER PRIMARY KEY);
            INSERT INTO collections VALUES (1,'AI for Science',NULL,'ROOT1'),
                                           (2,'01 Methods',1,'C01'),
                                           (3,'02 Biology',1,'C02');
            INSERT INTO fields VALUES (1,'DOI'),(2,'title');
            INSERT INTO itemDataValues VALUES (10,'10.1/a'),(11,'Paper A'),
                                              (12,'10.1/b'),(13,'Paper B');
            INSERT INTO itemData VALUES (100,1,10),(100,2,11),(101,1,12),(101,2,13);
            INSERT INTO collectionItems VALUES (2,100),(3,100),(2,101);
        """)
        con.commit()
        con.close()

    def test_collections_match_the_web_api_shape(self):
        import tempfile

        from lib.zotero_tree import fetch_collections_local

        with tempfile.TemporaryDirectory() as td:
            db = os.path.join(td, "zotero.sqlite")
            self._make_db(db)
            cols = fetch_collections_local(db)
        self.assertEqual(cols["ROOT1"], {"name": "AI for Science", "parent": None})
        self.assertEqual(cols["C01"], {"name": "01 Methods", "parent": "ROOT1"})
        self.assertEqual(list(child_categories(cols, "ROOT1").values()),
                         ["01 Methods", "02 Biology"])

    def test_items_carry_every_collection_they_belong_to(self):
        import tempfile

        from lib.zotero_tree import fetch_items_local

        with tempfile.TemporaryDirectory() as td:
            db = os.path.join(td, "zotero.sqlite")
            self._make_db(db)
            items = fetch_items_local("ROOT1", db)

        by_doi = {i["DOI"]: i for i in items}
        self.assertEqual(sorted(by_doi["10.1/a"]["collections"]), ["C01", "C02"])
        self.assertEqual(by_doi["10.1/b"]["collections"], ["C01"])
        self.assertEqual(by_doi["10.1/a"]["title"], "Paper A")

    def test_local_items_feed_build_assignments_unchanged(self):
        """sqlite 출력이 Web API 출력과 같은 형식이라 그대로 물린다."""
        import tempfile

        from lib.zotero_tree import fetch_collections_local, fetch_items_local

        with tempfile.TemporaryDirectory() as td:
            db = os.path.join(td, "zotero.sqlite")
            self._make_db(db)
            cols = fetch_collections_local(db)
            items = fetch_items_local("ROOT1", db)

        cats = child_categories(cols, "ROOT1")
        papers = [{"slug": "001_A", "doi": "10.1/a", "title": "Paper A"}]
        asg, stats = build_assignments(papers, items, cats)
        self.assertEqual(stats["matched_doi"], 1)
        self.assertEqual(asg[0]["all_categories"], ["01 Methods", "02 Biology"])

    def test_deleted_items_are_excluded(self):
        """휴지통에 넣은 논문이 카테고리에 남으면 안 된다."""
        import sqlite3
        import tempfile

        from lib.zotero_tree import fetch_items_local

        with tempfile.TemporaryDirectory() as td:
            db = os.path.join(td, "zotero.sqlite")
            self._make_db(db)
            con = sqlite3.connect(db)
            con.execute("INSERT INTO deletedItems VALUES (100)")
            con.commit()
            con.close()
            items = fetch_items_local("ROOT1", db)
        self.assertEqual([i["DOI"] for i in items], ["10.1/b"])

    def test_missing_db_returns_none_so_caller_can_fall_back(self):
        from lib.zotero_tree import (fetch_collections_local, fetch_items_local,
                                     local_db_path)

        self.assertIsNone(local_db_path("/nonexistent/zotero.sqlite"))
        self.assertIsNone(fetch_collections_local("/nonexistent/zotero.sqlite"))
        self.assertIsNone(fetch_items_local("ROOT1", "/nonexistent/zotero.sqlite"))

    def test_env_var_overrides_the_default_location(self):
        import tempfile
        from unittest.mock import patch

        from lib.zotero_tree import local_db_path

        with tempfile.TemporaryDirectory() as td:
            db = os.path.join(td, "custom.sqlite")
            open(db, "wb").close()
            with patch.dict(os.environ, {"ZOTERO_SQLITE": db}):
                self.assertEqual(str(local_db_path()), db)

    def test_original_db_is_not_opened_directly(self):
        """Zotero 실행 중 잠금을 피하려면 복사본을 읽어야 한다."""
        import inspect

        from lib import zotero_tree

        src = inspect.getsource(zotero_tree._open_readonly)
        self.assertIn("copy2", src)
        self.assertIn("mode=ro", src)


class CliWiringTests(unittest.TestCase):
    """classify_papers 의 공급원 선택 계약.

    upstream 사용자에게 영향이 없어야 하므로 기본값은 hdbscan 이고 Zotero 경로는
    opt-in 이다. 플래그를 엉뚱한 공급원에 붙이면 조용히 무시하지 않고 멈춘다 —
    --slugs 를 zotero 에 붙이면 "일부만 반영됐다"고 착각하게 된다.
    """

    def _dispatch(self, argv):
        from unittest.mock import patch

        import classify_papers

        calls = {}
        with patch.object(sys, "argv", ["classify_papers.py", *argv]), \
             patch.object(classify_papers, "_run_classify",
                          lambda **kw: calls.setdefault("hdbscan", kw)), \
             patch.object(classify_papers, "_run_classify_zotero",
                          lambda **kw: calls.setdefault("zotero", kw)), \
             patch("config_loader.resolve_topic", return_value="t"):
            classify_papers.main()
        return calls

    def test_default_source_is_hdbscan(self):
        """기존 동작 보호 — 아무것도 안 주면 예전과 같은 경로."""
        calls = self._dispatch([])
        self.assertIn("hdbscan", calls)
        self.assertNotIn("zotero", calls)

    def test_zotero_source_is_opt_in(self):
        calls = self._dispatch(["--classify-source", "zotero"])
        self.assertIn("zotero", calls)
        self.assertEqual(calls["zotero"]["unclassified"], "skip")

    def test_unclassified_flag_reaches_the_zotero_path(self):
        calls = self._dispatch(["--classify-source", "zotero",
                                "--unclassified", "include"])
        self.assertEqual(calls["zotero"]["unclassified"], "include")

    def test_slugs_with_zotero_is_refused(self):
        with self.assertRaises(SystemExit):
            self._dispatch(["--classify-source", "zotero", "--slugs", "001"])

    def test_unclassified_without_zotero_is_refused(self):
        with self.assertRaises(SystemExit):
            self._dispatch(["--unclassified", "include"])

class OperatorExtensionUnclassifiedGuardTests(unittest.TestCase):
    """The explicit legacy operator extension still rejects dropped flags."""

    def test_run_update_force_rejects_unclassified_on_hdbscan(self):
        """blk-1: behaviorally bind run_update_force's guard, not just its source text.

        The guard sits before resolve_topic, so a correct guard raises SystemExit with
        zero I/O. resolve_topic is patched to raise a NON-SystemExit error: if the guard
        is ever mutated to a no-op (raise->pass), execution falls through to that patch
        and the RuntimeError propagates, failing assertRaises(SystemExit) cleanly without
        touching Zotero. A source-regex test alone let that exact mutation pass green.
        """
        from unittest.mock import patch

        import run_update_force
        argv = ["run_update_force.py", "--topic", "t",
                "--unclassified", "include", "--dry-run"]
        with patch("config_loader.resolve_topic",
                   side_effect=RuntimeError("guard should have stopped this run")), \
                patch.object(sys, "argv", argv):
            with self.assertRaises(SystemExit):
                run_update_force.main()

    def test_guard_raises_in_operator_extension(self):
        """소스에 조건뿐 아니라 `raise` 까지 있어야 한다.

        기존 정규식은 조건 두 줄만 매칭해서, `raise SystemExit` 를 `pass` 로 바꾼
        변이(=gen-1 침묵 드롭 재현)도 통과했다. raise 를 요구하도록 조인다.
        """
        import re

        pattern = re.compile(
            r'unclassified.*!=.*"skip"[\s\S]{0,200}?'
            r'classify_source.*!=.*"zotero"[\s\S]{0,200}?raise SystemExit')
        sources = {"run_update_force": os.path.join(PIPELINE, "run_update_force.py")}
        for name, path in sources.items():
            src = open(path, encoding="utf-8").read()
            self.assertRegex(
                src, pattern,
                f"{name}.py lacks a raising --unclassified fail-fast guard",
            )



if __name__ == "__main__":
    unittest.main(verbosity=2)
