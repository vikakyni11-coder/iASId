"""ASCII-арт и псевдо-таблицы: баннеры, таблицы, прогресс-бары."""


def banner(text, char="#"):
    """Простой баннер: текст, обрамлённый рамкой из char."""
    text = str(text)
    width = len(text) + 4
    edge = char * width
    return "\n".join([edge, f"{char} {text} {char}", edge])


def table(headers, rows):
    """Текстовая таблица с рамками, выравнивание по ширине колонок."""
    col_widths = [len(str(header)) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            col_widths[index] = max(col_widths[index], len(str(cell)))

    def fmt(cells):
        return "| " + " | ".join(
            str(cell).ljust(col_widths[index])
            for index, cell in enumerate(cells)
        ) + " |"

    separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"
    lines = [separator, fmt(headers), separator]
    for row in rows:
        lines.append(fmt(row))
    lines.append(separator)
    return "\n".join(lines)


def progress_bar(percent, width=20):
    """Прогресс-бар вида [#####.....]  45.0%."""
    percent = max(0.0, min(100.0, percent))
    filled = int(round(width * percent / 100.0))
    bar = "#" * filled + "." * (width - filled)
    return f"[{bar}] {percent:6.1f}%"


def pixel_block(text, fill="#"):
    """Рисует текст «пикселями»: каждая буква в квадрате из fill."""
    lines = []
    for char in str(text):
        lines.append(f"{fill} {char} {fill}")
    return "\n".join(lines)
