"""Parser regression tests for SONORA v6."""
import unittest

from main import (
    animation_profile, parse_lrc, parse_srt, transition_ease,
)


class LyricsParserTests(unittest.TestCase):
    def test_lrc_single_timestamp(self):
        self.assertEqual(parse_lrc("[00:12.50]Hello"), [(12.5, "Hello")])

    def test_lrc_multiple_timestamps(self):
        self.assertEqual(
            parse_lrc("[00:01.00][00:02.50]Repeat"),
            [(1.0, "Repeat"), (2.5, "Repeat")],
        )

    def test_srt_multiline_caption(self):
        source = (
            "1\n00:00:01,250 --> 00:00:03,500\n"
            "First caption line\nSecond caption line\n"
        )
        self.assertEqual(
            parse_srt(source),
            [(1.25, "First caption line Second caption line")],
        )

    def test_srt_dot_milliseconds(self):
        source = "1\n00:00:02.125 --> 00:00:03.000\nA line\n"
        self.assertEqual(parse_srt(source), [(2.125, "A line")])


class OverlayAnimationTests(unittest.TestCase):
    def test_fade_speed_scales_fade_durations_not_hold(self):
        slow = animation_profile(0.5, "Smooth Rise")
        fast = animation_profile(2.0, "Smooth Rise")
        self.assertAlmostEqual(slow[0], 1.7)
        self.assertAlmostEqual(slow[1], 1.45)
        self.assertAlmostEqual(slow[2], 5.0)
        self.assertAlmostEqual(fast[0], 0.425)
        self.assertAlmostEqual(fast[1], 1.45)
        self.assertAlmostEqual(fast[2], 1.25)

    def test_transition_travel_presets(self):
        self.assertEqual(animation_profile(1.0, "Fade Only")[3], 0.0)
        self.assertEqual(animation_profile(1.0, "Gentle Glide")[3], 125.0)
        self.assertEqual(animation_profile(1.0, "Soft Drift")[3], 72.0)

    def test_easing_is_bounded_and_reaches_endpoints(self):
        for preset in ("Smooth Rise", "Gentle Glide", "Soft Drift", "Fade Only"):
            self.assertEqual(transition_ease(0.0, preset), 0.0)
            self.assertAlmostEqual(transition_ease(1.0, preset), 1.0)
            self.assertGreaterEqual(transition_ease(0.5, preset), 0.0)
            self.assertLessEqual(transition_ease(0.5, preset), 1.0)


if __name__ == "__main__":
    unittest.main()
