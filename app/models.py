
# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from .database import Base

class Socio(Base):
    __tablename__ = "socios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    cedula = Column(String(10), unique=True)

    cuentas = relationship("Cuenta", back_populates="titular", cascade="all, delete-orphan")
    prestamos = relationship("Prestamo", back_populates="socio", cascade="all, delete-orphan")

class Cuenta(Base):
    __tablename__ = "cuentas"
    id = Column(Integer, primary_key=True, index=True)
    numero_cuenta = Column(String(20), unique=True)
    saldo = Column(Float, default=0.0)
    socio_id = Column(Integer, ForeignKey("socios.id"))

    titular = relationship("Socio", back_populates="cuentas")
    transacciones = relationship("Transaccion", back_populates="cuenta", cascade="all, delete-orphan")

class Transaccion(Base):
    __tablename__ = "transacciones"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20))  # DEPOSITO o RETIRO
    monto = Column(Float)
    # Portátil para SQLite: CURRENT_TIMESTAMP
    fecha = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    cuenta_id = Column(Integer, ForeignKey("cuentas.id"))

    cuenta = relationship("Cuenta", back_populates="transacciones")

class Prestamo(Base):
    __tablename__ = "prestamos"
    id = Column(Integer, primary_key=True, index=True)
    monto_aprobado = Column(Float)
    cuotas = Column(Integer)
    socio_id = Column(Integer, ForeignKey("socios.id"))

    socio = relationship("Socio", back_populates="prestamos")

