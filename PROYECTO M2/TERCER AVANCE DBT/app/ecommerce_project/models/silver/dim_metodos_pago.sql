{{ config(materialized='table') }}

SELECT
    {{ dbt_utils.generate_surrogate_key(['"MetodoPagoID"']) }} AS "MetodoPagoSK",
    "MetodoPagoID",
    "Nombre",
    "Descripcion",
    current_timestamp AS "FechaInicio",
    NULL AS "FechaFin",
    true AS "Activo"
FROM {{ ref('stg_metodos_pago') }}