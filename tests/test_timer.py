"""
Тесты для core/timer.py.

Проверяем: Timer, Elapsed, timed() — корректность замера,
поведение при исключении, строковое представление.
"""

import time

import pytest

from cli_file_processor.core.timer import Elapsed, Timer, timed

# ─────────────────────────────────────────────
# Тесты для Elapsed
# ─────────────────────────────────────────────


def test_elapsed_str_milliseconds() -> None:
    # Меньше 1 секунды — выводим миллисекунды
    e = Elapsed(0.025)
    assert str(e) == "25ms"


def test_elapsed_str_zero_ms() -> None:
    e = Elapsed(0.0)
    assert str(e) == "0ms"


def test_elapsed_str_seconds() -> None:
    # 1 секунда и больше — выводим секунды с двумя знаками
    e = Elapsed(1.234)
    assert str(e) == "1.23s"


def test_elapsed_str_boundary() -> None:
    # Ровно 1 секунда — переходим в "секунды"
    e = Elapsed(1.0)
    assert str(e) == "1.00s"


# ─────────────────────────────────────────────
# Тесты для Timer (__enter__ / __exit__)
# ─────────────────────────────────────────────


def test_timer_returns_self_from_enter() -> None:
    # with Timer() as t → t должен быть самим Timer, не None
    with Timer() as t:
        assert isinstance(t, Timer)


def test_timer_sets_elapsed_after_exit() -> None:
    with Timer() as t:
        pass  # блок завершился нормально

    # После выхода из with — elapsed установлен
    assert t.elapsed is not None
    assert isinstance(t.elapsed, Elapsed)


def test_timer_measures_real_time() -> None:
    with Timer() as t:
        time.sleep(0.02)  # 20ms

    assert t.elapsed is not None
    # Даём небольшой запас — sleep не абсолютно точен
    assert t.elapsed.seconds >= 0.015


def test_timer_sets_elapsed_even_on_exception() -> None:
    # __exit__ вызывается даже если внутри блока было исключение.
    # elapsed должен быть зафиксирован до того как исключение пробросится.
    t = Timer()
    with pytest.raises(ValueError):
        with t:
            raise ValueError("тестовое исключение")

    assert t.elapsed is not None


def test_timer_does_not_suppress_exceptions() -> None:
    # __exit__ возвращает False — исключение НЕ подавляется.
    # pytest.raises убеждается что ValueError действительно прошёл наружу.
    with pytest.raises(ValueError, match="должно пробросить"):
        with Timer():
            raise ValueError("должно пробросить")


def test_timer_elapsed_is_none_before_exit() -> None:
    # До выхода из блока elapsed ещё не установлен
    timer = Timer()
    assert timer.elapsed is None
    with timer:
        assert timer.elapsed is None
    assert timer.elapsed is not None


# ─────────────────────────────────────────────
# Тесты для timed() (@contextmanager)
# ─────────────────────────────────────────────


def test_timed_sets_elapsed() -> None:
    with timed() as t:
        pass

    assert t.elapsed is not None


def test_timed_measures_real_time() -> None:
    with timed() as t:
        time.sleep(0.02)

    assert t.elapsed is not None
    assert t.elapsed.seconds >= 0.015


def test_timed_sets_elapsed_on_exception() -> None:
    # finally в генераторе выполняется даже при исключении
    t = Timer()
    with pytest.raises(RuntimeError):
        with timed() as t:
            raise RuntimeError("ошибка внутри timed")

    assert t.elapsed is not None


def test_timed_does_not_suppress_exceptions() -> None:
    with pytest.raises(RuntimeError):
        with timed():
            raise RuntimeError("должно пробросить")
