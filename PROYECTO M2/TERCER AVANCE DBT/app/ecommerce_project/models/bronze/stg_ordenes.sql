{{ config(materialized='view') }}
SELECT
  "OrdenID",
  "UsuarioID",
  "FechaOrden",
  "Total",
  "Estado"
FROM {{ source('src', 'Ordenes') }}