# avion_builder.py
# Extiende Builder para armar Aviones

from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Avion:
    modelo: str
    body: str
    turbinas: int
    alas: int
    tren_aterrizaje: str

class AvionBuilder:
    """
    Builder genérico para Avion:
    - body
    - 2 turbinas
    - 2 alas
    - tren de aterrizaje
    """
    def __init__(self, modelo: str):
        self._modelo = modelo
        self._body: Optional[str] = None
        self._turbinas: Optional[int] = None
        self._alas: Optional[int] = None
        self._tren: Optional[str] = None

    def body(self, tipo: str) -> "AvionBuilder":
        self._body = tipo
        return self

    def turbinas(self, cant: int) -> "AvionBuilder":
        self._turbinas = cant
        return self

    def alas(self, cant: int) -> "AvionBuilder":
        self._alas = cant
        return self

    def tren_aterrizaje(self, tipo: str) -> "AvionBuilder":
        self._tren = tipo
        return self

    def build(self) -> Avion:
        # valores por defecto
        body = self._body or "Fuselaje estándar"
        turb = self._turbinas or 2
        alas = self._alas or 2
        tren = self._tren or "Retráctil"
        return Avion(self._modelo, body, turb, alas, tren)

# Ejemplo
if __name__ == "__main__":
    boeing = (
        AvionBuilder("Boeing 747")
        .body("Fuselaje ancho")
        .turbinas(4)
        .alas(2)
        .tren_aterrizaje("Fijo triple")
        .build()
    )
    print(boeing)

    jet = AvionBuilder("Jet Privado").build()
    print(jet)
