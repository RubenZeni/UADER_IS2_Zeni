#!/usr/bin/env python3
# ----------------------------------------------------------------------------
#  getJason_refactor.py
#  Copyright UADER-FCyT-IS2©2024. Todos los derechos reservados.
#  Re-Factoría OOP + Singleton + CLI robusta + Version 1.1
# ----------------------------------------------------------------------------

import json
import os
import sys
import argparse
from abc import ABC, abstractmethod

VERSION = "1.1"


class IKeyRetriever(ABC):
    """Interface para recuperar un valor de JSON dado un key."""
    @abstractmethod
    def retrieve(self, filepath: str, key: str) -> str:
        pass


class JSONKeyFetcher(IKeyRetriever):
    """Singleton que implementa IKeyRetriever para JSON."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(JSONKeyFetcher, cls).__new__(cls)
        return cls._instance

    def retrieve(self, filepath: str, key: str) -> str:
        """Lee JSON y retorna obj[key], o lanza RuntimeError con mensaje controlado."""
        if not os.path.isfile(filepath):
            raise RuntimeError(f"ERROR: archivo no encontrado: {filepath}")
        try:
            with open(filepath, 'r') as f:
                obj = json.load(f)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"ERROR: JSON inválido: {e}")
        if key not in obj:
            raise RuntimeError(f"ERROR: clave '{key}' no existe en {filepath}")
        return obj[key]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description="Recupera una clave de un JSON de microservicios bancarios."
    )
    parser.add_argument(
        "jsonfile",
        nargs="?",
        help="ruta al archivo JSON (p.ej. sitedata.json)."
    )
    parser.add_argument(
        "jsonkey",
        nargs="?",
        default="token1",
        help="clave a recuperar; default 'token1'."
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
        help="muestra la versión del programa y sale."
    )
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    # Validar que al menos jsonfile esté presente
    if not args.jsonfile:
        parser.error("falta el archivo JSON")
    retriever = JSONKeyFetcher()

    try:
        valor = retriever.retrieve(args.jsonfile, args.jsonkey)
        print(valor)
    except RuntimeError as err:
        print(str(err), file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        # Capturamos cualquier otro fallo inesperado
        print(f"ERROR inesperado: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
