"""CLI проекта iASId: парсер аргументов и диспетчер подкоманд.

Импорт функциональных модулей сделан ленивым (внутри обработчиков),
чтобы CLI можно было запускать даже с частично собранным пакетом.
"""

import argparse
import sys

from . import __version__
from .log import get_logger

logger = get_logger()


def build_parser():
    """Собирает дерево подкоманд argparse."""
    parser = argparse.ArgumentParser(
        prog="iasid",
        description="iASId — совершенно бесполезный набор утилит.",
        epilog="Пример: python main.py excuse --today",
    )
    parser.add_argument(
        "--version", action="version", version=f"iasid {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_excuse = sub.add_parser("excuse", help="случайная отмазка")
    p_excuse.add_argument("--context", choices=["работа", "учеба", "спорт"])
    p_excuse.add_argument("--today", action="store_true", help="отмазка дня")
    p_excuse.add_argument("--count", type=int, default=1)

    p_cipher = sub.add_parser("cipher", help="шифрование текста")
    p_cipher.add_argument("text", nargs="+")
    p_cipher.add_argument(
        "--algo",
        choices=["caesar", "drunk", "rot13", "atbash", "vigenere", "affine"],
        default="caesar",
    )
    p_cipher.add_argument("--shift", type=int, default=3)
    p_cipher.add_argument("--key", help="ключ для Виженера")
    p_cipher.add_argument("--a", type=int, default=5, help="множитель (affine)")
    p_cipher.add_argument("--b", type=int, default=8, help="сдвиг (affine)")
    p_cipher.add_argument("--decrypt", action="store_true")

    p_rand = sub.add_parser("random", help="случайности")
    p_rand.add_argument("--dice", type=int, nargs="?", const=2, help="кубики")
    p_rand.add_argument("--sides", type=int, default=6)
    p_rand.add_argument("--password", type=int, nargs="?", const=16)
    p_rand.add_argument("--coins", type=int, nargs="?", const=1)

    p_ascii = sub.add_parser("ascii", help="ascii-арт и таблицы")
    p_ascii.add_argument("text", nargs="*")
    p_ascii.add_argument("--bar", type=float, help="прогресс-бар, %%")

    p_horo = sub.add_parser("horoscope", help="гороскоп")
    p_horo.add_argument("sign")
    p_horo.add_argument("--compat", metavar="SIGN", help="совместимость")

    sub.add_parser("quote", help="цитата дня")

    p_timer = sub.add_parser("timer", help="таймер прокрастинации")
    p_timer.add_argument("--minutes", type=int, default=1)
    p_timer.add_argument("--quiet", action="store_true")

    return parser


def _cmd_excuse(args):
    from .excuses import excuse_of_the_day, excuses_for_context, random_excuse

    if args.today:
        logger.info("сегодняшняя отмазка")
        print(excuse_of_the_day())
    elif args.context:
        logger.info("отмазки по контексту: %s", args.context)
        for excuse in excuses_for_context(args.context):
            print("-", excuse)
    else:
        for _ in range(args.count):
            print("-", random_excuse())
    return 0


def _cmd_cipher(args):
    from .cipher import (
        affine,
        atbash,
        caesar,
        drunk_caesar,
        rot13,
        vigenere,
    )

    text = " ".join(args.text)
    if args.algo == "caesar":
        result = caesar(text, args.shift)
    elif args.algo == "drunk":
        result = drunk_caesar(text)
    elif args.algo == "rot13":
        result = rot13(text)
    elif args.algo == "atbash":
        result = atbash(text)
    elif args.algo == "vigenere":
        result = vigenere(text, args.key or "пароль", decrypt=args.decrypt)
    else:
        result = affine(text, args.a, args.b, decrypt=args.decrypt)
    print(result)
    return 0


def _cmd_random(args):
    from .randomizer import (
        flip_coins,
        random_password,
        random_uuid,
        roll_dice,
        weighted_pick,
    )

    if args.dice is not None:
        roll = roll_dice(args.dice, args.sides)
        print(f"Кубики d{roll['sides']}: {roll['rolls']} = {roll['total']}")
    if args.password is not None:
        print("Пароль:", random_password(args.password))
    if args.coins is not None:
        print("Монетки:", ", ".join(flip_coins(args.coins)))
    if args.dice is None and args.password is None and args.coins is None:
        print("Взвешенный выбор:", weighted_pick(["дело", "отдых"], [30, 70]))
        print("UUID:", random_uuid())
    return 0


def _cmd_ascii(args):
    from .ascii import banner, table, progress_bar

    if args.text:
        print(banner(" ".join(args.text)))
        print(table(
            ["модуль", "статус"],
            [["excuses", "готов"], ["cipher", "готов"], ["timer", "ломается по плану"]],
        ))
    if args.bar is not None:
        print(progress_bar(args.bar))
    return 0


def _cmd_horoscope(args):
    from .astrology import compatibility, horoscope

    if args.compat:
        result = compatibility(args.sign, args.compat)
        print(f"{result['signs'][0]} и {result['signs'][1]}: "
              f"совместимость {result['score']}/100 — {result['verdict']}")
    else:
        print(horoscope(args.sign))
    return 0


def _cmd_quote(_args):
    from .motivation import quote_of_the_day

    print(quote_of_the_day())
    return 0


def _cmd_timer(args):
    from .timer import procrastinate

    print(procrastinate(args.minutes, quiet=args.quiet))
    return 0


HANDLERS = {
    "excuse": _cmd_excuse,
    "cipher": _cmd_cipher,
    "random": _cmd_random,
    "ascii": _cmd_ascii,
    "horoscope": _cmd_horoscope,
    "quote": _cmd_quote,
    "timer": _cmd_timer,
}


def main(argv=None):
    """Точка входа CLI. Возвращает код возврата."""
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = HANDLERS.get(args.command)
    if handler is None:
        parser.print_help()
        return 2
    try:
        return handler(args)
    except (ValueError, KeyError) as exc:
        logger.error(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
