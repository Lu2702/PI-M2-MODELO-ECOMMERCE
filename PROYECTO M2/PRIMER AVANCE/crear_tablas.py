from db_conector import get_db_engine, Base
from modelos import Usuarios, Categorias, Productos, Ordenes, DetalleOrdenes, DireccionesEnvio, Carrito, MetodosPago, OrdenesMetodosPago, ReseñasProductos, HistorialPagos
def main():
    engine = get_db_engine()
    try:
        Base.metadata.create_all(bind=engine)
        print("Todas las tablas fueron creadas exitosamente.")
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()