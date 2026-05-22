"""
Модуль поиска файлов.

Здесь находится бизнес-логика, связанная со сканированием папок.
Этот модуль ничего не знает о CLI — он просто умеет искать файлы.
"""

import logging
from pathlib import Path

from cli_file_processor.exceptions import InputDirNotFoundError, InputNotADirectoryError

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
    extension = extension.strip().lower()

    if not extension.startswith("."):
        extension = f".{extension}"

    logger.debug("расширение нормализовано: '%s'", extension)
    return extension


def scan_files(input_dir: Path, extension: str, recursive: bool = False) -> list[Path]:
    """
    Ищет файлы с указанным расширением в папке.

    Аргументы:
        input_dir — папка для поиска (объект Path)
        extension — расширение файлов, например ".txt" или "pdf"
        recursive — если True, ищет и во всех вложенных подпапках

    Возвращает:
        Список объектов Path — найденные файлы. Пустой список если ничего не нашли.
    """
    if not input_dir.exists():
        raise InputDirNotFoundError(input_dir)
    if not input_dir.is_dir():
        raise InputNotADirectoryError(input_dir)

    logger.debug("начинаем поиск в папке: %s (recursive=%s)", input_dir, recursive)

    normalized_extension = normalize_extension(extension)

    if recursive:
        # rglob("*.txt") — рекурсивный поиск: текущая папка + все вложенные.
        # "r" в rglob = recursive. Обходит всё дерево подпапок.
        files = list(input_dir.rglob(f"*{normalized_extension}"))
    else:
        # glob("*.txt") — поиск только в указанной папке, без вложенных.
        files = list(input_dir.glob(f"*{normalized_extension}"))

    logger.debug("найдено файлов: %d", len(files))
    return files
