import unittest

from iasid import randomizer, words


class RandomizerTest(unittest.TestCase):
    def test_dice_result(self):
        result = randomizer.roll_dice(2, 6, seed=1)
        self.assertEqual(len(result["rolls"]), 2)
        self.assertEqual(result["total"], sum(result["rolls"]))
        self.assertTrue(all(1 <= side <= 6 for side in result["rolls"]))

    def test_deterministic_with_seed(self):
        self.assertEqual(randomizer.roll_dice(3, 6, seed=7),
                         randomizer.roll_dice(3, 6, seed=7))

    def test_password_length(self):
        self.assertEqual(len(randomizer.random_password(24, seed=5)), 24)

    def test_weighted_pick_returns_item(self):
        picked = randomizer.weighted_pick(["a", "b", "c"], [1, 1, 1], seed=3)
        self.assertIn(picked, ["a", "b", "c"])

    def test_uuid_version(self):
        self.assertEqual(randomizer.random_uuid(seed=1).version, 4)

    def test_coins_values(self):
        self.assertTrue(set(randomizer.flip_coins(10)) <= {"орёл", "решка"})


class WordsTest(unittest.TestCase):
    def test_gibberish_is_capitalized(self):
        sentence = words.gibberish_sentence(seed=11)
        self.assertTrue(sentence[0].isupper())

    def test_gibberish_deterministic(self):
        self.assertEqual(words.gibberish_sentence(seed=11),
                         words.gibberish_sentence(seed=11))

    def test_shuffle_keeps_words(self):
        original = "одно два три четыре"
        shuffled = words.shuffle_words(original, seed=1)
        self.assertEqual(sorted(shuffled.split()), sorted(original.split()))

    def test_pig_latin(self):
        self.assertEqual(words.pig_latin("hello"), "ellohay")
        self.assertEqual(words.pig_latin("apple"), "appleway")

    def test_markov_sentence(self):
        self.assertTrue(words.markov_sentence(seed=2).endswith((".", "!", "...")))


if __name__ == "__main__":
    unittest.main()
