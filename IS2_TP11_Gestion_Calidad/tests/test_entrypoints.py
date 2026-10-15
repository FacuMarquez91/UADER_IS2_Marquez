"""Cobertura del flujo principal de los comandos y del cálculo."""

import io
import sys
from pathlib import Path

import pytest

from tp11_calidad.cli import main as cli_main
from tp11_calidad.collatz import main as collatz_main


def test_cli_stdin_stdout(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Ejecuta el filtro con entrada y salida estándar."""
    monkeypatch.setattr(sys, "stdin", io.StringIO('{"a":1}'))
    assert cli_main([]) == 0
    assert capsys.readouterr().out == "a\n1\n"


def test_cli_file(tmp_path: Path) -> None:
    """Ejecuta la ruta de archivos con delimitador alternativo."""
    source = tmp_path / "in.json"
    target = tmp_path / "out.csv"
    source.write_text('{"a":1,"b":2}', encoding="utf-8")
    assert cli_main(["-i", str(source), "-o", str(target), "-d", ";"]) == 0
    assert target.read_text(encoding="utf-8") == "a;b\n1;2\n"


def test_cli_error(capsys: pytest.CaptureFixture[str]) -> None:
    """Controla errores con archivo inexistente."""
    assert cli_main(["-i", "no_existe_832499.json"]) == 1
    assert "Error:" in capsys.readouterr().err


def test_cli_same_path(tmp_path: Path) -> None:
    """Evita sobrescritura del original."""
    source = tmp_path / "in.json"
    source.write_text('{"a":1}', encoding="utf-8")
    assert cli_main(["-i", str(source), "-o", str(source)]) == 1


@pytest.mark.parametrize("value", ["20", "0", "abc"])
def test_collatz_main(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], value: str
) -> None:
    """Cubre éxito y errores de la interacción por teclado."""
    monkeypatch.setattr("builtins.input", lambda _prompt: value)
    collatz_main()
    output = capsys.readouterr().out
    assert ("Error:" in output) if value != "20" else ("20 es 7" in output)


def test_collatz_eof(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """Cubre ausencia de datos de entrada."""

    def fail(_prompt: str) -> str:
        raise EOFError("Sin datos")

    monkeypatch.setattr("builtins.input", fail)
    collatz_main()
    assert "Error:" in capsys.readouterr().out
