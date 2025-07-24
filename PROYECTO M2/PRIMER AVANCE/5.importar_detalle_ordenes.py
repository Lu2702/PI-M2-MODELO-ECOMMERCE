import re
from sqlalchemy.orm import sessionmaker
from modelos import DetalleOrdenes
from db_conector import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("DATA M2/6.detalle_ordenes.sql", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

patron = re.compile(r"\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)")
contador = 0

for linea in lineas:
    if "INSERT INTO DetalleOrdenes" in linea:
        match = patron.search(linea)
        if match:
            try:
                orden_id = int(match.group(1))
                producto_id = int(match.group(2))
                cantidad = int(match.group(3))
                precio_unitario = float(match.group(4))

                detalle = DetalleOrdenes(
                    OrdenID=orden_id,
                    ProductoID=producto_id,
                    Cantidad=cantidad,
                    PrecioUnitario=precio_unitario
                )
                session.add(detalle)
                contador += 1
            except Exception as e:
                print(f"Error en línea:\n{linea}\n{e}")

try:
    session.commit()
    print(f"{contador} registros insertados en DetalleOrdenes.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar en DetalleOrdenes:\n{e}")
finally:
    session.close()