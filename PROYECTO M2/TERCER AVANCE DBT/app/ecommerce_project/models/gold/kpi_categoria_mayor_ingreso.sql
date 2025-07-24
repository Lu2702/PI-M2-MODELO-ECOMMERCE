{{ config(materialized='table') }}

SELECT
    p."CategoriaID",
    c."Nombre" AS "NombreCategoria",
    SUM(det."TotalOrden") AS "IngresoTotal"
FROM {{ ref('fct_detalleordenes') }} det
JOIN {{ ref('dim_productos') }} p
  ON det."ProductoID" = p."ProductoID"
JOIN {{ ref('dim_categorias') }} c
  ON p."CategoriaID" = c."CategoriaID"
JOIN {{ ref('fct_ordenes') }} o
  ON det."OrdenID" = o."OrdenID"
WHERE o."Estado" IN ('Completado', 'Enviado')
GROUP BY p."CategoriaID", c."Nombre"
ORDER BY "IngresoTotal" DESC
LIMIT 5