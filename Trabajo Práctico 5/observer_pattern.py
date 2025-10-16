# observer_pattern.py

class Sujeto:
    """Sujeto que notifica ID a los observers suscriptos."""
    def __init__(self):
        self._observers = []

    def suscribir(self, obs):
        self._observers.append(obs)

    def notificar(self, id_emitido):
        print(f"\n== Emisión ID: {id_emitido} ==")
        for obs in self._observers:
            obs.actualizar(id_emitido)


class ObserverBase:
    """Base de observers con ID propio."""
    def __init__(self, mi_id):
        self.mi_id = mi_id

    def actualizar(self, id_emitido):
        if id_emitido == self.mi_id:
            print(f"{self.__class__.__name__} detectó coincidencia con su ID ({self.mi_id})")


# Cuatro observers con distintos IDs
class ObsA(ObserverBase): pass
class ObsB(ObserverBase): pass
class ObsC(ObserverBase): pass
class ObsD(ObserverBase): pass


if __name__ == "__main__":
    sujeto = Sujeto()

    # Creo 4 observers con IDs de 4 caracteres
    a = ObsA("A1B2")
    b = ObsB("X9Y8")
    c = ObsC("ZZ00")
    d = ObsD("M3N4")

    # Los suscribo
    for obs in (a, b, c, d):
        sujeto.suscribir(obs)

    # Emisión de 8 IDs (asegurándome al menos 4 matches)
    emisiones = ["A1B2", "QWER", "M3N4", "ZZ00", "XXXX", "X9Y8", "M3N4", "A1D2"]
    for eid in emisiones:
        sujeto.notificar(eid)