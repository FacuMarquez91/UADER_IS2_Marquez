"""Conversión de documentos JSON a registros CSV con validación explícita."""

import csv
import io
import json
from typing import Any, TextIO, cast


class ConversionError(ValueError):
    """Error de entrada o estructura incompatible con una tabla CSV."""


def _records(data: Any) -> list[dict[str, Any]]:
    """Acepta un objeto JSON o una lista de objetos JSON no anidados."""
    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list) or not data:
        raise ConversionError("Se requiere un objeto o una lista no vacía de objetos JSON.")

    elements = cast(list[object], data)

    records: list[dict[str, Any]] = []

    for element in elements:
        if not isinstance(element, dict):
            raise ConversionError("Todos los elementos deben ser objetos JSON.")

        item = cast(dict[object, Any], element)
        row: dict[str, Any] = {}

        for key, val in item.items():
            if not isinstance(key, str):
                raise ConversionError("Las claves deben ser cadenas.")

            if isinstance(val, (dict, list)):
                raise ConversionError("No se permiten valores JSON anidados.")

            row[key] = val

        records.append(row)

    return records


def json_to_csv(source: TextIO, target: TextIO, delimiter: str = ",") -> None:
    """Convierte JSON leído de source y emite CSV a target."""
    if len(delimiter) != 1 or delimiter in ("\r", "\n", '"'):
        raise ConversionError(
            "El delimitador debe ser un carácter distinto de comillas o salto de línea."
        )
    try:
        data = json.load(source)
    except (ValueError, UnicodeError) as exc:
        raise ConversionError("El contenido de entrada no es JSON válido.") from exc
    rows = _records(data)
    fields = list(dict.fromkeys(key for row in rows for key in row))
    if not fields:
        raise ConversionError("Los objetos deben tener al menos un campo.")
    # Escribir en memoria primero evita archivos CSV parciales ante errores de conversión.
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, delimiter=delimiter, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: _scalar(value) for key, value in row.items()})
    target.write(buffer.getvalue())


def _scalar(value: Any) -> str:
    """Representa escalares JSON de forma inequívoca para CSV."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)
