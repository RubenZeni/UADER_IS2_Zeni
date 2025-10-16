# prototipo.py
# Patrón Prototype – clonación profunda

import copy

class Documento:
    def __init__(self, titulo: str, contenido: str, metadatos: dict):
        self.titulo = titulo
        self.contenido = contenido
        self.metadatos = metadatos  # p.ej. autor, fecha

    def clone(self) -> "Documento":
        """Devuelve una copia profunda de sí mismo."""
        return copy.deepcopy(self)

    def __str__(self):
        return f"Documento '{self.titulo}' con metadatos {self.metadatos}"

# Ejemplo
if __name__ == "__main__":
    doc1 = Documento("Informe", "Contenido principal", {"autor":"Ana", "fecha":"2025-06-10"})
    doc2 = doc1.clone()
    doc2.metadatos["autor"] = "Juan"
    print(doc1)  # autor: Ana
    print(doc2)  # autor: Juan
