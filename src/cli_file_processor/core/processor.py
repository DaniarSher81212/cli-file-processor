"""
Модуль обработки файлов.

Здесь находится бизнес-логика копирования файлов.
Этот модуль ничего не знает о CLI и о том, как выглядит вывод.
"""

import logging

# shutil — стандартная библиотека Python для высокоуровневых операций с файлами.
# "shutil" = "shell utilities". Умеет: копировать, перемещать, удалять деревья папок.
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


def process_files(files: list[Path], output_dir: Path) -> list[Path]:
    """
    Копирует файлы из списка в папку output_dir.

    Если output_dir не существует — создаёт её автоматически.
    Если файл с таким именем уже есть в output_dir — перезаписывает.

    Аргументы:
        files      — список файлов для копирования (объекты Path)
        output_dir — папка назначения

    Возвращает:
        Список путей к скопированным файлам в output_dir.
    """

    # mkdir() — создать папку.
    # parents=True  — создать все промежуточные папки если их нет.
    #                 Например: "data/output/sub" создаст и "data", и "output", и "sub".
    # exist_ok=True — не падать с ошибкой если папка уже существует.
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.debug("папка назначения: %s", output_dir)

    processed: list[Path] = []

    for source_path in files:
        # output_dir / source_path.name — строим путь назначения.
        # source_path.name — только имя файла: "data/input/file.txt" → "file.txt"
        # output_dir / "file.txt" → "data/output/file.txt"
        destination_path = output_dir / source_path.name

        # shutil.copy2() — копирует файл и сохраняет метаданные (дату создания и т.д.).
        # Отличие от shutil.copy(): copy() копирует только содержимое,
        # copy2() копирует ещё и метаданные файла.
        shutil.copy2(source_path, destination_path)

        logger.debug("скопирован: %s → %s", source_path.name, destination_path)

        # .append() — добавляет элемент в конец списка.
        processed.append(destination_path)

    logger.debug("обработано файлов: %d", len(processed))
    return processed
