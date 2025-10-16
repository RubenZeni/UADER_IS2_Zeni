from abc import ABC, abstractmethod

# Implementador
class RollingMill(ABC):
    @abstractmethod
    def produce(self, thickness: float, width: float) -> str:
        pass

class Mill5m(RollingMill):
    def produce(self, thickness: float, width: float) -> str:
        return (f"Producida lámina de {thickness}\" x {width}m "
                f"en tren de 5m")

class Mill10m(RollingMill):
    def produce(self, thickness: float, width: float) -> str:
        return (f"Producida lámina de {thickness}\" x {width}m "
                f"en tren de 10m")

# Abstracción
class Laminate:
    def __init__(self, thickness: float, width: float, mill: RollingMill):
        self.thickness = thickness
        self.width = width
        self.mill = mill

    def set_mill(self, mill: RollingMill):
        self.mill = mill

    def produce(self) -> str:
        return self.mill.produce(self.thickness, self.width)

# Ejemplo de uso:
if __name__ == "__main__":
    lam = Laminate(0.5, 1.5, Mill5m())
    print(lam.produce())   # Tren 5m
    lam.set_mill(Mill10m())
    print(lam.produce())   # Ahora tren 10m
