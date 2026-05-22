"""
Тесты для модуля core/scanner.py.

Юнит-тесты — проверяют одну функцию в изоляции, без CLI и без .env.
"""

# tmp_path — встроенная pytest fixture, тип Path нужен для аннотации.
from pathlib import Path

import pytest

from cli_file_processor.core.scanner import normalize_extension, scan_files
from cli_file_processor.exceptions import InputDirNotFoundError, InputNotADirectoryError

# ─────────────────────────────────────────────
# Тесты для normalize_extension
# ─────────────────────────────────────────────


# @pytest.mark.parametrize запускает один тест несколько раз с разными данными.
# Первый аргумент — имена параметров (строка через запятую).
# Второй аргумент — список кортежей (raw, expected).
# pytest создаст отдельный тест-кейс для каждой строки и покажет их по отдельности.
@pytest.mark.parametrize(
    "raw,expected",
    [
        ("txt", ".txt"),  # без точки — добавляется
        (".txt", ".txt"),  # точка есть — не дублируется
        ("PDF", ".pdf"),  # верхний регистр → нижний
        ("  .TXT  ", ".txt"),  # пробелы по краям убираются
        ("  PDF  ", ".pdf"),  # всё вместе: пробелы + регистр + без точки
    ],
)
def test_normalize_extension(raw: str, expected: str) -> None:
    assert normalize_extension(raw) == expected


# ─────────────────────────────────────────────
# Тесты для scan_files
# ─────────────────────────────────────────────

# tmp_path — встроенная fixture pytest. Pytest создаёт временную папку
# специально для этого теста и удаляет её после. Мы не трогаем реальные файлы.
# Fixture — это вспомогательный объект, который pytest автоматически передаёт
# в тест когда видит аргумент с нужным именем.


def test_scan_files_finds_txt_files(sample_txt_dir: Path) -> None:
    # sample_txt_dir — наша fixture из conftest.py: 2 .txt + 1 .pdf
    # pytest передаёт её автоматически по имени аргумента
    result = scan_files(input_dir=sample_txt_dir, extension=".txt")

    assert len(result) == 2


def test_scan_files_returns_only_matching_extension(tmp_path: Path):
    (tmp_path / "file.txt").touch()
    (tmp_path / "file.xlsx").touch()
    (tmp_path / "file.pdf").touch()

    result = scan_files(input_dir=tmp_path, extension=".xlsx")

    assert len(result) == 1
    # result[0] — первый элемент списка. .name — только имя файла без пути.
    assert result[0].name == "file.xlsx"


def test_scan_files_returns_empty_when_no_match(tmp_path: Path):
    # Папка есть, файлы есть, но нужного расширения нет
    (tmp_path / "file.txt").touch()

    result = scan_files(input_dir=tmp_path, extension=".pdf")

    # Должен вернуться пустой список, а не ошибка
    assert result == []


def test_scan_files_normalizes_extension(tmp_path: Path):
    # scan_files должен принять "PDF" (без точки, верхний регистр)
    # и всё равно найти файлы .pdf
    (tmp_path / "document.pdf").touch()

    result = scan_files(input_dir=tmp_path, extension="PDF")

    assert len(result) == 1


def test_scan_files_returns_path_objects(tmp_path: Path):
    # Проверяем тип возвращаемых данных — должны быть объекты Path
    (tmp_path / "file.txt").touch()

    result = scan_files(input_dir=tmp_path, extension=".txt")

    # isinstance(obj, тип) — проверяет, является ли obj экземпляром указанного типа
    assert isinstance(result[0], Path)


def test_scan_files_empty_directory(tmp_path: Path):
    # Папка существует, но пустая — не должно быть ошибки
    result = scan_files(input_dir=tmp_path, extension=".txt")

    assert result == []


def test_scan_files_recursive_finds_in_subdirs(tmp_path: Path):
    # Файл в корне и файл во вложенной папке
    (tmp_path / "root.txt").touch()
    subdir = tmp_path / "sub"
    subdir.mkdir()
    (subdir / "nested.txt").touch()

    result = scan_files(input_dir=tmp_path, extension=".txt", recursive=True)

    assert len(result) == 2


def test_scan_files_non_recursive_excludes_subdirs(tmp_path: Path):
    # Без recursive=True файлы в подпапках не должны попадать в результат
    (tmp_path / "root.txt").touch()
    subdir = tmp_path / "sub"
    subdir.mkdir()
    (subdir / "nested.txt").touch()

    result = scan_files(input_dir=tmp_path, extension=".txt", recursive=False)

    assert len(result) == 1
    assert result[0].name == "root.txt"


# ─────────────────────────────────────────────
# Тесты для кастомных исключений
# ─────────────────────────────────────────────


def test_scan_files_raises_when_dir_not_found(tmp_path: Path) -> None:
    # pytest.raises() — контекстный менеджер: тест упадёт если исключение НЕ было брошено.
    with pytest.raises(InputDirNotFoundError) as exc_info:
        scan_files(input_dir=tmp_path / "nonexistent", extension=".txt")
    # exc_info.value — сам объект исключения. Проверяем атрибут и сообщение.
    assert exc_info.value.path == tmp_path / "nonexistent"
    assert "не найдена" in str(exc_info.value)


def test_scan_files_raises_when_not_a_directory(tmp_path: Path) -> None:
    some_file = tmp_path / "iam_a_file.txt"
    some_file.touch()
    with pytest.raises(InputNotADirectoryError) as exc_info:
        scan_files(input_dir=some_file, extension=".txt")
    assert exc_info.value.path == some_file
    assert "не папка" in str(exc_info.value)
