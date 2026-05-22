"""
Конфигурация приложения.

Использует Pydantic Settings: читает переменные из .env,
валидирует типы и предоставляет единый объект настроек.
"""

from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Все настройки приложения в одном месте.

    Pydantic автоматически:
    - читает переменные из .env (через model_config)
    - конвертирует строки в нужные типы (str → Path)
    - валидирует значения через field_validator
    """

    # Каждое поле = одна настройка.
    # Тип поля (Path, str) — Pydantic приведёт к нему значение из .env.
    # Значение после = — дефолт если переменная не задана.
    default_input_dir: Path = Path("data/input")
    default_extension: str = ".txt"
    default_output_dir: Path = Path("data/output")
    app_version: str = "0.1.0"

    # model_config — настройки самого класса Settings.
    # env_file=".env" — читать переменные из этого файла.
    # env_file_encoding="utf-8" — кодировка файла.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # field_validator — валидатор конкретного поля.
    # Запускается после чтения значения, до сохранения в объект.
    @field_validator("default_extension")
    @classmethod
    def extension_must_start_with_dot(cls, value: str) -> str:
        """Расширение должно начинаться с точки."""
        if not value.startswith("."):
            return f".{value}"
        return value


# Единственный экземпляр настроек — создаётся один раз при импорте.
# Все модули импортируют этот объект, а не создают свой.
settings = Settings()


# Функции-обёртки сохраняем для обратной совместимости с cli.py.
# Они делегируют к объекту settings.
def get_default_input_dir() -> Path:
    return settings.default_input_dir


def get_default_extension() -> str:
    return settings.default_extension


def get_default_output_dir() -> Path:
    return settings.default_output_dir


def get_app_version() -> str:
    return settings.app_version
