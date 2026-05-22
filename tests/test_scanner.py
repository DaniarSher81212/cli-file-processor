"""
Тесты для модуля core/scanner.py.

Юнит-тесты — проверяют одну функцию в изоляции, без CLI и без .env.
"""

# tmp_path — встроенная pytest fixture, тип Path нужен для аннотации.
from pathlib import Path

from cli_file_processor.core.scanner import normalize_extension, scan_files

# ─────────────────────────────────────────────
# Тесты для normalize_extension
# ─────────────────────────────────────────────

# Каждая тестовая функция начинается с test_ — pytest находит их автоматически.
# Имя описывает сценарий: test_<что_проверяем>_<при_каком_условии>


def test_normalize_extension_adds_dot():
    # Проверяем: "txt" без точки → ".txt" с точкой
    # assert — ключевое слово Python. Если выражение False — тест падает с ошибкой.
    assert normalize_extension("txt") == ".txt"


def test_normalize_extension_keeps_existing_dot():
    # Если точка уже есть — не должна добавиться вторая
    assert normalize_extension(".txt") == ".txt"


def test_normalize_extension_lowercases():
    # Верхний регистр должен стать нижним
    assert normalize_extension("PDF") == ".pdf"


def test_normalize_extension_strips_spaces():
    # Пробелы по краям должны убираться
    assert normalize_extension("  .TXT  ") == ".txt"


def test_normalize_extension_combined():
    # Всё сразу: без точки + верхний регистр + пробелы
    assert normalize_extension("  PDF  ") == ".pdf"


# ─────────────────────────────────────────────
# Тесты для scan_files
# ─────────────────────────────────────────────

# tmp_path — встроенная fixture pytest. Pytest создаёт временную папку
# специально для этого теста и удаляет её после. Мы не трогаем реальные файлы.
# Fixture — это вспомогательный объект, который pytest автоматически передаёт
# в тест когда видит аргумент с нужным именем.


def test_scan_files_finds_txt_files(tmp_path: Path):
    # Создаём тестовые файлы в временной папке
    # tmp_path / "file.txt" — оператор / у Path создаёт вложенный путь
    (tmp_path / "file1.txt").touch()  # .touch() создаёт пустой файл
    (tmp_path / "file2.txt").touch()
    (tmp_path / "report.pdf").touch()  # этот не должен попасть в результат

    result = scan_files(input_dir=tmp_path, extension=".txt")

    # Должны найти ровно 2 файла
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
