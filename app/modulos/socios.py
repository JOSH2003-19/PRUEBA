
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
import random
from .validaciones import validar_cedula

router = APIRouter(prefix="/socios", tags=["Socios"])

@router.post("/registrar")
def registrar_socio(nombre: str, cedula: str, db: Session = Depends(get_db)):
    validar_cedula(cedula)

    existente = db.query(models.Socio).filter(models.Socio.cedula == cedula).first()
    if existente:
        raise HTTPException(status_code=400, detail="La cédula ya está registrada")

    nuevo_socio = models.Socio(nombre=nombre, cedula=cedula)
    db.add(nuevo_socio)
    db.commit()
    db.refresh(nuevo_socio)

    nueva_cuenta = models.Cuenta(
        numero_cuenta=str(random.randint(100000, 999999)),
        saldo=0.0,
        socio_id=nuevo_socio.id
    )
    db.add(nueva_cuenta)
    db.commit()
    db.refresh(nueva_cuenta)

    return {
        "mensaje": "Socio y Cuenta creados",
        "socio": {"id": nuevo_socio.id, "nombre": nuevo_socio.nombre, "cedula": nuevo_socio.cedula},
        "cuenta": {"id": nueva_cuenta.id, "numero_cuenta": nueva_cuenta.numero_cuenta, "saldo": nueva_cuenta.saldo}
    }

@router.get("/listar")
def listar_socios(db: Session = Depends(get_db)):
    return db.query(models.Socio).all()
