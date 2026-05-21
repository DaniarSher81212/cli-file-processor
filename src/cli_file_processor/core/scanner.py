"""
Модуль поиска файлов.

Здесь находится бизнес-логика, связанная со сканированием папок.
Этот модуль ничего не знает о CLI — он просто умеет искать файлы.
"""

import logging

# Path — объект для работы с путями. Умеет: .exists(), .is_dir(), .glob(), и многое другое.
from pathlib import Path

# logging.getLogger(__name__) — создаём логгер для этого модуля.
# __name__ — специальная переменная Python. Внутри модуля она равна его полному имени:
# "cli_file_processor.core.scanner". Это позволяет фильтровать логи по модулям.
# Соглашение: один логгер на файл, всегда с именем __name__.
logger = logging.getLogger(__name__)


def normalize_extension(extension: str) -> str:
    """
    Нормализует расширение файла — приводит к единому виду.

    Примеры:
        "txt"    -> ".txt"
        ".txt"   -> ".txt"
        "PDF"    -> ".pdf"
        " .Txt " -> ".txt"
    """

    # .strip() убирает пробелы с обоих краёв строки: " .txt " -> ".txt"
    # .lower() переводит все символы в нижний регистр: "PDF" -> "pdf"
    # Методы вызываются цепочкой: каждый следующий работает с результатом предыдущего.
    extension = extension.strip().lower()

    # .startswith(".") проверяет, начинается ли строка с точки.
    # "not" инвертирует результат: заходим в блок если точки НЕТ.
    if not extension.startswith("."):
        # f-строка: f".{extension}" при extension="txt" даёт ".txt"
        extension = f".{extension}"

    # logger.debug() — сообщение видно только с флагом --verbose.
    # Используем для деталей, которые нужны при отладке, но шумят в обычном режиме.
    logger.debug("расширение нормализовано: '%s'", extension)

    return extension


def scan_files(input_dir: Path, extension: str) -> list[Path]:
    """
    Ищет файлы с указанным расширением в папке.

    Аргументы:
        input_dir  — папка для поиска (объект Path)
        extension  — расширение файлов, например ".txt" или "pdf"

    Возвращает:
        Список объектов Path — найденные файлы. Пустой список если ничего не нашли.
    """

    logger.debug("начинаем поиск в папке: %s", input_dir)

    # Сначала нормализуем расширение: "PDF" -> ".pdf", "txt" -> ".txt"
    normalized_extension = normalize_extension(extension)

    # Path.glob(паттерн) ищет файлы по шаблону внутри папки.
    # "*" означает "любое имя файла".
    # Итого: "*.txt" — все файлы с расширением .txt в этой папке.
    # glob() возвращает генератор (ленивый итератор) — list() превращает его в обычный список.
    files = list(input_dir.glob(f"*{normalized_extension}"))

    # logger.debug() — видно только с --verbose.
    # Результат для пользователя уже выводит cli.py через typer.echo.
    # Здесь нам нужна только внутренняя диагностика — сколько нашёл glob.
    logger.debug("glob вернул файлов: %d", len(files))

    return files
