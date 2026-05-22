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


def print_scan_results(files: list[Path], base_dir: Path | None = None) -> None:
    """
    Выводит результаты сканирования в виде таблицы.

    Аргументы:
        files    — список найденных файлов (объекты Path)
        base_dir — если передана, показывает путь относительно этой папки.
                   Нужно для режима --recursive: видно в какой подпапке файл.
    """
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Файл", style="white")
    table.add_column("Расширение", style="dim")
    table.add_column("Размер", justify="right", style="green")

    for file_path in files:
        size = file_path.stat().st_size

        if base_dir is not None:
            # .relative_to(base_dir) — путь относительно base_dir.
            # Пример: Path("data/input/reports/file.txt").relative_to(Path("data/input"))
            #       → Path("reports/file.txt")
            # Так пользователь видит в какой подпапке находится файл.
            display_name = str(file_path.relative_to(base_dir))
        else:
            # Обычный режим — только имя файла
            display_name = file_path.name

        table.add_row(display_name, file_path.suffix, _format_size(size))

    console.print(table)
    console.print(f"Найдено: [bold]{len(files)}[/bold] файл(ов)")


def process_files_with_progress(files: list[Path], output_dir: Path) -> list[Path]:
    """
    Копирует файлы в output_dir, показывая прогресс-бар Rich.

    Эта функция живёт в output.py, а не в processor.py, потому что
    она отвечает за ВИД операции (прогресс-бар) — это задача слоя вывода.
    Сама логика копирования по-прежнему в processor.py.

    Аргументы:
        files      — список файлов для копирования
        output_dir — папка назначения

    Возвращает:
        Список путей к скопированным файлам.
    """
    # Импортируем здесь, чтобы не создавать циклический импорт на уровне модуля.
    # processor.py → output.py было бы плохо, но output.py → processor.py — нормально.
    from cli_file_processor.core.processor import process_files

    processed: list[Path] = []

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
            processed.extend(result)
            # advance() увеличивает счётчик на 1 — прогресс-бар продвигается.
            progress.advance(task)

    return processed


def print_process_results(processed: list[Path], output_dir: Path) -> None:
    """Выводит итоги команды process."""
    console.print(
        f"\nГотово: скопировано [bold green]{len(processed)}[/bold green] файл(ов) "
        f"в [cyan]{output_dir}[/cyan]"
    )


def print_dry_run_results(files: list[Path], output_dir: Path) -> None:
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

    for file_path in files:
        # Строим путь назначения так же как это делает processor.py
        # но файл НЕ копируем
        destination = output_dir / file_path.name
        table.add_row(file_path.name, str(destination))

    console.print(table)
    console.print(
        f"\nИтого: [bold]{len(files)}[/bold] файл(ов) будет скопировано в [cyan]{output_dir}[/cyan]"
    )
    console.print("[dim]Запустите без --dry-run чтобы применить изменения.[/dim]")
