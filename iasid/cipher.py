"""Шифры: Цезарь, пьяный Цезарь, rot13, atbash, Виженер, аффинный.

Все шифры работают и с латиницей, и с кириллицей; символы вне алфавита
(пробелы, пунктуация, цифры) сохраняются на месте.
"""

import random
import string

ALPHABET_EN = string.ascii_lowercase
ALPHABET_RU = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def _alphabet_for(char):
    """Подбирает алфавит для символа: кириллический или латинский."""
    lowered = char.lower()
    if lowered == "ё" or "а" <= lowered <= "я":
        return ALPHABET_RU
    return ALPHABET_EN


def _shift_char(char, shift):
    alphabet = _alphabet_for(char)
    idx = alphabet.index(char.lower())
    new_char = alphabet[(idx + shift) % len(alphabet)]
    return new_char.upper() if char.isupper() else new_char


def caesar(text, shift):
    """Шифр Цезаря: каждая буква сдвигается на shift позиций."""
    return "".join(
        _shift_char(char, shift) if char.isalpha() else char
        for char in text
    )


def drunk_caesar(text, seed=None):
    """Пьяный Цезарь: каждая буква сдвигается на случайный сдвиг.

    При указании seed результат воспроизводим.
    """
    rng = random.Random(seed)
    return "".join(
        _shift_char(char, rng.randint(-3, 3)) if char.isalpha() else char
        for char in text
    )


def rot13(text):
    """rot13 — частный случай Цезаря со сдвигом 13."""
    return caesar(text, 13)


def atbash(text):
    """Атбаш: буква заменяется на симметричную в алфавите (а -> я/z)."""
    result = []
    for char in text:
        if not char.isalpha():
            result.append(char)
            continue
        alphabet = _alphabet_for(char)
        new_char = alphabet[-1 - alphabet.index(char.lower())]
        result.append(new_char.upper() if char.isupper() else new_char)
    return "".join(result)


def vigenere(text, key, decrypt=False):
    """Шифр Виженера. Ключ может содержать только буквы."""
    key = "".join(ch for ch in key.lower() if ch.isalpha())
    if not key:
        raise ValueError("ключ должен содержать хотя бы одну букву")
    result = []
    key_index = 0
    for char in text:
        if not char.isalpha():
            result.append(char)
            continue
        key_shift = ALPHABET_EN.index(key[key_index % len(key)])
        if decrypt:
            key_shift = -key_shift
        result.append(_shift_char(char, key_shift))
        key_index += 1
    return "".join(result)


def _mod_inverse(a, m):
    """Обратное число к a по модулю m или None, если его нет."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def affine(text, a, b, decrypt=False):
    """Аффинный шифр: (a * x + b) mod m, где m — длина алфавита.

    Для расшифровки требуется обратимость a по модулю m.
    """
    result = []
    for char in text:
        if not char.isalpha():
            result.append(char)
            continue
        alphabet = _alphabet_for(char)
        modulus = len(alphabet)
        idx = alphabet.index(char.lower())
        if decrypt:
            inverse = _mod_inverse(a % modulus, modulus)
            if inverse is None:
                raise ValueError(
                    f"множитель {a} необратим по модулю {modulus}, "
                    "используйте нечётное a"
                )
            new_idx = (inverse * (idx - b)) % modulus
        else:
            new_idx = (a * idx + b) % modulus
        new_char = alphabet[new_idx]
        result.append(new_char.upper() if char.isupper() else new_char)
    return "".join(result)
