"""Interfaz de línea de comandos del filtro JSON a CSV."""

import argparse
import io
import os
import sys
import tempfile
from pathlib import Path
from typing import Sequence

from tp11_calidad.converter import ConversionError, json_to_csv


def main(argv: Sequence[str] | None = None) -> int:
    """Procesa opciones, convierte datos y devuelve un código de salida."""
    parser = argparse.ArgumentParser(description="Convierte JSON a CSV.")
    parser.add_argument("-i", "--input", help="Archivo JSON de entrada (por defecto stdin).")
    parser.add_argument("-o", "--output", help="Archivo CSV de salida (por defecto stdout).")
    parser.add_argument("-d", "--delimiter", default=",", help="Delimitador CSV (un carácter).")
    args = parser.parse_args(argv)
    try:
        if args.input and args.output and Path(args.input).resolve() == Path(args.output).resolve():
            raise ConversionError("El archivo de salida debe ser distinto al de entrada.")
        if args.input:
            with open(args.input, encoding="utf-8") as source:
                payload = source.read()
        else:
            payload = sys.stdin.read()
        result = io.StringIO()
        json_to_csv(io.StringIO(payload), result, args.delimiter)
        if args.output:
            destination = Path(args.output)
            # Sustitución atómica para no dejar contenido incompleto ante errores.
            temp_name: str | None = None
            try:
                with tempfile.NamedTemporaryFile(
                    "w", encoding="utf-8", newline="", dir=destination.parent, delete=False
                ) as temp:
                    temp_name = temp.name
                    temp.write(result.getvalue())
                os.replace(temp_name, destination)
            finally:
                if temp_name and os.path.exists(temp_name):
                    os.unlink(temp_name)
        else:
            sys.stdout.write(result.getvalue())
        return 0
    except (ConversionError, OSError, UnicodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
