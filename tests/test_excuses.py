import unittest

from iasid import excuses


class ExcusesTest(unittest.TestCase):
    def test_pool_size(self):
        self.assertGreaterEqual(len(excuses.EXCUSES), 20)

    def test_excuse_of_the_day_stable(self):
        first = excuses.excuse_of_the_day("2026-08-13")
        second = excuses.excuse_of_the_day("2026-08-13")
        self.assertEqual(first, second)

    def test_excuse_of_the_day_changes_by_day(self):
        self.assertNotEqual(excuses.excuse_of_the_day("2026-08-13"),
                            excuses.excuse_of_the_day("2026-08-14"))

    def test_random_excuse_in_pool(self):
        for _ in range(50):
            self.assertIn(excuses.random_excuse(), excuses.EXCUSES)

    def test_context_excuses(self):
        pool = excuses.excuses_for_context("работа", count=3)
        self.assertEqual(len(pool), 3)
        for item in pool:
            self.assertIn(item, excuses.CONTEXT_EXCUSES["работа"])

    def test_unknown_context_falls_back(self):
        pool = excuses.excuses_for_context("такого нет", count=2)
        self.assertEqual(len(pool), 2)


if __name__ == "__main__":
    unittest.main()
