"""Логирование с уровнями и цветами ANSI.

Логгер реализован как синглтон: сколько ни вызывай get_logger(),
вернётся один и тот же объект. Уровни: debug < info < warn < error.
"""

import sys
from datetime import datetime

LEVELS = {"debug": 0, "info": 1, "warn": 2, "error": 3}
COLORS = {
    "debug": "\033[90m",
    "info": "\033[36m",
    "warn": "\033[33m",
    "error": "\033[31m",
}
RESET = "\033[0m"


class Logger:
    """Простой логгер с поддержкой цветов и синглтон-поведением."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, level="info", use_colors=True):
        self.level = level
        self.use_colors = use_colors

    def _emit(self, level, message):
        if LEVELS[level] < LEVELS.get(self.level, 1):
            return
        ts = datetime.now().strftime("%H:%M:%S")
        label = level.upper()
        line = f"[{ts}] {label:5s} {message}"
        if self.use_colors and sys.stdout.isatty():
            line = f"{COLORS[level]}{line}{RESET}"
        stream = sys.stderr if level in ("warn", "error") else sys.stdout
        print(line, file=stream)

    def debug(self, message):
        self._emit("debug", message)

    def info(self, message):
        self._emit("info", message)

    def warn(self, message):
        self._emit("warn", message)

    def error(self, message):
        self._emit("error", message)

    def set_level(self, level):
        if level in LEVELS:
            self.level = level


def get_logger():
    """Возвращает глобальный экземпляр логгера."""
    return Logger()
