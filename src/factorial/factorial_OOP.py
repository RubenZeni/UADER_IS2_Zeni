#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número usando POO                            *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys

class Factorial:
    def __init__(self, num):
        self.num = num

    def calcular(self):
        if self.num < 0:
            print("Factorial de un número negativo no existe")
            return 0
        elif self.num == 0:
            return 1
        else:
            fact = 1
            for i in range(1, self.num + 1):
                fact *= i
            return fact

if __name__ == "__main__":
    if len(sys.argv) < 2:
        entrada = input("Ingrese un número o rango (ej. 4-8): ")
    else:
        entrada = sys.argv[1]

    # Manejo de rangos
    if "-" in entrada:
        partes = entrada.split("-")
        desde = int(partes[0]) if partes[0] else 1
        hasta = int(partes[1]) if partes[1] else 60
    else:
        desde, hasta = int(entrada), int(entrada)

    for i in range(desde, hasta + 1):
        fact_obj = Factorial(i)
        print(f"Factorial {i}! es {fact_obj.calcular()}")


