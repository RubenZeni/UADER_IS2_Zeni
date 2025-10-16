# Trabajo Práctico N°8: Re-ingeniería de `getJason_refactor_v2.py` → `getJason_refactor_v3.py`

Enunciado breve:
> A partir del Singleton que recupera tokens (v2), crear un sistema de pagos que automatice la selección de la cuenta (token1 o token2), balanceando los pagos y documentando con Chain of Responsibility e Iterator. Avanzar la versión a 1.2.

---

## a) Integración automática de JSONKeyFetcher en el proceso de pago
> “a) Partiendo del objeto singleton que, dado un nombre de token (banco), da la clave, integrar en un nuevo componente que ante una solicitud de pago seleccione automáticamente la cuenta desde la que se hará el mismo.”

**Modificación realizada:**  
1. Se crea la clase **`PaymentRequest`** para encapsular `(order_num, amount)`.
2. Se crea la clase **`PaymentRecord`** para almacenar el resultado `(order_num, token, key, amount)`.
3. Se define la clase abstracta **`PaymentHandler`** que, al procesar un pago, invoca:
   ```python
   key = self.key_fetcher.retrieve(jsonfile, self.token)
   ```

Es decir, reutiliza el Singleton `JSONKeyFetcher` para obtener la clave asociada al `token`.

4. Se añaden estos bloques **al comienzo** de `get_jason_refactor_v3.py` después de `JSONKeyFetcher` (v2):

```python
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
        self.next_handler = handler

    def handle_request(self,
                       request: PaymentRequest,
                       jsonfile: str,
                       manager: "PaymentProcessor",
                       start_from_here: bool = False) -> bool:
        """
        Intenta procesar el pago:
        – Si esta cuenta tiene saldo >= request.amount y
          es la que le tocaba (start_from_here == True), procesa aquí.
        – Si no alcanza saldo, pasa al siguiente handler.
        """
        if start_from_here:
            if self.balance >= request.amount:
                self.balance -= request.amount
                key = self.key_fetcher.retrieve(jsonfile, self.token)
                manager.record_payment(PaymentRecord(
                    request.order_num, self.token, key, request.amount
                ))
                return True
        if self.next_handler:
            return self.next_handler.handle_request(
                request, jsonfile, manager, start_from_here=True
            )
        return False
```

---

## b) Nuevo componente con Chain of Responsibility para cuentas
> “b) La decisión se puede automatizar, basta que exista saldo en la cuenta y los pagos se hagan balanceados.

> d) Se realizará una clase usando cadena de comando que controle las dos cuentas (...) ambas inicialmente con saldo \$1000 y \$2000.”

**Modificación realizada:**
1. Se crea la clase **`PaymentProcessor`** inmediatamente después de `PaymentHandler`:
   * Recibe `jsonfile` y `accounts_info = [("token1", 1000.0), ("token2", 2000.0)]`.
   * Inicializa un Singleton `key_fetcher = JSONKeyFetcher()`.
   * Crea dos instancias de `PaymentHandlerConcrete`, una por cada cuenta, le pasa el `token`, el `initial_balance` y el `key_fetcher`.
   * Enlaza cada handler en cadena circular (`handler1.set_next(handler2)`, `handler2.set_next(handler1)`).
   * Lleva un índice `next_index_to_try` para alternar la cuenta inicial (round robin).
2. Se define la clase **`PaymentHandlerConcrete(PaymentHandler)`** que simplemente hereda la lógica (no agrega métodos nuevos).
3. El método **`process_payment(self, request)`** en `PaymentProcessor` realiza:
   ```python
   start_idx = self.next_index_to_try % len(self.handlers)
   handled = self.handlers[start_idx].handle_request(
       request, self.jsonfile, self, start_from_here=True
   )
   self.next_index_to_try = (self.next_index_to_try + 1) % n
   return handled
   ```
   De este modo, cada nueva llamada a `process_payment` arranca el intento en una cuenta distinta (cadena circular).

**Bloque agregado (en v3) después de `PaymentHandler`:**
```python
class PaymentProcessor:
    """
    Administra la cadena de handlers y las solicitudes de pago.
    – Mantiene lista de handlers en orden.
    – Alterna en “round robin” la cuenta inicial para cada pago.
    – Registra todos los PaymentRecord en orden cronológico.
    – Provee un Iterator para listar los pagos.
    """
    def __init__(self, jsonfile: str,
                 accounts_info: List[tuple[str, float]]):
        self.jsonfile = jsonfile
        self.handlers: List[PaymentHandler] = []
        self.next_index_to_try = 0  # para round robin
        self.payment_history: List[PaymentRecord] = []
        key_fetcher = JSONKeyFetcher()
        for token_name, init_balance in accounts_info:
            handler = PaymentHandlerConcrete(token_name,
                                             init_balance,
                                             key_fetcher)
            self.handlers.append(handler)
        for idx, handler in enumerate(self.handlers):
            next_idx = (idx + 1) % len(self.handlers)
            handler.set_next(self.handlers[next_idx])

    def process_payment(self, request: PaymentRequest) -> bool:
        n = len(self.handlers)
        start_idx = self.next_index_to_try % n
        handled = self.handlers[start_idx].handle_request(
            request, self.jsonfile, self, start_from_here=True
        )
        self.next_index_to_try = (self.next_index_to_try + 1) % n
        return handled

    def record_payment(self, record: PaymentRecord) -> None:
        self.payment_history.append(record)

    def __iter__(self) -> Iterator[PaymentRecord]:
        return iter(self.payment_history)

class PaymentHandlerConcrete(PaymentHandler):
    """
    Implementación concreta del PaymentHandler.
    """
    pass  # Toda la lógica de manejo está en PaymentHandler
```
* Hay dos cuentas (`token1` y `token2`) con saldos iniciales \$1000 y \$2000.
* Cada pago se envía a través de la cadena: si la cuenta inicial no tiene saldo, pasa a la siguiente.
* Se alterna cuál cuenta arranca el intento para balancear.

---

## c) Agregar iterador para listado de pagos (punto e)
> “e) Se realizarán pedidos de pago de \$500. … Prever una función de “listado” que muestre todos los pagos realizados por orden cronológico (utilizar un patrón iterator al efecto).”

**Modificación realizada:**
1. En la clase **`PaymentProcessor`**, se expone un **iterator** con:
   ```python
   def __iter__(self) -> Iterator[PaymentRecord]:
       return iter(self.payment_history)
   ```
2. La estructura `payment_history: List[PaymentRecord]` se llena cada vez que un handler procesa.
3. El sub-comando **`list`** de la CLI iterará sobre `processor` y mostrará cada `PaymentRecord`.

**Bloque CLI agregado en `v3` (parte `elif args.command == "list":`):**

```python
elif args.command == "list":
    historial = list(processor)
    if not historial:
        print("No hay pagos registrados aún.")
    else:
        print("Listado de pagos (cronológico):")
        for rec in historial:
            print(f" • Pedido {rec.order_num}: token='{rec.token}', "
                  f"clave='{rec.key}', monto=${rec.amount:.2f}")
```
Con esto se cumple el **punto (e)**: tenemos un Iterator que recorre cada pago en orden y la CLI muestra toda la lista.

---

## d) CLI robusta y versión 1.2 (punto f y g)
> f) De este punto, por inferencia pragmática o funcional típica en ciclos de desarrollo incremental, deduzco que debo mejorar el funcionamiento controlando que los argumentos sean correctos y termine con error controlado. Además, si el programa se ejecuta con ‘-v’, que emita la versión 1.2.”

> “g) Se documentará apropiadamente todo el programa.

**Modificación realizada:**
1. **Subcomandos con argparse** (`build_arg_parser_v3()`):
   * Posicionales:
     * `jsonfile` (ruta al JSON con las claves).
   * Subparsers:
     * `pay order_num [amount]`
     * `list`
   * Flag `-v/--version` → imprime versión y sale.
2. Validaciones:
   * Antes de instanciar `PaymentProcessor`, verifico que `jsonfile` exista:
     ```python
     if not os.path.isfile(jsonfile):
         print(f"ERROR: archivo no encontrado: {jsonfile}", file=sys.stderr)
         sys.exit(1)
     ```
   * En `process_payment`, si `JSONKeyFetcher` lanza `RuntimeError`, lo capturo y salgo con código 1.
   * Si `process_payment` retorna False (ninguna cuenta procesó el pago), imprimo:
     ```python
     print(f"ERROR: Ninguna cuenta tiene saldo suficiente para pedido {order} (${monto}).",
           file=sys.stderr)
     sys.exit(1)
     ```
3. **Version a 1.2**:
   * `VERSION = "1.2"`.
   * En `build_arg_parser_v3()` se define:
     ```python
     parser.add_argument(
         "-v", "--version",
         action="version",
         version=f"%(prog)s {VERSION}",
         help="muestra la versión del programa y sale."
     )
     ```
   * Al ejecutar `./get_jason_refactor_v3.py -v`, verá `get_jason_refactor_v3.py 1.2`.
4. **Control de errores en CLI**:
   * Si falta `jsonfile`, `argparse` obliga a pasarlo.
   * Si falta subcomando, `argparse` obliga a proveer alguno (con `required=True`).
   * Todos los errores de usuario se imprimen con: `print(..., file=sys.stderr)` y `sys.exit(1)` para no arrojar excepciones sin capturar.

**Bloque completo de `build_arg_parser_v3()` (en `v3`):**
```python
def build_arg_parser_v3() -> argparse.ArgumentParser:
    """
    Construye el parser de argumentos para la v1.2:
      • jsonfile         (obligatorio): sitedata.json
      • subcomando “pay” : order_num (int), amount (float; default=500)
      • subcomando “list”: no recibe args extra
      • -v/--version     : muestra versión y sale
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
    # Posicional: ruta al JSON
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
        help="Registra un pago de monto fijo (default $500) o especificado."
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
```

Con esto, **(f)** (control de argumentos y error controlado) y **(g)** (flag de versión 1.2) están implementados.

---

## e) Documentación final del programa (punto g)
> “g) Se documentará apropiadamente todo el programa.”

**Modificación realizada:**
* **Docstring de módulo** al tope de `get_jason_refactor_v3.py` que explica:
  * Propósito general.
  * Patrones de diseño usados: Singleton, Chain of Responsibility, Iterator.
  * Licencia/documento: “Copyright UADER-FCyT-IS2©2024…”.
* **Docstrings en cada clase y método público** explicando inputs, outputs y excepciones.
* **Comentarios en línea** que destacan dónde se implementa cada punto (a)–(f).

## f) Verificación con Pylint
> “h) Se hará una ejecución de verificación con pylint para chequear el resultado obteniendo un puntaje de 8 o superior. Hacer las modificaciones que fueran necesarias para conseguirlo.”

Para comprobar que el código cumple con un puntaje ≥ 8, ejecuté:
```bash
pylint get_jason_refactor_v3.py
```

**Salida (resumida):**
```
************* Module getJason_refactor_v3
getJason_refactor_v3.py:5:0: C0301: Line too long (104/100) (line-too-long)
getJason_refactor_v3.py:9:0: C0301: Line too long (105/100) (line-too-long)
getJason_refactor_v3.py:10:0: C0301: Line too long (106/100) (line-too-long)
getJason_refactor_v3.py:343:67: C0303: Trailing whitespace (trailing-whitespace)
getJason_refactor_v3.py:377:0: C0301: Line too long (102/100) (line-too-long)
getJason_refactor_v3.py:1:0: C0103: Module name "getJason_refactor_v3" doesn't conform to snake_case naming style (invalid-name)
getJason_refactor_v3.py:51:8: W0107: Unnecessary pass statement (unnecessary-pass)
getJason_refactor_v3.py:42:0: R0903: Too few public methods (1/2) (too-few-public-methods)
getJason_refactor_v3.py:197:4: W0107: Unnecessary pass statement (unnecessary-pass)
getJason_refactor_v3.py:329:15: W0718: Catching too general exception Exception (broad-exception-caught)
getJason_refactor_v3.py:399:0: R0914: Too many local variables (17/15) (too-many-locals)
getJason_refactor_v3.py:470:15: W0718: Catching too general exception Exception (broad-exception-caught)

-----------------------------------
Your code has been rated at 9.32/10
```

Como el puntaje final (`9.32/10`) es mayor que 8, se cumple el requisito sin necesidad de modificar nada más el código.

---

## 5. Ejecución paso a paso y ejemplos
Supongamos que arrancamos con carpeta vacía (solo está `get_jason_refactor_v3.py` y `sitedata.json`, sin `payment_state.json`). Veamos secuencia de pruebas:

### 5.1. Ver versión
```bash
$ ./get_jason_refactor_v3.py -v
get_jason_refactor_v3.py 1.2
```

### 5.2. Listado inicial (sin state file)
```bash
$ ./get_jason_refactor_v3.py sitedata.json list
No hay pagos registrados aún.
```
* Como no existe `payment_state.json`, parte vacía e imprime “No hay pagos registrados aún.”

### 5.3. Primer pago
```bash
$ ./get_jason_refactor_v3.py sitedata.json pay 1
Pedido 1: Pago de $500.00 procesado correctamente.
```
* Se inicia con saldos (`token1:1000`, `token2:2000`).
* Pago #1 (\$500) → “turno” de `token1`, saldo suficiente →
  `token1` queda en 1000–500 = 500.
* `JSONKeyFetcher` recupera la clave para `token1` (“C598-ECF9-F0F7-881A”).
* Se crea un `PaymentRecord(order_num=1, token='token1', key='C598-ECF9-F0F7-881A', amount=500.0)`.
* Se guarda el estado en `payment_state.json`, que ahora contendrá:
  ```json
  {
    "balances": {
      "token1": 500.0,
      "token2": 2000.0
    },
    "history": [
      {
        "order_num": 1,
        "token": "token1",
        "key": "C598-ECF9-F0F7-881A",
        "amount": 500.0
      }
    ]
  }
  ```

### 5.4. Segundo pago
```bash
$ ./get_jason_refactor_v3.py sitedata.json pay 2
Pedido 2: Pago de $500.00 procesado correctamente.
```
* Al arrancar, `main()` detecta que `payment_state.json` existe.
* Lo lee y extrae:
  * `initial_balances = {"token1": 500.0, "token2": 2000.0}`
  * `initial_history = [ {order_num:1, token:"token1", key:"…", amount:500.0} ]`
* Crea el `PaymentProcessor` con esos datos:
  * Handler para `token1` con balance 500.0
  * Handler para `token2` con balance 2000.0
  * Historial en memoria con un único `PaymentRecord #1`.
* Al llamar `pay 2`:
  * “turno” de `token1`: pero ya no tiene saldo (500 < 500?)
    
    *¡Ojo! 500 >= 500 es cierto, entonces aún alcanza. De hecho, con 500 alcanza.*
    * Queda en 0.0.
    * Se graba el pago #2 en historial con `token1` y saldo final 0.0.
  * Si quisieras que el segundo pago fuera a `token2`, tendrías que verificar el índice de “round robin”.
    
    En nuestra implementación, el índice se incrementa **luego** de cada `pay`, así:
    * 1° pago arrancó desde idx=0 (token1).
    * 2° pago arranca desde idx=1 (token2).
    * Pero si solo detecta que `token1` **aún** tenía 500 ≥ 500 (antes del 2° pago), se procesó ahí.
    * Para forzar que el segundo pago vaya a `token2`, podríamos hacer el “round robin” al inicio del método, antes de consultar saldos.
    * En la versión actual, usamos el índice *después* de procesar, así que es cierto que el 2° pago igualmente también lo procesó `token1`.
      Si queremos estrictamente alternar cuenta1–cuenta2 sin considerar saldo, habría que mover la actualización de índice *antes* del procesamiento.
  * Por simplicidad y coherencia con el ejemplo, consideremos que el “turno” se actualiza al final:
    > 1er pago: idx=0 (token1) → se procesó
    
    > luego se fijó `next_index_to_try=1`
    
    > 2° pago: idx=1 (token2) → si `token2` tuviera saldo ≥ 500, se procesaría allí.
    
    > En cada caso revisamos `start_from_here` en el `PaymentHandler`.
  * En la implementación provista, **el segundo pago (order\_num=2) irá a `token2`, no a `token1`**, porque antes de invocar el 2° `process_payment` se hizo `next_index_to_try=1`.
  * **Resultado**:

    * `token1` queda en 500
    * `token2` queda en 2000
    * Se procesó con `token2`, que llega a 1500
    * Historial pasa a:

      ```json
      "history": [
        {order_num:1, token:"token1", key:"…", amount:500.0},
        {order_num:2, token:"token2", key:"…", amount:500.0}
      ]
      ```
* Luego guarda `payment_state.json` actualizado con balances `{"token1":500.0,"token2":1500.0}` y ese historial de dos pagos.

### 5.5. Tercer pago, cuarto pago, etc.
Podemos seguir invocando `pay` varias veces. Cada vez:
* Se carga `payment_state.json` con los saldos e historial anteriores.
* Se crea el `PaymentProcessor` correspondiente.
* Se procesa un nuevo pedido:
  * Se intenta con la cuenta apuntada por `next_index_to_try`.
  * Si no alcanza saldo, deriva al siguiente.
  * Se almacena el pago en la historia y se actualiza el saldo en memoria.
* Se guarda el estado final de todos los saldos e historial en `payment_state.json`.

#### Ejemplo secuencial (resúmen simplificado):
1. Estado inicial:
   ```
   balances = { "token1": 1000, "token2": 2000 }
   history = []
   next_index_to_try = 0
   ```
2. `pay 1`:
   * idx=0 → token1 (1000 ≥ 500) → procesa → token1=500
   * Guarda state:
     ```json
     {
       "balances": { "token1": 500, "token2": 2000 },
       "history": [ {order_num:1, token:"token1", key:"…", amount:500} ]
     }
     ```
   * `next_index_to_try` pasa a 1.
3. `pay 2`:
   * Carga state previo.
   * idx=1 → token2 (2000 ≥ 500) → procesa → token2=1500
   * Guarda state:
     ```json
     {
       "balances": { "token1": 500, "token2": 1500 },
       "history": [
         {order_num:1, token:"token1", key:"…", amount:500},
         {order_num:2, token:"token2", key:"…", amount:500}
       ]
     }
     ```
   * `next_index_to_try` pasa a 0.
4. `pay 3 600`:
   * Carga state previo `{token1:500, token2:1500}`. idx=0 → token1 (500 < 600) → no alcanza → lo pasa a token2.
   * token2 (1500 ≥ 600) → procesa → token2=900
   * Guarda state:
     ```json
     {
       "balances": { "token1": 500, "token2": 900 },
       "history": [
         {order_num:1, token:"token1", key:"…", amount:500},
         {order_num:2, token:"token2", key:"…", amount:500},
         {order_num:3, token:"token2", key:"…", amount:600}
       ]
     }
     ```
   * `next_index_to_try` pasa a 1.
5. `pay 4 1000`:
   * Carga state previo `{token1:500, token2:900}`. idx=1 → token2 (900 < 1000) → no alcanza → deriva a token1.
   * token1 (500 < 1000) → tampoco alcanza → devuelve False.
   * Mensaje de error:
     ```
     ERROR: Ninguna cuenta tiene saldo suficiente para pedido 4 ($1000.0).
     ```
   * **No guarda state** (saldos e historial quedan tal como estaban).

### 5.6. Listar pagos
```bash
$ ./get_jason_refactor_v3.py sitedata.json list
Listado de pagos (cronológico):
 • Pedido 1: token='token1', clave='C598-ECF9-F0F7-881A', monto=$500.00
 • Pedido 2: token='token2', clave='C598-ECF9-F0F7-881B', monto=$500.00
 • Pedido 3: token='token2', clave='C598-ECF9-F0F7-881B', monto=$600.00
```
* Toma el estado actual de `payment_state.json` (que incluía tres pagos).
* Itera sobre `processor.payment_history` (que se reconstruyó en memoria)
  e imprime cada uno en orden.

---

## 6. Cómo resetear el sistema
Si querés volver a empezar desde saldos originales y sin historial, basta con **eliminar** (o renombrar) el archivo `payment_state.json`. Por ejemplo:
```bash
$ rm payment_state.json
```
La próxima invocación partirá desde:
```
balances = { "token1": 1000.0, "token2": 2000.0 }
history = []
```

---

## Detalles

Debido a la falta de persistencia y, por consiguiente, de sueldos y pagos, se agregó lo siguiente al programa:
```python
# =================================================================
# CORRECCIÓN: Restaurar turno en round-robin según cantidad de pagos
# =================================================================
processor.next_index_to_try = len(processor.payment_history) % len(processor.handlers)
```
Y además se agregó el archivo `payment_state.json`.
