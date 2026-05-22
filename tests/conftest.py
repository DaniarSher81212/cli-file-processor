"""
Общие pytest fixtures для всех тестов проекта.

conftest.py — специальный файл: pytest находит его автоматически
и делает все fixtures доступными в любом файле тестов в той же директории.
Не нужно ничего импортировать вручную.
"""

from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from cli_file_processor.api import app


@pytest.fixture
def sample_txt_dir(tmp_path: Path) -> Path:
    """Папка с 2 .txt и 1 .pdf файлами — стандартный набор для тестов scanner."""
    (tmp_path / "file1.txt").touch()
    (tmp_path / "file2.txt").touch()
    (tmp_path / "report.pdf").touch()
    return tmp_path


# Обе фикстуры используют tmp_path — pytest гарантирует что они получат
# один и тот же tmp_path в рамках одного теста. Файлы окажутся в одной папке.
@pytest.fixture
def input_dir(tmp_path: Path) -> Path:
    """Создаёт tmp_path/input/ и возвращает путь к ней."""
    d = tmp_path / "input"
    d.mkdir()
    return d


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Путь к tmp_path/output/ (папка намеренно не создаётся — тест проверит это сам)."""
    return tmp_path / "output"


# scope="module" — фикстура создаётся один раз на весь файл тестов, не на каждый тест.
# Это важно для TestClient: поднять FastAPI-приложение дорого, делаем это один раз.
@pytest.fixture(scope="module")
def api_client() -> Generator[TestClient, None, None]:
    """
    FastAPI TestClient с правильным lifecycle.

    yield — разделяет setup (до yield) и teardown (после yield).
    with TestClient(app) запускает startup-события FastAPI при входе
    и shutdown-события при выходе. Это точная имитация продакшен-запуска.
    """
    with TestClient(app) as client:
        yield client
        # teardown: FastAPI shutdown events запустятся здесь автоматически
