{{ config(materialized='view') }}
SELECT
  "CategoriaID",
  "Nombre",
  "Descripcion"
FROM {{ source('src', 'Categorias') }}