"""
Модуль вывода.

Отвечает только за то, КАК данные отображаются в терминале.
cli.py решает ЧТО показать, output.py решает КАК это выглядит.
"""

from pathlib import Path

# Console — главный объект Rich. Через него выводим весь текст.
# Он умеет: цвета, таблицы, прогресс-бары, форматирование.
from rich.console import Console

# track() — оборачивает любой итерируемый объект и показывает прогресс-бар.
# Использование: for item in track(items, description="..."):
from rich.progress import track

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


def print_scan_results(files: list[Path]) -> None:
    """
    Выводит результаты сканирования в виде таблицы.

    Аргументы:
        files — список найденных файлов (объекты Path)
    """
    # Table() — создаём объект таблицы.
    # show_header=True — показывать строку с названиями колонок.
    # header_style — стиль заголовков колонок.
    table = Table(show_header=True, header_style="bold cyan")

    # .add_column() — добавляем колонку.
    # Первый аргумент — название колонки (заголовок).
    # style — стиль текста в этой колонке.
    # no_wrap — не переносить длинный текст на новую строку.
    table.add_column("Файл", style="white", no_wrap=True)
    table.add_column("Расширение", style="dim")
    table.add_column("Размер", justify="right", style="green")

    # Заполняем таблицу строками — по одной на каждый файл.
    for file_path in files:
        # .stat() — возвращает информацию о файле с диска.
        # .st_size — размер файла в байтах.
        size = file_path.stat().st_size

        # .add_row() — добавляем строку. Аргументы соответствуют колонкам по порядку.
        # .name — только имя файла без папок: "data/input/file.txt" → "file.txt"
        # .suffix — расширение файла: "file.txt" → ".txt"
        table.add_row(
            file_path.name,
            file_path.suffix,
            _format_size(size),
        )

    # Выводим таблицу в терминал
    console.print(table)

    # Итоговая строка — количество файлов.
    # [bold] ... [/bold] — жирный текст. Числа выделяем цветом.
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

    # track(iterable, description=) — оборачивает список и рисует прогресс-бар.
    # На каждой итерации цикл получает очередной элемент, как обычный for.
    # Rich сам считает прогресс и обновляет полосу заполнения.
    for file_path in track(files, description="Копирование файлов..."):
        # Копируем по одному файлу за раз — передаём список из одного элемента.
        result = process_files([file_path], output_dir)
        processed.extend(result)   # extend() добавляет все элементы списка в processed

    return processed


def print_process_results(processed: list[Path], output_dir: Path) -> None:
    """Выводит итоги команды process."""
    console.print(
        f"\nГотово: скопировано [bold green]{len(processed)}[/bold green] файл(ов) "
        f"в [cyan]{output_dir}[/cyan]"
    )
