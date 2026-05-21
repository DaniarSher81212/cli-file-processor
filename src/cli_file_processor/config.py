"""
Конфигурация приложения.

Читает настройки из переменных окружения / .env файла.
Всё приложение должно брать настройки отсюда, а не хардкодить значения.
"""

# Path — современный способ работы с путями файловой системы в Python.
# Вместо строки "/home/user/data" используем объект Path со своими методами.
from pathlib import Path

# load_dotenv — функция из библиотеки python-dotenv.
# Она читает файл .env и кладёт переменные в os.environ.
from dotenv import load_dotenv

# os — стандартная библиотека. os.getenv() читает переменные окружения.
import os


# load_dotenv() вызывается прямо при импорте модуля.
# Алгоритм: ищет .env в текущей папке → читает строки KEY=VALUE → кладёт в os.environ.
# Если .env нет — просто ничего не делает (не падает с ошибкой).
load_dotenv()


# -> Path — аннотация возвращаемого типа. Говорит: "функция всегда возвращает Path".
# Python не проверяет это на ходу, но IDE и Pyright используют для подсказок.
def get_default_input_dir() -> Path:
    # os.getenv("КЛЮЧ", "запасное_значение"):
    #   - ищет переменную DEFAULT_INPUT_DIR в os.environ (туда load_dotenv положил данные из .env)
    #   - если нашёл — возвращает её значение (строку)
    #   - если не нашёл — возвращает "data/input" (второй аргумент)
    # Path(...) — оборачиваем строку в объект Path, чтобы дальше вызывать .exists(), .is_dir() и т.д.
    return Path(os.getenv("DEFAULT_INPUT_DIR", "data/input"))


def get_default_extension() -> str:
    # Аналогично: читаем DEFAULT_EXTENSION из .env, по умолчанию ".txt".
    # Здесь Path не нужен — расширение остаётся строкой.
    return os.getenv("DEFAULT_EXTENSION", ".txt")


def get_default_output_dir() -> Path:
    return Path(os.getenv("DEFAULT_OUTPUT_DIR", "data/output"))


def get_app_version() -> str:
    return "0.1.0"
