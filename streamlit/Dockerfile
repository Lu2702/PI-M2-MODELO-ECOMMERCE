# Usa una imagen oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia primero el archivo de dependencias
COPY requirements.txt .

# Instala dependencias necesarias (incluye timeout extendido)
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Expone el puerto que usa Streamlit por defecto
EXPOSE 8501

# Comando por defecto para ejecutar la app de Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]