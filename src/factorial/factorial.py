#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número o rango de números                    *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys

def factorial(num): 
    #Calcula el factorial de un número no negativo
    if num < 0: 
        print("El factorial de un número negativo no existe")
        return 0
    elif num == 0: #factorial de 0 es igual a 1
        return 1
    else:   # calcula el factorial del argumento
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 

# Programa principal
if len(sys.argv) < 2:
    # Si no hay argumento, solicita un número de entrada
    entrada = input("Ingrese un número o rango (ej: 5, 4-8, -10, 5-): ")
else:
    entrada = sys.argv[1] # si hay argumento lo utiliza

# Verificar si el argumento es un rango
if '-' in entrada:
    partes = entrada.split('-')
    
    # Argumento  -10 (no tiene limite inferior, desde 1 hasta 10)
    if partes[0] == '' and partes[1] != '':
        inicio = 1
        fin = int(partes[1]) #limite inferior
        print(f"Calculando factoriales desde {inicio} hasta {fin}:")
        for i in range(inicio, fin + 1): #calcula factorial para cada número
            print(f"Factorial {i}! = {factorial(i)}")
    
    # Argumento 5- (no tiene limite superior, desde 5 hasta 60)
    elif partes[0] != '' and partes[1] == '':
        inicio = int(partes[0])
        fin = 60  # Límite superior
        print(f"Calculando factoriales desde {inicio} hasta {fin}:")
        for i in range(inicio, fin + 1): #calcula el factorial para cada número
            print(f"Factorial {i}! = {factorial(i)}")
    
    # Argumento "4-8" (devuelve el rango)
    elif partes[0] != '' and partes[1] != '':
        inicio = int(partes[0]) #limite inferior
        fin = int(partes[1]) #limite superior
        print(f"Calculando factoriales desde {inicio} hasta {fin}:")
        for i in range(inicio, fin + 1): #calcula factorial para cada número en el rango
            print(f"Factorial {i}! = {factorial(i)}")
    
    else: #Formato ingresado invalido
        print("Formato no válido. Use: 5, 4-8, -10, 5-")
else:
    num = int(entrada)
    print(f"Factorial {num}! = {factorial(num)}")