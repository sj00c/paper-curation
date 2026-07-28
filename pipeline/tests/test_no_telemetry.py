"""Regression tests ensuring Audio generation has no usage telemetry side channel."""
import hashlib
import tempfile
import sys
import threading
import types as stdlib_types
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch


PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import generate_audio
from lib.audio_operation import AudioSettings, PaperAudioInputV1, create_audio_plan
from lib.operation_consent import OperationConsent


FORBIDDEN_TELEMETRY_MARKERS = (
    "usage_log",
    "/pc/usage",
    "opentelemetry",
    "pc_usage_endpoint",
)


class NoTelemetryTests(unittest.TestCase):
    def test_production_python_and_audio_generator_contain_no_telemetry_receiver(self):
        production = [
            path for path in PIPELINE.rglob("*.py")
            if "tests" not in path.relative_to(PIPELINE).parts
        ]
        violations = []
        for path in production:
            source = path.read_text(encoding="utf-8").lower()
            for marker in FORBIDDEN_TELEMETRY_MARKERS:
                if marker in source:
                    violations.append(f"{path.relative_to(PIPELINE)}: {marker}")
        self.assertEqual(violations, [])

        audio_source = (PIPELINE / "generate_audio.py").read_text(encoding="utf-8").lower()
        self.assertNotIn("urllib", audio_source)
        self.assertNotIn("requests", audio_source)
        self.assertNotIn("telemetry", audio_source)

    def test_authorized_synthetic_tts_does_not_send_telemetry_or_start_reporter_thread(self):
        prompt = "synthetic prompt"
        source = PaperAudioInputV1("a" * 64, "title", "review", ())
        with tempfile.TemporaryDirectory() as root:
            output = Path(root) / "audio.mp3"
            consent = OperationConsent(clock=lambda: 10)
            plan = create_audio_plan(
                operation_id="telemetry-test",
                topic="topic",
                source=source,
                settings=AudioSettings(600, 1),
                auth="api-key",
                created_at=1,
                expires_at=100,
                script_model=generate_audio.SCRIPT_MODEL,
                tts_model=generate_audio.TTS_MODEL,
                prompt_digest=hashlib.sha256(prompt.encode()).hexdigest(),
                output_path=str(output),
            )
            created = consent.create_plan(plan.claim)
            consent.bind_plan(created.operation_id, created.plan_hash, plan.operation_digest)
            approval = consent.approve(created.operation_id, created.plan_hash)
            generate_audio.require_audio_approval(
                consent=consent,
                approval=approval,
                plan=plan,
                prompt=prompt,
                source_digest=source.source_digest,
                output_root=Path(root),
                output_path=output,
            )

        class FakeModels:
            def generate_content(self, **_kwargs):
                return stdlib_types.SimpleNamespace(
                    candidates=[stdlib_types.SimpleNamespace(
                        content=stdlib_types.SimpleNamespace(
                            parts=[stdlib_types.SimpleNamespace(
                                inline_data=stdlib_types.SimpleNamespace(data=b"pcm"))]))])

        fake_types = stdlib_types.SimpleNamespace(
            GenerateContentConfig=lambda **kwargs: kwargs,
            HttpOptions=lambda **kwargs: kwargs,
        )
        client = stdlib_types.SimpleNamespace(models=FakeModels())
        with (
            patch.object(generate_audio, "types", fake_types, create=True),
            patch.object(urllib.request, "urlopen") as urlopen,
            patch.object(threading, "Thread") as thread,
        ):
            self.assertEqual(generate_audio.tts_call(client, "synthetic", object()), b"pcm")

        self.assertTrue(consent._approvals[approval.token].consumed)
        urlopen.assert_not_called()
        thread.assert_not_called()


if __name__ == "__main__":
    unittest.main()
