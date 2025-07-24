import re 
from sqlalchemy.orm import sessionmaker
from modelos import Productos
from db_conector import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("DATA M2/4.productos.sql", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()

# Busca todas las tuplas con 5 campos (usando comillas simples y separadas por coma)
# Captura: 'texto', 'texto', número, número, número
patron = re.compile(
    r"\('([^']*)'\s*,\s*'([^']*)'\s*,\s*([\d.]+)\s*,\s*(\d+)\s*,\s*(\d+)\)",
    re.IGNORECASE
)

matches = patron.findall(contenido)
contador = 0

for nombre, descripcion, precio, stock, categoria_id in matches:
    try:
        producto = Productos(
            Nombre=nombre,
            Descripcion=descripcion,
            Precio=float(precio),
            Stock=int(stock),
            CategoriaID=int(categoria_id)
        )
        session.add(producto)
        contador += 1
    except Exception as e:
        print(f"Error al procesar producto: {nombre}\n{e}")

try:
    session.commit()
    print(f"{contador} productos insertados correctamente.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar productos:\n{e}")
finally:
    session.close()