"""
CLI-модуль проекта.

Здесь находятся команды, которые пользователь запускает из терминала.
Принцип: CLI только принимает параметры и показывает результат.
Вся бизнес-логика — в других модулях (scanner.py и т.д.).
"""

from pathlib import Path

import typer

# Импортируем функции из config.py — они читают настройки из .env
from cli_file_processor.config import (
    get_app_version,
    get_default_extension,
    get_default_input_dir,
    get_default_output_dir,
)

# Импортируем бизнес-логику поиска файлов из core/scanner.py
from cli_file_processor.core.scanner import scan_files

# Импортируем функцию настройки логирования
from cli_file_processor.logging_config import setup_logging

# Импортируем функции вывода из output.py — они отвечают за внешний вид
from cli_file_processor.output import (
    print_error,
    print_process_results,
    print_scan_results,
    print_warning,
    process_files_with_progress,
)

# typer.Typer() — создаём объект приложения. Это "контейнер" для всех команд.
# help= — текст, который появляется при запуске: cli-file-processor --help
app = typer.Typer(
    help="CLI File Processor — инструмент для обработки файлов."
)


# @app.command() — декоратор. Говорит Typer: "зарегистрируй функцию check как команду CLI".
@app.command()
def check() -> None:
    """
    Проверяет, что CLI-приложение запускается.
    """
    typer.echo("Project check: OK")


@app.command()
def version() -> None:
    """
    Показывает версию приложения.
    """
    typer.echo(get_app_version())


@app.command()
def scan(
    # typer.Option() — параметр-флаг: пользователь пишет --input-dir /path
    # Path | None — тип: либо объект Path, либо None (если флаг не передан)
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        "-i",
        help="Папка, в которой нужно искать файлы.",
    ),
    extension: str | None = typer.Option(
        None,
        "--extension",
        "-e",
        help="Расширение файлов для поиска. Например: .txt, .xlsx, .pdf",
    ),
    # Typer автоматически обрабатывает bool-параметры как флаги.
    # Пользователь пишет --verbose (True) или не пишет (False, по умолчанию).
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Показать подробный вывод (DEBUG-логи).",
    ),
) -> None:
    """
    Ищет файлы с указанным расширением во входной папке.
    """

    # Настраиваем логирование в самом начале команды, до любой работы.
    # verbose=True → уровень DEBUG (подробно), verbose=False → уровень INFO (кратко).
    setup_logging(verbose=verbose)

    # Если пользователь не передал флаг — берём значение из config.py (.env).
    # Приоритет: флаг в терминале → значение в .env → запасное значение в config.py
    if input_dir is None:
        input_dir = get_default_input_dir()
    if extension is None:
        extension = get_default_extension()

    # Валидация — проверяем входные данные ДО начала работы.
    if not input_dir.exists():
        print_error(f"папка не найдена: {input_dir}")
        raise typer.Exit(code=1)

    if not input_dir.is_dir():
        print_error(f"это не папка: {input_dir}")
        raise typer.Exit(code=1)

    # Вызываем бизнес-логику — функцию из scanner.py.
    files = scan_files(input_dir=input_dir, extension=extension)

    if not files:
        # print_warning — жёлтое предупреждение, не ошибка
        print_warning(f"файлы с расширением {extension} не найдены.")
        return

    # Передаём результат в output.py — пусть он решает как это выглядит.
    print_scan_results(files)


@app.command()
def process(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        "-i",
        help="Папка с исходными файлами.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Папка назначения для скопированных файлов.",
    ),
    extension: str | None = typer.Option(
        None,
        "--extension",
        "-e",
        help="Расширение файлов для обработки. Например: .txt, .xlsx, .pdf",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Показать подробный вывод (DEBUG-логи).",
    ),
) -> None:
    """
    Находит файлы с указанным расширением и копирует их в папку назначения.
    """
    setup_logging(verbose=verbose)

    # Подставляем дефолты из config.py если флаги не переданы
    if input_dir is None:
        input_dir = get_default_input_dir()
    if output_dir is None:
        output_dir = get_default_output_dir()
    if extension is None:
        extension = get_default_extension()

    # Валидация входной папки — она должна существовать
    if not input_dir.exists():
        print_error(f"папка не найдена: {input_dir}")
        raise typer.Exit(code=1)

    if not input_dir.is_dir():
        print_error(f"это не папка: {input_dir}")
        raise typer.Exit(code=1)

    # Папку назначения НЕ проверяем на существование — processor.py создаст её сам.

    # Находим файлы
    files = scan_files(input_dir=input_dir, extension=extension)

    if not files:
        print_warning(f"файлы с расширением {extension} не найдены.")
        return

    # Копируем с прогресс-баром и выводим итог
    processed = process_files_with_progress(files, output_dir)
    print_process_results(processed, output_dir)
