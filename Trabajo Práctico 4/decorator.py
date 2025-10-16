from abc import ABC, abstractmethod

# Componente
class Number(ABC):
    @abstractmethod
    def get(self) -> float:
        pass

    @abstractmethod
    def print(self):
        pass

# Componente concreto
class SimpleNumber(Number):
    def __init__(self, value: float):
        self._value = value

    def get(self) -> float:
        return self._value

    def print(self):
        print(f"Valor: {self._value}")

# Decorator base
class NumberDecorator(Number):
    def __init__(self, wrapped: Number):
        self._wrapped = wrapped

    @abstractmethod
    def get(self) -> float:
        pass

    def print(self):
        print(f"Valor decorado: {self.get()}")

# Decorators concretos
class Add2(NumberDecorator):
    def get(self) -> float:
        return self._wrapped.get() + 2

class Mul2(NumberDecorator):
    def get(self) -> float:
        return self._wrapped.get() * 2

class Div3(NumberDecorator):
    def get(self) -> float:
        return self._wrapped.get() / 3

# Ejemplo de uso:
if __name__ == "__main__":
    base = SimpleNumber(10)
    print("Sin decoradores:")
    base.print()

    # Encadenado: ((10 + 2) * 2) / 3
    decorated = Div3(Mul2(Add2(base)))
    print("\nCon decoradores anidados (Add2 → Mul2 → Div3):")
    decorated.print()
