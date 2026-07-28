"""Offline contract tests for the bounded, read-only Zotero reader."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

from lib.zotero_bounded import (  # noqa: E402
    TransportResponse, ZoteroBoundedError, ZoteroBoundedReader, ZoteroBounds,
    bounded_scratch_pdf, validate_pdf_text,
)


def item(key, date, **data):
    return {"data": {"key": key, "dateAdded": date, **data}}


def response(body, *, total="0", version="1", status=200, **headers):
    encoded = body if isinstance(body, bytes) else json.dumps(body).encode()
    return TransportResponse(status, {"Total-Results": total,
                                      "Last-Modified-Version": version, **headers}, encoded)


class SpyTransport:
    def __init__(self, callback):
        self.callback = callback
        self.calls = []

    def request(self, method, url, headers, **kwargs):
        self.calls.append((method, url, dict(headers), kwargs))
        return self.callback(method, url)


class BoundedZoteroE2E(unittest.TestCase):
    def reader(self, transport, **bounds):
        return ZoteroBoundedReader(transport, "test-key", "42", bounds=ZoteroBounds(**bounds))

    def test_complete_pagination_is_pinned_and_sorted_read_only(self):
        pages = {
            "0": [item(f"k{n:03}", f"2024-01-{n + 1:03}") for n in range(100)],
            "100": [item("a", "2023-12-31")],
        }
        def fixture(method, url):
            self.assertEqual(method, "GET")
            start = parse_qs(urlsplit(url).query)["start"][0]
            return response(pages[start], total="101", version="9")
        spy = SpyTransport(fixture)
        result = self.reader(spy).collection_items("C")
        self.assertEqual(result[0]["data"]["key"], "a")
        self.assertEqual(result[-1]["data"]["key"], "k099")
        self.assertEqual([parse_qs(urlsplit(x[1]).query)["start"][0] for x in spy.calls], ["0", "100"])
        self.assertTrue(all(call[0] == "GET" for call in spy.calls))

    def test_pagination_rejects_duplicate_missing_and_version_drift(self):
        cases = [
            ([item("a", "1"), item("a", "2")], "2", "duplicate-item-key"),
            ([item("a", "1")], "2", "total-results-mismatch"),
        ]
        for body, total, expected in cases:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ZoteroBoundedError, expected):
                    self.reader(SpyTransport(lambda *_: response(body, total=total))).collection_items("C")
        calls = 0
        def drift(*_):
            nonlocal calls
            calls += 1
            batch = [item(f"{calls}-{n}", str(n)) for n in range(100 if calls == 1 else 1)]
            return response(batch, total="101", version=str(calls))
        with self.assertRaisesRegex(ZoteroBoundedError, "pagination-drift"):
            self.reader(SpyTransport(drift)).collection_items("C")

    def test_total_and_tenth_page_ceiling_stop_without_another_request(self):
        over = SpyTransport(lambda *_: response([], total="1001"))
        with self.assertRaisesRegex(ZoteroBoundedError, "total-results-budget"):
            self.reader(over).collection_items("C")
        self.assertEqual(len(over.calls), 1)
        def full(method, url):
            start = int(parse_qs(urlsplit(url).query)["start"][0])
            return response([item(f"{start}-{n}", f"{start}-{n}") for n in range(100)], total="1000")
        spy = SpyTransport(full)
        self.assertEqual(len(self.reader(spy).collection_items("C")), 1000)
        self.assertEqual(len(spy.calls), 10)

    def test_request_and_response_budgets_fail_before_next_effect(self):
        spy = SpyTransport(lambda *_: response([], total="1"))
        with self.assertRaisesRegex(ZoteroBoundedError, "attempt-budget"):
            self.reader(spy, max_attempts=0).collection_items("C")
        self.assertEqual(spy.calls, [])
        spy = SpyTransport(lambda *_: response([], total="0", **{"Content-Length": "21"}))
        with self.assertRaisesRegex(ZoteroBoundedError, "metadata-response-budget"):
            self.reader(spy, max_response_bytes=20).collection_items("C")

    def test_redirects_require_exact_https_origin_and_are_bounded(self):
        for location in ("http://api.zotero.org/x", "https://evil.example/x"):
            spy = SpyTransport(lambda *_: TransportResponse(302, {"Location": location}))
            with self.subTest(location=location), self.assertRaisesRegex(ZoteroBoundedError, "unsafe-redirect-origin"):
                self.reader(spy).collection_items("C")
        spy = SpyTransport(lambda *_: TransportResponse(302, {"Location": "/again"}))
        with self.assertRaisesRegex(ZoteroBoundedError, "redirect-request-budget"):
            self.reader(spy).collection_items("C")
        self.assertEqual(len(spy.calls), 3)

    def test_parent_and_attachment_plus_one_limits_make_no_request(self):
        parent = item("p", "1")
        spy = SpyTransport(lambda *_: response([], total="0"))
        reader = self.reader(spy, max_parent_lookups=0)
        with self.assertRaisesRegex(ZoteroBoundedError, "parent-lookup-budget"):
            reader.children(parent)
        self.assertEqual(spy.calls, [])
        parents = [item(f"p{n}", str(n)) for n in range(21)]
        def children(method, url):
            key = url.split("/items/")[1].split("/")[0]
            return response([item("a" + key, "1", itemType="attachment", parentItem=key,
                                  contentType="application/pdf")])
        spy = SpyTransport(children)
        reader = self.reader(spy, max_attachment_heads=0)
        with self.assertRaisesRegex(ZoteroBoundedError, "attachment-head-budget"):
            reader.first_complete_pdf([parents[0]])
        self.assertEqual(len(spy.calls), 1)  # child GET only; no HEAD

    def test_deterministic_first_pdf_and_head_limit(self):
        parents = [item("p2", "2"), item("p1", "1")]
        def fixture(method, url):
            if method == "HEAD":
                return TransportResponse(200, {})
            key = url.split("/items/")[1].split("/")[0]
            return response([item("z" + key, "1", itemType="attachment", parentItem=key,
                                  contentType="application/pdf")])
        spy = SpyTransport(fixture)
        chosen = self.reader(spy).first_complete_pdf(parents)
        self.assertEqual(chosen[0]["data"]["key"], "p1")
        self.assertEqual(chosen[1]["data"]["key"], "zp1")
        self.assertEqual([call[0] for call in spy.calls], ["GET", "GET", "HEAD"])

    def test_pdf_signature_text_and_atomic_cleanup_gates(self):
        good = b"%PDF-1.7\ncontent"
        text = ("word " * 500)
        self.assertEqual(validate_pdf_text(good, lambda _: {"text": text}), text)
        for pdf, parser, error in [
            (b"not-pdf", lambda _: {"text": text}, "invalid-pdf-signature"),
            (good, lambda _: {"text": text, "encrypted": True}, "encrypted-pdf"),
            (good, lambda _: {"text": "short"}, "insufficient-extracted-text"),
        ]:
            with self.subTest(error=error), self.assertRaisesRegex(ZoteroBoundedError, error):
                validate_pdf_text(pdf, parser)
        with tempfile.TemporaryDirectory() as scratch:
            with bounded_scratch_pdf(good, scratch) as path:
                self.assertEqual(path.read_bytes(), good)
                self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)
            self.assertEqual(list(Path(scratch).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
