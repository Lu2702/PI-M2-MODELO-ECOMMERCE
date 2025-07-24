{{ config(materialized='view') }}
SELECT
  "ProductoID",
  "Nombre",
  "Descripcion",
  "Precio",
  "Stock",
  "CategoriaID"
FROM {{ source('src', 'Productos') }}