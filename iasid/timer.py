"""Таймер прокрастинации: считает время, которое вы «работаете».

Главный результат работы таймера — красивая цифра на экране и ощущение,
что день прожит не зря.
"""

import sys
import time

from .utils import format_seconds


def procrastinate(minutes=1, interval_seconds=10, quiet=False):
    """Отсчитывает минуты «занятости» и возвращает честный вывод.

    quiet=True отключает промежуточные сообщения (для скриптов).
    """
    if minutes <= 0:
        raise ValueError("минуты должны быть положительными")
    total = minutes * 60
    remaining = total
    while remaining > 0:
        if not quiet:
            sys.stdout.write(
                f"\rПрикидываюсь занятым: "
                f"{format_seconds(remaining)} осталось"
            )
            sys.stdout.flush()
        time.sleep(interval_seconds)
        remaining -= interval_seconds
    if not quiet:
        sys.stdout.write("\n")
    return f"Прошло {format_seconds(total)}. Работать так и не начали."


def pomodoro_parody(work_minutes=25, breaks_taken=0):
    """Возвращает план «помидорки», который никто не выполнит."""
    steps = []
    for round_no in range(1, 4):
        steps.append(
            f"раунд {round_no}: {work_minutes} минут думаем о том, "
            "что нужно работать"
        )
    steps.append(f"перерыв №{breaks_taken + 1} — длится вечность")
    return steps
