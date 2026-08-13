"""Вспомогательные функции общего назначения."""

import functools
import random
from datetime import date


def seeded_rng(seed=None):
    """Создаёт генератор случайных чисел с опциональным сидом."""
    return random.Random(seed)


def day_seed():
    """Числовой сид, одинаковый в течение всего дня."""
    return date.today().toordinal()


def clamp(value, low, high):
    """Ограничивает значение диапазоном [low, high]."""
    return max(low, min(high, value))


def pluralize(count, one, few, many):
    """Русская плюрализация: pluralize(3, 'файл', 'файла', 'файлов')."""
    n = abs(count) % 100
    n1 = n % 10
    if 10 < n < 20:
        return many
    if 1 < n1 < 5:
        return few
    if n1 == 1:
        return one
    return many


def memoize(func):
    """Декоратор кеширования результатов по позиционным аргументам."""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


def ensure_list(value):
    """Гарантирует, что результат — список (или кортеж)."""
    return value if isinstance(value, (list, tuple)) else [value]


def format_seconds(seconds):
    """Преобразует секунды в строку вида '1ч 05м 12с'."""
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    parts = []
    if hours:
        parts.append(f"{hours}ч")
    if hours or minutes:
        parts.append(f"{minutes:02d}м")
    parts.append(f"{secs:02d}с")
    return " ".join(parts)
