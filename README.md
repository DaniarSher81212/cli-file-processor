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
   - [Тема 14 — Git: базовые команды и рабочий процесс](#тема-14--git-базовые-команды-и-рабочий-процесс)
   - [Тема 15 — GitHub CLI (gh)](#тема-15--github-cli-gh)
   - [Тема 16 — Создание репозитория и remote](#тема-16--создание-репозитория-и-remote)
   - [Тема 17 — Ветки: feature-branch workflow](#тема-17--ветки-feature-branch-workflow)
   - [Тема 18 — Pull Request](#тема-18--pull-request)
   - [Тема 19 — GitHub Actions CI](#тема-19--github-actions-ci)
   - [Тема 20 — Жизненный цикл CLI-команды](#тема-20--жизненный-цикл-cli-команды)
   - [Тема 21 — Exit codes](#тема-21--exit-codes)
   - [Тема 22 — Аннотации типов (Type Hints)](#тема-22--аннотации-типов-type-hints)
   - [Тема 23 — Merge conflicts](#тема-23--merge-conflicts)
   - [Тема 24 — Conventional Commits](#тема-24--conventional-commits)
   - [Тема 25 — Полный engineering lifecycle](#тема-25--полный-engineering-lifecycle)
   - [Тема 26 — Coverage: покрытие кода тестами](#тема-26--coverage-покрытие-кода-тестами)
   - [Тема 27 — Mypy: статическая проверка типов](#тема-27--mypy-статическая-проверка-типов)
   - [Тема 28 — Docker: контейнеризация](#тема-28--docker-контейнеризация)
   - [Тема 29 — Makefile: стандартные команды проекта](#тема-29--makefile-стандартные-команды-проекта)
   - [Тема 30 — Pydantic Settings: типизированная конфигурация](#тема-30--pydantic-settings-типизированная-конфигурация)
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

### Тема 14 — Git: базовые команды и рабочий процесс

**Git** — система контроля версий. Хранит всю историю изменений проекта, позволяет
откатиться к любому состоянию, работать в параллельных ветках и объединять изменения.

**Инициализация репозитория:**

```bash
git init          # создать новый репозиторий в текущей папке
git clone <url>   # скачать существующий репозиторий с GitHub
```

**Просмотр состояния:**

```bash
git status        # показать изменённые и неотслеживаемые файлы
git log           # история коммитов
git log --oneline # история в сжатом виде — по одной строке на коммит
git diff          # что изменилось в файлах (ещё не добавлено в staging)
git diff --staged # что добавлено в staging и войдёт в следующий коммит
```

**Создание коммита — три шага:**

```bash
# Шаг 1: посмотреть что изменилось
git status

# Шаг 2: добавить нужные файлы в staging (подготовить к коммиту)
git add src/cli_file_processor/cli.py   # конкретный файл
git add src/                            # всю папку
git add -p                              # интерактивно — по кускам изменений

# Шаг 3: зафиксировать изменения
git commit -m "add --recursive flag to scan command"
```

**Staging area (индекс)** — промежуточная зона между рабочей папкой и коммитом.
Позволяет выбрать точно что войдёт в коммит, даже если изменений много.

```
Рабочая папка  →  git add  →  Staging area  →  git commit  →  История
```

**Отмена изменений:**

```bash
git restore <file>          # отменить изменения в файле (до git add)
git restore --staged <file> # убрать файл из staging (после git add)
git revert <commit-hash>    # создать новый коммит, отменяющий старый
```

**`.gitignore`** — файл со списком того, что Git должен игнорировать:

```
.venv/          # виртуальное окружение — у каждого своё
__pycache__/    # кеш Python — генерируется автоматически
.env            # секреты — никогда не коммитить
data/output/    # результаты работы — не код
*.pyc           # скомпилированные файлы Python
```

**Хорошие практики коммитов:**

```bash
# Плохо — непонятно что сделано
git commit -m "fix"
git commit -m "changes"

# Хорошо — ясно что и зачем
git commit -m "add --recursive flag to scan command"
git commit -m "fix ruff format errors in tests/"
git commit -m "update README with GitHub Actions topics"
```

Формат: глагол в настоящем времени + что сделано. Коммит = одно логическое изменение.

---

### Тема 15 — GitHub CLI (gh)

**`gh`** — официальный CLI от GitHub. Позволяет работать с репозиториями,
PR, Issues и Actions прямо из терминала без браузера.

**Установка:**

```bash
# Ubuntu / Debian
sudo apt install gh

# macOS
brew install gh

# Проверить установку
gh --version
```

**Авторизация:**

```bash
gh auth login
```

Команда задаёт вопросы интерактивно:

```
? What account do you want to log into?   → GitHub.com
? What is your preferred protocol?         → SSH (или HTTPS)
? Upload your SSH public key?              → выбрать ключ из ~/.ssh/
? Title for your SSH key:                  → Enter (оставить по умолчанию)
? How would you like to authenticate?      → Login with a web browser
```

При выборе браузера — показывает одноразовый код (например `65ED-50CF`),
открывает `github.com/login/device`, ты вводишь код и подтверждаешь.

**Проверить статус авторизации:**

```bash
gh auth status
# github.com
#   ✓ Logged in to github.com account DaniarSher81212
#   - Git operations protocol: SSH
#   - Token scopes: 'gist', 'read:org', 'repo', 'workflow'
```

**Основные команды `gh`:**

```bash
# Репозитории
gh repo create        # создать новый репозиторий
gh repo clone <repo>  # клонировать репозиторий
gh repo view          # открыть репозиторий в браузере

# Pull Requests
gh pr create          # создать PR
gh pr list            # список открытых PR
gh pr view            # посмотреть PR
gh pr merge           # смержить PR

# GitHub Actions
gh run list           # список последних запусков CI
gh run watch          # следить за текущим запуском в реальном времени
gh run view --log-failed  # показать логи упавшего запуска

# Issues
gh issue create       # создать задачу
gh issue list         # список задач
```

---

### Тема 16 — Создание репозитория и remote

**Создание репозитория через `gh`:**

```bash
# Создать публичный репозиторий из текущей папки,
# добавить remote и сразу запушить текущую ветку
gh repo create cli-file-processor --public --source=. --remote=origin --push
```

Флаги:
- `--public` — публичный репозиторий (виден всем)
- `--source=.` — использовать текущую папку как источник
- `--remote=origin` — добавить remote с именем `origin`
- `--push` — сразу запушить текущую ветку

**Что такое remote:**

Remote — это ссылка на репозиторий на сервере (GitHub, GitLab, Bitbucket).
Локальный git знает куда пушить и откуда тянуть изменения.

```bash
git remote -v              # показать все remotes
git remote add origin <url> # добавить remote вручную
git remote remove origin    # удалить remote
```

Имя `origin` — соглашение. Технически можно назвать как угодно,
но `origin` понимают все.

**Push и pull:**

```bash
# Первый push — устанавливает связь ветки с remote
git push -u origin main
# -u = --set-upstream: запоминает что local main → remote origin/main

# Следующие push'и — уже без флагов
git push

# Забрать изменения с GitHub
git pull
git pull origin main  # явно указать remote и ветку
```

**Запушить конкретную ветку:**

```bash
git push origin feature/recursive    # запушить ветку на GitHub
git push origin --delete my-branch  # удалить ветку на GitHub
```

---

### Тема 17 — Ветки: feature-branch workflow

**Ветка** — независимая линия разработки. В `main` хранится стабильный код,
новые фичи делаются в отдельных ветках.

**Зачем ветки:**
```
main             ← всегда рабочий, стабильный код
├── feature/recursive   ← разработка новой фичи
├── fix/scanner-bug     ← исправление бага
└── docs/readme-update  ← обновление документации
```

Пока делаешь фичу в своей ветке — `main` не трогается. Сломал что-то?
Удалил ветку — `main` цел.

**Создание и переключение:**

```bash
# Создать ветку и сразу переключиться на неё
git checkout -b feature/recursive

# Современный синтаксис (git 2.23+)
git switch -c feature/recursive

# Просто переключиться на существующую ветку
git checkout main
git switch main

# Список всех веток
git branch          # локальные
git branch -r       # remote-ветки
git branch -a       # все
```

**Типичный цикл работы:**

```bash
# 1. Создать ветку от актуального main
git switch main
git pull
git switch -c feature/my-feature

# 2. Работать — коммитить по мере прогресса
git add ...
git commit -m "..."

# 3. Запушить ветку на GitHub
git push -u origin feature/my-feature

# 4. Открыть PR (см. следующую тему)

# 5. После merge — удалить ветку локально
git branch -d feature/my-feature
```

**Соглашения по именованию веток:**

```
feature/<название>   — новая функциональность:  feature/recursive-search
fix/<название>       — исправление бага:         fix/scanner-empty-dir
docs/<название>      — документация:             docs/readme-github
refactor/<название>  — рефакторинг:              refactor/output-module
```

---

### Тема 18 — Pull Request

**Pull Request (PR)** — запрос на слияние ветки в `main`. Это место для
code review: другие разработчики смотрят код, оставляют комментарии,
CI прогоняет тесты. Только после одобрения — merge.

**Создание PR через `gh`:**

```bash
gh pr create \
  --title "Add --recursive flag to scan and process" \
  --body "..." \
  --base main \
  --head feature/recursive
```

Флаги:
- `--title` — заголовок PR (кратко, до 70 символов)
- `--body` — описание: что сделано, как тестировать
- `--base` — куда мержим (обычно `main`)
- `--head` — что мержим (твоя ветка)

**Просмотр PR:**

```bash
gh pr list               # список открытых PR
gh pr view 1             # посмотреть PR #1
gh pr view 1 --web       # открыть PR #1 в браузере
gh pr checks 1           # статус CI-проверок
```

**Merge PR:**

```bash
# Слить PR и удалить ветку на GitHub
gh pr merge 1 --merge --delete-branch

# Виды merge:
gh pr merge 1 --merge   # обычный merge commit
gh pr merge 1 --squash  # все коммиты ветки → один коммит
gh pr merge 1 --rebase  # rebase поверх main
```

**`--delete-branch`** — удаляет ветку на GitHub после merge.
Хорошая практика: смержил → почистил. Старые ветки захламляют репозиторий.

**Хорошее описание PR** содержит:
```markdown
## Summary
- Что сделано (буллеты)

## Test plan
- [ ] pytest проходит
- [ ] Проверил вручную: cli-file-processor scan --recursive
- [ ] CI зелёный
```

**Жизненный цикл PR:**

```
git push origin feature/my-feature
          ↓
gh pr create
          ↓
CI запускается автоматически (GitHub Actions)
          ↓
Code review (комментарии, правки)
          ↓
CI зелёный + одобрение
          ↓
gh pr merge --delete-branch
          ↓
Код в main ✓
```

---

### Тема 19 — GitHub Actions CI

**Файл:** `.github/workflows/ci.yml`

**GitHub Actions** — встроенная система автоматизации GitHub. Запускает
команды на виртуальных машинах в ответ на события в репозитории.

**Полный разбор файла `ci.yml`:**

```yaml
name: CI   # имя workflow — отображается во вкладке Actions на GitHub

# Триггеры — когда запускать workflow
on:
  push:
    branches: [main, "feature/**"]   # при push в main или любую feature-ветку
  pull_request:
    branches: [main]                 # при открытии или обновлении PR в main

jobs:
  test:                        # имя job (может быть несколько jobs)
    runs-on: ubuntu-latest     # тип виртуальной машины
    env:
      FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true  # использовать Node.js 24

    steps:
      # actions/checkout — скачивает код репозитория на виртуальную машину
      # без этого шага машина не знает о твоём коде
      - name: Checkout code
        uses: actions/checkout@v4

      # actions/setup-python — устанавливает нужную версию Python
      # на ubuntu-latest Python может быть другой версии
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # run: — произвольная bash-команда
      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Ruff lint
        run: ruff check src/ tests/

      - name: Ruff format check
        run: ruff format --check src/ tests/

      - name: Run tests
        run: pytest tests/ -v
```

**Просмотр результатов через `gh`:**

```bash
# Список последних запусков
gh run list
# STATUS  TITLE                    BRANCH            EVENT  ID
# ✓       add CI workflow          feature/recursive  push   123456

# Следить за запуском в реальном времени
gh run watch 123456

# Посмотреть что упало (только логи упавших шагов)
gh run view 123456 --log-failed

# Полный лог всего запуска
gh run view 123456 --log
```

**Что видит CI в упавшем шаге:**

```
test  Ruff format check  Would reformat: tests/test_cli.py
test  Ruff format check  2 files would be reformatted
test  Ruff format check  Error: Process completed with exit code 1.
```

Это значит: файлы не отформатированы. Запускаешь `ruff format tests/`,
коммитишь, пушишь — CI перезапускается.

**Чему учит CI:**

- Код проверяется на чистой машине — нет "у меня работает, у тебя нет"
- Каждый push автоматически проходит через lint + format + tests
- PR нельзя смержить пока CI красный — защита ветки `main`
- Логи доступны всей команде — любой видит что упало и почему

**Матрица версий (продвинутое):**

Можно проверять на нескольких версиях Python одновременно:

```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

Запустит три параллельных job — один на каждую версию.

---

### Тема 20 — Жизненный цикл CLI-команды

Что происходит под капотом когда ты пишешь в терминале:

```bash
cli-file-processor scan -i data/input -e .txt
```

**Полный путь от команды до результата:**

```
1. Shell получает строку "cli-file-processor scan -i data/input -e .txt"
       ↓
2. Shell ищет "cli-file-processor" в PATH
   (~/.venv/bin/, /usr/local/bin/, и т.д.)
       ↓
3. Находит wrapper-скрипт, созданный pip при `pip install -e .`
   Скрипт содержит: from cli_file_processor.cli import app; app()
       ↓
4. Python запускает интерпретатор, импортирует пакет
       ↓
5. Typer получает sys.argv = ["scan", "-i", "data/input", "-e", ".txt"]
   Парсит аргументы: input_dir=Path("data/input"), extension=".txt"
       ↓
6. Typer вызывает функцию scan(input_dir=..., extension=..., ...)
       ↓
7. scan() вызывает setup_logging()      → logging_config.py
8. scan() вызывает get_default_input_dir() → config.py (если нужно)
9. scan() вызывает scan_files()         → core/scanner.py
   scanner.py вызывает normalize_extension()
   scanner.py вызывает Path.glob("*.txt")
       ↓
10. scan() вызывает print_scan_results() → output.py
    output.py строит Rich Table
    output.py вызывает console.print(table)
       ↓
11. Rich отрисовывает таблицу в stdout
       ↓
12. Процесс завершается с exit code 0
```

**Где создаётся wrapper-скрипт:**

```toml
# pyproject.toml
[project.scripts]
cli-file-processor = "cli_file_processor.cli:app"
#  ↑                    ↑                    ↑
#  имя команды          модуль               объект Typer
```

После `pip install -e .` pip создаёт файл `.venv/bin/cli-file-processor` —
это Python-скрипт, который импортирует `app` и вызывает его.

**Как убедиться:**

```bash
which cli-file-processor
# /home/dan/dev/projects/python/cli_file_processor/.venv/bin/cli-file-processor

cat $(which cli-file-processor)
# #!/path/to/python
# from cli_file_processor.cli import app
# app()
```

---

### Тема 21 — Exit codes

**Exit code** — число, которое программа возвращает при завершении.
Это язык общения между программами: `0` всегда означает успех, всё остальное — ошибку.

**Стандартные значения:**

| Код | Значение |
|-----|----------|
| `0` | Успех — всё прошло нормально |
| `1` | Общая ошибка — что-то пошло не так |
| `2` | Неверные аргументы — пользователь передал неправильные параметры |

**Как проверить exit code в терминале:**

```bash
cli-file-processor scan -i data/input -e .txt
echo $?   # → 0  (успех)

cli-file-processor scan -i /nonexistent -e .txt
echo $?   # → 1  (ошибка: папка не найдена)
```

**Как Typer возвращает ошибку:**

```python
# cli.py
if not input_dir.exists():
    print_error(f"папка не найдена: {input_dir}")
    raise typer.Exit(code=1)   # ← завершает программу с кодом 1
```

`raise typer.Exit(code=1)` — не исключение в обычном смысле. Typer его перехватывает
и завершает процесс с нужным кодом. Пользователь не видит traceback.

**Почему exit code важен:**

```bash
# Скрипты используют exit code для принятия решений
cli-file-processor scan -i data/input -e .txt && echo "Нашли файлы!"
#                                               ↑
#                  && выполняется ТОЛЬКО если exit code = 0

# CI делает то же самое:
pytest tests/ && ruff check src/
# если pytest упал (exit code != 0) — ruff не запустится
```

**Как pytest использует exit code:**

| Код | Значение |
|-----|----------|
| `0` | Все тесты прошли |
| `1` | Некоторые тесты упали |
| `2` | Прерван пользователем (Ctrl+C) |
| `5` | Тестов не найдено |

GitHub Actions проверяет exit code каждого шага. Если код не `0` — шаг упал,
весь job помечается как FAILED.

---

### Тема 22 — Аннотации типов (Type Hints)

**Type hints** — подсказки для IDE, линтеров и разработчиков о том, какого типа
значения принимает и возвращает функция. Python их не проверяет во время выполнения,
но они дают огромную пользу при разработке.

**Базовый синтаксис:**

```python
# Аргумент: тип указывается после двоеточия
# Возвращаемое значение: тип указывается после ->

def normalize_extension(extension: str) -> str:
    ...

def scan_files(input_dir: Path, extension: str, recursive: bool = False) -> list[Path]:
    ...

def setup_logging(verbose: bool = False) -> None:
    ...
```

**Типы из этого проекта:**

```python
str           # строка: "txt", ".pdf"
bool          # булево: True / False
int           # целое число: 42
Path          # объект pathlib.Path
list[Path]    # список объектов Path
Path | None   # либо Path, либо None (не передали аргумент)
-> None       # функция ничего не возвращает
-> str        # функция возвращает строку
-> list[Path] # функция возвращает список Path
```

**`Path | None` — union type:**

```python
# До Python 3.10 писали так:
from typing import Optional
def scan(input_dir: Optional[Path]) -> None: ...

# Python 3.10+ — современный синтаксис с |
def scan(input_dir: Path | None) -> None: ...
```

**Зачем нужны type hints:**

```python
# Без type hints — IDE не знает что возвращает функция
files = scan_files(...)
files.  # IDE не предлагает методы ← нет подсказок

# С type hints — IDE знает что files: list[Path]
files = scan_files(...)
files.  # IDE предлагает: .append(), .extend(), len()...
# И для каждого элемента Path:
files[0].  # → .name, .suffix, .exists(), .stat()...
```

**Ruff проверяет type hints** — правила группы `UP` предлагают современный синтаксис:

```python
# UP007 — устаревший Optional
from typing import Optional
def f(x: Optional[str]) -> None: ...

# Ruff исправляет на современный:
def f(x: str | None) -> None: ...
```

---

### Тема 23 — Merge conflicts

**Merge conflict** возникает когда два коммита изменили одну и ту же строку в одном
файле. Git не знает какую версию оставить — просит человека решить.

**Типичная ситуация:**

```
main:              def scan_files(input_dir, extension):
feature/recursive: def scan_files(input_dir, extension, recursive=False):
feature/sort:      def scan_files(input_dir, extension, sort=True):
```

Когда мержим `feature/sort` в `main` после `feature/recursive` — конфликт.

**Как выглядит конфликт в файле:**

```python
<<<<<<< HEAD
def scan_files(input_dir: Path, extension: str, recursive: bool = False) -> list[Path]:
=======
def scan_files(input_dir: Path, extension: str, sort: bool = True) -> list[Path]:
>>>>>>> feature/sort
```

```
<<<<<<< HEAD      ← начало — текущее состояние ветки (куда мержим)
=======           ← разделитель
>>>>>>> feature/sort ← конец — входящие изменения (что мержим)
```

**Как разрешить:**

1. Открыть файл с конфликтом
2. Выбрать итоговый вариант (убрать маркеры `<<<<`, `====`, `>>>>`)
3. Написать финальный код:

```python
# Объединили оба аргумента
def scan_files(input_dir: Path, extension: str, recursive: bool = False, sort: bool = False) -> list[Path]:
```

4. Добавить и закоммитить:

```bash
git add src/cli_file_processor/core/scanner.py
git commit -m "resolve merge conflict in scan_files signature"
```

**Команды для работы с конфликтами:**

```bash
git status                  # показывает файлы с конфликтами (both modified)
git diff                    # показывает все конфликты
git merge --abort           # отменить merge, вернуться к состоянию до
git log --merge             # коммиты которые вызвали конфликт
```

**Как избегать конфликтов:**

```bash
# Перед началом работы — обновить main
git switch main
git pull
git switch -c feature/my-feature

# Регулярно подтягивать изменения из main во время работы
git fetch origin
git rebase origin/main   # перебазировать ветку поверх актуального main
```

---

### Тема 24 — Conventional Commits

**Conventional Commits** — стандарт оформления сообщений коммитов.
Делает историю git читаемой и позволяет автоматически генерировать changelog.

**Формат:**

```
<тип>(<область>): <описание>

тип     — что это за изменение (feat, fix, docs, ...)
область — какая часть кода затронута (опционально)
описание — кратко что сделано, глагол в настоящем времени
```

**Типы:**

| Тип | Назначение | Пример |
|-----|-----------|--------|
| `feat` | Новая функциональность | `feat: add --recursive flag` |
| `fix` | Исправление бага | `fix: handle missing input directory` |
| `docs` | Только документация | `docs: update README with GitHub topics` |
| `refactor` | Рефакторинг без изменения поведения | `refactor: extract normalize_extension` |
| `test` | Добавление или правка тестов | `test: add recursive scan tests` |
| `ci` | Изменения CI/CD | `ci: add GitHub Actions workflow` |
| `chore` | Служебное (зависимости, конфиг) | `chore: add ruff and pre-commit` |
| `style` | Форматирование, без логики | `style: apply ruff format to tests/` |

**Примеры из этого проекта в стиле Conventional Commits:**

```bash
# Было (наш стиль):
git commit -m "add --recursive flag to scan command"
git commit -m "add GitHub Actions CI workflow"
git commit -m "apply ruff format to tests/"

# В стиле Conventional Commits:
git commit -m "feat(scan): add --recursive flag for subdirectory search"
git commit -m "ci: add GitHub Actions workflow with ruff and pytest"
git commit -m "style: apply ruff format to tests/"
```

**Почему это полезно:**

```bash
# По истории сразу видно структуру изменений:
git log --oneline
# feat(scan): add --recursive flag
# feat(process): add --dry-run flag
# ci: add GitHub Actions workflow
# chore: add ruff and pre-commit
# fix: handle empty directory in scan
# docs: update README with all topics
```

Инструменты вроде `semantic-release` умеют по типам коммитов автоматически
определять версию (feat → minor, fix → patch) и генерировать CHANGELOG.md.

---

### Тема 25 — Полный engineering lifecycle

Всё что мы изучили — это не набор отдельных инструментов, а единый цикл разработки.
Вот как он выглядит в этом проекте:

```
┌─────────────────────────────────────────────────────────────┐
│                   РАЗРАБОТКА                                │
│                                                             │
│  Пишешь код в IDE                                          │
│       ↓                                                     │
│  pytest tests/ -v          ← убеждаешься что ничего не сломал│
│       ↓                                                     │
│  ruff check src/           ← линтер проверяет стиль        │
│  ruff format src/          ← форматтер приводит к единому виду│
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│                   КОММИТ                                    │
│                                                             │
│  git add <files>                                            │
│  git commit -m "feat: ..."                                  │
│       ↓                                                     │
│  pre-commit hook срабатывает автоматически:                 │
│    → ruff check --fix                                       │
│    → ruff format                                            │
│  Если нашёл — исправил файлы, коммит отменён               │
│  git add → git commit — снова                               │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│                   PUSH И PR                                 │
│                                                             │
│  git push origin feature/my-feature                        │
│       ↓                                                     │
│  gh pr create --title "..." --base main                    │
│       ↓                                                     │
│  GitHub Actions CI запускается автоматически:               │
│    → ruff check src/ tests/                                 │
│    → ruff format --check src/ tests/                        │
│    → pytest tests/ -v                                       │
│  ✓ Passed — PR можно мержить                               │
│  ✗ Failed — видишь логи, правишь, пушишь снова             │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│                   MERGE                                     │
│                                                             │
│  gh pr merge 1 --merge --delete-branch                     │
│       ↓                                                     │
│  Код попадает в main                                        │
│  Ветка удаляется                                           │
│  CI запускается ещё раз на main — финальная проверка       │
└─────────────────────────────────────────────────────────────┘
```

**Каждый слой защиты ловит свой класс проблем:**

| Слой | Когда | Что ловит |
|------|-------|-----------|
| IDE (подсветка) | Во время написания | Синтаксические ошибки |
| pytest | Локально, до коммита | Сломанная логика |
| pre-commit | При `git commit` | Стиль, форматирование |
| GitHub Actions | При push/PR | Всё вместе на чистой машине |

Чем раньше поймал — тем дешевле исправить.

---

### Тема 26 — Coverage: покрытие кода тестами

**Файлы:** `pyproject.toml`, `tests/test_config.py`, обновлённые тесты

**Coverage** показывает какой процент строк кода выполнялся во время тестов.
Тесты могут проходить, но часть кода при этом не проверяется — coverage
показывает точно где дыры.

**Установка:**

```bash
pip install pytest-cov
```

**Запуск:**

```bash
# Базовый отчёт в терминале
pytest tests/ --cov=src/cli_file_processor

# С указанием непокрытых строк (самый полезный режим)
pytest tests/ --cov=src/cli_file_processor --cov-report=term-missing

# HTML-отчёт — открывается в браузере, подсвечивает строки
pytest tests/ --cov=src/cli_file_processor --cov-report=html
open htmlcov/index.html
```

**Как читать отчёт:**

```
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
src/cli_file_processor/cli.py                 54      5    91%   96, 98, 166, 168, 170
src/cli_file_processor/config.py              12      0   100%
src/cli_file_processor/core/scanner.py        17      0   100%
src/cli_file_processor/output.py              48      1    98%   40
------------------------------------------------------------------------
TOTAL                                        151      6    96%
```

```
Stmts   — сколько строк кода в файле (statements)
Miss    — сколько строк не выполнялось ни разу
Cover   — процент покрытия: (Stmts - Miss) / Stmts * 100
Missing — конкретные номера непокрытых строк
```

**Настройка в `pyproject.toml`:**

```toml
[tool.pytest.ini_options]
# addopts — аргументы которые pytest добавляет при каждом запуске автоматически.
# Теперь простой "pytest tests/" уже включает coverage.
addopts = "--cov=src/cli_file_processor --cov-report=term-missing --cov-fail-under=90"

[tool.coverage.run]
omit = [
    "src/cli_file_processor/main.py",  # if __name__ == "__main__" — не тестируется
]

[tool.coverage.report]
exclude_lines = [
    "if __name__ == .__main__.",  # стандартная точка входа
]
```

**`--cov-fail-under=90`** — pytest завершается с exit code 1 если покрытие ниже 90%.
Это значит CI упадёт, защищая `main` от непокрытого кода.

```bash
pytest tests/
# ...
# FAIL Required test coverage of 90% not reached. Total coverage: 87%
# exit code: 1  ← CI видит это и помечает шаг как FAILED
```

**Coverage в GitHub Actions CI:**

```yaml
- name: Run tests
  run: pytest tests/ -v --cov=src/cli_file_processor --cov-report=term-missing --cov-fail-under=90
```

Теперь при каждом PR GitHub проверяет не только что тесты проходят,
но и что покрытие не упало ниже порога.

**Осознанные пробелы — что не покрываем и почему:**

| Строки | Что там | Почему не покрываем |
|--------|---------|---------------------|
| `cli.py:96,98,166-170` | Ветки "нет аргумента → берём дефолт из `.env`" | Требует мокать файловую систему — усложняет тесты непропорционально пользе |
| `output.py:40` | Форматирование размера в MB (> 1 МБ) | Создавать мегабайтный файл в тестах — излишество |

Это не баги — это осознанное решение. 96% при разумных тестах лучше,
чем 100% при искусственных.

**Что нового написали:**

```
tests/test_config.py   ← новый файл: 8 тестов для config.py
tests/test_cli.py      ← добавлены тесты: version, --recursive, KB-размер, process-с-файлом
tests/test_scanner.py  ← добавлены тесты: recursive=True, recursive=False
```

**Итог:** 36 тестов → 53 теста, покрытие 87% → **96%**.

---

### Тема 27 — Mypy: статическая проверка типов

**Файлы:** `pyproject.toml`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`

**Mypy** проверяет type hints до запуска программы. Ruff проверяет стиль,
pytest проверяет поведение — mypy проверяет **типы**.

**Три слоя проверок в проекте:**

```
ruff   → стиль и логика: неиспользуемые импорты, порядок, форматирование
mypy   → типы: правильно ли передаются аргументы, что возвращают функции
pytest → поведение: правильно ли работает программа во время выполнения
```

**Что mypy ловит:**

```python
def scan_files(input_dir: Path, extension: str) -> list[Path]:
    ...

# Mypy поймает до запуска:
scan_files(input_dir="data/input", extension=".txt")
# error: Argument "input_dir" has incompatible type "str"; expected "Path"

files = scan_files(Path("data/input"), ".txt")
files.upper()   # list не имеет метода upper()
# error: "list[Path]" has no attribute "upper"
```

Python эти ошибки не заметит — они проявятся только во время выполнения.
Mypy находит их статически, без запуска кода.

**Установка:**

```bash
pip install mypy
```

**Запуск:**

```bash
# Обычная проверка
python -m mypy src/

# Строгий режим — максимальная проверка
python -m mypy src/ --strict
```

**Конфигурация в `pyproject.toml`:**

```toml
[tool.mypy]
python_version = "3.12"   # версия Python для проверки синтаксиса
strict = true             # включает все строгие проверки
pretty = true             # читаемый вывод с указателями на строки
```

**Что включает `strict = true`:**

| Флаг | Что проверяет |
|------|--------------|
| `--disallow-untyped-defs` | Все функции должны иметь аннотации |
| `--disallow-any-generics` | Нельзя писать `list` без параметра — только `list[str]` |
| `--warn-return-any` | Нельзя молча возвращать `Any` |
| `--warn-unused-ignores` | Нельзя игнорировать ошибки которых нет |
| `--check-untyped-defs` | Проверяет тело функций без аннотаций |

**Pre-commit хук:**

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.16.0
  hooks:
    - id: mypy
      additional_dependencies: [typer, rich]   # нужны для проверки импортов
      args: [--strict]
```

`additional_dependencies` — mypy в pre-commit окружении изолирован, нужно явно
указать сторонние библиотеки чтобы он мог проверять их типы.

**GitHub Actions CI:**

```yaml
- name: Mypy type check
  run: python -m mypy src/ --strict
```

**Почему наш код прошёл строгий режим:**

Потому что type hints писались правильно с самого начала:

```python
# Все функции аннотированы
def normalize_extension(extension: str) -> str: ...
def scan_files(input_dir: Path, extension: str, recursive: bool = False) -> list[Path]: ...
def print_scan_results(files: list[Path], base_dir: Path | None = None) -> None: ...

# Используется современный синтаксис (Python 3.10+)
Path | None      # не Optional[Path]
list[Path]       # не List[Path] из typing

# Нет неаннотированных функций, нет Any
```

Если бы type hints отсутствовали или были написаны небрежно — mypy нашёл бы
десятки ошибок.

**Полная цепочка проверок при коммите:**

```
git commit
    ↓
pre-commit:
  ruff check --fix    ← стиль и логика
  ruff format         ← форматирование
  mypy --strict       ← типы
    ↓ (всё прошло)
коммит создан ✓
```

---

### Тема 28 — Docker: контейнеризация

**Файлы:** `Dockerfile`, `.dockerignore`

**Проблема которую решает Docker:**

```
Без Docker:
  твоя машина  → Python 3.12, venv, зависимости → работает
  сервер        → Python 3.10, нет venv           → не работает
  коллега       → другая ОС, другие версии        → "у меня не запускается"

С Docker:
  любая машина  → docker run cli-file-processor   → работает одинаково
```

**Три ключевых понятия:**

```
Dockerfile  — инструкция как собрать образ (текстовый рецепт)
Image       — собранный образ: snapshot окружения + кода (результат рецепта)
Container   — запущенный образ: живой изолированный процесс
```

**Dockerfile проекта:**

```dockerfile
# Базовый образ — официальный Python 3.12 на минимальном Debian.
# slim весит ~50MB против ~900MB у полного образа.
FROM python:3.12-slim

# Рабочая папка внутри контейнера.
# Все следующие команды выполняются относительно неё.
WORKDIR /app

# Копируем pyproject.toml и src/ отдельно от остального кода.
# Docker кеширует каждый слой — если изменился только README,
# слой с pip install не пересобирается.
COPY pyproject.toml .
COPY src/ ./src/

# Устанавливаем пакет и зависимости.
# --no-cache-dir — не хранить кеш pip внутри образа, экономит место.
RUN pip install --no-cache-dir .

# Создаём папки для данных.
RUN mkdir -p data/input data/output

# ENTRYPOINT — фиксированная команда при старте контейнера.
# docker run <image> scan → cli-file-processor scan
ENTRYPOINT ["cli-file-processor"]

# CMD — аргументы по умолчанию если не передано ничего.
# docker run <image>      → cli-file-processor --help
CMD ["--help"]
```

**Почему порядок COPY важен — кеширование слоёв:**

```
COPY pyproject.toml .    ← слой 1: пересобирается если pyproject.toml изменился
COPY src/ ./src/         ← слой 2: пересобирается если код изменился
RUN pip install .        ← слой 3: кешируется если слои 1-2 не менялись
```

Если ты поменял только логику в `scanner.py` — Docker пересобирает только
слои 2 и 3. Слой 1 берётся из кеша. Это ускоряет сборку.

**`.dockerignore` — что не копируем в образ:**

```
.venv/          ← виртуальное окружение — в образе своё Python
.git/           ← история git не нужна в production
tests/          ← тесты не нужны в итоговом образе
.env            ← секреты — передаются через переменные окружения
data/output/    ← результаты работы — создаются при запуске
```

Без `.dockerignore` контекст сборки был бы в разы больше и образ содержал бы лишнее.

**Основные команды:**

```bash
# Собрать образ с тегом (именем)
docker build -t cli-file-processor .

# Запустить с аргументами по умолчанию (--help)
docker run --rm cli-file-processor

# Запустить команду
docker run --rm cli-file-processor version
docker run --rm cli-file-processor check

# Список собранных образов
docker images

# Список запущенных контейнеров
docker ps

# Удалить образ
docker rmi cli-file-processor
```

**`--rm`** — удалить контейнер после завершения. Без него остановленные
контейнеры накапливаются: `docker ps -a` показывает их все.

**Volume — пробросить папку с хоста в контейнер:**

```bash
# Синтаксис: -v <путь_на_хосте>:<путь_в_контейнере>
docker run --rm \
  -v $(pwd)/data/input:/app/data/input \
  -v $(pwd)/data/output:/app/data/output \
  cli-file-processor scan --input-dir data/input --extension .txt
```

Без volume контейнер изолирован — не видит файлы на твоей машине.
С volume — папка `data/input` с хоста монтируется внутрь как `/app/data/input`.

**ENTRYPOINT vs CMD:**

```dockerfile
ENTRYPOINT ["cli-file-processor"]   # фиксировано — нельзя переопределить при запуске
CMD ["--help"]                       # по умолчанию — заменяется аргументами

# docker run cli-file-processor           → cli-file-processor --help  (CMD используется)
# docker run cli-file-processor scan ...  → cli-file-processor scan ... (CMD игнорируется)
```

**Размер образа:**

```bash
docker images cli-file-processor
# REPOSITORY           TAG      IMAGE ID       SIZE
# cli-file-processor   latest   e9a58b7bdbbb   210MB
```

`python:3.12-slim` (~50MB) + зависимости (typer, rich, dotenv) + код = ~210MB.
Для сравнения, `python:3.12` (полный образ) дал бы ~1.2GB.

---

### Тема 29 — Makefile: стандартные команды проекта

**Файл:** `Makefile`

**Проблема которую решает:**

```bash
# Без Makefile — нужно помнить и печатать:
python -m ruff check src/ tests/
python -m mypy src/ --strict
pytest tests/ -v --cov=src/cli_file_processor --cov-report=term-missing
docker build -t cli-file-processor .

# С Makefile — просто:
make lint
make type-check
make test
make build
```

Makefile — стандарт в профессиональных проектах. Новый разработчик клонирует
репозиторий, запускает `make help` — и сразу видит все доступные команды.

**Синтаксис:**

```makefile
# Переменная
PYTHON := .venv/bin/python

# Цель: зависимости
# [TAB] команда
test: lint
	$(PYTHON) -m pytest tests/ -v
```

Важно: отступ перед командой — это **Tab**, не пробелы. Make требует именно Tab.

**Полный Makefile проекта:**

```makefile
PYTHON := .venv/bin/python

.PHONY: install lint format type-check test check build clean help

help:
	@echo "Доступные команды:"
	@echo "  make install     — установить проект и dev-зависимости"
	@echo "  make lint        — проверить стиль кода (ruff)"
	@echo "  make format      — отформатировать код (ruff format)"
	@echo "  make type-check  — проверить типы (mypy --strict)"
	@echo "  make test        — запустить тесты с покрытием"
	@echo "  make check       — lint + type-check + test"
	@echo "  make build       — собрать Docker-образ"
	@echo "  make clean       — удалить временные файлы"

install:
	pip install -e ".[dev]"
	pre-commit install

lint:
	$(PYTHON) -m ruff check src/ tests/

format:
	$(PYTHON) -m ruff format src/ tests/

type-check:
	$(PYTHON) -m mypy src/ --strict

test:
	$(PYTHON) -m pytest tests/ -v

check: lint type-check test

build:
	docker build -t cli-file-processor .

clean:
	rm -rf .coverage htmlcov/ .mypy_cache/ .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
```

**Ключевые концепции:**

**`.PHONY`** — объявляет цели командами, а не файлами:

```makefile
.PHONY: test

test:
	pytest tests/
```

Без `.PHONY` если в папке существует файл с именем `test` — make решит
что цель уже выполнена и ничего не запустит.

**Переменная `PYTHON`** — не зависит от активации venv:

```makefile
PYTHON := .venv/bin/python

# Вместо:
pytest tests/          ← использует системный Python
# Используем:
$(PYTHON) -m pytest    ← использует Python из виртуального окружения
```

**Зависимости между целями:**

```makefile
# check зависит от lint, type-check и test
# Они запустятся по порядку перед командами самого check
check: lint type-check test
```

Если `lint` упал — `type-check` и `test` не запустятся. Это защита:
бессмысленно проверять типы если код не прошёл линтер.

**`@` перед командой** — скрывает саму команду, показывает только вывод:

```makefile
help:
	@echo "make test — запустить тесты"  # выводит: make test — запустить тесты
	echo "make test — запустить тесты"   # выводит: echo "..." и потом сам текст
```

**Первая цель = цель по умолчанию:**

```bash
make        # → запускает help (первая цель в файле)
make test   # → запускает test
make check  # → lint + type-check + test
```

**Типичный рабочий процесс с Makefile:**

```bash
# После клонирования репозитория — один раз
make install

# Во время разработки — перед каждым коммитом
make check

# Отдельные команды по необходимости
make format      # отформатировать код
make test        # только тесты (быстро)
make build       # собрать Docker-образ
make clean       # почистить временные файлы
```

---

### Тема 30 — Pydantic Settings: типизированная конфигурация

**Файл:** `src/cli_file_processor/config.py`

**Что было до — `os.getenv` подход:**

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_default_input_dir() -> Path:
    return Path(os.getenv("DEFAULT_INPUT_DIR", "data/input"))

def get_default_extension() -> str:
    return os.getenv("DEFAULT_EXTENSION", ".txt")

def get_default_output_dir() -> Path:
    return Path(os.getenv("DEFAULT_OUTPUT_DIR", "data/output"))
```

Проблемы: четыре отдельные функции, нет валидации, тип приходится приводить вручную (`Path(...)`), нет единого места где видны все настройки.

**Что стало — Pydantic Settings:**

```python
from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    default_input_dir: Path = Path("data/input")
    default_extension: str = ".txt"
    default_output_dir: Path = Path("data/output")
    app_version: str = "0.1.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @field_validator("default_extension")
    @classmethod
    def extension_must_start_with_dot(cls, value: str) -> str:
        if not value.startswith("."):
            return f".{value}"
        return value

settings = Settings()
```

**Как Pydantic Settings читает конфигурацию — приоритет:**

```
1. Переменные окружения (наивысший)  export DEFAULT_INPUT_DIR=/data
2. Переменные из .env файла          DEFAULT_INPUT_DIR=data/input
3. Значения по умолчанию в классе    default_input_dir: Path = Path("data/input")
```

**Автоматическое приведение типов:**

```python
# В .env написано:
DEFAULT_INPUT_DIR=data/reports

# Pydantic читает строку "data/reports" и сам конвертирует в Path:
settings.default_input_dir   # → Path("data/reports"), уже Path — не str
```

Не нужно писать `Path(os.getenv(...))` — Pydantic делает это сам.

**`field_validator` — валидация при старте:**

```python
@field_validator("default_extension")
@classmethod
def extension_must_start_with_dot(cls, value: str) -> str:
    if not value.startswith("."):
        return f".{value}"
    return value
```

Если в `.env` написано `DEFAULT_EXTENSION=txt` (без точки) — валидатор
автоматически исправит на `.txt`. Это происходит один раз при запуске программы,
до любой обработки файлов.

**`model_config = SettingsConfigDict(...)`** — настройки самого класса:

```python
model_config = SettingsConfigDict(
    env_file=".env",              # читать переменные из этого файла
    env_file_encoding="utf-8",    # кодировка файла
)
```

**Единственный экземпляр — `settings = Settings()`:**

```python
# config.py — создаётся один раз при первом импорте модуля
settings = Settings()

# cli.py, scanner.py, любой другой модуль — импортирует готовый объект
from cli_file_processor.config import settings
print(settings.default_input_dir)  # Path("data/input")
```

Python кешируют импортированные модули — `settings` создаётся ровно один раз
за всё время работы программы.

**Функции-обёртки для обратной совместимости:**

```python
# Сохранили старый интерфейс — cli.py не трогали
def get_default_input_dir() -> Path:
    return settings.default_input_dir

def get_default_extension() -> str:
    return settings.default_extension
```

Это паттерн **обратной совместимости**: внутренняя реализация изменилась,
внешний интерфейс остался прежним. Все вызывающие код модули продолжают работать.

**Что поймали по дороге — pre-commit и изолированное окружение:**

Mypy в pre-commit работает в собственном изолированном окружении.
Он не видит пакеты из `.venv` — нужно явно перечислить зависимости:

```yaml
# .pre-commit-config.yaml
- id: mypy
  additional_dependencies: [typer, rich, pydantic-settings]  # ← добавили
  args: [--strict]
```

Без этого mypy в pre-commit падал с `Cannot find implementation for module "pydantic"`,
хотя локально (`make type-check`) всё проходило.

**Установка:**

```bash
pip install pydantic-settings
```

---

## Зависимости

| Библиотека | Назначение | Тип |
|------------|-----------|-----|
| `typer` | Создание CLI команд, парсинг аргументов | основная |
| `python-dotenv` | Чтение `.env` файлов | основная |
| `rich` | Цвета, таблицы, прогресс-бар в терминале | основная |
| `pydantic-settings` | Типизированная конфигурация из `.env` | основная |
| `pytest` | Запуск и организация тестов | dev |
| `pytest-cov` | Измерение покрытия кода тестами | dev |
| `mypy` | Статическая проверка типов | dev |
| `ruff` | Линтер + форматтер кода | dev |
| `pre-commit` | Автозапуск проверок перед git commit | dev |

**Внешние инструменты (устанавливаются отдельно, не через pip):**

| Инструмент | Назначение | Установка |
|------------|-----------|-----------|
| `git` | Система контроля версий | `sudo apt install git` |
| `gh` | GitHub CLI — управление репо, PR, Actions | `sudo apt install gh` |

**Стандартные библиотеки Python (не нужно устанавливать):**

| Библиотека | Что используем |
|------------|---------------|
| `pathlib` | `Path` — работа с путями файловой системы |
| `logging` | Уровни логирования, `basicConfig`, `getLogger` |
| `shutil` | `copy2` — копирование файлов с метаданными |
| `os` | `os.getenv` — чтение переменных окружения |
