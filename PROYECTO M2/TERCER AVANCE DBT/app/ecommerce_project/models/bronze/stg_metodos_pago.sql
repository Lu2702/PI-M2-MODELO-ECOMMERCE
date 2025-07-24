{{ config(materialized='view') }}
SELECT
  "MetodoPagoID",
  "Nombre",
  "Descripcion"
FROM {{ source('src', 'MetodosPago') }}