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
from cli_file_processor.core.timer import Timer
from cli_file_processor.exceptions import ProcessorError

# Импортируем функцию настройки логирования
from cli_file_processor.logging_config import setup_logging

# Импортируем функции вывода из output.py — они отвечают за внешний вид
from cli_file_processor.output import (
    print_dry_run_results,
    print_error,
    print_process_results,
    print_scan_results,
    print_warning,
    process_files_with_progress,
)

# typer.Typer() — создаём объект приложения. Это "контейнер" для всех команд.
# help= — текст, который появляется при запуске: cli-file-processor --help
app = typer.Typer(help="CLI File Processor — инструмент для обработки файлов.")


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
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Искать файлы во всех вложенных подпапках.",
    ),
) -> None:
    """
    Ищет файлы с указанным расширением во входной папке.
    """
    setup_logging(verbose=verbose)

    if input_dir is None:
        input_dir = get_default_input_dir()
    if extension is None:
        extension = get_default_extension()

    # scanner.py сам проверяет директорию и бросает ProcessorError если что-то не так.
    # CLI ловит базовый класс — любая ошибка бизнес-логики обрабатывается одинаково.
    try:
        # Timer измеряет время даже если scan_files бросит исключение:
        # __exit__ вызовется до того как исключение дойдёт до except.
        with Timer() as t:
            result = scan_files(input_dir=input_dir, extension=extension, recursive=recursive)
    except ProcessorError as e:
        print_error(str(e))
        raise typer.Exit(code=1)

    if not result.files:
        print_warning(f"файлы с расширением {extension} не найдены.")
        return

    print_scan_results(result, elapsed=t.elapsed)


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
    # --dry-run: показать что БУДЕТ сделано, но ничего не делать.
    # Паттерн "симуляция" — стандарт для деструктивных операций.
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Показать что будет скопировано без реального копирования.",
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Искать файлы во всех вложенных подпапках.",
    ),
) -> None:
    """
    Находит файлы с указанным расширением и копирует их в папку назначения.
    """
    setup_logging(verbose=verbose)

    if input_dir is None:
        input_dir = get_default_input_dir()
    if output_dir is None:
        output_dir = get_default_output_dir()
    if extension is None:
        extension = get_default_extension()

    try:
        scan_result = scan_files(input_dir=input_dir, extension=extension, recursive=recursive)
    except ProcessorError as e:
        print_error(str(e))
        raise typer.Exit(code=1)

    if not scan_result.files:
        print_warning(f"файлы с расширением {extension} не найдены.")
        return

    if dry_run:
        print_dry_run_results(scan_result, output_dir)
    else:
        with Timer() as process_timer:
            process_result = process_files_with_progress(scan_result.files, output_dir)
        print_process_results(process_result, elapsed=process_timer.elapsed)
