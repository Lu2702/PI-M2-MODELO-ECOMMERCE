{{ config(materialized='table') }}

SELECT
    o."UsuarioID",
    u."Nombre",
    u."Apellido",
    SUM(mp."MontoPagado") AS "IngresoTotal"
FROM {{ ref('fct_ordenes') }} o
JOIN {{ ref('fct_ordenes_metodos_pago') }} mp
  ON o."OrdenID" = mp."OrdenID"
JOIN {{ ref('dim_usuarios') }} u
  ON o."UsuarioID" = u."UsuarioID"
WHERE o."Estado" IN ('Completado', 'Enviado')
GROUP BY o."UsuarioID", u."Nombre", u."Apellido"
ORDER BY "IngresoTotal" DESC
LIMIT 5