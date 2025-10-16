import os

#*--------------------------------------------------------------------
#* Ejemplo de design pattern de tipo State con memorias de frecuencias
#*--------------------------------------------------------------------

class State:
    """State base: recorre stations y muestra el nombre."""
    def __init__(self, radio):
        self.radio = radio
        self.stations = []
        self.pos = 0
        self.name = ""

    def scan(self):
        self.pos = (self.pos + 1) % len(self.stations)
        print(f"Sintonizando... Estación {self.stations[self.pos]} {self.name}")
    
    def toggle_amfm(self):
        raise NotImplementedError()


class AmState(State):
    def __init__(self, radio):
        super().__init__(radio)
        self.stations = ["1250", "1380", "1510"]
        self.name = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate


class FmState(State):
    def __init__(self, radio):
        super().__init__(radio)
        self.stations = ["81.3", "89.1", "103.9"]
        self.name = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate


class Radio:
    """Radio que barre AM, FM y memorias memorizadas (M1–M4)."""
    def __init__(self):
        self.fmstate = FmState(self)
        self.amstate = AmState(self)
        self.state = self.fmstate

        # Memorias: etiqueta → (banda, frecuencia)
        self.memorias = {
            "M1": ("AM", "1250"),
            "M2": ("FM", "89.1"),
            "M3": ("AM", "1510"),
            "M4": ("FM", "103.9"),
        }
        # Lista fija de etiquetas para barrido
        self.mem_list = list(self.memorias.keys())
        self.mem_pos = -1

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        """Si estamos en modo normal, usa State.scan; si en 'MEM', barre memorias."""
        self.state.scan()

    def scan_memorias(self):
        """Recorre las memorias M1–M4 en cada ciclo."""
        self.mem_pos = (self.mem_pos + 1) % len(self.mem_list)
        etiqueta = self.mem_list[self.mem_pos]
        banda, freq = self.memorias[etiqueta]
        print(f"Sintonizando memoria {etiqueta}: {freq} {banda}")

    def ciclo_barrido(self):
        """Un ciclo completo: 1–4, blind scan y toggle."""
        # Primero las 4 memorias
        for _ in range(len(self.mem_list)):
            self.scan_memorias()
        # Luego un scan normal en la banda actual
        self.scan()
        # Y cambiamos de banda
        self.toggle_amfm()


if __name__ == "__main__":
    #os.system("clear")
    print("=== Simulando barrido con memorias y cambio automático ===")
    radio = Radio()
    # Ejecutamos, por ejemplo, 3 ciclos
    for i in range(3):
        print(f"\n--- Ciclo #{i+1} ---")
        radio.ciclo_barrido()