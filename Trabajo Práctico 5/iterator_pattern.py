# iterator_pattern.py

class CadenaIterator:
    """Iterador que recorre una cadena forward o reverse."""
    def __init__(self, cadena, reverse=False):
        self._cadena = cadena
        self._reverse = reverse
        self._index = len(cadena) - 1 if reverse else 0

    def __iter__(self):
        return self

    def __next__(self):
        if not self._reverse and self._index >= len(self._cadena):
            raise StopIteration
        if self._reverse and self._index < 0:
            raise StopIteration

        caracter = self._cadena[self._index]
        self._index += -1 if self._reverse else 1
        return caracter


class Cadena:
    """Agrega métodos para recorrer in y reverse."""
    def __init__(self, texto):
        self.texto = texto

    def __iter__(self):
        return CadenaIterator(self.texto, reverse=False)

    def reverse_iterator(self):
        return CadenaIterator(self.texto, reverse=True)


if __name__ == "__main__":
    c = Cadena("¡Hola!")
    print("Recorrido forward:")
    for ch in c:
        print(ch, end=' ')
    print("\nRecorrido reverse:")
    for ch in c.reverse_iterator():
        print(ch, end=' ')
    print()