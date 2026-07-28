import hashlib
import re
import sys
import unittest
from pathlib import Path

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import generate_audio  # noqa: E402  (producer under test; see D1 gap tests)
from pipeline.lib.audio_operation import (
    AUDIO_BUDGET_SECONDS, AudioOperationError, AudioSettings, FRAMING_RESERVE,
    FourOrdinalWindow, GAP_SECONDS, MAX_CHUNK_BYTES, MAX_CHUNK_SECONDS,
    MAX_CHUNKS, MAX_TARGET_SECONDS, PCM_BYTES_PER_SAMPLE, PCM_SAMPLE_RATE,
    PcmChunk, PaperAudioInputV1, SILENCE_SAMPLES, admit_chunk,
    create_answer_input, create_audio_plan, retain_answer_source,
    validate_audio_output,
)


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


class AudioOperationTests(unittest.TestCase):
    def test_paper_plan_binds_ordered_context_and_gemini_tasks(self):
        paper = PaperAudioInputV1(digest("asset"), "title", "review", ("first", "second"))
        settings = AudioSettings(30, 1)
        plan = create_audio_plan(
            operation_id="op", topic="topic", source=paper, settings=settings, auth="oauth",
            created_at=1, expires_at=100, script_model="gemini-script", tts_model="gemini-tts",
        )
        self.assertEqual(plan.claim.input_digests, (paper.source_digest,))
        self.assertEqual([task.provider for task in plan.claim.providers], ["gemini", "gemini"])
        self.assertEqual([task.fallbacks for task in plan.claim.providers], [(), ()])
        self.assertEqual(plan.dag[0], "A01.script")
        self.assertEqual(plan.dag[-1], "A03.assemble")

    def test_answer_transfer_is_bound_copied_and_same_capability_only(self):
        answer = create_answer_input(
            capability="cap", operation_id="normal-op", result_digest=digest("result"),
            query="why?", final_digest=digest("final"), final_payload=b"answer", expires_at=100,
        )
        copied = retain_answer_source(answer, capability="cap", now=99)
        self.assertEqual(copied.reconstruct_text(), "[질문] why?\n\n[답변] answer")
        with self.assertRaises(AudioOperationError):
            retain_answer_source(answer, capability="other", now=99)
        with self.assertRaises(AudioOperationError):
            retain_answer_source(answer, capability="cap", now=100)

    def test_settings_cover_speakers_and_target_boundaries(self):
        for speakers in (1, 2, 3):
            for target in (30, 3599, 3600):
                self.assertEqual(AudioSettings(target, speakers).requested_target_seconds, target)
        for target in (29, 3601):
            with self.assertRaises(AudioOperationError):
                AudioSettings(target, 1)

    def test_output_chunk_limits_and_actual_not_billed(self):
        pcm = b"\0\0" * (24_000 * 120)
        output = validate_audio_output([PcmChunk(1, pcm)], b"mp3", playable_seconds=3600, provider_billed_units=999)
        self.assertEqual(output.actual_pcm_samples, 24_000 * 120)
        self.assertEqual(output.provider_billed_units, 999)
        self.assertEqual(output.timeline_seconds, 120)
        for count in (1, 4, 29, 30, 31, 32):
            chunks = [PcmChunk(n, b"\0\0") for n in range(1, count + 1)]
            self.assertGreaterEqual(validate_audio_output(chunks, b"mp3", playable_seconds=0).timeline_seconds, 0)
        with self.assertRaises(AudioOperationError):
            validate_audio_output([PcmChunk(1, b"\0" * (24_000 * 120 * 2 + 1))], b"mp3", playable_seconds=0)
        with self.assertRaises(AudioOperationError):
            validate_audio_output([PcmChunk(1, b"\0" * (MAX_CHUNK_BYTES + 1))], b"mp3", playable_seconds=0)
        with self.assertRaises(AudioOperationError):
            validate_audio_output([PcmChunk(1, b"\0\0")] * 33, b"mp3", playable_seconds=0)
        with self.assertRaises(AudioOperationError):
            validate_audio_output([PcmChunk(1, b"\0\0")], b"mp3", playable_seconds=MAX_TARGET_SECONDS + 1)

    def test_window_is_exactly_four_and_acknowledgements_are_ordered(self):
        window = FourOrdinalWindow(32)
        for ordinal in range(1, 5):
            self.assertTrue(window.may_launch(ordinal))
            window.verify(ordinal)
        self.assertFalse(window.may_launch(5))
        with self.assertRaises(AudioOperationError):
            window.acknowledge(2)
        window.acknowledge(1)
        self.assertTrue(window.may_launch(5))

    def test_gaps_are_exactly_250ms(self):
        usage = validate_audio_output([PcmChunk(1, b"\0\0" * 24_000), PcmChunk(2, b"\0\0" * 24_000)], b"mp3", playable_seconds=2.25)
        self.assertEqual(usage.actual_pcm_seconds, 2)
        self.assertEqual(usage.timeline_seconds, 2.25)

    def test_python_and_codec_inter_chunk_gap_are_identical(self):
        """D1: one gap authority across the fd3 boundary.

        Before this retrofit `generate_audio.SILENCE_MS = 200` produced 4,800
        samples while accounting and the codec both used 6,000, drifting the
        realized timeline by 50 ms per gap (up to 1.55 s over 31 gaps).
        """
        self.assertEqual(SILENCE_SAMPLES, 6_000)
        self.assertEqual(SILENCE_SAMPLES, round(GAP_SECONDS * PCM_SAMPLE_RATE))
        self.assertAlmostEqual(SILENCE_SAMPLES / PCM_SAMPLE_RATE, 0.250, places=9)

        # The producer's own bound value, not just the accounting module's.
        self.assertEqual(generate_audio.SILENCE_SAMPLES, SILENCE_SAMPLES)
        self.assertEqual(generate_audio.SAMPLE_RATE, PCM_SAMPLE_RATE)

        codec = (Path(__file__).resolve().parents[2]
                 / "bin" / "audio-encode-lamejs.mjs").read_text(encoding="utf-8")
        # findall, not search: a second (shadowing) declaration must fail loudly
        # instead of being masked by whichever one happens to come first.
        declared = re.findall(r"\bSILENCE_SAMPLES\s*=\s*([0-9][0-9_]*)\s*;", codec)
        self.assertEqual(len(declared), 1,
                         f"codec must declare SILENCE_SAMPLES exactly once, found {declared}")
        self.assertEqual(int(declared[0].replace("_", "")), SILENCE_SAMPLES)

        # generate_audio must not reintroduce a second, divergent gap constant.
        generator = (Path(__file__).resolve().parents[1]
                     / "generate_audio.py").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"^\s*SILENCE_MS\s*=", generator, re.M),
                          "SILENCE_MS must not be reintroduced")

    def test_concat_pcm_builds_the_shared_250ms_gap(self):
        """D1: the realized Python-side join uses the single authority."""
        parts = [b"\0\0" * 24_000, b"\0\0" * 24_000, b"\0\0" * 24_000]
        joined = generate_audio.concat_pcm(parts)
        expected_gap_bytes = SILENCE_SAMPLES * PCM_BYTES_PER_SAMPLE
        self.assertEqual(len(joined), sum(map(len, parts)) + 2 * expected_gap_bytes)
        self.assertEqual(joined[len(parts[0]):len(parts[0]) + expected_gap_bytes],
                         b"\x00" * expected_gap_bytes)
        self.assertEqual(len(generate_audio.concat_pcm([parts[0]])), len(parts[0]))
        self.assertEqual(generate_audio.concat_pcm([]), b"")

        # 32 chunks / 31 gaps is the plan's stated worst case: exactly 7.75 s.
        many = [b"\0\0" * 10] * 32
        self.assertEqual(
            len(generate_audio.concat_pcm(many)) - sum(map(len, many)),
            31 * expected_gap_bytes,
        )

    def test_empty_and_nonfinite_outputs_and_aggregate_timeline_fail(self):
        for playable in (float("nan"), float("inf")):
            with self.subTest(playable=playable), self.assertRaises(AudioOperationError):
                validate_audio_output(
                    [PcmChunk(1, b"\0\0")],
                    b"mp3",
                    playable_seconds=playable,
                )
        with self.assertRaises(AudioOperationError):
            validate_audio_output(
                [PcmChunk(1, b"")],
                b"mp3",
                playable_seconds=0,
            )
        with self.assertRaises(AudioOperationError):
            validate_audio_output(
                [PcmChunk(1, b"\0\0")],
                b"",
                playable_seconds=0,
            )
        full_chunks = [
            PcmChunk(ordinal, b"\0\0" * (24_000 * 120))
            for ordinal in range(1, 32)
        ]
        with self.assertRaisesRegex(AudioOperationError, "timeline"):
            validate_audio_output(
                full_chunks,
                b"mp3",
                playable_seconds=MAX_TARGET_SECONDS,
            )

    # ---- D3: pre-dispatch admission control -----------------------------
    def test_budget_reserve_and_hard_ceiling_are_three_distinct_values(self):
        """D3: the scheduling budget sits strictly below the unchanged ceiling."""
        self.assertEqual(MAX_TARGET_SECONDS, 3600)
        self.assertEqual(FRAMING_RESERVE, 0.100)
        self.assertEqual(AUDIO_BUDGET_SECONDS, 3599.900)
        self.assertEqual(len({MAX_TARGET_SECONDS, FRAMING_RESERVE, AUDIO_BUDGET_SECONDS}), 3)
        self.assertLess(AUDIO_BUDGET_SECONDS, MAX_TARGET_SECONDS)
        self.assertAlmostEqual(MAX_TARGET_SECONDS - AUDIO_BUDGET_SECONDS, FRAMING_RESERVE, places=9)
        # The reserve covers the measured lamejs@1.2.1 worst case (1,727 samples).
        self.assertGreater(FRAMING_RESERVE, 1_727 / PCM_SAMPLE_RATE)
        self.assertAlmostEqual(FRAMING_RESERVE - 1_727 / PCM_SAMPLE_RATE, 0.028042, places=6)

    def test_hard_ceiling_is_unchanged_by_the_scheduling_budget(self):
        """D3: 3599.900 is a budget, never a demotion of the 3600-second gate."""
        usage = validate_audio_output(
            [PcmChunk(1, b"\0\0" * (24_000 * 120))], b"mp3", playable_seconds=3600,
        )
        self.assertEqual(usage.timeline_seconds, 120)
        # Durations above the budget but within the ceiling are still valid output.
        for playable in (AUDIO_BUDGET_SECONDS + 0.001, 3599.999, float(MAX_TARGET_SECONDS)):
            with self.subTest(playable=playable):
                self.assertEqual(
                    validate_audio_output(
                        [PcmChunk(1, b"\0\0")], b"mp3", playable_seconds=playable,
                    ).actual_pcm_samples,
                    1,
                )
        with self.assertRaises(AudioOperationError):
            validate_audio_output(
                [PcmChunk(1, b"\0\0")], b"mp3", playable_seconds=MAX_TARGET_SECONDS + 1,
            )

    def test_admit_chunk_admits_at_the_budget_and_refuses_one_sample_past(self):
        """D3: the predicate is exact at the boundary, in both directions."""
        exact = round(AUDIO_BUDGET_SECONDS * PCM_SAMPLE_RATE)  # 86,397,600 samples
        self.assertEqual(exact, 86_397_600)
        self.assertTrue(admit_chunk(exact, 1, 0.0))
        self.assertFalse(admit_chunk(exact + 1, 1, 0.0))

        # A full 120-second next chunk consumes the same budget.
        with_next = round((AUDIO_BUDGET_SECONDS - MAX_CHUNK_SECONDS) * PCM_SAMPLE_RATE)
        self.assertTrue(admit_chunk(with_next, 1, MAX_CHUNK_SECONDS))
        self.assertFalse(admit_chunk(with_next + 1, 1, MAX_CHUNK_SECONDS))

        # Mid-sequence the accumulated gaps are charged too (ordinal 5 => 4 gaps).
        gapped = round(
            (AUDIO_BUDGET_SECONDS - MAX_CHUNK_SECONDS - GAP_SECONDS * 4) * PCM_SAMPLE_RATE
        )
        self.assertTrue(admit_chunk(gapped, 5, MAX_CHUNK_SECONDS))
        self.assertFalse(admit_chunk(gapped + 1, 5, MAX_CHUNK_SECONDS))
        # The refusal above is caused by the accrued gaps, not by the PCM alone:
        # the same sample count with the same 120 s chunk still fits at ordinal 1.
        self.assertTrue(admit_chunk(gapped + 1, 1, MAX_CHUNK_SECONDS))

    def test_admit_chunk_refuses_the_32x120_second_schedule_before_spending(self):
        """D3: the plan's worst case stops early instead of being fully scheduled."""
        chunk_samples = MAX_CHUNK_SECONDS * PCM_SAMPLE_RATE
        worst_case = MAX_CHUNKS * MAX_CHUNK_SECONDS + GAP_SECONDS * (MAX_CHUNKS - 1)
        self.assertEqual(worst_case, 3847.75)
        self.assertGreater(worst_case, AUDIO_BUDGET_SECONDS)

        admitted = 0
        first_refused = None
        for ordinal in range(1, MAX_CHUNKS + 1):
            if not admit_chunk(admitted * chunk_samples, ordinal, MAX_CHUNK_SECONDS):
                first_refused = ordinal
                break
            admitted += 1
        self.assertEqual(first_refused, 30)
        self.assertEqual(admitted, 29)
        self.assertLess(admitted, MAX_CHUNKS)
        # Everything actually scheduled still fits under the budget and the ceiling.
        scheduled = admitted * MAX_CHUNK_SECONDS + GAP_SECONDS * (admitted - 1)
        self.assertEqual(scheduled, 3487.0)
        self.assertLessEqual(scheduled, AUDIO_BUDGET_SECONDS)
        # And refusal happens before the last chunks pay for TTS.
        self.assertFalse(admit_chunk(admitted * chunk_samples, MAX_CHUNKS, MAX_CHUNK_SECONDS))

    def test_admit_chunk_raises_on_invalid_input_instead_of_returning_false(self):
        """D3: malformed input must never be readable as 'the budget is full'."""
        for prev in (-1, 1.5, True, False, "0", None, MAX_CHUNKS * MAX_CHUNK_SECONDS * PCM_SAMPLE_RATE + 1):
            with self.subTest(prev_samples=prev), self.assertRaises(AudioOperationError):
                admit_chunk(prev, 1, 0.0)
        for ordinal in (0, -1, MAX_CHUNKS + 1, 1.0, True, None):
            with self.subTest(ordinal=ordinal), self.assertRaises(AudioOperationError):
                admit_chunk(0, ordinal, 0.0)
        for nxt in (-0.001, float("nan"), float("inf"), float("-inf"), True,
                    MAX_CHUNK_SECONDS + 0.001, "120", None):
            with self.subTest(max_next_seconds=nxt), self.assertRaises(AudioOperationError):
                admit_chunk(0, 1, nxt)

    def test_generate_audio_admission_uses_the_budget_not_the_ceiling(self):
        """D3: the producer's pre-dispatch gate rejects observably, above budget."""
        self.assertEqual(generate_audio.validate_playable_duration(AUDIO_BUDGET_SECONDS),
                         AUDIO_BUDGET_SECONDS)
        for rejected in (AUDIO_BUDGET_SECONDS + 0.000001, 3599.999, MAX_TARGET_SECONDS,
                         float("nan"), -0.001):
            with self.subTest(seconds=rejected), self.assertRaisesRegex(
                    generate_audio.AudioApprovalError, "AUDIO_PLAYABLE_DURATION_EXCEEDED"):
                generate_audio.validate_playable_duration(rejected)
        # The hard maximum the approval claim is bound to is still 3600.
        self.assertEqual(generate_audio.MAX_PLAYABLE_SECONDS, MAX_TARGET_SECONDS)


if __name__ == "__main__":
    unittest.main()
