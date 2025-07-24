{{ config(materialized='table') }}
SELECT
    "DetalleID",
    "OrdenID",
    "ProductoID",
    "Cantidad",
    "PrecioUnitario",
    "Cantidad" * "PrecioUnitario" AS "TotalOrden"
FROM {{ ref('stg_detalleordenes') }}