# Calc API (FastAPI)

API mínima en FastAPI que reutiliza la función `sumar(a, b)` de `calc.py` para sumar dos números.

## Requisitos

- Python 3.8+
- Paquetes: `fastapi`, `uvicorn`

Instalación (opcional en entorno actual):

```powershell
python -m pip install fastapi uvicorn
```

## Ejecución

Desde la carpeta del proyecto:

```powershell
python -m uvicorn app:app --reload --port 8000
```

- Documentación interactiva: http://127.0.0.1:8000/docs
- Esquema OpenAPI (JSON): http://127.0.0.1:8000/openapi.json

## Endpoints

- GET `/` → Estado de la API.
- GET `/sumar?a=NUM&b=NUM` → Suma por query params.
- POST `/sumar` → Suma por JSON body `{ "a": NUM, "b": NUM }`.

## Ejemplos

GET (PowerShell):

```powershell
Invoke-RestMethod -Method GET "http://127.0.0.1:8000/sumar?a=3&b=4"
```

POST (PowerShell):

```powershell
Invoke-RestMethod -Method POST "http://127.0.0.1:8000/sumar" -ContentType "application/json" -Body (@{ a = 3; b = 4 } | ConvertTo-Json)
```

cURL (alternativa):

```bash
curl "http://127.0.0.1:8000/sumar?a=3&b=4"

curl -X POST "http://127.0.0.1:8000/sumar" \
  -H "Content-Type: application/json" \
  -d '{"a": 3, "b": 4}'
```

## Notas

- La documentación Swagger UI se genera automáticamente en `/docs`.
- La lógica de suma vive en `calc.py` y se importa en `app.py` para mantener una única fuente de verdad.
