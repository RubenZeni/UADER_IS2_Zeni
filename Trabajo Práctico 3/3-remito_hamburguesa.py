# remito_hamburguesa.py
# Patrón Factory sencillo para entrega de comida rápida

from abc import ABC, abstractmethod

class Entrega(ABC):
    @abstractmethod
    def enviar(self) -> str:
        pass

class EntregaMostrador(Entrega):
    def enviar(self) -> str:
        return "Hamburguesa entregada en mostrador."

class EntregaRetiro(Entrega):
    def enviar(self) -> str:
        return "Hamburguesa lista para retiro por el cliente."

class EntregaDelivery(Entrega):
    def enviar(self) -> str:
        return "Hamburguesa enviada por delivery."

class HamburguesaRemitoFactory:
    @staticmethod
    def crear_entrega(modo: str) -> Entrega:
        modo = modo.lower()
        if modo == "mostrador":
            return EntregaMostrador()
        if modo == "retiro":
            return EntregaRetiro()
        if modo == "delivery":
            return EntregaDelivery()
        raise ValueError(f"Modo de entrega desconocido: {modo}")

# Ejemplo
if __name__ == "__main__":
    for modo in ["mostrador","retiro","delivery"]:
        remito = HamburguesaRemitoFactory.crear_entrega(modo)
        print(remito.enviar())
