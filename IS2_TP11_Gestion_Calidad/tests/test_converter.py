"""Pruebas unitarias del conversor y entradas inválidas."""

import io

import pytest

from tp11_calidad.converter import ConversionError, json_to_csv


def convert(value: str, delimiter: str = ",") -> str:
    """Convierte contenido JSON en memoria."""
    output = io.StringIO()
    json_to_csv(io.StringIO(value), output, delimiter)
    return output.getvalue()


def test_list_of_objects() -> None:
    """Genera encabezados y filas."""
    assert convert('[{"a":1,"b":"hola"},{"a":2,"b":"chau"}]') == "a,b\n1,hola\n2,chau\n"


def test_object() -> None:
    """Admite un objeto único."""
    assert convert('{"x":1}') == "x\n1\n"


def test_union_columns() -> None:
    """Combina claves de distintas filas manteniendo su orden."""
    assert convert('[{"a":1},{"b":2}]') == "a,b\n1,\n,2\n"


def test_escaping() -> None:
    """Escapa saltos, delimitadores y comillas con reglas CSV."""
    assert (
        convert('{"a":"hola, mundo","b":"dijo \\"sí\\""}') == 'a,b\n"hola, mundo","dijo ""sí"""\n'
    )


def test_tab_separator() -> None:
    """Permite otro delimitador."""
    assert convert('{"a":1,"b":2}', ";") == "a;b\n1;2\n"


def test_scalar_types() -> None:
    """Representa nulos y booleanos."""
    assert convert('{"a":null,"b":true,"c":false}') == "a,b,c\n,true,false\n"


@pytest.mark.parametrize(
    "value", ["", "no json", "[]", "null", "5", "[1,2]", '{"a":{"b":2}}', '{"a":[1,2]}', "{}"]
)
def test_bad_payload(value: str) -> None:
    """Rechaza entradas inadecuadas."""
    with pytest.raises(ConversionError):
        convert(value)


@pytest.mark.parametrize("delimiter", ["", "::", '"', "\n"])
def test_bad_delimiter(delimiter: str) -> None:
    """Valida el delimitador."""
    with pytest.raises(ConversionError):
        convert('{"a":1}', delimiter)
