# Usa una imagen de Python como base
FROM python:3.10

# Instala dbt para PostgreSQL
RUN pip install dbt-postgres

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app