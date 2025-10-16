#!/usr/bin/env python3
"""
getJason_mod.py – Recupera claves de un JSON de microservicios bancarios.

Uso:
  getJason_mod.py <jsonfile> [jsonkey]

Parámetros:
  jsonfile  Ruta al archivo JSON (p.ej. sitedata.json).
  jsonkey   (Opcional) Clave a recuperar. Si no se pasa, usa 'token1'.

Ejemplos:
  ./getJason_mod.py sitedata.json
  ./getJason_mod.py sitedata.json token2
"""

import json
import sys
import os

def print_usage():
    prog = os.path.basename(sys.argv[0])
    print(f"Uso: {prog} <jsonfile> [jsonkey]", file=sys.stderr)
    print("  jsonfile : ruta al archivo JSON", file=sys.stderr)
    print("  jsonkey  : (opcional) clave dentro del JSON; default 'token1'", file=sys.stderr)
    sys.exit(1)

def main():
    argc = len(sys.argv) - 1
    if argc < 1 or argc > 2:
        print("ERROR: número de argumentos inválido.", file=sys.stderr)
        print_usage()

    jsonfile = sys.argv[1]
    jsonkey  = sys.argv[2] if argc == 2 else 'token1'

    # Validar existencia de archivo
    if not os.path.isfile(jsonfile):
        print(f"ERROR: archivo no encontrado: {jsonfile}", file=sys.stderr)
        sys.exit(1)

    # Leer y parsear JSON
    try:
        with open(jsonfile, 'r') as f:
            obj = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON inválido: {e}", file=sys.stderr)
        sys.exit(1)

    # Validar existencia de la clave
    if jsonkey not in obj:
        print(f"ERROR: clave '{jsonkey}' no existe en {jsonfile}", file=sys.stderr)
        sys.exit(1)

    # Imprimir valor
    print(obj[jsonkey])

if __name__ == "__main__":
    main()
