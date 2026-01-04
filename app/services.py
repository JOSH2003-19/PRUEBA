
# app/services.py
from sqlalchemy.orm import Session
from . import models

def get_socio_by_cedula(db: Session, cedula: str) -> models.Socio | None:
    return db.query(models.Socio).filter(models.Socio.cedula == cedula).first()

def get_first_cuenta_of_socio(db: Session, socio_id: int) -> models.Cuenta | None:
    # Política simple: tomar la primera cuenta asociada
    return db.query(models.Cuenta).filter(models.Cuenta.socio_id == socio_id).first()
