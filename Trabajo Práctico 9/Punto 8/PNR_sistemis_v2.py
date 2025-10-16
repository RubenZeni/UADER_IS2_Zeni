#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* TP9_Punto8a.py
#* Programa derivado para visualizar el modelo PNR para un esfuerzo de proyecto dado (K)
#* comparado con el modelo de calibración y los datos históricos.
#*
#* UADER - FCyT - Ingeniería de Software II
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
import numpy as np
import argparse
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# --- Función del modelo PNR para el esfuerzo instantáneo p(t) ---
def pnr_model(t, K, a):
    """Calcula el esfuerzo instantáneo p(t) = 2 * K * a * t * exp(-a * t^2)"""
    return 2 * K * a * t * np.exp(-a * t**2)

# --- Argumentos de línea de comandos ---
parser = argparse.ArgumentParser(description='Visualizador del modelo PNR para un esfuerzo de proyecto.')
parser.add_argument('-k', '--esfuerzo', type=float, required=True, help='Esfuerzo total del nuevo proyecto en Personas-Mes (PM).')
args = parser.parse_args()

# --- 1. Cargar y calibrar con el dataset histórico ---
# Dataset del taller "Modelos dinámicos"
t_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])       # Tiempo en meses
E_data = np.array([8, 21, 25, 30, 25, 24, 17, 15, 11, 6]) # Esfuerzo en PM

# El esfuerzo total histórico (K_hist) es la suma de los esfuerzos observados
K_hist = np.sum(E_data)
print(f"Esfuerzo histórico total (K_hist): {K_hist:.2f} PM")

# Para calibrar 'a', necesitamos ajustar una función que solo dependa de 'a'.
# p(t) = K * f(t, a), por lo que definimos una función f(t,a) para el ajuste.
def fit_func(t, a):
    return pnr_model(t, K_hist, a)

# Usamos curve_fit para encontrar el mejor valor de 'a' que ajuste los datos históricos
popt, _ = curve_fit(fit_func, t_data, E_data, p0=[0.01])
a_calibrado = popt[0]
print(f"Parámetro 'a' calibrado desde la historia: {a_calibrado:.4f}")

# --- 2. Preparar los datos para la graficación ---
# Esfuerzo del nuevo proyecto, aceptado por parámetro
K_nuevo = args.esfuerzo

# Creamos un eje de tiempo continuo para graficar curvas suaves
t_continuo = np.linspace(0, 12, 200)

# Calculamos los valores del modelo de mejor ajuste para los datos históricos
y_modelo_hist = pnr_model(t_continuo, K_hist, a_calibrado)

# Calculamos los valores del modelo para el nuevo proyecto
y_nuevo_proy = pnr_model(t_continuo, K_nuevo, a_calibrado)

# --- 3. Graficar los resultados ---
plt.figure(figsize=(12, 7))

# a) Graficar los puntos del dataset histórico de calibración
plt.scatter(t_data, E_data, color='blue', zorder=5, label=f'Dataset Histórico (K={K_hist:.0f} PM)')

# b) Graficar el modelo obtenido por mejor ajuste
plt.plot(t_continuo, y_modelo_hist, color='red', linestyle='--', label=f'Modelo Ajustado a la Historia')

# c) Graficar la curva para el nuevo proyecto
plt.plot(t_continuo, y_nuevo_proy, color='green', linewidth=2, label=f'Nuevo Proyecto (K={K_nuevo:.0f} PM)')

# --- Configuración del gráfico ---
plt.title('Distribución de Esfuerzo (Modelo PNR)')
plt.xlabel('Tiempo (Meses)')
plt.ylabel('Esfuerzo (Personas-Mes)')
plt.legend()
plt.grid(True)
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.savefig(f'distribucion_esfuerzo_{K_nuevo:.0f}PM.png')
plt.show()

