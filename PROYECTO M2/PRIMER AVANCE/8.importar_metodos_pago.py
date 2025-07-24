import re
from sqlalchemy.orm import sessionmaker
from modelos import MetodosPago
from db_conector import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("DATA M2\9.metodos_pago.sql", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()

# Buscar múltiples valores en una sola instrucción INSERT
patron = re.compile(r"\(\s*'([^']*)'\s*,\s*'([^']*)'\s*\)", re.IGNORECASE)

coincidencias = patron.findall(contenido)
contador = 0

for nombre, descripcion in coincidencias:
    metodo = MetodosPago(
        Nombre=nombre,
        Descripcion=descripcion
    )
    session.add(metodo)
    contador += 1

try:
    session.commit()
    print(f"{contador} métodos de pago insertados correctamente.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar métodos de pago:\n{e}")
finally:
    session.close()