import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# Conexión a PostgreSQL
conn = psycopg2.connect(
    host="db",                # nombre del servicio en docker-compose
    database="EcommerceDB",   
    user="admin",          # o tu usuario real
    password="admin123"       # o tu contraseña real
)

# Configuración general de la app
st.set_page_config(page_title="Dashboard de KPIs", layout="wide")
st.title("📊 Dashboard de KPIs - DBT + Streamlit")
st.markdown("---")

# Función para cargar datos desde una tabla
def cargar_tabla(nombre_tabla):
    return pd.read_sql(f'SELECT * FROM public."{nombre_tabla}"', conn)

# --- KPI 1: Categoría con Mayor Ingreso ---
st.subheader("🏆 Categoría con Mayor Ingreso")
df_cat = cargar_tabla("kpi_categoria_mayor_ingreso")
st.dataframe(df_cat, use_container_width=True)
fig1 = px.bar(df_cat, x="NombreCategoria", y="IngresoTotal", title="Ingreso por Categoría")
st.plotly_chart(fig1, use_container_width=True)
st.markdown("---")

# --- KPI 2: Ingresos Mensuales ---
st.subheader("📅 Ingresos Mensuales")
df_ing = cargar_tabla("kpi_ingresos_mensuales")
st.dataframe(df_ing, use_container_width=True)

fig2 = px.line(df_ing, x="mes", y=["IngresoMensual", "IngresoAcumulado"],
               title="Ingresos Totales por Mes y Acumulados")
fig2.update_layout(yaxis_title="Monto en $", legend_title="Tipo de Ingreso")
st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")

# --- KPI 3: Tasa de Cancelación ---
st.subheader("❌ Tasa de Cancelación")
df_cancel = cargar_tabla("kpi_tasa_cancelacion")
st.dataframe(df_cancel, use_container_width=True)

# Extraer los valores correctamente respetando las mayúsculas
total_canceladas = df_cancel['TotalCanceladas'][0]
total_ordenes = df_cancel['TotalOrdenes'][0]
total_completadas = total_ordenes - total_canceladas

# Crear gráfico de pastel
fig3 = px.pie(
    names=["Canceladas", "Completadas"],
    values=[total_canceladas, total_completadas],
    title="Órdenes Canceladas vs Completadas"
)
st.plotly_chart(fig3, use_container_width=True)
st.markdown("---")

# --- KPI 4: Tasa de Conversión desde el Carrito ---
st.subheader("🛒 Tasa de Conversión desde el Carrito")
df_conv = cargar_tabla("kpi_tasa_conversion_carrito")
st.dataframe(df_conv, use_container_width=True)

# Crear gráfico de barras con tres categorías
fig4 = px.bar(
    x=["Usuarios con Carrito", "Usuarios con Compra", "Tasa de Conversión"],
    y=[df_conv["UsuariosConCarrito"][0], df_conv["UsuariosConCompra"][0], df_conv["TasaConversion"][0] * 100],
    labels={"x": "Métrica", "y": "Valor"},
    title="Tasa de Conversión desde el Carrito (%)"
)
fig4.update_traces(texttemplate='%{y:.2f}', textposition='outside')
fig4.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig4, use_container_width=True)
st.markdown("---")

# --- KPI 5: Usuario con Mayor Ingreso ---
st.subheader("👤 Usuario con Mayor Ingreso")
df_user = cargar_tabla("kpi_usuario_mayor_ingreso")
st.dataframe(df_user, use_container_width=True)

# Crear columna con nombre completo
df_user["NombreCompleto"] = df_user["Nombre"] + " " + df_user["Apellido"]

# Gráfico de barras por nombre completo
fig5 = px.bar(
    df_user,
    x="NombreCompleto",
    y="IngresoTotal",
    title="Usuarios con Mayor Ingreso",
    labels={"IngresoTotal": "Ingreso Total", "NombreCompleto": "Usuario"}
)
fig5.update_traces(texttemplate='%{y:.2f}', textposition='outside')
fig5.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig5, use_container_width=True)
