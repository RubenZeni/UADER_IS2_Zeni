#!/usr/bin/env python3
# src/chat.py

"""
chat.py
Script de consola para invocar al API de OpenAI Chat:
- Lee input del usuario.
- Añade prefijos You: / chatGPT:.
- Maneja excepción de cuota (modo mock).
- Soporta historial con readline.
"""

import os
import sys
import readline

from openai import OpenAI, RateLimitError  # pylint: disable=import-error
from dotenv import load_dotenv  # pylint: disable=import-error

# 1. Carga de la API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Variable para guardar la última consulta
_last_query = ""


def obtener_consulta():
    """
    Solicita una consulta al usuario, valida que no esté vacía,
    la registra en el historial de readline y la devuelve.
    """
    global _last_query  # uso controlado de estado compartido
    try:
        consulta = input("Ingresa tu consulta (↑ para repetir la última): ").strip()
        if not consulta:
            raise ValueError("La consulta está vacía.")
        readline.add_history(consulta)
        _last_query = consulta
        return consulta
    except (ValueError, EOFError) as e:
        print(f"Error al leer la consulta: {e}")
        return None


def procesar_consulta(consulta):
    """
    Imprime la consulta con el prefijo "You: " y la retorna.
    """
    try:
        mensaje = f"You: {consulta}"
        print(mensaje)
        return mensaje
    except (TypeError,) as e:
        print(f"Error al procesar la consulta: {e}")
        return None


def invocar_chatgpt(mensaje):
    """
    Llama al API de ChatGPT (gpt-3.5-turbo) con la consulta
    y muestra la respuesta o un mock si falla la cuota.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensaje}],
            max_tokens=50
        )
        content = response.choices[0].message.content
    except RateLimitError:
        content = "Este es un mensaje de prueba (modo mock)"
    except Exception as e:
        print(f"Error al invocar el API: {e}")
        return
    print(f"chatGPT: {content}")


def main():
    """
    Bucle principal:
    - obtener_consulta()
    - procesar_consulta()
    - invocar_chatgpt()
    - repetir hasta Ctrl+C.
    """
    while True:
        consulta = obtener_consulta()
        if not consulta:
            continue
        mensaje = procesar_consulta(consulta)
        if not mensaje:
            continue
        invocar_chatgpt(mensaje)
        print()  # Espacio entre interacciones


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")
        sys.exit(0)