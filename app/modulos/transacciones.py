
from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .validaciones import validar_monto_positivo, validar_saldo_suficiente, validar_cedula
from ..services import get_socio_by_cedula, get_first_cuenta_of_socio

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

class TipoOperacion(str, Enum):
    DEPOSITO = "DEPOSITO"
    RETIRO   = "RETIRO"

@router.post("/operacion-por-cedula")
def realizar_transaccion_por_cedula(
    cedula: str,
    tipo: TipoOperacion = Query(..., description="DEPOSITO o RETIRO"),
    monto: float = Query(..., gt=0.0, description="Monto > 0"),
    db: Session = Depends(get_db),
):
    validar_cedula(cedula)
    validar_monto_positivo(monto)

    socio = get_socio_by_cedula(db, cedula)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")

    cuenta = get_first_cuenta_of_socio(db, socio.id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada para el socio")

    if tipo == TipoOperacion.RETIRO:
        validar_saldo_suficiente(cuenta.saldo, monto)
        cuenta.saldo -= monto
    else:
        cuenta.saldo += monto

    trans = models.Transaccion(tipo=tipo.value, monto=monto, cuenta_id=cuenta.id)
    db.add(trans)
    db.commit()

    return {"mensaje": "Transacción exitosa", "cedula": cedula, "cuenta_id": cuenta.id, "nuevo_saldo": cuenta.saldo}
