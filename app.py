from fastapi import FastAPI, Query
from pydantic import BaseModel

from calc import sumar


app = FastAPI(
    title="Calc API",
    description="API sencilla para sumar dos números usando la función existente `sumar(a, b)`.",
    version="1.0.0",
)


class SumaRequest(BaseModel):
    a: float
    b: float


class SumaResponse(BaseModel):
    resultado: float


@app.get("/", summary="Estado de la API")
def root() -> dict:
    return {"status": "ok"}


@app.get(
    "/sumar",
    response_model=SumaResponse,
    summary="Suma dos números (query)",
    description="Proporciona `a` y `b` como parámetros de consulta para obtener la suma.",
)
def sumar_query(
    a: float = Query(..., description="Primer número"),
    b: float = Query(..., description="Segundo número"),
) -> SumaResponse:
    return SumaResponse(resultado=sumar(a, b))


@app.post(
    "/sumar",
    response_model=SumaResponse,
    summary="Suma dos números (JSON)",
    description="Envía un cuerpo JSON con `a` y `b` para obtener la suma.",
)
def sumar_body(payload: SumaRequest) -> SumaResponse:
    return SumaResponse(resultado=sumar(payload.a, payload.b))

