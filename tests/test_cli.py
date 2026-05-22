"""
Тесты для модуля cli.py.

Интеграционные тесты — проверяют всю цепочку: CLI → config → scanner.
Используем CliRunner: он симулирует запуск команды без реального терминала.
"""

from pathlib import Path

# CliRunner — инструмент Typer для тестирования CLI команд.
# Позволяет вызывать команды как функции и проверять их вывод и код завершения.
from typer.testing import CliRunner

# Импортируем объект app — это наше CLI приложение
from cli_file_processor.cli import app

# Создаём один runner на весь файл — он переиспользуется во всех тестах.
# mix_stderr=False — разделяет stdout (обычный вывод) и stderr (ошибки).
runner = CliRunner()


# ─────────────────────────────────────────────
# Тесты команды check
# ─────────────────────────────────────────────


def test_check_command_succeeds():
    # runner.invoke(app, ["аргументы"]) — запускает CLI команду.
    # Возвращает объект result с полями:
    #   .exit_code — код завершения (0 = успех, 1+ = ошибка)
    #   .output    — всё что напечатала команда
    #   .exception — исключение если команда упала (None если всё хорошо)
    result = runner.invoke(app, ["check"])

    assert result.exit_code == 0


def test_check_command_output():
    result = runner.invoke(app, ["check"])

    # .strip() убирает переводы строки в конце вывода
    assert "OK" in result.output


# ─────────────────────────────────────────────
# Тесты команды scan
# ─────────────────────────────────────────────


def test_scan_finds_files(tmp_path: Path):
    # Создаём тестовые файлы во временной папке
    (tmp_path / "a.txt").touch()
    (tmp_path / "b.txt").touch()

    # str(tmp_path) — преобразуем Path в строку для передачи в CLI
    result = runner.invoke(app, ["scan", "--input-dir", str(tmp_path), "--extension", ".txt"])

    assert result.exit_code == 0
    # Проверяем что в выводе есть количество файлов
    assert "2" in result.output


def test_scan_shows_filenames(tmp_path: Path):
    (tmp_path / "report.txt").touch()

    result = runner.invoke(app, ["scan", "--input-dir", str(tmp_path), "--extension", ".txt"])

    # Имя файла должно появиться в выводе
    assert "report.txt" in result.output


def test_scan_fails_when_dir_not_found():
    # Передаём путь к папке которой не существует
    result = runner.invoke(app, ["scan", "--input-dir", "/nonexistent/path", "--extension", ".txt"])

    # Команда должна завершиться с ошибкой (код != 0)
    assert result.exit_code != 0
    assert "не найдена" in result.output


def test_scan_fails_when_path_is_file(tmp_path: Path):
    # Создаём файл и передаём его путь вместо папки
    some_file = tmp_path / "iam_a_file.txt"
    some_file.touch()

    result = runner.invoke(app, ["scan", "--input-dir", str(some_file), "--extension", ".txt"])

    assert result.exit_code != 0
    assert "не папка" in result.output


def test_scan_no_files_found(tmp_path: Path):
    # Папка есть, но файлов нужного расширения нет
    (tmp_path / "file.pdf").touch()

    result = runner.invoke(app, ["scan", "--input-dir", str(tmp_path), "--extension", ".txt"])

    # Команда завершается успешно (0) — "не найдено" это не ошибка
    assert result.exit_code == 0
    assert "не найдены" in result.output


def test_scan_verbose_shows_debug_logs(tmp_path: Path):
    (tmp_path / "file.txt").touch()

    result = runner.invoke(
        app, ["scan", "--input-dir", str(tmp_path), "--extension", ".txt", "--verbose"]
    )

    assert result.exit_code == 0
    # В verbose режиме должны быть строки DEBUG в выводе
    assert "DEBUG" in result.output


def test_scan_short_flags(tmp_path: Path):
    # Проверяем что короткие флаги -i и -e работают так же как длинные
    (tmp_path / "file.txt").touch()

    result = runner.invoke(app, ["scan", "-i", str(tmp_path), "-e", ".txt"])

    assert result.exit_code == 0
    assert "file.txt" in result.output


def test_scan_normalizes_extension(tmp_path: Path):
    # Пользователь ввёл расширение без точки — должно всё равно работать
    (tmp_path / "file.txt").touch()

    result = runner.invoke(app, ["scan", "--input-dir", str(tmp_path), "--extension", "txt"])

    assert result.exit_code == 0
    assert "file.txt" in result.output


# ─────────────────────────────────────────────
# Тесты команды process
# ─────────────────────────────────────────────


def test_process_copies_files(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    (input_dir / "file.txt").write_text("содержимое")

    result = runner.invoke(
        app,
        [
            "process",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--extension",
            ".txt",
        ],
    )

    assert result.exit_code == 0
    # Файл должен появиться в output_dir
    assert (output_dir / "file.txt").exists()


def test_process_reports_count(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    (input_dir / "a.txt").write_text("")
    (input_dir / "b.txt").write_text("")

    result = runner.invoke(
        app,
        [
            "process",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--extension",
            ".txt",
        ],
    )

    assert result.exit_code == 0
    assert "2" in result.output


def test_process_fails_when_input_missing(tmp_path: Path):
    result = runner.invoke(
        app,
        [
            "process",
            "--input-dir",
            str(tmp_path / "nonexistent"),
            "--output-dir",
            str(tmp_path / "output"),
            "--extension",
            ".txt",
        ],
    )

    assert result.exit_code != 0
    assert "не найдена" in result.output


def test_process_warns_when_no_files(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    # Папка есть, но файлов нужного расширения нет
    result = runner.invoke(
        app,
        [
            "process",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--extension",
            ".txt",
        ],
    )

    assert result.exit_code == 0
    assert "не найдены" in result.output


def test_process_creates_output_dir(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "new" / "nested" / "output"
    # output_dir не существует — команда должна создать её

    (input_dir / "file.txt").write_text("")

    result = runner.invoke(
        app,
        [
            "process",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--extension",
            ".txt",
        ],
    )

    assert result.exit_code == 0
    assert output_dir.exists()


# ─────────────────────────────────────────────
# Тесты флага --dry-run
# ─────────────────────────────────────────────


def test_dry_run_does_not_copy_files(tmp_path: Path):
    # Главное свойство dry-run: файлы НЕ должны копироваться
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    (input_dir / "file.txt").write_text("содержимое")

    runner.invoke(
        app,
        [
            "process",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--extension",
            ".txt",
            "--dry-run",
        ],
    )

    # output_dir не должна быть создана — копирования не было
    assert not output_dir.exists()


def test_dry_run_shows_filenames(tmp_path: Path):
    # dry-run должен показать имена файлов которые БЫЛИ БЫ скопированы
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    (input_dir / "report.txt").write_text("")

    result = runner.invoke(
        app,
        [
            "process",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--extension",
            ".txt",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    assert "report.txt" in result.output


def test_dry_run_shows_destination(tmp_path: Path):
    # dry-run должен показать куда файлы БЫЛИ БЫ скопированы
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    (input_dir / "file.txt").write_text("")

    result = runner.invoke(
        app,
        [
            "process",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--extension",
            ".txt",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    # Путь назначения должен быть в выводе
    assert str(output_dir) in result.output


def test_dry_run_exits_successfully(tmp_path: Path):
    # dry-run — это не ошибка, exit code должен быть 0
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "file.txt").write_text("")

    result = runner.invoke(
        app,
        [
            "process",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(tmp_path / "output"),
            "--extension",
            ".txt",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
