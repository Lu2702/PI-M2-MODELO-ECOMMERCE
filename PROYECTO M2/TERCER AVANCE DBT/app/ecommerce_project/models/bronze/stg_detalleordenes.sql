{{ config(materialized='view') }}
SELECT
  "DetalleID",
  "OrdenID",
  "ProductoID",
  "Cantidad",
  "PrecioUnitario"
FROM {{ source('src', 'DetalleOrdenes') }}