#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
get_jason_refactor_v3.py – Re-Ingeniería con Chain of Responsibility, Iterator y persistencia de estado.

Módulo que:
  • Usa el Singleton JSONKeyFetcher para obtener la clave de cada “token” (banco).
  • Define dos cuentas (“token1” con $1000 y “token2” con $2000) o recupera su estado previo desde disco.
  • Procesa pagos de monto variable (default $500) alternando cuentas (siempre que haya saldo suficiente),
    mediante un patrón Cadena de Responsabilidad.
  • Registra cada pago (número, token usado, monto, clave) en el historial y lo guarda en disco.
  • Permite listar todos los pagos realizados en orden cronológico (Iterator).
  • CLI robusta con argparse:
      - Posicional: jsonfile (ruta al JSON con los tokens).
      - Sub-comando “pay”  → order_num (int) y amount (float, default=500).
      - Sub-comando “list” → muestra todos los pagos registrados.
      - Flag “-v/--version”: muestra versión (1.2) y sale.
  • Control de errores totalmente gestionado; nunca sale con excepción no controlada.
  • Almacena el estado (saldos e historial) en `payment_state.json`.
  • Versión 1.2.

Copyright UADER-FCyT-IS2©2024. Todos los derechos reservados.
"""

import argparse
import json
import os
import sys
from abc import ABC, abstractmethod
from typing import List, Iterator, Optional

VERSION = "1.2"
STATE_FILENAME = "payment_state.json"


# --------------------------------------------------------------------
# ∙ Punto (a) y (b): reutilizamos JSONKeyFetcher (Singleton) para que
#   devuelva la “clave” (string) asociada a cada token (banco).
# --------------------------------------------------------------------

class IKeyRetriever(ABC):
    """Interfaz para recuperadores de claves de un JSON."""

    @abstractmethod
    def retrieve(self, filepath: str, key: str) -> str:
        """
        Lee `filepath` (JSON) y retorna el valor de `key`.
        Debe lanzar RuntimeError con mensaje controlado si hay fallo.
        """
        pass


# pylint: disable=too-few-public-methods
class JSONKeyFetcher(IKeyRetriever):
    """Singleton que implementa IKeyRetriever para archivos JSON."""

    _instance: Optional["JSONKeyFetcher"] = None

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
        Lanza RuntimeError con mensaje claro si:
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


# --------------------------------------------------------------------
# ∙ Punto (c) y (d): definimos el patrón Chain of Responsibility
#   para procesar pagos en dos cuentas (token1 y token2), con persistencia.
# --------------------------------------------------------------------

class PaymentRequest:
    """
    Representa un pedido de pago.
    """
    def __init__(self, order_num: int, amount: float):
        self.order_num = order_num
        self.amount = amount


class PaymentRecord:
    """
    Almacena el resultado de un pago:
      – order_num: número de pedido
      – token:     nombre del token que se usó
      – key:       clave obtenida del JSON
      – amount:    monto efectivamente debitado
    """
    def __init__(self, order_num: int, token: str, key: str, amount: float):
        self.order_num = order_num
        self.token = token
        self.key = key
        self.amount = amount

    def to_dict(self) -> dict:
        """
        Convierte este PaymentRecord a dict para serializar a JSON.
        """
        return {
            "order_num": self.order_num,
            "token": self.token,
            "key": self.key,
            "amount": self.amount
        }

    @staticmethod
    def from_dict(data: dict) -> "PaymentRecord":
        """
        Reconstruye un PaymentRecord a partir de un dict.
        """
        return PaymentRecord(
            data.get("order_num"),
            data.get("token"),
            data.get("key"),
            data.get("amount")
        )


class PaymentHandler(ABC):
    """
    Handler abstracto para la Cadena de Responsabilidad de cuentas.
    Cada cuenta concreta hereda de este y define su propia lógica de manejo.
    """
    def __init__(self, token: str, initial_balance: float,
                 key_fetcher: JSONKeyFetcher):
        self.token = token
        self.balance = initial_balance
        self.key_fetcher = key_fetcher
        self.next_handler: Optional["PaymentHandler"] = None

    def set_next(self, handler: "PaymentHandler") -> None:
        """
        Define el siguiente handler en la cadena.
        """
        self.next_handler = handler

    def handle_request(self,
                       request: PaymentRequest,
                       jsonfile: str,
                       manager: "PaymentProcessor",
                       start_from_here: bool = False) -> bool:
        """
        Intenta procesar el pago:
        – Si esta cuenta tiene saldo >= request.amount y
          es la que le tocaba (start_from_here == True), procesa aquí:
            • Resta el monto de self.balance.
            • Obtiene la clave desde JSONKeyFetcher.
            • Registra el pago en el manager (que guarda el historial).
            • Retorna True.
        – Si no alcanza saldo o no es su turno, delega al siguiente handler.
        Retorna True si algún handler procesó el pago; False en caso contrario.
        """
        if start_from_here:
            if self.balance >= request.amount:
                # Procesar acá
                self.balance -= request.amount
                key = self.key_fetcher.retrieve(jsonfile, self.token)
                manager.record_payment(PaymentRecord(
                    request.order_num, self.token, key, request.amount
                ))
                return True
        # Si no se procesó aquí o no era su turno, derivar al siguiente
        if self.next_handler:
            return self.next_handler.handle_request(
                request, jsonfile, manager, start_from_here=True
            )
        # Si no hay siguiente, no se procesó en ninguna cuenta
        return False


class PaymentHandlerConcrete(PaymentHandler):
    """
    Implementación concreta del PaymentHandler.
    No agrega métodos nuevos; hereda la lógica básica.
    """
    pass  # Toda la lógica de manejo está en PaymentHandler


class PaymentProcessor:
    """
    Administra la cadena de handlers, las solicitudes de pago y la persistencia.
    – Mantiene lista de handlers en orden.
    – Alterna en “round robin” la cuenta inicial para cada pago.
    – Registra todos los PaymentRecord en orden cronológico.
    – Provee un Iterator para listar los pagos.
    – Puede cargar/guardar el estado (balances e historial) desde/hacia un JSON.
    """
    def __init__(self,
                 jsonfile: str,
                 initial_balances: dict[str, float],
                 initial_history: List[dict] = None):
        """
        Inicializa:
          jsonfile: ruta al JSON donde están las claves.
          initial_balances: dict con {token_name: saldo_restante}.
          initial_history: lista de dicts, cada dict corresponde a PaymentRecord.
        """
        self.jsonfile = jsonfile
        self.handlers: List[PaymentHandler] = []
        self.next_index_to_try = 0  # Para round robin
        self.payment_history: List[PaymentRecord] = []

        # Creamos un JSONKeyFetcher singleton
        key_fetcher = JSONKeyFetcher()

        # 1. Crear handlers con saldos iniciales
        for token_name, saldo in initial_balances.items():
            handler = PaymentHandlerConcrete(token_name, saldo, key_fetcher)
            self.handlers.append(handler)

        # 2. Enlazar en cadena circular (último → primero)
        for idx, handler in enumerate(self.handlers):
            next_idx = (idx + 1) % len(self.handlers)
            handler.set_next(self.handlers[next_idx])

        # 3. Reconstruir historial si se pasó initial_history
        if initial_history:
            for rec_dict in initial_history:
                # Desde dict a PaymentRecord
                pago = PaymentRecord.from_dict(rec_dict)
                self.payment_history.append(pago)

    def process_payment(self, request: PaymentRequest) -> bool:
        """
        Procesa un PaymentRequest de monto request.amount sin recursión:
        1) Intenta con la cuenta en índice start_idx.
        2) Si falla (saldo insuficiente), intenta con la otra cuenta (start_idx+1).
        3) Actualiza next_index_to_try para la próxima invocación (round robin).
        4) Retorna True si el pago se procesó, False si ninguna cuenta alcanzó saldo.
        """
        n = len(self.handlers)
        start_idx = self.next_index_to_try % n
        other_idx = (start_idx + 1) % n

        handler1 = self.handlers[start_idx]
        handler2 = self.handlers[other_idx]

        # Intento 1: si handler1 tiene saldo suficiente, procesar aquí
        if handler1.balance >= request.amount:
            handler1.balance -= request.amount
            key = handler1.key_fetcher.retrieve(self.jsonfile, handler1.token)
            self.record_payment(PaymentRecord(
                request.order_num, handler1.token, key, request.amount
            ))
            self.next_index_to_try = other_idx
            return True

        # Intento 2: si handler2 tiene saldo suficiente, procesar ahí
        if handler2.balance >= request.amount:
            handler2.balance -= request.amount
            key = handler2.key_fetcher.retrieve(self.jsonfile, handler2.token)
            self.record_payment(PaymentRecord(
                request.order_num, handler2.token, key, request.amount
            ))
            self.next_index_to_try = start_idx
            return True

        # Ninguna cuenta pudo procesar
        self.next_index_to_try = other_idx
        return False



    def record_payment(self, record: PaymentRecord) -> None:
        """
        Agrega el PaymentRecord al historial en memoria.
        """
        self.payment_history.append(record)

    def __iter__(self) -> Iterator[PaymentRecord]:
        """
        Iterator que recorre payment_history en orden cronológico.
        """
        return iter(self.payment_history)

    def get_current_state(self) -> dict:
        """
        Retorna un dict con el estado actual completo:
        {
          "balances": { "token1": 500.0, "token2": 1500.0 },
          "history": [ {order_num:..., token:..., key:..., amount:...}, ... ]
        }
        """
        # Extraer saldos actuales de cada handler
        balances: dict[str, float] = {}
        for handler in self.handlers:
            balances[handler.token] = handler.balance

        # Extraer historial como lista de dicts
        history_dicts = [rec.to_dict() for rec in self.payment_history]

        return {
            "balances": balances,
            "history": history_dicts
        }

    @staticmethod
    def load_state(filepath: str) -> dict:
        """
        Carga el state JSON de disco. Si no existe, retorna None.
        """
        if not os.path.isfile(filepath):
            return None
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
                return state
        except Exception:
            # Si hay cualquier error al leer/parsear, ignoramos y devolvemos None
            return None

    @staticmethod
    def save_state(filepath: str, state: dict) -> None:
        """
        Guarda el state dict en filepath como JSON (con indentación para legibilidad).
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)


# --------------------------------------------------------------------
# ∙ Punto (e) y (f): CLI con argparse + subcomandos “pay” y “list”, 
#   usando persistencia. Versión 1.2.
# --------------------------------------------------------------------

def build_arg_parser_v3() -> argparse.ArgumentParser:
    """
    Construye el parser de argumentos para la v1.2:
      • jsonfile         (obligatorio): sitedata.json (con tokens y claves).
      • subcomando “pay” : order_num (int), amount (float; default=500).
      • subcomando “list”: no recibe args extra.
      • -v/--version     : muestra versión y sale.
    """
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description="Procesador de pagos automático balanceado (v1.2)."
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
        help="muestra la versión del programa y sale."
    )
    # Posicional: ruta al JSON con los tokens (sitedata.json)
    parser.add_argument(
        "jsonfile",
        help="ruta al archivo JSON con los tokens (p.ej. sitedata.json)."
    )
    # Subparsers
    subparsers = parser.add_subparsers(
        title="comandos", dest="command", required=True
    )
    # Subcomando "pay"
    pay_parser = subparsers.add_parser(
        "pay",
        help="Registra un pago. Ej: `pay 123` (order_num=123, monto=500 por defecto) o `pay 123 600`."
    )
    pay_parser.add_argument(
        "order_num",
        type=int,
        help="número de pedido (entero)."
    )
    pay_parser.add_argument(
        "amount",
        type=float,
        nargs="?",
        default=500.0,
        help="monto a debitar (float). Si no se pasa, usa 500."
    )
    # Subcomando "list"
    subparsers.add_parser(
        "list",
        help="Muestra el listado de todos los pagos en orden cronológico."
    )
    return parser


def main():
    """
    Punto de entrada v1.2 con persistencia:
      – Parsea CLI.
      – Carga estado previo desde `payment_state.json` (si existe).
      – Inicializa PaymentProcessor con balances e historial cargados o saldos originales.
      – “pay”: crea un PaymentRequest y llama a process_payment().
        • Si se procesó, guarda el estado actualizado en disco.
        • Si no pudo, sale con error controlado.
      – “list”: itera sobre todos los PaymentRecord e imprime.
      – Maneja errores controlados y sale con sys.exit(1) si hay fallo.
    """
    parser = build_arg_parser_v3()
    args = parser.parse_args()

    # 1) Validar existencia de jsonfile (sitedata.json)
    jsonfile = args.jsonfile
    if not os.path.isfile(jsonfile):
        print(f"ERROR: archivo no encontrado: {jsonfile}", file=sys.stderr)
        sys.exit(1)

    # 2) Leer estado previo desde payment_state.json
    saved = PaymentProcessor.load_state(STATE_FILENAME)
    if saved:
        # Si había estado guardado, extraemos balances e historial
        balances_raw = saved.get("balances", {})
        history_raw = saved.get("history", [])
        # Si el JSON no tenía alguna cuenta, le ponemos saldo 0
        # (pero asumiendo que si faltan keys, no es el caso normal)
        initial_balances = {
            "token1": balances_raw.get("token1", 0.0),
            "token2": balances_raw.get("token2", 0.0)
        }
        initial_history = history_raw
    else:
        # Estado nuevo: balances originales
        initial_balances = {"token1": 1000.0, "token2": 2000.0}
        initial_history = []

    # 3) Crear el PaymentProcessor con estado cargado o por defecto
    processor = PaymentProcessor(jsonfile,
                                 initial_balances,
                                 initial_history)

    # =================================================================
    # CORRECCIÓN: Restaurar turno en round-robin según cantidad de pagos
    # =================================================================
    processor.next_index_to_try = len(processor.payment_history) % len(processor.handlers)

    # 4) Atender subcomandos
    if args.command == "pay":
        # a) Intentar procesar el pago
        order = args.order_num
        monto = args.amount
        request = PaymentRequest(order, monto)
        try:
            pudo = processor.process_payment(request)
        except RuntimeError as err:
            # Si JSONKeyFetcher falla (JSON inválido/claves), cae aquí
            print(err, file=sys.stderr)
            sys.exit(1)

        if not pudo:
            # Ninguna cuenta pudo cubrir el pago
            print(f"ERROR: Ninguna cuenta tiene saldo suficiente para pedido {order} (${monto}).",
                  file=sys.stderr)
            sys.exit(1)
        # b) Si se procesó, guardamos el estado actualizado en disk
        new_state = processor.get_current_state()
        try:
            PaymentProcessor.save_state(STATE_FILENAME, new_state)
        except Exception as err:
            # Si falla al guardar, igual informamos éxito, pero avisamos que no se guardó.
            print(f"ADVERTENCIA: no se pudo guardar el estado: {err}", file=sys.stderr)

        # c) Imprimir confirmación al usuario
        print(f"Pedido {order}: Pago de ${monto:.2f} procesado correctamente.")

    elif args.command == "list":
        # Mostrar todos los PaymentRecord en orden
        historial = list(processor)  # itera sobre PaymentRecord
        if not historial:
            print("No hay pagos registrados aún.")
        else:
            print("Listado de pagos (cronológico):")
            for rec in historial:
                print(f" • Pedido {rec.order_num}: token='{rec.token}', "
                      f"clave='{rec.key}', monto=${rec.amount:.2f}")
    else:
        # No debería ocurrir (argparse obliga a pasar "pay" o "list")
        parser.error("Comando inválido.")

if __name__ == "__main__":
    main()
