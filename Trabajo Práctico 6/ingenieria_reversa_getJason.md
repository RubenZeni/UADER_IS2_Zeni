## Archivos disponibles
```getJason.pyc```

```sitedata.json```

**No hay documentación externa.**

#### Programa
- Debe recuperar cualquier clave existente en el archivo JSON indicándola como argumento, siendo el default "token1".
- Requiere al menos 1 argumento (sys.argv[1]).
- Hard-codea jsonkey = 'token1'.
- No acepta key distinto de token1.
---
El ```getJason.py``` decompilado:
- Toma único parámetro de entrada → nombre de archivo JSON.
- Fija la clave a buscar en 'token1'.
- Parsea todo el JSON.
- Imprime el valor de esa clave.
---
Si invoco con **```python3 getJason.pyc sitedata.json```**:
- Imprime **C598-ECF9-F0F7-881A**.
- No permite cambiar jsonkey.
- Si no le pasás args, cruza un IndexError.
- Si el archivo no existe, arroja FileNotFoundError.
- **Caso exitoso**: 1 arg → imprime token1.
- **Errores posibles**: falta arg, archivo inválido, key inexistente (KeyError).
---
**Flujo de datos**
```
Usuario → getJason.pyc: args
getJason.pyc ──> sys.argv[1]
getJason.pyc ──> open(JSON)
getJason.pyc ──> json.loads → dict
getJason.pyc ──> dict['token1']
getJason.pyc ──> escribe en stdout
```
