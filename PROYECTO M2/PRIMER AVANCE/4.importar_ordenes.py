import re
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from modelos import Ordenes
from db_conector import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("DATA M2/5.ordenes.sql", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

# Captura: (int, 'YYYY-MM-DD HH:MM:SS', float, 'Estado')
patron = re.compile(
    r"\(\s*(\d+)\s*,\s*'([\d\-:\s]+)'\s*,\s*([\d.]+)\s*,\s*'([^']+)'\s*\)", re.IGNORECASE
)

contador = 0

for linea in lineas:
    if "INSERT INTO Ordenes" in linea:
        match = patron.search(linea)
        if match:
            try:
                usuario_id = int(match.group(1))
                fecha = datetime.strptime(match.group(2), "%Y-%m-%d %H:%M:%S")
                total = float(match.group(3))
                estado = match.group(4)

                orden = Ordenes(
                    UsuarioID=usuario_id,
                    FechaOrden=fecha,
                    Total=total,
                    Estado=estado
                )
                session.add(orden)
                contador += 1
            except Exception as e:
                print(f"Error al procesar línea:\n{linea}\n{e}")

try:
    session.commit()
    print(f"{contador} órdenes insertadas correctamente.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar órdenes:\n{e}")
finally:
    session.close()
