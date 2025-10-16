# factura.py
# Generación de factura con condición impositiva

class Factura:
    """
    Factura con total y condición fiscal: 'Responsable', 'No Inscripto', 'Exento'.
    """
    CONDICIONES = {
        "responsable": "IVA Responsable",
        "no_inscripto": "IVA No Inscripto",
        "exento": "IVA Exento"
    }

    def __init__(self, total: float, condicion: str):
        if total < 0:
            raise ValueError("El total no puede ser negativo")
        clave = condicion.lower().replace(" ", "_")
        if clave not in self.CONDICIONES:
            raise ValueError(f"Condición fiscal inválida: {condicion}")
        self.total = total
        self.condicion = self.CONDICIONES[clave]

    def __str__(self):
        return f"Factura: Total = ${self.total:.2f} | Condición: {self.condicion}"

# Ejemplo
if __name__ == "__main__":
    for cond in ["responsable","no_inscripto","exento"]:
        print(Factura(2500.75, cond))
