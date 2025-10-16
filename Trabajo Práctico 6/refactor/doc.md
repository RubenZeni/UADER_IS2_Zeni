### Detalles
- Docstring arriba explica uso y ejemplos.
- ```print_usage()``` muestra ayuda estandarizada.
- Validaciones de args, existencia de archivo, decodificación JSON y existencia de clave.
- ```sys.exit(1)``` en todos los errores, de acuerdo a buenas práctica.

### Casos de prueba
**Sin args**:
```
./getJason_mod.py
```
> ERROR: número de argumentos inválido.
  Uso: getJason_mod.py <jsonfile> [jsonkey]
    jsonfile : ruta al archivo JSON
    jsonkey  : (opcional) clave dentro del JSON; default 'token1'

**Solo JSON**:
```
./getJason_mod.py sitedata.json
```
> C598-ECF9-F0F7-881A.

**JSON + token2**:
```
./getJason_mod.py sitedata.json token2
```
> C598-ECF9-F0F7-881B.

**JSON + clave inexistente**:
```
./getJason_mod.py sitedata.json tokenX
```
> ERROR: clave 'tokenX' no existe en sitedata.json

**Archivo inválido**:
```
./getJason_mod.py no_existe.json
```
> ERROR: archivo no encontrado: no_existe.json

**Demasiados args**:
```
./getJason_mod.py a b c
```
> ERROR: número de argumentos inválido.
  Uso: getJason_mod.py <jsonfile> [jsonkey]
    jsonfile : ruta al archivo JSON
    jsonkey  : (opcional) clave dentro del JSON; default 'token1'

---

En la carpeta **```raíz/refactor/```** se encuentra el ```.pyc``` compilado con ```python3 -m compileall getJason_mod.py```.
