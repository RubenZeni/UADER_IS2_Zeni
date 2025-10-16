#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
get_jason_refactor.py – Refactoría OOP con Singleton y CLI robusta.

Módulo que recupera claves de un JSON de microservicios bancarios,
con control estricto de errores y bandera de versión (1.1).

Copyright UADER-FCyT-IS2©2024. Todos los derechos reservados.
"""

import argparse
import json
import os
import sys
from abc import ABC, abstractmethod

VERSION = "1.1"


class IKeyRetriever(ABC):
    """Interfaz para recuperadores de claves de un JSON."""

    @abstractmethod
    def retrieve(self, filepath: str, key: str) -> str:
        """
        Lee `filepath` (JSON) y retorna el valor de `key`.
        Lanza RuntimeError con mensaje controlado ante cualquier fallo.
        """
        pass


# pylint: disable=too-few-public-methods
class JSONKeyFetcher(IKeyRetriever):
    """Singleton que implementa IKeyRetriever para archivos JSON."""

    _instance = None

    def __new__(cls):
        """
        Asegura única instancia (Singleton).
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def retrieve(self, filepath: str, key: str) -> str:
        """
        Abre y parsea JSON en `filepath`, luego devuelve obj[key].
        RuntimeError con mensaje claro si:
          - no existe el archivo,
          - JSON inválido,
          - la clave no está presente.
        """
        if not os.path.isfile(filepath):
            raise RuntimeError(f"ERROR: archivo no encontrado: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                obj = json.load(f)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"ERROR: JSON inválido: {exc}") from exc
        if key not in obj:
            raise RuntimeError(f"ERROR: clave '{key}' no existe en {filepath}")
        return obj[key]


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Construye el parser de argumentos de línea de comandos,
    con:
      - jsonfile (posicional, obligatorio)
      - jsonkey  (posicional, opcional; default 'token1')
      - -v/--version
    """
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description="Recupera clave de JSON de microservicios bancarios."
    )
    parser.add_argument(
        "jsonfile",
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
    """
    Punto de entrada. Parsea args, usa JSONKeyFetcher para extraer el valor
    y lo imprime. Todas las fallas son capturadas como RuntimeError.
    """
    parser = build_arg_parser()
    args = parser.parse_args()

    retriever = JSONKeyFetcher()
    try:
        valor = retriever.retrieve(args.jsonfile, args.jsonkey)
    except RuntimeError as err:
        print(err, file=sys.stderr)
        sys.exit(1)

    print(valor)


if __name__ == "__main__":
    main()
