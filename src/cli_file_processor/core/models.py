"""
Доменные модели проекта.

Dataclasses описывают структуры данных, которые передаются между слоями:
scanner.py → cli.py/api.py/output.py

Ключевое правило: dataclass описывает ЧТО, а не КАК.
Никакой логики ввода-вывода — только данные и их свойства.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ScanResult:
    """
    Результат сканирования папки.

    Содержит не только файлы, но и контекст сканирования:
    из какой папки, с каким расширением, был ли рекурсивный поиск.
    """

    files: list[Path]
    scanned_dir: Path
    extension: str
    recursive: bool = False
    # field(default_factory=list) — правильный способ задать пустой список по умолчанию.
    # Нельзя писать errors: list[str] = [] — Python создаст ОДИН список на все экземпляры.
    # default_factory= создаёт новый список для каждого нового объекта.
    errors: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # __post_init__ вызывается автоматически после __init__.
        # Используется для валидации и нормализации данных.
        if not self.extension.startswith("."):
            raise ValueError(f"расширение должно начинаться с точки, получено: {self.extension!r}")

    @property
    def total(self) -> int:
        """Количество найденных файлов. Вычисляется из списка — не хранится отдельно."""
        return len(self.files)


@dataclass(frozen=True)
class ProcessResult:
    """
    Результат операции копирования.

    frozen=True — экземпляр нельзя изменить после создания:
    нельзя переприсвоить processed или output_dir.
    Это гарантирует что результат остаётся неизменным на протяжении всей программы.
    """

    processed: list[Path]
    output_dir: Path

    @property
    def total(self) -> int:
        """Количество скопированных файлов."""
        return len(self.processed)
