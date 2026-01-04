
# app/database.py
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Cargar variables desde .env ubicado en la carpeta app ---
ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)

# Si DATABASE_URL no está, usar un archivo SQLite dentro de app/
DEFAULT_DB_PATH = Path(os.path.dirname(__file__)) / "caja.db"
DEFAULT_SQLITE_URL = f"sqlite:///{DEFAULT_DB_PATH}"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# Para SQLite + FastAPI/uvicorn (threads)
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# --- Crear Engine ---
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False  # Cambia a True si deseas ver el SQL en consola
)

# --- Session y Base compartida ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Dependencia para FastAPI ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
