#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys
def factorial(num): 
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
        
    else: 
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 

if len(sys.argv) < 2:
    entrada = input("Ingrese un número o rango (ej. 4-8): ")
else:
    entrada=(sys.argv[1])

# Verificar si es un rango
if "-" in entrada:
    partes = entrada.split("-")
    desde = int(partes[0]) if partes[0] else 1
    hasta = int(partes[1]) if partes[1] else 60
else:
    desde, hasta = int(entrada), int(entrada)

# Calcular factoriales en el rango
for i in range(desde, hasta + 1):
    print(f"Factorial {i}! es {factorial(i)}") 

