from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def show(self, indent: int = 0):
        pass

class Leaf(Component):
    def __init__(self, name: str):
        self.name = name

    def show(self, indent: int = 0):
        print(" " * indent + f"- Pieza: {self.name}")

class Composite(Component):
    def __init__(self, name: str):
        self.name = name
        self._children = []

    def add(self, component: Component):
        self._children.append(component)

    def remove(self, component: Component):
        self._children.remove(component)

    def show(self, indent: int = 0):
        print(" " * indent + f"+ Conjunto: {self.name}")
        for child in self._children:
            child.show(indent + 4)

# Generación de la jerarquía:
if __name__ == "__main__":
    producto = Composite("Producto Principal")
    # Tres subconjuntos iniciales
    for i in range(1, 4):
        sub = Composite(f"Subconjunto {i}")
        # Cada uno con cuatro piezas
        for j in range(1, 5):
            sub.add(Leaf(f"Pieza {i}.{j}"))
        producto.add(sub)
    # Mostrar antes de opcional
    print("Estructura inicial:")
    producto.show()

    # Agregar subconjunto opcional adicional
    opcional = Composite("Subconjunto Opcional")
    for k in range(1, 5):
        opcional.add(Leaf(f"Pieza O.{k}"))
    producto.add(opcional)

    print("\nEstructura con subconjunto opcional:")
    producto.show()
