import unittest

from iasid import cipher


class CaesarTest(unittest.TestCase):
    def test_roundtrip(self):
        self.assertEqual(cipher.caesar(cipher.caesar("Hello, world", 5), -5),
                         "Hello, world")

    def test_preserves_punctuation(self):
        self.assertEqual(cipher.caesar("a!b? 123", 1), "b!c? 123")

    def test_russian_letters(self):
        self.assertEqual(cipher.caesar("абв", 1), "бвг")

    def test_rot13(self):
        self.assertEqual(cipher.rot13("abc"), "nop")

    def test_atbash(self):
        self.assertEqual(cipher.atbash("abc"), "zyx")


class VigenereTest(unittest.TestCase):
    def test_roundtrip(self):
        encrypted = cipher.vigenere("secret message", "key")
        self.assertEqual(cipher.vigenere(encrypted, "key", decrypt=True),
                         "secret message")

    def test_empty_key_raises(self):
        with self.assertRaises(ValueError):
            cipher.vigenere("text", "123")


class AffineTest(unittest.TestCase):
    def test_roundtrip(self):
        encrypted = cipher.affine("hello", 5, 8)
        self.assertEqual(cipher.affine(encrypted, 5, 8, decrypt=True), "hello")

    def test_non_invertible_raises(self):
        with self.assertRaises(ValueError):
            cipher.affine("hello", 4, 1, decrypt=True)


class DrunkCaesarTest(unittest.TestCase):
    def test_stable_with_seed(self):
        self.assertEqual(cipher.drunk_caesar("abc", seed=42),
                         cipher.drunk_caesar("abc", seed=42))


if __name__ == "__main__":
    unittest.main()
