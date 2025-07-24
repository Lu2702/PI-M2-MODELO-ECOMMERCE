import re
import unicodedata
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from modelos import Usuarios
from db_conector import engine

# Función para eliminar tildes/acentos
def eliminar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )

Session = sessionmaker(bind=engine)
session = Session()

with open("DATA M2/2.usuarios.sql", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

# Regex para extraer los valores dentro de VALUES(...)
patron = re.compile(r"VALUES\s*\((.*?)\);", re.IGNORECASE)

contador = 0

for linea in lineas:
    if "INSERT INTO Usuarios" in linea:
        match = patron.search(linea)
        if match:
            valores = match.group(1)
            campos = [v.strip().strip("'") for v in valores.split(",")]

            if len(campos) == 5:
                try:
                    nombre = str(campos[0])
                    apellido = str(campos[1])
                    dni = str(campos[2])
                    email = eliminar_acentos(campos[3].strip().replace(" ", ""))
                    contraseña = str(campos[4])
                    fecha_registro = datetime.now()

                    usuario = Usuarios(
                        Nombre=nombre,
                        Apellido=apellido,
                        dni=dni,
                        Email=email,
                        Contraseña=contraseña,
                        FechaRegistro=fecha_registro
                    )
                    session.add(usuario)
                    contador += 1

                except Exception as e:
                    print(f"Error al procesar línea:\n{linea}\n{e}")

try:
    session.commit()
    print(f"{contador} usuarios insertados correctamente.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar usuarios:\n{e}")
finally:
    session.close()