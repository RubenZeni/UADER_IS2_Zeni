
## Trabajo Práctico N°7 "Ingeniería Reversa, Re-Factoría y Re-Ingeniería", sobre `getJason_mod.py`.

---

## 1. Objetivo  
Partiendo del bytecode legado (`getJason.pyc`) y su decompilado original (`getJason.py`), refactorizar el programa para:

1. Reusar y extender la funcionalidad (parámetros CLI, default clave, versión).
2. Aplicar Programación Orientada a Objetos (interfaz, Singleton).
3. Robustecer la CLI con `argparse`, manejo controlado de errores y flag de versión.
4. Cumplir guía de estilo **Pylint ≥ 8.0**.

---

## 2. Archivos y versiones  

| Archivo                          | Descripción                                  |
|----------------------------------|----------------------------------------------|
| `getJason.pyc`                   | Bytecode legado (Python 3.7).                |
| `sitedata.json`                  | JSON de prueba con `"token1"` y `"token2"`.  |
| `getJason.py`                    | Código decompilado original (hardcodea key). |
| **Refactor**                     |                                              |
| `getJason_mod.py`                | Versión procedimental con `sys.argv`.        |
| `getJason_refactor_v1.py`        | Primera versión OOP+Singleton+argparse.      |
| `getJason_refactor_v2.py`        | Ajustes tras Pylint → nombre módulo, docstrings, encoding, raises. |
| **Análisis de Pylint**           |                                              |
| `pylint_test1.txt`               | Informe de `v1` (puntuación 7.76/10).        |
| `pylint_test2.txt`               | Informe de `v2` (puntuación 9.32/10).        |

---

## 3. Metodología de Re-Factoría

1. **Branching by Abstraction**
   - Definimos la interface `IKeyRetriever` (abstract class).
   - Implementamos `JSONKeyFetcher` como Singleton.
   - Permitimos futura extensión sin romper el legado.

2. **OOP & Singleton**
   - `JSONKeyFetcher.__new__()`: única instancia.
   - `retrieve(filepath, key)` expone API limpia.

3. **CLI robusta**
   - `argparse` maneja:
     - Posicionales: `jsonfile` (obligatorio), `jsonkey` (opcional, default `token1`).
     - Flag `-v/--version` → imprime “versión 1.1”.
   - Uso de `parser.error()` y `RuntimeError` para terminar con códigos controlados.

4. **Control de errores**
   - Archivo inexistente → mensaje y `sys.exit(1)`.
   - JSON malformado → `RuntimeError` con `from`.
   - Clave no hallada → `RuntimeError`.
   - Captura “broad exception” eliminada; solo `RuntimeError` propagada.

5. **Pylint**
   - **V1** (`getJason_refactor_v1.py`): revisión arrojó 7.76/10 → faltaban docstrings, encoding, nombrado de módulo.
   - **V2** (`get_jason_refactor.py`, renombrado snake_case):
     - Módulo docstring (C0114).
     - Funciones y métodos documentados (C0116).
     - `open(..., encoding='utf-8')` (W1514).
     - `raise … from exc` (W0707).
     - Eliminados args/kwargs no usados.
     - Desactivado `too-few-public-methods` con pragma.
   - **Resultado**: 9.32/10.

---

## 4. Resumen de Cambios vs. Versión Procedimental

| Aspecto                  | `getJason_mod.py`             | `get_jason_refactor.py`                  |
|--------------------------|-------------------------------|-------------------------------------------|
| Estructura               | Funciones libres              | Clase Singleton + Interface abstracta    |
| CLI                      | `sys.argv` manual             | `argparse` con help, error y version flag|
| Errores                  | `sys.exit(1)` directo         | `RuntimeError` controlado y `parser.error()` |
| Documentación interna    | Docstring en módulo y uso     | Docstrings en módulo, clases y métodos   |
| Testing de estilo        | —                             | Pylint ≥ 8.0 (obtenido 9.32/10)           |

---

## 5. Casos de Prueba (`get_jason_refactor.py`)

```bash
$ ./get_jason_refactor.py -v
get_jason_refactor.py 1.1

$ ./get_jason_refactor.py
usage: get_jason_refactor.py [-h] [-v] jsonfile [jsonkey]
get_jason_refactor.py: error: the following arguments are required: jsonfile

$ ./get_jason_refactor.py sitedata.json
C598-ECF9-F0F7-881A

$ ./get_jason_refactor.py sitedata.json token2
C598-ECF9-F0F7-881B

$ ./get_jason_refactor.py sitedata.json missing
ERROR: clave 'missing' no existe en sitedata.json

$ ./get_jason_refactor.py no_file.json
ERROR: archivo no encontrado: no_file.json

$ ./get_jason_refactor.py a b c
usage: get_jason_refactor.py [-h] [-v] jsonfile [jsonkey]
get_jason_refactor.py: error: unrecognized arguments: c
````

---

## 6. Conclusiones

* La **re-factoría** orientada a objetos y el patrón **Singleton** facilitan la extensión futura.
* `argparse` y manejo controlado de errores mejoran la robustez y la UX CLI.
* El scoring de **Pylint > 8** garantiza calidad de código y estandarización.
* Queda listo para su integración en producción, con código claro, testable y mantenible.

---

**Nota:** El desarrollo de los códigos para el Trabajo Práctico lo realicé con la ayuda de *ChatGPT*, es por esto que ```main()``` se ve tan afectado y el desarrollo es relativamente basto.
No obstante, sin mi continua atención e intervención, el mismo sería mucho más burdo y estaría más desconectado de la idea y visión general.
