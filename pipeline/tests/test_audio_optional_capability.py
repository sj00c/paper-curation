"""Offline contract tests for the optional, server-routed Audio capability."""
import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import generate_audio
from lib import audio_overview
from lib.audio_operation import (
    AudioOperationError,
    AudioSettings,
    PaperAudioInputV1,
    create_audio_plan,
    validate_output_path,
)
from lib.operation_consent import OperationConsent

class AudioOptionalCapabilityTests(unittest.TestCase):
    def test_missing_auth_is_informational_and_ui_is_disabled_without_provider_work(self):
        capability = audio_overview.derive_audio_capability(
            auth="", models={"script": audio_overview.SCRIPT_MODEL, "tts": audio_overview.TTS_MODEL}
        )
        self.assertEqual(capability.state, "UNAVAILABLE")
        self.assertEqual(capability.reason, "GEMINI_AUTH_UNAVAILABLE")
        status = audio_overview.audio_plan_status(capability)
        self.assertEqual(status["result"], "FEATURE_UNAVAILABLE")
        self.assertEqual(status["capability"]["state"], "UNAVAILABLE")
        self.assertEqual(status["capability"]["reason"], "GEMINI_AUTH_UNAVAILABLE")
        self.assertNotIn("mutated", status)
        html = audio_overview.audio_script_block(capability=capability)
        self.assertIn('button.disabled = !ready', html)
        self.assertNotIn("generativelanguage.googleapis.com", html)
        self.assertNotIn("_GEMINI_KEY", html)
        self.assertNotIn("localStorage", html)

    def test_plan_status_carries_the_result_discriminator_on_both_variants(self):
        """A6: clients switch on `result`, never on the absence of a key."""
        unavailable = audio_overview.derive_audio_capability(auth="", models={})
        available = audio_overview.derive_audio_capability(
            auth="configured",
            models={"script": audio_overview.SCRIPT_MODEL, "tts": audio_overview.TTS_MODEL},
        )
        self.assertEqual(available.state, "AVAILABLE")

        for capability, expected in ((unavailable, "FEATURE_UNAVAILABLE"), (available, "PLANNED")):
            with self.subTest(result=expected):
                status = audio_overview.audio_plan_status(capability)
                # `result` is required on BOTH variants, not just the unavailable one.
                self.assertIn("result", status)
                self.assertEqual(status["result"], expected)
                self.assertEqual(status["schema"], 1)
                self.assertEqual(set(status), {"schema", "result", "capability"})
                self.assertEqual(status["capability"], capability.to_dict())
                # The capability record itself never carries credential material.
                self.assertNotIn("auth", status["capability"])
                self.assertNotIn("key", json.dumps(status).lower().replace("api_key_absent", ""))

    def test_server_capability_and_route_use_the_library_contract(self):
        """A6: the live audio.create route must actually emit the discriminator.

        The contract was previously defined in the library while
        `serve_local.audio_capability()` hand-built its own dict, so the server
        could never report GEMINI_MODEL_UNAVAILABLE or
        AUDIO_TEMP_RECOVERY_AMBIGUOUS and shipped a stray `models` key.
        """
        import serve_local

        with patch.object(serve_local, "resolve_google_key", return_value=None):
            record = serve_local._audio_capability_record()
            self.assertEqual(record.state, "UNAVAILABLE")
            self.assertEqual(record.reason, "GEMINI_AUTH_UNAVAILABLE")
            self.assertEqual(
                audio_overview.audio_plan_status(record)["result"], "FEATURE_UNAVAILABLE"
            )

        with patch.object(serve_local, "resolve_google_key", return_value="configured"):
            record = serve_local._audio_capability_record()
            self.assertEqual(record.state, "AVAILABLE")
            self.assertEqual(audio_overview.audio_plan_status(record)["result"], "PLANNED")
            # The server dict is exactly the library record: no stray keys.
            self.assertEqual(
                set(serve_local.audio_capability()),
                set(audio_overview.AudioCapabilityV1().to_dict()),
            )
            self.assertNotIn("models", serve_local.audio_capability())

    def test_browser_audio_js_emits_the_same_discriminated_pair(self):
        """A6: the browser half must not drift back to the retired shape.

        `AUDIO_JS` ships to the generated pages, so a regression there is
        invisible to the Python contract tests unless the source is asserted.
        """
        js = audio_overview.AUDIO_JS
        self.assertIn('result:"FEATURE_UNAVAILABLE"', js)
        self.assertIn('result:"PLANNED"', js)
        self.assertIn("capability:c", js)
        # The retired untagged shape must be gone from the browser half too.
        self.assertNotIn("mutated", js)
        self.assertIsNone(re.search(r"state\s*:\s*c\.state", js))
        # Both return paths carry the discriminator, so a client never has to
        # infer intent from a missing key.
        returns = re.findall(r"return\s*\{schema:1[^}]*\}", js)
        self.assertEqual(len(returns), 2, f"expected both variants, found {returns}")
        for emitted in returns:
            self.assertIn("result:", emitted)

    def test_missing_model_and_unsafe_root_are_local_unavailable_states(self):
        self.assertEqual(
            audio_overview.derive_audio_capability(auth="configured", models={}).reason,
            "GEMINI_MODEL_UNAVAILABLE",
        )
        self.assertEqual(
            audio_overview.derive_audio_capability(
                auth="configured",
                models={"script": audio_overview.SCRIPT_MODEL, "tts": audio_overview.TTS_MODEL},
                safe_root=False,
            ).reason,
            "AUDIO_TEMP_RECOVERY_AMBIGUOUS",
        )

    def test_available_capability_is_local_and_gemini_only(self):
        capability = audio_overview.derive_audio_capability(
            auth="configured",
            models={"script": audio_overview.SCRIPT_MODEL, "tts": audio_overview.TTS_MODEL},
        )
        self.assertEqual(capability.to_dict(), {
            "schema": "AudioCapabilityV1", "feature": "audio_overview", "provider": "gemini",
            "state": "AVAILABLE", "reason": "READY", "model": audio_overview.SCRIPT_MODEL,
        })

    def test_approval_is_opaque_and_binds_prompt_models_duration_and_output(self):
        source = PaperAudioInputV1("a" * 64, "title", "review", ())
        prompt = "exact prompt"
        with tempfile.TemporaryDirectory() as root:
            output = Path(root) / "audio.mp3"
            consent = OperationConsent(clock=lambda: 10)
            plan = create_audio_plan(
                operation_id="audio-test", topic="topic", source=source,
                settings=AudioSettings(600, 2), auth="api-key", created_at=1, expires_at=100,
                script_model=generate_audio.SCRIPT_MODEL, tts_model=generate_audio.TTS_MODEL,
                prompt_digest=hashlib.sha256(prompt.encode()).hexdigest(), output_path=str(output),
            )
            created = consent.create_plan(plan.claim)
            consent.bind_plan(created.operation_id, created.plan_hash, plan.operation_digest)
            approval = consent.approve(created.operation_id, created.plan_hash)
            with patch.object(generate_audio, "_load_google") as sdk:
                generate_audio.require_audio_approval(
                    consent=consent, approval=approval, plan=plan, prompt=prompt,
                    source_digest=source.source_digest, output_root=Path(root), output_path=output,
                )
                with self.assertRaisesRegex(generate_audio.AudioApprovalError, "REJECTED"):
                    generate_audio.require_audio_approval(
                        consent=consent, approval=approval, plan=plan, prompt=prompt,
                        source_digest=source.source_digest, output_root=Path(root), output_path=output,
                    )
                sdk.assert_not_called()
            changed_prompt = "scope changed"
            with self.assertRaisesRegex(generate_audio.AudioApprovalError, "SCOPE_CHANGED"):
                generate_audio.require_audio_approval(
                    consent=consent, approval=approval, plan=plan, prompt=changed_prompt,
                    source_digest=source.source_digest, output_root=Path(root), output_path=output,
                )
    def test_output_path_rejects_escape_symlink_and_overwrite(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as outside:
            root_path = Path(root)
            outside_path = Path(outside)
            with self.assertRaises(AudioOperationError):
                validate_output_path(root_path, outside_path / "audio.mp3")
            link = root_path / "linked"
            link.symlink_to(outside_path, target_is_directory=True)
            with self.assertRaises(AudioOperationError):
                validate_output_path(root_path, link / "audio.mp3")
            existing = root_path / "audio.mp3"
            existing.write_bytes(b"old")
            with self.assertRaises(AudioOperationError):
                validate_output_path(root_path, existing)

    def test_target_is_approximate_but_first_value_over_budget_fails(self):
        for duration in (30, 599.5, 600, 3599.899, 3599.900):
            self.assertEqual(generate_audio.validate_playable_duration(duration), duration)
        with self.assertRaisesRegex(generate_audio.AudioApprovalError, "EXCEEDED"):
            generate_audio.validate_playable_duration(3599.900001)


if __name__ == "__main__":
    unittest.main()
