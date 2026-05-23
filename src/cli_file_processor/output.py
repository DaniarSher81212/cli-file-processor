"""
Модуль вывода.

Отвечает только за то, КАК данные отображаются в терминале.
cli.py решает ЧТО показать, output.py решает КАК это выглядит.
"""

from pathlib import Path

# Console — главный объект Rich. Через него выводим весь текст.
# Он умеет: цвета, таблицы, прогресс-бары, форматирование.
from rich.console import Console

# Progress — полноценный прогресс-бар с настраиваемыми колонками.
# track() — упрощённая обёртка над Progress для простых случаев (одна строка).
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

# Table — объект для построения таблиц с рамками и колонками.
from rich.table import Table

from cli_file_processor.core.models import ProcessResult, ScanResult
from cli_file_processor.core.timer import Elapsed

# Создаём один Console на весь модуль.
# highlight=False — отключает автоподсветку чисел и строк (нам не нужна).
console = Console(highlight=False)


def _format_size(size_bytes: int) -> str:
    """
    Переводит размер из байт в читаемый вид: B, KB, MB.

    Имя начинается с _ — соглашение Python: "эта функция внутренняя,
    не предназначена для использования снаружи этого модуля".
    """
    # Выбираем единицу измерения в зависимости от размера
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        # :.1f — форматирование числа: один знак после запятой. 1536 → "1.5 KB"
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def print_error(message: str) -> None:
    """Выводит сообщение об ошибке красным цветом."""
    # Строки в [] внутри текста — это разметка Rich.
    # [bold red] — жирный красный. [/bold red] — закрывает стиль (как в HTML).
    console.print(f"[bold red]Ошибка:[/bold red] {message}")


def print_warning(message: str) -> None:
    """Выводит предупреждение жёлтым цветом."""
    console.print(f"[yellow]Предупреждение:[/yellow] {message}")


def print_scan_results(result: ScanResult, elapsed: Elapsed | None = None) -> None:
    """
    Выводит результаты сканирования в виде таблицы.

    Аргументы:
        result  — объект ScanResult с файлами и контекстом сканирования.
        elapsed — время сканирования (опционально).
    """
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Файл", style="white")
    table.add_column("Расширение", style="dim")
    table.add_column("Размер", justify="right", style="green")

    for file_path in result.files:
        size = file_path.stat().st_size

        if result.recursive:
            # .relative_to(base_dir) — путь относительно base_dir.
            # Пример: Path("data/input/reports/file.txt").relative_to(Path("data/input"))
            #       → Path("reports/file.txt")
            # Так пользователь видит в какой подпапке находится файл.
            display_name = str(file_path.relative_to(result.scanned_dir))
        else:
            # Обычный режим — только имя файла
            display_name = file_path.name

        table.add_row(display_name, file_path.suffix, _format_size(size))

    console.print(table)
    timing = f"  [dim]{elapsed}[/dim]" if elapsed else ""
    console.print(f"Найдено: [bold]{result.total}[/bold] файл(ов){timing}")


def process_files_with_progress(files: list[Path], output_dir: Path) -> ProcessResult:
    """
    Копирует файлы в output_dir, показывая прогресс-бар Rich.

    Эта функция живёт в output.py, а не в processor.py, потому что
    она отвечает за ВИД операции (прогресс-бар) — это задача слоя вывода.
    Сама логика копирования по-прежнему в processor.py.

    Аргументы:
        files      — список файлов для копирования
        output_dir — папка назначения

    Возвращает:
        ProcessResult — объект с итогами копирования.
    """
    # Импортируем здесь, чтобы не создавать циклический импорт на уровне модуля.
    # processor.py → output.py было бы плохо, но output.py → processor.py — нормально.
    from cli_file_processor.core.processor import process_files

    all_processed: list[Path] = []

    # Progress — контекстный менеджер (with). При выходе очищает строку прогресса.
    # Каждый аргумент — колонка, они выводятся слева направо.
    with Progress(
        SpinnerColumn(),  # анимированный спиннер: ⠋ ⠙ ⠹ ⠸ ...
        TextColumn("[progress.description]{task.description}"),  # текст задачи
        BarColumn(),  # полоса заполнения: ████████░░
        TaskProgressColumn(),  # "3/10"
        TimeElapsedColumn(),  # "0:00:02"
    ) as progress:
        # add_task() регистрирует задачу и возвращает её ID.
        # total= — сколько шагов всего (нужно для вычисления процента).
        task = progress.add_task("Копирование...", total=len(files))

        for file_path in files:
            # update() меняет description на лету — показываем текущий файл.
            progress.update(task, description=f"[cyan]{file_path.name}[/cyan]")
            result = process_files([file_path], output_dir)
            all_processed.extend(result.processed)
            # advance() увеличивает счётчик на 1 — прогресс-бар продвигается.
            progress.advance(task)

    return ProcessResult(processed=all_processed, output_dir=output_dir)


def print_process_results(result: ProcessResult, elapsed: Elapsed | None = None) -> None:
    """Выводит итоги команды process."""
    timing = f"  [dim]{elapsed}[/dim]" if elapsed else ""
    console.print(
        f"\nГотово: скопировано [bold green]{result.total}[/bold green] файл(ов) "
        f"в [cyan]{result.output_dir}[/cyan]{timing}"
    )


def print_dry_run_results(result: ScanResult, output_dir: Path) -> None:
    """
    Выводит предпросмотр команды process в режиме --dry-run.

    Показывает что БЫЛО БЫ сделано без реального копирования.
    """
    # Жёлтый заголовок — сигнал что это не реальное действие
    console.print(
        "\n[bold yellow]Предпросмотр (--dry-run) — файлы НЕ будут скопированы[/bold yellow]\n"
    )

    # Таблица: что → куда
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Файл", style="white")
    table.add_column("Куда будет скопирован", style="dim")

    for file_path in result.files:
        # Строим путь назначения так же как это делает processor.py
        # но файл НЕ копируем
        destination = output_dir / file_path.name
        table.add_row(file_path.name, str(destination))

    console.print(table)
    console.print(
        f"\nИтого: [bold]{result.total}[/bold] файл(ов) будет скопировано в [cyan]{output_dir}[/cyan]"
    )
    console.print("[dim]Запустите без --dry-run чтобы применить изменения.[/dim]")
