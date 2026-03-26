#!/usr/bin/python3
# Python program to display all the prime numbers within an interval


#Programa que muestra todos los números primos 

#Definición de limites
lower = 1 #Limite inferior
upper = 500 #Limite superior

#Titulo del programa
print("Prime numbers between", lower, "and", upper, "are:")

for num in range(lower, upper + 1):
   # Verifica que los números esan mayores que 1
   if num > 1:
       for i in range(2, num): # Verifica si el número puede dividirse entre 2 
           if (num % i) == 0:
               break
       else: #Si no se encontró divisor, es primo
           print(num)
