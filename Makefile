# Переменная — путь к Python в виртуальном окружении.
# Используем его явно чтобы не зависеть от активации venv.
PYTHON := .venv/bin/python

# .PHONY говорит make: эти цели — не файлы, а команды.
# Без этого make проверял бы: "есть ли файл с именем test?" и не запускал бы цель.
.PHONY: install lint format type-check test build clean help

# Первая цель — запускается по умолчанию при вызове просто make.
help:
	@echo "Доступные команды:"
	@echo "  make install      — установить проект и dev-зависимости"
	@echo "  make lint         — проверить стиль кода (ruff)"
	@echo "  make format       — отформатировать код (ruff format)"
	@echo "  make type-check   — проверить типы (mypy --strict)"
	@echo "  make test         — запустить тесты с покрытием"
	@echo "  make check        — lint + type-check + test (полная проверка)"
	@echo "  make build        — собрать Docker-образ"
	@echo "  make clean        — удалить временные файлы"

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

# check запускает lint, type-check и test последовательно.
# Если одна цель упала — следующие не запустятся (поведение make по умолчанию).
check: lint type-check test

build:
	docker build -t cli-file-processor .

clean:
	rm -rf .coverage htmlcov/ .mypy_cache/ .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
