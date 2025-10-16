#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* collatz.py                                                              *
#* Calcula la conjetura de Collatz para números entre 1 y 10,000           *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import matplotlib.pyplot as plt

def collatz_iterations(n, max_iter=1000, max_value=10**6):
    count = 0
    seen = set()  # Para detectar ciclos

    while n != 1 and count < max_iter:
        if n in seen or n > max_value:  # Si hay ciclo o el número crece demasiado, detenemos
            return max_iter
        seen.add(n)

        if n % 2 == 0:
            n = n // 2
        else:
            n = 2 * n + 1  # Variante 2n+1 de Collatz
        count += 1

    return count

# Generar datos
n_values = list(range(1, 10001))
iterations = [collatz_iterations(n) for n in n_values]

# Crear gráfico
plt.figure(figsize=(10, 6))
plt.scatter(iterations, n_values, color="blue", s=1)
plt.xlabel("Número de iteraciones")
plt.ylabel("Número inicial n")
plt.title("Conjetura de Collatz (variante 2n+1)")

# Guardar gráfico
plt.savefig("collatz_plot.png")
plt.show()

