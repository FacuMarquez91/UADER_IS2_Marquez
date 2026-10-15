"""Pruebas funcionales del filtro como comando."""

import subprocess
import sys
from pathlib import Path


def run(*args: str, input_text: str = "") -> subprocess.CompletedProcess[str]:
    """Ejecuta el programa en un proceso nuevo."""
    return subprocess.run(
        [sys.executable, "json2csv.py", *args],
        input=input_text,
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )


def test_stream_filter() -> None:
    """Funciona con stdin y stdout sin argumentos."""
    result = run(input_text='[{"a":1}]')
    assert result.returncode == 0
    assert result.stdout == "a\n1\n"


def test_input_output_files(tmp_path: Path) -> None:
    """Convierte archivos utilizando las opciones solicitadas."""
    source = tmp_path / "input.txt"
    target = tmp_path / "output.txt"
    source.write_text('[{"a":1,"b":2}]', encoding="utf-8")
    result = run("-i", str(source), "-o", str(target), "-d", ";")
    assert result.returncode == 0
    assert target.read_text(encoding="utf-8") == "a;b\n1;2\n"


def test_invalid_input() -> None:
    """Informa errores por stderr y devuelve código no cero."""
    result = run(input_text="invalido")
    assert result.returncode == 1
    assert "Error:" in result.stderr
    assert result.stdout == ""


def test_missing_input_file() -> None:
    """Controla archivos inexistentes."""
    result = run("-i", "archivo_inexistente_x_12345.json")
    assert result.returncode == 1
    assert "Error:" in result.stderr


def test_same_input_output(tmp_path: Path) -> None:
    """No sobrescribe el archivo de entrada."""
    source = tmp_path / "data.json"
    source.write_text('{"x":1}', encoding="utf-8")
    result = run("-i", str(source), "-o", str(source))
    assert result.returncode == 1
    assert source.read_text(encoding="utf-8") == '{"x":1}'
