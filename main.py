import random
import sys

EXCUSES = [
    "собака съела интернет",
    "меня сломало обновление Windows",
    "я был в другом часовом поясе",
    "git reset --hard --прошлое",
    "тестировщики отдыхали",
    "это не баг, это фича",
    "у меня лапки",
    "компилятор косплеил тормоз",
    "виноват коллега из другого кабинета",
    "AI сделал рефакторинг без спроса",
]

def random_excuse():
    return random.choice(EXCUSES)

def drunk_caesar(text, shift=None):
    if shift is None:
        shift = random.randint(-3, 3)
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("а") if "а" <= ch.lower() <= "я" else ord("a")
            offset = (ord(ch.lower()) - base + shift) % 26
            new = chr(base + offset)
            result.append(new.upper() if ch.isupper() else new)
        else:
            result.append(ch)
    return "".join(result)

def main():
    print("=== Генератор бесполезности v0.1 ===")
    msg = sys.argv[1] if len(sys.argv) > 1 else "я всё сломал"
    print(f"Сообщение: {msg}")
    print(f"Шифровка: {drunk_caesar(msg)}")
    print(f"Отмазка: {random_excuse()}")
    print(f"Случайное число: {random.randint(1, 100)} (зачем — никто не знает)")

if __name__ == "__main__":
    main()
