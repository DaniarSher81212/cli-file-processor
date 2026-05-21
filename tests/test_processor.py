"""
Тесты для модуля core/processor.py.
"""

from pathlib import Path

from cli_file_processor.core.processor import process_files


def test_process_files_copies_to_output(tmp_path: Path):
    # Создаём структуру: input/ и output/ во временной папке
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"
    # output_dir НЕ создаём — processor должен создать сам

    # Создаём исходный файл
    source_file = input_dir / "file.txt"
    source_file.write_text("содержимое файла")

    process_files([source_file], output_dir)

    # Проверяем что файл появился в папке назначения
    assert (output_dir / "file.txt").exists()


def test_process_files_creates_output_dir(tmp_path: Path):
    # Проверяем что process_files создаёт output_dir если её нет
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "deeply" / "nested" / "output"
    # Папка не существует — даже промежуточные

    source_file = input_dir / "file.txt"
    source_file.write_text("текст")

    process_files([source_file], output_dir)

    assert output_dir.exists()


def test_process_files_preserves_content(tmp_path: Path):
    # Проверяем что содержимое файла сохраняется при копировании
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    source_file = input_dir / "file.txt"
    source_file.write_text("важное содержимое 123")

    process_files([source_file], output_dir)

    # read_text() — читает содержимое файла как строку
    copied_content = (output_dir / "file.txt").read_text()
    assert copied_content == "важное содержимое 123"


def test_process_files_returns_destination_paths(tmp_path: Path):
    # process_files должен вернуть пути в output_dir, а не в input_dir
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    source_file = input_dir / "file.txt"
    source_file.write_text("")

    result = process_files([source_file], output_dir)

    assert len(result) == 1
    # Путь должен указывать в output_dir
    assert result[0].parent == output_dir


def test_process_files_handles_multiple_files(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    files = []
    for name in ["a.txt", "b.txt", "c.txt"]:
        f = input_dir / name
        f.write_text(name)
        files.append(f)

    result = process_files(files, output_dir)

    assert len(result) == 3
    # Все три файла должны быть в output_dir
    for name in ["a.txt", "b.txt", "c.txt"]:
        assert (output_dir / name).exists()


def test_process_files_overwrites_existing(tmp_path: Path):
    # Если файл уже есть в output — он должен перезаписаться
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Создаём "старый" файл в output
    old_file = output_dir / "file.txt"
    old_file.write_text("старое содержимое")

    # Копируем новый файл с тем же именем
    source_file = input_dir / "file.txt"
    source_file.write_text("новое содержимое")

    process_files([source_file], output_dir)

    assert old_file.read_text() == "новое содержимое"
