#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* TP9_Punto9.py
#* Programa modificado para procesar modelos de regresión con un nuevo dataset
#* y estimar el esfuerzo para un tamaño de proyecto dado.
#*
#* UADER - FCyT - Ingeniería de Software II
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
import numpy as np
import pandas as pd
import argparse
import statsmodels.api as sm
import sys
import os
import matplotlib.pyplot as plt

#*------------------------------------------------------------------------------------------------
#* MODIFICACIÓN 1: Se actualiza el dataset histórico con los datos del punto 9.
#*------------------------------------------------------------------------------------------------
data = {
    'LOC': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
    'Esfuerzo': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
}
df = pd.DataFrame(data)

#*------------------------------------------------------------------------------------------------
#* Inicialización y procesamiento de argumentos
#*------------------------------------------------------------------------------------------------
version = "8.0-TP9"
linear = False
exponential = False
estimation_loc = None
os.system('clear')

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--version", required=False, help="version", action="store_true")
ap.add_argument("-x", "--exponential", required=False, help="Modelo Exponencial", action="store_true")
ap.add_argument("-l", "--linear", required=False, help="Modelo Lineal", action="store_true")
#* MODIFICACIÓN 2: Se agrega un argumento para poder estimar.
ap.add_argument("-e", "--estimar", type=float, required=False, help="Estimar esfuerzo para un valor de LOC.")
args = vars(ap.parse_args())

if args['version']:
    print(f"Programa {sys.argv[0]} version {version}")
    sys.exit(0)

linear = args['linear']
exponential = args['exponential']
estimation_loc = args['estimar']

if not linear and not exponential:
    print("Debe indicar modelo lineal (-l) o exponencial (-x) o ambos.")
    sys.exit(0)

#*-----------------------------------------------------------------------------------------------
#* Procesamiento de modelos y guardado de resultados para su uso posterior
#*-----------------------------------------------------------------------------------------------
best_model_type = None
best_r_squared = -1
model_params = {}

#*--- Modelo Lineal ---
if linear:
    a, b = np.polyfit(df['LOC'], df['Esfuerzo'], 1)
    # Corrección para obtener R-squared
    correlation_matrix = np.corrcoef(df['LOC'], df['Esfuerzo'])
    r_squared_linear = correlation_matrix[0, 1]**2
    
    model_params['linear'] = {'a': a, 'b': b, 'r2': r_squared_linear}
    
    print(f"Modelo lineal: E = {b:.6f} + {a:.6f} * LOC")
    print(f"El R-squared (lineal) = {r_squared_linear:.4f}")
    
    if r_squared_linear > best_r_squared:
        best_r_squared = r_squared_linear
        best_model_type = 'linear'

#*--- Modelo Exponencial ---
if exponential:
    df['logEsfuerzo'] = np.log(df['Esfuerzo'])
    df['logLOC'] = np.log(df['LOC'])
    
    X = sm.add_constant(df['logLOC'])
    Y = df['logEsfuerzo']
    
    mx = sm.OLS(Y, X).fit()
    
    k = np.exp(mx.params['const'])
    b_exp = mx.params['logLOC']
    r_squared_exp = mx.rsquared

    model_params['exponential'] = {'k': k, 'b': b_exp, 'r2': r_squared_exp}

    print(f"Modelo exponencial: E = {k:.6f} * (LOC^{b_exp:.6f})")
    print(f"El R-squared (exponencial) = {r_squared_exp:.4f}")

    if r_squared_exp > best_r_squared:
        best_r_squared = r_squared_exp
        best_model_type = 'exponential'

print(f"\nEl mejor modelo es el {best_model_type.upper()} con un R-squared de {best_r_squared:.4f}")

#*------------------------------------------------------------------------------------------------
#* Graficación
#*------------------------------------------------------------------------------------------------
plt.figure(figsize=(12, 7))
plt.scatter(df['LOC'], df['Esfuerzo'], label='Datos históricos', zorder=5)

# Generar puntos para una curva suave
loc_continuo = np.linspace(df['LOC'].min(), df['LOC'].max(), 200)

if linear:
    params = model_params['linear']
    plt.plot(loc_continuo, params['a'] * loc_continuo + params['b'], label=f"Modelo Lineal (R²={params['r2']:.2f})", color='red')

if exponential:
    params = model_params['exponential']
    plt.plot(loc_continuo, params['k'] * (loc_continuo**params['b']), label=f"Modelo Exponencial (R²={params['r2']:.2f})", color='green')

#* MODIFICACIÓN 3: Lógica para estimar y graficar el nuevo punto.
if estimation_loc is not None:
    if best_model_type == 'linear':
        params = model_params['linear']
        estimated_effort = params['a'] * estimation_loc + params['b']
    elif best_model_type == 'exponential':
        params = model_params['exponential']
        estimated_effort = params['k'] * (estimation_loc**params['b'])
    
    print(f"\nEstimación para LOC = {estimation_loc}: Esfuerzo = {estimated_effort:.2f} PM")
    
    # Graficar el punto estimado
    plt.scatter([estimation_loc], [estimated_effort], color='purple', marker='*', s=200, zorder=10, label=f'Estimación ({estimation_loc} LOC)')
    
    # Ajustar límites del gráfico si la estimación está fuera del rango
    if estimation_loc < plt.xlim()[0] or estimation_loc > plt.xlim()[1]:
        plt.xlim(min(plt.xlim()[0], estimation_loc*0.9), max(plt.xlim()[1], estimation_loc*1.1))


plt.xlabel('Complejidad (LOC)')
plt.ylabel('Esfuerzo (Personas-Mes)')
plt.title('Modelo de Estimación de Esfuerzo')
plt.legend()
plt.grid(True)
plt.show()

