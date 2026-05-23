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
   - [Тема 31 — FastAPI: REST-интерфейс поверх бизнес-логики](#тема-31--fastapi-rest-интерфейс-поверх-бизнес-логики)
   - [Тема 32 — conftest.py: общие fixtures и parametrize](#тема-32--conftestpy-общие-fixtures-и-parametrize)
   - [Тема 33 — Rich Progress Bar: прогресс-бар для долгих операций](#тема-33--rich-progress-bar-прогресс-бар-для-долгих-операций)
   - [Тема 34 — Кастомные исключения: иерархия ошибок проекта](#тема-34--кастомные-исключения-иерархия-ошибок-проекта)
   - [Тема 35 — Dataclasses: структурированные результаты вместо сырых списков](#тема-35--dataclasses-структурированные-результаты-вместо-сырых-списков)
   - [Тема 36 — Контекст-менеджеры: `with`, `__enter__`/`__exit__`, `@contextmanager`](#тема-36--контекст-менеджеры-with-__enter____exit__-contextmanager)
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

### Тема 31 — FastAPI: REST-интерфейс поверх бизнес-логики

**Файл:** `src/cli_file_processor/api.py`

**Идея:** та же бизнес-логика (`scan_files()`) — два интерфейса: CLI и REST API. `scanner.py` не знает ни о том, ни о другом.

**Что реализовали:**

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from cli_file_processor.config import settings
from cli_file_processor.core.scanner import scan_files

app = FastAPI(title="CLI File Processor API", version=settings.app_version)

class FileInfo(BaseModel):
    name: str
    path: str
    size: int
    extension: str

class ScanResult(BaseModel):
    total: int
    files: list[FileInfo]

@app.get("/health")
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=settings.app_version)

@app.get("/scan", response_model=ScanResult)
def scan(
    extension: str = Query(default=settings.default_extension),
    input_dir: str = Query(default=str(settings.default_input_dir)),
    recursive: bool = Query(default=False),
) -> ScanResult:
    dir_path = Path(input_dir)
    if not dir_path.exists():
        raise HTTPException(status_code=404, detail=f"Папка не найдена: {input_dir}")
    files = scan_files(input_dir=dir_path, extension=extension, recursive=recursive)
    ...
```

**Ключевые концепции:**

| Концепция | Что делает |
|-----------|-----------|
| `FastAPI()` | Создаёт приложение, генерирует `/docs` автоматически |
| `BaseModel` (Pydantic) | Описывает структуру JSON-ответа, FastAPI сериализует автоматически |
| `@app.get("/scan")` | Регистрирует GET-эндпоинт |
| `Query(default=...)` | Параметр из URL: `/scan?extension=.pdf&recursive=true` |
| `response_model=` | FastAPI проверяет что ответ соответствует схеме |
| `HTTPException` | Возвращает HTTP-ошибку (404, 400) с JSON-телом |

**Запуск:**

```bash
make api
# или напрямую:
uvicorn cli_file_processor.api:app --reload

# Тестирование:
curl http://localhost:8000/health
curl "http://localhost:8000/scan?extension=.txt"
curl "http://localhost:8000/scan?extension=.txt&recursive=true"
# Автодокументация:
# http://localhost:8000/docs
```

**Тестирование FastAPI — TestClient:**

FastAPI предоставляет `TestClient` (на основе `httpx`) — тесты выглядят как обычные HTTP-запросы, но без реального сервера:

```python
from fastapi.testclient import TestClient
from cli_file_processor.api import app

client = TestClient(app)

def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_scan_nonexistent_dir_returns_404() -> None:
    response = client.get("/scan?input_dir=/nonexistent")
    assert response.status_code == 404
```

**Итог:** бизнес-логика в `scanner.py` осталась без изменений — CLI и API просто два разных способа вызвать те же функции.

---

### Тема 32 — conftest.py: общие fixtures и parametrize

**Файл:** `tests/conftest.py`

**Проблема:** 60 тестов в 5 файлах — одинаковый setup-код в каждом тесте:
```python
# Это повторялось в 8 разных тестах:
input_dir = tmp_path / "input"
input_dir.mkdir()
output_dir = tmp_path / "output"
```

**`conftest.py`** — специальный файл, который pytest находит автоматически. Все fixtures в нём доступны в любом тест-файле без явного импорта.

**Что создали:**

```python
import pytest
from pathlib import Path
from collections.abc import Generator
from fastapi.testclient import TestClient
from cli_file_processor.api import app

@pytest.fixture
def sample_txt_dir(tmp_path: Path) -> Path:
    """Папка с 2 .txt и 1 .pdf — стандартный набор для тестов scanner."""
    (tmp_path / "file1.txt").touch()
    (tmp_path / "file2.txt").touch()
    (tmp_path / "report.pdf").touch()
    return tmp_path

@pytest.fixture
def input_dir(tmp_path: Path) -> Path:
    d = tmp_path / "input"
    d.mkdir()
    return d

@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    return tmp_path / "output"  # папка не создаётся — тест проверит это сам

# scope="module" — один экземпляр на весь файл тестов (не на каждый тест)
@pytest.fixture(scope="module")
def api_client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client  # setup выше, teardown (shutdown FastAPI) — после yield
```

**Ключевые концепции:**

| Концепция | Что делает |
|-----------|-----------|
| `conftest.py` | pytest находит его автоматически, импорт не нужен |
| `@pytest.fixture` | Функция становится фикстурой — pytest передаёт её по имени аргумента |
| `scope="module"` | Фикстура создаётся один раз на файл (не на каждый тест) |
| `yield` в fixture | Код до `yield` — setup, после — teardown |
| `tmp_path` | Встроенная fixture pytest для временных файлов |

**Важно про `tmp_path`:** если две фикстуры в одном тесте используют `tmp_path`, они получают один и тот же объект. Поэтому `input_dir` и `output_dir` живут в одной папке:

```python
def test_process(input_dir: Path, output_dir: Path):
    # input_dir = /tmp/.../input/
    # output_dir = /tmp/.../output/
    # Одна и та же /tmp/.../ папка — pytest это гарантирует
    (input_dir / "file.txt").write_text("data")
    ...
```

**`@pytest.mark.parametrize`** — запускает один тест с разными данными:

```python
# До: 5 отдельных функций с одинаковой структурой
def test_normalize_extension_adds_dot(): assert normalize_extension("txt") == ".txt"
def test_normalize_extension_keeps_existing_dot(): assert normalize_extension(".txt") == ".txt"
# ...

# После: одна функция, 5 тест-кейсов
@pytest.mark.parametrize("raw,expected", [
    ("txt", ".txt"),
    (".txt", ".txt"),
    ("PDF", ".pdf"),
    ("  .TXT  ", ".txt"),
    ("  PDF  ", ".pdf"),
])
def test_normalize_extension(raw: str, expected: str) -> None:
    assert normalize_extension(raw) == expected
```

Pytest показывает каждый кейс отдельно:
```
test_normalize_extension[txt-.txt] PASSED
test_normalize_extension[PDF-.pdf] PASSED
```

---

### Тема 33 — Rich Progress Bar: прогресс-бар для долгих операций

**Файл:** `src/cli_file_processor/output.py` → `process_files_with_progress()`

**Два уровня API в Rich:**

```python
# Простой способ — track(): одна строка, нет контроля
from rich.progress import track

for file in track(files, description="Копирование..."):
    process(file)

# Продвинутый — Progress: полный контроль над колонками и обновлениями
from rich.progress import Progress, SpinnerColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn, TextColumn
```

**Что реализовали:**

```python
with Progress(
    SpinnerColumn(),                                        # ⠋ ⠙ ⠹ ⠸ — анимация
    TextColumn("[progress.description]{task.description}"), # имя файла
    BarColumn(),                                            # ████████░░
    TaskProgressColumn(),                                   # 3/10
    TimeElapsedColumn(),                                    # 0:00:02
) as progress:
    task = progress.add_task("Копирование...", total=len(files))

    for file_path in files:
        progress.update(task, description=f"[cyan]{file_path.name}[/cyan]")
        process_files([file_path], output_dir)
        progress.advance(task)  # +1 к счётчику, прогресс-бар двигается
```

**Как это выглядит:**
```
⠸ report.pdf   ████████░░░░░░░  3/10  0:00:01
```

**Ключевые концепции:**

| Что | Зачем |
|-----|-------|
| `with Progress(...) as progress` | Контекстный менеджер — при выходе очищает строку прогресса |
| `add_task(total=N)` | Регистрирует задачу, возвращает ID для дальнейших вызовов |
| `progress.update(task, description=...)` | Меняет текст задачи на лету — показываем текущий файл |
| `progress.advance(task)` | Увеличивает счётчик на 1 — полоса продвигается |
| `[cyan]{task.description}[/cyan]` | Rich markup внутри TextColumn — цвет без `console.print` |

**Почему не в `processor.py`:** копирование файлов — бизнес-логика. Прогресс-бар — способ *показать* эту логику. Разные уровни ответственности → код вывода остаётся в `output.py`, `processor.py` не знает о Rich.

---

### Тема 34 — Кастомные исключения: иерархия ошибок проекта

**Файл:** `src/cli_file_processor/exceptions.py`

**Проблема до:** одинаковые проверки в двух местах — `cli.py` и `api.py`. При добавлении нового интерфейса нужно копировать ещё раз.

```python
# Было — дублируется в cli.py И в api.py:
if not input_dir.exists():
    ...  # cli: print_error + Exit(1), api: HTTPException(404)
if not input_dir.is_dir():
    ...  # cli: print_error + Exit(1), api: HTTPException(400)
```

**Решение — исключения как иерархия:**

```python
class ProcessorError(Exception):
    """Базовый класс — ловить все ошибки приложения сразу."""

class InputDirNotFoundError(ProcessorError):
    def __init__(self, path: Path) -> None:
        self.path = path                          # атрибут — для программного доступа
        super().__init__(f"папка не найдена: {path}")  # str(e) вернёт это

class InputNotADirectoryError(ProcessorError):
    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"это не папка: {path}")
```

**Валидация переехала в `scanner.py` — один раз, одно место:**

```python
def scan_files(input_dir: Path, ...) -> list[Path]:
    if not input_dir.exists():
        raise InputDirNotFoundError(input_dir)   # бросаем — не печатаем
    if not input_dir.is_dir():
        raise InputNotADirectoryError(input_dir)
    ...
```

**CLI ловит базовый класс** — обрабатывает любую ошибку одинаково:

```python
try:
    files = scan_files(...)
except ProcessorError as e:
    print_error(str(e))          # str(e) → "папка не найдена: /path"
    raise typer.Exit(code=1)
```

**API ловит конкретные подтипы** — каждый маппится в свой HTTP-код:

```python
try:
    files = scan_files(...)
except InputDirNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
except InputNotADirectoryError as e:
    raise HTTPException(status_code=400, detail=str(e))
```

**Тест проверяет тип, атрибут и текст:**

```python
def test_scan_raises_when_dir_not_found(tmp_path: Path) -> None:
    with pytest.raises(InputDirNotFoundError) as exc_info:
        scan_files(input_dir=tmp_path / "nonexistent", extension=".txt")
    assert exc_info.value.path == tmp_path / "nonexistent"  # атрибут
    assert "не найдена" in str(exc_info.value)              # текст сообщения
```

**Итог:** бизнес-логика бросает исключения, не зная кто их поймает. CLI и API реагируют по-своему на одно и то же исключение — разделение ответственности.

---

### Тема 35 — Dataclasses: структурированные результаты вместо сырых списков

**Файлы:** `src/cli_file_processor/core/models.py` (новый), изменены `scanner.py`, `processor.py`, `output.py`, `cli.py`, `api.py`

#### Проблема: сырые данные без контекста

До этой темы функции возвращали "голые" типы:

```python
# scanner.py — было:
def scan_files(...) -> list[Path]:
    return files                  # просто список путей

# processor.py — было:
def process_files(...) -> list[Path]:
    return processed              # тоже просто список путей
```

Вызывающий код (`cli.py`, `api.py`) получал список и сразу терял контекст: из какой папки сканировали? с каким расширением? был ли рекурсивный поиск? Эту информацию приходилось передавать отдельными аргументами в каждую следующую функцию.

```python
# cli.py — было: контекст тащится вручную через 3 функции
files = scan_files(input_dir, extension, recursive)
print_scan_results(files, base_dir=input_dir if recursive else None)
#                          ↑ приходится знать про recursive здесь
```

#### Решение: dataclass как контейнер данных + контекст

Создаём `core/models.py` с двумя датаклассами, которые несут в себе и данные, и контекст:

```python
# Стало: всё в одном объекте
result = scan_files(input_dir, extension, recursive)
print_scan_results(result)   # result сам знает про recursive
```

---

#### Что такое dataclass

`@dataclass` — декоратор из стандартной библиотеки `dataclasses`. Он автоматически генерирует несколько магических методов, которые иначе пришлось бы писать вручную.

```python
from dataclasses import dataclass

@dataclass
class ScanResult:
    files: list[Path]
    scanned_dir: Path
    extension: str
```

Python видит это и автоматически создаёт:

| Метод | Что делает | Пример |
|-------|-----------|--------|
| `__init__` | Конструктор — принимает все поля | `ScanResult(files=[...], scanned_dir=p, extension=".txt")` |
| `__repr__` | Строковое представление для отладки | `ScanResult(files=[...], scanned_dir=PosixPath('...'), ...)` |
| `__eq__` | Сравнение по значению полей | `r1 == r2` работает правильно |

Без `@dataclass` пришлось бы писать всё это руками:

```python
# Без dataclass — много бойлерплейта:
class ScanResult:
    def __init__(self, files, scanned_dir, extension):
        self.files = files
        self.scanned_dir = scanned_dir
        self.extension = extension

    def __repr__(self):
        return f"ScanResult(files={self.files!r}, ...)"

    def __eq__(self, other):
        if not isinstance(other, ScanResult):
            return NotImplemented
        return (self.files == other.files and
                self.scanned_dir == other.scanned_dir and
                self.extension == other.extension)
```

`@dataclass` заменяет всё это тремя строками с аннотациями типов.

---

#### Поля с дефолтами — правило для изменяемых типов

У `ScanResult` есть поле `recursive: bool = False`. Это простое значение — дефолт безопасен.

Но для **изменяемых типов** (`list`, `dict`, `set`) нельзя писать дефолт напрямую:

```python
# НЕПРАВИЛЬНО — Python создаст ОДИН список на все экземпляры класса:
@dataclass
class ScanResult:
    errors: list[str] = []   # ← ошибка: ValueError от dataclass

# ПРАВИЛЬНО — field(default_factory=list) создаёт новый список для каждого объекта:
from dataclasses import dataclass, field

@dataclass
class ScanResult:
    errors: list[str] = field(default_factory=list)
```

**Почему это важно:**

```python
# Демонстрация проблемы с изменяемым дефолтом (обычный класс, не dataclass):
class Bad:
    def __init__(self, items=[]):   # ← опасно
        self.items = items

a = Bad()
b = Bad()
a.items.append("x")
print(b.items)   # ["x"] — b видит изменения в a!
                 # Они ДЕЛЯТ один и тот же список!

# С field(default_factory=list) каждый экземпляр получает СВОЙ список:
@dataclass
class Good:
    items: list[str] = field(default_factory=list)

a = Good()
b = Good()
a.items.append("x")
print(b.items)   # [] — b не затронут
```

В нашем проекте поле `errors: list[str] = field(default_factory=list)` в `ScanResult` — это место для будущих предупреждений при сканировании. Каждый вызов `scan_files` получает свой независимый список.

---

#### @property — вычисляемые атрибуты

`@property` — декоратор, который позволяет вызывать метод как атрибут (без скобок). Используется для значений, которые **вычисляются** из других полей и не должны храниться отдельно.

```python
@dataclass
class ScanResult:
    files: list[Path]
    ...

    @property
    def total(self) -> int:
        return len(self.files)
```

Использование:

```python
result = scan_files(...)
print(result.total)      # работает как атрибут, не как метод
# print(result.total())  # ← так НЕЛЬЗЯ, @property не требует скобок
```

**Зачем это лучше, чем хранить `total` как поле:**

```python
# Плохо — дублирование данных:
@dataclass
class ScanResult:
    files: list[Path]
    total: int           # может не совпадать с len(files)!

result = ScanResult(files=[f1, f2], total=5)  # ← никто не мешает солгать

# Хорошо — один источник правды:
@dataclass
class ScanResult:
    files: list[Path]

    @property
    def total(self) -> int:
        return len(self.files)   # всегда точно, невозможно рассинхронизировать
```

---

#### __post_init__ — валидация после инициализации

`__post_init__` — специальный метод, который `@dataclass` вызывает автоматически **после** `__init__`. Используется для проверки данных при создании объекта.

```python
@dataclass
class ScanResult:
    files: list[Path]
    scanned_dir: Path
    extension: str

    def __post_init__(self) -> None:
        # Эта проверка выполнится при каждом ScanResult(...)
        if not self.extension.startswith("."):
            raise ValueError(
                f"расширение должно начинаться с точки, получено: {self.extension!r}"
            )
```

В нашем проекте `scan_files` всегда нормализует расширение перед созданием `ScanResult`, поэтому ошибка в реальном коде не возникнет. Но `__post_init__` защищает от ошибок при прямом создании объекта (например, в тестах или при рефакторинге):

```python
# Это упадёт сразу при создании, а не где-то позже:
ScanResult(files=[], scanned_dir=Path("."), extension="txt")
# ValueError: расширение должно начинаться с точки, получено: 'txt'

# Это нормально:
ScanResult(files=[], scanned_dir=Path("."), extension=".txt")
```

**Порядок выполнения:** `__init__` присваивает поля → `__post_init__` проверяет их.

---

#### frozen=True — иммутабельный объект

`@dataclass(frozen=True)` запрещает изменение полей после создания объекта. Попытка присвоить новое значение вызывает `FrozenInstanceError`.

```python
@dataclass(frozen=True)
class ProcessResult:
    processed: list[Path]
    output_dir: Path

    @property
    def total(self) -> int:
        return len(self.processed)
```

```python
result = process_files(files, output_dir)

# Попытка изменить поле:
result.output_dir = Path("/other")   # ← FrozenInstanceError!
result.processed = []                # ← FrozenInstanceError!

# Но(!) содержимое изменяемых объектов внутри можно трогать:
result.processed.append(Path("/new"))  # ← это РАБОТАЕТ (список сам изменяемый)
                                       # frozen защищает только переприсваивание
```

**Когда использовать `frozen=True`:**

- Когда объект является "результатом" — его создали один раз и он не должен меняться.
- `ProcessResult` — результат операции копирования. Он иммутабелен: файлы уже скопированы, менять объект бессмысленно.
- `ScanResult` — мутабелен намеренно: поле `errors` может пополняться в будущем.

---

#### Итоговый код в проекте

**`core/models.py`** — новый файл с доменными моделями:

```python
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ScanResult:
    files: list[Path]
    scanned_dir: Path
    extension: str
    recursive: bool = False
    errors: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.extension.startswith("."):
            raise ValueError(f"расширение должно начинаться с точки, получено: {self.extension!r}")

    @property
    def total(self) -> int:
        return len(self.files)


@dataclass(frozen=True)
class ProcessResult:
    processed: list[Path]
    output_dir: Path

    @property
    def total(self) -> int:
        return len(self.processed)
```

**`core/scanner.py`** — теперь возвращает `ScanResult`:

```python
def scan_files(input_dir: Path, extension: str, recursive: bool = False) -> ScanResult:
    ...
    return ScanResult(
        files=files,
        scanned_dir=input_dir,
        extension=normalized_extension,
        recursive=recursive,
    )
```

**`core/processor.py`** — теперь возвращает `ProcessResult`:

```python
def process_files(files: list[Path], output_dir: Path) -> ProcessResult:
    ...
    return ProcessResult(processed=processed, output_dir=output_dir)
```

**`cli.py`** — код стал проще, контекст не нужно передавать вручную:

```python
# scan:
result = scan_files(input_dir=input_dir, extension=extension, recursive=recursive)
if not result.files:
    ...
print_scan_results(result)   # result знает про recursive сам

# process:
scan_result = scan_files(...)
process_result = process_files_with_progress(scan_result.files, output_dir)
print_process_results(process_result)   # total и output_dir уже внутри
```

**`api.py`** — Pydantic-класс `ScanResult` переименован в `ScanResponse`, чтобы не конфликтовать с доменным датаклассом. Разные уровни — разные имена:

```python
class ScanResponse(BaseModel):      # HTTP-схема ответа (Pydantic)
    total: int
    files: list[FileInfo]

# Эндпоинт конвертирует доменный ScanResult → HTTP ScanResponse:
scan_result = scan_files(...)       # доменный dataclass
file_infos = [FileInfo(...) for f in scan_result.files]
return ScanResponse(total=scan_result.total, files=file_infos)
```

---

#### Dataclass vs Pydantic vs TypedDict

| | `@dataclass` | `pydantic.BaseModel` | `TypedDict` |
|---|---|---|---|
| Откуда | stdlib | сторонняя библиотека | stdlib |
| Валидация типов | нет (только аннотации) | да, при создании | нет |
| JSON сериализация | нет (нужен `asdict`) | встроена | нет |
| Производительность | быстрый | медленнее | самый быстрый |
| Когда использовать | доменные модели, результаты | API-схемы, конфиг | только аннотации |

В нашем проекте:
- **`@dataclass`** — для `ScanResult` и `ProcessResult` (доменный слой, никакого JSON)
- **`pydantic.BaseModel`** — для `ScanResponse`, `FileInfo` в `api.py` (HTTP-ответы с сериализацией)
- **`pydantic-settings`** — для `Settings` в `config.py` (конфиг из `.env`)

---

#### Что изменилось в архитектуре

```
До:
scan_files()  →  list[Path]   →  cli.py берёт файлы + отдельно передаёт recursive, input_dir

После:
scan_files()  →  ScanResult   →  cli.py берёт result и всё нужное уже внутри
                   ├── files
                   ├── scanned_dir    # знает откуда
                   ├── extension      # знает что искали
                   ├── recursive      # знает режим поиска
                   ├── total          # вычисляется автоматически
                   └── errors         # место для предупреждений
```

Слои больше не обмениваются "сырыми" структурами (`list[Path]`). Они передают **объекты с контекстом**, которые несут всё необходимое для следующего шага.

---

### Тема 36 — Контекст-менеджеры: `with`, `__enter__`/`__exit__`, `@contextmanager`

**Файлы:** `src/cli_file_processor/core/timer.py` (новый), изменены `cli.py`, `output.py`

#### Что такое контекст-менеджер и зачем он нужен

Контекст-менеджер — объект, который управляет ресурсом: захватывает его при входе в блок `with` и гарантированно освобождает при выходе — даже если произошло исключение.

**Без контекст-менеджера** нужно вручную следить за cleanup:

```python
# Открыть файл — нужно не забыть закрыть
f = open("file.txt")
try:
    data = f.read()
finally:
    f.close()   # ← надо помнить, легко пропустить
```

**С контекст-менеджером** cleanup автоматический:

```python
with open("file.txt") as f:
    data = f.read()
# f.close() вызовется здесь автоматически — даже при исключении
```

Контекст-менеджер отвечает на вопрос: **"что нужно сделать при входе и выходе из блока?"**

---

#### Синтаксис `with`

```python
with ВЫРАЖЕНИЕ as ПЕРЕМЕННАЯ:
    # тело блока
```

- `ВЫРАЖЕНИЕ` — объект-контекст-менеджер
- `as ПЕРЕМЕННАЯ` — опционально: получить значение, которое вернул `__enter__`
- При выходе из блока (нормально или через исключение) всегда вызывается `__exit__`

```python
# as можно опустить, если возвращаемое значение не нужно:
with open("file.txt"):
    ...

# Несколько менеджеров в одной строке:
with open("src.txt") as src, open("dst.txt", "w") as dst:
    dst.write(src.read())
```

---

#### Способ 1 — класс с `__enter__` и `__exit__`

Python вызывает эти два метода автоматически:

```
with Timer() as t:
    do_work()
    
↓ разворачивается в:

_cm = Timer()
t = _cm.__enter__()      # вызывается при входе в with
try:
    do_work()
finally:
    _cm.__exit__(...)    # вызывается при выходе — всегда
```

В нашем проекте — `Timer` из `core/timer.py`:

```python
class Timer:
    def __init__(self) -> None:
        self.elapsed: Elapsed | None = None
        self._start: float = 0.0

    def __enter__(self) -> "Timer":
        # Вызывается при входе в with. Запускаем секундомер.
        # Возвращаем self — именно этот объект попадёт в переменную after as.
        self._start = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,   # тип исключения (None если не было)
        exc_val: BaseException | None,           # объект исключения
        exc_tb: object,                          # traceback
    ) -> bool:
        # Вызывается при выходе из with — ВСЕГДА, даже при исключении.
        self.elapsed = Elapsed(time.perf_counter() - self._start)
        return False   # False = не подавлять исключение
```

**Три параметра `__exit__`:**

| Параметр | Что содержит | При нормальном выходе |
|----------|-------------|----------------------|
| `exc_type` | Класс исключения (`ValueError`, `OSError`, ...) | `None` |
| `exc_val` | Объект исключения | `None` |
| `exc_tb` | Traceback | `None` |

**Возвращаемое значение `__exit__`:**

```python
return False   # исключение пробрасывается дальше (обычное поведение)
return True    # исключение ПОДАВЛЯЕТСЯ — как будто его не было
```

Подавлять исключения нужно редко — только когда это осмысленно (например, `contextlib.suppress`).

---

#### Способ 2 — генераторная функция с `@contextmanager`

`contextlib.contextmanager` — декоратор, который превращает генераторную функцию в контекст-менеджер. Это более лаконичный способ для простых случаев.

```python
from contextlib import contextmanager

@contextmanager
def timed() -> Generator[Timer, None, None]:
    t = Timer()
    t._start = time.perf_counter()
    try:
        yield t          # ← здесь выполняется тело with-блока
    finally:
        t.elapsed = Elapsed(time.perf_counter() - t._start)
```

**Как это работает:**

```
with timed() as t:
    do_work()

↓ эквивалентно:

генератор запускается → выполняется код ДО yield → yield t
  → t попадает в переменную, выполняется тело with-блока
  → при выходе (нормально или исключение) генератор возобновляется → finally
```

| Часть генератора | Роль |
|-----------------|------|
| Код до `yield` | `__enter__` |
| `yield <значение>` | Значение для `as`, пауза на время тела блока |
| `finally` после `yield` | `__exit__` — выполняется всегда |

**Почему обязательно `try/finally`:**

```python
# БЕЗ try/finally — cleanup не выполнится при исключении:
@contextmanager
def bad_timed():
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start  # ← эта строка не выполнится если было исключение!
    print(f"Время: {elapsed}")

# С try/finally — cleanup всегда выполнится:
@contextmanager
def good_timed():
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start  # ← выполнится в любом случае
        print(f"Время: {elapsed}")
```

---

#### `Elapsed` — датакласс с умным `__str__`

```python
@dataclass
class Elapsed:
    seconds: float

    def __str__(self) -> str:
        if self.seconds < 1:
            return f"{int(self.seconds * 1000)}ms"   # 0.025 → "25ms"
        return f"{self.seconds:.2f}s"                 # 1.234 → "1.23s"
```

`__str__` — магический метод, который вызывается когда объект нужно представить как строку: `str(e)`, `f"{e}"`, `print(e)`. Здесь он позволяет писать `f"время: {t.elapsed}"` и получать красивый вывод автоматически.

---

#### `contextlib.suppress` — встроенный подавитель исключений

Стандартная библиотека уже содержит контекст-менеджер для подавления конкретных исключений:

```python
from contextlib import suppress

# Вместо:
try:
    os.remove("temp.txt")
except FileNotFoundError:
    pass   # файла нет — ничего страшного

# Можно писать:
with suppress(FileNotFoundError):
    os.remove("temp.txt")
```

`suppress` реализован через `__exit__` с `return True` для указанных типов исключений — хороший пример того, когда подавление исключений оправдано.

---

#### Контекст-менеджеры в нашем проекте до этой темы

Проект уже использовал контекст-менеджеры — теперь понятно как они работают изнутри:

| Место | Менеджер | Что делает при выходе |
|-------|---------|----------------------|
| `output.py` | `with Progress(...) as progress:` | Останавливает и очищает прогресс-бар |
| `conftest.py` | `with TestClient(app) as client:` | Запускает/останавливает FastAPI lifecycle |
| `test_scanner.py` | `with pytest.raises(SomeError):` | Проверяет что исключение было брошено |

---

#### Итоговый код

**`core/timer.py`** — класс-based и generator-based менеджеры:

```python
class Timer:
    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.elapsed = Elapsed(time.perf_counter() - self._start)
        return False


@contextmanager
def timed() -> Generator[Timer, None, None]:
    t = Timer()
    t._start = time.perf_counter()
    try:
        yield t
    finally:
        t.elapsed = Elapsed(time.perf_counter() - t._start)
```

**`cli.py`** — Timer оборачивает `scan_files`, elapsed передаётся в вывод:

```python
# scan команда:
with Timer() as t:
    result = scan_files(input_dir=input_dir, extension=extension, recursive=recursive)
print_scan_results(result, elapsed=t.elapsed)
# → "Найдено: 5 файл(ов)  12ms"

# process команда:
with Timer() as process_timer:
    process_result = process_files_with_progress(scan_result.files, output_dir)
print_process_results(process_result, elapsed=process_timer.elapsed)
# → "Готово: скопировано 5 файл(ов) в data/output  43ms"
```

**`output.py`** — функции принимают опциональный `elapsed`:

```python
def print_scan_results(result: ScanResult, elapsed: Elapsed | None = None) -> None:
    ...
    timing = f"  [dim]{elapsed}[/dim]" if elapsed else ""
    console.print(f"Найдено: [bold]{result.total}[/bold] файл(ов){timing}")
```

---

#### Класс vs `@contextmanager` — когда что выбирать

| | Класс с `__enter__`/`__exit__` | `@contextmanager` |
|---|---|---|
| Синтаксис | Больше кода | Компактнее |
| Состояние | Легко хранить в `self` | Через локальные переменные до/после `yield` |
| Переиспользование | Удобно наследовать | Нельзя |
| Читаемость | Явная структура | Нагляднее для простых случаев |
| Когда выбирать | Сложная логика, хранение состояния | Простой setup/teardown |

В проекте `Timer` реализован обоими способами — `Timer` (класс) и `timed()` (генератор) делают одно и то же. В `cli.py` используется `Timer`, потому что нам нужен доступ к `t.elapsed` после блока.

---

## Зависимости

| Библиотека | Назначение | Тип |
|------------|-----------|-----|
| `typer` | Создание CLI команд, парсинг аргументов | основная |
| `python-dotenv` | Чтение `.env` файлов | основная |
| `rich` | Цвета, таблицы, прогресс-бар в терминале | основная |
| `pydantic-settings` | Типизированная конфигурация из `.env` | основная |
| `fastapi` | REST API фреймворк | основная |
| `uvicorn` | ASGI-сервер для запуска FastAPI | основная |
| `pytest` | Запуск и организация тестов | dev |
| `pytest-cov` | Измерение покрытия кода тестами | dev |
| `mypy` | Статическая проверка типов | dev |
| `ruff` | Линтер + форматтер кода | dev |
| `pre-commit` | Автозапуск проверок перед git commit | dev |
| `httpx` | HTTP-клиент для TestClient в тестах FastAPI | dev |

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
