{{ config(materialized='view') }}
SELECT
  "OrdenMetodoID",
  "OrdenID",
  "MetodoPagoID",
  "MontoPagado"
FROM {{ source('src', 'OrdenesMetodosPago') }}
