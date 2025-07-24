import re
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from modelos import OrdenesMetodosPago
from db_conector import engine

Session = sessionmaker(bind=engine)
session = Session()

# Leer archivo SQL
with open("DATA M2/10.ordenes_metodospago.sql", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

# Expresión regular para capturar: (int, int, float)
patron = re.compile(r"\(\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)", re.IGNORECASE)

contador = 0

for linea in lineas:
    if "INSERT INTO OrdenesMetodosPago" in linea:
        match = patron.search(linea)
        if match:
            try:
                orden_id = int(match.group(1))
                metodo_pago_id = int(match.group(2))
                monto_pagado = float(match.group(3))

                entrada = OrdenesMetodosPago(
                    OrdenID=orden_id,
                    MetodoPagoID=metodo_pago_id,
                    MontoPagado=monto_pagado
                )
                session.add(entrada)
                contador += 1
            except Exception as e:
                print(f"Error al procesar línea:\n{linea}\n{e}")

try:
    session.commit()
    print(f"{contador} registros insertados en OrdenesMetodosPago correctamente.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar en OrdenesMetodosPago:\n{e}")
finally:
    session.close()
