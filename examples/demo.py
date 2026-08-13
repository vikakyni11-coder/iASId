"""Демонстрация возможностей пакета iASId одной командой."""

from iasid import __version__
from iasid.ascii import banner
from iasid.astrology import compatibility, horoscope
from iasid.cipher import caesar, drunk_caesar
from iasid.excuses import excuse_of_the_day
from iasid.motivation import quote_of_the_day
from iasid.randomizer import roll_dice
from iasid.words import gibberish_sentence, markov_sentence


def main():
    print(banner(f"iASId v{__version__}"))
    print("Отмазка дня:", excuse_of_the_day())
    print("Шифр Цезаря:", caesar("привет мир", 3))
    print("Пьяный Цезарь:", drunk_caesar("я всё сломал", seed=42))
    print("Бессмыслица:", gibberish_sentence(seed=11))
    print("Марков:", markov_sentence(seed=3))
    print("Кубики:", roll_dice(2, 20, seed=1))
    print("Гороскоп:", horoscope("овен"))
    print("Совместимость:", compatibility("овен", "телец"))
    print("Цитата:", quote_of_the_day())


if __name__ == "__main__":
    main()
