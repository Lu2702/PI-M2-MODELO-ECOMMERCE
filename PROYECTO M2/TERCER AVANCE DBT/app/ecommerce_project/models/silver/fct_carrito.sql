{{ config(materialized='table') }}
SELECT
    "CarritoID",
    "UsuarioID",
    "ProductoID",
    "Cantidad", 
    "FechaAgregado"
FROM {{ ref('stg_carrito') }}