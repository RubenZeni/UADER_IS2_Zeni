# Multimetric

## Antes de los cambios:

#### Comando utilizado:
```bash
multimetric src/chatGPT/chat.py > doc/multimetric/multimetric_output_1.txt
```
#### Sección *Overall* de las métricas obtenidas:
```txt
  "overall": {
    "comment_ratio": 17.498,
    "cyclomatic_complexity": 0,
    "fanout_external": 5,
    "fanout_internal": 0,
    "halstead_bugprop": 0.487,
    "halstead_difficulty": 23.37,
    "halstead_effort": 34118.736,
    "halstead_timerequired": 1895.485,
    "halstead_volume": 1459.937,
    "loc": 65,
    "maintainability_index": 65.487,
    "operands_sum": 123,
    "operands_uniq": 50,
    "operators_sum": 116,
    "operators_uniq": 19,
    "pylint": 100.0,
    "tiobe": 99.769,
    "tiobe_compiler": 100.0,
    "tiobe_complexity": 98.462,
    "tiobe_coverage": 100.0,
    "tiobe_duplication": 100.0,
    "tiobe_fanout": 100.0,
    "tiobe_functional": 100.0,
    "tiobe_security": 100.0,
    "tiobe_standard": 100.0
  }
```
---

## Cambios realizados:

| Valores exigidos | Antes | Después | Detalles de cambios |
|---|---|---|---|
| Comment Ratio | 17.498% | 33.21% | Añadí docstrings y comentarios inline, aumentando el valor por encima del 33%. Queda bien documentado. |
| Halstead Effort | 34118.736 | 38601.348 | El Halstead Effort aumentó ≈4482 unidades debido al mayor volumen introducido por la documentación. |
| Halstead Timerequired | 1895.485 | 2144.519 | El tiempo estimado subió ≈249 s (≈4.15 min), reflejando el mayor volumen de código. |
| Halstead Bugprop | 0.487 | 0.502 | La probabilidad teórica de bugs aumentó levemente, también, por el incremento de volumen. |

- *cyclomatic_complexity: 0*
  - Al ser nulo el valor, no es necesario aplicar estrategias para minimizarlo.
- Cantidad de defectos reales solucionados: 2
  - Ambos errores surgieron debido a la falta de librerías.
- Tiempo real de desarrollo y depuración estimado: 7200 s


---

## Después de los cambios:

#### Comando utilizado:
```bash
multimetric src/chatGPT/chat.py > doc/multimetric/multimetric_output_2.txt
```
#### Sección *Overall* de las métricas despés de los cambios:
```txt
  "overall": {
    "comment_ratio": 33.21,
    "cyclomatic_complexity": 0,
    "fanout_external": 5,
    "fanout_internal": 0,
    "halstead_bugprop": 0.502,
    "halstead_difficulty": 25.62,
    "halstead_effort": 38601.348,
    "halstead_timerequired": 2144.519,
    "halstead_volume": 1506.688,
    "loc": 68,
    "maintainability_index": 64.592,
    "operands_sum": 122,
    "operands_uniq": 50,
    "operators_sum": 123,
    "operators_uniq": 21,
    "pylint": 100.0,
    "tiobe": 99.769,
    "tiobe_compiler": 100.0,
    "tiobe_complexity": 98.462,
    "tiobe_coverage": 100.0,
    "tiobe_duplication": 100.0,
    "tiobe_fanout": 100.0,
    "tiobe_functional": 100.0,
    "tiobe_security": 100.0,
    "tiobe_standard": 100.0
  }
```
