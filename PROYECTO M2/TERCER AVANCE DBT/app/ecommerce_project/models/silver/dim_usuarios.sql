{{ config(materialized='table') }}

SELECT
    {{ dbt_utils.generate_surrogate_key(['"UsuarioID"']) }} AS "UsuarioSK",
    "UsuarioID",
    "Nombre",
    "Apellido",
    "dni",
    "Email",
    "Contraseña",
    "FechaRegistro",
    current_timestamp AS "FechaInicio",
    NULL AS "FechaFin",
    true AS "Activo"
FROM {{ ref('stg_usuarios') }}