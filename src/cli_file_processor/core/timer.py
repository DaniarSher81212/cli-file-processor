"""
Измерение времени выполнения операций.

Демонстрирует два способа создать контекст-менеджер:
  1. Класс с __enter__ / __exit__  (Timer)
  2. Генераторная функция с @contextmanager  (timed)
"""

import time
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class Elapsed:
    """Результат замера времени с удобным строковым представлением."""

    seconds: float

    def __str__(self) -> str:
        # Меньше секунды — показываем миллисекунды: "25ms"
        # Секунда и больше — показываем секунды: "1.23s"
        if self.seconds < 1:
            return f"{int(self.seconds * 1000)}ms"
        return f"{self.seconds:.2f}s"


class Timer:
    """
    Класс-based контекст-менеджер для измерения времени.

    Использование:
        with Timer() as t:
            do_something()
        print(t.elapsed)   # "25ms" или "1.23s"
    """

    def __init__(self) -> None:
        self.elapsed: Elapsed | None = None
        self._start: float = 0.0

    def __enter__(self) -> "Timer":
        # __enter__ вызывается при входе в блок with.
        # Возвращаем self — именно этот объект окажется в переменной after as.
        self._start = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        # __exit__ вызывается при выходе из блока with — ВСЕГДА, даже при исключении.
        # exc_type / exc_val / exc_tb — тип, значение, traceback исключения.
        # Все три None если блок завершился нормально.
        self.elapsed = Elapsed(time.perf_counter() - self._start)
        # None (ничего не возвращаем) = не подавлять исключение.
        # Если бы возвращали True — исключение было бы подавлено.


@contextmanager
def timed() -> Generator[Timer, None, None]:
    """
    Генераторный вариант Timer — то же поведение, другой синтаксис.

    @contextmanager превращает генератор в контекст-менеджер:
      - код до yield      →  __enter__
      - yield <значение>  →  объект, который попадает в переменную after as
      - finally-блок      →  __exit__ (выполняется всегда)

    Использование:
        with timed() as t:
            do_something()
        print(t.elapsed)
    """
    t = Timer()
    t._start = time.perf_counter()
    try:
        # yield приостанавливает генератор и отдаёт t вызывающему коду.
        # Пока выполняется тело with-блока — генератор "заморожен" здесь.
        yield t
    finally:
        # finally выполняется всегда — и при успехе, и при исключении.
        # Именно поэтому @contextmanager требует try/finally для надёжного cleanup.
        t.elapsed = Elapsed(time.perf_counter() - t._start)
