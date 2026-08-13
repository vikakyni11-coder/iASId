"""Слова и бессмыслица: генератор чепухи, марковские цепи, пиг-латынь.

Модуль генерирует осмысленно выглядящий текст, который не значит ничего.
Идеально для тех, кто хочет занять место в отчёте.
"""

import random

NOUNS = [
    "дедлайн", "коммит", "рефакторинг", "спринт", "алгоритм", "сервер",
    "бэклог", "инцидент", "миграция", "релиз", "дашборд", "очередь",
    "задача", "флаг", "заглушка", "кеш", "таймаут", "конфиг", "пиво",
    "чат", "бот", "скрипт", "лог", "парсер", "монитор", "прокси",
]

ADJECTIVES = [
    "срочный", "мудрый", "недо-документированный", "двухслойный",
    "критический", "ленивый", "производственный", "виртуальный",
    "рекурсивный", "параллельный", "импровизированный", "бэкапный",
    "распределённый", "монолитный", "быстрый", "трогательный",
]

VERBS = [
    "сломается", "деплоится", "зависнет", "коммитится", "собирается",
    "падает", "ретраится", "кешируется", "утекает", "перезапускается",
    "валидируется", "моргает", "поддерживает", "прогревает",
]

ADVERBS = [
    "настойчиво", "предсказуемо", "внезапно", "демонстративно",
    "производственно", "безопасно", "параллельно", "лениво",
    "рекурсивно", "безнадёжно", "оптимистично", "тихо",
]

CORPUS = (
    "сегодня я сделаю всё что задумал но только после того как выпью чай "
    "завтра будет новый день и новый список отмазок главное не забыть "
    "прогресс требует жертв поэтому сначала жертвуем часом сна "
    "никаких дедлайнов не существует есть только напоминания о них "
    "проект растёт сам главное вовремя закоммитить а то вырастет не туда "
    "вдохновение приходит не по расписанию и уходит без предупреждения "
)


def gibberish_sentence(seed=None, words=8):
    """Генерирует бессмысленное, но красиво звучащее предложение."""
    rng = random.Random(seed)
    parts = []
    for _ in range(words):
        pattern = rng.choice(["adj-noun", "noun-verb", "adv-adj-noun"])
        if pattern == "adj-noun":
            parts.append(f"{rng.choice(ADJECTIVES)} {rng.choice(NOUNS)}")
        elif pattern == "noun-verb":
            parts.append(f"{rng.choice(NOUNS)} {rng.choice(VERBS)}")
        else:
            parts.append(
                f"{rng.choice(ADVERBS)} {rng.choice(ADJECTIVES)} "
                f"{rng.choice(NOUNS)}"
            )
    return " ".join(parts).capitalize() + rng.choice([".", "...", "!", "?"])


def shuffle_words(text, seed=None):
    """Перемешивает слова в строке."""
    rng = random.Random(seed)
    words = text.split()
    rng.shuffle(words)
    return " ".join(words)


VOWELS = "aeiouy"


def pig_latin(text):
    """Переводит английские слова на пиг-латынь (поросячий латинский)."""
    result = []
    for raw in text.split():
        word = raw.lower()
        if not word.isalpha():
            result.append(raw)
            continue
        if word[0] in VOWELS:
            result.append(word + "way")
            continue
        for index, char in enumerate(word):
            if char in VOWELS:
                result.append(word[index:] + word[:index] + "ay")
                break
    return " ".join(result)


def markov_sentence(seed=None):
    """Генерирует предложение цепью Маркова второго порядка по корпусу."""
    rng = random.Random(seed)
    tokens = CORPUS.split()
    links = {}
    for index in range(len(tokens) - 1):
        links.setdefault(tokens[index], []).append(tokens[index + 1])
    current = rng.choice(tokens)
    output = [current]
    for _ in range(rng.randint(8, 14)):
        output.append(rng.choice(links.get(output[-1], tokens)))
    sentence = " ".join(output).capitalize()
    return sentence + rng.choice([".", "!", "..."])
