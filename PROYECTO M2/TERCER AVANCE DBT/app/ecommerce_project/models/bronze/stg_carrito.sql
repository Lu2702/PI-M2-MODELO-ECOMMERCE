{{ config(materialized='view') }}
SELECT
  "CarritoID",
  "UsuarioID",
  "ProductoID",
  "Cantidad",
  "FechaAgregado"
FROM {{ source('src', 'Carrito') }}