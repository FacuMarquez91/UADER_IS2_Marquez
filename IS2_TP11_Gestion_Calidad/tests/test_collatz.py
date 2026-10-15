"""Validaciones básicas del algoritmo matemático."""

import pytest

from tp11_calidad.collatz import collatz


@pytest.mark.parametrize("number,expected", [(1, 0), (2, 1), (3, 7), (5, 5), (20, 7), (1999, 50)])
def test_known_sequences(number: int, expected: int) -> None:
    """Reproduce seis casos conocidos."""
    assert collatz(number) == expected


@pytest.mark.parametrize("number", [0, -1, 2000])
def test_bounds(number: int) -> None:
    """Rechaza enteros fuera del dominio permitido."""
    with pytest.raises(ValueError):
        collatz(number)
