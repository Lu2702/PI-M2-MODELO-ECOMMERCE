from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, DateTime, func, CheckConstraint, Text
from sqlalchemy.orm import relationship
# importa la base en comun 
from db_conector import Base 

# Tabla usuarios 
class Usuarios(Base):
    __tablename__= 'Usuarios'
    UsuarioID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Apellido = Column(String(100), nullable=False)
    dni = Column(String(20), nullable=False, unique=True)
    Email = Column(String(255), nullable=False, unique=True)
    Contraseña = Column(String(255), nullable=False)
    FechaRegistro = Column(DateTime, default=func.now())

    ordenes = relationship("Ordenes", back_populates="usuario")
    direcciones = relationship("DireccionesEnvio", back_populates="usuario")
    carrito = relationship("Carrito", back_populates="usuario")
    resenas_productos = relationship("ReseñasProductos", back_populates="usuario")

    def __repr__(self):
        return f"<usuario(Nombre={self.Nombre}, Apellido={self.Apellido}, dni={self.dni})>"

# Tabla categorias
class Categorias(Base):
    __tablename__= 'Categorias'
    CategoriaID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(255), nullable=False)

    productos = relationship("Productos", back_populates="categoria")

    def __repr__(self):
        return f"<categoria(Nombre={self.Nombre})>"

# Tabla productos
class Productos(Base):
    __tablename__ = 'Productos'
    ProductoID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(255), nullable=False, unique=True)
    Descripcion = Column(String, nullable=False)
    Precio = Column(Numeric(10, 2), nullable=False)
    Stock = Column(Integer, nullable=False)
    CategoriaID = Column(Integer, ForeignKey('Categorias.CategoriaID'), nullable=False)

    categoria = relationship("Categorias", back_populates="productos")
    detalle = relationship("DetalleOrdenes", back_populates="producto")
    carrito = relationship("Carrito", back_populates="producto")
    resenas_productos = relationship("ReseñasProductos", back_populates="producto")

    def __repr__(self):
        return f"<producto(ProductoID={self.ProductoID}, Nombre={self.Nombre}, Precio={self.Precio})>"

# Tabla ordenes
class Ordenes(Base):
    __tablename__ = 'Ordenes'
    OrdenID = Column(Integer, primary_key=True, autoincrement=True)
    UsuarioID = Column(Integer, ForeignKey('Usuarios.UsuarioID'), nullable=False)
    FechaOrden = Column(DateTime, default=func.now())
    Total = Column(Numeric(10, 2), nullable=False)
    Estado = Column(String(50), default='Pendiente', nullable=False)

    usuario = relationship("Usuarios", back_populates="ordenes")
    detalle = relationship("DetalleOrdenes", back_populates="orden")
    historial_pago = relationship("HistorialPagos", back_populates="orden")
    orden_metodo_pago = relationship("OrdenesMetodosPago", back_populates="orden")

    def __repr__(self):
        return f"<orden(OrdenID={self.OrdenID}, FechaOrden={self.FechaOrden}, Total={self.Total})>"

# Tabla detalle ordenes
class DetalleOrdenes(Base):
    __tablename__ = 'DetalleOrdenes'
    DetalleID = Column(Integer, primary_key=True, autoincrement=True)
    OrdenID = Column(Integer, ForeignKey('Ordenes.OrdenID'), nullable=False)
    ProductoID = Column(Integer, ForeignKey('Productos.ProductoID'), nullable=False)
    Cantidad = Column(Integer, nullable=False)
    PrecioUnitario = Column(Numeric(10, 2), nullable=False)

    orden = relationship("Ordenes", back_populates="detalle")
    producto = relationship("Productos", back_populates="detalle")

    def __repr__(self):
        return f"<detalleorden(DetalleID={self.DetalleID}, Cantidad={self.Cantidad}, PrecioUnitario={self.PrecioUnitario})>"

# Tabla direcciones de envio
class DireccionesEnvio(Base):
    __tablename__ = 'DireccionesEnvio'
    DireccionID = Column(Integer, primary_key=True, autoincrement=True)
    UsuarioID = Column(Integer, ForeignKey('Usuarios.UsuarioID'), nullable=False)
    Calle = Column(String(255), nullable=False)
    Ciudad = Column(String(100), nullable=False)
    Departamento = Column(String(100))
    Provincia = Column(String(100))
    Distrito = Column(String(100))
    Estado = Column(String(100))
    CodigoPostal = Column(String(20))
    Pais = Column(String(100), nullable=False)

    usuario = relationship("Usuarios", back_populates="direcciones")

    def __repr__(self):
        return f"<direccionenvio(DireccionID={self.DireccionID}, UsuarioID={self.UsuarioID}, Calle={self.Calle}, Ciudad={self.Ciudad}, Pais={self.Pais})>"

# Tabla carrito de compras
class Carrito(Base):
    __tablename__ = 'Carrito'
    CarritoID = Column(Integer, primary_key=True, autoincrement=True)
    UsuarioID = Column(Integer, ForeignKey('Usuarios.UsuarioID'), nullable=False)
    ProductoID = Column(Integer, ForeignKey('Productos.ProductoID'), nullable=False)
    Cantidad = Column(Integer, nullable=False)
    FechaAgregado = Column(DateTime, default=func.now())

    usuario = relationship("Usuarios", back_populates="carrito")
    producto = relationship("Productos", back_populates="carrito")

    def __repr__(self):
        return f"<carrito(CarritoID={self.CarritoID}, Cantidad={self.Cantidad}, FechaAgregado={self.FechaAgregado})>"

# Tabla metodos de pago
class MetodosPago(Base):
    __tablename__ = 'MetodosPago'
    MetodoPagoID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(255), nullable=False)

    orden_metodo_pago = relationship("OrdenesMetodosPago", back_populates="metodo_pago")
    historial_pago = relationship("HistorialPagos", back_populates="metodo_pago")

    def __repr__(self):
        return f"<metodopago(MetodoPagoID={self.MetodoPagoID}, Nombre={self.Nombre})>"

# Tabla ordenes metodos de pago
class OrdenesMetodosPago(Base):
    __tablename__ = 'OrdenesMetodosPago'
    OrdenMetodoID = Column(Integer, primary_key=True, autoincrement=True)
    OrdenID = Column(Integer, ForeignKey('Ordenes.OrdenID'), nullable=False)
    MetodoPagoID = Column(Integer, ForeignKey('MetodosPago.MetodoPagoID'), nullable=False)
    MontoPagado = Column(Numeric(10, 2), nullable=False)

    orden = relationship("Ordenes", back_populates="orden_metodo_pago")
    metodo_pago = relationship("MetodosPago", back_populates="orden_metodo_pago")

    def __repr__(self):
        return f"<ordenmetodopago(OrdenMetodoID={self.OrdenMetodoID}, MontoPagado={self.MontoPagado})>"

# Tabla reseñas productos
class ReseñasProductos(Base):
    __tablename__ = 'ReseñasProductos'
    ReseñaID = Column(Integer, primary_key=True, autoincrement=True)
    UsuarioID = Column(Integer, ForeignKey('Usuarios.UsuarioID'), nullable=False)
    ProductoID = Column(Integer, ForeignKey('Productos.ProductoID'), nullable=False)
    Calificacion = Column(Integer, nullable=False)
    Comentario = Column(Text)
    Fecha = Column(DateTime, default=func.now())

    usuario = relationship("Usuarios", back_populates="resenas_productos")
    producto = relationship("Productos", back_populates="resenas_productos")

    def __repr__(self):
        return f"<reseñaproductos(ReseñaID={self.ReseñaID}, Calificacion={self.Calificacion})>"

# Tabla historial pagos
class HistorialPagos(Base):
    __tablename__ = 'HistorialPagos'
    PagoID = Column(Integer, primary_key=True, autoincrement=True)
    OrdenID = Column(Integer, ForeignKey('Ordenes.OrdenID'), nullable=False)
    MetodoPagoID = Column(Integer, ForeignKey('MetodosPago.MetodoPagoID'), nullable=False)
    Monto = Column(Numeric(10, 2), nullable=False)
    FechaPago = Column(DateTime, default=func.now())
    EstadoPago = Column(String(100), default='Procesando', nullable=False)

    orden = relationship("Ordenes", back_populates="historial_pago")
    metodo_pago = relationship("MetodosPago", back_populates="historial_pago")

    def __repr__(self):
        return f"<historialpago(PagoID={self.PagoID}, Monto={self.Monto}, EstadoPago={self.EstadoPago})>"


