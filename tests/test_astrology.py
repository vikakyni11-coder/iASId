import unittest

from iasid import astrology


class AstrologyTest(unittest.TestCase):
    def test_signs_count(self):
        self.assertEqual(len(astrology.signs()), 12)

    def test_horoscope_returns_text(self):
        text = astrology.horoscope("овен")
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 10)

    def test_horoscope_accepts_upper_case(self):
        self.assertEqual(astrology.horoscope("ОВЕН"), astrology.horoscope("овен"))

    def test_unknown_sign_raises(self):
        with self.assertRaises(ValueError):
            astrology.horoscope("козерожка")

    def test_compatibility_score_range(self):
        result = astrology.compatibility("овен", "телец")
        self.assertTrue(1 <= result["score"] <= 100)
        self.assertIn("verdict", result)

    def test_fortune_not_empty(self):
        self.assertTrue(astrology.fortune())


if __name__ == "__main__":
    unittest.main()
