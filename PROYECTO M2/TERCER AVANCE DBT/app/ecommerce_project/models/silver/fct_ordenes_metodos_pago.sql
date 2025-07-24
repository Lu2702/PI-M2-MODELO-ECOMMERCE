{{ config(materialized='table') }}
SELECT
    "OrdenMetodoID",
    "OrdenID",
    "MetodoPagoID",
    "MontoPagado",
    CASE WHEN "MontoPagado" > 0 THEN 1 ELSE 0 END AS "PagoRealizado"
FROM {{ ref('stg_ordenes_metodos_pago') }}
