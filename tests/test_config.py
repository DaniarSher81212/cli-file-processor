"""
Тесты для модуля config.py.

Юнит-тесты — проверяют что функции конфигурации возвращают
правильные значения по умолчанию.
"""

from pathlib import Path

from cli_file_processor.config import (
    get_app_version,
    get_default_extension,
    get_default_input_dir,
    get_default_output_dir,
)


def test_get_default_input_dir_returns_path():
    result = get_default_input_dir()
    assert isinstance(result, Path)


def test_get_default_input_dir_default_value():
    result = get_default_input_dir()
    assert result == Path("data/input")


def test_get_default_extension_returns_str():
    result = get_default_extension()
    assert isinstance(result, str)


def test_get_default_extension_default_value():
    result = get_default_extension()
    assert result == ".txt"


def test_get_default_output_dir_returns_path():
    result = get_default_output_dir()
    assert isinstance(result, Path)


def test_get_default_output_dir_default_value():
    result = get_default_output_dir()
    assert result == Path("data/output")


def test_get_app_version_returns_str():
    result = get_app_version()
    assert isinstance(result, str)


def test_get_app_version_format():
    result = get_app_version()
    # Версия должна быть в формате X.Y.Z
    parts = result.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
