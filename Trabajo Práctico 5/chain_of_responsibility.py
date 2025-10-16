# chain_of_responsibility.py

class Handler:
    """Clase base del patrón Cadena de Responsabilidad."""
    def __init__(self, siguiente=None):
        self.siguiente = siguiente

    def manejar(self, número):
        """Intenta procesar; si no, deriva al siguiente."""
        if self.siguiente:
            return self.siguiente.manejar(número)
        else:
            print(f"No consumido: {número}")
            return False


class PrimoHandler(Handler):
    def __init__(self, siguiente=None):
        super().__init__(siguiente)

    def es_primo(self, n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def manejar(self, número):
        if self.es_primo(número):
            print(f"PrimoHandler consumió: {número}")
            return True
        else:
            return super().manejar(número)


class ParHandler(Handler):
    def __init__(self, siguiente=None):
        super().__init__(siguiente)

    def manejar(self, número):
        if número % 2 == 0:
            print(f"ParHandler consumió: {número}")
            return True
        else:
            return super().manejar(número)


if __name__ == "__main__":
    # Armo la cadena: Primo -> Par -> (final)
    handler = PrimoHandler(ParHandler())

    # Paso del 1 al 100
    for num in range(1, 101):
        handler.manejar(num)