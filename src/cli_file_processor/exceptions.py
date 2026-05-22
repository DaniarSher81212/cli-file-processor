"""
Кастомные исключения проекта.

Иерархия: ProcessorError — базовый класс для всех ошибок приложения.
Конкретные ошибки наследуют от него, что позволяет ловить их
по-отдельности (конкретный тип) или все сразу (ProcessorError).
"""

from pathlib import Path


class ProcessorError(Exception):
    """Базовый класс для всех ошибок приложения."""


class InputDirNotFoundError(ProcessorError):
    """Директория не существует."""

    def __init__(self, path: Path) -> None:
        # Сохраняем путь как атрибут — вызывающий код может его использовать.
        self.path = path
        # super().__init__() — передаём сообщение в базовый Exception.
        # str(e) вернёт именно этот текст.
        super().__init__(f"папка не найдена: {path}")


class InputNotADirectoryError(ProcessorError):
    """Путь существует, но указывает на файл, а не на директорию."""

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"это не папка: {path}")
