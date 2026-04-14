"""
Módulo rpn.py - Evaluador de Expresiones en Notación Polaca Inversa (RPN).
"""

import sys
import math
import operator


class RPNError(Exception):
    """Excepción personalizada para errores específicos en la evaluación RPN."""


# --- TABLAS DE DESPACHO ---
OPERACIONES_BINARIAS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "yx": operator.pow,
}

OPERACIONES_UNARIAS = {
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "ex": math.exp,
    "10x": lambda x: 10**x,
    "1/x": lambda x: 1 / x,
    "chs": operator.neg,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tg": lambda x: math.tan(math.radians(x)),
    "asin": lambda x: math.degrees(math.asin(x)),
    "acos": lambda x: math.degrees(math.acos(x)),
    "atg": lambda x: math.degrees(math.atan(x)),
}

CONSTANTES = {"p": math.pi, "e": math.e, "j": (1 + math.sqrt(5)) / 2}
# ------------------------------------------------------------------------


# pylint: disable=too-many-branches, too-many-statements
def evaluar_rpn(expresion):
    """Procesa y evalúa una cadena de texto que contiene una expresión RPN."""
    pila = []
    memoria = {f"{i:02d}": 0.0 for i in range(10)}

    def sacar(n=1):
        """Extrae uno o más elementos de la cima de la pila principal."""
        try:
            if n == 1:
                return pila.pop()
            return [pila.pop() for _ in range(n)][::-1]
        except IndexError as exc:
            raise RPNError("Pila insuficiente para operar.") from exc

    tokens = iter(expresion.split())

    for t in tokens:
        try:
            pila.append(float(t))
            continue
        except ValueError:
            # Si no es número, seguimos con la lógica. (Pylint odia 'pass' aquí,
            # pero es necesario, por eso lo desactivamos en la línea).
            pass  # pylint: disable=unnecessary-pass

        t_lower = t.lower()

        try:
            if t_lower in OPERACIONES_BINARIAS:
                a, b = sacar(2)
                pila.append(OPERACIONES_BINARIAS[t_lower](a, b))

            elif t_lower in OPERACIONES_UNARIAS:
                pila.append(OPERACIONES_UNARIAS[t_lower](sacar()))

            elif t_lower in CONSTANTES:
                pila.append(CONSTANTES[t_lower])

            elif t_lower == "dup":
                pila.append(pila[-1] if pila else sacar())
            elif t_lower == "swap":
                a, b = sacar(2)
                pila.extend([b, a])
            elif t_lower == "drop":
                sacar()
            elif t_lower == "clear":
                pila.clear()

            elif t_lower.startswith("sto") or t_lower.startswith("rcl"):
                es_sto = t_lower.startswith("sto")
                reg = t_lower[3:] if len(t_lower) > 3 else next(tokens, None)

                if reg not in memoria:
                    raise RPNError(f"Memoria inválida: '{reg}'. Use 00 a 09.")

                if es_sto:
                    memoria[reg] = sacar()
                else:
                    pila.append(memoria[reg])
            else:
                raise RPNError(f"Token inválido detectado: {t}")

        except ZeroDivisionError as exc:
            if t_lower == "1/x":
                raise RPNError("División por cero en 1/x.") from exc
            raise RPNError("División por cero.") from exc
        except ValueError as exc:
            raise RPNError("Raíz cuadrada de negativos o dominio inválido.") from exc

    try:
        # pylint: disable=unbalanced-tuple-unpacking
        [res] = pila
        return int(res) if res.is_integer() else res
    except ValueError as exc:
        raise RPNError(
            f"Debe quedar 1 valor en la pila. Quedaron {len(pila)}."
        ) from exc


def main():
    """Punto de entrada principal de la aplicación."""
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
    else:
        try:
            expr = input("Ingrese la expresión RPN: ")
        except EOFError:
            return

    if not expr.strip():
        return

    try:
        resultado = evaluar_rpn(expr)
        print(resultado)
    except RPNError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
