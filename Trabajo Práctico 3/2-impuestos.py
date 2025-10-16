# impuestos.py
# Cálculo de IVA (21%), IIBB (5%) y contribuciones municipales (1.2%)

class Impuestos:
    def calcular(self, base: float) -> float:
        """
        Recibe base imponible y retorna base + IVA + IIBB + contribuciones.
        IVA: 21%, IIBB:5%, Municipal:1.2%
        """
        if base < 0:
            raise ValueError("La base imponible no puede ser negativa")
        iva = base * 0.21
        iibb = base * 0.05
        municip = base * 0.012
        return base + iva + iibb + municip

# Ejemplo
if __name__ == "__main__":
    imp = Impuestos()
    print(imp.calcular(1000.0))  # 1000 + 210 + 50 + 12 = 1272
