# CLI File Processor

Учебный проект — профессиональный CLI-инструмент для обработки файлов на Python.  
Создан в процессе изучения разработки CLI-приложений с нуля.

---

## Содержание

1. [Что делает проект](#что-делает-проект)
2. [Структура проекта](#структура-проекта)
3. [Установка и запуск](#установка-и-запуск)
4. [Команды](#команды)
5. [Изученные темы](#изученные-темы)
   - [Тема 1 — Структура Python-проекта](#тема-1--структура-python-проекта)
   - [Тема 2 — Точка входа](#тема-2--точка-входа)
   - [Тема 3 — Конфигурация через .env](#тема-3--конфигурация-через-env)
   - [Тема 4 — Логирование](#тема-4--логирование)
   - [Тема 5 — Тестирование с pytest](#тема-5--тестирование-с-pytest)
   - [Тема 6 — Красивый вывод с Rich](#тема-6--красивый-вывод-с-rich)
   - [Тема 7 — Работа с файлами и путями](#тема-7--работа-с-файлами-и-путями)
   - [Тема 8 — Разделение ответственности](#тема-8--разделение-ответственности)
   - [Тема 9 — Версионирование: команда version](#тема-9--версионирование-команда-version)
   - [Тема 10 — Паттерн --dry-run](#тема-10--паттерн---dry-run)
   - [Тема 11 — Линтер и форматтер: Ruff](#тема-11--линтер-и-форматтер-ruff)
   - [Тема 12 — Pre-commit хуки](#тема-12--pre-commit-хуки)
   - [Тема 13 — Рекурсивный поиск: флаг --recursive](#тема-13--рекурсивный-поиск-флаг---recursive)
6. [Зависимости](#зависимости)

---

## Что делает проект

```
cli-file-processor scan    --input-dir data/input --extension .txt
cli-file-processor scan    --input-dir data/input --extension .txt --recursive
cli-file-processor process --input-dir data/input --output-dir data/output --extension .pdf
cli-file-processor process --input-dir data/input --output-dir data/output --dry-run
cli-file-processor version
```

- **scan** — находит файлы с нужным расширением и показывает их в таблице
- **process** — находит файлы и копирует их в папку назначения с прогресс-баром
- **check** — проверяет что CLI работает
- **version** — показывает текущую версию приложения

Оба `scan` и `process` поддерживают флаги `--recursive` (поиск во вложенных папках) и `--dry-run` (предпросмотр без реального действия).

---

## Структура проекта

```
cli_file_processor/
│
├── pyproject.toml              ← паспорт проекта: зависимости, entry point, версия
├── .pre-commit-config.yaml     ← хуки, которые запускаются перед каждым git commit
├── .env                        ← настройки для локальной машины (не в git)
├── .env.example                ← шаблон настроек (в git, для других разработчиков)
│
├── data/
│   ├── input/                  ← входные файлы для обработки
│   └── output/                 ← куда копируются обработанные файлы
│
├── src/
│   └── cli_file_processor/
│       ├── main.py             ← тонкая точка входа (запуск через python -m)
│       ├── cli.py              ← команды CLI: check, version, scan, process
│       ├── config.py           ← чтение настроек из .env + версия приложения
│       ├── logging_config.py   ← настройка уровней логирования
│       ├── output.py           ← Rich: таблицы, цвета, прогресс-бар, dry-run вывод
│       └── core/
│           ├── scanner.py      ← бизнес-логика поиска файлов (glob / rglob)
│           └── processor.py    ← бизнес-логика копирования файлов
│
└── tests/
    ├── test_scanner.py         ← юнит-тесты для scanner.py (11 тестов)
    ├── test_cli.py             ← интеграционные тесты CLI команд (15 тестов)
    └── test_processor.py       ← юнит-тесты для processor.py (6 тестов)
```

---

## Установка и запуск

```bash
# Клонировать проект и перейти в папку
cd cli_file_processor

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate       # Linux / Mac
.venv\Scripts\activate          # Windows

# Установить проект и зависимости
pip install -e .

# Установить зависимости для разработки (pytest, ruff, pre-commit)
pip install -e ".[dev]"

# Установить pre-commit хуки (только один раз на репозиторий)
pre-commit install

# Скопировать шаблон настроек
cp .env.example .env
```

---

## Команды

### `check` — проверка работы

```bash
cli-file-processor check
# Project check: OK
```

### `version` — текущая версия

```bash
cli-file-processor version
# 0.1.0
```

### `scan` — поиск файлов

```bash
# С явными параметрами
cli-file-processor scan --input-dir data/input --extension .txt

# Короткие флаги
cli-file-processor scan -i data/input -e .txt

# Подробный вывод (DEBUG-логи)
cli-file-processor scan -i data/input -e .txt --verbose

# Рекурсивный поиск — включая все вложенные подпапки
cli-file-processor scan -i data/input -e .txt --recursive

# Без параметров — берёт дефолты из .env
cli-file-processor scan
```

Вывод (обычный режим):
```
┏━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┓
┃ Файл      ┃ Расширение ┃ Размер ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━┩
│ file1.txt │ .txt       │ 1.2 KB │
│ file2.txt │ .txt       │ 0.8 KB │
└───────────┴────────────┴────────┘
Найдено: 2 файл(ов)
```

Вывод (режим `--recursive` — видны подпапки):
```
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┓
┃ Файл                 ┃ Расширение ┃ Размер ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━┩
│ file1.txt            │ .txt       │ 1.2 KB │
│ reports/monthly.txt  │ .txt       │ 3.4 KB │
└──────────────────────┴────────────┴────────┘
Найдено: 2 файл(ов)
```

### `process` — копирование файлов

```bash
# Обычное копирование
cli-file-processor process --input-dir data/input --output-dir data/output --extension .txt

# Предпросмотр без реального копирования
cli-file-processor process -i data/input -o data/output -e .txt --dry-run

# Рекурсивный поиск + копирование
cli-file-processor process -i data/input -o data/output -e .txt --recursive
```

Вывод (обычный режим):
```
Копирование файлов... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

Готово: скопировано 2 файл(ов) в data/output
```

Вывод (режим `--dry-run`):
```
Предпросмотр (--dry-run) — файлы НЕ будут скопированы

┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Файл      ┃ Куда будет скопирован          ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ file1.txt │ data/output/file1.txt          │
│ file2.txt │ data/output/file2.txt          │
└───────────┴────────────────────────────────┘

Итого: 2 файл(ов) будет скопировано в data/output
Запустите без --dry-run чтобы применить изменения.
```

### Запуск тестов

```bash
pytest tests/ -v
# 32 passed in 0.38s
```

---

## Изученные темы

---

### Тема 1 — Структура Python-проекта

**Файл:** `pyproject.toml`

Современный стандарт описания Python-проекта (замена `setup.py`).

```toml
[project]
name = "cli-file-processor"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "typer>=0.12.0",
    "python-dotenv>=1.0.0",
    "rich>=13.0.0",
]

# Entry point — говорит pip: "создай команду cli-file-processor в терминале"
# Формат: "имя-команды" = "пакет.модуль:объект"
[project.scripts]
cli-file-processor = "cli_file_processor.cli:app"

# Зависимости только для разработки — не нужны пользователю инструмента
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.4.0",
    "pre-commit>=3.7.0",
]
```

**Концепция src-layout:**

```
src/cli_file_processor/   ← код живёт внутри src/, не в корне
```

Зачем: изолирует код от корня проекта. Без этого Python может случайно
найти твой код напрямую из папки, а не через установленный пакет — тесты
дадут неправильные результаты.

**`pip install -e .`** — установка в "редактируемом" режиме. Изменения в коде
сразу отражаются без переустановки. Флаг `-e` = editable.

**`pip install -e ".[dev]"` — установка с дополнительными зависимостями:**
- `pip install -e .` → только основные зависимости
- `pip install -e ".[dev]"` → основные + зависимости из секции `[dev]`

---

### Тема 2 — Точка входа

**Файл:** `src/cli_file_processor/main.py`

```python
from cli_file_processor.cli import app

if __name__ == "__main__":
    app()
```

**`if __name__ == "__main__"`** — один из самых частых идиомов Python:

```
python main.py         → __name__ == "__main__"  → app() вызывается
python -c "import main" → __name__ == "main"     → app() НЕ вызывается
```

Когда файл запускают напрямую — `__name__` равен `"__main__"`.  
Когда файл импортируют — `__name__` равен имени модуля.

**Зачем тонкая точка входа:** `main.py` не содержит бизнес-логики — только
импортирует и вызывает `app`. Весь код живёт в `cli.py`. Так легче тестировать
и переиспользовать.

---

### Тема 3 — Конфигурация через .env

**Файлы:** `config.py`, `.env`, `.env.example`

**Принцип:** настройки не хардкодятся в коде. Разные окружения (твой компьютер,
сервер, CI) используют разные значения через `.env` файл.

```
.env.example   ← коммитится в git — шаблон для команды
.env           ← НЕ коммитится — реальные значения на твоей машине
```

**Содержимое `.env`:**
```
DEFAULT_INPUT_DIR=data/input
DEFAULT_EXTENSION=.txt
DEFAULT_OUTPUT_DIR=data/output
```

**Как работает config.py:**
```python
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()  # читает .env → кладёт переменные в os.environ

def get_default_input_dir() -> Path:
    # os.getenv("КЛЮЧ", "запасное_значение")
    # Если переменная есть в .env — возвращает её значение
    # Если нет — возвращает "data/input"
    return Path(os.getenv("DEFAULT_INPUT_DIR", "data/input"))
```

**Цепочка приоритетов:**
```
1. Флаг из терминала:   --input-dir /path   (наивысший)
2. Переменная в .env:   DEFAULT_INPUT_DIR=/path
3. Запасное значение:   "data/input" в os.getenv (наименьший)
```

---

### Тема 4 — Логирование

**Файлы:** `logging_config.py`, `core/scanner.py`, `core/processor.py`

**Разница между `print` и `logging`:**

```
print / typer.echo  → для пользователя: результат работы команды
logging             → для разработчика: что происходит внутри программы
```

**Уровни логирования (от тихого к громкому):**

```
DEBUG    — детали выполнения (только при отладке, флаг --verbose)
INFO     — нормальный ход работы
WARNING  — что-то странное, но программа работает
ERROR    — ошибка, операция не выполнена
CRITICAL — критическая ошибка, программа не может продолжать
```

**Настройка:**
```python
import logging

def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    log_format = "%(levelname)-8s %(name)s: %(message)s"

    # force=True — перенастраивает даже если basicConfig уже вызывался.
    # Важно в тестах: каждый тест запускает команду заново в одном процессе.
    logging.basicConfig(level=level, format=log_format, force=True)
```

**Создание логгера в каждом модуле:**
```python
# __name__ — полное имя модуля: "cli_file_processor.core.scanner"
# Соглашение: один логгер на файл, всегда с именем __name__
logger = logging.getLogger(__name__)

# Уровни вызова:
logger.debug("расширение нормализовано: '%s'", extension)  # только с --verbose
logger.info("обработано файлов: %d", len(files))           # в обычном режиме
```

**Почему `%s` а не f-строки в логах:**
```python
# f-строка вычисляется всегда, даже если лог не будет показан
logger.debug(f"файлов: {len(files)}")   # len() вызывается всегда

# % вычисляется только если сообщение реально выводится
logger.debug("файлов: %d", len(files))  # len() вызывается только при DEBUG
```

**Иерархия логгеров:**
```
root logger
└── cli_file_processor
    └── cli_file_processor.core
        ├── cli_file_processor.core.scanner
        └── cli_file_processor.core.processor
```

Каждый логгер передаёт сообщение вверх к root, который решает — показывать или нет.

---

### Тема 5 — Тестирование с pytest

**Файлы:** `tests/test_scanner.py`, `tests/test_cli.py`, `tests/test_processor.py`

**Зачем тесты:** изменил код → за секунду знаешь сломал ли что-то.

**Два вида тестов в проекте:**

| Вид | Что проверяет | Пример |
|-----|---------------|--------|
| Юнит-тест | Одну функцию в изоляции | `normalize_extension("PDF") == ".pdf"` |
| Интеграционный | Всю цепочку от CLI до результата | `runner.invoke(app, ["scan", ...])` |

**Базовый синтаксис:**
```python
# Функция должна начинаться с test_
def test_normalize_extension_lowercases():
    # assert — если выражение False, тест падает с ошибкой
    assert normalize_extension("PDF") == ".pdf"
```

**Встроенная fixture `tmp_path`:**
```python
# pytest автоматически создаёт временную папку и передаёт в тест
# После теста папка удаляется. Реальные файлы не трогаем.
def test_scan_finds_files(tmp_path: Path):
    (tmp_path / "file.txt").touch()   # создаём пустой файл
    result = scan_files(input_dir=tmp_path, extension=".txt")
    assert len(result) == 1
```

**`CliRunner` — симуляция терминала:**
```python
from typer.testing import CliRunner
from cli_file_processor.cli import app

runner = CliRunner()

def test_scan_fails_when_dir_not_found():
    # Запускаем CLI команду как если бы написали в терминале
    result = runner.invoke(app, ["scan", "--input-dir", "/nonexistent"])

    # result.exit_code — код завершения (0 = успех, 1+ = ошибка)
    assert result.exit_code != 0
    # result.output — весь вывод команды
    assert "не найдена" in result.output
```

**Именование тестов:**
```
test_<что_проверяем>_<при_каком_условии>

test_normalize_extension_adds_dot           ← добавляет точку
test_scan_files_returns_empty_when_no_match ← пустой список если нет совпадений
test_process_fails_when_input_missing       ← ошибка если папка не найдена
```

**Итого тестов в проекте: 32**
- `test_scanner.py` — 11 тестов (normalize_extension, scan_files)
- `test_cli.py` — 15 тестов (check, scan, process команды)
- `test_processor.py` — 6 тестов (process_files)

---

### Тема 6 — Красивый вывод с Rich

**Файл:** `output.py`

**Console — основной объект для вывода:**
```python
from rich.console import Console
console = Console(highlight=False)

console.print("[bold red]Ошибка:[/bold red] папка не найдена")
console.print("[yellow]Предупреждение:[/yellow] файлы не найдены")
console.print(f"Найдено: [bold]{len(files)}[/bold] файл(ов)")
```

**Разметка Rich** работает как HTML-теги:
```
[bold]текст[/bold]          — жирный
[red]текст[/red]            — красный
[bold red]текст[/bold red]  — жирный красный
[dim]текст[/dim]            — приглушённый
[cyan]текст[/cyan]          — голубой
```

**Таблица:**
```python
from rich.table import Table

table = Table(show_header=True, header_style="bold cyan")
table.add_column("Файл",       style="white")
table.add_column("Расширение", style="dim")
table.add_column("Размер",     justify="right", style="green")

for file_path in files:
    table.add_row(
        file_path.name,
        file_path.suffix,
        _format_size(file_path.stat().st_size),
    )

console.print(table)
```

**Прогресс-бар — одна строка кода:**
```python
from rich.progress import track

# Оборачиваем любой список в track() — получаем прогресс-бар
for file_path in track(files, description="Копирование файлов..."):
    process(file_path)
```

**Важно:** Rich в нетерминальном режиме (тесты, пайпы) убирает цвета
но сохраняет текст. Поэтому `assert "report.txt" in result.output` работает.

---

### Тема 7 — Работа с файлами и путями

**Файлы:** `core/scanner.py`, `core/processor.py`

**`pathlib.Path` — современная работа с путями:**

```python
from pathlib import Path

path = Path("data/input/file.txt")

path.exists()          # True если путь существует
path.is_dir()          # True если это папка
path.is_file()         # True если это файл
path.name              # "file.txt"        — только имя файла
path.suffix            # ".txt"            — расширение
path.stem              # "file"            — имя без расширения
path.parent            # Path("data/input") — родительская папка
path.stat().st_size    # размер файла в байтах

# Оператор / создаёт вложенный путь:
output = Path("data/output") / "file.txt"   # Path("data/output/file.txt")

# Создать папку (с родительскими, без ошибки если существует):
path.mkdir(parents=True, exist_ok=True)

# Создать пустой файл:
path.touch()

# Записать текст в файл:
path.write_text("содержимое")

# Прочитать текст из файла:
content = path.read_text()

# Поиск файлов по паттерну:
files = list(Path("data/input").glob("*.txt"))   # только в этой папке
files = list(Path("data/input").rglob("*.txt"))  # включая подпапки
```

**`shutil` — операции с файлами:**

```python
import shutil

shutil.copy(src, dst)   # копирует содержимое файла
shutil.copy2(src, dst)  # копирует содержимое + метаданные (дата, права)
shutil.move(src, dst)   # перемещает файл
shutil.rmtree(path)     # удаляет папку со всем содержимым
```

**`glob` vs `rglob`:**
```python
# glob — ищет только в указанной папке
list(folder.glob("*.txt"))     # ["folder/a.txt", "folder/b.txt"]

# rglob — рекурсивно, включая все подпапки
list(folder.rglob("*.txt"))    # ["folder/a.txt", "folder/sub/c.txt"]
```

---

### Тема 8 — Разделение ответственности

**Принцип:** каждый модуль отвечает только за одну вещь. Это делает код понятнее,
легче тестировать и изменять по частям.

**Архитектура проекта:**

```
cli.py          ← ТОЛЬКО: принять параметры, провалидировать, вызвать нужные функции
config.py       ← ТОЛЬКО: читать настройки из .env и хранить версию
logging_config  ← ТОЛЬКО: настроить уровень логирования
output.py       ← ТОЛЬКО: решать как данные выглядят (Rich, таблицы, цвета)
scanner.py      ← ТОЛЬКО: находить файлы по расширению
processor.py    ← ТОЛЬКО: копировать файлы
```

**Как это выглядит в коде:**

```python
# cli.py — команда scan
def scan(input_dir, extension, verbose, recursive):
    setup_logging(verbose)               # → logging_config.py
    input_dir = get_default_input_dir()  # → config.py
    files = scan_files(input_dir, ext, recursive)  # → scanner.py (бизнес-логика)
    print_scan_results(files)            # → output.py   (отображение)
```

CLI не знает КАК ищутся файлы и КАК они отображаются — он только координирует.

**Зачем это важно:**
- Хочешь изменить внешний вид таблицы → меняешь только `output.py`
- Хочешь искать файлы рекурсивно → меняешь только `scanner.py`
- Ни в том, ни в другом случае `cli.py` не трогаешь

---

### Тема 9 — Версионирование: команда version

**Файлы:** `config.py`, `cli.py`

**Зачем нужна версия в CLI-инструменте:**  
Версия позволяет пользователю и системам CI понять, какая именно сборка
установлена. Стандартный паттерн: `tool --version` или `tool version`.

**Где хранить версию:**

В этом проекте версия хранится в `config.py` — в одном месте, откуда её
может взять любой модуль:

```python
# config.py
def get_app_version() -> str:
    return "0.1.0"
```

Альтернативный подход (продвинутый) — читать версию из `pyproject.toml` через
`importlib.metadata`, чтобы она была в одном месте:

```python
from importlib.metadata import version
def get_app_version() -> str:
    return version("cli-file-processor")
```

**Команда в CLI:**

```python
# cli.py
@app.command()
def version() -> None:
    """
    Показывает версию приложения.
    """
    typer.echo(get_app_version())
```

**Запуск:**
```bash
cli-file-processor version
# 0.1.0
```

---

### Тема 10 — Паттерн --dry-run

**Файлы:** `cli.py`, `output.py`

**Что такое dry-run:**  
"Симуляция" — показывает что произойдёт, но ничего не делает. Стандартный паттерн
для команд, которые изменяют файлы, базы данных или отправляют запросы. Даёт
пользователю возможность проверить перед тем как применить.

**Пример из реальных инструментов:**
```bash
rsync --dry-run ...     # синхронизация файлов — показывает без копирования
ansible-playbook --check  # применение конфигураций — симуляция
terraform plan          # изменения инфраструктуры — предпросмотр
```

**Как реализован в проекте:**

```python
# cli.py — флаг --dry-run в команде process
dry_run: bool = typer.Option(
    False,
    "--dry-run",
    help="Показать что будет скопировано без реального копирования.",
)

# В теле команды — одна развилка:
if dry_run:
    print_dry_run_results(files, output_dir)   # только показываем
else:
    processed = process_files_with_progress(files, output_dir)  # реально копируем
    print_process_results(processed, output_dir)
```

**Вывод dry-run в `output.py`:**

```python
def print_dry_run_results(files: list[Path], output_dir: Path) -> None:
    console.print(
        "\n[bold yellow]Предпросмотр (--dry-run) — файлы НЕ будут скопированы[/bold yellow]\n"
    )

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Файл", style="white")
    table.add_column("Куда будет скопирован", style="dim")

    for file_path in files:
        destination = output_dir / file_path.name  # строим путь — но НЕ копируем
        table.add_row(file_path.name, str(destination))

    console.print(table)
    console.print("[dim]Запустите без --dry-run чтобы применить изменения.[/dim]")
```

**Ключевое:** `print_dry_run_results` использует ту же логику построения пути
(`output_dir / file_path.name`), что и настоящее копирование в `processor.py`.
Это гарантирует что предпросмотр точно соответствует реальному поведению.

---

### Тема 11 — Линтер и форматтер: Ruff

**Файл:** `pyproject.toml` (секция `[tool.ruff]`)

**Что такое линтер и форматтер:**

```
Линтер    — проверяет код на ошибки и плохой стиль, но не меняет файлы
Форматтер — автоматически переформатирует код в единый стиль
```

**Ruff** — современный инструмент на Rust, который объединяет оба: заменяет
`flake8` (линтер), `isort` (сортировка импортов), `pyupgrade` (современный синтаксис)
и `black` (форматтер). Работает в 10-100 раз быстрее аналогов.

**Конфигурация в `pyproject.toml`:**

```toml
[tool.ruff]
line-length = 100       # максимальная длина строки (PEP8 = 79, на практике 88-100)
src = ["src", "tests"]  # папки с кодом — Ruff правильно сортирует импорты

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP"]
# E, W — ошибки и предупреждения стиля (pycodestyle)
# F     — логические ошибки: неиспользуемые импорты, переменные (pyflakes)
# I     — порядок импортов (isort)
# UP    — предложения по современному синтаксису Python (pyupgrade)
ignore = ["E501"]       # E501 = длина строки (контролируем сами через line-length)

[tool.ruff.lint.isort]
known-first-party = ["cli_file_processor"]   # свои модули — отдельная группа импортов

[tool.ruff.format]
quote-style = "double"          # строки в двойных кавычках
indent-style = "space"          # отступы пробелами (не табами)
skip-magic-trailing-comma = false  # не убирать trailing comma если она поставлена намеренно
```

**Команды:**

```bash
# Проверка — только показывает ошибки, ничего не меняет
ruff check src/

# Проверка + автоисправление (безопасных ошибок)
ruff check src/ --fix

# Форматирование — переформатирует файлы
ruff format src/

# Предпросмотр форматирования — показывает что изменится, не меняет
ruff format src/ --check
```

**Что ruff format делает с кодом — примеры:**

```python
# До форматирования
app = typer.Typer(
    help="CLI File Processor — инструмент для обработки файлов."
)

# После форматирования (если строка вмещается в line-length)
app = typer.Typer(help="CLI File Processor — инструмент для обработки файлов.")
```

```python
# До — длинная строка
console.print("\n[bold yellow]Предпросмотр (--dry-run) — файлы НЕ будут скопированы[/bold yellow]\n")

# После — разбита на строки чтобы не превышать line-length
console.print(
    "\n[bold yellow]Предпросмотр (--dry-run) — файлы НЕ будут скопированы[/bold yellow]\n"
)
```

**Группы импортов, которые создаёт isort (I):**

```python
# 1. Стандартная библиотека Python
import logging
from pathlib import Path

# 2. Сторонние библиотеки (установленные через pip)
import typer
from rich.console import Console

# 3. Свои модули проекта (known-first-party)
from cli_file_processor.config import get_default_input_dir
```

---

### Тема 12 — Pre-commit хуки

**Файл:** `.pre-commit-config.yaml`

**Что такое pre-commit хуки:**  
Git позволяет запускать скрипты перед коммитом. `pre-commit` — инструмент
для управления такими скриптами. Если хук падает — коммит не создаётся.
Это гарантирует что в репозиторий не попадёт плохо оформленный код.

**Конфигурация `.pre-commit-config.yaml`:**

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0        # конкретная версия — воспроизводимость
    hooks:
      - id: ruff
        args: [--fix]  # ruff check --fix: проверяет и исправляет автоматически
      - id: ruff-format # ruff format: форматирует код
```

**Установка и использование:**

```bash
# Установить pre-commit (один раз для проекта)
pip install pre-commit

# Зарегистрировать хуки в репозитории (один раз, после clone)
pre-commit install
# → pre-commit installed at .git/hooks/pre-commit

# Теперь при каждом git commit хуки запускаются автоматически:
git commit -m "my changes"
# ruff.....................................................................Passed
# ruff-format..............................................................Passed
# [main abc1234] my changes
```

**Что происходит если хук находит проблему:**

```bash
git commit -m "bad code"
# ruff.....................................................................Failed
# - hook id: ruff
# - exit code: 1
# src/cli_file_processor/cli.py:5:1: F401 'os' imported but unused
```

Коммит не создаётся. Нужно исправить ошибку, снова `git add` и `git commit`.

**Цикл работы с pre-commit:**

```
Пишешь код → git add → git commit
                              ↓
                        pre-commit запускает ruff check --fix
                              ↓ (если нашёл и исправил)
                        Файлы изменены → коммит отменён
                              ↓
                        git add (снова) → git commit
                              ↓
                        ruff check: Passed
                        ruff-format: Passed
                              ↓
                        Коммит создан ✓
```

**При первом коммите** pre-commit скачивает и устанавливает окружение с ruff.
Это занимает ~30 секунд. При следующих коммитах — мгновенно (окружение кешируется).

**Запуск хуков вручную (без коммита):**
```bash
pre-commit run --all-files   # проверить все файлы
pre-commit run ruff          # запустить только один хук
```

---

### Тема 13 — Рекурсивный поиск: флаг --recursive

**Файлы:** `cli.py`, `core/scanner.py`, `output.py`

**Задача:** по умолчанию `scan` и `process` ищут файлы только в указанной папке.
Флаг `--recursive` включает поиск во всех вложенных подпапках.

**Пример структуры:**
```
data/input/
├── report.txt          ← найдёт и без --recursive
├── notes.txt           ← найдёт и без --recursive
└── reports/
    └── monthly.txt     ← найдёт ТОЛЬКО с --recursive
```

**Изменения в `scanner.py`:**

```python
def scan_files(input_dir: Path, extension: str, recursive: bool = False) -> list[Path]:
    normalized_extension = normalize_extension(extension)

    if recursive:
        # rglob("*.txt") — рекурсивный поиск: текущая папка + все вложенные.
        # "r" в rglob означает recursive.
        files = list(input_dir.rglob(f"*{normalized_extension}"))
    else:
        # glob("*.txt") — поиск только в указанной папке.
        files = list(input_dir.glob(f"*{normalized_extension}"))

    return files
```

**`glob` vs `rglob` — наглядное сравнение:**

```python
# Структура: data/input/a.txt, data/input/sub/b.txt

list(Path("data/input").glob("*.txt"))
# → [Path("data/input/a.txt")]           # только корень

list(Path("data/input").rglob("*.txt"))
# → [Path("data/input/a.txt"),
#    Path("data/input/sub/b.txt")]        # корень + все подпапки
```

**Изменения в `output.py` — относительные пути:**

В режиме `--recursive` важно показать пользователю в какой именно подпапке
находится файл. Для этого `print_scan_results` принимает аргумент `base_dir`:

```python
def print_scan_results(files: list[Path], base_dir: Path | None = None) -> None:
    for file_path in files:
        if base_dir is not None:
            # .relative_to(base_dir) — делает путь относительным
            # Path("data/input/reports/monthly.txt").relative_to(Path("data/input"))
            # → Path("reports/monthly.txt")
            display_name = str(file_path.relative_to(base_dir))
        else:
            display_name = file_path.name  # просто "monthly.txt"

        table.add_row(display_name, file_path.suffix, _format_size(size))
```

**Изменения в `cli.py` — как передаётся `base_dir`:**

```python
# Если режим --recursive — передаём input_dir, чтобы таблица показывала
# относительные пути. Если нет — передаём None (обычный вывод).
print_scan_results(files, base_dir=input_dir if recursive else None)
```

**Флаг добавлен в обе команды — `scan` и `process`:**

```python
recursive: bool = typer.Option(
    False,
    "--recursive",
    "-r",
    help="Искать файлы во всех вложенных подпапках.",
)
```

Короткий флаг `-r` позволяет писать компактно: `cli-file-processor scan -i data/input -e .txt -r`

---

## Зависимости

| Библиотека | Назначение | Тип |
|------------|-----------|-----|
| `typer` | Создание CLI команд, парсинг аргументов | основная |
| `python-dotenv` | Чтение `.env` файлов | основная |
| `rich` | Цвета, таблицы, прогресс-бар в терминале | основная |
| `pytest` | Запуск и организация тестов | dev |
| `ruff` | Линтер + форматтер кода | dev |
| `pre-commit` | Автозапуск проверок перед git commit | dev |

**Стандартные библиотеки Python (не нужно устанавливать):**

| Библиотека | Что используем |
|------------|---------------|
| `pathlib` | `Path` — работа с путями файловой системы |
| `logging` | Уровни логирования, `basicConfig`, `getLogger` |
| `shutil` | `copy2` — копирование файлов с метаданными |
| `os` | `os.getenv` — чтение переменных окружения |
