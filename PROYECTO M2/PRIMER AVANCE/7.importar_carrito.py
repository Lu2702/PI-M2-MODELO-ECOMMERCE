import re
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from modelos import Carrito
from db_conector import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("DATA M2/8.carrito.sql", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

# Captura: (UsuarioID, ProductoID, Cantidad, 'YYYY-MM-DD HH:MM:SS')
patron = re.compile(
    r"\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*'([\d\-:\s]+)'\s*\)", re.IGNORECASE
)

contador = 0

for linea in lineas:
    if "INSERT INTO Carrito" in linea:
        match = patron.search(linea)
        if match:
            try:
                usuario_id = int(match.group(1))
                producto_id = int(match.group(2))
                cantidad = int(match.group(3))
                fecha = datetime.strptime(match.group(4), "%Y-%m-%d %H:%M:%S")

                carrito = Carrito(
                    UsuarioID=usuario_id,
                    ProductoID=producto_id,
                    Cantidad=cantidad,
                    FechaAgregado=fecha
                )
                session.add(carrito)
                contador += 1
            except Exception as e:
                print(f"Error al procesar línea:\n{linea}\n{e}")

try:
    session.commit()
    print(f"{contador} registros insertados correctamente en Carrito.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar en Carrito:\n{e}")
finally:
    session.close()
