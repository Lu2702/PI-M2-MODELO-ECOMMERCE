{{ config(materialized='table') }}

SELECT
    {{ dbt_utils.generate_surrogate_key(['"ProductoID"']) }} AS "ProductoSK",
    "ProductoID",
    "Nombre",
    "Descripcion",
    "Precio",
    "Stock",
    "CategoriaID",
    current_timestamp AS "FechaInicio",
    NULL AS "FechaFin",
    true AS "Activo"
FROM {{ ref('stg_productos') }}