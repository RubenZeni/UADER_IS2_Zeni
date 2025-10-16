# factorial_singleton.py
# Patrones de Creación – Singleton
# Unica instancia que calcula factorial

class FactorialCalculator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def factorial(self, n: int) -> int:
        """Calcula el factorial de n (n!). Lanza ValueError si n < 0."""
        if n < 0:
            raise ValueError("El factorial no está definido para n < 0")
        resultado = 1
        for i in range(2, n+1):
            resultado *= i
        return resultado

# Ejemplo rápido
if __name__ == "__main__":
    f1 = FactorialCalculator()
    f2 = FactorialCalculator()
    print(f1 is f2)            # True: misma instancia
    print(f1.factorial(5))     # 120
    print(f2.factorial(0))     # 1
