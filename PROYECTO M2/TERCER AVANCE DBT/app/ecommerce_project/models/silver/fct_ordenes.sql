{{ config(materialized='table') }}
SELECT
    "OrdenID",
    "UsuarioID",
    "FechaOrden",
    "Total",
    "Estado",
    CASE WHEN "Estado" = 'Cancelado' THEN 1 ELSE 0 END AS "EsCancelada"
FROM {{ ref('stg_ordenes') }}