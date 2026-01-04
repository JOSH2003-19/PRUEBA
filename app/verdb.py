
# ver_db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("caja.db")

def main():
    if not DB_PATH.exists():
        print(f" No se encontró la base de datos en: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Listar tablas
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tablas = [r["name"] for r in cur.fetchall()]
    print("📦 Tablas en la base:", tablas)

    # Contar registros por tabla
    for t in tablas:
        try:
            cur.execute(f"SELECT COUNT(*) AS c FROM {t};")
            c = cur.fetchone()["c"]
            print(f"   - {t}: {c} registros")
        except sqlite3.Error as e:
            print(f"   - {t}: error al contar -> {e}")

    conn.close()

if __name__ == "__main__":
    main()
