from fastapi import HTTPException

def validar_monto_positivo(monto: float):
    if monto <= 0:
        raise HTTPException(status_code=400, detail="El monto debe ser mayor a cero")

def validar_saldo_suficiente(saldo_actual: float, monto_retiro: float):
    if saldo_actual < monto_retiro:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar el retiro")

def validar_cedula(cedula: str):
    if len(cedula) != 10 or not cedula.isdigit():
        raise HTTPException(status_code=400, detail="La cédula debe tener exactamente 10 dígitos numéricos")