{{ config(materialized='table') }}

SELECT
  "CategoriaID",
  "Nombre",
  "Descripcion"
FROM {{ ref('stg_categorias') }}