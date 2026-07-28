"""dense 임베딩 부재는 패키지 부재와 구분되어야 한다.

둘 다 exit 1 이면 호출부가 "Gemini 를 안 붙였다" 와 "google-genai 를 설치
안 했다" 를 구별할 수 없다. 앞은 의도된 선택 기능 비활성이고 뒤는 설치 결함이다.
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import build_search_index as bsi  # noqa: E402


class ExitCodeContractTests(unittest.TestCase):
    def test_the_two_codes_are_distinct_and_pinned(self):
        self.assertEqual(bsi.EXIT_MISSING_GENAI_PACKAGE, 1)
        self.assertEqual(bsi.EXIT_EMBEDDINGS_UNAVAILABLE, 5)
        self.assertNotEqual(bsi.EXIT_MISSING_GENAI_PACKAGE,
                            bsi.EXIT_EMBEDDINGS_UNAVAILABLE)

    def test_exit_five_is_not_already_used_for_another_meaning(self):
        """5 가 다른 실패에도 쓰이면 구분이 무너진다."""
        import re
        src = (PIPELINE / "build_search_index.py").read_text(encoding="utf-8")
        literal_fives = re.findall(r"sys\.exit\(\s*5\s*\)", src)
        self.assertEqual(literal_fives, [],
                         "exit 5 는 EXIT_EMBEDDINGS_UNAVAILABLE 상수로만 쓸 것")


class KeyResolutionTests(unittest.TestCase):
    """키 해석은 공용 해석기 하나만 거친다."""

    def test_module_uses_the_shared_resolver(self):
        from config_loader import get_google_key
        self.assertIs(bsi.get_google_key, get_google_key)

    def test_no_local_env_chain_survives(self):
        import re
        src = (PIPELINE / "build_search_index.py").read_text(encoding="utf-8")
        # 주석/메시지의 이름 언급은 허용, 실제 os.environ 읽기는 금지.
        reads = re.findall(r'os\.environ\.get\(\s*["\'](?:GOOGLE|GEMINI)_API_KEY',
                           src)
        self.assertEqual(reads, [],
                         "build_search_index 는 env 를 직접 읽지 않는다")

    def test_dead_config_reader_is_gone(self):
        self.assertFalse(hasattr(bsi, "_load_gemini_key_from_config"))

    def test_off_switch_is_honored_through_the_resolver(self):
        import config_loader
        with patch.dict("os.environ", {"GOOGLE_API_KEY": "AIza-x"}, clear=False):
            with patch.object(config_loader, "load_config", return_value={}):
                self.assertTrue(bsi.get_google_key())
            with patch.dict("os.environ",
                            {"PAPER_CURATION_NO_GEMINI": "1"}, clear=False):
                with patch.object(config_loader, "load_config", return_value={}):
                    self.assertEqual(bsi.get_google_key(), "")


if __name__ == "__main__":
    unittest.main()
