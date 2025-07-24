import re
from sqlalchemy.orm import sessionmaker
from modelos import DireccionesEnvio
from db_conector import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("DATA M2/7.direcciones_envio.sql", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

patron = re.compile(
    r"\(\s*(\d+)\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*\)"
)

contador = 0

for linea in lineas:
    if "INSERT INTO DireccionesEnvio" in linea:
        match = patron.search(linea)
        if match:
            try:
                direccion = DireccionesEnvio(
                    UsuarioID=int(match.group(1)),
                    Calle=match.group(2),
                    Ciudad=match.group(3),
                    Departamento=match.group(4),
                    Provincia=match.group(5),
                    Distrito=match.group(6),
                    Estado=match.group(7),
                    CodigoPostal=match.group(8),
                    Pais=match.group(9)
                )
                session.add(direccion)
                contador += 1
            except Exception as e:
                print(f"Error al procesar línea:\n{linea}\n{e}")

try:
    session.commit()
    print(f"{contador} direcciones insertadas correctamente.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar direcciones:\n{e}")
finally:
    session.close()
