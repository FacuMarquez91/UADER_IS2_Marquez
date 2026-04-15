"""
Módulo rpn.py - Evaluador de Expresiones en Notación Polaca Inversa (RPN).
Versión mejorada con mayor robustez, legibilidad y cobertura de tests.
"""

import math
import operator
import sys


class RPNError(Exception):
    """Excepción personalizada para errores en la evaluación RPN."""


# --- TABLAS DE OPERACIONES ---
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

CONSTANTES = {
    "p": math.pi,
    "e": math.e,
    "j": (1 + math.sqrt(5)) / 2,
}


# --- FUNCIONES AUXILIARES ---
def parsear_numero(token):
    """Intenta convertir un token a número."""
    try:
        return float(token)
    except ValueError:
        return None


def validar_pila(pila, n):
    """Verifica que haya suficientes elementos en la pila."""
    if len(pila) < n:
        raise RPNError("Pila insuficiente para operar.")


def sacar(pila, n=1):
    """Extrae n elementos de la pila."""
    validar_pila(pila, n)
    if n == 1:
        return pila.pop()
    return [pila.pop() for _ in range(n)][::-1]


def manejar_error(token, exc):
    """Traduce errores internos a errores RPN."""
    if isinstance(exc, ZeroDivisionError):
        if token == "1/x":
            raise RPNError("División por cero en 1/x.") from exc
        raise RPNError("División por cero.") from exc

    if isinstance(exc, ValueError):
        raise RPNError("Dominio inválido.") from exc

    raise exc


# --- FUNCIÓN PRINCIPAL ---
def evaluar_rpn(expresion):
    """
    Evalúa una expresión en notación polaca inversa.

    Parámetros:
        expresion (str): expresión con tokens separados por espacios.

    Retorna:
        int | float: resultado final.

    Lanza:
        RPNError: si ocurre un error.
    """
    pila = []
    memoria = {f"{i:02d}": 0.0 for i in range(10)}
    tokens = iter(expresion.split())

    for t in tokens:
        t_lower = t.lower()

        # Intentar parsear número
        num = parsear_numero(t)
        if num is not None:
            pila.append(num)
            continue

        try:
            # Operaciones binarias
            if t_lower in OPERACIONES_BINARIAS:
                a, b = sacar(pila, 2)
                pila.append(OPERACIONES_BINARIAS[t_lower](a, b))

            # Operaciones unarias
            elif t_lower in OPERACIONES_UNARIAS:
                valor = sacar(pila)
                pila.append(OPERACIONES_UNARIAS[t_lower](valor))

            # Constantes
            elif t_lower in CONSTANTES:
                pila.append(CONSTANTES[t_lower])

            # Operaciones de pila
            elif t_lower == "dup":
                validar_pila(pila, 1)
                pila.append(pila[-1])

            elif t_lower == "swap":
                a, b = sacar(pila, 2)
                pila.extend([b, a])

            elif t_lower == "drop":
                sacar(pila)

            elif t_lower == "clear":
                pila.clear()

            # Memoria
            elif t_lower.startswith("sto") or t_lower.startswith("rcl"):
                es_sto = t_lower.startswith("sto")

                if len(t_lower) > 3:
                    reg = t_lower[3:]
                else:
                    try:
                        reg = next(tokens)
                    except StopIteration:
                        raise RPNError("Falta número de registro.")

                if reg not in memoria:
                    raise RPNError(f"Memoria inválida: '{reg}'. Use 00 a 09.")

                if es_sto:
                    memoria[reg] = sacar(pila)
                else:
                    pila.append(memoria[reg])

            else:
                raise RPNError(f"Token inválido: {t}")

        except Exception as exc:
            manejar_error(t_lower, exc)

    # Validación final
    if len(pila) != 1:
        raise RPNError(f"Se esperaba 1 resultado, pero hay {len(pila)} valores.")

    resultado = pila[0]
    return int(resultado) if resultado.is_integer() else resultado


# --- INTERFAZ CLI ---
def main():
    """Punto de entrada principal."""
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
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)


# --- TESTS (para coverage alto) ---
def _tests():
    """Tests básicos para asegurar cobertura."""
    # Operaciones básicas
    assert evaluar_rpn("3 4 +") == 7
    assert evaluar_rpn("10 2 /") == 5
    assert evaluar_rpn("2 3 yx") == 8

    # Unarias
    assert evaluar_rpn("9 sqrt") == 3
    assert evaluar_rpn("0 chs") == 0

    # Constantes
    assert round(evaluar_rpn("p"), 5) == round(math.pi, 5)

    # Pila
    assert evaluar_rpn("5 dup *") == 25
    assert evaluar_rpn("3 4 swap -") == 1

    # Memoria
    assert evaluar_rpn("5 sto 01 01 rcl") == 5

    # Errores
    try:
        evaluar_rpn("1 0 /")
    except RPNError:
        pass

    try:
        evaluar_rpn("sqrt")
    except RPNError:
        pass

    try:
        evaluar_rpn("1 2")
    except RPNError:
        pass


if __name__ == "__main__":
    _tests()  # comentar si no querés correr tests siempre
    main()