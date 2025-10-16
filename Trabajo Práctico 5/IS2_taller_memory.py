import os
#*--------------------------------------------------------------------
#* Design pattern Memento con historial de hasta 4 estados
#*--------------------------------------------------------------------

class Memento:
    """Guarda estado del archivo: nombre y contenido."""
    def __init__(self, file, content):
        self.file = file
        self.content = content


class FileWriterUtility:
    """Originator que puede escribir, salvar y deshacer."""
    def __init__(self, file):
        self.file = file
        self.content = ""

    def write(self, string):
        self.content += string

    def save(self):
        return Memento(self.file, self.content)

    def undo(self, memento):
        self.file = memento.file
        self.content = memento.content


class FileWriterCaretaker:
    """Caretaker que guarda hasta 4 mementos ciclando en buffer."""
    def __init__(self, capacidad=4):
        self.capacidad = capacidad
        self._history = []  # lista de Mementos

    def save(self, writer):
        m = writer.save()
        if len(self._history) >= self.capacidad:
            # descartar el más viejo
            self._history.pop(0)
        self._history.append(m)

    def undo(self, writer, steps=0):
        """
        steps=0: inmediato anterior (penúltimo salvo),
        1: el anterior al anterior, etc.
        """
        # índice del penúltimo = len-2, luego retrocedemos 'steps'
        idx = len(self._history) - 2 - steps
        if idx < 0 or idx >= len(self._history):
            print("No hay estado para ese undo (paso fuera de rango).")
            return
        m = self._history[idx]
        writer.undo(m)
        print(f"Deshizo a estado #{idx} (steps={steps}).")


if __name__ == '__main__':
    #os.system("clear")
    print("== Memento con historial de hasta 4 estados (corregido)==\n")
    caretaker = FileWriterCaretaker(capacidad=4)
    writer = FileWriterUtility("GFG.txt")

    print("Escribo primera línea y salvo")
    writer.write("Linea 1: Clase IS2 en UADER\n")
    print(writer.content)
    caretaker.save(writer)

    print("Escribo segunda línea y salvo")
    writer.write("Linea 2: Material de patrones\n")
    print(writer.content)
    caretaker.save(writer)

    print("Escribo tercera línea y salvo")
    writer.write("Linea 3: Ejemplos extra\n")
    print(writer.content)
    caretaker.save(writer)

    print("Escribo cuarta línea y salvo")
    writer.write("Linea 4: Más ejemplos\n")
    print(writer.content)
    caretaker.save(writer)

    print("Escribo quinta línea y salvo (debería descartar la primera)")
    writer.write("Linea 5: Último estado\n")
    print(writer.content)
    caretaker.save(writer)

    # Probamos undo con distintos steps
    print("\n-- Undo step=0 (último anterior) --")
    caretaker.undo(writer, steps=0)
    print(writer.content)

    print("\n-- Undo step=1 (anterior) --")
    caretaker.undo(writer, steps=1)
    print(writer.content)

    print("\n-- Undo step=3 (más antiguo disponible) --")
    caretaker.undo(writer, steps=3)
    print(writer.content)

    print("\n-- Undo step=4 (fuera de rango) --")
    caretaker.undo(writer, steps=4)