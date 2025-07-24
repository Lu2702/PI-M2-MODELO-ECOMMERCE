import re 
from sqlalchemy.orm import sessionmaker
from modelos import Categorias
from db_conector import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("DATA M2/3.categorias.sql", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()

# Encuentra todas las tuplas de valores ('nombre', 'descripcion')
patron = re.compile(r"\('([^']*)'\s*,\s*'([^']*)'\)", re.IGNORECASE)
matches = patron.findall(contenido)

contador = 0

for nombre, descripcion in matches:
    categoria = Categorias(
        Nombre=nombre,
        Descripcion=descripcion,
    )
    session.add(categoria)
    contador += 1

try:
    session.commit()
    print(f"{contador} categorías insertadas correctamente.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar categorías:\n{e}")
finally:
    session.close()