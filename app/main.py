
# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import engine, get_db, DATABASE_URL
from . import models
from .modulos import socios, transacciones, prestamos
import logging

# --- CONFIGURACIÓN DE LOGGING (AUDITORÍA) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("app.main")

app = FastAPI(title="Sistema Caja de Ahorros - Grupo D (SQLite Edition)")

# Crear tablas automáticamente al iniciar
models.Base.metadata.create_all(bind=engine)

# Registrar Módulos del Sistema
app.include_router(socios.router)
app.include_router(transacciones.router)
app.include_router(prestamos.router)

@app.on_event("startup")
async def startup_event():
    logger.info(">>> SISTEMA INICIADO: Conexión con SQLite verificada.")
    logger.info(f">>> DATABASE_URL: {DATABASE_URL}")

@app.get("/")
def inicio():
    return {"mensaje": "API Grupo D Online y Operativa (SQLite)"}

@app.get("/salud", tags=["Mantenimiento"])
def verificar_salud(db: Session = Depends(get_db)):
    """Verifica si la base de datos SQLite responde correctamente"""
    try:
        db.execute(text("SELECT 1")) 
        return {"status": "online", "database": "Conectado a SQLite"}
    except Exception as e:
        logger.error(f"Error de conexión con SQLite: {e}")
        return {"status": "error", "detalle": str(e)}
