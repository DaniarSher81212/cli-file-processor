"""
REST API модуль проекта.

FastAPI-интерфейс поверх той же бизнес-логики что и CLI.
scanner.py и processor.py не знают ни о CLI, ни об API —
они просто работают с файлами.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from cli_file_processor.config import settings
from cli_file_processor.core.scanner import scan_files
from cli_file_processor.exceptions import InputDirNotFoundError, InputNotADirectoryError

# FastAPI() — создаём объект приложения.
# title и description появятся в автодокументации (/docs).
app = FastAPI(
    title="CLI File Processor API",
    description="REST API для поиска и обработки файлов.",
    version=settings.app_version,
)


# ─── Схемы ответов ────────────────────────────────────────────────────────────

# BaseModel из Pydantic — описывает структуру JSON-ответа.
# FastAPI автоматически сериализует объекты этих классов в JSON.


class FileInfo(BaseModel):
    """Информация об одном файле."""

    name: str  # имя файла
    path: str  # полный путь
    size: int  # размер в байтах
    extension: str  # расширение


class ScanResponse(BaseModel):
    """HTTP-ответ эндпоинта /scan."""

    total: int  # сколько файлов найдено
    files: list[FileInfo]  # список файлов


class HealthResponse(BaseModel):
    """Ответ на проверку работоспособности."""

    status: str
    version: str


# ─── Эндпоинты ────────────────────────────────────────────────────────────────


# @app.get("/health") — регистрирует GET /health эндпоинт.
# response_model — FastAPI проверит что ответ соответствует схеме.
@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Проверка что API работает."""
    return HealthResponse(status="ok", version=settings.app_version)


@app.get("/scan", response_model=ScanResponse)
def scan(
    # Query() — параметр из URL: /scan?extension=.txt&input_dir=data/input
    # default= — значение если параметр не передан.
    extension: str = Query(default=settings.default_extension),
    input_dir: str = Query(default=str(settings.default_input_dir)),
    recursive: bool = Query(default=False),
) -> ScanResponse:
    """
    Ищет файлы с указанным расширением в папке.

    Примеры запросов:
        GET /scan
        GET /scan?extension=.pdf
        GET /scan?extension=.txt&input_dir=data/input&recursive=true
    """
    dir_path = Path(input_dir)

    # API ловит конкретные типы исключений и маппит каждый в свой HTTP-код.
    # CLI делает то же самое, но реагирует иначе: печатает текст и выходит с кодом 1.
    try:
        scan_result = scan_files(input_dir=dir_path, extension=extension, recursive=recursive)
    except InputDirNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InputNotADirectoryError as e:
        raise HTTPException(status_code=400, detail=str(e))

    file_infos = [
        FileInfo(
            name=f.name,
            path=str(f),
            size=f.stat().st_size,
            extension=f.suffix,
        )
        for f in scan_result.files
    ]

    return ScanResponse(total=scan_result.total, files=file_infos)
