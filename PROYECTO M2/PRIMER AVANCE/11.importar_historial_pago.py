import re
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from modelos import HistorialPagos  
from db_conector import engine      

# Crear sesión
Session = sessionmaker(bind=engine)
session = Session()

with open("DATA M2/12.historial_pagos.sql", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

# Expresión regular para capturar: (int, int, float, 'YYYY-MM-DD HH:MM:SS', 'Estado')
patron = re.compile(
    r"\(\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*,\s*'([\d\-:\s]+)'\s*,\s*'([^']+)'\s*\)", re.IGNORECASE
)

contador = 0

for linea in lineas:
    if "INSERT INTO HistorialPagos" in linea:
        match = patron.search(linea)
        if match:
            try:
                orden_id = int(match.group(1))
                metodo_id = int(match.group(2))
                monto = float(match.group(3))
                fecha = datetime.strptime(match.group(4), "%Y-%m-%d %H:%M:%S")
                estado = match.group(5)

                pago = HistorialPagos(
                    OrdenID=orden_id,
                    MetodoPagoID=metodo_id,
                    Monto=monto,
                    FechaPago=fecha,
                    EstadoPago=estado
                )
                session.add(pago)
                contador += 1
            except Exception as e:
                print(f"Error al procesar línea:\n{linea}\n{e}")

# Guardar cambios
try:
    session.commit()
    print(f"{contador} pagos insertados correctamente.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar en HistorialPagos:\n{e}")
finally:
    session.close()
