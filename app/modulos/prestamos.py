
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .validaciones import validar_monto_positivo, validar_cedula
from ..services import get_socio_by_cedula

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])

@router.post("/solicitar-por-cedula")
def solicitar_prestamo_por_cedula(
    cedula: str,
    monto: float = Query(..., gt=0.0, description="Monto > 0"),
    meses: int = Query(..., gt=0, description="Meses >= 1"),
    db: Session = Depends(get_db)
):
    validar_cedula(cedula)
    validar_monto_positivo(monto)

    socio = get_socio_by_cedula(db, cedula)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")

    nuevo_prestamo = models.Prestamo(monto_aprobado=monto, cuotas=meses, socio_id=socio.id)
    db.add(nuevo_prestamo)
    db.commit()

    valor_cuota = monto / meses
    tabla = [{"mes": i+1, "cuota": valor_cuota} for i in range(meses)]

    return {
        "mensaje": "Préstamo aprobado",
        "socio": {"id": socio.id, "nombre": socio.nombre, "cedula": socio.cedula},
        "tabla_amortizacion": tabla
    }
