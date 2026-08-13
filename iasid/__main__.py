"""Поддержка запуска как модуля: python -m iasid."""
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
