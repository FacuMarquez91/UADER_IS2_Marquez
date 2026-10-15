"""Cálculo de iteraciones de Collatz y validación de entrada."""


def collatz(numero: int) -> int:
    """Devuelve la cantidad de pasos necesarios hasta alcanzar uno."""
    if not 1 <= numero <= 1999:
        raise ValueError("El número debe estar entre 1 y 1999.")
    pasos = 0
    while numero != 1:
        numero = numero // 2 if numero % 2 == 0 else 3 * numero + 1
        pasos += 1
    return pasos


def main() -> None:
    """Lee un número positivo e informa sus iteraciones."""
    try:
        numero = int(input("Ingrese un número entero entre 1 y 1999: "))
        print(f"El número de iteraciones para {numero} es {collatz(numero)}")
    except (ValueError, EOFError) as exc:
        print(f"Error: entrada inválida: {exc}")


if __name__ == "__main__":
    main()
