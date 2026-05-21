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
6. [Зависимости](#зависимости)

---

## Что делает проект

```
cli-file-processor scan    --input-dir data/input --extension .txt
cli-file-processor process --input-dir data/input --output-dir data/output --extension .pdf
```

- **scan** — находит файлы с нужным расширением и показывает их в таблице
- **process** — находит файлы и копирует их в папку назначения с прогресс-баром
- **check** — проверяет что CLI работает

---

## Структура проекта

```
cli_file_processor/
│
├── pyproject.toml              ← паспорт проекта: зависимости, entry point, версия
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
│       ├── cli.py              ← команды CLI: check, scan, process
│       ├── config.py           ← чтение настроек из .env
│       ├── logging_config.py   ← настройка уровней логирования
│       ├── output.py           ← Rich: таблицы, цвета, прогресс-бар
│       └── core/
│           ├── scanner.py      ← бизнес-логика поиска файлов
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

# Установить зависимости для разработки (pytest)
pip install -e ".[dev]"

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

### `scan` — поиск файлов

```bash
# С явными параметрами
cli-file-processor scan --input-dir data/input --extension .txt

# Короткие флаги
cli-file-processor scan -i data/input -e .txt

# Подробный вывод (DEBUG-логи)
cli-file-processor scan -i data/input -e .txt --verbose

# Без параметров — берёт дефолты из .env
cli-file-processor scan
```

Вывод:
```
┏━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┓
┃ Файл      ┃ Расширение ┃ Размер ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━┩
│ file1.txt │ .txt       │ 1.2 KB │
│ file2.txt │ .txt       │ 0.8 KB │
└───────────┴────────────┴────────┘
Найдено: 2 файл(ов)
```

### `process` — копирование файлов

```bash
cli-file-processor process --input-dir data/input --output-dir data/output --extension .txt
```

Вывод:
```
Копирование файлов... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

Готово: скопировано 2 файл(ов) в data/output
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
dev = ["pytest>=8.0.0"]
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

test_normalize_extension_adds_dot          ← добавляет точку
test_scan_files_returns_empty_when_no_match ← пустой список если нет совпадений
test_process_fails_when_input_missing      ← ошибка если папка не найдена
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
table.add_column("Файл",       style="white", no_wrap=True)
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
path.name              # "file.txt"      — только имя файла
path.suffix            # ".txt"          — расширение
path.stem              # "file"          — имя без расширения
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
config.py       ← ТОЛЬКО: читать настройки из .env
logging_config  ← ТОЛЬКО: настроить уровень логирования
output.py       ← ТОЛЬКО: решать как данные выглядят (Rich, таблицы, цвета)
scanner.py      ← ТОЛЬКО: находить файлы по расширению
processor.py    ← ТОЛЬКО: копировать файлы
```

**Как это выглядит в коде:**

```python
# cli.py — команда scan
def scan(input_dir, extension, verbose):
    setup_logging(verbose)               # → logging_config.py
    input_dir = get_default_input_dir()  # → config.py
    files = scan_files(input_dir, ext)   # → scanner.py  (бизнес-логика)
    print_scan_results(files)            # → output.py   (отображение)
```

CLI не знает КАК ищутся файлы и КАК они отображаются — он только координирует.

**Зачем это важно:**
- Хочешь изменить внешний вид таблицы → меняешь только `output.py`
- Хочешь искать файлы рекурсивно → меняешь только `scanner.py`
- Ни в том, ни в другом случае `cli.py` не трогаешь

---

## Зависимости

| Библиотека | Назначение | Установка |
|------------|-----------|-----------|
| `typer` | Создание CLI команд, парсинг аргументов | основная |
| `python-dotenv` | Чтение `.env` файлов | основная |
| `rich` | Цвета, таблицы, прогресс-бар в терминале | основная |
| `pytest` | Запуск и организация тестов | dev |

**Стандартные библиотеки Python (не нужно устанавливать):**

| Библиотека | Что используем |
|------------|---------------|
| `pathlib` | `Path` — работа с путями файловой системы |
| `logging` | Уровни логирования, `basicConfig`, `getLogger` |
| `shutil` | `copy2` — копирование файлов с метаданными |
| `os` | `os.getenv` — чтение переменных окружения |
