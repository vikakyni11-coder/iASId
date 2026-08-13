"""Случайности: кубики, монетки, пароли, взвешенные выборы, uuid.

Все функции принимают опциональный seed — при одинаковом seed результат
всегда одинаковый, что очень удобно для тестов.
"""

import random
import string
import uuid

DICE_SIDES = [4, 6, 8, 10, 12, 20]
SYMBOLS = ["*", "$", "#", "@", "%", "&", "~", "^", "!", "?"]


def roll_dice(count=2, sides=6, seed=None):
    """Бросает count кубиков с sides гранями."""
    rng = random.Random(seed)
    rolls = [rng.randint(1, sides) for _ in range(count)]
    return {"rolls": rolls, "total": sum(rolls), "sides": sides}


def flip_coins(count=1, seed=None):
    """Подбрасывает монетки: 'орёл' или 'решка'."""
    rng = random.Random(seed)
    return [rng.choice(["орёл", "решка"]) for _ in range(count)]


def weighted_pick(items, weights, seed=None):
    """Случайный выбор с весами. Сумма весов не обязательно 1."""
    rng = random.Random(seed)
    total = sum(weights)
    if total <= 0:
        return items[-1]
    pick = rng.uniform(0.0, total)
    upto = 0.0
    for item, weight in zip(items, weights):
        upto += weight
        if pick <= upto:
            return item
    return items[-1]


def random_password(length=16, use_symbols=True, seed=None):
    """Генерирует пароль заданной длины."""
    rng = random.Random(seed)
    pool = string.ascii_letters + string.digits
    if use_symbols:
        pool += string.punctuation
    return "".join(rng.choice(pool) for _ in range(length))


def random_uuid(seed=None):
    """UUID версии 4, но с сидом (строго говоря, это уже не случайность)."""
    return uuid.UUID(int=random.Random(seed).getrandbits(128), version=4)


def random_face(seed=None):
    """Случайное ascii-выражение лица."""
    faces = [
        "( ͡° ͜ʖ ͡°)",
        "¯\\_(ツ)_/¯",
        "(>_<)",
        "o_O",
        ":-D",
        "(¬_¬)",
        "└[°﹃°]┘",
        "(づ｡◕‿‿◕｡)づ",
    ]
    return random.Random(seed).choice(faces)


def random_number(low=1, high=100, seed=None):
    """Случайное целое число в диапазоне [low, high]."""
    return random.Random(seed).randint(low, high)
