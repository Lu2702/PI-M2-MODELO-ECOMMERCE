import re
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from modelos import ReseñasProductos  
from db_conector import engine        

# Crear sesión
Session = sessionmaker(bind=engine)
session = Session()

with open("DATA M2/11.resenas_productos.sql", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

# Expresión regular para capturar los datos del INSERT
# Captura: (int, int, int, 'comentario', 'fecha')
patron = re.compile(
    r"\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*'([^']*)'\s*,\s*'([\d\-:\s]+)'\s*\)", re.IGNORECASE
)

contador = 0

for linea in lineas:
    if "INSERT INTO ReseñasProductos" in linea:
        match = patron.search(linea)
        if match:
            try:
                usuario_id = int(match.group(1))
                producto_id = int(match.group(2))
                calificacion = int(match.group(3))
                comentario = match.group(4)
                fecha = datetime.strptime(match.group(5), "%Y-%m-%d %H:%M:%S")

                reseña = ReseñasProductos(
                    UsuarioID=usuario_id,
                    ProductoID=producto_id,
                    Calificacion=calificacion,
                    Comentario=comentario,
                    Fecha=fecha
                )
                session.add(reseña)
                contador += 1
            except Exception as e:
                print(f"Error al procesar línea:\n{linea}\n{e}")

# Guardar en la base de datos
try:
    session.commit()
    print(f"{contador} reseñas insertadas correctamente.")
except Exception as e:
    session.rollback()
    print(f"Error al insertar reseñas:\n{e}")
finally:
    session.close()