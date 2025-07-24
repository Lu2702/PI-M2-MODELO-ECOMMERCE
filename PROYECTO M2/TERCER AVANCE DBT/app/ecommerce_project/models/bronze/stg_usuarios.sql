{{ config(materialized='view') }}
SELECT
  "UsuarioID",
  "FechaRegistro",
  "Nombre",
  "Apellido",
  "dni",
  "Email",
  "Contraseña"
FROM {{ source('src', 'Usuarios') }}