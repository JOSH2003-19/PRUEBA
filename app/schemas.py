
# app/schemas.py
from pydantic import BaseModel, Field

class SocioCreate(BaseModel):
    nombre: str = Field(min_length=1)
    cedula: str = Field(min_length=10, max_length=10)

class TransaccionPorCedula(BaseModel):
    cedula: str = Field(min_length=10, max_length=10)
    tipo: str   # "DEPOSITO" o "RETIRO"
    monto: float

class PrestamoPorCedula(BaseModel):
    cedula: str = Field(min_length=10, max_length=10)
    monto: float
    meses: int
